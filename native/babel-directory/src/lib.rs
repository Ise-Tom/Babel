//! Bounded identity and schema primitives for a single disposable synthetic directory.
#![forbid(unsafe_code)]

use std::{collections::BTreeMap, fmt};

mod identity;
mod schema;

pub use identity::{DomainSid, Guid, Identity, Sid};
pub use schema::{DistinguishedName, NAMING_CONTEXT, ObjectClass, SCHEMA_PROFILE};

use schema::{Field, Value, validate_attributes};

pub const MAX_ENTRIES: usize = 1024;
const FIRST_RID: u32 = 1000;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DirectoryError {
    InvalidDn,
    OutsideNamingContext,
    InvalidClass,
    UnknownAttribute,
    ManagedAttribute,
    AttributeNotAllowed,
    TooManyAttributes,
    DuplicateAttribute,
    MissingAttribute,
    InvalidAttributeSyntax,
    UnsupportedMatchingRule,
    NameCollision,
    EntryNotFound,
    CapacityExceeded,
    IdentitySourceUnavailable,
    IdentityCollision,
}

impl fmt::Display for DirectoryError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self {
            Self::InvalidDn => "invalid synthetic distinguished name",
            Self::OutsideNamingContext => "name is outside the synthetic naming context",
            Self::InvalidClass => "unsupported object class",
            Self::UnknownAttribute => "unknown synthetic attribute",
            Self::ManagedAttribute => "attribute is managed by the directory",
            Self::AttributeNotAllowed => "attribute is not allowed on this class",
            Self::TooManyAttributes => "attribute count exceeds the synthetic profile limit",
            Self::DuplicateAttribute => "attribute appears more than once",
            Self::MissingAttribute => "required class attribute is missing",
            Self::InvalidAttributeSyntax => "value is outside the synthetic attribute syntax",
            Self::UnsupportedMatchingRule => "matching rule is unsupported for this attribute",
            Self::NameCollision => "name belongs to an existing object",
            Self::EntryNotFound => "object does not exist",
            Self::CapacityExceeded => "synthetic directory is full",
            Self::IdentitySourceUnavailable => "identity source is unavailable",
            Self::IdentityCollision => "generated identifier is already in use",
        })
    }
}

impl std::error::Error for DirectoryError {}

/// A read-only entry. Caller-provided values keep their display spelling.
#[derive(Debug)]
pub struct Entry {
    identity: Identity,
    dn: DistinguishedName,
    class: ObjectClass,
    attributes: BTreeMap<Field, Value>,
}

impl Entry {
    pub fn identity(&self) -> Identity {
        self.identity
    }

    pub fn dn(&self) -> &DistinguishedName {
        &self.dn
    }

    pub fn object_class(&self) -> ObjectClass {
        self.class
    }

    pub fn attribute(&self, name: &str) -> Option<&str> {
        match Field::parse(name).ok()? {
            Field::CommonName => Some(self.dn.common_name()),
            field => self
                .attributes
                .get(&field)
                .map(|value| value.display.as_str()),
        }
    }

    fn comparison_key(&self, field: Field) -> Option<&str> {
        match field {
            Field::CommonName => Some(self.dn.key()),
            field => self.attributes.get(&field).map(|value| value.key.as_str()),
        }
    }
}

/// A new directory instance owns one fresh synthetic domain and its RID sequence.
/// Exclusive mutable access serializes changes to its entries and indexes.
pub struct Directory {
    domain: DomainSid,
    next_rid: u32,
    entries: BTreeMap<Guid, Entry>,
    names: BTreeMap<String, Guid>,
    sids: BTreeMap<Sid, Guid>,
}

impl Directory {
    pub fn new() -> Result<Self, DirectoryError> {
        Ok(Self {
            domain: DomainSid::allocate()?,
            next_rid: FIRST_RID,
            entries: BTreeMap::new(),
            names: BTreeMap::new(),
            sids: BTreeMap::new(),
        })
    }

    pub fn domain_sid(&self) -> DomainSid {
        self.domain
    }

    /// Create an entry under the declared schema and reserve its name and identifiers.
    /// CN comes from the DN. All other accepted input attributes are single-valued.
    pub fn create(
        &mut self,
        dn: &str,
        object_class: &str,
        attributes: &[(&str, &str)],
    ) -> Result<Identity, DirectoryError> {
        self.create_with(dn, object_class, attributes, Guid::allocate)
    }

    fn create_with(
        &mut self,
        dn: &str,
        object_class: &str,
        attributes: &[(&str, &str)],
        allocate_guid: impl FnOnce() -> Result<Guid, DirectoryError>,
    ) -> Result<Identity, DirectoryError> {
        let dn = DistinguishedName::parse(dn)?;
        let class = ObjectClass::parse(object_class)?;
        let attributes = validate_attributes(class, attributes)?;
        if self.names.contains_key(dn.key()) {
            return Err(DirectoryError::NameCollision);
        }
        if self.entries.len() >= MAX_ENTRIES {
            return Err(DirectoryError::CapacityExceeded);
        }
        let guid = allocate_guid()?;
        if self.entries.contains_key(&guid) {
            return Err(DirectoryError::IdentityCollision);
        }

        // Run every fallible validation before publishing any index entry.
        let sid = Sid::new(self.domain, self.next_rid);
        let identity = Identity { guid, sid };
        self.names.insert(dn.key().to_owned(), guid);
        self.sids.insert(sid, guid);
        self.entries.insert(
            guid,
            Entry {
                identity,
                dn,
                class,
                attributes,
            },
        );
        self.next_rid += 1; // At most MAX_ENTRIES allocations are possible in this instance.
        Ok(identity)
    }

    pub fn lookup_dn(&self, dn: &str) -> Result<Option<&Entry>, DirectoryError> {
        let dn = DistinguishedName::parse(dn)?;
        Ok(self
            .names
            .get(dn.key())
            .and_then(|guid| self.lookup_guid(*guid)))
    }

    pub fn lookup_guid(&self, guid: Guid) -> Option<&Entry> {
        self.entries.get(&guid)
    }

    pub fn lookup_sid(&self, sid: Sid) -> Option<&Entry> {
        self.sids.get(&sid).and_then(|guid| self.lookup_guid(*guid))
    }

    /// Evaluate the selected field's exact synthetic equality rule.
    /// Result order is internal and carries no protocol or replication semantics.
    pub fn lookup_equal(
        &self,
        attribute: &str,
        rule: &str,
        assertion: &str,
    ) -> Result<Vec<&Entry>, DirectoryError> {
        let field = Field::parse(attribute)?;
        if rule != field.matching_rule() {
            return Err(DirectoryError::UnsupportedMatchingRule);
        }
        let key = field.comparison_key(assertion)?;
        Ok(self
            .entries
            .values()
            .filter(|entry| entry.comparison_key(field) == Some(key.as_str()))
            .collect())
    }

    /// Rename a leaf in the same synthetic naming context. Its identity is immutable.
    pub fn rename(&mut self, guid: Guid, destination: &str) -> Result<(), DirectoryError> {
        let dn = DistinguishedName::parse(destination)?;
        let entry = self
            .entries
            .get_mut(&guid)
            .ok_or(DirectoryError::EntryNotFound)?;
        if self.names.get(dn.key()).is_some_and(|&other| other != guid) {
            return Err(DirectoryError::NameCollision);
        }
        if entry.dn.key() != dn.key() {
            self.names.remove(entry.dn.key());
            self.names.insert(dn.key().to_owned(), guid);
        }
        entry.dn = dn;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identifier_allocation_failures_leave_name_and_rid_available() {
        let mut directory = Directory::new().unwrap();
        let first = directory
            .create("CN=First,DC=babel,DC=test", "group", &[])
            .unwrap();
        let destination = "CN=Next,DC=babel,DC=test";
        assert_eq!(
            directory.create_with(destination, "group", &[], || Err(
                DirectoryError::IdentitySourceUnavailable
            )),
            Err(DirectoryError::IdentitySourceUnavailable),
        );
        assert_eq!(
            directory.create_with(destination, "group", &[], || Ok(first.guid)),
            Err(DirectoryError::IdentityCollision),
        );
        assert!(directory.lookup_dn(destination).unwrap().is_none());
        assert_eq!(directory.lookup_sid(first.sid).unwrap().identity(), first);
        assert_eq!(
            directory
                .create(destination, "group", &[])
                .unwrap()
                .sid
                .rid(),
            first.sid.rid() + 1
        );
    }
}

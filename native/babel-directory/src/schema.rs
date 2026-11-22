use std::{collections::BTreeMap, fmt};

use crate::DirectoryError;

pub const SCHEMA_PROFILE: &str = "babel-synthetic-directory-v1";
pub const NAMING_CONTEXT: &str = "DC=babel,DC=test";
const MAX_COMMON_NAME: usize = 64;
const MAX_ATTRIBUTES: usize = 4;

/// A single CN RDN directly below the synthetic naming context.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DistinguishedName {
    common_name: String,
    key: String,
}

impl DistinguishedName {
    pub(crate) fn parse(dn: &str) -> Result<Self, DirectoryError> {
        if dn.len() > "CN=,".len() + MAX_COMMON_NAME + NAMING_CONTEXT.len() {
            return Err(DirectoryError::InvalidDn);
        }
        let (rdn, suffix) = dn.split_once(',').ok_or(DirectoryError::InvalidDn)?;
        if !suffix.eq_ignore_ascii_case(NAMING_CONTEXT) {
            return Err(DirectoryError::OutsideNamingContext);
        }
        let (attribute, name) = rdn.split_once('=').ok_or(DirectoryError::InvalidDn)?;
        if !attribute.eq_ignore_ascii_case("cn") || !common_name(name) {
            return Err(DirectoryError::InvalidDn);
        }
        Ok(Self {
            common_name: name.to_owned(),
            key: name.to_ascii_lowercase(),
        })
    }

    pub fn common_name(&self) -> &str {
        &self.common_name
    }

    pub(crate) fn key(&self) -> &str {
        &self.key
    }
}

impl fmt::Display for DistinguishedName {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "CN={},{NAMING_CONTEXT}", self.common_name)
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ObjectClass {
    User,
    Computer,
    Group,
}

impl ObjectClass {
    pub(crate) fn parse(name: &str) -> Result<Self, DirectoryError> {
        if name.eq_ignore_ascii_case("user") {
            Ok(Self::User)
        } else if name.eq_ignore_ascii_case("computer") {
            Ok(Self::Computer)
        } else if name.eq_ignore_ascii_case("group") {
            Ok(Self::Group)
        } else {
            Err(DirectoryError::InvalidClass)
        }
    }

    fn required(self) -> &'static [Field] {
        match self {
            Self::User => &[Field::DisplayName, Field::UidNumber],
            Self::Computer => &[Field::DnsHostName],
            Self::Group => &[],
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum Field {
    CommonName,
    Description,
    DisplayName,
    DnsHostName,
    UidNumber,
}

impl Field {
    pub(crate) fn parse(name: &str) -> Result<Self, DirectoryError> {
        [
            ("cn", Self::CommonName),
            ("description", Self::Description),
            ("displayName", Self::DisplayName),
            ("dnsHostName", Self::DnsHostName),
            ("uidNumber", Self::UidNumber),
        ]
        .into_iter()
        .find_map(|(label, field)| name.eq_ignore_ascii_case(label).then_some(field))
        .ok_or(DirectoryError::UnknownAttribute)
    }

    fn equality(self) -> Equality {
        match self {
            Self::CommonName | Self::DisplayName | Self::DnsHostName => Equality::AsciiCaseIgnore,
            Self::Description => Equality::AsciiExact,
            Self::UidNumber => Equality::UnsignedInteger,
        }
    }

    pub(crate) fn matching_rule(self) -> &'static str {
        match self.equality() {
            Equality::AsciiCaseIgnore => "ascii-case-ignore",
            Equality::AsciiExact => "ascii-exact",
            Equality::UnsignedInteger => "unsigned-integer",
        }
    }

    pub(crate) fn comparison_key(self, value: &str) -> Result<String, DirectoryError> {
        let valid = match self {
            Self::CommonName => common_name(value),
            Self::Description => printable_ascii(value, 128),
            Self::DisplayName => printable_ascii(value, 64),
            Self::DnsHostName => host_name(value),
            Self::UidNumber => {
                value.len() <= 10
                    && value.bytes().all(|b| b.is_ascii_digit())
                    && (value == "0" || !value.starts_with('0'))
                    && value.parse::<u32>().is_ok()
            }
        };
        if !valid {
            return Err(DirectoryError::InvalidAttributeSyntax);
        }
        Ok(match self.equality() {
            Equality::AsciiCaseIgnore => value.to_ascii_lowercase(),
            Equality::AsciiExact | Equality::UnsignedInteger => value.to_owned(),
        })
    }
}

enum Equality {
    AsciiCaseIgnore,
    AsciiExact,
    UnsignedInteger,
}

#[derive(Debug)]
pub(crate) struct Value {
    pub(crate) display: String,
    pub(crate) key: String,
}

pub(crate) fn validate_attributes(
    class: ObjectClass,
    attributes: &[(&str, &str)],
) -> Result<BTreeMap<Field, Value>, DirectoryError> {
    if attributes.len() > MAX_ATTRIBUTES {
        return Err(DirectoryError::TooManyAttributes);
    }
    let mut validated = BTreeMap::new();
    for &(name, raw) in attributes {
        if [
            "cn",
            "distinguishedName",
            "objectClass",
            "objectGUID",
            "objectSid",
        ]
        .into_iter()
        .any(|managed| name.eq_ignore_ascii_case(managed))
        {
            return Err(DirectoryError::ManagedAttribute);
        }
        let field = Field::parse(name)?;
        if field != Field::Description && !class.required().contains(&field) {
            return Err(DirectoryError::AttributeNotAllowed);
        }
        let key = field.comparison_key(raw)?;
        if validated
            .insert(
                field,
                Value {
                    display: raw.to_owned(),
                    key,
                },
            )
            .is_some()
        {
            return Err(DirectoryError::DuplicateAttribute);
        }
    }
    if class
        .required()
        .iter()
        .any(|field| !validated.contains_key(field))
    {
        return Err(DirectoryError::MissingAttribute);
    }
    Ok(validated)
}

fn common_name(value: &str) -> bool {
    value.len() <= MAX_COMMON_NAME
        && alphanumeric_ends(value)
        && value
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || matches!(b, b' ' | b'-' | b'_'))
}

fn printable_ascii(value: &str, max_length: usize) -> bool {
    !value.is_empty()
        && value.len() <= max_length
        && value.bytes().all(|b| b == b' ' || b.is_ascii_graphic())
}

fn alphanumeric_ends(value: &str) -> bool {
    value
        .as_bytes()
        .first()
        .is_some_and(u8::is_ascii_alphanumeric)
        && value
            .as_bytes()
            .last()
            .is_some_and(u8::is_ascii_alphanumeric)
}

fn host_name(value: &str) -> bool {
    const SUFFIX: &str = ".babel.test";
    if value.len() <= SUFFIX.len() || value.len() > 253 || !value.is_ascii() {
        return false;
    }
    let suffix_start = value.len() - SUFFIX.len();
    value[suffix_start..].eq_ignore_ascii_case(SUFFIX)
        && value.split('.').all(|label| {
            label.len() <= 63
                && alphanumeric_ends(label)
                && label
                    .bytes()
                    .all(|b| b.is_ascii_alphanumeric() || b == b'-')
        })
}

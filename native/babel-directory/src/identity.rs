use std::fmt;

use crate::DirectoryError;

/// A UUIDv4 in canonical octet order. Windows wire encoding has its own conversion.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct Guid([u8; 16]);

impl Guid {
    pub(crate) fn allocate() -> Result<Self, DirectoryError> {
        let mut bytes = random_bytes()?;
        bytes[6] = (bytes[6] & 0x0f) | 0x40;
        bytes[8] = (bytes[8] & 0x3f) | 0x80;
        Ok(Self(bytes))
    }

    pub fn as_bytes(&self) -> &[u8; 16] {
        &self.0
    }
}

impl fmt::Display for Guid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for (index, byte) in self.0.iter().enumerate() {
            if matches!(index, 4 | 6 | 8 | 10) {
                f.write_str("-")?;
            }
            write!(f, "{byte:02x}")?;
        }
        Ok(())
    }
}

/// The three synthetic sub-authorities following S-1-5-21.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct DomainSid([u32; 3]);

impl DomainSid {
    pub(crate) fn allocate() -> Result<Self, DirectoryError> {
        let bytes: [u8; 12] = random_bytes()?;
        Ok(Self([
            u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]),
            u32::from_le_bytes([bytes[4], bytes[5], bytes[6], bytes[7]]),
            u32::from_le_bytes([bytes[8], bytes[9], bytes[10], bytes[11]]),
        ]))
    }

    pub fn sub_authorities(self) -> [u32; 3] {
        self.0
    }
}

impl fmt::Display for DomainSid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let [a, b, c] = self.0;
        write!(f, "S-1-5-21-{a}-{b}-{c}")
    }
}

/// An immutable object SID within the synthetic domain.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct Sid {
    domain: DomainSid,
    rid: u32,
}

impl Sid {
    pub(crate) fn new(domain: DomainSid, rid: u32) -> Self {
        Self { domain, rid }
    }

    pub fn domain(self) -> DomainSid {
        self.domain
    }

    pub fn rid(self) -> u32 {
        self.rid
    }
}

impl fmt::Display for Sid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}-{}", self.domain, self.rid)
    }
}

/// Stable identifiers allocated together by the core.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Identity {
    pub guid: Guid,
    pub sid: Sid,
}

fn random_bytes<const N: usize>() -> Result<[u8; N], DirectoryError> {
    let mut bytes = [0; N];
    getrandom::fill(&mut bytes).map_err(|_| DirectoryError::IdentitySourceUnavailable)?;
    Ok(bytes)
}

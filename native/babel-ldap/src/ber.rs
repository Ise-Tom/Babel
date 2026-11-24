use crate::{DecodeError, MAX_FRAME_BYTES};

pub(crate) struct Cursor<'a> {
    bytes: &'a [u8],
    offset: usize,
}

impl<'a> Cursor<'a> {
    pub(crate) fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, offset: 0 }
    }

    fn byte(&mut self) -> Result<u8, DecodeError> {
        let value = *self.bytes.get(self.offset).ok_or(DecodeError::Truncated)?;
        self.offset += 1;
        Ok(value)
    }

    pub(crate) fn tlv(&mut self) -> Result<(u8, &'a [u8]), DecodeError> {
        let tag = self.byte()?;
        // The implemented LDAP subset uses only single-octet tags.
        if tag & 0x1f == 0x1f {
            return Err(DecodeError::InvalidTag);
        }
        let first = self.byte()?;
        let length = if first & 0x80 == 0 {
            usize::from(first)
        } else {
            let count = usize::from(first & 0x7f);
            if count == 0 || count > 4 {
                return Err(DecodeError::InvalidLength);
            }
            let mut length = 0usize;
            for _ in 0..count {
                length = length
                    .checked_mul(256)
                    .and_then(|n| n.checked_add(usize::from(self.byte().ok()?)))
                    .ok_or(DecodeError::InvalidLength)?;
            }
            length
        };
        if length > MAX_FRAME_BYTES {
            return Err(DecodeError::TooLarge);
        }
        let end = self
            .offset
            .checked_add(length)
            .ok_or(DecodeError::TooLarge)?;
        let value = self
            .bytes
            .get(self.offset..end)
            .ok_or(DecodeError::Truncated)?;
        self.offset = end;
        Ok((tag, value))
    }

    pub(crate) fn expect(&mut self, expected: u8) -> Result<&'a [u8], DecodeError> {
        let (tag, value) = self.tlv()?;
        if tag != expected {
            return Err(DecodeError::InvalidTag);
        }
        Ok(value)
    }

    pub(crate) fn uint(&mut self, tag: u8) -> Result<u32, DecodeError> {
        let bytes = self.expect(tag)?;
        if bytes.is_empty() || bytes.len() > 4 || bytes[0] & 0x80 != 0 {
            return Err(DecodeError::InvalidInteger);
        }
        if bytes.len() > 1 && bytes[0] == 0 && bytes[1] & 0x80 == 0 {
            return Err(DecodeError::InvalidInteger);
        }
        Ok(bytes.iter().fold(0, |n, byte| (n << 8) | u32::from(*byte)))
    }

    pub(crate) fn boolean(&mut self) -> Result<bool, DecodeError> {
        match self.expect(0x01)? {
            [0] => Ok(false),
            [0xff] => Ok(true),
            _ => Err(DecodeError::InvalidValue),
        }
    }

    pub(crate) fn finish(&self) -> Result<(), DecodeError> {
        if self.offset == self.bytes.len() {
            Ok(())
        } else {
            Err(DecodeError::TrailingData)
        }
    }

    pub(crate) fn next_tag(&self) -> Option<u8> {
        self.bytes.get(self.offset).copied()
    }

    pub(crate) fn is_empty(&self) -> bool {
        self.offset == self.bytes.len()
    }
}

pub(crate) fn tlv(tag: u8, value: &[u8]) -> Vec<u8> {
    let mut encoded = vec![tag];
    if value.len() < 128 {
        encoded.push(value.len() as u8);
    } else {
        let bytes = value.len().to_be_bytes();
        let first = bytes
            .iter()
            .position(|n| *n != 0)
            .unwrap_or(bytes.len() - 1);
        encoded.push(0x80 | (bytes.len() - first) as u8);
        encoded.extend_from_slice(&bytes[first..]);
    }
    encoded.extend_from_slice(value);
    encoded
}

pub(crate) fn uint(tag: u8, number: u32) -> Vec<u8> {
    let bytes = number.to_be_bytes();
    let start = bytes.iter().position(|n| *n != 0).unwrap_or(3);
    let mut value = Vec::new();
    if bytes[start] & 0x80 != 0 {
        value.push(0);
    }
    value.extend_from_slice(&bytes[start..]);
    tlv(tag, &value)
}

pub(crate) fn octets(value: &[u8]) -> Vec<u8> {
    tlv(0x04, value)
}

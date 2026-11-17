use crate::ber::{Cursor, octets, tlv, uint};
use crate::filter::{FilterResult, evaluate};
use crate::{MAX_ATTRIBUTE_BYTES, MAX_ATTRIBUTES, MAX_FRAME_BYTES};

/// Static error categories never contain request bytes or credentials.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DecodeError {
    Truncated,
    InvalidTag,
    InvalidLength,
    TooLarge,
    InvalidInteger,
    InvalidValue,
    TrailingData,
    UnsupportedControls,
    UnsupportedOperation,
    AttributeLimit,
    FilterLimit,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Operation {
    Bind {
        version: u32,
        anonymous: bool,
    },
    Search {
        root: bool,
        scope: u32,
        filter: FilterResult,
        types_only: bool,
        attributes: Vec<Vec<u8>>,
    },
    Unbind,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Request {
    pub message_id: u32,
    pub operation: Operation,
}

pub(crate) fn valid_attribute(name: &[u8]) -> bool {
    if matches!(name, b"*" | b"+" | b"1.1") {
        return true;
    }
    let mut parts = name.split(|byte| *byte == b';');
    let base = parts.next().unwrap_or_default();
    let descriptor = base.first().is_some_and(u8::is_ascii_alphabetic)
        && base.iter().all(|b| b.is_ascii_alphanumeric() || *b == b'-');
    let oid = base.contains(&b'.')
        && base.split(|b| *b == b'.').all(|part| {
            !part.is_empty()
                && part.iter().all(u8::is_ascii_digit)
                && (part.len() == 1 || part[0] != b'0')
        });
    (descriptor || oid)
        && parts.all(|option| {
            !option.is_empty()
                && option
                    .iter()
                    .all(|b| b.is_ascii_alphanumeric() || *b == b'-')
        })
}

/// Decode one complete, bounded LDAPMessage without recursion or credential copies.
pub fn decode(frame: &[u8]) -> Result<Request, DecodeError> {
    if frame.len() > MAX_FRAME_BYTES {
        return Err(DecodeError::TooLarge);
    }
    let mut outer = Cursor::new(frame);
    let mut message = Cursor::new(outer.expect(0x30)?);
    outer.finish()?;
    let message_id = message.uint(0x02)?;
    if message_id == 0 {
        return Err(DecodeError::InvalidInteger);
    }
    let (tag, value) = message.tlv()?;
    let mut operation = Cursor::new(value);
    let operation = match tag {
        0x60 => {
            let version = operation.uint(0x02)?;
            let dn = operation.expect(0x04)?;
            if dn.len() > 1024 {
                return Err(DecodeError::InvalidValue);
            }
            let (auth_tag, auth) = operation.tlv()?;
            if auth_tag != 0x80 && auth_tag != 0xa3 {
                return Err(DecodeError::InvalidTag);
            }
            operation.finish()?;
            Operation::Bind {
                version,
                anonymous: auth_tag == 0x80 && dn.is_empty() && auth.is_empty(),
            }
        }
        0x63 => {
            let base = operation.expect(0x04)?;
            if base.len() > 1024 {
                return Err(DecodeError::InvalidValue);
            }
            let scope = operation.uint(0x0a)?;
            let deref = operation.uint(0x0a)?;
            if scope > 2 || deref > 3 {
                return Err(DecodeError::InvalidValue);
            }
            operation.uint(0x02)?; // sizeLimit: the subset returns at most one entry.
            operation.uint(0x02)?; // timeLimit: bounded server-side independently.
            let types_only = operation.boolean()?;
            let (filter_tag, filter) = operation.tlv()?;
            let filter = evaluate(filter_tag, filter)?;
            let mut names = Cursor::new(operation.expect(0x30)?);
            let mut attributes = Vec::new();
            while !names.is_empty() {
                let name = names.expect(0x04)?;
                if name.is_empty() || name.len() > MAX_ATTRIBUTE_BYTES || !valid_attribute(name) {
                    return Err(DecodeError::InvalidValue);
                }
                if attributes.len() == MAX_ATTRIBUTES {
                    return Err(DecodeError::AttributeLimit);
                }
                attributes.push(name.to_vec());
            }
            operation.finish()?;
            Operation::Search {
                root: base.is_empty(),
                scope,
                filter,
                types_only,
                attributes,
            }
        }
        0x42 => {
            operation.finish()?;
            Operation::Unbind
        }
        _ => return Err(DecodeError::UnsupportedOperation),
    };
    if !message.is_empty() {
        let (tag, _) = message.tlv()?;
        return Err(if tag == 0xa0 {
            DecodeError::UnsupportedControls
        } else {
            DecodeError::TrailingData
        });
    }
    Ok(Request {
        message_id,
        operation,
    })
}

fn message(id: u32, tag: u8, payload: &[u8]) -> Vec<u8> {
    let mut body = uint(0x02, id);
    body.extend(tlv(tag, payload));
    tlv(0x30, &body)
}

fn result(id: u32, tag: u8, code: u32, diagnostic: &[u8]) -> Vec<u8> {
    let mut body = uint(0x0a, code);
    body.extend(octets(b"")); // matchedDN
    body.extend(octets(diagnostic));
    message(id, tag, &body)
}

fn entry(id: u32, requested: &[Vec<u8>], types_only: bool) -> Vec<u8> {
    let user_all = requested.is_empty() || requested.iter().any(|a| a == b"*");
    let operational_all = requested.iter().any(|a| a == b"+");
    let mut attributes = Vec::new();
    for (name, value, operational) in [
        (b"objectClass".as_slice(), b"top".as_slice(), false),
        (b"supportedLDAPVersion".as_slice(), b"3".as_slice(), true),
        (b"vendorName".as_slice(), b"Babel".as_slice(), true),
        (
            b"vendorVersion".as_slice(),
            concat!(env!("CARGO_PKG_VERSION"), "-lab").as_bytes(),
            true,
        ),
    ] {
        if (operational && operational_all)
            || (!operational && user_all)
            || requested.iter().any(|a| a.eq_ignore_ascii_case(name))
        {
            let mut attribute = octets(name);
            attribute.extend(tlv(
                0x31,
                &if types_only {
                    Vec::new()
                } else {
                    octets(value)
                },
            ));
            attributes.extend(tlv(0x30, &attribute));
        }
    }
    let mut body = octets(b"");
    body.extend(tlv(0x30, &attributes));
    message(id, 0x64, &body)
}

/// Return only static public lab data. No credential, account or AD-capability claims.
pub fn respond(request: &Request) -> Option<Vec<u8>> {
    match &request.operation {
        Operation::Unbind => None,
        Operation::Bind { version, anonymous } => Some(if *version != 3 {
            result(request.message_id, 0x61, 2, b"Only LDAPv3 is supported")
        } else if !anonymous {
            result(
                request.message_id,
                0x61,
                53,
                b"Credential authentication is not implemented",
            )
        } else {
            result(request.message_id, 0x61, 0, b"")
        }),
        Operation::Search {
            root,
            scope,
            filter,
            types_only,
            attributes,
        } => Some(if !root {
            result(
                request.message_id,
                0x65,
                32,
                b"Only the public lab RootDSE exists",
            )
        } else if *scope != 0 || *filter == FilterResult::Unsupported {
            result(
                request.message_id,
                0x65,
                53,
                b"Search scope or matching rule is not implemented",
            )
        } else if *filter != FilterResult::Matches {
            result(request.message_id, 0x65, 0, b"")
        } else {
            let mut output = entry(request.message_id, attributes, *types_only);
            output.extend(result(request.message_id, 0x65, 0, b""));
            output
        }),
    }
}

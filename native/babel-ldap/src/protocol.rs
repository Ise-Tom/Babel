use crate::ber::{Cursor, octets, tlv, uint};
pub use crate::controls::{COOKIE_BYTES, PageRequest, SearchControls};
use crate::filter::{FilterResult, evaluate, evaluate_with};
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
        directory: Option<DirectorySearch>,
    },
    Unbind,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Request {
    pub message_id: u32,
    pub operation: Operation,
    pub controls: SearchControls,
}

/// The alternative listener retains bounded search input for matching and cursor binding.
#[derive(Clone, PartialEq, Eq)]
pub struct DirectorySearch {
    base: Vec<u8>,
    filter: Vec<u8>,
    filter_tag: u8,
    pub deref: u32,
    pub size_limit: u32,
    time_limit: u32,
}

impl std::fmt::Debug for DirectorySearch {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str("DirectorySearch")
    }
}

impl DirectorySearch {
    pub fn base(&self) -> Result<&str, std::str::Utf8Error> {
        std::str::from_utf8(&self.base)
    }

    pub fn evaluate(
        &self,
        mut leaf: impl FnMut(&[u8], Option<&[u8]>) -> FilterResult,
    ) -> Result<FilterResult, DecodeError> {
        evaluate_with(self.filter_tag, &self.filter, &mut leaf)
    }
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
    decode_with(frame, false)
}

/// Decode in the synthetic directory listener, including bounded search controls.
pub fn decode_directory(frame: &[u8]) -> Result<Request, DecodeError> {
    decode_with(frame, true)
}

fn decode_with(frame: &[u8], directory_reads: bool) -> Result<Request, DecodeError> {
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
            let size_limit = operation.uint(0x02)?;
            let time_limit = operation.uint(0x02)?;
            let types_only = operation.boolean()?;
            let (filter_tag, filter_bytes) = operation.tlv()?;
            let filter = if directory_reads && !base.is_empty() {
                evaluate_with(filter_tag, filter_bytes, &mut |_, _| {
                    FilterResult::Undefined
                })?
            } else {
                evaluate(filter_tag, filter_bytes)?
            };
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
                directory: (directory_reads && !base.is_empty()).then(|| DirectorySearch {
                    base: base.to_vec(),
                    filter_tag,
                    filter: filter_bytes.to_vec(),
                    deref,
                    size_limit,
                    time_limit,
                }),
            }
        }
        0x42 => {
            operation.finish()?;
            Operation::Unbind
        }
        _ => return Err(DecodeError::UnsupportedOperation),
    };
    let controls = if message.is_empty() {
        SearchControls::None
    } else {
        let (tag, encoded) = message.tlv()?;
        if tag != 0xa0 {
            return Err(DecodeError::TrailingData);
        }
        if !directory_reads || !matches!(operation, Operation::Search { .. }) {
            return Err(DecodeError::UnsupportedControls);
        }
        message.finish()?;
        crate::controls::decode(encoded)?
    };
    Ok(Request {
        message_id,
        operation,
        controls,
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

/// Encode a synthetic search result. The caller supplies only approved public fields.
pub fn search_entry<'a>(
    id: u32,
    dn: &str,
    fields: impl IntoIterator<Item = (&'a str, &'a str, bool)>,
    requested: &[Vec<u8>],
    types_only: bool,
) -> Vec<u8> {
    let user_all = requested.is_empty() || requested.iter().any(|a| a == b"*");
    let operational_all = requested.iter().any(|a| a == b"+");
    let mut attributes = Vec::new();
    for (name, value, operational) in fields {
        if (operational && operational_all)
            || (!operational && user_all)
            || requested
                .iter()
                .any(|a| a.eq_ignore_ascii_case(name.as_bytes()))
        {
            let mut attribute = octets(name.as_bytes());
            let values = if types_only {
                Vec::new()
            } else {
                octets(value.as_bytes())
            };
            attribute.extend(tlv(0x31, &values));
            attributes.extend(tlv(0x30, &attribute));
        }
    }
    let mut body = octets(dn.as_bytes());
    body.extend(tlv(0x30, &attributes));
    message(id, 0x64, &body)
}

pub fn search_done(
    id: u32,
    code: u32,
    matched_dn: &str,
    diagnostic: &[u8],
    page_cookie: Option<&[u8]>,
) -> Vec<u8> {
    let mut payload = uint(0x0a, code);
    payload.extend(octets(matched_dn.as_bytes()));
    payload.extend(octets(diagnostic));
    let mut body = uint(0x02, id);
    body.extend(tlv(0x65, &payload));
    if let Some(cookie) = page_cookie {
        body.extend(crate::controls::response(cookie));
    }
    tlv(0x30, &body)
}

fn root_entry(id: u32, attributes: &[Vec<u8>], types_only: bool) -> Vec<u8> {
    search_entry(
        id,
        "",
        [
            ("objectClass", "top", false),
            ("supportedLDAPVersion", "3", true),
            ("vendorName", "Babel", true),
            (
                "vendorVersion",
                concat!(env!("CARGO_PKG_VERSION"), "-lab"),
                true,
            ),
        ],
        attributes,
        types_only,
    )
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
            ..
        } => Some(if request.controls == SearchControls::Invalid {
            result(request.message_id, 0x65, 2, b"Invalid search controls")
        } else if matches!(
            request.controls,
            SearchControls::Unavailable | SearchControls::Page(PageRequest { critical: true, .. })
        ) {
            result(
                request.message_id,
                0x65,
                12,
                b"Requested critical control is unavailable",
            )
        } else if !root {
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
            let mut output = root_entry(request.message_id, attributes, *types_only);
            output.extend(result(request.message_id, 0x65, 0, b""));
            output
        }),
    }
}

use crate::DecodeError;
use crate::ber::{Cursor, octets, tlv, uint};

const PAGED_RESULTS: &[u8] = b"1.2.840.113556.1.4.319";
const MAX_CONTROLS: usize = 8;
pub const COOKIE_BYTES: usize = 16;

#[derive(Clone, PartialEq, Eq)]
pub struct PageRequest {
    pub size: u32,
    pub cookie: Vec<u8>,
    pub critical: bool,
}

#[derive(Clone, PartialEq, Eq)]
pub enum SearchControls {
    None,
    Page(PageRequest),
    Unavailable,
    Invalid,
}

impl std::fmt::Debug for SearchControls {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(match self {
            Self::None => "None",
            Self::Page(_) => "Page",
            Self::Unavailable => "Unavailable",
            Self::Invalid => "Invalid",
        })
    }
}

fn page(value: &[u8], critical: bool) -> Result<PageRequest, DecodeError> {
    let mut outer = Cursor::new(value);
    let mut inner = Cursor::new(outer.expect(0x30)?);
    outer.finish()?;
    let size = inner.uint(0x02)?;
    let cookie = inner.expect(0x04)?;
    inner.finish()?;
    if cookie.len() > COOKIE_BYTES {
        return Err(DecodeError::InvalidValue);
    }
    Ok(PageRequest {
        size,
        cookie: cookie.to_vec(),
        critical,
    })
}

pub(crate) fn decode(bytes: &[u8]) -> Result<SearchControls, DecodeError> {
    let mut controls = Cursor::new(bytes);
    if controls.is_empty() {
        return Ok(SearchControls::Invalid);
    }
    let mut paging = None;
    let mut unavailable = false;
    for _ in 0..MAX_CONTROLS {
        let mut control = Cursor::new(controls.expect(0x30)?);
        let id = control.expect(0x04)?;
        let (critical, value) = match control.next_tag() {
            Some(0x01) => {
                let critical = control.boolean()?;
                let value = if control.is_empty() {
                    None
                } else {
                    Some(control.expect(0x04)?)
                };
                (critical, value)
            }
            Some(_) => (false, Some(control.expect(0x04)?)),
            None => (false, None),
        };
        control.finish()?;

        if id == PAGED_RESULTS {
            let Some(request) = value.and_then(|value| page(value, critical).ok()) else {
                return Ok(SearchControls::Invalid);
            };
            if paging.replace(request).is_some() {
                return Ok(SearchControls::Invalid);
            }
        } else {
            unavailable |= critical;
        }
        if controls.is_empty() {
            return Ok(if unavailable {
                SearchControls::Unavailable
            } else {
                paging.map_or(SearchControls::None, SearchControls::Page)
            });
        }
    }
    Ok(SearchControls::Invalid)
}

pub(crate) fn response(cookie: &[u8]) -> Vec<u8> {
    let mut value = uint(0x02, 0); // RFC 2696 permits zero when no estimate is supplied.
    value.extend(octets(cookie));
    let mut control = octets(PAGED_RESULTS);
    control.extend(octets(&tlv(0x30, &value)));
    tlv(0xa0, &tlv(0x30, &control))
}

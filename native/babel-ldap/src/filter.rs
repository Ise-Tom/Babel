//! Bounded, allocation-free LDAP filter traversal and synthetic RootDSE matching.
use crate::ber::Cursor;
use crate::protocol::valid_attribute;
use crate::{DecodeError, MAX_ATTRIBUTE_BYTES};

pub const MAX_FILTER_DEPTH: usize = 8;
pub const MAX_FILTER_NODES: usize = 64;
pub const MAX_ASSERTION_BYTES: usize = 256;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FilterResult {
    Matches,
    NoMatch,
    Undefined,
    Unsupported,
}

impl FilterResult {
    fn combine(self, other: Self, and: bool) -> Self {
        use FilterResult::*;
        match (self, other) {
            (Unsupported, _) | (_, Unsupported) => Unsupported,
            (NoMatch, _) | (_, NoMatch) if and => NoMatch,
            (Matches, _) | (_, Matches) if !and => Matches,
            (Undefined, _) | (_, Undefined) => Undefined,
            _ => other,
        }
    }
}

fn attribute(name: &[u8]) -> Result<(), DecodeError> {
    if name.is_empty()
        || name.len() > MAX_ATTRIBUTE_BYTES
        || matches!(name, b"*" | b"+")
        || !valid_attribute(name)
    {
        return Err(DecodeError::InvalidValue);
    }
    Ok(())
}

fn object_class(name: &[u8]) -> bool {
    name.eq_ignore_ascii_case(b"objectClass") || name == b"2.5.4.0"
}

fn present(name: &[u8]) -> FilterResult {
    if object_class(name)
        || [
            b"supportedLDAPVersion".as_slice(),
            b"vendorName",
            b"vendorVersion",
        ]
        .iter()
        .any(|known| name.eq_ignore_ascii_case(known))
    {
        FilterResult::Matches
    } else {
        // Unknown schema/options must not become a match when negated.
        FilterResult::Undefined
    }
}

pub(crate) fn evaluate(tag: u8, value: &[u8]) -> Result<FilterResult, DecodeError> {
    evaluate_with(tag, value, &mut root_leaf)
}

fn root_leaf(name: &[u8], assertion: Option<&[u8]>) -> FilterResult {
    use FilterResult::*;
    let Some(assertion) = assertion else {
        return present(name);
    };
    if !object_class(name) {
        return if present(name) == Undefined {
            Undefined
        } else {
            Unsupported
        };
    }
    if assertion.contains(&b';') || matches!(assertion, b"*" | b"+") || !valid_attribute(assertion)
    {
        return Undefined;
    }
    if assertion.eq_ignore_ascii_case(b"top") || assertion == b"2.5.6.0" {
        Matches
    } else {
        NoMatch
    }
}

pub(crate) fn evaluate_with(
    tag: u8,
    value: &[u8],
    leaf: &mut impl FnMut(&[u8], Option<&[u8]>) -> FilterResult,
) -> Result<FilterResult, DecodeError> {
    let mut remaining = MAX_FILTER_NODES;
    evaluate_node(tag, value, 1, &mut remaining, leaf)
}

fn evaluate_node(
    tag: u8,
    value: &[u8],
    depth: usize,
    remaining: &mut usize,
    leaf: &mut impl FnMut(&[u8], Option<&[u8]>) -> FilterResult,
) -> Result<FilterResult, DecodeError> {
    use FilterResult::*;
    if depth > MAX_FILTER_DEPTH || *remaining == 0 {
        return Err(DecodeError::FilterLimit);
    }
    *remaining -= 1;
    let mut cursor = Cursor::new(value);
    match tag {
        0x87 => {
            attribute(value)?;
            Ok(leaf(value, None))
        }
        0xa3 => {
            let name = cursor.expect(0x04)?;
            attribute(name)?;
            let assertion = cursor.expect(0x04)?;
            if assertion.len() > MAX_ASSERTION_BYTES {
                return Err(DecodeError::FilterLimit);
            }
            cursor.finish()?;
            Ok(leaf(name, Some(assertion)))
        }
        0xa0 | 0xa1 => {
            if cursor.is_empty() {
                return Err(DecodeError::InvalidValue);
            }
            let and = tag == 0xa0;
            let mut result = if and { Matches } else { NoMatch };
            while !cursor.is_empty() {
                let (child_tag, child) = cursor.tlv()?;
                // Always inspect every branch: true/false cannot hide unsupported or invalid input.
                result = result.combine(
                    evaluate_node(child_tag, child, depth + 1, remaining, leaf)?,
                    and,
                );
            }
            Ok(result)
        }
        0xa2 => {
            let (child_tag, child) = cursor.tlv()?;
            let result = evaluate_node(child_tag, child, depth + 1, remaining, leaf)?;
            cursor.finish()?;
            Ok(match result {
                Matches => NoMatch,
                NoMatch => Matches,
                other => other,
            })
        }
        // Substring, ordering, approximate and extensible matching are not implemented.
        0xa4..=0xa6 | 0xa8 | 0xa9 => Ok(Unsupported),
        _ => Err(DecodeError::InvalidTag),
    }
}

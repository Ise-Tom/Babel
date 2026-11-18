//! Bounded fixture types; these are not AD GUID/SID allocation or name matching.
use crate::Failure;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ObjectId(u128);
impl ObjectId {
    pub fn new(value: u128) -> Result<Self, Failure> {
        if value == 0 {
            return Err(Failure::Configuration);
        }
        Ok(Self(value))
    }
    pub(crate) fn text(self) -> String {
        let s = format!("{:032x}", self.0);
        format!(
            "{}-{}-{}-{}-{}",
            &s[..8],
            &s[8..12],
            &s[12..16],
            &s[16..20],
            &s[20..]
        )
    }
}
#[derive(Clone)]
pub struct Mutation {
    pub(crate) actor: ObjectId,
    pub(crate) request: ObjectId,
    pub(crate) object: ObjectId,
    pub(crate) rid: u32,
    pub(crate) label: String,
    pub(crate) operation: &'static str,
    pub(crate) expected: i64,
}
impl Mutation {
    pub fn create(
        actor: ObjectId,
        request: ObjectId,
        object: ObjectId,
        rid: u32,
        label: &str,
    ) -> Result<Self, Failure> {
        if !(1000..=999_999_999).contains(&rid)
            || label.is_empty()
            || label.len() > 32
            || !label.as_bytes()[0].is_ascii_lowercase()
            || !label
                .bytes()
                .all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == b'-')
        {
            return Err(Failure::Configuration);
        }
        Ok(Self {
            actor,
            request,
            object,
            rid,
            label: label.to_owned(),
            operation: "create",
            expected: 0,
        })
    }
    pub fn rename(
        actor: ObjectId,
        request: ObjectId,
        object: ObjectId,
        rid: u32,
        label: &str,
        expected: i64,
    ) -> Result<Self, Failure> {
        let mut value = Self::create(actor, request, object, rid, label)?;
        if expected <= 0 {
            return Err(Failure::Configuration);
        }
        value.operation = "rename";
        value.expected = expected;
        Ok(value)
    }
}

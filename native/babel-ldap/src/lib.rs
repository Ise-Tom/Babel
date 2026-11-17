//! Bounded, read-only LDAP RootDSE laboratory subset. Not a domain controller.
#![forbid(unsafe_code)]

mod ber;
pub mod protocol;
pub mod server;

pub use protocol::{DecodeError, Operation, Request, decode, respond};

/// Hard limit applied before allocation, including the outer BER header.
pub const MAX_FRAME_BYTES: usize = 16 * 1024;
pub const MAX_ATTRIBUTES: usize = 64;
pub const MAX_ATTRIBUTE_BYTES: usize = 64;

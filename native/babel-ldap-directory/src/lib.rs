//! Bounded anonymous LDAP reads over the accepted in-memory directory profile.

#![forbid(unsafe_code)]

use babel_directory::{Directory, DirectoryError, Entry, NAMING_CONTEXT, ObjectClass};
use babel_ldap::protocol::{
    COOKIE_BYTES, SearchControls, decode_directory, search_done, search_entry,
};
use babel_ldap::{FilterResult, Operation, Request, respond};
use std::io;
use std::net::SocketAddr;

const MAX_PAGE_SIZE: u32 = 4;
const FIELDS: [(&str, &str); 7] = [
    ("objectClass", ""),
    ("dc", ""),
    ("cn", "ascii-case-ignore"),
    ("displayName", "ascii-case-ignore"),
    ("uidNumber", "unsigned-integer"),
    ("dnsHostName", "ascii-case-ignore"),
    ("description", "ascii-exact"),
];

#[derive(Clone, Copy)]
enum Candidate<'a> {
    Context,
    Leaf(&'a Entry),
}

impl<'a> Candidate<'a> {
    fn attribute(self, name: &str) -> Option<&'a str> {
        match (self, name) {
            (Self::Context, "dc") => Some("babel"),
            (Self::Context, "objectClass") => Some("domain"),
            (Self::Context, _) => None,
            (Self::Leaf(entry), "objectClass") => Some(match entry.object_class() {
                ObjectClass::User => "user",
                ObjectClass::Computer => "computer",
                ObjectClass::Group => "group",
            }),
            (Self::Leaf(entry), _) => entry.attribute(name),
        }
    }

    fn dn(self) -> String {
        match self {
            Self::Context => NAMING_CONTEXT.to_owned(),
            Self::Leaf(entry) => entry.dn().to_string(),
        }
    }
}

#[derive(Debug, Clone, Copy)]
struct SearchError {
    code: u32,
    matched_dn: &'static str,
    diagnostic: &'static [u8],
}

impl SearchError {
    const fn new(code: u32, diagnostic: &'static [u8]) -> Self {
        Self {
            code,
            matched_dn: "",
            diagnostic,
        }
    }
}

const INVALID_DN: SearchError = SearchError::new(34, b"DN is outside the synthetic syntax");
const MISSING_BASE: SearchError = SearchError::new(32, b"Search base does not exist");
const INVALID_CURSOR: SearchError = SearchError::new(53, b"Invalid or expired paging cookie");

struct Fixture {
    directory: Directory,
}

impl Fixture {
    fn new() -> Result<Self, DirectoryError> {
        let mut directory = Directory::new()?;
        directory.create(
            "CN=Alice,DC=babel,DC=test",
            "user",
            &[
                ("displayName", "Alice Example"),
                ("uidNumber", "1001"),
                ("description", "Public fixture"),
            ],
        )?;
        directory.create(
            "CN=Bob,DC=babel,DC=test",
            "user",
            &[("displayName", "Bob Example"), ("uidNumber", "1002")],
        )?;
        directory.create(
            "CN=Readers,DC=babel,DC=test",
            "group",
            &[("description", "Synthetic group")],
        )?;
        directory.create(
            "CN=Workstation,DC=babel,DC=test",
            "computer",
            &[("dnsHostName", "workstation.babel.test")],
        )?;
        Ok(Self { directory })
    }

    fn candidates(&self, base: &str, scope: u32) -> Result<Vec<Candidate<'_>>, SearchError> {
        if base.eq_ignore_ascii_case(NAMING_CONTEXT) {
            let mut candidates = Vec::new();
            if scope != 1 {
                candidates.push(Candidate::Context);
            }
            if scope != 0 {
                candidates.extend(self.directory.entries_by_name().map(Candidate::Leaf));
            }
            return Ok(candidates);
        }
        let entry = self
            .directory
            .lookup_dn(base)
            .map_err(|error| match error {
                DirectoryError::OutsideNamingContext => MISSING_BASE,
                _ => INVALID_DN,
            })?;
        let entry = entry.ok_or(SearchError {
            matched_dn: NAMING_CONTEXT,
            ..MISSING_BASE
        })?;
        Ok(if scope == 1 {
            Vec::new()
        } else {
            vec![Candidate::Leaf(entry)]
        })
    }

    fn leaf(
        &self,
        candidate: Candidate<'_>,
        name: &[u8],
        assertion: Option<&[u8]>,
    ) -> FilterResult {
        use FilterResult::{Matches, NoMatch, Undefined};
        let name: &[u8] = if name == b"2.5.4.0" {
            b"objectClass"
        } else {
            name
        };
        let Some((field, rule)) = FIELDS
            .iter()
            .find(|(field, _)| name.eq_ignore_ascii_case(field.as_bytes()))
        else {
            return Undefined;
        };
        let value = candidate.attribute(field);
        let Some(assertion) = assertion else {
            return if value.is_some() { Matches } else { NoMatch };
        };
        let Ok(assertion) = std::str::from_utf8(assertion) else {
            return Undefined;
        };
        if rule.is_empty() {
            if assertion.is_empty()
                || !assertion
                    .bytes()
                    .all(|b| b.is_ascii_alphanumeric() || b == b'-')
            {
                return Undefined;
            }
            return if value.is_some_and(|value| value.eq_ignore_ascii_case(assertion)) {
                Matches
            } else {
                NoMatch
            };
        }
        match self.directory.lookup_equal(field, rule, assertion) {
            Ok(matches) => {
                if let Candidate::Leaf(entry) = candidate
                    && matches.iter().any(|found| std::ptr::eq(*found, entry))
                {
                    Matches
                } else {
                    NoMatch
                }
            }
            Err(_) => Undefined,
        }
    }
}

struct Cursor {
    search: Operation,
    offset: usize,
    cookie: [u8; COOKIE_BYTES],
}

#[derive(Default)]
struct Session {
    cursor: Option<Cursor>,
}

impl Session {
    fn respond(&mut self, fixture: &Fixture, request: &Request) -> Option<Vec<u8>> {
        if matches!(request.operation, Operation::Bind { .. }) {
            self.cursor = None;
        }
        if !matches!(
            request.operation,
            Operation::Search {
                directory: Some(_),
                ..
            }
        ) {
            return respond(request);
        }
        let id = request.message_id;
        Some(self.search(fixture, request).unwrap_or_else(|error| {
            search_done(id, error.code, error.matched_dn, error.diagnostic, None)
        }))
    }

    fn search(&mut self, fixture: &Fixture, request: &Request) -> Result<Vec<u8>, SearchError> {
        let Operation::Search {
            scope,
            types_only,
            attributes,
            filter,
            directory: Some(search),
            ..
        } = &request.operation
        else {
            unreachable!("directory search dispatch")
        };
        let id = request.message_id;
        let page = match &request.controls {
            SearchControls::None => None,
            SearchControls::Page(page) => Some(page),
            SearchControls::Invalid => return Err(SearchError::new(2, b"Invalid search controls")),
            SearchControls::Unavailable => {
                return Err(SearchError::new(
                    12,
                    b"Requested critical control is unavailable",
                ));
            }
        };
        if search.deref != 0 || *filter == FilterResult::Unsupported {
            return Err(SearchError::new(
                53,
                b"Alias dereferencing or filter is unsupported",
            ));
        }
        if page.is_some_and(|page| page.size > MAX_PAGE_SIZE) {
            return Err(SearchError::new(11, b"Page size exceeds profile limit"));
        }
        let offset = match page {
            Some(page) if !page.cookie.is_empty() => {
                let cursor = self.cursor.as_ref().ok_or(INVALID_CURSOR)?;
                if cursor.cookie.as_slice() != page.cookie || cursor.search != request.operation {
                    return Err(INVALID_CURSOR);
                }
                if page.size == 0 {
                    self.cursor = None;
                    return Ok(search_done(id, 0, "", b"", Some(b"")));
                }
                cursor.offset
            }
            Some(page) if page.size == 0 => {
                return Err(SearchError::new(
                    2,
                    b"Empty paging cookie cannot cancel a search",
                ));
            }
            _ => {
                self.cursor = None;
                0
            }
        };

        let base = search.base().map_err(|_| INVALID_DN)?;
        let mut matches = Vec::new();
        for candidate in fixture.candidates(base, *scope)? {
            if search
                .evaluate(|field, assertion| fixture.leaf(candidate, field, assertion))
                .map_err(|_| SearchError::new(2, b"Invalid search filter"))?
                == FilterResult::Matches
            {
                matches.push(candidate);
            }
        }
        let total = if search.size_limit == 0 {
            matches.len()
        } else {
            matches.len().min(search.size_limit as usize)
        };
        let end = page.map_or(total, |page| total.min(offset + page.size as usize));
        let mut cookie = [0; COOKIE_BYTES];
        let continuation = end < total;
        if continuation {
            getrandom::fill(&mut cookie)
                .map_err(|_| SearchError::new(52, b"Paging service is unavailable"))?;
        }
        self.cursor = continuation.then(|| Cursor {
            search: request.operation.clone(),
            offset: end,
            cookie,
        });

        let mut reply = Vec::new();
        for candidate in &matches[offset..end] {
            let fields = FIELDS.iter().filter_map(|(name, _)| {
                candidate.attribute(name).map(|value| (*name, value, false))
            });
            reply.extend(search_entry(
                id,
                &candidate.dn(),
                fields,
                attributes,
                *types_only,
            ));
        }
        let (code, diagnostic) = if !continuation && total < matches.len() {
            (4, b"Search size limit exceeded".as_slice())
        } else {
            (0, b"".as_slice())
        };
        let response_cookie = page.map(|_| if continuation { cookie.as_slice() } else { b"" });
        reply.extend(search_done(id, code, "", diagnostic, response_cookie));
        Ok(reply)
    }
}

pub fn serve(address: SocketAddr, max_connections: Option<usize>) -> io::Result<()> {
    let fixture = Fixture::new().map_err(io::Error::other)?;
    let fixture = &fixture;
    babel_ldap::server::serve_with(address, max_connections, decode_directory, || {
        let mut session = Session::default();
        move |request| session.respond(fixture, request)
    })
}

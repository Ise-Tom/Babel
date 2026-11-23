//! Bounded DNS responses for one synthetic DC discovery zone.

#![forbid(unsafe_code)]

use std::net::{Ipv4Addr, Ipv6Addr};

const ZONE: &str = "discovery.example.test";
const HEADER: usize = 12;
const MAX_MESSAGE: usize = 512;
const MAX_NAME: usize = 255;
const IN: u16 = 1;
const A: u16 = 1;
const SOA: u16 = 6;
const AAAA: u16 = 28;
const SRV: u16 = 33;

const QR: u16 = 0x8000;
const OPCODE: u16 = 0x7800;
const AA: u16 = 0x0400;
const TC: u16 = 0x0200;
const RD: u16 = 0x0100;
const NOERROR: u16 = 0;
const FORMERR: u16 = 1;
const NXDOMAIN: u16 = 3;
const NOTIMP: u16 = 4;
const REFUSED: u16 = 5;

const MAX_TTL: u64 = 30;

#[derive(Clone, Copy, PartialEq, Eq)]
enum Site {
    East,
    West,
}

const LOCATORS: [(&str, Option<Site>); 3] = [
    ("_ldap._tcp.dc._msdcs.discovery.example.test", None),
    (
        "_ldap._tcp.east._sites.dc._msdcs.discovery.example.test",
        Some(Site::East),
    ),
    (
        "_ldap._tcp.west._sites.dc._msdcs.discovery.example.test",
        Some(Site::West),
    ),
];

struct Dc {
    host: &'static str,
    site: Site,
    v4: Ipv4Addr,
    v6: Ipv6Addr,
    eligible: bool,
    expires_at: u64,
}

const fn ip6(last: u16) -> Ipv6Addr {
    Ipv6Addr::new(0x2001, 0xdb8, 0, 0, 0, 0, 0, last)
}

const DCS: [Dc; 5] = [
    Dc {
        host: "dc-east.discovery.example.test",
        site: Site::East,
        v4: Ipv4Addr::new(192, 0, 2, 10),
        v6: ip6(0x10),
        eligible: true,
        expires_at: 300,
    },
    Dc {
        host: "dc-west.discovery.example.test",
        site: Site::West,
        v4: Ipv4Addr::new(192, 0, 2, 20),
        v6: ip6(0x20),
        eligible: true,
        expires_at: 300,
    },
    Dc {
        host: "dc-stale.discovery.example.test",
        site: Site::East,
        v4: Ipv4Addr::new(192, 0, 2, 30),
        v6: ip6(0x30),
        eligible: true,
        expires_at: 0,
    },
    Dc {
        host: "dc-ineligible.discovery.example.test",
        site: Site::West,
        v4: Ipv4Addr::new(192, 0, 2, 40),
        v6: ip6(0x40),
        eligible: false,
        expires_at: 300,
    },
    Dc {
        host: "dc-invalid.discovery.example.test",
        site: Site::East,
        v4: Ipv4Addr::UNSPECIFIED,
        v6: ip6(0x50),
        eligible: true,
        expires_at: 300,
    },
];

impl Dc {
    fn ttl(&self, elapsed: u64) -> Option<u32> {
        if !self.eligible || self.v4.is_unspecified() || self.v6.is_unspecified() {
            return None;
        }
        let remaining = self.expires_at.saturating_sub(elapsed);
        (remaining > 0).then_some(remaining.min(MAX_TTL) as u32)
    }
}

struct Question<'a> {
    name: String,
    kind: u16,
    class: u16,
    wire: &'a [u8],
}

impl<'a> Question<'a> {
    fn parse(packet: &'a [u8]) -> Option<Self> {
        let mut pos = HEADER;
        let mut name = String::new();
        loop {
            let length = usize::from(*packet.get(pos)?);
            pos += 1;
            if length == 0 {
                break;
            }
            // The sole question has no earlier DNS name to point to.
            if length > 63 || pos + length - HEADER >= MAX_NAME {
                return None;
            }
            let label = packet.get(pos..pos + length)?;
            if !label
                .iter()
                .all(|c| c.is_ascii_alphanumeric() || matches!(c, b'-' | b'_'))
            {
                return None;
            }
            if !name.is_empty() {
                name.push('.');
            }
            name.extend(label.iter().map(|c| char::from(c.to_ascii_lowercase())));
            pos += length;
        }
        let fields = packet.get(pos..pos + 4)?;
        Some(Self {
            name,
            kind: word(fields, 0),
            class: word(fields, 2),
            wire: &packet[HEADER..pos + 4],
        })
    }
}

fn word(bytes: &[u8], at: usize) -> u16 {
    u16::from_be_bytes([bytes[at], bytes[at + 1]])
}

fn name_on_wire(out: &mut Vec<u8>, name: &str) {
    for label in name.split('.') {
        out.push(label.len() as u8);
        out.extend_from_slice(label.as_bytes());
    }
    out.push(0);
}

struct Record {
    kind: u16,
    ttl: u32,
    data: Vec<u8>,
}

impl Record {
    fn srv(dc: &Dc, ttl: u32) -> Self {
        let mut data = vec![0, 0, 0, 0];
        data.extend_from_slice(&389_u16.to_be_bytes());
        // The SRV target name is never compressed.
        name_on_wire(&mut data, dc.host);
        Self {
            kind: SRV,
            ttl,
            data,
        }
    }

    fn negative_soa() -> Self {
        let mut data = Vec::new();
        name_on_wire(&mut data, ZONE);
        name_on_wire(&mut data, "hostmaster.discovery.example.test");
        for field in [1_u32, 3600, 600, 86400, 0] {
            data.extend_from_slice(&field.to_be_bytes());
        }
        Self {
            kind: SOA,
            ttl: 0,
            data,
        }
    }

    fn write(&self, out: &mut Vec<u8>) {
        out.extend_from_slice(&self.kind.to_be_bytes());
        out.extend_from_slice(&IN.to_be_bytes());
        out.extend_from_slice(&self.ttl.to_be_bytes());
        out.extend_from_slice(&(self.data.len() as u16).to_be_bytes());
        out.extend_from_slice(&self.data);
    }
}

fn response_header(
    request: &[u8],
    question: Option<&Question<'_>>,
    status: u16,
    authoritative: bool,
    answers: u16,
    authority: u16,
) -> Vec<u8> {
    let mut reply = Vec::with_capacity(MAX_MESSAGE);
    let flags = QR | (word(request, 2) & (OPCODE | RD)) | status;
    let flags = if authoritative { flags | AA } else { flags };
    for field in [
        word(request, 0),
        flags,
        u16::from(question.is_some()),
        answers,
        authority,
        0,
    ] {
        reply.extend_from_slice(&field.to_be_bytes());
    }
    if let Some(question) = question {
        reply.extend_from_slice(question.wire);
    }
    reply
}

fn within(name: &str, zone: &str) -> bool {
    name == zone
        || name
            .strip_suffix(zone)
            .is_some_and(|prefix| prefix.ends_with('.'))
}

fn lookup(question: &Question<'_>, elapsed: u64) -> (bool, Vec<Record>) {
    if let Some((_, site)) = LOCATORS.iter().find(|(owner, _)| *owner == question.name) {
        if question.kind != SRV {
            return (true, Vec::new());
        }
        let records: Vec<_> = DCS
            .iter()
            .filter(|dc| site.is_none_or(|site| site == dc.site))
            .filter_map(|dc| dc.ttl(elapsed).map(|ttl| (dc, ttl)))
            .collect();
        // Publish a uniform TTL within the RRset even when leases differ.
        let ttl = records.iter().map(|(_, ttl)| *ttl).min().unwrap_or(0);
        return (
            true,
            records
                .into_iter()
                .map(|(dc, _)| Record::srv(dc, ttl))
                .collect(),
        );
    }
    if let Some((dc, ttl)) = DCS
        .iter()
        .find(|dc| dc.host == question.name)
        .and_then(|dc| dc.ttl(elapsed).map(|ttl| (dc, ttl)))
    {
        let data = match question.kind {
            A => dc.v4.octets().to_vec(),
            AAAA => dc.v6.octets().to_vec(),
            _ => return (true, Vec::new()),
        };
        return (
            true,
            vec![Record {
                kind: question.kind,
                ttl,
                data,
            }],
        );
    }
    // A parent of a configured owner exists even if it has no RRset of its own.
    let present = LOCATORS
        .iter()
        .any(|(owner, _)| within(owner, &question.name));
    (present, Vec::new())
}

/// Respond to one UDP datagram using seconds from the start of the synthetic lease clock.
/// Ignore responses and packets without a complete header.
pub fn reply(request: &[u8], elapsed: u64) -> Option<Vec<u8>> {
    let header = request.get(..HEADER)?;
    let flags = word(header, 2);
    if flags & QR != 0 {
        return None;
    }
    let error = |status| Some(response_header(header, None, status, false, 0, 0));
    if flags & OPCODE != 0 {
        // Includes UPDATE. No update section is decoded and no state can be mutated.
        return error(NOTIMP);
    }
    if request.len() > MAX_MESSAGE
        || flags & TC != 0
        || word(header, 4) != 1
        || word(header, 6) != 0
        || word(header, 8) != 0
    {
        return error(FORMERR);
    }
    let Some(question) = Question::parse(request) else {
        return error(FORMERR);
    };
    let refuse = |status| {
        Some(response_header(
            header,
            Some(&question),
            status,
            false,
            0,
            0,
        ))
    };
    if word(header, 10) != 0 {
        return refuse(NOTIMP);
    }
    if question.wire.len() + HEADER != request.len() {
        return error(FORMERR);
    }
    if !within(&question.name, ZONE) {
        return refuse(REFUSED);
    }
    if question.class != IN || !matches!(question.kind, A | AAAA | SRV) {
        return refuse(NOTIMP);
    }

    let (exists, answers) = lookup(&question, elapsed);
    let status = if exists { NOERROR } else { NXDOMAIN };
    let negative = answers.is_empty();
    let mut response = response_header(
        header,
        Some(&question),
        status,
        true,
        answers.len() as u16,
        u16::from(negative),
    );
    for answer in answers {
        response.extend_from_slice(&[0xc0, 0x0c]); // Owner points to the echoed question.
        answer.write(&mut response);
    }
    if negative {
        name_on_wire(&mut response, ZONE);
        Record::negative_soa().write(&mut response);
    }
    Some(response)
}

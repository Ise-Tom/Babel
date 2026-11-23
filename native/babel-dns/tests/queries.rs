use babel_dns::reply;

const DOMAIN_LOCATOR: &str = "_ldap._tcp.dc._msdcs.discovery.example.test";
const EAST_LOCATOR: &str = "_ldap._tcp.east._sites.dc._msdcs.discovery.example.test";
const EAST_DC: &str = "dc-east.discovery.example.test";

fn query(name: &str, kind: u16) -> Vec<u8> {
    let mut packet = vec![0x12, 0x34, 0x01, 0, 0, 1, 0, 0, 0, 0, 0, 0];
    for label in name.split('.') {
        packet.push(label.len() as u8);
        packet.extend_from_slice(label.as_bytes());
    }
    packet.push(0);
    packet.extend_from_slice(&kind.to_be_bytes());
    packet.extend_from_slice(&[0, 1]);
    packet
}

fn word(packet: &[u8], at: usize) -> u16 {
    u16::from_be_bytes([packet[at], packet[at + 1]])
}

fn status(packet: &[u8], expected: u16, authoritative: bool) {
    assert_eq!(word(packet, 0), 0x1234);
    assert_eq!(word(packet, 2) & 0x808f, 0x8000 | expected);
    assert_eq!(word(packet, 2) & 0x0400 != 0, authoritative);
}

#[test]
fn srv_and_addresses_expire_at_the_lease_boundary() {
    for (host, kind) in [(EAST_LOCATOR, 33), (EAST_DC, 1), (EAST_DC, 28)] {
        let request = query(host, kind);
        let response = reply(&request, 299).unwrap();
        status(&response, 0, true);
        assert_eq!(word(&response, 6), 1);
        assert_eq!(word(&response, 8), 0);
        let ttl = request.len() + 6;
        assert_eq!(&response[ttl..ttl + 4], &1_u32.to_be_bytes());
        let expired = reply(&request, 300).unwrap();
        status(&expired, if kind == 33 { 0 } else { 3 }, true);
        assert_eq!(word(&expired, 6), 0);
        assert_eq!(word(&expired, 8), 1);
    }
}

#[test]
fn unsupported_questions_return_explicit_errors() {
    for name in ["outside.example.test", "notdiscovery.example.test"] {
        let request = query(name, 1);
        let response = reply(&request, 0).unwrap();
        status(&response, 5, false);
        assert_eq!(word(&response, 4), 1);
        assert_eq!(&response[12..], &request[12..]);
    }
    for kind in [16, 252, 255] {
        let request = query(EAST_DC, kind);
        status(&reply(&request, 0).unwrap(), 4, false);
    }
    let mut class = query(EAST_DC, 1);
    *class.last_mut().unwrap() = 3;
    status(&reply(&class, 0).unwrap(), 4, false);
    let mut additional = query(EAST_DC, 1);
    additional[11] = 1;
    status(&reply(&additional, 0).unwrap(), 4, false);
    let mut update = query(EAST_DC, 1);
    update[2] = 0x28;
    let response = reply(&update, 0).unwrap();
    status(&response, 4, false);
    assert_eq!(word(&response, 2) & 0x7800, 0x2800);
    assert_eq!(word(&response, 4), 0);
    status(&reply(&query(EAST_DC, 1), 0).unwrap(), 0, true);
}

#[test]
fn parser_bounds_counts_names_and_datagrams() {
    let request = query(DOMAIN_LOCATOR, 33);
    for cut in 0..request.len() {
        let result = reply(&request[..cut], 0);
        if cut < 12 {
            assert!(result.is_none());
        } else {
            status(&result.unwrap(), 1, false);
        }
    }
    for (offset, value) in [(2, 3), (5, 2), (7, 1), (9, 1), (12, 0xc0), (13, b'.')] {
        let mut malformed = request.clone();
        malformed[offset] = value;
        status(&reply(&malformed, 0).unwrap(), 1, false);
    }
    let mut trailing = request.clone();
    trailing.push(0);
    status(&reply(&trailing, 0).unwrap(), 1, false);
    trailing.resize(513, 0);
    status(&reply(&trailing, 0).unwrap(), 1, false);
    let label = "x".repeat(63);
    let long_name = [label.as_str(); 4].join(".");
    status(&reply(&query(&long_name, 1), 0).unwrap(), 1, false);
    let mut incoming_response = request;
    incoming_response[2] |= 0x80;
    assert!(reply(&incoming_response, 0).is_none());
}

#[test]
fn empty_nonterminals_and_absent_names_have_distinct_status() {
    let empty = reply(&query("_msdcs.discovery.example.test", 1), 0).unwrap();
    status(&empty, 0, true);
    assert_eq!(word(&empty, 6), 0);
    assert_eq!(word(&empty, 8), 1);
    let absent = reply(&query("absent.discovery.example.test", 1), 0).unwrap();
    status(&absent, 3, true);
    assert_eq!(word(&absent, 6), 0);
    assert_eq!(word(&absent, 8), 1);
}

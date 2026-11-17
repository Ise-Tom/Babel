use babel_ldap::{DecodeError, MAX_FRAME_BYTES, Operation, decode, respond};
use proptest::prelude::*;

fn tlv(tag: u8, body: &[u8]) -> Vec<u8> {
    let mut bytes = vec![tag];
    if body.len() < 128 {
        bytes.push(body.len() as u8);
    } else {
        bytes.extend([0x82, (body.len() >> 8) as u8, body.len() as u8]);
    }
    bytes.extend(body);
    bytes
}
fn integer(tag: u8, n: u32) -> Vec<u8> {
    let raw = n.to_be_bytes();
    let first = raw.iter().position(|b| *b != 0).unwrap_or(3);
    let mut body = Vec::new();
    if raw[first] & 128 != 0 {
        body.push(0);
    }
    body.extend(&raw[first..]);
    tlv(tag, &body)
}
fn message(id: u32, op: &[u8]) -> Vec<u8> {
    let mut body = integer(2, id);
    body.extend(op);
    tlv(0x30, &body)
}
fn search(
    base: &[u8],
    scope: u32,
    filter: &[u8],
    attributes: &[&[u8]],
    types_only: bool,
) -> Vec<u8> {
    let mut body = tlv(4, base);
    body.extend(integer(10, scope));
    body.extend([
        10,
        1,
        0,
        2,
        1,
        0,
        2,
        1,
        0,
        1,
        1,
        if types_only { 255 } else { 0 },
    ]);
    body.extend(filter);
    let names: Vec<u8> = attributes.iter().flat_map(|name| tlv(4, name)).collect();
    body.extend(tlv(0x30, &names));
    message(7, &tlv(0x63, &body))
}
fn root(attributes: &[&[u8]], types_only: bool) -> Vec<u8> {
    search(b"", 0, &tlv(0x87, b"objectClass"), attributes, types_only)
}
fn has(bytes: &[u8], needle: &[u8]) -> bool {
    bytes.windows(needle.len()).any(|w| w == needle)
}

#[test]
fn golden_anonymous_bind_and_unbind() {
    let bind = [0x30, 0x0c, 2, 1, 1, 0x60, 7, 2, 1, 3, 4, 0, 0x80, 0];
    let request = decode(&bind).unwrap();
    assert_eq!(
        request.operation,
        Operation::Bind {
            version: 3,
            anonymous: true
        }
    );
    assert_eq!(
        respond(&request).unwrap(),
        [0x30, 0x0c, 2, 1, 1, 0x61, 7, 10, 1, 0, 4, 0, 4, 0]
    );
    let unbind = decode(&[0x30, 5, 2, 1, 1, 0x42, 0]).unwrap();
    assert_eq!(respond(&unbind), None);
}

#[test]
fn credential_bind_is_rejected_without_retaining_or_echoing_secrets() {
    let mut body = vec![2, 1, 3];
    body.extend(tlv(4, b"cn=admin"));
    body.extend(tlv(0x80, b"fixture-not-a-credential"));
    let request = decode(&message(2, &tlv(0x60, &body))).unwrap();
    assert!(!format!("{request:?}").contains("fixture-not-a-credential"));
    assert!(!format!("{request:?}").contains("cn=admin"));
    let response = respond(&request).unwrap();
    assert!(has(&response, &[10, 1, 53]));
    assert!(!has(&response, b"fixture-not-a-credential"));
}

#[test]
fn unsupported_bind_version_and_sasl_cannot_succeed() {
    for (version, authentication, code) in [(2, vec![0x80, 0], 2), (3, vec![0xa3, 0], 53)] {
        let mut body = integer(2, version);
        body.extend([4, 0]);
        body.extend(authentication);
        let response = respond(&decode(&message(1, &tlv(0x60, &body))).unwrap()).unwrap();
        assert!(has(&response, &[10, 1, code]));
    }
}

#[test]
fn rootdse_attribute_projection_is_explicit_and_truthful() {
    let response =
        respond(&decode(&root(&[b"supportedLDAPVersion", b"VENDORNAME"], false)).unwrap()).unwrap();
    assert!(has(&response, b"supportedLDAPVersion"));
    assert!(has(&response, b"Babel"));
    assert!(!has(&response, b"vendorVersion"));
    assert!(!has(&response, b"namingContexts"));
    assert!(!has(&response, b"supportedCapabilities"));
    assert!(has(&response, &[10, 1, 0]));
}

#[test]
fn default_star_plus_no_attributes_and_types_only_are_distinct() {
    for attrs in [vec![], vec![b"*".as_slice()]] {
        let response = respond(&decode(&root(&attrs, false)).unwrap()).unwrap();
        assert!(has(&response, b"objectClass"));
        assert!(!has(&response, b"supportedLDAPVersion"));
    }
    let plus = respond(&decode(&root(&[b"+"], false)).unwrap()).unwrap();
    assert!(has(&plus, b"supportedLDAPVersion"));
    assert!(!has(&plus, b"objectClass"));
    let none = respond(&decode(&root(&[b"1.1"], false)).unwrap()).unwrap();
    assert!(!has(&none, b"objectClass"));
    assert!(!has(&none, b"vendorName"));
    let types = respond(&decode(&root(&[b"vendorName"], true)).unwrap()).unwrap();
    assert!(has(&types, b"vendorName"));
    assert!(!has(&types, b"Babel"));
    assert!(has(&types, &[0x31, 0]));
}

#[test]
fn unsupported_searches_return_failure_not_empty_success() {
    for (base, scope, filter, code) in [
        (b"dc=example".as_slice(), 0, tlv(0x87, b"objectClass"), 32),
        (b"".as_slice(), 2, tlv(0x87, b"objectClass"), 53),
        (b"".as_slice(), 0, tlv(0xa4, b""), 53),
    ] {
        let response =
            respond(&decode(&search(base, scope, &filter, &[], false)).unwrap()).unwrap();
        assert!(has(&response, &[10, 1, code]));
        assert!(!has(&response, b"Babel"));
    }
}

#[test]
fn every_truncation_and_trailing_bytes_fail() {
    let valid = root(&[b"supportedLDAPVersion"], false);
    for length in 0..valid.len() {
        assert!(decode(&valid[..length]).is_err());
    }
    let mut trailing = valid;
    trailing.push(0);
    assert_eq!(decode(&trailing), Err(DecodeError::TrailingData));
}

#[test]
fn invalid_lengths_ids_tags_enums_and_bool_are_rejected() {
    for frame in [
        vec![0x30, 0x80],
        vec![0x30, 0x85, 0, 0, 0, 0, 0],
        vec![0x30, 0x84, 0xff, 0xff, 0xff, 0xff],
        vec![0x30, 0x7f],
        vec![0x31, 0],
        vec![0x3f, 0],
        vec![0x30, 5, 2, 1, 0, 0x42, 0],
        vec![0x30, 5, 2, 1, 0xff, 0x42, 0],
        vec![0x30, 6, 2, 2, 0, 1, 0x42, 0],
        vec![0x30, 4, 2, 0, 0x42, 0],
        vec![0x30, 5, 2, 1, 1, 0x4a, 0],
    ] {
        assert!(decode(&frame).is_err(), "accepted {frame:02x?}");
    }
    assert!(decode(&search(b"", 3, &tlv(0x87, b"objectClass"), &[], false)).is_err());
    let mut boolean = root(&[], false);
    let index = boolean.windows(3).position(|v| v == [1, 1, 0]).unwrap();
    boolean[index + 2] = 1;
    assert_eq!(decode(&boolean), Err(DecodeError::InvalidValue));
}

#[test]
fn controls_attribute_limits_and_large_frames_fail_closed() {
    let mut body = vec![2, 1, 1, 0x42, 0];
    body.extend([0xa0, 0]);
    assert_eq!(
        decode(&tlv(0x30, &body)),
        Err(DecodeError::UnsupportedControls)
    );
    assert_eq!(
        decode(&vec![0; MAX_FRAME_BYTES + 1]),
        Err(DecodeError::TooLarge)
    );
    let attributes = vec![b"cn".as_slice(); 65];
    assert_eq!(
        decode(&root(&attributes, false)),
        Err(DecodeError::AttributeLimit)
    );
    for attribute in [vec![], vec![b'a'; 65], vec![0xff]] {
        assert_eq!(
            decode(&root(&[&attribute], false)),
            Err(DecodeError::InvalidValue)
        );
    }
}

#[test]
fn malformed_nested_filters_are_rejected() {
    let filter = tlv(0xa0, &vec![0xa0; 4000]);
    assert!(decode(&search(b"", 0, &filter, &[], false)).is_err());
}

fn equality(name: &[u8], value: &[u8]) -> Vec<u8> {
    let mut assertion = tlv(4, name);
    assertion.extend(tlv(4, value));
    tlv(0xa3, &assertion)
}

fn filter_reply(filter: &[u8]) -> Vec<u8> {
    respond(&decode(&search(b"", 0, filter, &[b"vendorName"], false)).unwrap()).unwrap()
}

#[test]
fn rootdse_presence_and_object_class_equality_support_boolean_filters() {
    for filter in [
        tlv(0x87, b"VENDORNAME"),
        equality(b"OBJECTCLASS", b"TOP"),
        equality(b"2.5.4.0", b"2.5.6.0"),
        tlv(0xa2, &equality(b"objectClass", b"person")),
        tlv(
            0xa0,
            &[
                equality(b"objectClass", b"top"),
                tlv(0x87, b"vendorVersion"),
            ]
            .concat(),
        ),
        tlv(
            0xa1,
            &[
                equality(b"objectClass", b"person"),
                equality(b"objectClass", b"top"),
            ]
            .concat(),
        ),
    ] {
        let reply = filter_reply(&filter);
        assert!(has(&reply, b"Babel"));
        assert!(has(&reply, &[10, 1, 0]));
    }
}

#[test]
fn nonmatches_and_undefined_filters_return_success_without_an_entry() {
    for filter in [
        equality(b"objectClass", b"person"),
        tlv(0x87, b"unknownAttribute"),
        tlv(0xa2, &tlv(0x87, b"unknownAttribute")),
        equality(b"unknownAttribute", b"top"),
        tlv(0xa2, &equality(b"unknownAttribute", b"top")),
        equality(b"objectClass", b"*"),
        tlv(0xa2, &equality(b"objectClass", b"*")),
        equality(b"objectClass", b"top;lang-en"),
        equality(b"objectClass", &[0xff]),
        tlv(
            0xa0,
            &[
                tlv(0x87, b"unknownAttribute"),
                equality(b"objectClass", b"person"),
            ]
            .concat(),
        ),
        tlv(
            0xa1,
            &[
                tlv(0x87, b"unknownAttribute"),
                equality(b"objectClass", b"person"),
            ]
            .concat(),
        ),
    ] {
        let reply = filter_reply(&filter);
        assert!(!has(&reply, b"Babel"));
        assert!(has(&reply, &[10, 1, 0]));
    }
    let undefined = tlv(0x87, b"unknownAttribute");
    assert!(has(
        &filter_reply(&tlv(
            0xa1,
            &[undefined.clone(), equality(b"objectClass", b"top")].concat()
        )),
        b"Babel"
    ));
    assert!(!has(
        &filter_reply(&tlv(
            0xa0,
            &[undefined, equality(b"objectClass", b"top")].concat()
        )),
        b"Babel"
    ));
}

#[test]
fn unsupported_matching_is_not_hidden_by_boolean_short_circuiting() {
    for unsupported in [
        tlv(0xa4, b""),
        tlv(0xa5, b""),
        tlv(0xa6, b""),
        tlv(0xa8, b""),
        tlv(0xa9, b""),
        equality(b"vendorName", b"Babel"),
    ] {
        for filter in [
            unsupported.clone(),
            tlv(0xa2, &unsupported),
            tlv(
                0xa1,
                &[equality(b"objectClass", b"top"), unsupported.clone()].concat(),
            ),
            tlv(
                0xa0,
                &[equality(b"objectClass", b"person"), unsupported].concat(),
            ),
        ] {
            let reply = filter_reply(&filter);
            assert!(has(&reply, &[10, 1, 53]));
            assert!(!has(&reply, b"Babel"));
        }
    }
}

#[test]
fn filter_depth_node_assertion_and_structural_limits_are_enforced() {
    use babel_ldap::{MAX_ASSERTION_BYTES, MAX_FILTER_DEPTH, MAX_FILTER_NODES};
    let mut nested = tlv(0x87, b"objectClass");
    for _ in 1..MAX_FILTER_DEPTH {
        nested = tlv(0xa2, &nested);
    }
    assert!(decode(&search(b"", 0, &nested, &[], false)).is_ok());
    nested = tlv(0xa2, &nested);
    assert_eq!(
        decode(&search(b"", 0, &nested, &[], false)),
        Err(DecodeError::FilterLimit)
    );
    for count in [MAX_FILTER_NODES - 1, MAX_FILTER_NODES] {
        let filter = tlv(0xa0, &tlv(0x87, b"objectClass").repeat(count));
        assert_eq!(
            decode(&search(b"", 0, &filter, &[], false)).is_ok(),
            count < MAX_FILTER_NODES
        );
    }
    assert!(
        decode(&search(
            b"",
            0,
            &equality(b"objectClass", &vec![b'a'; MAX_ASSERTION_BYTES]),
            &[],
            false
        ))
        .is_ok()
    );
    assert_eq!(
        decode(&search(
            b"",
            0,
            &equality(b"objectClass", &vec![b'a'; MAX_ASSERTION_BYTES + 1]),
            &[],
            false
        )),
        Err(DecodeError::FilterLimit)
    );
    for filter in [
        tlv(0xa0, b""),
        tlv(0xa1, b""),
        tlv(0xa2, b""),
        tlv(0xa2, &tlv(0x87, b"objectClass").repeat(2)),
        tlv(0xa7, b""),
        tlv(0x87, b"*"),
        equality(b"", b"top"),
        equality(&[b'a'; 65], b"top"),
        tlv(0xa3, &tlv(4, b"objectClass")),
    ] {
        assert!(decode(&search(b"", 0, &filter, &[], false)).is_err());
    }
}

#[test]
fn filter_assertions_are_never_retained_or_echoed() {
    let frame = search(
        b"",
        0,
        &equality(b"unknownAttribute", b"fixture-not-a-credential"),
        &[],
        false,
    );
    let request = decode(&frame).unwrap();
    assert!(!format!("{request:?}").contains("fixture-not-a-credential"));
    assert!(!has(
        &respond(&request).unwrap(),
        b"fixture-not-a-credential"
    ));
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(256))]
    #[test]
    fn boolean_filter_order_and_double_negation_preserve_results(a in 0usize..3, b in 0usize..3, and in any::<bool>()) {
        let leaves = [equality(b"objectClass", b"top"), equality(b"objectClass", b"person"), tlv(0x87, b"unknownAttribute")];
        let tag = if and { 0xa0 } else { 0xa1 };
        let filter = tlv(tag, &[leaves[a].clone(), leaves[b].clone()].concat());
        let reversed = tlv(tag, &[leaves[b].clone(), leaves[a].clone()].concat());
        prop_assert_eq!(filter_reply(&filter), filter_reply(&reversed));
        prop_assert_eq!(filter_reply(&filter), filter_reply(&tlv(0xa2, &tlv(0xa2, &filter))));
    }
    #[test]
    fn object_class_assertions_match_only_the_public_class(value in "[a-zA-Z][a-zA-Z0-9-]{0,40}") {
        let reply = filter_reply(&equality(b"objectClass", value.as_bytes()));
        prop_assert_eq!(has(&reply, b"Babel"), value.eq_ignore_ascii_case("top"));
    }
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(256))]
    #[test]
    fn arbitrary_frames_never_panic_or_produce_unbounded_responses(bytes in prop::collection::vec(any::<u8>(), 0..=MAX_FRAME_BYTES + 32)) {
        if let Ok(request) = decode(&bytes) && let Some(response) = respond(&request) { prop_assert!(response.len() <= 1024); }
    }
    #[test]
    fn positive_message_ids_survive_round_trip(id in 1u32..=i32::MAX as u32) {
        let request = decode(&message(id, &[0x42, 0])).unwrap();
        prop_assert_eq!(request.message_id, id);
    }
    #[test]
    fn mutation_of_a_valid_request_is_always_bounded(position in 0usize..128, value in any::<u8>()) {
        let mut frame = root(&[b"supportedLDAPVersion"], false);
        let index = position % frame.len();
        frame[index] = value;
        if let Ok(request) = decode(&frame) && let Some(response) = respond(&request) { prop_assert!(response.len() <= 1024); }
    }
}

#[test]
fn attribute_descriptions_accept_valid_options_and_reject_control_or_ambiguous_names() {
    for name in [b"cn;lang-en".as_slice(), b"1.2.840.113556".as_slice()] {
        assert!(decode(&root(&[name], false)).is_ok());
    }
    for name in [
        b"cn\0".as_slice(),
        b"cn;",
        b"1..2",
        b"01.2",
        b"cn=x",
        b";cn",
        b"-cn",
        b"\t",
    ] {
        assert_eq!(
            decode(&root(&[name], false)),
            Err(DecodeError::InvalidValue)
        );
    }
}

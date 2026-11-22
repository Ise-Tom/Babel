//! Public API evidence for P01-02's bounded synthetic schema.

use babel_directory::{Directory, DirectoryError as Error, Identity, MAX_ENTRIES, ObjectClass};

const ALICE: &str = "CN=Alice,DC=babel,DC=test";
const BOB: &str = "CN=Bob,DC=babel,DC=test";
const ALICE_ATTRS: &[(&str, &str)] = &[
    ("displayName", "Alice Example"),
    ("uidNumber", "42"),
    ("description", "Original Value"),
];

fn ids(entries: Vec<&babel_directory::Entry>) -> Vec<Identity> {
    entries.into_iter().map(|entry| entry.identity()).collect()
}

#[test]
fn create_and_lookup_stable_identities_and_class_attributes() {
    let mut directory = Directory::new().unwrap();
    let alice = directory.create(ALICE, "USER", ALICE_ATTRS).unwrap();
    let workstation = directory
        .create(
            "CN=Station,DC=babel,DC=test",
            "computer",
            &[("dnsHostName", "Node-1.Babel.Test")],
        )
        .unwrap();
    let group = directory
        .create("CN=Readers,DC=babel,DC=test", "group", &[])
        .unwrap();

    for (id, class) in [
        (alice, ObjectClass::User),
        (workstation, ObjectClass::Computer),
        (group, ObjectClass::Group),
    ] {
        let entry = directory.lookup_guid(id.guid).unwrap();
        assert_eq!(entry.object_class(), class);
        assert_eq!(entry.identity(), id);
        assert_eq!(directory.lookup_sid(id.sid).unwrap().identity(), id);
        assert_eq!(id.sid.domain(), directory.domain_sid());
        assert_eq!(id.guid.as_bytes()[6] >> 4, 4);
        assert_eq!(id.guid.as_bytes()[8] >> 6, 2);
    }
    assert_eq!(alice.guid.to_string().len(), 36);
    assert_eq!(
        alice.sid.to_string(),
        format!("{}-1000", directory.domain_sid())
    );
    assert!(directory.domain_sid().to_string().starts_with("S-1-5-21-"));
    assert_ne!(alice.guid, workstation.guid);
    assert_ne!(group.guid, workstation.guid);
    assert_eq!(workstation.sid.rid(), alice.sid.rid() + 1);
    assert_eq!(group.sid.rid(), workstation.sid.rid() + 1);

    let by_name = directory
        .lookup_dn("cn=ALICE,dc=BABEL,dc=TEST")
        .unwrap()
        .unwrap();
    assert_eq!(by_name.identity(), alice);
    assert_eq!(by_name.dn().to_string(), ALICE);
    assert_eq!(by_name.attribute("CN"), Some("Alice"));
    assert_eq!(by_name.attribute("DisplayName"), Some("Alice Example"));
    assert_eq!(by_name.attribute("dnsHostName"), None);
    assert_eq!(by_name.attribute("unknown"), None);
}

#[test]
fn same_domain_rename_moves_name_lookup_and_preserves_both_ids() {
    let mut directory = Directory::new().unwrap();
    let before = directory.create(ALICE, "user", ALICE_ATTRS).unwrap();

    let renamed = "CN=Alice Renamed,DC=babel,DC=test";
    directory.rename(before.guid, renamed).unwrap();
    assert!(directory.lookup_dn(ALICE).unwrap().is_none());
    let after = directory.lookup_dn(renamed).unwrap().unwrap();
    assert_eq!(after.identity(), before);
    assert_eq!(after.dn().to_string(), renamed);
    assert_eq!(after.attribute("cn"), Some("Alice Renamed"));
    assert_eq!(after.attribute("description"), Some("Original Value"));
    assert_eq!(directory.lookup_guid(before.guid).unwrap().dn(), after.dn());
    assert_eq!(directory.lookup_sid(before.sid).unwrap().dn(), after.dn());
    assert_eq!(
        ids(directory
            .lookup_equal("CN", "ascii-case-ignore", "ALICE RENAMED")
            .unwrap()),
        vec![before]
    );

    // A display-only change leaves the canonical locator occupied by the same object.
    directory
        .rename(before.guid, "cn=ALICE RENAMED,dc=BABEL,dc=TEST")
        .unwrap();
    assert_eq!(
        directory
            .lookup_dn(renamed)
            .unwrap()
            .unwrap()
            .dn()
            .common_name(),
        "ALICE RENAMED"
    );
    directory
        .rename(before.guid, "cn=ALICE RENAMED,dc=BABEL,dc=TEST")
        .unwrap();
    assert_eq!(
        directory.create(renamed, "group", &[]),
        Err(Error::NameCollision)
    );
    let replacement = directory.create(ALICE, "group", &[]).unwrap();
    assert_ne!(replacement.guid, before.guid);
    assert_eq!(replacement.sid.rid(), before.sid.rid() + 1);
}

#[test]
fn rejected_rename_leaves_both_entries_and_all_lookup_paths_unchanged() {
    let mut directory = Directory::new().unwrap();
    let alice = directory.create(ALICE, "user", ALICE_ATTRS).unwrap();
    let bob = directory
        .create(BOB, "group", &[("description", "Bob's group")])
        .unwrap();
    let foreign = Directory::new()
        .unwrap()
        .create(ALICE, "group", &[])
        .unwrap();

    assert!(directory.lookup_sid(foreign.sid).is_none());
    assert_eq!(
        directory.rename(foreign.guid, ALICE),
        Err(Error::EntryNotFound)
    );
    for (destination, error) in [
        ("cn=BOB,dc=babel,dc=TEST", Error::NameCollision),
        ("CN=Alice,DC=other,DC=test", Error::OutsideNamingContext),
        ("CN=,DC=babel,DC=test", Error::InvalidDn),
    ] {
        assert_eq!(directory.rename(alice.guid, destination), Err(error));
        for (name, identity, description) in
            [(ALICE, alice, "Original Value"), (BOB, bob, "Bob's group")]
        {
            let entry = directory.lookup_dn(name).unwrap().unwrap();
            assert_eq!(entry.identity(), identity);
            assert_eq!(entry.attribute("description"), Some(description));
            assert_eq!(entry.dn().to_string(), name);
            assert_eq!(
                directory.lookup_guid(identity.guid).unwrap().dn(),
                entry.dn()
            );
            assert_eq!(directory.lookup_sid(identity.sid).unwrap().dn(), entry.dn());
            assert_eq!(
                ids(directory
                    .lookup_equal("description", "ascii-exact", description)
                    .unwrap()),
                vec![identity]
            );
        }
    }
}

#[test]
fn invalid_schema_does_not_consume_names_or_rids() {
    let mut directory = Directory::new().unwrap();
    let alice = directory.create(ALICE, "user", ALICE_ATTRS).unwrap();
    for (class, attrs, expected) in [
        ("service", &[][..], Error::InvalidClass),
        (
            "user",
            &[("displayName", "Unpaired")],
            Error::MissingAttribute,
        ),
        ("computer", &[], Error::MissingAttribute),
        ("group", &[("uidNumber", "2")], Error::AttributeNotAllowed),
        (
            "group",
            &[("password", "synthetic")],
            Error::UnknownAttribute,
        ),
        (
            "group",
            &[("objectGUID", "caller-selected")],
            Error::ManagedAttribute,
        ),
        (
            "group",
            &[("OBJECTSID", "caller-selected")],
            Error::ManagedAttribute,
        ),
        ("group", &[("cn", "Wrong")], Error::ManagedAttribute),
        (
            "group",
            &[("description", "First"), ("DESCRIPTION", "Second")],
            Error::DuplicateAttribute,
        ),
        (
            "group",
            &[("description", "Line\nbreak")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "user",
            &[("displayName", "Böb"), ("uidNumber", "42")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "computer",
            &[("dnsHostName", "-bad.babel.test")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "computer",
            &[("dnsHostName", "node..babel.test")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "computer",
            &[("dnsHostName", "babel.test")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "computer",
            &[("dnsHostName", "node.other.test")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "computer",
            &[("dnsHostName", "nød.babel.test")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "user",
            &[("displayName", "Bob"), ("uidNumber", "042")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "user",
            &[("displayName", "Bob"), ("uidNumber", "+42")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "user",
            &[("displayName", "Bob"), ("uidNumber", "4294967296")],
            Error::InvalidAttributeSyntax,
        ),
        (
            "group",
            &[("description", "all"); 5],
            Error::TooManyAttributes,
        ),
    ] {
        assert_eq!(
            directory.create(BOB, class, attrs),
            Err(expected),
            "{class}: {attrs:?}"
        );
        assert!(directory.lookup_dn(BOB).unwrap().is_none());
        assert_eq!(directory.lookup_sid(alice.sid).unwrap().identity(), alice);
    }
    assert_eq!(
        directory.create("cn=ALICE,dc=BABEL,dc=test", "group", &[]),
        Err(Error::NameCollision)
    );
    let bob = directory.create(BOB, "group", &[]).unwrap();
    assert_eq!(bob.sid.rid(), alice.sid.rid() + 1);
}

#[test]
fn names_outside_the_profile_fail_without_creating_entries() {
    let mut directory = Directory::new().unwrap();
    let long_name = format!("CN={},DC=babel,DC=test", "a".repeat(65));
    for name in [
        "",
        "cn=Standalone",
        "Bob,DC=babel,DC=test",
        "OU=Bob,DC=babel,DC=test",
        "CN= Bob,DC=babel,DC=test",
        "CN=Bob ,DC=babel,DC=test",
        "CN=Böb,DC=babel,DC=test",
        "CN=Bob+UID=1,DC=babel,DC=test",
        r"CN=Bob\2cJones,DC=babel,DC=test",
        &long_name,
    ] {
        assert_eq!(
            directory.create(name, "group", &[]),
            Err(Error::InvalidDn),
            "{name}"
        );
        assert_eq!(directory.lookup_dn(name).unwrap_err(), Error::InvalidDn);
    }
    for name in [
        "CN=Bob,OU=People,DC=babel,DC=test",
        "CN=Bob,DC=other,DC=test",
    ] {
        assert_eq!(
            directory.create(name, "group", &[]),
            Err(Error::OutsideNamingContext)
        );
    }
    assert_eq!(directory.create(BOB, "group", &[]).unwrap().sid.rid(), 1000);
}

#[test]
fn equality_uses_the_field_rule_and_refuses_unsupported_matching() {
    let mut directory = Directory::new().unwrap();
    let alice = directory.create(ALICE, "user", ALICE_ATTRS).unwrap();
    let bob = directory
        .create(BOB, "user", &[("displayName", "Bob"), ("uidNumber", "0")])
        .unwrap();
    let workstation = directory
        .create(
            "CN=Node,DC=babel,DC=test",
            "computer",
            &[("dnsHostName", "Node.BABEL.TEST")],
        )
        .unwrap();
    for (field, rule, expected_value, identity) in [
        ("displayname", "ascii-case-ignore", "ALICE EXAMPLE", alice),
        ("uidNumber", "unsigned-integer", "42", alice),
        ("uidNumber", "unsigned-integer", "0", bob),
        ("description", "ascii-exact", "Original Value", alice),
        (
            "dnsHostName",
            "ascii-case-ignore",
            "node.babel.test",
            workstation,
        ),
    ] {
        assert_eq!(
            ids(directory.lookup_equal(field, rule, expected_value).unwrap()),
            vec![identity]
        );
    }
    assert!(
        directory
            .lookup_equal("description", "ascii-exact", "original value")
            .unwrap()
            .is_empty()
    );
    assert!(
        directory
            .lookup_equal("uidNumber", "unsigned-integer", "17")
            .unwrap()
            .is_empty()
    );
    assert_eq!(
        directory
            .lookup_equal("displayName", "approximate", "Alice")
            .unwrap_err(),
        Error::UnsupportedMatchingRule
    );
    assert_eq!(
        directory
            .lookup_equal("uidNumber", "ascii-case-ignore", "42")
            .unwrap_err(),
        Error::UnsupportedMatchingRule
    );
    assert_eq!(
        directory
            .lookup_equal("uidNumber", "unsigned-integer", "0042")
            .unwrap_err(),
        Error::InvalidAttributeSyntax
    );
    assert_eq!(
        directory
            .lookup_equal("description", "ascii-exact", &"x".repeat(129))
            .unwrap_err(),
        Error::InvalidAttributeSyntax
    );
    assert_eq!(
        directory
            .lookup_equal("unknown", "ascii-exact", "value")
            .unwrap_err(),
        Error::UnknownAttribute
    );
    assert_eq!(
        directory.lookup_dn(ALICE).unwrap().unwrap().identity(),
        alice
    );
}

#[test]
fn capacity_failure_preserves_the_last_object_and_allows_rename() {
    let mut directory = Directory::new().unwrap();
    for index in 0..MAX_ENTRIES - 1 {
        let name = format!("CN=Group-{index},DC=babel,DC=test");
        directory.create(&name, "group", &[]).unwrap();
    }
    let last = directory.create(ALICE, "group", &[]).unwrap();
    assert_eq!(
        directory.create(BOB, "group", &[]),
        Err(Error::CapacityExceeded)
    );
    assert!(directory.lookup_dn(BOB).unwrap().is_none());
    assert_eq!(
        directory.lookup_dn(ALICE).unwrap().unwrap().identity(),
        last
    );
    directory.rename(last.guid, BOB).unwrap();
    assert_eq!(directory.lookup_dn(BOB).unwrap().unwrap().identity(), last);
    assert!(directory.lookup_dn(ALICE).unwrap().is_none());
}

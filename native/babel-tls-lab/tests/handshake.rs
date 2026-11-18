//! Synthetic ephemeral PKI and bounded in-memory TLS tests, not AD/client conformance.
use babel_tls_lab::{MAX_DER_BYTES, MAX_WIRE_BYTES, REQUEST, server_config};
use proptest::prelude::*;
use rcgen::{
    BasicConstraints, Certificate, CertificateParams, ExtendedKeyUsagePurpose, IsCa, Issuer,
    KeyPair, date_time_ymd,
};
use rustls::pki_types::{CertificateDer, PrivateKeyDer, ServerName};
use rustls::{ClientConfig, ClientConnection, RootCertStore, ServerConnection};
use std::io::{Cursor, Read, Write};
use std::sync::Arc;

struct Authority {
    cert: Certificate,
    issuer: Issuer<'static, KeyPair>,
}
fn authority() -> Authority {
    let key = KeyPair::generate().unwrap();
    let mut params = CertificateParams::new(vec!["ca.example.test".into()]).unwrap();
    params.is_ca = IsCa::Ca(BasicConstraints::Unconstrained);
    params.not_before = date_time_ymd(2020, 1, 1);
    params.not_after = date_time_ymd(4096, 1, 1);
    let cert = params.self_signed(&key).unwrap();
    Authority {
        cert,
        issuer: Issuer::new(params, key),
    }
}
fn leaf(ca: &Authority, server: bool, dates: Option<(i32, i32)>) -> (Vec<u8>, Vec<u8>) {
    let key = KeyPair::generate().unwrap();
    let mut params = CertificateParams::new(vec![
        if server {
            "babel.example.test"
        } else {
            "client.example.test"
        }
        .into(),
    ])
    .unwrap();
    params.extended_key_usages = vec![if server {
        ExtendedKeyUsagePurpose::ServerAuth
    } else {
        ExtendedKeyUsagePurpose::ClientAuth
    }];
    let (start, end) = dates.unwrap_or((2020, 4096));
    params.not_before = date_time_ymd(start, 1, 1);
    params.not_after = date_time_ymd(end, 1, 1);
    let cert = params.signed_by(&key, &ca.issuer).unwrap();
    (cert.der().to_vec(), key.serialize_der())
}
fn client(
    ca: &Authority,
    credential: Option<(Vec<u8>, Vec<u8>)>,
    hostname: &str,
    version: &'static rustls::SupportedProtocolVersion,
) -> ClientConnection {
    let mut roots = RootCertStore::empty();
    roots.add(ca.cert.der().clone()).unwrap();
    let builder =
        ClientConfig::builder_with_provider(Arc::new(rustls::crypto::ring::default_provider()))
            .with_protocol_versions(&[version])
            .unwrap()
            .with_root_certificates(roots);
    let config = match credential {
        Some((cert, key)) => builder
            .with_client_auth_cert(
                vec![CertificateDer::from(cert)],
                PrivateKeyDer::try_from(key).unwrap(),
            )
            .unwrap(),
        None => builder.with_no_client_auth(),
    };
    ClientConnection::new(
        Arc::new(config),
        ServerName::try_from(hostname.to_owned()).unwrap(),
    )
    .unwrap()
}
fn pump(c: &mut ClientConnection, s: &mut ServerConnection) -> Result<(), rustls::Error> {
    for _ in 0..32 {
        let mut wire = Vec::new();
        c.write_tls(&mut wire).unwrap();
        assert!(wire.len() <= MAX_WIRE_BYTES);
        s.read_tls(&mut Cursor::new(wire)).unwrap();
        s.process_new_packets()?;
        let mut wire = Vec::new();
        s.write_tls(&mut wire).unwrap();
        assert!(wire.len() <= MAX_WIRE_BYTES);
        c.read_tls(&mut Cursor::new(wire)).unwrap();
        c.process_new_packets()?;
        if !c.is_handshaking() && !s.is_handshaking() {
            return Ok(());
        }
    }
    panic!("bounded synthetic handshake did not finish")
}
#[test]
fn tls12_and_tls13_mutual_authenticate_and_export_matching_scoped_keys() {
    let ca = authority();
    let (cert, key) = leaf(&ca, true, None);
    let config = server_config(cert, key, ca.cert.der().to_vec()).unwrap();
    assert_eq!(config.max_early_data_size, 0);
    assert_eq!(config.send_tls13_tickets, 0);
    assert!(!config.session_storage.can_cache());
    assert!(!config.ticketer.enabled());
    for version in [&rustls::version::TLS12, &rustls::version::TLS13] {
        let mut c = client(
            &ca,
            Some(leaf(&ca, false, None)),
            "babel.example.test",
            version,
        );
        let mut s = ServerConnection::new(config.clone()).unwrap();
        pump(&mut c, &mut s).unwrap();
        assert!(s.peer_certificates().is_some());
        assert_eq!(c.protocol_version(), s.protocol_version());
        let a = c
            .export_keying_material([0u8; 32], b"EXPORTER-Babel-Lab", Some(b"scope-a"))
            .unwrap();
        let b = s
            .export_keying_material([0u8; 32], b"EXPORTER-Babel-Lab", Some(b"scope-a"))
            .unwrap();
        let different = s
            .export_keying_material([0u8; 32], b"EXPORTER-Babel-Lab", Some(b"scope-b"))
            .unwrap();
        assert!(a == b && a != different); // Never print exported material.
        c.writer().write_all(REQUEST).unwrap();
        pump(&mut c, &mut s).unwrap();
        let mut received = [0u8; 64];
        let n = s.reader().read(&mut received).unwrap();
        assert_eq!(&received[..n], REQUEST);
    }
}
#[test]
fn missing_untrusted_expired_future_or_wrong_purpose_client_certificates_fail() {
    let ca = authority();
    let stranger = authority();
    let (cert, key) = leaf(&ca, true, None);
    let config = server_config(cert, key, ca.cert.der().to_vec()).unwrap();
    let credentials = [
        None,
        Some(leaf(&stranger, false, None)),
        Some(leaf(&ca, false, Some((2000, 2001)))),
        Some(leaf(&ca, false, Some((4095, 4096)))),
        Some(leaf(&ca, true, None)),
    ];
    for credential in credentials {
        let mut c = client(
            &ca,
            credential,
            "babel.example.test",
            &rustls::version::TLS13,
        );
        let mut s = ServerConnection::new(config.clone()).unwrap();
        assert!(pump(&mut c, &mut s).is_err());
    }
}
#[test]
fn server_identity_root_validity_and_purpose_fail_closed() {
    for mode in 0..5 {
        let ca = authority();
        let stranger = authority();
        let (cert, key) = leaf(
            &ca,
            mode != 4,
            match mode {
                2 => Some((2000, 2001)),
                3 => Some((4095, 4096)),
                _ => None,
            },
        );
        let config = server_config(cert, key, ca.cert.der().to_vec()).unwrap();
        let mut c = client(
            if mode == 1 { &stranger } else { &ca },
            Some(leaf(&ca, false, None)),
            if mode == 0 {
                "wrong.example.test"
            } else if mode == 4 {
                "client.example.test"
            } else {
                "babel.example.test"
            },
            &rustls::version::TLS13,
        );
        let mut s = ServerConnection::new(config).unwrap();
        assert!(pump(&mut c, &mut s).is_err());
    }
}
#[test]
fn invalid_bounded_configuration_never_exposes_key_material() {
    let ca = authority();
    let (cert, key) = leaf(&ca, true, None);
    let (_, wrong_key) = leaf(&ca, true, None);
    let inputs = [
        (vec![], key.clone(), ca.cert.der().to_vec()),
        (
            vec![0; MAX_DER_BYTES + 1],
            key.clone(),
            ca.cert.der().to_vec(),
        ),
        (
            cert.clone(),
            b"synthetic-invalid-key".to_vec(),
            ca.cert.der().to_vec(),
        ),
        (cert.clone(), wrong_key, ca.cert.der().to_vec()),
        (cert, key, vec![1, 2, 3]),
    ];
    for (cert, key, root) in inputs {
        let error = server_config(cert, key, root).unwrap_err();
        assert!(!error.contains("synthetic-invalid-key"));
    }
}
#[test]
fn encrypted_record_tampering_is_not_plaintext_success() {
    let ca = authority();
    let (cert, key) = leaf(&ca, true, None);
    let mut s =
        ServerConnection::new(server_config(cert, key, ca.cert.der().to_vec()).unwrap()).unwrap();
    let mut c = client(
        &ca,
        Some(leaf(&ca, false, None)),
        "babel.example.test",
        &rustls::version::TLS13,
    );
    pump(&mut c, &mut s).unwrap();
    c.writer().write_all(REQUEST).unwrap();
    let mut wire = Vec::new();
    c.write_tls(&mut wire).unwrap();
    *wire.last_mut().unwrap() ^= 1;
    s.read_tls(&mut Cursor::new(wire)).unwrap();
    assert!(s.process_new_packets().is_err());
}
proptest! {
    #![proptest_config(ProptestConfig::with_cases(64))]
    #[test]
    fn arbitrary_short_records_are_bounded(data in prop::collection::vec(any::<u8>(),0..4096)) {
        let ca=authority(); let (cert,key)=leaf(&ca,true,None);
        let mut s=ServerConnection::new(server_config(cert,key,ca.cert.der().to_vec()).unwrap()).unwrap();
        s.set_buffer_limit(Some(4096));
        let mut cursor=Cursor::new(data); let _=s.read_tls(&mut cursor); let _=s.process_new_packets();
        prop_assert!(cursor.position()<=4096);
    }
}

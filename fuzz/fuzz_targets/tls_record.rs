#![no_main]
use libfuzzer_sys::fuzz_target;
use rcgen::{BasicConstraints, CertificateParams, ExtendedKeyUsagePurpose, IsCa, Issuer, KeyPair};
use std::io::Cursor;
use std::sync::{Arc, LazyLock};

static FIXTURE: LazyLock<(Vec<u8>, Vec<u8>, Vec<u8>)> = LazyLock::new(|| {
    let root_key = KeyPair::generate().expect("synthetic fuzz key");
    let mut root = CertificateParams::new(vec!["ca.example.test".into()]).expect("synthetic name");
    root.is_ca = IsCa::Ca(BasicConstraints::Unconstrained);
    let root_cert = root.self_signed(&root_key).expect("synthetic root");
    let issuer = Issuer::new(root, root_key);
    let key = KeyPair::generate().expect("synthetic fuzz key");
    let mut leaf =
        CertificateParams::new(vec!["babel.example.test".into()]).expect("synthetic name");
    leaf.extended_key_usages = vec![ExtendedKeyUsagePurpose::ServerAuth];
    let cert = leaf
        .signed_by(&key, &issuer)
        .expect("synthetic certificate");
    (
        cert.der().to_vec(),
        key.serialize_der(),
        root_cert.der().to_vec(),
    )
});
static CONFIG: LazyLock<Arc<rustls::ServerConfig>> = LazyLock::new(|| {
    babel_tls_lab::server_config(FIXTURE.0.clone(), FIXTURE.1.clone(), FIXTURE.2.clone())
        .expect("synthetic config")
});

fuzz_target!(|input: &[u8]| {
    let input = &input[..input.len().min(16384)];
    let _ = babel_tls_lab::revocation_config(
        FIXTURE.0.clone(),
        FIXTURE.1.clone(),
        FIXTURE.2.clone(),
        input.to_vec(),
    );
    let mut connection =
        rustls::ServerConnection::new(CONFIG.clone()).expect("qualified lab config");
    connection.set_buffer_limit(Some(4096));
    let mut cursor = Cursor::new(input);
    for _ in 0..32 {
        match connection.read_tls(&mut cursor) {
            Ok(0) | Err(_) => break,
            Ok(_) => {
                if connection.process_new_packets().is_err() {
                    break;
                }
            }
        }
        if cursor.position() as usize >= input.len() {
            break;
        }
    }
    assert!(cursor.position() as usize <= input.len());
});

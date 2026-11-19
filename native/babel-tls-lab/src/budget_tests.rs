use super::*;
use std::net::TcpListener;

fn pair() -> (TcpStream, TcpStream) {
    let listener = TcpListener::bind(("127.0.0.1", 0)).unwrap();
    let client = TcpStream::connect(listener.local_addr().unwrap()).unwrap();
    (listener.accept().unwrap().0, client)
}
#[test]
fn io_budgets_and_deadlines_bound_each_direction() {
    let (socket, mut peer) = pair();
    let mut bounded = BudgetStream {
        socket,
        deadline: Instant::now() + Duration::from_secs(2),
        read_left: 1,
        write_left: 1,
    };
    peer.write_all(b"ab").unwrap();
    assert_eq!(bounded.read(&mut [0; 2]).unwrap(), 1);
    assert_eq!(
        bounded.read(&mut [0; 1]).unwrap_err().kind(),
        io::ErrorKind::InvalidData
    );
    assert_eq!(bounded.write(b"xy").unwrap(), 1);
    bounded.flush().unwrap();
    let mut received = [0];
    peer.read_exact(&mut received).unwrap();
    assert_eq!(received, *b"x");
    assert_eq!(
        bounded.write(b"z").unwrap_err().kind(),
        io::ErrorKind::InvalidData
    );
    bounded.read_left = 1;
    bounded.write_left = 1;
    bounded.deadline = Instant::now();
    assert_eq!(
        bounded.read(&mut [0; 1]).unwrap_err().kind(),
        io::ErrorKind::TimedOut
    );
    assert_eq!(
        bounded.write(b"z").unwrap_err().kind(),
        io::ErrorKind::TimedOut
    );
    assert_eq!(bounded.flush().unwrap_err().kind(), io::ErrorKind::TimedOut);
}

#[derive(Debug)]
struct NoEntropy;
impl rustls::crypto::SecureRandom for NoEntropy {
    fn fill(&self, _: &mut [u8]) -> Result<(), rustls::crypto::GetRandomFailed> {
        Err(rustls::crypto::GetRandomFailed)
    }
}
#[derive(Debug)]
struct NoKeys;
#[derive(Debug)]
struct NoClock;
impl rustls::time_provider::TimeProvider for NoClock {
    fn current_time(&self) -> Option<rustls::pki_types::UnixTime> {
        None
    }
}
impl rustls::crypto::KeyProvider for NoKeys {
    fn load_private_key(
        &self,
        _: PrivateKeyDer<'static>,
    ) -> Result<Arc<dyn rustls::sign::SigningKey>, rustls::Error> {
        Err(rustls::Error::General("synthetic key-provider loss".into()))
    }
}
#[derive(Debug)]
struct UnavailableSigner;
#[derive(Debug)]
struct FailedKey(Arc<dyn rustls::sign::SigningKey>);
#[derive(Debug)]
struct FailedSignature(rustls::SignatureScheme);
impl rustls::crypto::KeyProvider for UnavailableSigner {
    fn load_private_key(
        &self,
        key: PrivateKeyDer<'static>,
    ) -> Result<Arc<dyn rustls::sign::SigningKey>, rustls::Error> {
        Ok(Arc::new(FailedKey(
            ring_provider().key_provider.load_private_key(key)?,
        )))
    }
}
impl rustls::sign::SigningKey for FailedKey {
    fn choose_scheme(
        &self,
        offered: &[rustls::SignatureScheme],
    ) -> Option<Box<dyn rustls::sign::Signer>> {
        self.0
            .choose_scheme(offered)
            .map(|s| Box::new(FailedSignature(s.scheme())) as Box<dyn rustls::sign::Signer>)
    }
    fn public_key(&self) -> Option<rustls::pki_types::SubjectPublicKeyInfoDer<'_>> {
        self.0.public_key()
    }
    fn algorithm(&self) -> rustls::SignatureAlgorithm {
        self.0.algorithm()
    }
}
impl rustls::sign::Signer for FailedSignature {
    fn sign(&self, _: &[u8]) -> Result<Vec<u8>, rustls::Error> {
        Err(rustls::Error::General(
            "synthetic signer unavailable".into(),
        ))
    }
    fn scheme(&self) -> rustls::SignatureScheme {
        self.0
    }
}

#[test]
fn entropy_clock_key_loading_and_live_signing_loss_never_complete_authentication() {
    use rcgen::{
        BasicConstraints, CertificateParams, ExtendedKeyUsagePurpose, IsCa, Issuer, KeyPair,
    };
    use rustls::{ClientConfig, ClientConnection, ServerConnection};
    use std::io::Cursor;
    let root_key = KeyPair::generate().unwrap();
    let mut params = CertificateParams::new(vec!["ca.example.test".into()]).unwrap();
    params.is_ca = IsCa::Ca(BasicConstraints::Unconstrained);
    let root = params.self_signed(&root_key).unwrap();
    let issuer = Issuer::new(params, root_key);
    let make_leaf = |server: bool| {
        let key = KeyPair::generate().unwrap();
        let mut params = CertificateParams::new(vec!["babel.example.test".into()]).unwrap();
        params.extended_key_usages = vec![if server {
            ExtendedKeyUsagePurpose::ServerAuth
        } else {
            ExtendedKeyUsagePurpose::ClientAuth
        }];
        (
            params.signed_by(&key, &issuer).unwrap().der().to_vec(),
            key.serialize_der(),
        )
    };
    let (cert, key) = make_leaf(true);
    for fault in 0..4 {
        let mut provider = ring_provider();
        if fault == 0 {
            provider.secure_random = &NoEntropy;
        }
        if fault == 1 {
            provider.key_provider = &NoKeys;
        }
        if fault == 2 {
            provider.key_provider = &UnavailableSigner;
        }
        let candidate = configure(
            cert.clone(),
            key.clone(),
            root.der().to_vec(),
            None,
            provider,
        );
        if fault == 1 {
            assert_eq!(
                candidate.unwrap_err(),
                "certificate/key configuration rejected"
            );
            continue;
        }
        let mut config = candidate.unwrap();
        if fault == 3 {
            Arc::get_mut(&mut config).unwrap().time_provider = Arc::new(NoClock);
        }
        let mut server = ServerConnection::new(config).unwrap();
        let mut roots = RootCertStore::empty();
        roots.add(root.der().clone()).unwrap();
        let (client_cert, client_key) = make_leaf(false);
        let config = ClientConfig::builder_with_provider(Arc::new(ring_provider()))
            .with_protocol_versions(&[&rustls::version::TLS13])
            .unwrap()
            .with_root_certificates(roots)
            .with_client_auth_cert(
                vec![CertificateDer::from(client_cert)],
                PrivateKeyDer::try_from(client_key).unwrap(),
            )
            .unwrap();
        let mut client =
            ClientConnection::new(Arc::new(config), "babel.example.test".try_into().unwrap())
                .unwrap();
        let mut failed = false;
        for _ in 0..16 {
            let mut wire = Vec::new();
            client.write_tls(&mut wire).unwrap();
            server.read_tls(&mut Cursor::new(wire)).unwrap();
            if server.process_new_packets().is_err() {
                failed = true;
                break;
            }
            let mut wire = Vec::new();
            server.write_tls(&mut wire).unwrap();
            client.read_tls(&mut Cursor::new(wire)).unwrap();
            client.process_new_packets().unwrap();
        }
        assert!(
            failed,
            "provider fault must fail within the bounded handshake"
        );
        assert!(server.is_handshaking());
        assert!(channel_binding(&server).is_err());
        let mut plaintext = [0; 64];
        assert!(server.reader().read(&mut plaintext).is_err());
    }
}

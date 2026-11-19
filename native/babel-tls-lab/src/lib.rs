//! Bounded TLS qualification experiment; no LDAP, credentials or production service.
#![forbid(unsafe_code)]

use rustls::pki_types::{CertificateDer, CertificateRevocationListDer, PrivateKeyDer};
use rustls::{RootCertStore, ServerConfig};
use std::sync::Arc;

pub const MAX_DER_BYTES: usize = 16_384;
pub const MAX_WIRE_BYTES: usize = 65_536;
pub const MAX_APPLICATION_BYTES: usize = 64;

/// Explicit roots, mutual authentication and TLS 1.2/1.3; no bypass verifier.
pub fn server_config(
    certificate: Vec<u8>,
    key: Vec<u8>,
    client_root: Vec<u8>,
) -> Result<Arc<ServerConfig>, &'static str> {
    configure(certificate, key, client_root, None, ring_provider())
}

/// A strict leaf-CRL profile for the lab's direct-issuer certificate chain.
pub fn revocation_config(
    certificate: Vec<u8>,
    key: Vec<u8>,
    client_root: Vec<u8>,
    crl: Vec<u8>,
) -> Result<Arc<ServerConfig>, &'static str> {
    if crl.is_empty() || crl.len() > MAX_DER_BYTES {
        return Err("bounded CRL required");
    }
    configure(certificate, key, client_root, Some(crl), ring_provider())
}

fn ring_provider() -> rustls::crypto::CryptoProvider {
    let mut provider = rustls::crypto::ring::default_provider();
    provider.cipher_suites.retain(|suite| {
        matches!(
            suite.suite(),
            rustls::CipherSuite::TLS13_AES_256_GCM_SHA384
                | rustls::CipherSuite::TLS13_AES_128_GCM_SHA256
                | rustls::CipherSuite::TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
                | rustls::CipherSuite::TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
                | rustls::CipherSuite::TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
                | rustls::CipherSuite::TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
        )
    });
    provider
}

fn configure(
    certificate: Vec<u8>,
    key: Vec<u8>,
    client_root: Vec<u8>,
    crl: Option<Vec<u8>>,
    provider: rustls::crypto::CryptoProvider,
) -> Result<Arc<ServerConfig>, &'static str> {
    if [&certificate, &key, &client_root]
        .iter()
        .any(|v| v.is_empty() || v.len() > MAX_DER_BYTES)
    {
        return Err("bounded DER inputs required");
    }
    let provider = Arc::new(provider);
    let mut roots = RootCertStore::empty();
    roots
        .add(CertificateDer::from(client_root))
        .map_err(|_| "invalid client trust root")?;
    let mut verifier = rustls::server::WebPkiClientVerifier::builder_with_provider(
        Arc::new(roots),
        provider.clone(),
    );
    if let Some(crl) = crl {
        verifier = verifier
            .with_crls(vec![CertificateRevocationListDer::from(crl)])
            .only_check_end_entity_revocation()
            .enforce_revocation_expiration();
        // Unknown status remains denied; no allow_unknown_revocation_status call.
    }
    let verifier = verifier
        .build()
        .map_err(|_| "client verification configuration rejected")?;
    let key = PrivateKeyDer::try_from(key).map_err(|_| "invalid private key encoding")?;
    let mut config = ServerConfig::builder_with_provider(provider)
        .with_protocol_versions(&[&rustls::version::TLS13, &rustls::version::TLS12])
        .map_err(|_| "protocol configuration rejected")?
        .with_client_cert_verifier(verifier)
        .with_single_cert(vec![CertificateDer::from(certificate)], key)
        .map_err(|_| "certificate/key configuration rejected")?;
    config.max_fragment_size = Some(4096);
    config.session_storage = Arc::new(rustls::server::NoServerSessionStorage {});
    config.send_tls13_tickets = 0;
    config.max_early_data_size = 0;
    Ok(Arc::new(config))
}

/// Complete configuration replacement, retaining the old value on validation failure.
/// Existing connections keep their Arc; revocation is enforced on new handshakes.
pub struct ConfigSlot(Arc<ServerConfig>);
impl ConfigSlot {
    pub fn new(config: Arc<ServerConfig>) -> Self {
        Self(config)
    }
    pub fn current(&self) -> Arc<ServerConfig> {
        self.0.clone()
    }
    pub fn replace(
        &mut self,
        candidate: Result<Arc<ServerConfig>, &'static str>,
    ) -> Result<(), &'static str> {
        self.0 = candidate?;
        Ok(())
    }
}

pub const BINDING_REQUEST: &[u8] = b"BABEL-TLS-CB\n";
pub const BINDING_LABEL: &[u8] = b"EXPORTER-Channel-Binding";

/// RFC 9266 tls-exporter for this TLS 1.3-only binding experiment.
/// It is not LDAP/SASL/EPA or tls-server-end-point.
pub fn channel_binding(connection: &rustls::ServerConnection) -> Result<[u8; 32], &'static str> {
    if connection.is_handshaking()
        || connection.protocol_version() != Some(rustls::ProtocolVersion::TLSv1_3)
    {
        return Err("binding requires a completed TLS 1.3 handshake");
    }
    connection
        .export_keying_material([0; 32], BINDING_LABEL, None)
        .map_err(|_| "binding unavailable")
}

use std::io::{self, Read, Write};
use std::net::TcpStream;
use std::time::{Duration, Instant};

pub const REQUEST: &[u8] = b"BABEL-TLS-LAB\n";
pub const RESPONSE: &[u8] = b"verified lab session\n";

struct BudgetStream {
    socket: TcpStream,
    deadline: Instant,
    read_left: usize,
    write_left: usize,
}

impl BudgetStream {
    fn timeout(&self) -> io::Result<Duration> {
        self.deadline
            .checked_duration_since(Instant::now())
            .filter(|d| !d.is_zero())
            .ok_or_else(|| io::Error::new(io::ErrorKind::TimedOut, "lab deadline"))
    }
}
impl Read for BudgetStream {
    fn read(&mut self, buffer: &mut [u8]) -> io::Result<usize> {
        if self.read_left == 0 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "lab read budget",
            ));
        }
        self.socket.set_read_timeout(Some(self.timeout()?))?;
        let limit = buffer.len().min(self.read_left).min(8192);
        let count = self.socket.read(&mut buffer[..limit])?;
        self.read_left -= count;
        Ok(count)
    }
}
impl Write for BudgetStream {
    fn write(&mut self, buffer: &[u8]) -> io::Result<usize> {
        if self.write_left == 0 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "lab write budget",
            ));
        }
        self.socket.set_write_timeout(Some(self.timeout()?))?;
        let count = self
            .socket
            .write(&buffer[..buffer.len().min(self.write_left)])?;
        self.write_left -= count;
        Ok(count)
    }
    fn flush(&mut self) -> io::Result<()> {
        self.timeout()?;
        self.socket.flush()
    }
}

/// Exactly one bounded, authenticated test message. No directory operation exists.
pub fn exchange(
    socket: TcpStream,
    config: Arc<ServerConfig>,
    timeout: Duration,
) -> Result<&'static str, &'static str> {
    if !socket
        .peer_addr()
        .map_err(|_| "peer unavailable")?
        .ip()
        .is_loopback()
    {
        return Err("loopback peers only");
    }
    let mut connection =
        rustls::ServerConnection::new(config).map_err(|_| "TLS configuration rejected")?;
    connection.set_buffer_limit(Some(4096));
    let wire = BudgetStream {
        socket,
        deadline: Instant::now() + timeout,
        read_left: MAX_WIRE_BYTES,
        write_left: MAX_WIRE_BYTES,
    };
    let mut stream = rustls::StreamOwned::new(connection, wire);
    let mut request = Vec::new();
    while !request.contains(&b'\n') {
        let mut buffer = [0u8; MAX_APPLICATION_BYTES + 1];
        let count = stream
            .read(&mut buffer)
            .map_err(|_| "TLS exchange rejected")?;
        if count == 0 {
            return Err("incomplete lab request");
        }
        request.extend_from_slice(&buffer[..count]);
        if request.len() > MAX_APPLICATION_BYTES {
            return Err("lab application budget");
        }
    }
    if request.starts_with(BINDING_REQUEST) {
        let size = BINDING_REQUEST.len() + 32;
        if request.len() > size {
            return Err("invalid binding length");
        }
        let received = request.len();
        request.resize(size, 0);
        stream
            .read_exact(&mut request[received..])
            .map_err(|_| "incomplete binding")?;
        let expected = channel_binding(&stream.conn)?;
        if request[BINDING_REQUEST.len()..] != expected {
            return Err("channel binding mismatch");
        }
    } else if request != REQUEST {
        return Err("invalid lab request");
    }
    if stream
        .conn
        .peer_certificates()
        .is_none_or(|chain| chain.is_empty())
    {
        return Err("client authentication required");
    }
    let version = match stream.conn.protocol_version() {
        Some(rustls::ProtocolVersion::TLSv1_3) => "TLS1.3",
        Some(rustls::ProtocolVersion::TLSv1_2) => "TLS1.2",
        _ => return Err("unqualified protocol"),
    };
    stream
        .write_all(RESPONSE)
        .and_then(|_| stream.flush())
        .map_err(|_| "TLS response rejected")?;
    stream.conn.send_close_notify();
    stream
        .conn
        .complete_io(&mut stream.sock)
        .map_err(|_| "TLS close rejected")?;
    Ok(version)
}

#[cfg(test)]
mod budget_tests;

//! Bounded TLS qualification experiment; no LDAP, credentials or production service.
#![forbid(unsafe_code)]

use rustls::pki_types::{CertificateDer, PrivateKeyDer};
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
    if [&certificate, &key, &client_root]
        .iter()
        .any(|v| v.is_empty() || v.len() > MAX_DER_BYTES)
    {
        return Err("bounded DER inputs required");
    }
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
    let provider = Arc::new(provider);
    let mut roots = RootCertStore::empty();
    roots
        .add(CertificateDer::from(client_root))
        .map_err(|_| "invalid client trust root")?;
    let verifier = rustls::server::WebPkiClientVerifier::builder_with_provider(
        Arc::new(roots),
        provider.clone(),
    )
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
    if request != REQUEST {
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

//! One-session loopback-only qualification probe. Never a production service.
#![forbid(unsafe_code)]

use babel_tls_lab::{MAX_DER_BYTES, exchange, server_config};
use std::io::{Read, Write};
use std::net::TcpListener;
use std::path::Path;
use std::time::{Duration, Instant};

fn load(path: &str) -> Result<Vec<u8>, &'static str> {
    let path = Path::new(path);
    if path.is_symlink() || !path.is_file() {
        return Err("regular DER file required");
    }
    let file = std::fs::File::open(path).map_err(|_| "DER file unavailable")?;
    let mut bytes = Vec::new();
    file.take((MAX_DER_BYTES + 1) as u64)
        .read_to_end(&mut bytes)
        .map_err(|_| "DER read rejected")?;
    if bytes.is_empty() || bytes.len() > MAX_DER_BYTES {
        return Err("bounded DER file required");
    }
    Ok(bytes)
}
fn run() -> Result<(), &'static str> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() == 1 && args[0] == "--scope" {
        println!(
            "Loopback-only mutual TLS qualification lab; no LDAP, identity or production service."
        );
        return Ok(());
    }
    if args.len() != 3 {
        return Err("usage: babel-tls-lab SERVER_CERT_DER SERVER_KEY_DER CLIENT_CA_DER");
    }
    let config = server_config(load(&args[0])?, load(&args[1])?, load(&args[2])?)?;
    let listener = TcpListener::bind(("127.0.0.1", 0)).map_err(|_| "lab bind failed")?;
    listener
        .set_nonblocking(true)
        .map_err(|_| "lab listener setup failed")?;
    println!(
        "LISTEN {}",
        listener
            .local_addr()
            .map_err(|_| "lab address unavailable")?
    );
    std::io::stdout()
        .flush()
        .map_err(|_| "lab announcement failed")?;
    let deadline = Instant::now() + Duration::from_secs(5);
    let socket = loop {
        match listener.accept() {
            Ok((socket, _)) => break socket,
            Err(error)
                if error.kind() == std::io::ErrorKind::WouldBlock && Instant::now() < deadline =>
            {
                std::thread::sleep(Duration::from_millis(5))
            }
            Err(_) => return Err("lab accept deadline or failure"),
        }
    };
    let protocol = exchange(socket, config, Duration::from_secs(2))?;
    println!("VERIFIED {protocol} mutual-authenticated synthetic-lab-only");
    Ok(())
}
fn main() {
    if let Err(error) = run() {
        eprintln!("TLS lab rejected: {error}");
        std::process::exit(1);
    }
}

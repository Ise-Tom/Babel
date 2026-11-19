//! Bounded loopback-only qualification probe. Never a production service.
#![forbid(unsafe_code)]

use babel_tls_lab::{ConfigSlot, MAX_DER_BYTES, exchange, revocation_config, server_config};
use std::io::{Read, Write};
use std::net::TcpListener;
use std::os::unix::fs::PermissionsExt;
use std::path::Path;
use std::time::{Duration, Instant};

fn load(path: &str, private: bool) -> Result<Vec<u8>, &'static str> {
    let path = Path::new(path);
    if path.is_symlink() || !path.is_file() {
        return Err("regular DER file required");
    }
    let file = std::fs::File::open(path).map_err(|_| "DER file unavailable")?;
    let metadata = file.metadata().map_err(|_| "DER metadata unavailable")?;
    if !metadata.is_file() || (private && metadata.permissions().mode() & 0o077 != 0) {
        return Err("private DER must have owner-only permissions");
    }
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
    if args.len() < 3 {
        return Err("usage: babel-tls-lab CERT KEY CLIENT_CA [--crl DER] [--replace CERT KEY]");
    }
    let mut crl = None;
    let mut replacement = None;
    let mut index = 3;
    while index < args.len() {
        match args[index].as_str() {
            "--crl" if crl.is_none() && index + 1 < args.len() => {
                crl = Some(args[index + 1].as_str());
                index += 2;
            }
            "--replace" if replacement.is_none() && index + 2 < args.len() => {
                replacement = Some((args[index + 1].as_str(), args[index + 2].as_str()));
                index += 3;
            }
            _ => return Err("invalid lab options"),
        }
    }
    let configure = |cert: &str, key: &str| {
        let (cert, key, root) = (load(cert, false)?, load(key, true)?, load(&args[2], false)?);
        match crl {
            Some(path) => revocation_config(cert, key, root, load(path, false)?),
            None => server_config(cert, key, root),
        }
    };
    let mut slot = ConfigSlot::new(configure(&args[0], &args[1])?);
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
    let sessions = if replacement.is_some() { 2 } else { 1 };
    for session in 0..sessions {
        let deadline = Instant::now() + Duration::from_secs(5);
        let socket = loop {
            match listener.accept() {
                Ok((socket, _)) => break socket,
                Err(error)
                    if error.kind() == std::io::ErrorKind::WouldBlock
                        && Instant::now() < deadline =>
                {
                    std::thread::sleep(Duration::from_millis(5))
                }
                Err(_) => return Err("lab accept deadline or failure"),
            }
        };
        let protocol = exchange(socket, slot.current(), Duration::from_secs(2))?;
        println!("VERIFIED {protocol} mutual-authenticated synthetic-lab-only");
        if session == 0
            && let Some((cert, key)) = replacement
        {
            slot.replace(configure(cert, key))?;
        }
    }
    Ok(())
}
fn main() {
    if let Err(error) = run() {
        eprintln!("TLS lab rejected: {error}");
        std::process::exit(1);
    }
}

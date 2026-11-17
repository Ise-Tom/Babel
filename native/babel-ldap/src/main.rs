#![forbid(unsafe_code)]
use std::net::SocketAddr;

fn run() -> Result<(), String> {
    let mut address: SocketAddr = "127.0.0.1:1389"
        .parse()
        .map_err(|_| "invalid default address")?;
    let mut limit = None;
    let mut args = std::env::args().skip(1);
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--help" => {
                println!(
                    "babel-ldap: public RootDSE lab only; no credentials or AD capability\n--listen LOOPBACK:PORT [--max-connections N]"
                );
                return Ok(());
            }
            "--listen" => {
                address = args
                    .next()
                    .ok_or("missing listen address")?
                    .parse()
                    .map_err(|_| "invalid listen address")?;
            }
            "--max-connections" => {
                let value: usize = args
                    .next()
                    .ok_or("missing connection count")?
                    .parse()
                    .map_err(|_| "invalid connection count")?;
                if value == 0 || value > 10000 {
                    return Err("connection count must be 1..10000".into());
                }
                limit = Some(value);
            }
            _ => return Err("unsupported argument (use --help)".into()),
        }
    }
    babel_ldap::server::serve(address, limit).map_err(|e| e.to_string())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(1);
    }
}

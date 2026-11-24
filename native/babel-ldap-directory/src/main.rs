#![forbid(unsafe_code)]

use std::error::Error;
use std::net::SocketAddr;
use std::num::NonZeroUsize;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args().skip(1);
    let address: SocketAddr = args.next().as_deref().unwrap_or("127.0.0.1:0").parse()?;
    let count = args
        .next()
        .map(|arg| arg.parse::<NonZeroUsize>())
        .transpose()?;
    if args.next().is_some() {
        return Err("usage: babel-ldap-directory [LOOPBACK:PORT] [MAX_CONNECTIONS]".into());
    }
    babel_ldap_directory::serve(address, count.map(NonZeroUsize::get))?;
    Ok(())
}

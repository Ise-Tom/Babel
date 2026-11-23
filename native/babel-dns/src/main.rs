#![forbid(unsafe_code)]

use std::error::Error;
use std::io::{self, Write};
use std::net::{SocketAddr, UdpSocket};
use std::num::NonZeroUsize;
use std::time::Instant;

fn main() -> Result<(), Box<dyn Error>> {
    let mut args = std::env::args().skip(1);
    let mut address: SocketAddr = "127.0.0.1:0".parse()?;
    let mut max_datagrams = usize::MAX;
    while let Some(flag) = args.next() {
        let value = args.next().ok_or("DNS listener option requires a value")?;
        match flag.as_str() {
            "--listen" => address = value.parse()?,
            "--max-datagrams" => max_datagrams = value.parse::<NonZeroUsize>()?.get(),
            _ => {
                return Err("usage: babel-dns [--listen LOOPBACK:PORT] [--max-datagrams N]".into());
            }
        }
    }
    if !address.ip().is_loopback() {
        return Err("DNS discovery lab must listen on loopback".into());
    }
    let socket = UdpSocket::bind(address)?;
    let clock = Instant::now();
    println!("LISTENING {}", socket.local_addr()?);
    io::stdout().flush()?;

    // Receive the full UDP datagram so oversize input cannot be mistaken for valid input.
    let mut packet = [0; 65_535];
    for _ in 0..max_datagrams {
        let (size, peer) = socket.recv_from(&mut packet)?;
        if let Some(response) = babel_dns::reply(&packet[..size], clock.elapsed().as_secs()) {
            socket.send_to(&response, peer)?;
        }
    }
    Ok(())
}

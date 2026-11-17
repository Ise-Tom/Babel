//! Single-connection-at-a-time laboratory transport with total session budgets.
use crate::{MAX_FRAME_BYTES, decode, respond};
use std::io::{self, Read, Write};
use std::net::{SocketAddr, TcpListener, TcpStream};
use std::time::{Duration, Instant};

pub const SESSION_BUDGET: Duration = Duration::from_secs(5);
pub const MAX_MESSAGES: usize = 32;

/// Read exactly one frame, rejecting oversized declarations before allocating a body.
pub fn read_frame(reader: &mut impl Read) -> io::Result<Option<Vec<u8>>> {
    let mut tag = [0u8];
    if reader.read(&mut tag)? == 0 {
        return Ok(None);
    }
    if tag[0] != 0x30 {
        return Err(io::Error::new(
            io::ErrorKind::InvalidData,
            "invalid LDAP frame",
        ));
    }
    let mut first = [0u8];
    reader.read_exact(&mut first)?;
    let mut header = vec![tag[0], first[0]];
    let length = if first[0] & 0x80 == 0 {
        usize::from(first[0])
    } else {
        let count = usize::from(first[0] & 0x7f);
        if count == 0 || count > 4 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "invalid BER length",
            ));
        }
        let mut length = 0usize;
        for _ in 0..count {
            let mut octet = [0u8];
            reader.read_exact(&mut octet)?;
            header.push(octet[0]);
            length = length
                .checked_mul(256)
                .and_then(|n| n.checked_add(usize::from(octet[0])))
                .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "invalid BER length"))?;
        }
        length
    };
    let total = header
        .len()
        .checked_add(length)
        .filter(|n| *n <= MAX_FRAME_BYTES)
        .ok_or_else(|| {
            io::Error::new(io::ErrorKind::InvalidData, "LDAP frame exceeds lab limit")
        })?;
    header.resize(total, 0);
    let offset = total - length;
    reader.read_exact(&mut header[offset..])?;
    Ok(Some(header))
}

struct DeadlineStream {
    stream: TcpStream,
    deadline: Instant,
}
impl DeadlineStream {
    fn remaining(&self) -> io::Result<Duration> {
        self.deadline
            .checked_duration_since(Instant::now())
            .filter(|d| !d.is_zero())
            .ok_or_else(|| io::Error::new(io::ErrorKind::TimedOut, "lab session budget exceeded"))
    }
}
impl Read for DeadlineStream {
    fn read(&mut self, buffer: &mut [u8]) -> io::Result<usize> {
        self.stream.set_read_timeout(Some(self.remaining()?))?;
        self.stream.read(buffer)
    }
}
impl Write for DeadlineStream {
    fn write(&mut self, buffer: &[u8]) -> io::Result<usize> {
        self.stream.set_write_timeout(Some(self.remaining()?))?;
        self.stream.write(buffer)
    }
    fn flush(&mut self) -> io::Result<()> {
        self.stream.flush()
    }
}

pub fn serve_connection(stream: TcpStream, budget: Duration) -> io::Result<()> {
    let mut stream = DeadlineStream {
        stream,
        deadline: Instant::now() + budget,
    };
    for _ in 0..MAX_MESSAGES {
        let Some(frame) = read_frame(&mut stream)? else {
            return Ok(());
        };
        let request = decode(&frame).map_err(|_| {
            io::Error::new(
                io::ErrorKind::InvalidData,
                "invalid or unsupported LDAP frame",
            )
        })?;
        let Some(reply) = respond(&request) else {
            return Ok(());
        };
        stream.write_all(&reply)?;
    }
    Ok(())
}

pub fn serve(address: SocketAddr, max_connections: Option<usize>) -> io::Result<()> {
    if !address.ip().is_loopback() {
        return Err(io::Error::new(
            io::ErrorKind::PermissionDenied,
            "lab listener must use loopback",
        ));
    }
    let listener = TcpListener::bind(address)?;
    println!("LISTENING {}", listener.local_addr()?);
    io::stdout().flush()?;
    let mut accepted = 0usize;
    while max_connections.is_none_or(|max| accepted < max) {
        let (stream, _) = listener.accept()?;
        accepted += 1;
        if serve_connection(stream, SESSION_BUDGET).is_err() {
            // Static diagnostic: never log a frame, DN, credential or peer payload.
            eprintln!("Lab connection closed: invalid, unsupported or expired session");
        }
    }
    Ok(())
}

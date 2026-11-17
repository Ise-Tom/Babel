use babel_ldap::server::{read_frame, serve, serve_connection};
use proptest::prelude::*;
use std::io::{Cursor, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;
use std::time::{Duration, Instant};

const BIND: &[u8] = &[0x30, 0x0c, 2, 1, 1, 0x60, 7, 2, 1, 3, 4, 0, 0x80, 0];

#[test]
fn framing_preserves_coalesced_messages_and_reports_clean_eof() {
    let mut wire = BIND.to_vec();
    wire.extend(BIND);
    let mut input = Cursor::new(wire);
    assert_eq!(read_frame(&mut input).unwrap().unwrap(), BIND);
    assert_eq!(read_frame(&mut input).unwrap().unwrap(), BIND);
    assert!(read_frame(&mut input).unwrap().is_none());
}

#[test]
fn oversized_declarations_and_indefinite_lengths_fail_before_body_allocation() {
    for frame in [
        vec![0x30, 0x84, 0xff, 0xff, 0xff, 0xff],
        vec![0x30, 0x80],
        vec![0x30, 0x85],
        vec![0x31],
    ] {
        assert!(read_frame(&mut Cursor::new(frame)).is_err());
    }
    for length in 1..BIND.len() {
        assert!(read_frame(&mut Cursor::new(&BIND[..length])).is_err());
    }
}

#[test]
fn long_definite_length_and_fragmented_input_are_supported() {
    let mut frame = vec![0x30, 0x81, 0x80];
    frame.extend([0u8; 128]);
    struct Fragments(Cursor<Vec<u8>>);
    impl Read for Fragments {
        fn read(&mut self, buffer: &mut [u8]) -> std::io::Result<usize> {
            let count = buffer.len().min(1);
            self.0.read(&mut buffer[..count])
        }
    }
    assert_eq!(
        read_frame(&mut Fragments(Cursor::new(frame.clone())))
            .unwrap()
            .unwrap(),
        frame
    );
}

#[test]
fn lab_service_cannot_bind_public_interfaces() {
    assert!(serve("0.0.0.0:0".parse().unwrap(), Some(0)).is_err());
    assert!(serve("[::]:0".parse().unwrap(), Some(0)).is_err());
}

#[test]
fn session_budget_stops_partial_or_idle_clients() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let client = TcpStream::connect(listener.local_addr().unwrap()).unwrap();
    let (stream, _) = listener.accept().unwrap();
    let start = Instant::now();
    let worker = thread::spawn(move || serve_connection(stream, Duration::from_millis(60)));
    assert!(worker.join().unwrap().is_err());
    assert!(start.elapsed() < Duration::from_secs(2));
    drop(client);
}

#[test]
fn real_socket_supports_bind_unbind_and_a_fixed_message_budget() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let mut client = TcpStream::connect(listener.local_addr().unwrap()).unwrap();
    client
        .set_read_timeout(Some(Duration::from_secs(2)))
        .unwrap();
    let (stream, _) = listener.accept().unwrap();
    let worker = thread::spawn(move || serve_connection(stream, Duration::from_secs(2)));
    client.write_all(BIND).unwrap();
    assert!(read_frame(&mut client).unwrap().is_some());
    client.write_all(&[0x30, 5, 2, 1, 2, 0x42, 0]).unwrap();
    assert!(worker.join().unwrap().is_ok());
    assert!(read_frame(&mut client).unwrap().is_none());

    let mut client = TcpStream::connect(listener.local_addr().unwrap()).unwrap();
    client
        .set_read_timeout(Some(Duration::from_secs(2)))
        .unwrap();
    let (stream, _) = listener.accept().unwrap();
    let worker = thread::spawn(move || serve_connection(stream, Duration::from_secs(2)));
    for _ in 0..babel_ldap::server::MAX_MESSAGES {
        client.write_all(BIND).unwrap();
        assert!(read_frame(&mut client).unwrap().is_some());
    }
    assert!(worker.join().unwrap().is_ok());
    assert!(read_frame(&mut client).unwrap().is_none());
}

proptest! {
    #[test]
    fn arbitrary_streams_never_allocate_oversized_frames(input in prop::collection::vec(any::<u8>(), 0..17000)) {
        if let Ok(Some(frame)) = read_frame(&mut Cursor::new(input)) {
            prop_assert!(frame.len() <= babel_ldap::MAX_FRAME_BYTES);
        }
    }
}

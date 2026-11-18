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

#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|input: &[u8]| {
    if let Ok(request) = babel_ldap::decode(input)
        && let Some(reply) = babel_ldap::respond(&request)
    {
        assert!(reply.len() <= 1024);
    }
    if let Ok(Some(frame)) = babel_ldap::server::read_frame(&mut std::io::Cursor::new(input)) {
        assert!(frame.len() <= babel_ldap::MAX_FRAME_BYTES);
    }
});

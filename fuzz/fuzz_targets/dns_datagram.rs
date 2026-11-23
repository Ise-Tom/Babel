#![no_main]
#![forbid(unsafe_code)]

use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Some(response) = babel_dns::reply(data, 0) {
        assert!((12..=512).contains(&response.len()));
        assert_eq!(response[..2], data[..2]);
        assert_ne!(response[2] & 0x80, 0);
    }
});

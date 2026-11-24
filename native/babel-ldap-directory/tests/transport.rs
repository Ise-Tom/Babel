use std::process::Command;

#[test]
fn directory_binary_refuses_non_loopback_and_zero_connection_limit() {
    for args in [["0.0.0.0:0", "1"], ["127.0.0.1:0", "0"]] {
        let output = Command::new(env!("CARGO_BIN_EXE_babel-ldap-directory"))
            .args(args)
            .output()
            .unwrap();
        assert!(!output.status.success());
        assert!(output.stdout.is_empty());
    }
}

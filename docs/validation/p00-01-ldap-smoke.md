# P00-01 local Babel LDAP smoke receipt

This project-owned receipt records the observed output of the existing
[independent LDAP smoke](../../native/babel-ldap/tests/smoke_ldap.py) on
23 November 2026 Paris time. It used the locked release binary on loopback and
the harness's built-in synthetic requests. The input hashes bind the requests
and dependency locks. This environment supplies no exact qualified guest image
and has no Windows reference target. Product comparison scenarios are recorded
separately in [the follow-up](p00-01-conformance.md).

~~~text
765a229c7ba1c64a8a592d74d60c9757235afe04
2026-11-22T23:53:12Z
Linux 6.18.33.2-microsoft-standard-WSL2 x86_64
Ubuntu 26.04 LTS
3.14.4
rustc 1.100.0 (0ef1bc386 2026-11-09)
ldap3 2.9.1
pyasn1 0.6.5
f9d7c93479ae65d4a2063965e0a88dc8dc6cbd0b2a10b6467958903e6bde4388  Cargo.lock
eea5a87a06fa1d64c13af7fc239eb3c3c412c950753fe1aea12ef1a413c99059  requirements-ci.txt
6dcd609532bc47fa8ac286b37f9154b6bab5834956c10eec5a63d2506e260261  native/babel-ldap/tests/smoke_ldap.py
f6e519b2818f99c7bef07d3b509d6ecf720a51cf8bb46e9d033269be837b0ea2  target/release/babel-ldap
LDAP smoke passed: RootDSE, credential/scope denial, malformed-peer recovery
~~~

The smoke exited 0 after all assertions. Anonymous base-scope RootDSE returned
one entry with LDAPv3 and vendor name Babel. The credential bind, unsupported
matching equality and subtree search each returned LDAP result 53, and a
nonexistent naming context returned 32. A second RootDSE read succeeded after
the peer rejection. The harness checked its diagnostics for credential
redaction.

Reproduce at the source revision above with the pinned Rust toolchain and the
hash-locked test client.

~~~sh
python -m pip install --require-hashes -r requirements-ci.txt -r requirements-ci.in
cargo build --locked --release -p babel-ldap
python native/babel-ldap/tests/smoke_ldap.py target/release/babel-ldap
~~~

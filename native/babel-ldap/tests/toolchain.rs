//! The qualified release profile must fail visibly instead of wrapping integers.
#![forbid(unsafe_code)]

#[test]
fn integer_overflow_is_detected_in_debug_and_release_profiles() {
    let result =
        std::panic::catch_unwind(|| std::hint::black_box(u64::MAX) + std::hint::black_box(1));
    assert!(
        result.is_err(),
        "qualified arithmetic must not silently wrap"
    );
}

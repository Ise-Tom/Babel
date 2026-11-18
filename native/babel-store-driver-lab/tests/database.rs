//! Real database tests, enabled explicitly by the owned-container harness.
use babel_store_driver_lab::{Failure, Session};
use std::path::PathBuf;
use std::time::Duration;
use tokio_postgres::NoTls;

fn inputs() -> (PathBuf, String) {
    (
        std::env::var_os("BABEL_DRIVER_SOCKET")
            .expect("Owned socket required")
            .into(),
        std::env::var("BABEL_DRIVER_PASSWORD").expect("Synthetic password required"),
    )
}
async fn session(name: &str) -> Session {
    let (socket, password) = inputs();
    Session::connect(&socket, &password, name)
        .await
        .expect("Synthetic connection rejected")
}
async fn count(session: &mut Session, id: i64) -> i64 {
    session
        .query(
            "SELECT count(*) FROM driver_lab.records WHERE id=$1",
            &[&id],
        )
        .await
        .expect("Count rejected")[0]
        .get(0)
}

#[tokio::test]
async fn invalid_configuration_and_unavailable_socket_are_redacted() {
    let (socket, password) = inputs();
    for (path, secret, app) in [
        (
            PathBuf::from("relative"),
            password.clone(),
            "valid".to_string(),
        ),
        (socket.clone(), String::new(), "valid".to_string()),
        (socket.clone(), "x".repeat(129), "valid".to_string()),
        (socket.clone(), password.clone(), String::new()),
        (socket.clone(), password.clone(), "x".repeat(49)),
        (
            socket.clone(),
            password.clone(),
            "invalid space".to_string(),
        ),
    ] {
        assert!(matches!(
            Session::connect(&path, &secret, &app).await,
            Err(Failure::Configuration)
        ));
    }
    let missing = tempfile::tempdir().expect("Private fixture directory");
    assert!(matches!(
        Session::connect(missing.path(), &password, "absent").await,
        Err(Failure::Unavailable)
    ));
    assert_eq!(
        Failure::Constraint.to_string(),
        "Driver lab rejected: Constraint"
    );
}

#[tokio::test]
async fn scram_authentication_and_least_privilege_are_real() {
    let (socket, _) = inputs();
    assert!(matches!(
        Session::connect(&socket, "synthetic-wrong-password", "wrong-password").await,
        Err(Failure::Authentication)
    ));
    let mut db = session("privileges").await;
    assert_eq!(
        db.query("SELECT * FROM babel_lab.objects", &[]).await.err(),
        Some(Failure::Denied)
    );
    assert_eq!(
        db.query("ALTER SYSTEM SET fsync=off", &[]).await.err(),
        Some(Failure::Denied)
    );
    let rows = db.query("SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication FROM pg_roles WHERE rolname=current_user", &[]).await.expect("Role inspection");
    for i in 0..4 {
        assert!(!rows[0].get::<_, bool>(i));
    }
}

#[tokio::test]
async fn parameter_binding_handles_literals_null_and_binary_without_sql_execution() {
    let mut db = session("parameters").await;
    let literal = "x'); DROP SCHEMA driver_lab CASCADE; -- 🐧";
    let bytes = vec![0u8, 1, 255];
    let absent: Option<&str> = None;
    let rows = db
        .query(
            "SELECT $1::text, $2::bytea, $3::text",
            &[&literal, &bytes, &absent],
        )
        .await
        .expect("Bound parameters");
    assert_eq!(rows[0].get::<_, &str>(0), literal);
    assert_eq!(rows[0].get::<_, &[u8]>(1), bytes);
    assert_eq!(rows[0].get::<_, Option<&str>>(2), None);
    assert!(
        db.query("SELECT 1 FROM driver_lab.records LIMIT 1", &[])
            .await
            .is_ok()
    );
    assert_eq!(
        db.query("SELECT $1::bigint", &[&literal]).await.err(),
        Some(Failure::Rejected)
    );
    assert_eq!(
        db.query("SELECT 1/0", &[]).await.err(),
        Some(Failure::Rejected)
    );
}

#[tokio::test]
async fn commit_and_explicit_or_drop_rollback_preserve_coupled_state() {
    let mut db = session("transactions").await;
    let mut tx = db.begin().await.expect("Begin");
    tx.execute(
        "INSERT INTO driver_lab.records VALUES ($1,$2)",
        &[&1i64, &"committed"],
    )
    .await
    .expect("Record");
    tx.execute("INSERT INTO driver_lab.journal VALUES ($1)", &[&1i64])
        .await
        .expect("Journal");
    tx.commit().await.expect("Commit");
    assert_eq!(count(&mut db, 1).await, 1);
    let journal: i64 = db
        .query("SELECT count(*) FROM driver_lab.journal WHERE id=1", &[])
        .await
        .expect("Journal read")[0]
        .get(0);
    assert_eq!(journal, 1);
    let mut tx = db.begin().await.expect("Begin");
    tx.execute(
        "INSERT INTO driver_lab.records VALUES ($1,$2)",
        &[&2i64, &"rolled-back"],
    )
    .await
    .expect("Record");
    tx.rollback().await.expect("Rollback");
    assert_eq!(count(&mut db, 2).await, 0);
    let mut tx = db.begin().await.expect("Begin");
    tx.execute(
        "INSERT INTO driver_lab.records VALUES ($1,$2)",
        &[&3i64, &"drop-rollback"],
    )
    .await
    .expect("Record");
    drop(tx);
    assert_eq!(count(&mut db, 3).await, 0);
}

#[tokio::test]
async fn caught_statement_failure_never_becomes_successful_commit() {
    let mut db = session("failed-transaction").await;
    let mut tx = db.begin().await.expect("Begin");
    tx.execute(
        "INSERT INTO driver_lab.records VALUES ($1,$2)",
        &[&10i64, &"first-unique"],
    )
    .await
    .expect("Record");
    assert_eq!(
        tx.execute(
            "INSERT INTO driver_lab.records VALUES ($1,$2)",
            &[&10i64, &"duplicate"]
        )
        .await
        .err(),
        Some(Failure::Constraint)
    );
    assert_eq!(tx.commit().await, Err(Failure::Aborted));
    assert_eq!(count(&mut db, 10).await, 0);
}

#[tokio::test]
async fn deferred_commit_failure_never_acknowledges_success() {
    let mut db = session("deferred-failure").await;
    let mut tx = db.begin().await.expect("Begin");
    tx.execute("INSERT INTO driver_lab.journal VALUES ($1)", &[&99999i64])
        .await
        .expect("Deferred insert");
    assert_eq!(tx.commit().await, Err(Failure::UnknownCommit));
}

#[tokio::test]
async fn lock_timeout_is_bounded_and_session_can_be_reused() {
    let mut a = session("lock-holder").await;
    let mut b = session("lock-waiter").await;
    a.query("INSERT INTO driver_lab.records VALUES (20,'lock')", &[])
        .await
        .expect("Seed");
    let mut tx = a.begin().await.expect("Begin");
    tx.execute(
        "UPDATE driver_lab.records SET label='locked' WHERE id=20",
        &[],
    )
    .await
    .expect("Lock");
    assert_eq!(
        b.query(
            "UPDATE driver_lab.records SET label='waiting' WHERE id=20",
            &[]
        )
        .await
        .err(),
        Some(Failure::Busy)
    );
    tx.rollback().await.expect("Release");
    assert!(
        b.query(
            "UPDATE driver_lab.records SET label='released' WHERE id=20",
            &[]
        )
        .await
        .is_ok()
    );
}

#[tokio::test]
async fn serialization_failure_is_retryable_without_partial_commit() {
    let mut a = session("serial-a").await;
    let mut b = session("serial-b").await;
    a.query("INSERT INTO driver_lab.records VALUES (30,'serial')", &[])
        .await
        .expect("Seed");
    a.query("BEGIN ISOLATION LEVEL SERIALIZABLE", &[])
        .await
        .expect("Begin");
    b.query("BEGIN ISOLATION LEVEL SERIALIZABLE", &[])
        .await
        .expect("Begin");
    for db in [&mut a, &mut b] {
        assert_eq!(count(db, 30).await, 1);
    }
    a.query(
        "UPDATE driver_lab.records SET label='serial-committed' WHERE id=30",
        &[],
    )
    .await
    .expect("Update");
    a.query("COMMIT", &[]).await.expect("Commit");
    assert_eq!(
        b.query(
            "UPDATE driver_lab.records SET label='serial-stale' WHERE id=30",
            &[]
        )
        .await
        .err(),
        Some(Failure::Retryable)
    );
    b.query("ROLLBACK", &[]).await.expect("Rollback");
    assert_eq!(
        b.query("SELECT label FROM driver_lab.records WHERE id=30", &[])
            .await
            .expect("Read")[0]
            .get::<_, &str>(0),
        "serial-committed"
    );
}

#[tokio::test]
async fn server_statement_timeout_cancels_and_preserves_connection() {
    let mut db = session("statement-timeout").await;
    assert_eq!(
        db.query("SELECT pg_sleep(3)", &[]).await.err(),
        Some(Failure::Cancelled)
    );
    assert!(db.query("SELECT 1", &[]).await.is_ok());
}

#[tokio::test]
async fn explicit_cancel_reaches_the_active_query() {
    let mut db = session("cancel-target").await;
    let mut observer = session("cancel-observer").await;
    db.query("SET statement_timeout='5s'", &[])
        .await
        .expect("Cancellation fixture");
    let token = db.cancel_token();
    let cancellation = async {
        tokio::time::timeout(Duration::from_millis(500),async {
            loop {
                let rows=observer.query("SELECT count(*) FROM pg_stat_activity WHERE application_name='cancel-target' AND wait_event='PgSleep'", &[]).await.expect("Observe active query");
                if rows[0].get::<_,i64>(0)==1 { break; }
                tokio::time::sleep(Duration::from_millis(2)).await;
            }
            token.cancel_query(NoTls).await.expect("Cancel active query");
        }).await.expect("Cancellation deadline");
    };
    let (result, ()) = tokio::join!(db.query("SELECT pg_sleep(3)", &[]), cancellation);
    assert_eq!(result.err(), Some(Failure::Cancelled));
    assert!(db.query("SELECT 1", &[]).await.is_ok());
}

#[tokio::test]
async fn client_deadline_discards_session_when_server_timeout_is_absent() {
    let mut db = session("client-deadline").await;
    db.query("SET statement_timeout=0", &[])
        .await
        .expect("Synthetic fault");
    assert_eq!(
        db.query("SELECT pg_sleep(3)", &[]).await.err(),
        Some(Failure::Deadline)
    );
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
    assert!(matches!(db.begin().await, Err(Failure::Unavailable)));
}

#[tokio::test]
async fn unresponsive_unix_peer_has_a_connection_deadline() {
    let directory = tempfile::tempdir().expect("Private socket directory");
    let listener = tokio::net::UnixListener::bind(directory.path().join(".s.PGSQL.5432"))
        .expect("Synthetic peer");
    let stalled = tokio::spawn(async move {
        let (_peer, _) = listener.accept().await.expect("Accept local fixture");
        tokio::time::sleep(Duration::from_secs(4)).await;
    });
    assert!(matches!(
        Session::connect(directory.path(), "synthetic", "stalled").await,
        Err(Failure::Deadline)
    ));
    stalled.abort();
}

#[tokio::test]
async fn unsafe_session_durability_is_rejected() {
    let mut db = session("durability").await;
    db.query("SET synchronous_commit=off", &[])
        .await
        .expect("Synthetic fault");
    assert_eq!(db.verify_durability().await, Err(Failure::UnsafeDurability));
    assert!(matches!(db.begin().await, Err(Failure::UnsafeDurability)));
}

#[tokio::test]
async fn transaction_deadline_prevents_commit_and_session_reuse() {
    let mut db = session("transaction-deadline").await;
    db.query("SET statement_timeout=0", &[])
        .await
        .expect("Synthetic fault");
    let mut tx = db.begin().await.expect("Begin");
    assert_eq!(
        tx.execute("SELECT pg_sleep(3)", &[]).await,
        Err(Failure::Deadline)
    );
    assert_eq!(tx.execute("SELECT 1", &[]).await, Err(Failure::Unavailable));
    assert_eq!(tx.commit().await, Err(Failure::Aborted));
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
}

#[tokio::test]
async fn lost_connection_during_transaction_has_unknown_commit_outcome() {
    let mut db = session("lost-connection").await;
    let mut killer = session("owned-peer-termination").await;
    let pid: i32 = db
        .query("SELECT pg_backend_pid()", &[])
        .await
        .expect("Own PID")[0]
        .get(0);
    let mut tx = db.begin().await.expect("Begin");
    tx.execute(
        "INSERT INTO driver_lab.records VALUES ($1,$2)",
        &[&40i64, &"lost-transaction"],
    )
    .await
    .expect("Insert");
    killer
        .query("SELECT pg_terminate_backend($1)", &[&pid])
        .await
        .expect("Terminate owned lab session");
    assert_eq!(tx.commit().await, Err(Failure::UnknownCommit));
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
    assert_eq!(count(&mut killer, 40).await, 0);
}

#[tokio::test]
async fn raw_driver_aborted_commit_requires_application_failure_tracking() {
    tokio::time::timeout(Duration::from_secs(3), async {
        let (socket, password) = inputs();
        let mut config = tokio_postgres::Config::new();
        config
            .host_path(socket)
            .user("babel_driver_lab")
            .password(password)
            .dbname("babel_store_lab");
        let (mut client, connection) = config.connect(NoTls).await.expect("Owned raw comparison");
        let task = tokio::spawn(async move {
            let _ = connection.await;
        });
        let tx = client.transaction().await.expect("Raw begin");
        tx.execute(
            "INSERT INTO driver_lab.records VALUES ($1,$2)",
            &[&50i64, &"raw-comparison"],
        )
        .await
        .expect("Insert");
        assert!(
            tx.execute(
                "INSERT INTO driver_lab.records VALUES ($1,$2)",
                &[&50i64, &"raw-duplicate"]
            )
            .await
            .is_err()
        );
        // Successful SQL command completion does not prove a mutation was committed:
        // PostgreSQL has rolled the failed transaction back.
        assert!(tx.commit().await.is_ok());
        let mut observer = session("raw-rollback-observer").await;
        assert_eq!(count(&mut observer, 50).await, 0);
        task.abort();
    })
    .await
    .expect("Raw comparison deadline");
}

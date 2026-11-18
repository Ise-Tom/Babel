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
        "Driver rejected: Constraint"
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

mod support;
use babel_store_driver_lab::{MAX_RESULT_BYTES, MAX_ROWS, Mutation, ObjectId};
const ACTOR: u128 = 0x00000000000040008000000000000001;
fn typed(request: u128, object: u128, rid: u32, label: &str) -> Mutation {
    Mutation::create(
        ObjectId::new(ACTOR).unwrap(),
        ObjectId::new(request).unwrap(),
        ObjectId::new(object).unwrap(),
        rid,
        label,
    )
    .expect("Bounded fixture mutation")
}
fn object_text(object: u128) -> String {
    let s = format!("{object:032x}");
    format!(
        "{}-{}-{}-{}-{}",
        &s[..8],
        &s[8..12],
        &s[12..16],
        &s[16..20],
        &s[20..]
    )
}
async fn effects(db: &mut Session, object: u128) -> Vec<i64> {
    let rows = db
        .query(
            "SELECT * FROM driver_lab.effects($1::text)",
            &[&object_text(object)],
        )
        .await
        .expect("Observed fixture state");
    (0..4).map(|i| rows[0].get(i)).collect()
}
async fn wait_active(observer: &mut Session, app: &str, wait: &str) {
    tokio::time::timeout(Duration::from_secs(2),async {
        loop {
            let rows=observer.query("SELECT count(*) FROM pg_stat_activity WHERE application_name=$1 AND wait_event_type=$2",&[&app,&wait]).await.expect("Owned session observation");
            if rows[0].get::<_,i64>(0)==1 { break; }
            tokio::time::sleep(Duration::from_millis(2)).await;
        }
    }).await.expect("Activity barrier");
}
async fn wait_gone(observer: &mut Session, app: &str) {
    tokio::time::timeout(Duration::from_secs(3), async {
        loop {
            let rows = observer
                .query(
                    "SELECT count(*) FROM pg_stat_activity WHERE application_name=$1",
                    &[&app],
                )
                .await
                .expect("Owned session observation");
            if rows[0].get::<_, i64>(0) == 0 {
                break;
            }
            tokio::time::sleep(Duration::from_millis(2)).await;
        }
    })
    .await
    .expect("Disconnected session cleanup");
}

#[tokio::test]
async fn typed_mutations_bind_identity_payload_and_reauthorize_receipt_replay() {
    let mut db = session("typed-mutations").await;
    let create = typed(10001, 10001, 10001, "native-create");
    let first = db.mutate(&create).await.expect("Typed durable create");
    assert_eq!(db.mutate(&create).await, Ok(first));
    assert_eq!(effects(&mut db, 10001).await, vec![1, 1, 1, 1]);
    assert_eq!(
        db.mutate(&typed(10001, 10001, 10001, "changed-payload"))
            .await,
        Err(Failure::Rejected)
    );
    let rename = Mutation::rename(
        ObjectId::new(ACTOR).unwrap(),
        ObjectId::new(10002).unwrap(),
        ObjectId::new(10001).unwrap(),
        10001,
        "native-rename",
        1,
    )
    .unwrap();
    assert!(db.mutate(&rename).await.expect("Typed rename") > first);
    assert_eq!(db.mutate(&rename).await.unwrap(), first + 1);
    assert_eq!(effects(&mut db, 10001).await, vec![1, 2, 2, 2]);
    db.query(
        "SELECT driver_lab.set_actor_active($1::text,false)",
        &[&object_text(ACTOR)],
    )
    .await
    .unwrap();
    let revoked = db.mutate(&create).await;
    db.query(
        "SELECT driver_lab.set_actor_active($1::text,true)",
        &[&object_text(ACTOR)],
    )
    .await
    .unwrap();
    assert_eq!(revoked, Err(Failure::Denied));
    let inactive = Mutation::create(
        ObjectId::new(999).unwrap(),
        ObjectId::new(10003).unwrap(),
        ObjectId::new(10003).unwrap(),
        10003,
        "inactive",
    )
    .unwrap();
    assert_eq!(db.mutate(&inactive).await, Err(Failure::Denied));
    let stale = Mutation::rename(
        ObjectId::new(ACTOR).unwrap(),
        ObjectId::new(10004).unwrap(),
        ObjectId::new(10001).unwrap(),
        10001,
        "stale",
        1,
    )
    .unwrap();
    assert_eq!(db.mutate(&stale).await, Err(Failure::Retryable));
}

#[tokio::test]
async fn typed_input_limits_reject_before_any_database_request() {
    let id = ObjectId::new(1).unwrap();
    assert!(ObjectId::new(0).is_err());
    for label in [
        "",
        "x'",
        "Uppercase",
        "x\0",
        "invalid space",
        &"a".repeat(33),
    ] {
        assert!(Mutation::create(id, id, id, 1000, label).is_err());
    }
    for rid in [0, 999, 1_000_000_000] {
        assert!(Mutation::create(id, id, id, rid, "valid").is_err());
    }
    assert!(Mutation::rename(id, id, id, 1000, "valid", 0).is_err());
    assert!(Mutation::create(id, id, id, 999_999_999, &"a".repeat(32)).is_ok());
}

#[tokio::test]
async fn bounded_results_discard_over_budget_sessions() {
    let mut rows = session("rows-budget").await;
    let max = MAX_ROWS as i32;
    assert_eq!(
        rows.query("SELECT generate_series(1,$1::int)", &[&max])
            .await
            .unwrap()
            .len(),
        MAX_ROWS
    );
    assert_eq!(
        rows.query("SELECT generate_series(1,$1::int)", &[&(max + 1)])
            .await
            .err(),
        Some(Failure::Budget)
    );
    assert_eq!(
        rows.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
    let mut bytes = session("bytes-budget").await;
    let max = MAX_RESULT_BYTES as i32;
    assert_eq!(
        bytes
            .query("SELECT repeat('x',$1::int)", &[&max])
            .await
            .unwrap()[0]
            .get::<_, &str>(0)
            .len(),
        MAX_RESULT_BYTES
    );
    assert_eq!(
        bytes
            .query("SELECT repeat('x',$1::int)", &[&(max + 1)])
            .await
            .err(),
        Some(Failure::Budget)
    );
    let mut columns = session("column-budget").await;
    assert_eq!(
        columns
            .query(
                "SELECT 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1",
                &[]
            )
            .await
            .err(),
        Some(Failure::Budget)
    );
}

#[tokio::test]
async fn caller_dropped_query_discards_its_session() {
    let mut db = session("dropped-query").await;
    db.query("SET statement_timeout=0", &[]).await.unwrap();
    let mut observer = session("drop-query-observer").await;
    let mut pending = Box::pin(db.query("SELECT pg_sleep(3)", &[]));
    tokio::select! { _=wait_active(&mut observer,"dropped-query","Timeout")=>{}, _=&mut pending=>panic!("Query completed before cancellation barrier") }
    drop(pending);
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
}

#[tokio::test]
async fn caller_dropped_begin_and_rollback_discard_their_sessions() {
    let (socket, password) = inputs();
    for command in [b"START TRANSACTION\0".as_slice(), b"ROLLBACK\0".as_slice()] {
        let proxy = support::ReplyHold::new(&socket, command);
        let mut db = Session::connect(&proxy.path, &password, "dropped-control")
            .await
            .unwrap();
        if command == b"START TRANSACTION\0" {
            let mut pending = Box::pin(db.begin());
            tokio::select! { _=proxy.held.notified()=>{}, result=&mut pending=>panic!("Begin reply unexpectedly delivered: {:?}", result.map(|_| ())) }
            drop(pending);
        } else {
            let tx = db.begin().await.unwrap();
            let mut pending = Box::pin(tx.rollback());
            tokio::select! { _=proxy.held.notified()=>{}, _=&mut pending=>panic!("Rollback reply unexpectedly delivered") }
            drop(pending);
        }
        assert_eq!(
            db.query("SELECT 1", &[]).await.err(),
            Some(Failure::Unavailable)
        );
    }
}

#[tokio::test]
async fn caller_dropped_mutation_rolls_back_and_prevents_connection_reuse() {
    let mut db = session("dropped-mutation").await;
    db.query("SET statement_timeout=0", &[]).await.unwrap();
    let mut observer = session("mutation-observer").await;
    observer
        .query("SELECT pg_advisory_lock(882204)", &[])
        .await
        .unwrap();
    let value = typed(11001, 11001, 11001, "wait-mutation");
    let mut pending = Box::pin(db.mutate(&value));
    tokio::select! { _=wait_active(&mut observer,"dropped-mutation","Lock")=>{}, _=&mut pending=>panic!("Mutation completed before its controlled lock barrier") }
    drop(pending);
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
    observer
        .query("SELECT pg_advisory_unlock(882204)", &[])
        .await
        .unwrap();
    wait_gone(&mut observer, "dropped-mutation").await;
    assert_eq!(effects(&mut observer, 11001).await, vec![0, 0, 0, 0]);
}

#[tokio::test]
async fn durable_commit_with_lost_reply_is_recovered_without_repeating_mutation() {
    let (socket, password) = inputs();
    let proxy = support::ReplyHold::new(&socket, b"COMMIT\0");
    let mut db = Session::connect(&proxy.path, &password, "lost-commit-reply")
        .await
        .unwrap();
    let value = typed(12001, 12001, 12001, "durable-lost-reply");
    let mut pending = Box::pin(db.mutate(&value));
    tokio::select! { _=proxy.held.notified()=>{}, _=&mut pending=>panic!("Commit reply unexpectedly delivered") }
    let mut observer = session("committed-state-observer").await;
    assert_eq!(effects(&mut observer, 12001).await, vec![1, 1, 1, 1]);
    drop(proxy);
    assert_eq!(pending.await, Err(Failure::UnknownCommit));
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
    let result = observer.mutate(&value).await.unwrap();
    assert_eq!(observer.mutate(&value).await, Ok(result));
    assert_eq!(effects(&mut observer, 12001).await, vec![1, 1, 1, 1]);
}

#[tokio::test]
async fn dropped_commit_future_after_durability_requires_receipt_recovery() {
    let (socket, password) = inputs();
    let proxy = support::ReplyHold::new(&socket, b"COMMIT\0");
    let mut db = Session::connect(&proxy.path, &password, "dropped-commit")
        .await
        .unwrap();
    let value = typed(13001, 13001, 13001, "dropped-after-commit");
    let mut pending = Box::pin(db.mutate(&value));
    tokio::select! { _=proxy.held.notified()=>{}, _=&mut pending=>panic!("Commit reply unexpectedly delivered") }
    let mut observer = session("drop-commit-observer").await;
    assert_eq!(effects(&mut observer, 13001).await, vec![1, 1, 1, 1]);
    drop(pending);
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
    drop(proxy);
    assert!(observer.mutate(&value).await.is_ok());
    assert_eq!(effects(&mut observer, 13001).await, vec![1, 1, 1, 1]);
}

#[tokio::test]
async fn concurrent_identical_requests_commit_once_and_conflicting_reuse_is_denied() {
    let mut a = session("duplicate-a").await;
    let mut b = session("duplicate-b").await;
    let value = typed(14001, 14001, 14001, "concurrent-retry");
    let (first, second) = tokio::join!(a.mutate(&value), b.mutate(&value));
    assert!(first.is_ok());
    assert_eq!(first, second);
    assert_eq!(effects(&mut a, 14001).await, vec![1, 1, 1, 1]);
    assert_eq!(
        a.mutate(&typed(14001, 14001, 14001, "conflicting-reuse"))
            .await,
        Err(Failure::Rejected)
    );
    assert_eq!(effects(&mut a, 14001).await, vec![1, 1, 1, 1]);
}

async fn restart_checkpoint(name: &str) {
    let control: PathBuf = std::env::var_os("BABEL_DRIVER_CONTROL")
        .expect("Owned crash coordinator required")
        .into();
    std::fs::write(control.join(format!("{name}.ready")), b"ready").expect("Crash checkpoint");
    tokio::time::timeout(Duration::from_secs(30), async {
        loop {
            if std::fs::read(control.join(format!("{name}.done")))
                .ok()
                .as_deref()
                == Some(b"restarted")
            {
                break;
            }
            tokio::time::sleep(Duration::from_millis(20)).await;
        }
    })
    .await
    .expect("Owned crash/restart deadline");
}

#[tokio::test]
async fn driver_recovery_after_confirmed_commit() {
    let mut db = session("recovery-committed").await;
    let value = typed(15001, 15001, 15001, "survives-real-restart");
    let original = db.mutate(&value).await.unwrap();
    restart_checkpoint("after_commit").await;
    assert!(db.query("SELECT 1", &[]).await.is_err());
    let mut recovered = session("recovered-confirmed").await;
    assert_eq!(effects(&mut recovered, 15001).await, vec![1, 1, 1, 1]);
    assert_eq!(recovered.mutate(&value).await, Ok(original));
    assert_eq!(effects(&mut recovered, 15001).await, vec![1, 1, 1, 1]);
    let rename = Mutation::rename(
        ObjectId::new(ACTOR).unwrap(),
        ObjectId::new(15002).unwrap(),
        ObjectId::new(15001).unwrap(),
        15001,
        "after-recovery",
        1,
    )
    .unwrap();
    assert!(recovered.mutate(&rename).await.unwrap() > original);
}

#[tokio::test]
async fn driver_recovery_before_commit() {
    let mut db = session("recovery-uncommitted").await;
    let mut tx = db.begin().await.unwrap();
    let actor = object_text(ACTOR);
    let request = object_text(15101);
    let object = object_text(15101);
    tx.execute("SELECT driver_lab.apply($1::text,$2::text,'create',$3::text,'S-1-5-21-100-200-300-15101','uncommitted-restart',0)",&[&actor,&request,&object]).await.unwrap();
    let staged = tx
        .query("SELECT * FROM driver_lab.effects($1::text)", &[&object])
        .await
        .unwrap();
    assert_eq!(
        (0..4)
            .map(|i| staged[0].get::<_, i64>(i))
            .collect::<Vec<_>>(),
        vec![1, 1, 1, 1]
    );
    restart_checkpoint("before_commit").await;
    assert_eq!(tx.commit().await, Err(Failure::UnknownCommit));
    let mut recovered = session("recovered-uncommitted").await;
    assert_eq!(effects(&mut recovered, 15101).await, vec![0, 0, 0, 0]);
    let value = typed(15101, 15101, 15101, "uncommitted-restart");
    let result = recovered.mutate(&value).await.unwrap();
    assert_eq!(recovered.mutate(&value).await, Ok(result));
    assert_eq!(effects(&mut recovered, 15101).await, vec![1, 1, 1, 1]);
}

#[tokio::test]
async fn statement_and_parameter_budgets_are_enforced_before_execution() {
    let mut sql = session("sql-budget").await;
    let oversized: &'static str = Box::leak(" ".repeat(4097).into_boxed_str());
    assert_eq!(sql.query(oversized, &[]).await.err(), Some(Failure::Budget));
    let mut db = session("parameter-budget").await;
    let value = 1i32;
    let params = vec![&value as &(dyn tokio_postgres::types::ToSql + Sync); 33];
    assert_eq!(
        db.query("SELECT $1::int", &params).await.err(),
        Some(Failure::Budget)
    );
    assert_eq!(
        db.query("SELECT 1", &[]).await.err(),
        Some(Failure::Unavailable)
    );
}

#[tokio::test]
async fn transaction_result_limits_prevent_false_commit_and_partial_state() {
    let mut db = session("tx-read-budget").await;
    let mut tx = db.begin().await.unwrap();
    tx.execute(
        "INSERT INTO driver_lab.records VALUES (70,'budget-rollback')",
        &[],
    )
    .await
    .unwrap();
    assert_eq!(
        tx.query("SELECT generate_series(1,129)", &[]).await.err(),
        Some(Failure::Budget)
    );
    assert_eq!(tx.commit().await, Err(Failure::Aborted));
    let mut observer = session("tx-budget-observer").await;
    wait_gone(&mut observer, "tx-read-budget").await;
    assert_eq!(count(&mut observer, 70).await, 0);
}

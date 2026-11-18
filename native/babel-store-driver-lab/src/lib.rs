//! Qualified local PostgreSQL transaction profile; no AD storage/schema or credentials.
#![forbid(unsafe_code)]

use futures_util::TryStreamExt;
use std::path::Path;
use std::time::Duration;
use tokio::task::{AbortHandle, JoinHandle};
use tokio::time::timeout;
use tokio_postgres::{
    Client, NoTls, Row,
    types::{FromSql, ToSql, Type},
};

mod mutation;
pub use mutation::{Mutation, ObjectId};
const DEADLINE: Duration = Duration::from_millis(600);
pub const MAX_ROWS: usize = 128;
pub const MAX_RESULT_BYTES: usize = 65_536;
const MAX_COLUMNS: usize = 32;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Failure {
    Configuration,
    Authentication,
    Unavailable,
    Deadline,
    Constraint,
    Denied,
    Busy,
    Retryable,
    Cancelled,
    Rejected,
    UnsafeDurability,
    Aborted,
    UnknownCommit,
    Budget,
}
impl std::fmt::Display for Failure {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Driver rejected: {self:?}")
    }
}
impl std::error::Error for Failure {}
pub fn classify(error: &tokio_postgres::Error) -> Failure {
    match error.code().map(|code| code.code()) {
        Some("28P01" | "28000") => Failure::Authentication,
        Some("23505" | "23503" | "23514" | "23502") => Failure::Constraint,
        Some("42501") => Failure::Denied,
        Some("55P03") => Failure::Busy,
        Some("40001" | "40P01") => Failure::Retryable,
        Some("57014") => Failure::Cancelled,
        Some(_) => Failure::Rejected,
        None if error.is_closed() => Failure::Unavailable,
        None => Failure::Rejected,
    }
}

/// Armed before polling an operation. Dropping its future closes the connection,
/// including when a COMMIT may already have executed and its reply is unobserved.
struct InFlight<'a> {
    poisoned: &'a mut bool,
    abort: AbortHandle,
    armed: bool,
}
impl<'a> InFlight<'a> {
    fn new(poisoned: &'a mut bool, abort: AbortHandle) -> Result<Self, Failure> {
        if *poisoned {
            return Err(Failure::Unavailable);
        }
        Ok(Self {
            poisoned,
            abort,
            armed: true,
        })
    }
    fn complete(mut self) {
        self.armed = false;
    }
}
impl Drop for InFlight<'_> {
    fn drop(&mut self) {
        if self.armed {
            *self.poisoned = true;
            self.abort.abort();
        }
    }
}

// Count actual binary field bytes without decoding/reformatting application values.
#[derive(Debug)]
struct FieldBytes<'a>(&'a [u8]);
impl<'a> FromSql<'a> for FieldBytes<'a> {
    fn from_sql(_: &Type, raw: &'a [u8]) -> Result<Self, Box<dyn std::error::Error + Sync + Send>> {
        Ok(Self(raw))
    }
    fn accepts(_: &Type) -> bool {
        true
    }
}
async fn read_rows(
    client: &impl tokio_postgres::GenericClient,
    sql: &'static str,
    params: &[&(dyn ToSql + Sync)],
) -> Result<Vec<Row>, Failure> {
    if sql.len() > 4096 || params.len() > 32 {
        return Err(Failure::Budget);
    }
    let stream = client
        .query_raw(sql, params.iter().copied())
        .await
        .map_err(|e| classify(&e))?;
    let mut stream = std::pin::pin!(stream);
    let mut rows = Vec::new();
    let mut bytes = 0usize;
    while let Some(row) = stream.try_next().await.map_err(|e| classify(&e))? {
        if rows.len() == MAX_ROWS || row.len() > MAX_COLUMNS {
            return Err(Failure::Budget);
        }
        for index in 0..row.len() {
            let value = row
                .try_get::<_, Option<FieldBytes<'_>>>(index)
                .map_err(|_| Failure::Rejected)?;
            bytes = bytes.saturating_add(value.map_or(0, |v| v.0.len()));
        }
        if bytes > MAX_RESULT_BYTES {
            return Err(Failure::Budget);
        }
        rows.push(row);
    }
    Ok(rows)
}

pub struct Session {
    client: Client,
    task: JoinHandle<()>,
    poisoned: bool,
}
impl Drop for Session {
    fn drop(&mut self) {
        self.task.abort();
    }
}
impl Session {
    pub async fn connect(
        socket: &Path,
        password: &str,
        application: &str,
    ) -> Result<Self, Failure> {
        if !socket.is_absolute()
            || !socket.is_dir()
            || password.is_empty()
            || password.len() > 128
            || application.is_empty()
            || application.len() > 48
            || !application
                .bytes()
                .all(|c| c.is_ascii_alphanumeric() || c == b'-')
        {
            return Err(Failure::Configuration);
        }
        let mut config = tokio_postgres::Config::new();
        config.host_path(socket).user("babel_driver_lab").password(password).dbname("babel_store_lab")
            .application_name(application).options("-c statement_timeout=300ms -c lock_timeout=100ms -c idle_in_transaction_session_timeout=3s");
        let (client, connection) = timeout(Duration::from_secs(2), config.connect(NoTls))
            .await
            .map_err(|_| Failure::Deadline)?
            .map_err(|error| {
                if classify(&error) == Failure::Authentication {
                    Failure::Authentication
                } else {
                    Failure::Unavailable
                }
            })?;
        let task = tokio::spawn(async move {
            let _ = connection.await;
        });
        let mut session = Self {
            client,
            task,
            poisoned: false,
        };
        session.verify_durability().await?;
        Ok(session)
    }
    async fn query_internal(
        &mut self,
        sql: &'static str,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>, Failure> {
        let guard = InFlight::new(&mut self.poisoned, self.task.abort_handle())?;
        match timeout(DEADLINE, read_rows(&self.client, sql, params)).await {
            Ok(result) if !matches!(result, Err(Failure::Budget)) => {
                guard.complete();
                result
            }
            Ok(_) => Err(Failure::Budget),
            Err(_) => Err(Failure::Deadline),
        }
    }
    /// Raw SQL is available only to the explicitly enabled qualification tests.
    #[cfg(feature = "qualification")]
    pub async fn query(
        &mut self,
        sql: &'static str,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>, Failure> {
        self.query_internal(sql, params).await
    }
    pub async fn verify_durability(&mut self) -> Result<(), Failure> {
        let rows = self.query_internal("SELECT current_setting('server_version_num')::int, current_setting('fsync'), current_setting('full_page_writes'), current_setting('synchronous_commit')", &[]).await?;
        let row = &rows[0];
        let version: i32 = row.get(0);
        if !(180_000..190_000).contains(&version) || (1..=3).any(|i| row.get::<_, &str>(i) != "on")
        {
            return Err(Failure::UnsafeDurability);
        }
        Ok(())
    }
    pub fn cancel_token(&self) -> tokio_postgres::CancelToken {
        self.client.cancel_token()
    }
    async fn begin_internal(&mut self) -> Result<LabTransaction<'_>, Failure> {
        self.verify_durability().await?;
        let abort = self.task.abort_handle();
        let guard = InFlight::new(&mut self.poisoned, abort.clone())?;
        let transaction = timeout(DEADLINE, self.client.transaction())
            .await
            .map_err(|_| Failure::Deadline)?
            .map_err(|error| classify(&error))?;
        guard.complete();
        Ok(LabTransaction {
            transaction,
            abort,
            poisoned: &mut self.poisoned,
            failed: false,
        })
    }
    #[cfg(feature = "qualification")]
    pub async fn begin(&mut self) -> Result<LabTransaction<'_>, Failure> {
        self.begin_internal().await
    }
    /// Typed non-credential fixture operation. A confirmed durable commit is the only
    /// success; a fresh session can retry the same actor/request/payload after UnknownCommit.
    pub async fn mutate(&mut self, mutation: &Mutation) -> Result<i64, Failure> {
        let mut tx = self.begin_internal().await?;
        let actor = mutation.actor.text();
        let request = mutation.request.text();
        let object = mutation.object.text();
        let sid = format!("S-1-5-21-100-200-300-{}", mutation.rid);
        let result = tx.query_internal("SELECT driver_lab.apply($1::text,$2::text,$3::text,$4::text,$5::text,$6::text,$7::bigint)", &[&actor,&request,&mutation.operation,&object,&sid,&mutation.label,&mutation.expected]).await?;
        let usn = result[0].get(0);
        tx.commit().await?;
        Ok(usn)
    }
}

pub struct LabTransaction<'a> {
    transaction: tokio_postgres::Transaction<'a>,
    abort: AbortHandle,
    poisoned: &'a mut bool,
    failed: bool,
}
impl LabTransaction<'_> {
    #[cfg(feature = "qualification")]
    pub async fn query(
        &mut self,
        sql: &'static str,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>, Failure> {
        self.query_internal(sql, params).await
    }
    async fn query_internal(
        &mut self,
        sql: &'static str,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>, Failure> {
        let previous_failed = self.failed;
        self.failed = true;
        let guard = InFlight::new(self.poisoned, self.abort.clone())?;
        let result = timeout(DEADLINE, read_rows(&self.transaction, sql, params))
            .await
            .map_err(|_| Failure::Deadline)?;
        if !matches!(result, Err(Failure::Budget)) {
            guard.complete();
        }
        if result.is_ok() {
            self.failed = previous_failed;
        }
        result
    }
    #[cfg(feature = "qualification")]
    pub async fn execute(
        &mut self,
        sql: &'static str,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<u64, Failure> {
        let previous_failed = self.failed;
        self.failed = true;
        let guard = InFlight::new(self.poisoned, self.abort.clone())?;
        let result = timeout(DEADLINE, self.transaction.execute(sql, params))
            .await
            .map_err(|_| Failure::Deadline)?;
        guard.complete();
        if result.is_ok() {
            self.failed = previous_failed;
        }
        result.map_err(|error| classify(&error))
    }
    pub async fn commit(self) -> Result<(), Failure> {
        // Failed transactions are rolled back, never acknowledged as committed.
        if self.failed {
            if let Ok(guard) = InFlight::new(self.poisoned, self.abort.clone())
                && matches!(
                    timeout(DEADLINE, self.transaction.rollback()).await,
                    Ok(Ok(()))
                )
            {
                guard.complete();
            }
            return Err(Failure::Aborted);
        }
        let guard =
            InFlight::new(self.poisoned, self.abort.clone()).map_err(|_| Failure::UnknownCommit)?;
        match timeout(DEADLINE, self.transaction.commit()).await {
            Ok(Ok(())) => {
                guard.complete();
                Ok(())
            }
            _ => Err(Failure::UnknownCommit),
        }
    }
    #[cfg(feature = "qualification")]
    pub async fn rollback(self) -> Result<(), Failure> {
        let guard = InFlight::new(self.poisoned, self.abort.clone())?;
        let result = timeout(DEADLINE, self.transaction.rollback())
            .await
            .map_err(|_| Failure::Deadline)?;
        guard.complete();
        result.map_err(|error| classify(&error))
    }
}

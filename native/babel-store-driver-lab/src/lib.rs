//! Synthetic PostgreSQL driver qualification helpers. No native directory adapter.
#![forbid(unsafe_code)]

use std::path::Path;
use std::time::Duration;
use tokio::task::{AbortHandle, JoinHandle};
use tokio::time::timeout;
use tokio_postgres::{Client, NoTls, Row, types::ToSql};

const DEADLINE: Duration = Duration::from_millis(600);
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
}

impl std::fmt::Display for Failure {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Driver lab rejected: {self:?}")
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
        config
            .host_path(socket)
            .user("babel_driver_lab")
            .password(password)
            .dbname("babel_store_lab")
            .application_name(application)
            .options("-c statement_timeout=300ms -c lock_timeout=100ms -c idle_in_transaction_session_timeout=3s");
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
    pub async fn query(
        &mut self,
        sql: &'static str,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<Vec<Row>, Failure> {
        if self.poisoned {
            return Err(Failure::Unavailable);
        }
        match timeout(DEADLINE, self.client.query(sql, params)).await {
            Ok(result) => result.map_err(|error| classify(&error)),
            Err(_) => {
                self.poisoned = true;
                self.task.abort();
                Err(Failure::Deadline)
            }
        }
    }
    pub async fn verify_durability(&mut self) -> Result<(), Failure> {
        let rows = self.query("SELECT current_setting('server_version_num')::int, current_setting('fsync'), current_setting('full_page_writes'), current_setting('synchronous_commit')", &[]).await?;
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
    pub async fn begin(&mut self) -> Result<LabTransaction<'_>, Failure> {
        if self.poisoned {
            return Err(Failure::Unavailable);
        }
        self.verify_durability().await?;
        let abort = self.task.abort_handle();
        let transaction = timeout(DEADLINE, self.client.transaction())
            .await
            .map_err(|_| {
                self.poisoned = true;
                abort.abort();
                Failure::Deadline
            })?
            .map_err(|error| classify(&error))?;
        Ok(LabTransaction {
            transaction,
            abort,
            poisoned: &mut self.poisoned,
            failed: false,
        })
    }
}

/// Tracks failed statements so a COMMIT returning PostgreSQL's ROLLBACK tag cannot
/// accidentally become a successful synthetic mutation acknowledgment.
pub struct LabTransaction<'a> {
    transaction: tokio_postgres::Transaction<'a>,
    abort: AbortHandle,
    poisoned: &'a mut bool,
    failed: bool,
}
impl LabTransaction<'_> {
    pub async fn execute(
        &mut self,
        sql: &'static str,
        params: &[&(dyn ToSql + Sync)],
    ) -> Result<u64, Failure> {
        if *self.poisoned {
            self.failed = true;
            return Err(Failure::Unavailable);
        }
        let result = match timeout(DEADLINE, self.transaction.execute(sql, params)).await {
            Ok(result) => result.map_err(|error| classify(&error)),
            Err(_) => {
                *self.poisoned = true;
                self.abort.abort();
                Err(Failure::Deadline)
            }
        };
        if result.is_err() {
            self.failed = true;
        }
        result
    }
    pub async fn commit(self) -> Result<(), Failure> {
        if self.failed {
            if !matches!(
                timeout(DEADLINE, self.transaction.rollback()).await,
                Ok(Ok(()))
            ) {
                *self.poisoned = true;
                self.abort.abort();
            }
            return Err(Failure::Aborted);
        }
        match timeout(DEADLINE, self.transaction.commit()).await {
            Ok(Ok(())) => Ok(()),
            // No connection/deadline failure proves rollback. Never automatically retry.
            _ => {
                *self.poisoned = true;
                self.abort.abort();
                Err(Failure::UnknownCommit)
            }
        }
    }
    pub async fn rollback(self) -> Result<(), Failure> {
        match timeout(DEADLINE, self.transaction.rollback()).await {
            Ok(result) => result.map_err(|error| classify(&error)),
            Err(_) => {
                *self.poisoned = true;
                self.abort.abort();
                Err(Failure::Deadline)
            }
        }
    }
}

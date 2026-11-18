//! Owned Unix fault fixture. Holds a real server command reply without changing it.
use std::io;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::{UnixListener, UnixStream};
use tokio::sync::Notify;
use tokio::task::JoinHandle;

pub struct ReplyHold {
    _directory: tempfile::TempDir,
    pub path: PathBuf,
    pub held: Arc<Notify>,
    task: JoinHandle<()>,
}
impl Drop for ReplyHold {
    fn drop(&mut self) {
        self.task.abort();
    }
}
impl ReplyHold {
    pub fn new(database: &Path, command: &'static [u8]) -> Self {
        let directory = tempfile::tempdir().expect("Private fault socket");
        let path = directory.path().to_owned();
        let listener = UnixListener::bind(path.join(".s.PGSQL.5432")).expect("Owned proxy");
        let backend = database.join(".s.PGSQL.5432");
        let held = Arc::new(Notify::new());
        let signal = held.clone();
        let task = tokio::spawn(async move {
            let Ok((client, _)) = listener.accept().await else {
                return;
            };
            let Ok(server) = UnixStream::connect(backend).await else {
                return;
            };
            let (mut input, mut output) = client.into_split();
            let (mut replies, mut requests) = server.into_split();
            let upstream = tokio::io::copy(&mut input, &mut requests);
            let downstream = async {
                loop {
                    let tag = replies.read_u8().await?;
                    let length = replies.read_u32().await?;
                    if !(4..=65_536).contains(&length) {
                        return Err(io::Error::other("Fixture frame budget"));
                    }
                    let mut body = vec![0; (length - 4) as usize];
                    replies.read_exact(&mut body).await?;
                    if tag == b'C' && body == command {
                        signal.notify_one();
                        std::future::pending::<()>().await;
                    }
                    output.write_u8(tag).await?;
                    output.write_u32(length).await?;
                    output.write_all(&body).await?;
                }
                #[allow(unreachable_code)]
                Ok::<(), io::Error>(())
            };
            tokio::select! { _ = upstream => {}, _ = downstream => {} }
        });
        Self {
            _directory: directory,
            path,
            held,
            task,
        }
    }
}

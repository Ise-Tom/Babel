#!/usr/bin/env bash
# Disposable synthetic MIT Kerberos qualification. Run under Linux with gcc,
# make, bison, curl, tar and gpg. No host Kerberos configuration is changed.
set -euo pipefail

repo=$(cd "$(dirname "$0")/../.." && pwd)
lab=$(mktemp -d "${TMPDIR:-/tmp}/babel-krb5.XXXXXX")
cleanup() {
  if [[ -n "${kdc_pid:-}" ]]; then kill "$kdc_pid" 2>/dev/null || true; wait "$kdc_pid" 2>/dev/null || true; fi
  if [[ "${BABEL_KRB5_KEEP:-0}" == 1 ]]; then echo "debug_lab=$lab"; else rm -rf -- "$lab"; fi
}
trap cleanup EXIT
source_url=https://web.mit.edu/kerberos/dist/krb5/1.22/krb5-1.22.3.tar.gz
source_sha=fe90af8441ad9fa9b064b8e53077cefb782a96f8a68276b031dc54af1789ff0b
signer=C4493CB739F4A89F9852CBC20CBA08575F8372DF
mkdir -p "$lab/source" "$lab/gnupg" "$lab/build" "$lab/install" "$lab/state"
chmod 700 "$lab/gnupg" "$lab/state"
curl -fsSL "$source_url" -o "$lab/source/krb5.tar.gz"
curl -fsSL "$source_url.asc" -o "$lab/source/krb5.tar.gz.asc"
echo "$source_sha  $lab/source/krb5.tar.gz" | sha256sum -c -
gpg --homedir "$lab/gnupg" --batch --keyserver hkps://keyserver.ubuntu.com --recv-keys "$signer" >/dev/null
actual_fingerprint=$(gpg --homedir "$lab/gnupg" --batch --with-colons --fingerprint "$signer" | awk -F: '$1=="fpr" {print $10; exit}')
[[ "$actual_fingerprint" == "$signer" ]]
gpg --homedir "$lab/gnupg" --batch --verify "$lab/source/krb5.tar.gz.asc" "$lab/source/krb5.tar.gz" 2>"$lab/signature.log"
grep -q "Good signature" "$lab/signature.log"
tar -xf "$lab/source/krb5.tar.gz" -C "$lab/source"
(
  cd "$lab/build"
  "$lab/source/krb5-1.22.3/src/configure" --prefix="$lab/install" --disable-rpath --without-system-verto --without-libedit >"$lab/configure.log" 2>&1
  make -j2 >"$lab/make.log" 2>&1
  make install >"$lab/install.log" 2>&1
)
export LD_LIBRARY_PATH="$lab/install/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PATH="$lab/install/bin:$lab/install/sbin:$PATH"
export KRB5_CONFIG="$lab/state/krb5.conf"
export KRB5_KDC_PROFILE="$lab/state/kdc.conf"
export KRB5CCNAME="FILE:$lab/state/ccache"
export KRB5RCACHEDIR="$lab/state"
cat >"$KRB5_CONFIG" <<EOF
[libdefaults]
 default_realm = BABEL.TEST
 dns_lookup_kdc = false
 dns_lookup_realm = false
 dns_canonicalize_hostname = false
 rdns = false
 clockskew = 1
 allow_weak_crypto = false
 default_tkt_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96
 default_tgs_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96
 permitted_enctypes = aes256-cts-hmac-sha1-96 aes128-cts-hmac-sha1-96
[realms]
 BABEL.TEST = {
  kdc = 127.0.0.1:17889
 }
EOF
cat >"$KRB5_KDC_PROFILE" <<EOF
[kdcdefaults]
 kdc_listen = 127.0.0.1:17889
 kdc_tcp_listen = 127.0.0.1:17889
[realms]
 BABEL.TEST = {
  database_name = $lab/state/principal
  key_stash_file = $lab/state/stash
  acl_file = $lab/state/kadm5.acl
  max_life = 1d
  supported_enctypes = aes256-cts-hmac-sha1-96:normal aes128-cts-hmac-sha1-96:normal
 }
EOF
kdb5_util create -s -r BABEL.TEST -P synthetic-master-only >"$lab/kdb.log" 2>&1
kadmin.local -q 'addprinc -randkey alice@BABEL.TEST' >"$lab/admin.log" 2>&1
kadmin.local -q 'addprinc -randkey HTTP/service.babel.test@BABEL.TEST' >>"$lab/admin.log" 2>&1
kadmin.local -q 'addprinc -randkey HTTP/other.babel.test@BABEL.TEST' >>"$lab/admin.log" 2>&1
kadmin.local -q 'addprinc -randkey -e aes128-cts-hmac-sha1-96:normal HTTP/aes128.babel.test@BABEL.TEST' >>"$lab/admin.log" 2>&1
kadmin.local -q "ktadd -norandkey -k $lab/state/alice.keytab alice@BABEL.TEST" >>"$lab/admin.log" 2>&1
kadmin.local -q "ktadd -norandkey -k $lab/state/server.keytab HTTP/service.babel.test@BABEL.TEST HTTP/other.babel.test@BABEL.TEST HTTP/aes128.babel.test@BABEL.TEST krbtgt/BABEL.TEST@BABEL.TEST" >>"$lab/admin.log" 2>&1
chmod 600 "$lab/state/"*.keytab
krb5kdc -n >"$lab/kdc.log" 2>&1 &
kdc_pid=$!
sleep 1
kill -0 "$kdc_pid"
gcc -std=c11 -Wall -Wextra -Werror -I"$lab/install/include" "$repo/lab/kerberos/ap_req_probe.c" \
  -L"$lab/install/lib" -Wl,-rpath,"$lab/install/lib" -lkrb5 -lk5crypto -lcom_err -o "$lab/probe"
output=${1:-"$repo/reports/kerberos-qualification.json"}
mkdir -p "$(dirname "$output")"
results="$lab/results.txt"
{
  echo 'case=positive'
  kinit --request-pac -k -t "$lab/state/alice.keytab" alice@BABEL.TEST
  kvno HTTP/service.babel.test@BABEL.TEST
  klist -e
  "$lab/probe" positive HTTP service.babel.test HTTP/service.babel.test@BABEL.TEST HTTP/other.babel.test@BABEL.TEST "FILE:$lab/state/server.keytab"
  echo 'case=aes128'
  "$lab/probe" positive HTTP aes128.babel.test HTTP/aes128.babel.test@BABEL.TEST HTTP/other.babel.test@BABEL.TEST "FILE:$lab/state/server.keytab"
  echo 'case=missing_pac'
  kdestroy
  kinit --no-request-pac -k -t "$lab/state/alice.keytab" alice@BABEL.TEST
  "$lab/probe" missing HTTP service.babel.test HTTP/service.babel.test@BABEL.TEST HTTP/other.babel.test@BABEL.TEST "FILE:$lab/state/server.keytab"
  echo 'case=expired'
  kdestroy
  kinit -l 2s -k -t "$lab/state/alice.keytab" alice@BABEL.TEST
  "$lab/probe" expired HTTP service.babel.test HTTP/service.babel.test@BABEL.TEST HTTP/other.babel.test@BABEL.TEST "FILE:$lab/state/server.keytab"
} >"$results" 2>&1
cat "$results"
python3 - "$results" "$output" "$source_sha" "$signer" "$lab/probe" "$repo" <<'PY'
import hashlib, json, pathlib, platform, subprocess, sys
results, output, source_sha, signer, binary, repo = sys.argv[1:]
lines = pathlib.Path(results).read_text().splitlines()
cases = {}
current = None
for line in lines:
    if line.startswith('case='):
        current = line[5:]
        cases[current] = []
    elif current:
        cases[current].append(line)
expected = {
    'positive': ['accepted_enctype=18', 'wrong_service_rd_req=', 'replay_rd_req=', 'pac_signature_verify=0', 'pac_client_verify=0', 'pac_wrong_client_verify=', 'tampered_pac_verify='],
    'aes128': ['accepted_enctype=17', 'wrong_service_rd_req=', 'replay_rd_req=', 'pac_signature_verify=0', 'pac_client_verify=0', 'pac_wrong_client_verify=', 'tampered_pac_verify='],
    'missing_pac': ['pac_signature_verify=0', 'pac_present=0'],
    'expired': ['expired_rd_req='],
}
assert set(cases) == set(expected), cases.keys()
for case, markers in expected.items():
    assert all(any(line.startswith(marker) for line in cases[case]) for marker in markers), case
def digest(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def version(*command):
    return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT).splitlines()[0]
linkage = subprocess.check_output(('ldd', binary), text=True)
prefix = str(pathlib.Path(binary).parent / 'install' / 'lib')
for library in ('libkrb5.so.3', 'libk5crypto.so.3', 'libcom_err.so.3', 'libkrb5support.so.0'):
    assert any(line.strip().startswith(library + ' => ' + prefix + '/') for line in linkage.splitlines()), library
evidence = {
    'schema': 1,
    'kind': 'generic-mit-kerberos-qualification',
    'source_url': 'https://web.mit.edu/kerberos/dist/krb5/1.22/krb5-1.22.3.tar.gz',
    'source_sha256': source_sha,
    'signature_fingerprint': signer,
    'version': '1.22.3',
    'configure': '--disable-rpath --without-system-verto --without-libedit',
    'host': platform.platform(),
    'tool_versions': {name: version(*command) for name, command in {
        'gcc': ('gcc', '--version'), 'make': ('make', '--version'),
        'bison': ('bison', '--version'), 'gpg': ('gpg', '--version'),
        'curl': ('curl', '--version'), 'krb5': ('krb5-config', '--version'),
    }.items()},
    'probe_source_sha256': digest(pathlib.Path(repo) / 'lab/kerberos/ap_req_probe.c'),
    'runner_source_sha256': digest(pathlib.Path(repo) / 'lab/kerberos/run.sh'),
    'probe_sha256': digest(binary),
    'probe_linkage': linkage.splitlines(),
    'cases': {name: {'status': 'passed', 'output': case_lines} for name, case_lines in cases.items()},
    'unrun': ['Windows AD PAC contents and SID/group interpretation', 'S4U delegation', 'PKINIT', 'cross-realm trusts', 'Windows/Linux/macOS client conformance', 'replay cache across process restart and replicas'],
}
pathlib.Path(output).write_text(json.dumps(evidence, indent=2) + '\n')
PY
echo "report=$output"

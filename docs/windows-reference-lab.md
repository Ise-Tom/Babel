# Isolated Windows reference lab definition

Status is **definition, read-only preflight and synthetic-tested resource runner**. The inventoried Windows
Hyper-V host has insufficient free RAM and disk for this topology. Its VM and
switch inventory is inaccessible in the current session, and no licensed media
was supplied. Both live cycles remain unrun. See the
[redacted inventory, platform pins, terms and preflight commands](validation/p00-05-p00-12.md).

[lab/windows-reference.toml](../lab/windows-reference.toml) is a machine-readable
functional lab definition. The [validator](../scripts/check_lab_definition.py)
checks safety flags, topology, resource bounds and image metadata. CI exercises
those checks, the [preflight](../scripts/preflight_reference_lab.py) and the
[provision/teardown runner](../scripts/run_reference_lab.py) with synthetic inputs.
The [runner packet](validation/p00-05-runner.md) gives the exact plan, local result,
cleanup contract and guest-installation limits. Domain compatibility requires
runs on the real lab.

```sh
python scripts/check_lab_definition.py
python scripts/check_lab_definition.py --require-images
```

The second command intentionally fails for the checked-in placeholders. Use
the private manifest described in the [preflight evidence](validation/p00-05-p00-12.md)
to check host capacity and local image bytes. Select an eligible host before
implementing the provisioning path.

## Topology and resource plan

| Network | Machines | Purpose |
| --- | --- | --- |
| reference, 192.0.2.0/24, reference.example.test | Windows reference DC, Windows client, Linux probe | Record independently observed Windows AD behavior |
| babel, 198.51.100.0/24, babel.example.test | Linux Babel host, Windows client, Linux probe | Run the same declared scenarios against Babel |

These TEST-NET ranges and `.test` domains are isolated lab inputs, never real
production DNS/routing. There is no network forwarding, default route, bridge to
production, external DNS or shared dual-homed probe. Hypervisor management is a
separate plane with access restricted to the operator. Time is supplied from an
isolated lab source; timezone, offsets and deliberate skew are recorded.

The definition requests 16 vCPUs, 30 GiB guest memory and 344 GiB virtual
disks, before host overhead and working storage. The current route proposes
an existing x86-64 Hyper-V host with 64 GiB RAM as a sizing target. The measured
available capacity is checked against the guest budgets. The lab scope is
functional discovery on the two isolated networks.

Windows Server 2022/2025 and Windows 11 editions/builds are candidates, not an
accepted support matrix. Select actual available/licensed reference and client
images, record edition/build/patch level, immutable image identifiers, SHA-256
hashes and acquisition/redistribution terms. Image licensing is independent of
Babel’s Apache license. Do not redistribute Microsoft images or captured licensed
fixtures merely because this repository is public.

## Provisioning and teardown contract to implement after host selection

1. Allocate a unique run ID, scoped VM/disk/network names and a resource manifest;
   check free memory/disk and refuse production bridges or unexpected routing.
2. Verify approved local image bytes against recorded digests and license rights;
   generate fresh per-run synthetic credentials outside version control/logs.
   Expired evaluation media and unapproved updates fail preflight.
3. Build the two isolated networks and guests without internet exposure. Configure
   isolated DNS/time, record effective routes and prove that production/Internet
   destinations are unreachable. Use preapproved media for required packages.
4. Provision the reference forest independently. Run the same versioned scenario
   inputs on each client/probe; a reference server is test infrastructure, never
   a required Babel production runtime.
5. Capture only synthetic, redacted expected/actual evidence. Do not infer a Babel
   pass from a reference pass, simulator or mere network reachability.
6. Destroy exactly the manifest’s scoped VMs, disks, snapshots and networks even
   after failure. Do not delete arbitrary resources by prefix alone. Retain only
   redacted evidence and prove that no test credentials or network access remain.

The privileged provisioning runner must be main-only, independently reviewed and on
isolated trusted infrastructure. Public/fork PRs must never obtain a lab runner,
Windows credentials, signing keys or privileged hypervisor control.

## Qualification scenarios and evidence

Begin with the currently declared anonymous RootDSE subset and negative credential
bind behavior. All unimplemented operations stay explicitly unsupported/unrun.
Then add declared DNS/discovery, membership/secure-channel, user login/password
rotation, GPO application/revert and denied-operation scenarios with implementation.

Each scenario records requirement/operation ID, source/tool/specification revision,
exact guest builds, network/time profile, run ID, expected and actual behavior,
outcome, redacted evidence digests and reviewer. Two clean provision/teardown runs
are required by P00-05 before lab acceptance. A join/login/GPO pass requires the
actual corresponding Windows client behavior; no zero-test result qualifies.

I04 remains open until the host, rights, reproducible provisioning and real-client
execution evidence exist. See [D-02/D-10](decisions.md) and the
[verification contract](validation-plan.md).

## Non-Windows client qualification

The owner-selected initial profile also includes Ubuntu 24.04 LTS and Debian 13
with SSSD/MIT Kerberos, plus macOS on Apple Silicon and Intel. The current six-VM
Windows lab definition is not a complete cross-platform lab. Linux probe images
need exact SSSD/Kerberos/PAM/package versions and real login/password/SSO tests,
not only LDAP queries. Add dedicated disposable client images when provisioning
is implemented; never attach an operator's daily workstation to a synthetic domain.

macOS runs separately from this Windows/Linux topology. Each architecture needs
eligible Apple hardware or virtualization, image-use rights, exact OS/build and
native directory/Kerberos evidence. No Mac host or image is allocated. Keep test
clients on the appropriate isolated `.test` network, with controlled DNS/time and per-run
synthetic credentials. Record cleanup of local enrollment, caches and keychain
state and restore the disposable client. Mobile/appliance integrations use separate
protocol/module gates; Windows GPO cannot be assumed to apply to them.

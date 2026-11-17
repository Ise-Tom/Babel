# Isolated Windows reference lab definition

Status: **definition only; no host or licensed images supplied, no Windows tests
executed**. The project owner requested this preparation on 17 November 2026.
The current cloud worker has no KVM device or libvirt/QEMU tools; it is not a
qualified Windows virtualization host. Nothing here downloads an image, accepts
image terms, creates a VM or purchases capacity.

[lab/windows-reference.toml](../lab/windows-reference.toml) is a machine-readable
functional lab definition. The [validator](../scripts/check_lab_definition.py)
checks safety flags, topology, resource bounds and image metadata. CI exercises
those checks as configuration validation, not domain compatibility evidence.

```sh
python scripts/check_lab_definition.py
python scripts/check_lab_definition.py --require-images
```

The second command intentionally fails for the checked-in placeholders. Supplying
identifiers, digests and explicit rights acknowledgements only validates metadata;
it does not verify an image file, provision a host or qualify Windows behavior.
Host/provider selection requires a separate reviewed provisioning change.

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

The example requests 16 vCPUs, 30 GiB guest memory and 344 GiB virtual disks.
A 64-GiB Linux virtualization host with sufficient SSD capacity is a proposed
comfortable functional-lab budget, not a measured requirement or an authorized
purchase. Sequential scenarios can reduce concurrent resources after profiling.
This is not the six-DC/three-site capacity lab and proves no production SLO.

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

The future provisioning runner must be main-only, independently reviewed and on
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

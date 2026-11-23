# P00-05 isolated lab runner review

Status: **runner tested with synthetic inputs; both live cycles unrun**.
Based on [main `9164dd7`](https://github.com/Ise-Tom/Babel/commit/9164dd744e9b09eb52ff099162ce190a906e8cfa) and the existing-host/licensed-media owner decision in [PR #46](https://github.com/Ise-Tom/Babel/pull/46).

## Inspectable run plan

The [synthetic plan](../../lab/reference-lab/evidence/synthetic-plan.json) is generated from the checked-in [six-guest definition](../../lab/windows-reference.toml) with a fixed all-zero example run ID and a redacted storage root. It names both **Private** Hyper-V switches, all six unique VM names and VHDX paths, resource sizes, separate TEST-NET addresses, `.test` DNS suffixes, per-network DC DNS/time sources, absent default gateways and external DNS, and the discovery probes. Real runs generate a fresh UUID and use an operator-selected private fixed-disk location. No test VM, switch or disk was created for the example.

The runner creates two private switches, six dynamic VHDX disks and six Generation 2 VMs, attaches a digest-checked local ISO to each VM and starts it. The ISO boots an installer; **guest OS installation, patch staging, DNS/time configuration, AD DS or Babel setup and in-guest discovery are not automated**. The `discover` action checks host-visible VM ownership, states and switch attachments, and always reports guest probes unrun and P00-05 cycle incomplete. Operator-controlled guest setup and independent probe evidence remain required before any real cycle can be called complete. This is an explicit implementation limit, not a fabricated discovery pass.

## Preconditions and cleanup

`provision` calls the existing [preflight](../../scripts/preflight_reference_lab.py), requiring an observed eligible x86-64 Hyper-V host, accessible VM/switch inventory, 16 logical CPUs, at least 30,720 MiB available guest memory and 344 GiB free guest disk capacity, and a rights-reviewed manifest with all six local media digests verified. The runner then rechecks each ISO under the private manifest directory and its SHA-256 before any mutation; the Hyper-V helper checks the SHA-256 again before each VM creation. Preexisting run IDs or resources are refused.

An atomic private journal records every exact switch, disk and VM before creation. Creation records each completed step. Teardown walks the journal backward, checks VM ownership notes, private switch type and exact disk path, refuses mismatches or attached foreign resources, and removes only the recorded resources. It then removes the empty run directory; a foreign file is left intact and reported. Failed creation triggers teardown, and the same journal can be passed to teardown after process interruption. The journal is retained as a private audit artifact. A crash between `New-VM` and its ownership note is a narrow fail-closed case requiring operator review; no untagged VM is removed automatically.

Run only from a trusted operator session on an isolated host. Keep media manifest, state root, credentials and raw guest evidence outside Git and public CI. One run ID covers one cycle; use a new run ID and freshly validated inputs for the second cycle. The existing owner decision allows the private preflight route; it does not establish host/media readiness or P00-05 acceptance.

```powershell
python scripts/run_reference_lab.py plan --storage-root D:\LabDisks
python scripts/preflight_reference_lab.py --storage-root D:\LabDisks --media D:\LabMedia\approved.toml
python scripts/run_reference_lab.py provision --storage-root D:\LabDisks --state-root D:\LabState --media D:\LabMedia\approved.toml
python scripts/run_reference_lab.py discover --journal D:\LabState\babel-lab-<run-id>.json
python scripts/run_reference_lab.py teardown --journal D:\LabState\babel-lab-<run-id>.json
```

The operator must record the returned run ID/journal path, independently capture in-guest builds, installed packages, DNS answers, clock offsets, route tables and denied egress, then verify before/after Hyper-V inventories for every exact resource. Store redacted per-cycle evidence separately. These commands do not claim that guest probes have run.

## Fresh local evidence and remaining inputs

The [23 November read-only preflight](../../lab/reference-lab/evidence/local-preflight-2026-11-23.json) exited 2 on the available Windows 11 Pro 26H2 x86-64 machine. Hyper-V and VMMS were present, but VM/switch inventory was unavailable, only 16,613 MiB of guest memory and 266 GiB of disk were available, and all six media entries were missing. It reports both cycles `unrun`. The [synthetic tests](../../tests/test_reference_lab_runner.py) exercised plan topology, unsafe profile refusal, preflight blocking before creation, changed/outside media, successful cleanup, failure after a create, retry after an ownership mismatch, tampered-journal refusal and preservation of a foreign file. Python lint/type checks and PowerShell parser validation pass locally. No live Hyper-V mutation was attempted.

The next owner-supplied input is an **eligible x86-64 Hyper-V host and scoped operator session** with at least 30 GiB allocatable guest RAM, at least 344 GiB free guest-disk space plus staging headroom, and working VM/switch inventory permissions. Provide a private manifest for six already licensed local ISOs with exact SHA-256, edition/build/package pins and per-use rights records. In particular, confirm the Server 2025 Standard and two Windows 11 Pro guest VM/access/activation rights selected in PR #46, plus the Linux images and offline packages. No purchase or evaluation activation is assumed.

For P00-12, this run adds a host-only platform observation; actual guest builds and package inventories remain missing. For P00-16, no new publisher bytes or entitlement evidence were supplied. The synthetic plan and tests use project-owned text only; Windows/Linux private VM use rights and redistribution remain unresolved as recorded in [the asset review](p00-05-p00-12.md#p00-16-dispositions-for-those-assets). The macOS lanes remain separate.

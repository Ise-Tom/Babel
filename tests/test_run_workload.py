"""Exercise direct scheduling and accounting independently from the native CI run."""

import asyncio
import hashlib
import json
import sys
import unittest
from collections import Counter
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_workload as workload  # noqa: E402


class Scheduler(unittest.IsolatedAsyncioTestCase):
    def test_reproducible_offsets_and_mix(self):
        profile = workload.SMOKE
        plan = workload.schedule(profile, "fixture-one")
        self.assertEqual(plan, workload.schedule(profile, "fixture-one"))
        self.assertNotEqual(plan, workload.schedule(profile, "fixture-two"))
        self.assertEqual([o.offset_us for o in plan], [i * 1_000_000 // 60 for i in range(180)])
        for block in range(0, 180, 5):
            self.assertEqual(
                Counter(o.operation for o in plan[block : block + 5]),
                {"rootdse_base": 4, "rootdse_scope_denial": 1},
            )

    async def test_overload_and_absolute_deadline_include_queued_and_rejected_offers(self):
        profile = replace(workload.SMOKE, inflight_limit=1, outstanding_limit=2, deadline_ms=100)
        offers = [workload.Offer(0, "rootdse_base")] * 3

        async def stalled(operation):
            await asyncio.Event().wait()

        samples, peak, inflight = await workload.drive(profile, offers, stalled)
        self.assertEqual((peak, inflight), (2, 1))
        row = workload.summarize(samples, 1)
        self.assertEqual((row["offered"], row["started"], row["completed"]), (3, 1, 0))
        self.assertEqual(
            (row["timed_out"], row["timed_out_before_start"], row["rejected"]), (2, 1, 1)
        )
        self.assertEqual(row["queue_us"]["count"], 1)
        self.assertEqual(row["end_to_end_us"]["count"], 3)
        timeout = row["end_to_end_by_outcome"]["timed_out"]
        self.assertGreaterEqual(timeout["p50_us"], 99_000)

    async def test_scheduler_miss_and_transport_error_are_retained(self):
        async def disconnected(operation):
            raise EOFError

        offers = [workload.Offer(-1_000_000, "rootdse_base"), workload.Offer(0, "rootdse_base")]
        samples, _, _ = await workload.drive(workload.SMOKE, offers, disconnected)
        row = workload.summarize(samples, 1)
        self.assertEqual(
            (row["started"], row["timed_out_before_start"], row["unexpected_error"]), (1, 1, 1)
        )
        self.assertEqual(row["end_to_end_us"]["histogram_us_inclusive_upper_bounds"]["+inf"], 1)

    def test_percentiles_keep_tails_without_histogram_bucket_rounding(self):
        result = workload.distribution([17, 250, 101, 501_000])
        self.assertEqual(
            (result["p50_us"], result["p95_us"], result["p99_us"]), (101, 501_000, 501_000)
        )
        buckets = result["histogram_us_inclusive_upper_bounds"]
        self.assertEqual((buckets["100"], buckets["250"], buckets["+inf"]), (1, 2, 1))


class RetainedSmoke(unittest.TestCase):
    def test_captured_report_preserves_schedule_provenance_and_accounting(self):
        path = Path(__file__).resolve().parents[1] / "lab/p00-09-workload-smoke.json"
        data = json.loads(path.read_bytes())
        self.assertEqual(data["requirement"], "P00-09")
        self.assertEqual(data["profile"], workload.asdict(workload.SMOKE))
        self.assertEqual(data["status"], "passed")
        audit = data["dataset"]["audit"]
        self.assertFalse(data["dataset"]["loaded_into_server"])
        self.assertEqual(audit["status"], "synthetic_fixture_verified")
        self.assertEqual(audit["source_revision"], data["source_revision"])
        for digest in (audit["manifest_sha256"], data["binary_sha256"]):
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
        plan = workload.schedule(workload.SMOKE, audit["seed"])
        expected = hashlib.sha256(workload.encoded([workload.asdict(offer) for offer in plan]))
        self.assertEqual(data["schedule_sha256"], expected.hexdigest())
        self.assertEqual(data["unrun"], workload.UNRUN)
        self.assertTrue(workload.check_smoke(data))
        data["operations"]["rootdse_scope_denial"]["denied"] = 0
        self.assertFalse(workload.check_smoke(data))

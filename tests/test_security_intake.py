"""Negative controls for the offline-only P00-17 rehearsal record."""

import copy
import json
import unittest
from pathlib import Path

from scripts.check_security_intake import check


def record() -> dict:
    return json.loads(
        Path("lab/security-intake/offline-rehearsal.json").read_text(encoding="utf-8")
    )


class SecurityIntakeRecordTest(unittest.TestCase):
    def test_rehearsal_keeps_live_gate_open(self) -> None:
        result = check(record())
        retained = json.loads(
            Path("lab/security-intake/evidence/offline-rehearsal-result.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(result, retained)
        self.assertIs(result["p00_17_ready"], False)
        self.assertEqual(
            result["outcomes"]["all_mock_fields"], "offline_complete_not_gate_evidence"
        )
        self.assertTrue(
            result["outcomes"]["notification_without_owner_receipt"].startswith("incomplete:")
        )

    def test_false_or_corrupt_evidence_is_rejected(self) -> None:
        for change in (
            "claim_live",
            "invent_backup",
            "drop_case",
            "false_pass",
            "wrong_actor",
            "duplicate_event",
            "reverse_time",
        ):
            with self.subTest(change=change):
                data = copy.deepcopy(record())
                first = data["scenarios"][0]
                if change == "claim_live":
                    data["live_report_id"] = "fabricated-id"
                elif change == "invent_backup":
                    data["real_backup_contact"] = "fabricated-person"
                elif change == "drop_case":
                    data["scenarios"].pop()
                elif change == "false_pass":
                    data["scenarios"][1]["expected"] = "offline_complete_not_gate_evidence"
                elif change == "wrong_actor":
                    first["events"][4]["actor"] = "simulated-reporter"
                elif change == "duplicate_event":
                    first["events"].insert(5, copy.deepcopy(first["events"][4]))
                else:
                    first["events"][2]["at_utc"] = "2026-11-22T08:00:00Z"
                with self.assertRaises(ValueError):
                    check(data)

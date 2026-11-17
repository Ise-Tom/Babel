"""Lab definition checks are configuration tests, never Windows execution evidence."""

import copy
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_lab_definition as lab  # noqa: E402


class LabDefinition(unittest.TestCase):
    def setUp(self):
        self.profile = tomllib.loads(lab.PROFILE.read_text())

    def test_committed_definition_is_safe_but_missing_images_are_not_qualified(self):
        lab.validate(self.profile)
        with self.assertRaisesRegex(ValueError, "Missing"):
            lab.validate(self.profile, require_images=True)

    def test_image_metadata_requires_explicit_rights_and_valid_digest(self):
        for machine in self.profile["machines"]:
            machine.update(
                image_id="synthetic-test-image",
                image_sha256="a" * 64,
                build="fixture-build",
                edition="fixture-edition",
                image_license_accepted=True,
            )
        lab.validate(self.profile, require_images=True)
        self.profile["machines"][0]["image_license_accepted"] = False
        with self.assertRaisesRegex(ValueError, "rights not approved"):
            lab.validate(self.profile, require_images=True)
        self.profile["machines"][0]["image_license_accepted"] = True
        self.profile["machines"][0]["image_sha256"] = "not-a-digest"
        with self.assertRaisesRegex(ValueError, "Invalid image digest"):
            lab.validate(self.profile, require_images=True)

    def test_bridges_routes_dns_downloads_or_shared_credentials_are_rejected(self):
        for key in (
            "production_bridge",
            "default_route",
            "external_dns",
            "automatic_image_downloads",
        ):
            profile = copy.deepcopy(self.profile)
            profile["safety"][key] = True
            with self.subTest(key=key), self.assertRaises(ValueError):
                lab.validate(profile)
        for key in ("credentials", "evidence"):
            profile = copy.deepcopy(self.profile)
            profile["safety"][key] = "unsafe"
            with self.subTest(key=key), self.assertRaises(ValueError):
                lab.validate(profile)

    def test_network_overlap_public_network_and_public_dns_are_rejected(self):
        for changes in (
            {"cidr": "192.0.2.0/24"},
            {"cidr": "8.8.8.0/24"},
            {"cidr": "198.51.100.0/23"},
            {"domain": "example.com"},
            {"id": "reference"},
        ):
            profile = copy.deepcopy(self.profile)
            profile["networks"][1].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                lab.validate(profile)

    def test_topology_ids_resources_and_image_metadata_fail_closed(self):
        for changes in (
            {"id": "reference-client"},
            {"role": "windows_client"},
            {"network": "babel"},
            {"cpus": True},
            {"memory_mib": 0},
            {"disk_gib": 10000},
            {"image_id": 123},
            {"image_license_accepted": "yes"},
        ):
            profile = copy.deepcopy(self.profile)
            profile["machines"][0].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                lab.validate(profile)

    def test_unknown_schema_provider_status_and_missing_topology_are_rejected(self):
        for key, value in (
            ("schema_version", True),
            ("schema_version", 2),
            ("provider", "production-host"),
            ("status", "accepted"),
            ("networks", []),
            ("machines", []),
        ):
            profile = copy.deepcopy(self.profile)
            profile[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                lab.validate(profile)

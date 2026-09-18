"""Regression checks for collector KPI spelling and numeric residue."""
import unittest

from agents.rca.metrics import _family, _hypothesis
from agents.rca.onset import summarize_series


class SemanticsTests(unittest.TestCase):
    def test_collector_io_names_and_direction(self):
        for prefix, family, direction in (("r", "read_io", "read"), ("w", "write_io", "write")):
            for suffix in ("_s", "kb_s"):
                name = "system.io." + prefix + suffix
                self.assertEqual(_family(name), family)
                self.assertEqual(_hypothesis("node", name, family, {"direction": "increase", "spike": False}),
                                 f"node disk {direction} I/O consumption")
            self.assertIsNone(_hypothesis("node", f"system.io.{prefix}_await", family, {"direction": "increase"}))
        self.assertEqual(_family("system.disk.readonly"), "unknown")

    def test_disk_space_and_memory_usable_direction(self):
        for name, direction in (("system.disk.pct_usage", "increase"), ("system.disk.used", "increase"),
                                ("system.disk.free", "decrease"), ("system.mem.usable", "decrease")):
            result = _hypothesis("node", name, _family(name), {"direction": direction, "spike": False})
            self.assertEqual(result, "node memory consumption" if "mem" in name else "node disk space consumption")

    def test_recorded_floor_rejects_residue_preserves_activation_and_old_replay(self):
        samples = [(0, 0), (60, 0), (120, 0), (180, 2.8421709430404014e-14), (240, 2.8421709430404014e-14)]
        self.assertTrue(summarize_series(samples, 180, 300)["episodes"])
        self.assertFalse(summarize_series(samples, 180, 300, params={"absolute_noise_floor": 1e-12})["episodes"])
        samples[-2:] = [(180, .001), (240, .002)]
        self.assertTrue(summarize_series(samples, 180, 300, params={"absolute_noise_floor": 1e-12})["episodes"])

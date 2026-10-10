"""Coverage regressions: do not count derived evidence as fresh runs."""

import json
import importlib.util
import pathlib
import tempfile
import unittest
from unittest.mock import patch

import catalogue


class CatalogueTest(unittest.TestCase):
    def test_root_page_glossary_links_stay_at_root(self):
        spec = importlib.util.spec_from_file_location("lab_site", catalogue.ROOT / "probes/site.py")
        site = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(site)
        page = site.essay_page()
        self.assertIn('href="glossary.html#t-', page)
        self.assertNotIn('href="../glossary.html', page)
        self.assertIn('href="../glossary.html#t-dose"', site.popovers({"dose"}))

    def test_separate_counts_and_exclude_reanalyses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            results = root / "results"
            batch = results / "affect16-q27b"
            batch.mkdir(parents=True)
            data = {"model": "qwen-27b", "runs": [{"seed": 1}, {"seed": 2}],
                    "conditions": [1, 2, 3]}
            (batch / "affect16-A.json").write_text(json.dumps(data))
            (batch / "census-affect08.json").write_text(json.dumps(data))
            (batch / "analysis.json").write_text(json.dumps(data))
            (batch / "plain.md").write_text("A summary.")
            record = results / "test-record"
            record.mkdir()
            (record / "plain.md").write_text("A record summary.")
            index = [{"id": "test-record", "unit": 24, "created": "2026-09-07",
                      "model": "qwen-14b-nf4", "film": True},
                     {"id": "no-plain", "unit": "24", "created": "2026-09-08",
                      "model": "qwen-14b-nf4", "film": False},
                     {"id": "audit-record", "unit": "audit", "created": "2026-09-06",
                      "model": "qwen-27b", "film": False}]
            with patch.object(catalogue, "ROOT", root):
                coverage = catalogue.inventory(index)
            self.assertEqual(coverage["record_pages"], 3)
            self.assertEqual(coverage["affect_runs"], 2)
            self.assertEqual(coverage["units"], 1)
            self.assertEqual(coverage["other_groups"], ["audit"])
            self.assertEqual(coverage["plain_summaries"], 1)
            self.assertEqual(coverage["films"], 1)
            self.assertEqual(coverage["models"]["qwen-14b-nf4"], 2)
            self.assertEqual(coverage["batches"][0]["sources"], [
                {"path": "results/affect16-q27b/affect16-A.json", "runs": 2}])

    def test_analysis_only_summary_has_no_new_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            folder = root / "results/affect12-geom-q27b"
            folder.mkdir(parents=True)
            (folder / "plain.md").write_text("Geometry analysis.")
            (folder / "report.json").write_text(json.dumps({"runs": [1, 2, 3]}))
            with patch.object(catalogue, "ROOT", root):
                coverage = catalogue.inventory([])
            self.assertEqual(coverage["affect_runs"], 0)
            self.assertEqual(len(coverage["batches"]), 1)
            self.assertEqual(coverage["batches"][0]["sources"], [])


if __name__ == "__main__":
    unittest.main()

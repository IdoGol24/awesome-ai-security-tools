"""Offline checks for the README header and static entry metrics."""

from html.parser import HTMLParser
import unittest

import gen_readme


class HeaderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ReadmeHeaderTests(unittest.TestCase):
    def test_trendshift_badge_appears_once_below_title(self):
        rendered = gen_readme.build({"sections": []})
        header, _ = rendered.split("> A curated list", 1)
        self.assertTrue(header.startswith("# Awesome AI Security Tools "))
        self.assertEqual(rendered.count("https://trendshift.io/api/badge/"), 1)
        parser = HeaderParser()
        parser.feed(header)
        tags = dict(parser.tags)
        self.assertEqual(
            tags["a"]["href"],
            "https://trendshift.io/repositories/87988?utm_source=trendshift-badge"
            "&utm_medium=badge&utm_campaign=badge-trendshift-87988",
        )
        self.assertEqual(tags["a"]["target"], "_blank")
        self.assertEqual(tags["a"]["rel"], "noopener noreferrer")
        self.assertEqual(
            tags["img"]["src"],
            "https://trendshift.io/api/badge/trendshift/repositories/87988/daily?language=Python",
        )
        self.assertEqual(tags["img"]["alt"],
                         "scadastrangelove/awesome-ai-security-tools | Trendshift")
        self.assertEqual((tags["img"]["width"], tags["img"]["height"]), ("250", "55"))

    def test_entry_metrics_remain_static(self):
        entry = {
            "name": "Example", "repo": "owner/example", "status": ["open_source"],
            "desc": "Example description.",
            "metrics": {"stars": 42, "updated": "2026-10-21", "snapshot": "2026-10-22"},
        }
        rendered = gen_readme.render_entry(entry)
        self.assertIn("42", rendered)
        self.assertIn("updated 2026-10-21", rendered)
        self.assertNotIn("trendshift.io", rendered)
        self.assertNotIn("shields.io", rendered)
        self.assertNotIn("<img", rendered)


if __name__ == "__main__":
    unittest.main()

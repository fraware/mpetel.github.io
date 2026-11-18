#!/usr/bin/env python3
"""Validate machine-readable discovery metadata without editing authored pages.

Requires only Python 3.11+ standard library. External URL availability and search
engine indexing are intentionally outside the scope of these deterministic checks.
"""

from __future__ import annotations

import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = "https://mateopetel.xyz/"
SITEMAP = CANONICAL + "sitemap.xml"
INDEX = CANONICAL + "research-index.json"


class DiscoveryMetadataTests(unittest.TestCase):
    """Check crawl directives, canonical scope, and source-linked metadata."""

    def test_restored_site_is_the_only_indexed_page(self) -> None:
        """The sitemap must refer only to the pre-existing canonical homepage."""
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        self.assertEqual(
            root.tag,
            "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset",
        )
        urls = [
            element.text
            for element in root.findall(
                ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            )
        ]
        self.assertEqual(urls, [CANONICAL])
        self.assertFalse(
            any("lastmod" in element.tag for element in root.iter()),
            "Do not invent modification dates in the sitemap.",
        )
        self.assertEqual((ROOT / "CNAME").read_text(encoding="utf-8").strip(),
                         "mateopetel.xyz")
        self.assertIn(
            '<link rel="canonical" href="' + CANONICAL + '"',
            (ROOT / "index.html").read_text(encoding="utf-8"),
        )

    def test_robots_allow_homepage_discovery(self) -> None:
        """Sitemap advertised once, without blocking legitimate crawlers."""
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        directives = [
            line.strip()
            for line in robots.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(
            directives, ["User-agent: *", "Allow: /", "Sitemap: " + SITEMAP]
        )

    def test_machine_index_has_sources_and_maturity_scope(self) -> None:
        """All project entries point to independently inspectable public sources."""
        catalog = json.loads(
            (ROOT / "research-index.json").read_text(encoding="utf-8")
        )
        self.assertEqual(catalog["schemaVersion"], 1)
        self.assertEqual(catalog["site"], CANONICAL)
        self.assertEqual(catalog["identity"]["profileUrl"], CANONICAL)
        self.assertEqual(
            set(catalog["identity"]["sameAs"]),
            {"https://github.com/fraware",
             "https://www.linkedin.com/in/mateo-petel/"},
        )
        projects = catalog["projects"]
        self.assertEqual(len(projects), 4)
        self.assertEqual(len({p["name"] for p in projects}), len(projects))
        for project in projects:
            with self.subTest(project=project["name"]):
                self.assertTrue(project["summary"])
                self.assertEqual(urlsplit(project["source"]).scheme, "https")
                self.assertTrue(
                    project["source"].startswith("https://github.com/fraware/")
                )
                self.assertEqual(urlsplit(project["url"]).scheme, "https")
                self.assertTrue(
                    project.get("maturity") or project.get("originalPublication")
                )

    def test_agent_navigation_is_descriptive(self) -> None:
        """The optional llms file is an index, not a behavioral instruction."""
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn(CANONICAL, llms)
        self.assertIn(INDEX, llms)
        catalog = json.loads(
            (ROOT / "research-index.json").read_text(encoding="utf-8")
        )
        for project in catalog["projects"]:
            self.assertIn(project["url"], llms)
        self.assertNotRegex(
            llms.lower(),
            re.compile(r"ignore (all )?(previous|prior) instructions"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

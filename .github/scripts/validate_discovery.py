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

    def test_scholarly_registry_provenance(self) -> None:
        """Only directly author-attributed records count as verified works."""
        registry = json.loads(
            (ROOT / "scholarly-records.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registry["schemaVersion"], 1)
        self.assertEqual(registry["authoritativeHomepage"], CANONICAL)
        verified = registry["verifiedRecords"]
        pending = registry["recordsNeedingConfirmation"]
        self.assertEqual(len(verified), 5)
        self.assertEqual(len(pending), 1)
        self.assertEqual(
            len({p["id"] for p in verified + pending}),
            len(verified) + len(pending),
        )
        self.assertEqual(
            {p["publicationStatus"] for p in verified},
            {
                "published-in-ACM-proceedings",
                "accepted-paper-listed",
                "accepted-workshop-paper-listed",
                "accepted-poster-only",
                "listed-in-workshop-poster-session",
            },
        )
        for record in verified:
            with self.subTest(record=record["id"]):
                self.assertEqual(record["authors"], ["Mateo Petel"])
                self.assertEqual(record["year"], 2026)
                self.assertTrue(record["title"])
                self.assertTrue(record["limitations"])
                self.assertEqual(urlsplit(record["primaryRecord"]).scheme, "https")
                if "doi" in record:
                    self.assertEqual(
                        record["category"], "published-workshop-proceedings-paper"
                    )
                else:
                    self.assertNotIn(
                        "published-in-ACM-proceedings",
                        record["publicationStatus"],
                    )
        for candidate in pending:
            with self.subTest(candidate=candidate["id"]):
                self.assertNotIn("authors", candidate)
                self.assertEqual(candidate["authorVerification"], "pending")
                self.assertEqual(urlsplit(candidate["officialList"]).scheme, "https")
        identifiers = registry["identity"]["possibleResearcherIdentifiers"]
        self.assertEqual(len(identifiers), 1)
        self.assertIn("not independently authenticated",
                      identifiers[0]["verificationStatus"])
        self.assertEqual(
            self.catalogue_scholarly_url(),
            CANONICAL + "scholarly-records.json",
        )

    @staticmethod
    def catalogue_scholarly_url() -> str:
        """Return the sidecar link recorded in the existing research index."""
        catalog = json.loads(
            (ROOT / "research-index.json").read_text(encoding="utf-8")
        )
        return catalog["scholarlyRecords"]["url"]

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

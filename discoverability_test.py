"""Static checks for researcher identity, indexing, and research catalog consistency.

Run: python -m unittest discoverability_test.py
Dependencies: Python 3.11+ standard library only.
"""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
DOMAIN = "https://mateopetel.xyz"
HTML_PAGES = (
    "index.html",
    "research.html",
    "publications.html",
    "ai-for-science.html",
    "scientific-agents.html",
    "formal-verification.html",
)


class PageParser(HTMLParser):
    """Collect metadata, links, headings, and JSON-LD without executing scripts."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metas = {}
        self.links = []
        self.anchors = []
        self.headings = []
        self.scripts = []
        self._in_ld = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.metas[key] = attrs.get("content", "")
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "a":
            self.anchors.append(attrs.get("href", ""))
        elif tag == "h1":
            self.headings.append("h1")
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_data(self, data):
        if self._in_ld:
            self.scripts.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_ld = False


class DiscoveryTests(unittest.TestCase):
    """Check essential discovery mechanisms without assuming search ranking outcomes."""

    @classmethod
    def setUpClass(cls):
        cls.pages = {}
        for name in HTML_PAGES:
            source = (ROOT / name).read_text(encoding="utf-8")
            parsed = PageParser()
            parsed.feed(source)
            cls.pages[name] = (source, parsed)
        cls.catalog = json.loads((ROOT / "research.json").read_text(encoding="utf-8"))
        cls.publications = json.loads((ROOT / "publications.json").read_text(encoding="utf-8"))

    def test_html_metadata_and_canonical(self):
        for name, (source, page) in self.pages.items():
            with self.subTest(page=name):
                expected = DOMAIN + ("/" if name == "index.html" else "/" + name)
                self.assertTrue(source.lower().startswith("<!doctype html>"))
                self.assertTrue(page.metas["description"])
                self.assertIn("h1", page.headings)
                canonical = [link["href"] for link in page.links
                             if link.get("rel") == "canonical"]
                self.assertEqual(canonical, [expected])
                self.assertTrue(page.scripts)
                for raw in page.scripts:
                    self.assertIsInstance(json.loads(raw), dict)

    def test_json_ld_references_and_identity(self):
        home = json.loads("".join(self.pages["index.html"][1].scripts))
        graph = {entry["@type"]: entry for entry in home["@graph"]}
        person = graph["Person"]
        self.assertEqual(person["@id"], DOMAIN + "/#person")
        self.assertIn("https://github.com/fraware", person["sameAs"])
        self.assertIn("https://www.linkedin.com/in/mateo-petel/", person["sameAs"])
        self.assertIn("https://foresight.org/people/mateo-petel/", person["sameAs"])
        self.assertIn("https://philab.esa.int/team/mateo-petel/", person["sameAs"])
        self.assertEqual(graph["WebPage"]["mainEntity"]["@id"], person["@id"])
        research = json.loads("".join(self.pages["research.html"][1].scripts))
        index = {entry["@type"]: entry for entry in research["@graph"]}
        self.assertEqual(len(index["ItemList"]["itemListElement"]),
                         len(self.catalog["works"]))

    def test_catalog_links_and_research_status(self):
        html = self.pages["research.html"][0]
        self.assertEqual(self.catalog["person"]["website"], DOMAIN + "/")
        self.assertEqual(len({work["slug"] for work in self.catalog["works"]}),
                         len(self.catalog["works"]))
        for work in self.catalog["works"]:
            with self.subTest(work=work["slug"]):
                self.assertTrue(work["status"].strip())
                self.assertIn(work["source"], html)
                self.assertIn(work["url"], html)
                self.assertIn(work["title"], html)
                self.assertIn(work["slug"], html)
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        for work in self.catalog["works"]:
            self.assertIn(work["source"], llms)

    def test_internal_links_resolve(self):
        for name, (_, page) in self.pages.items():
            for href in page.anchors:
                parts = urlsplit(href)
                if parts.scheme or parts.netloc or not href:
                    continue
                path = parts.path
                if path.startswith("/"):
                    target = ROOT / (path.lstrip("/") or "index.html")
                else:
                    target = ROOT / name if path == "" else ROOT / path
                with self.subTest(page=name, link=href):
                    self.assertTrue(target.is_file(), f"Broken internal link: {href}")

    def test_sitemap_matches_canonical_pages(self):
        tree = ET.parse(ROOT / "sitemap.xml")
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        indexed = {n.text for n in tree.findall("./s:url/s:loc", ns)}
        self.assertEqual(indexed, {DOMAIN + ("/" if p == "index.html" else "/" + p)
                                   for p in HTML_PAGES})
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: " + DOMAIN + "/sitemap.xml", robots)

    def test_publication_provenance_and_status(self):
        """Every scholarly item retains a primary authority and publication class."""
        records = self.publications["publications"]
        self.assertEqual(len(records), 5)
        self.assertEqual(len({e["id"] for e in records}), len(records))
        html = self.pages["publications.html"][0]
        self.assertEqual(self.publications["canonicalUrl"], DOMAIN + "/publications.json")
        for e in records:
            with self.subTest(paper=e["id"]):
                self.assertEqual(e["authors"], ["Mateo Petel"])
                self.assertEqual(e["year"], 2026)
                self.assertTrue(e["status"])
                self.assertIn(e["title"], html)
                self.assertIn('id="' + e["id"] + '"', html)
                self.assertIn(e["primary"], html)
                self.assertTrue(e["record"].startswith("https://"))
                if e["kind"] == "proceedings-paper":
                    self.assertEqual(e["doi"], "10.1145/3806008.3811707")
                else:
                    self.assertNotIn("doi", e, "Unpublished venue work must not imply a DOI")
                if e["kind"].startswith("accepted-workshop"):
                    self.assertIn("workshop", e["status"].lower())

        schema = json.loads("".join(self.pages["publications.html"][1].scripts))
        item_list = next(v for v in schema["@graph"] if v["@type"] == "ItemList")
        self.assertEqual(len(item_list["itemListElement"]), len(records))
        for item in item_list["itemListElement"]:
            self.assertIn(item["url"].split("#")[-1], {e["id"] for e in records})

    def test_internal_discovery_links(self):
        home = self.pages["index.html"][0]
        for page in ("publications.html", "ai-for-science.html",
                     "scientific-agents.html", "formal-verification.html"):
            self.assertIn('href="/' + page + '"', home)
            self.assertIn('href="/' + page + '"', self.pages["research.html"][0])
            self.assertIn(DOMAIN + "/" + page, (ROOT / "llms.txt").read_text(encoding="utf-8"))
        self.assertEqual(self.catalog["publicationsIndex"], DOMAIN + "/publications.html")
        self.assertEqual(self.catalog["bibliography"], DOMAIN + "/publications.json")

    def test_no_agent_instruction_in_public_pages(self):
        for name, (source, _) in self.pages.items():
            with self.subTest(page=name):
                self.assertNotIn("ignore all previous instructions", source.lower())
                self.assertNotIn("color:white", source.replace(" ", "").lower())


if __name__ == "__main__":
    unittest.main()

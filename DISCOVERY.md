# Discovery and indexing maintenance

This is a static GitHub Pages site served at https://mateopetel.xyz/ (see `CNAME`).

## Canonical sources

- `index.html`: primary human-readable identity and homepage.
- `research.html`: selected public research, essays, and software with source links.
- `research.json`: machine-readable navigation index. Entries have explicit status and source URLs.
- `publications.html` and `publications.json`: externally verified publication/status registry, including bibliographic provenance and accepted-workshop distinctions.
- `ai-for-science.html`, `scientific-agents.html`, `formal-verification.html`: substantive topic pages linking directly to source research.
- `llms.txt`: optional discovery guide; no claim that an AI search engine reads or prioritizes it.
- `sitemap.xml` and `robots.txt`: crawler discovery. XML sitemap URLs use the custom domain.

Do not add a project without checking the current repository's public status, original authorship, and technical limitations. Distinguish a personal original project from a fork or an external collaboration. If the publication records change, verify dates, titles, and author attribution from independent conference or publisher records. Never turn workshop acceptance into a main-conference publication or infer a DOI from a planned presentation. If `publications.json` changes, update `publications.html` and all related topic pages. If `research.json` changes, update `research.html`, the `ItemList` JSON-LD, and `llms.txt` in the same change. Keep `sameAs` limited to profiles that refer to the same person. Cite primary project materials rather than inferred research results.

## Validation

From the repository root:

```sh
python -m unittest discoverability_test.py
```

The checks cover canonical URLs, JSON-LD, identity links, catalog consistency, local links, sitemap entries, and removal of agent-directed hidden text. They do not measure real-world search rankings or validate external website availability.

## Post-merge verification

1. Confirm that `https://mateopetel.xyz/`, `/research.html`, `/research.json`, `/robots.txt`, `/sitemap.xml`, and `/llms.txt` return the expected content over HTTPS. Confirm the canonical host and any alternate-domain redirects.
2. Validate structured data with Schema.org Validator and, for supported features, Google's Rich Results Test. A syntactically valid `Person` object does not guarantee a rich result.
3. Verify the `mateopetel.xyz` domain property in Google Search Console; submit `https://mateopetel.xyz/sitemap.xml`, inspect indexing for all canonical HTML pages, and review coverage issues. Configure Bing Webmaster Tools separately if appropriate.
4. Ensure GitHub profile README, LinkedIn profile, and relevant paper/project author bios link back to the canonical website. Keep role and affiliation descriptions current.
5. Establish a baseline in Search Console for branded queries (e.g. "Mateo Petel") and long-tail topical queries that correspond to documented work (e.g. "Mateo Petel scientific agents", "LabTrust Gym hospital automation"). Review impressions, clicks, indexed pages, and referring links monthly. Avoid interpreting a change in ranking from an isolated manual search as causal evidence.

Generic queries like "AI for science Stanford researcher" are highly competitive. Neither structured metadata, sitemaps, nor `llms.txt` provide a guaranteed search placement or citation by a model. The strongest long-term signal is accessible substantive work linked from relevant third-party sources.

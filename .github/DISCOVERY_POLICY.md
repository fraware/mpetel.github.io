# Non-intrusive discovery policy

The authored homepage, its visual presentation, and the GitHub profile README
are controlled by their author. SEO and AI discovery work must not edit those
assets or attempt to rewrite them through generated pages or injected scripts.

## Protected materials

- `index.html` (source of the personal homepage)
- `CNAME` and `favicon.ico` (existing site identity and routing)
- `fraware/fraware:README.md` (GitHub profile homepage; separate repository)
- LinkedIn's user-authored profile content

This repository publishes only four supplementary machine-oriented discovery
sidecars in this change: `robots.txt`, `sitemap.xml`, `llms.txt`, and
`research-index.json`. No extra HTML pages, tracking scripts, keyword text,
schema changes to `index.html`, or personal-profile changes are permitted
within this workstream.

The CI workflow rejects pull requests that modify the protected files in this
repository. It does not control the independent GitHub-profile repository.

## How the sidecars function

- `robots.txt` allows crawling and advertises the XML sitemap.
- `sitemap.xml` lists only the existing canonical homepage. It does not list
  external domains or uncreated HTML pages.
- `llms.txt` is an optional navigation convention for agents, with no
  guarantee that major AI systems fetch, trust, or prioritize it.
- `research-index.json` is standalone navigation metadata that lists
  original public projects, links to their primary sources, and maturity
  qualifications. It is not automatically consumed as embedded JSON-LD by
  Google and does not alter the contents of the personal homepage.

## Verification

Run `python .github/scripts/validate_discovery.py` using Python 3.11+.
GitHub Actions checks the same tests and additionally checks the PR diff for
protected homepage assets. Before merging, compare the Git blob SHAs of
`index.html`, `CNAME`, and `favicon.ico` with those on the target branch.

Search Console property verification, sitemap submission, analytics measurement,
canonical redirect inspection, and cross-site profile metadata remain separate
operational steps that need appropriate access. Only report search-ranking or
AI-citation improvements with measured evidence.

If the author explicitly edits the homepage independently, that is outside
this workstream; the protected-asset PR guard is comparative, not a permanently
pinned hash.

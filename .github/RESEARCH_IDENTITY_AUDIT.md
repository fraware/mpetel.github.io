# Research identity and repository discovery audit
**Audit date:** 2026-11-18  
**Scope:** read-only examination of existing public source records and GitHub repository metadata.

## Non-negotiable preservation rule

**Never alter `index.html` (personal homepage), `fraware/fraware:README.md`
(GitHub profile), LinkedIn profile content, or the authored content of any essay
website in this workstream.** The public site sidecars and documentation in
`.github/` are separate from those protected materials.

Baseline blob identity:
- `fraware/mpetel.github.io:index.html` = `e6865d49fb6900b3c010f55b70b570cfc66ef991`
- `fraware/fraware:README.md` = `993940502b705c3c9d7ba03214183b8b770ca4eb`
- `fraware/mpetel.github.io:CNAME` = `c40be4238fc3146eefd7a8c9a2f8fd042da32a3d`
- `fraware/mpetel.github.io:favicon.ico` = `4f31ae3070a4b5e0fe88f6aa0ea38084f9368bc0`

## What was independently verified

The source-linked selected scholarly record is in
[`scholarly-records.json`](../../scholarly-records.json).

1. **ACM SaT-CPS 2026**: dblp identifies a published contribution on
   pp. 73–82; exact DOI: [10.1145/3806008.3811707](https://doi.org/10.1145/3806008.3811707).
   The dblp record associates an ORCID identifier
   `0009-0006-7159-2375`. This is *bibliographic association*, not
   independent proof that the researcher controls that ORCID account.
   [Record](https://dblp.org/rec/conf/sat-cps/Petel26).
2. **IWSEC 2026**: the official accepted-paper title is
   "Runtime Enforcement for Agentic CPS Tool Invocation".
   [Accepted list](https://www.iwsec.org/2026/accepted_papers.html).
   Verify any final DOI only once the publisher makes a proceedings record available.
3. **CoRL Agentic Robotics 2026**: official workshop list gives
   "Recovery Credit: Evaluating Robot Decisions Under Physical-State Uncertainty"
   and author Mateo PETEL. Workshop status is distinct from archival
   main-conference CoRL status.
   [Accepted list](https://agentic-robotics-workshop.github.io/papers).
4. **SaTQuML 2026**: official P07 poster-only listing names the exact
   title and Mateo Petel.
   [Program](https://satquml.github.io/).
5. **AgenticOS 2026**: official workshop poster list identifies
   "What Must Agent Memory Preserve? Representation Contracts for Exact
   Invalidation" by Mateo Petel.
   [Program](https://agentic-fmos.github.io/).
6. **MATH-AI 2026**: the workshop accepted-paper list includes
   "Feedback Aliasing in Lean Repair Loops: A Controlled Intervention Study".
   It does *not* identify the author next to the title. The OpenReview
   page is gated by a browser challenge in this audit. Mateo Petel appears
   elsewhere on the workshop website in the reviewer list, which **does not
   independently establish paper authorship**. This entry remains
   author-attribution-pending in the machine-readable registry.
   [Workshop accepted list](https://mathai-2026.github.io/papers/).

Independent identity pages:
- [Foresight Institute](https://foresight.org/people/mateo-petel/)
  identifies the researcher and links the canonical site.
- [ESA Phi-lab](https://philab.esa.int/team/mateo-petel/) contains an older
  trainee biography referring to a 2023 future Stanford program. Treat
  this as historical material, not a current job title.
- [G-Research September 2026 grant winners](https://www.gresearch.com/news/g-research-september-2026-grant-winners/)
  includes a named researcher entry.

## GitHub About metadata audit

These observations use the public repository REST metadata and source READMEs
on 2026-11-18. **No About settings, topic sets, homepage fields, README files,
or source code were modified.** The connector available in this chat provides
repository metadata *read* access, not a matching write action.

| Repository | Observed discovery state | Proposed settings-only follow-up |
| --- | --- | --- |
| [Personal website](https://github.com/fraware/mpetel.github.io) | Description `Github Page M. Petel`; homepage URL empty; no topics. | Verify the About URL is set to `https://mateopetel.xyz/`; use accurate, concise research identity language and a few relevant topics. Preserve `index.html`. |
| [GitHub profile](https://github.com/fraware/fraware) | About description, homepage, topics empty. | Only edit independent repository About fields if authorized; never edit the profile README or displayed metrics. |
| [Forward Science](https://github.com/fraware/forward-science) | Clear descriptive About field; canonical Pages URL; relevant topics. | Maintain current metadata unless source content substantively changes. |
| [Compositional Intelligence](https://github.com/fraware/compositional-intelligence) | Accurate description and canonical Pages URL; topics emphasize compositionality and formal methods. | Consider `compositional-intelligence` or `ai-for-science` topic only if the README supports the designation; avoid broad keyword stuffing. |
| [LabTrust-Gym](https://github.com/fraware/LabTrust-Gym) | Description captures PettingZoo/Gym, though it omits simulation-only and not-clinical scope. | Clarify in About: research simulator and benchmarks; never describe as real clinical deployment. Candidate topics: `ai-for-science`, `agent-evaluation`, `multi-agent-systems`. |
| [MathEvidence](https://github.com/fraware/MathEvidence) | Detailed About description and Lean/math topics. | Keep exact source-limited claims; all capabilities remain research-preview maturity. |
| [LeanVerifier](https://github.com/fraware/leanverifier) | About description advertises robustness, fairness and interpretability of ML models; topic `transformers`. README and STATUS.md expressly limit formal implementation to rational affine binary classifiers; neural networks and transformers are unsupported legacy material. | Highest-priority settings correction. Suggested About: `Lean 4 research preview for exact rational affine classifiers and scoped L-infinity robustness checks; validation and release authorization pending.` Remove `transformers` topic; choose `lean4`, `formal-verification`, `affine-classifiers`, `research-preview`. |
| [POELIO](https://github.com/fraware/POELIO) | Domain-matched Pages URL; literary topics. | Retain. |
| [Verse](https://github.com/fraware/verse) | Domain-matched Pages URL; local-first/editor topics. | Retain. |

## Next evidence and permissions gates

- Obtain author-authenticated confirmation of the ORCID identifier and confirm
  the identity is recorded consistently by publisher, OpenAlex and scholarly
  registries before promoting it to a verified researcher alias.
- Inspect the MATH-AI manuscript's official authorship metadata. Keep it
  separate until a primary record is accessible.
- Confirm whether final IWSEC proceedings metadata is available following
  the scheduled conference, without assuming an accepted paper is published.
- Obtain Google Search Console and Bing Webmaster Tools property access.
  No impression, CTR, index coverage or ranking values are presently available
  from those services in this chat. Do not claim outcomes without them.
- If direct repository settings writes become available, review each proposed
  About edit for factual accuracy and target only approved metadata fields.
  README prose and website authored text remain immutable.
- Check independent publication-archiving permissions and release maturity
  before creating software or manuscript DOIs. Do not publish an experimental
  release solely for indexing benefits.

## Evidence standard

Every registry item has direct source URLs and an explicit status. The registry
is not a publisher DOI record, a complete CV, a citation count, or embedded
`schema.org` JSON-LD. It does not prove search ranking changes.

# {Topic}

**Date:** {YYYY-MM-DD}
**Agents:** {N} parallel researchers (sonnet)

---

## Sources & URLs

<!--
  Numbered list of every unique source consulted across all researchers.
  One line per source: `1. [Anchor text](URL) — annotation.`
  Aim for at least N×3 unique URLs. Deduplicate where the same URL was
  cited by multiple researchers.
-->

1. [Source title](https://example.com/path) — what's there in one line.
2. [Source title](https://example.com/path) — what's there in one line.
3. ...

## Summary

<!--
  Two or three paragraphs. Executive-level overview of the topic across
  all researched angles. Prose only — no bullets here. Acknowledge any
  angles where coverage was thin or where researchers disagreed.
-->

{First paragraph: framing — what is this topic, why it matters, what
the report covers.}

{Second paragraph: the main story across the angles — the most
important threads.}

{Optional third paragraph: caveats, gaps, open questions.}

## Key Findings

<!--
  5 to 10 bulleted takeaways, ranked by importance. Each finding is
  one sentence stating the fact, followed by inline source links.
  No researcher attributions ("Researcher 2 noted …") — speak as the
  synthesized voice.
-->

1. **{Finding}** — {1-sentence elaboration}. ([source](URL), [source](URL))
2. **{Finding}** — {1-sentence elaboration}. ([source](URL))
3. ...

## Comparison Table (optional)

<!--
  Include ONLY when the topic compares 3+ entities/options across 3+
  attributes (e.g. "compare LLM providers", "compare deployment
  options"). Otherwise delete this whole section — do not ship an
  empty placeholder.
-->

| {Entity}    | {Attribute 1} | {Attribute 2} | {Attribute 3} |
| ----------- | ------------- | ------------- | ------------- |
| {Option A}  | ...           | ...           | ...           |
| {Option B}  | ...           | ...           | ...           |
| {Option C}  | ...           | ...           | ...           |

## Confidence & Gaps

<!--
  Brief honesty section. Where was the evidence thin? Where did sources
  disagree? What did the team not cover? Helps the reader calibrate.
-->

- {Gap or low-confidence claim}
- {Researcher disagreement worth surfacing}

---

## Raw Researcher Dumps

<!--
  Appended for traceability. One `### Researcher N — <angle>` subsection
  per agent, containing that agent's verbatim output. Replaces the old
  separate ./output/<slug>/raw/ folder so the whole report lives in one
  readable file.
-->

### Researcher 1 — {angle}

{verbatim output of researcher 1}

### Researcher 2 — {angle}

{verbatim output of researcher 2}

### Researcher N — {angle}

{verbatim output of researcher N}
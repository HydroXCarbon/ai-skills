<!--
  Markdown skeleton for the consensus research report. The skill writes
  this to ./output/<slug>/report.md, then scripts/<slug>.py renders it
  to PDF. Replace the {placeholders} with synthesized content.
-->

# {TOPIC}

**Date:** {YYYY-MM-DD}
**Agents:** {N} Sonnet agents (same prompt, independent runs)

## Sources & URLs

1. [{short title}]({URL}) — {one-line annotation}
2. [{short title}]({URL}) — {one-line annotation}
3. ...

## Summary

{Two-to-three paragraph executive summary. State the strongest consensus findings first; note any major dissent.}

## Strong Consensus

Claims with score ≥ ⌈N/2⌉+1.

- **{K/N}** — {Claim sentence}. Source: [{canonical url}]({URL}).
- **{K/N}** — {Claim sentence}. Source: [{canonical url}]({URL}).

## Partial Consensus

Claims with 2 ≤ K ≤ ⌈N/2⌉.

- **{K/N}** — {Claim sentence}. Source: [{canonical url}]({URL}).
- **{K/N}** — {Claim sentence}. Source: [{canonical url}]({URL}).

## Outliers / Dissent

Single-agent claims and any contradictions between clusters.

- **1/N (outlier)** — {Claim sentence}. Source: [{canonical url}]({URL}).
- **Dissent** — {Claim A} ({K/N}) contradicts {Claim B} ({K/N}). Sources: [{URL A}]({URL A}), [{URL B}]({URL B}).

## Tables (optional)

Only include when comparing entities/options across attributes.

| {Entity} | {Attribute 1} | {Attribute 2} | Consensus |
| -------- | ------------- | ------------- | --------- |
| ...      | ...           | ...           | {K/N}     |

---

## Raw Agent Dumps

<!--
  Appended for traceability. One `### Agent N` subsection per agent
  containing that agent's verbatim output. Replaces the old separate
  ./output/<slug>/raw/ folder so the whole report lives in one readable
  file.
-->

### Agent 1

{verbatim output of agent 1}

### Agent 2

{verbatim output of agent 2}

### Agent N

{verbatim output of agent N}
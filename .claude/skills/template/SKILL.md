---
# Skill slug. Lowercase kebab-case. Must match the folder name.
name: template

# Trigger sentence Claude reads to decide whether to load this skill.
# Phrase as "Use when ...". This is the matcher — keep it specific.
description: "Folder template for new Claude skills — do not invoke directly. Copy via /create-skills."

# Optional. Hint shown to authors about what the skill expects as input.
# Skills don't receive `$ARGUMENTS` like commands do; this is documentary
# only. Delete this key if the skill takes no implicit arguments.
argument-hint: "{<required arg> or [optional arg]}"

# Optional. Comma-separated tool allowlist. Use scoped Bash patterns
# (e.g. `Bash(git status:*)`) when possible. Delete this key to inherit
# the session's full toolset.
allowed-tools: "Read, Bash(mkdir:*), AskUserQuestion"
---

# {Skill Display Name}

## Overview

<!--
  One short paragraph: what this skill does at a high level. Distinct
  from the frontmatter description — that's the matcher. Trigger
  phrases and negative cases go in `## When to use` below, not here.
-->

{Two- or three-sentence description of what this skill does, when it
activates, and what the user can expect as output.}

## When to use

<!-- Trigger phrases that should activate this skill, plus the
     negative cases that should NOT trigger it. The frontmatter
     description is the primary matcher; this section expands it
     with concrete examples and boundaries the matcher alone can't
     capture.

     Delete this section if the skill's frontmatter description is
     already specific enough to stand alone. -->

Trigger phrases include "{example phrase 1}", "{example phrase 2}", "{example phrase 3}".

Do **not** trigger for {boundary case 1} or {boundary case 2} — those are different skills.

## Arguments

<!--
  Description of the arguments this skill accepts. Skills do not
  receive $ARGUMENTS directly; instead, identify the semantic
  fields this skill extracts from the user's prompt.
-->

- **{arg1}** — {description}

## Step 1 — {verb phrase}

<!-- What the skill does first. Validate input, gather context, slugify
     args, etc. Use parallel tool calls when reads are independent.
     Delete this whole step if not needed. -->

- {action or command}
- {action or command}

## Step 2 — {verb phrase}

<!-- Core decision or transformation. Branch on what Step 1 found.
     If the skill has multiple branches, spell each one out:
       - **{condition}** → {action}. **Stop.**
       - **{condition}** → proceed to Step 3.
-->

- {action or command}

## Step 3 — {verb phrase}

<!-- Output, side effect, or final action. If the skill makes a
     destructive or irreversible change, preview it and confirm via
     `AskUserQuestion` before acting. Add Step 4..N as needed. -->

- {action or command}

<!--
  ─── Subfolder reference cheatsheet ───
  Keep only the line(s) matching subfolders this skill actually ships
  with. Delete the rest. /create-skills will strip the unused lines
  for you when scaffolding a new skill.

  For detailed criteria, see [references/example.md](references/example.md).
  Run [scripts/example.py](scripts/example.py) to validate the input.
  Use the template at [assets/README.md](assets/README.md).
-->

## Open questions

<!-- Runtime clarifying questions Claude should ask via `AskUserQuestion`
     when the user's input is ambiguous. NOT author-time TODOs.

     Pattern: state the trigger condition, then list 2–4 options. The
     runtime adds an "Other" option automatically — don't include it.

     Delete this whole section if the skill never needs to clarify. -->

If `{ambiguity description}`, ask via `AskUserQuestion`:

- **{Option label}** — {what happens if chosen}
- **{Option label}** — {what happens if chosen}

## Hard rules

<!-- Absolute invariants. Short, declarative, no hedging — no "usually"
     or "prefer". If something belongs here it must never be violated.

     Delete this section if the skill has no destructive operations
     and no invariants to enforce. -->

- {Invariant 1}
- {Invariant 2}
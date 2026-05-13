---
# One-line trigger sentence. Action verb, present tense. This is what users
# see in the `/` slash-command list and what Claude reads to decide intent.
description: "{Verb-phrase describing what this command does, in one line.}"

# Comma-separated allowlist. Use scoped Bash patterns where possible
# (e.g. `Bash(git status:*)`) instead of broad `Bash`. Include
# `AskUserQuestion` only if the Open questions section below is kept.
allowed-tools: Read, Bash(git status:*), AskUserQuestion

# Shown in `/` autocomplete. Wrap optional args in [brackets], required in {}.
# Delete this key entirely if the command takes no args.
argument-hint: "[optional {thing}]"
---

# {Command Display Name}

<!--
  Body opener: one or two sentences stating the command's intent.
  This is the prompt Claude runs when the user invokes `/<name>`.
  Keep it focused on a single intent — split into a separate command
  if you find yourself writing "and also ...".
-->

{One- or two-sentence statement of what this command does and on what.}

<!-- $ARGUMENTS holds whatever the user typed after the command name.
     May be empty — handle that case explicitly in Step 1 if it matters. -->
User input (may be empty): `$ARGUMENTS`

## Step 1 — {verb phrase}

<!-- What Claude does here. Typical first steps: inspect state, validate
     args, gather context. Use parallel Bash calls (single message, multiple
     tool calls) when the reads are independent. Delete this whole step if
     not needed. -->

- `{command or action}`
- `{command or action}`

## Step 2 — {verb phrase}

<!-- The core decision or transformation. Branch on what Step 1 found.
     If the command has multiple branches, spell each one out:
       - **{condition}** → {action}. **Stop.**
       - **{condition}** → proceed to Step 3.
-->

- `{command or action}`

## Step 3 — {verb phrase}

<!-- Output, side effect, or final action. If the command makes a
     destructive or irreversible change (commit, push, delete, write
     to a shared system), preview the change and confirm via
     AskUserQuestion before acting. Duplicate this step or add Step 4..N
     as needed; delete what you don't use. -->

- `{command or action}`

## Open questions

<!-- Runtime clarifying questions Claude should ask via AskUserQuestion
     when the user's input is ambiguous. NOT author-time TODOs.

     Pattern: state the trigger condition, then list 2–4 options. The
     runtime adds an "Other" option automatically — don't include it.

     Delete this whole section if the command never needs to clarify. -->

If `{ambiguity description}`, ask via `AskUserQuestion`:

- **{Option label}** — {what happens if chosen}
- **{Option label}** — {what happens if chosen}
- **{Option label}** — {what happens if chosen}

## Hard rules

<!-- Absolute invariants. Short, declarative, no hedging — no "usually" or
     "prefer". If something belongs here it must never be violated.

     Typical entries for git/fs/network commands:
       - Never use `--amend`, `--no-verify`, `--no-gpg-sign`, or `-a`.
       - Never run `git push`.
       - Never touch unstaged changes.
       - If a hook fails: report verbatim and stop.

     Delete this section if the command has no destructive operations
     and no invariants to enforce. -->

- {Invariant 1}
- {Invariant 2}
---
description: Draft a planning spec from a brief, on a new claude/feature/<slug> branch.
allowed-tools: Read, Write, Bash(git status:*), Bash(git rev-parse:*), Bash(git checkout:*), Bash(git branch:*), Bash(test:*), AskUserQuestion
argument-hint: "<feature brief>"
---

# Spec

Draft a planning spec for the brief in `$ARGUMENTS`. Create a new `claude/feature/<slug>` branch, then write `_specs/<slug>.md` from `_specs/template.md` with each section drafted from the brief. Planning only — no code, no implementation details.

User input (may be empty): `$ARGUMENTS`

## Step 1 — Validate brief and derive slug

- If `$ARGUMENTS` is empty: ask via `AskUserQuestion` for the feature brief in one or two sentences. Use the answer as the brief.
- Derive `feature-slug` from the brief: lowercase, replace spaces and `_` with `-`, strip punctuation other than `-`, collapse repeated `-`, trim leading/trailing `-`. Cap at ~60 chars.
- Reject reserved slug `template`. **Stop.**

## Step 2 — Verify clean working tree

Run in parallel (single message, multiple Bash calls):

- `git status --porcelain`
- `git rev-parse --abbrev-ref HEAD` (capture as source branch for the final report)

If `git status --porcelain` produces any output: **stop and report** the dirty paths. Tell the user to commit or stash before retrying. Do not branch, do not write the spec.

## Step 3 — Check for collisions

Run in parallel:

- `test -f _specs/<feature-slug>.md` → if it exists, **stop and report** the existing path. Do not overwrite.
- `git branch --list claude/feature/<feature-slug>` → if non-empty, **stop and report** the existing branch. Do not force-create.

## Step 4 — Create and switch branch

- `git checkout -b claude/feature/<feature-slug>`

If checkout fails for any reason, report the error verbatim and stop. Do not retry with `-B` or `--force`.

## Step 5 — Draft the spec

Create a markdown spec document that plan mode can use directly, and save it to `_specs/<feature-slug>.md`. Use the **exact structure** defined in `_specs/template.md` — that file owns the section list, per-section guidance, and the authoring rules.

- Read `_specs/template.md`. Follow its structure and its top-comment authoring rules verbatim.
- Substitute `<feature-name>` in the H1 with a human-readable feature name (title-cased slug by default; override if the brief implies a clearer name).
- Draft each section from the brief, obeying the per-section guidance written in the template's HTML comments.
- Write the result to `_specs/<feature-slug>.md` via `Write`. Do not add technical implementation details such as code examples.

## Step 6 — Report

Print:

- New spec path: `_specs/<feature-slug>.md`
- New branch: `claude/feature/<feature-slug>`
- Source branch (from Step 2)
- Count of bullets in **Open questions**
- Reminder: the spec file is **uncommitted** — review and commit manually.

## Open questions

If the brief is too vague to derive a meaningful slug or summary, ask via `AskUserQuestion`:

- **Restate the brief** — provide a clearer one-sentence description of the feature.
- **Pick a suggested slug** — Claude offers 2–3 candidate slugs derived from the brief for the user to choose from.
- **Cancel** — abort without creating the branch or spec.

## Hard rules

- Never overwrite an existing `_specs/<slug>.md`. Stop on conflict.
- Never overwrite or force-create an existing branch. Never use `git checkout -B`, `--force`, or `-f`.
- Never include code blocks, function signatures, file paths to be created/edited, library/framework choices, or other implementation details in the drafted spec. Planning only.
- Never run `git add`, `git commit`, `git push`, or modify any file outside `_specs/<feature-slug>.md`.
- Reject `template` as a slug — that name belongs to the source template.
- Stop immediately if the working tree is dirty. Do not stash, do not `--force`, do not carry changes onto the new branch silently.

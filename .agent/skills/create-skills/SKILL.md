---
name: create-skills
description: "Use when the user wants to scaffold a new skill folder from the template, create a new skill, or add a skill to the project."
---

# Create Skills

## Overview

Scaffolds a new skill under `.agents/skills/<slug>/` by copying `.agents/skills/template/`. Infers which optional subfolders (`scripts/`, `references/`, `assets/`) the skill needs from its description; the script language is confirmed with the user if scripts are included.

## When to use

Trigger phrases include "create a new skill", "scaffold a skill", "add a skill", "new skill called", "set up a skill folder".

Do **not** trigger for editing an existing skill, running a skill, or listing skills — those are separate tasks.

## Arguments

- **skill-slug** *(optional)* — the desired kebab-case identifier for the new skill, extracted from the user's prompt. If absent, ask.

## Step 1 — Resolve the slug

- If a slug was provided in the prompt: slugify it — lowercase, replace spaces and `_` with `-`, strip punctuation other than `-`, collapse repeated `-`.
- If absent: ask the user via `ask_question` for the skill name, then slugify their answer.
- Run `test -d .agents/skills/<slug>/`. **If the directory exists, stop and report the conflict.** Do not overwrite; do not add a numeric suffix.
- Reject reserved name `template`. **Stop.**

## Step 2 — Gather metadata

Ask via `ask_question` (one question per field):

- **Description** — the trigger sentence used to decide whether to load the skill. Should start with "Use when …" and be specific.
- **Display name** — the human-readable name for the `# {Skill Display Name}` H1 (e.g. slug `code-reviewer` → display `Code Reviewer`). Default to title-casing the slug; allow override.
- **Takes arguments?** — yes / no. If yes, ask once more for the `argument-hint` string (e.g. `"<topic>"` or `"[optional flag]"`).

Hold these values for Step 5.

## Step 3 — Decide optional subfolders (decide yourself)

Based on the skill's description from Step 2, infer which of the three optional subfolders the skill needs. Do **not** ask the user — make the call yourself. Empty selection is valid (SKILL.md only).

Decision heuristics:

- **scripts/** — include if the skill needs executable code: parsing, automation, data processing, API calls, validation logic, or any step better expressed in code than prose. Skip if the skill is purely procedural prose.
- **references/** — include if the skill has detailed sub-conditions, lookup tables, playbooks, or deep-dive material. Skip if SKILL.md contains everything inline.
- **assets/** — include if the skill needs static files at runtime: templates, fixtures, sample configs. Skip if no static file is needed.

Announce the choice in one short sentence so the user can override if they disagree. Proceed without waiting unless they object.

## Step 4 — Pick scripts language (only if scripts/ chosen)

Ask via `ask_question`:

- **Python (Recommended)** — keep `scripts/example.py` as-is, rename to `scripts/<slug>.py`.
- **Other** — ask in a follow-up `ask_question` which language. Generate the equivalent stub with the chosen language's idiomatic comment style and main-entry pattern.

## Step 5 — Generate the skill folder

Run these in order:

1. `mkdir -p .agents/skills/<slug>/`
2. Read `.agents/skills/template/SKILL.md`, then write to `.agents/skills/<slug>/SKILL.md` with substitutions:
   - `name: template` → `name: <slug>`
   - `description: "Folder template…"` → `description: "<user-provided description>"`
   - If args used: replace the `argument-hint` placeholder. If not: delete the `argument-hint` line.
   - `# {Skill Display Name}` → `# <user-provided display name>`
3. For each chosen subfolder, copy the template's contents:
   - **scripts/** → `cp -r .agents/skills/template/scripts .agents/skills/<slug>/scripts`, then rename `example.py` to `<slug>.<ext>`.
   - **references/** → `cp -r .agents/skills/template/references .agents/skills/<slug>/references`.
   - **assets/** → `cp -r .agents/skills/template/assets .agents/skills/<slug>/assets`.
4. Strip cheatsheet lines in the new `SKILL.md` for each subfolder NOT chosen.

## Step 6 — Offer to symlink globally

Ask via `ask_question`:

- **Symlink to `~/.gemini/config/skills/<slug>/`** *(Recommended for skills used across projects)* — `ln -s "$(realpath .agents/skills/<slug>)" ~/.gemini/config/skills/<slug>`.
- **No, project-level only** — skill loads only when this repo is cwd.

If the symlink target already exists, **stop** before running `ln` and report the conflict. Do not pass `-f`.

## Step 7 — Print result

Report:

- Absolute path to the new skill folder.
- Subfolders included (or "SKILL.md only" if none).
- Whether a global symlink was created and its path.
- Reminder: edit `SKILL.md` to fill in the body steps, Open questions, and Hard rules sections.

## Hard rules

- Never overwrite an existing `.agents/skills/<slug>/`. Stop on conflict.
- Never overwrite an existing symlink target. Stop on conflict; never pass `ln -f`.
- Never modify files outside the new skill folder (and the optional symlink).
- Never delete files. Never run `git add`, `git commit`, or `git push`.
- Reject `template` as a slug.
- Use exactly the script language the user specified — don't auto-translate idioms.

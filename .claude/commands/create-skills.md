---
description: Scaffold a new Claude skill folder from `.claude/skills/template/` with optional scripts, references, and assets.
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(cp:*), Bash(test:*), Bash(ln:*), Bash(realpath:*), AskUserQuestion
argument-hint: "[skill-slug]"
---

# Create Skills

Scaffold a new Claude skill under `.claude/skills/<slug>/` by copying `.claude/skills/template/`. Claude infers which optional subfolders the skill needs from its description; the script language is still confirmed with the user if scripts are included.

User-supplied slug (optional, may be empty): `$ARGUMENTS`

## Step 1 — Resolve the slug

- If `$ARGUMENTS` is non-empty: slugify it — lowercase, replace spaces and `_` with `-`, strip punctuation other than `-`, collapse repeated `-`.
- If empty: ask the user via `AskUserQuestion` for the skill name, then slugify their answer.
- Run `test -d .claude/skills/<slug>/`. **If the directory exists, stop and report the conflict.** Do not overwrite; do not add a numeric suffix.
- Reject reserved name `template`. **Stop.**

## Step 2 — Gather metadata

Ask via `AskUserQuestion` (one question per field):

- **Description** — the trigger sentence Claude reads to decide whether to load the skill. Should start with "Use when …" and be specific.
- **Display name** — the human-readable name for the `# {Skill Display Name}` H1 (e.g. slug `code-reviewer` → display `Code Reviewer`). Default to title-casing the slug; allow override.
- **Takes arguments?** — yes / no. If yes, ask once more for the `argument-hint` string (e.g. `"<topic>"` or `"[optional flag]"`).

Hold these values for Step 5.

## Step 3 — Decide optional subfolders (Claude decides)

Based on the skill's description from Step 2, infer which of the three optional subfolders the skill needs. Do **not** ask the user — make the call yourself. Empty selection is valid (SKILL.md only).

Decision heuristics:

- **scripts/** — include if the skill needs executable code: parsing, automation, data processing, API calls, validation logic, or any step better expressed in code than prose. Skip if the skill is purely procedural prose (asking questions, running shell one-liners, writing files via `Write`).
- **references/** — include if the skill has detailed sub-conditions, lookup tables, playbooks, or deep-dive material that should only load when a specific branch fires. Skip if the SKILL.md body already contains everything needed inline.
- **assets/** — include if the skill needs static files at runtime: templates, fixtures, sample configs, images, fonts. Skip if no static file is needed.

After deciding, announce the choice in one short sentence (e.g. *"Including `references/` and `assets/` — skill needs a crash-handling playbook and a TSV header template."*) so the user can override if they disagree. Proceed without waiting unless they object.

## Step 4 — Pick scripts language (only if scripts/ chosen)

Ask via `AskUserQuestion`:

- **Python (Recommended)** — keep `scripts/example.py` as-is, rename to `scripts/<slug>.py`.
- **Other** — ask in a follow-up `AskUserQuestion` which language. Generate the equivalent stub:
  - file extension matches the language (`.js`, `.ts`, `.sh`, `.rb`, etc.).
  - module-level docstring/comment mirrors the Python stub's wording, in the chosen language's idiomatic comment style.
  - main entry mirrors the Python `if __name__ == "__main__":` pattern (e.g. `function main()` for JS, top-level for shell).

## Step 5 — Generate the skill folder

Run these in order:

1. `mkdir -p .claude/skills/<slug>/`
2. Use `Read` on `.claude/skills/template/SKILL.md`, then `Write` to `.claude/skills/<slug>/SKILL.md` with substitutions:
   - `name: template` → `name: <slug>`
   - `description: "Folder template…"` → `description: "<user-provided description>"`
   - If args used: replace the `argument-hint` placeholder with the user's string. If not: delete the `argument-hint` line and its preceding comment block.
   - `# {Skill Display Name}` → `# <user-provided display name>`
3. For each chosen subfolder, copy the template's contents:
   - **scripts/** → `cp -r .claude/skills/template/scripts .claude/skills/<slug>/scripts`, then rename `<slug>/scripts/example.py` to `<slug>/scripts/<slug>.<ext>`. If language is non-Python, replace the file's content with the chosen-language stub from Step 4.
   - **references/** → `cp -r .claude/skills/template/references .claude/skills/<slug>/references`. Keep `example.md` as-is — author edits it.
   - **assets/** → `cp -r .claude/skills/template/assets .claude/skills/<slug>/assets`. Keep `README.md` as-is — author replaces it when adding real assets.
4. Strip the cheatsheet lines in the new `SKILL.md` for each subfolder NOT chosen, so the author isn't left with broken links. The cheatsheet block in the template is delimited by `─── Subfolder reference cheatsheet ───` and the closing `-->`. Remove the `[scripts/...]`, `[references/...]`, or `[assets/...]` line for each unchosen subfolder. If all three are unchosen, remove the entire cheatsheet block.

## Step 6 — Offer to symlink globally

Ask via `AskUserQuestion`:

- **Symlink to `~/.claude/skills/<slug>/`** (Recommended for skills used across projects) — `ln -s "$(realpath .claude/skills/<slug>)" ~/.claude/skills/<slug>`.
- **No, project-level only** — skill loads only when this repo is cwd.

If the symlink target already exists, **stop** before running `ln` and report the conflict. Do not pass `-f`.

## Step 7 — Print result

Report:

- Absolute path to the new skill folder.
- Subfolders included (or "SKILL.md only" if none).
- Whether a global symlink was created and its path.
- Reminder: edit `SKILL.md` to fill in the body steps, Open questions, and Hard rules sections — the scaffold ships with placeholders.

## Hard rules

- Never overwrite an existing `.claude/skills/<slug>/`. Stop on conflict.
- Never overwrite an existing `~/.claude/skills/<slug>` symlink target. Stop on conflict; never pass `ln -f`.
- Never modify files outside the new skill folder (and the optional symlink).
- Never delete files. Never run `git add`, `git commit`, or `git push`.
- Reject `template` as a slug — that name belongs to the source template.
- If the user picks a non-Python script language, use exactly what they specified — don't auto-translate Python idioms.

# AGENTS.md

> Rules and conventions for **all AI agents** (Antigravity, Codex, etc.) working in this repository.

## What this repo is

Personal vault of AI CLI customizations — skills, slash commands, subagents, and extensions for **Claude Code** and **Antigravity**. There is **no build, test, or lint step**. Everything is Markdown / JSON config consumed directly by the CLIs.

## Core rules

1. **No code generation outside config files.** This repo contains only declarative config (Markdown, TOML, JSON). Do not add Python, TypeScript, shell scripts, or other executable code unless it lives inside a skill's `scripts/` subdirectory and is directly referenced by that skill's `SKILL.md`.

2. **Preserve frontmatter.** Every `SKILL.md`, command `.md`, and agent `.md` file starts with YAML frontmatter. Never strip, reorder, or silently alter frontmatter fields.

3. **Match an existing example before inventing structure.** Before creating a new item, read at least one existing item of the same type (skill, command, agent) to confirm the expected shape.

4. **Do not symlink templates.** The `template` scaffolds (`.claude/commands/template.md`, `.claude/agents/template.md`, `.claude/skills/template/SKILL.md`) are starting-point copies — never symlink them.

5. **Claude commands use `$ARGUMENTS`.** Do not use other placeholder styles (e.g. `{{args}}`) in Claude command bodies.

6. **Skills live in the right CLI folder.** Claude skills go in `.claude/skills/`; Antigravity skills go in `.agent/skills/`. Do not mix them.

7. **Descriptions are matchers, not documentation.** The `description` frontmatter field on skills is the trigger sentence used by the agent to decide whether to load the skill. Write it as "Use when …" — not as a general summary.

## Item types and locations

| Item                 | Path                             | Required frontmatter                            |
| -------------------- | -------------------------------- | ----------------------------------------------- |
| Claude skill         | `.claude/skills/<name>/SKILL.md` | `name`, `description`                           |
| Claude slash command | `.claude/commands/<name>.md`     | `description`, `allowed-tools`, `argument-hint` |
| Claude subagent      | `.claude/agents/<name>.md`       | `name`, `description`, `tools`, `model`         |
| Antigravity skill    | `.agent/skills/<name>/SKILL.md`  | `name`, `description`                           |

## Validation

There is no CI. Validation means: **does the CLI load it without complaint?** After adding or editing an item, manually verify it appears in the target CLI's command/skill list.

## Global availability

Items inside `.claude/` auto-load when a Claude Code session runs with this repo as cwd. Items inside `.agent/` auto-load when an Antigravity session runs with this repo as cwd. For global availability across any working directory, symlink into the user-level config dir:

```bash
# Claude Code
ln -s "$PWD/.claude/skills/<name>"           ~/.claude/skills/<name>
ln -s "$PWD/.claude/commands/<name>.md"      ~/.claude/commands/<name>.md
ln -s "$PWD/.claude/agents/<name>.md"        ~/.claude/agents/<name>.md

# Antigravity
ln -s "$PWD/.agent/skills/<name>"            ~/.gemini/config/skills/<name>
```

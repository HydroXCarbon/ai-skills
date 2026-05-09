# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Personal vault of customizations for Claude Code and Gemini CLI — skills, slash commands, subagents, and extensions. **There is no build, test, or lint step.** Everything is markdown / TOML / JSON config consumed by the two CLIs.

The repo uses dotfile dirs (`.claude/`, `.gemini/`) so items auto-load when a session's cwd is this repo (project-level discovery). For global availability, symlink items into `~/.claude/` or `~/.gemini/` (see README.md for the source→target table).

When adding or editing items, the only "verification" is that the file format matches the conventions below — the CLI itself is the runtime.

## Layout and authoring conventions

Five item types live here. Each has a strict format; future-you should match an existing example before inventing structure.

| Item | Path | Format |
| --- | --- | --- |
| Claude skill | `.claude/skills/<name>/SKILL.md` (folder) | Markdown + YAML frontmatter: `name`, `description` |
| Claude slash command | `.claude/commands/<name>.md` (single file) | Markdown + frontmatter: `description`, `allowed-tools`, `argument-hint`; body uses `$ARGUMENTS` |
| Claude subagent | `.claude/agents/<name>.md` (single file) | Markdown + frontmatter: `name`, `description`, `tools`, `model` |
| Gemini command | `.gemini/commands/<name>.toml` | TOML with `description` and `prompt` keys; body uses `{{args}}` |
| Gemini extension | `.gemini/extensions/<name>/` (folder) | Must contain `gemini-extension.json`; may add `GEMINI.md` and `commands/*.toml` |

Canonical references for each format live in `template` files (`.claude/commands/template.md`, `.claude/agents/template.md`, `.claude/skills/template/SKILL.md`, `.gemini/commands/template.toml`). **Do not symlink the templates** — copy them as starting points for new items.

## Critical distinctions to keep straight

- **Skill vs. command**: A skill is a multi-step capability auto-loaded by Claude when its `description` matches user intent — write the description as a trigger sentence ("Use when …"). A command is a single named prompt the user explicitly invokes as `/<name>`.
- **Skill description is the matcher**: the frontmatter `description` is what Claude reads to decide whether to load a skill. The body should describe *what to do once loaded*, not repeat trigger conditions.
- **Agent `tools` field is an allowlist**: subagents only get the tools listed there. Bash permissions can be scoped (e.g. `Bash(git status:*)`) — the same pattern works in command `allowed-tools`.
- **Argument placeholders differ between CLIs**: Claude commands use `$ARGUMENTS`, Gemini commands use `{{args}}`. Don't cross-pollinate.
- **Mirror layouts when an item exists for both CLIs**: if a concept is implemented as both a Claude command and a Gemini command, keep names aligned (`claude/commands/foo.md` ↔ `gemini/commands/foo.toml`).

## Common operations

Items in `.claude/` and `.gemini/` auto-load whenever a CLI session runs with this repo as cwd (project-level discovery). For global availability across any cwd, symlink into the user-level config dir:

```bash
ln -s "$PWD/.claude/commands/<name>.md"      ~/.claude/commands/<name>.md
ln -s "$PWD/.claude/skills/<name>"           ~/.claude/skills/<name>
ln -s "$PWD/.claude/agents/<name>.md"        ~/.claude/agents/<name>.md
ln -s "$PWD/.gemini/commands/<name>.toml"    ~/.gemini/commands/<name>.toml
ln -s "$PWD/.gemini/extensions/<name>"       ~/.gemini/extensions/<name>
```

There are no package scripts, no test runner, and no CI. Validation is "does the CLI load it without complaint."

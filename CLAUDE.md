# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Personal vault of customizations for Claude Code and Antigravity — skills, slash commands, subagents, and Antigravity skills. **There is no build, test, or lint step.** Everything is Markdown / JSON config consumed by the CLIs.

The repo uses dotfile dirs (`.claude/`, `.agent/`) so items auto-load when a session's cwd is this repo (project-level discovery). For global availability, symlink items into `~/.claude/` or the Antigravity config dir (see README.md for the source→target table).

When adding or editing items, the only "verification" is that the file format matches the conventions below — the CLI itself is the runtime.

## Layout and authoring conventions

Four item types live here. Each has a strict format; future-you should match an existing example before inventing structure.

| Item                 | Path                             | Required frontmatter                            |
| -------------------- | -------------------------------- | ----------------------------------------------- |
| Claude skill         | `.claude/skills/<name>/SKILL.md` | `name`, `description`                           |
| Claude slash command | `.claude/commands/<name>.md`     | `description`, `allowed-tools`, `argument-hint` |
| Claude subagent      | `.claude/agents/<name>.md`       | `name`, `description`, `tools`, `model`         |
| Antigravity skill    | `.agent/skills/<name>/SKILL.md`  | `name`, `description`                           |

Canonical references for each format live in `template` files (`.claude/commands/template.md`, `.claude/agents/template.md`, `.claude/skills/template/SKILL.md`). **Do not symlink the templates** — copy them as starting points for new items.

## Critical distinctions to keep straight

- **Skill vs. command**: A skill is a multi-step capability auto-loaded by the CLI when its `description` matches user intent — write the description as a trigger sentence ("Use when …"). A command is a single named prompt the user explicitly invokes as `/<name>`.
- **Skill description is the matcher**: the frontmatter `description` is what the agent reads to decide whether to load a skill. The body should describe *what to do once loaded*, not repeat trigger conditions.
- **Agent `tools` field is an allowlist**: subagents only get the tools listed there. Bash permissions can be scoped (e.g. `Bash(git status:*)`) — the same pattern works in command `allowed-tools`.
- **Claude commands use `$ARGUMENTS`**: do not use other placeholder styles in Claude command bodies.
- **Skills live in the right folder**: Claude skills go in `.claude/skills/`; Antigravity skills go in `.agent/skills/`. Do not mix them.

## Common operations

Items in `.claude/` auto-load whenever a Claude Code session runs with this repo as cwd. Items in `.agent/` auto-load when an Antigravity session runs with this repo as cwd. For global availability across any cwd, symlink into the user-level config dir:

```bash
# Claude Code
ln -s "$PWD/.claude/commands/<name>.md"      ~/.claude/commands/<name>.md
ln -s "$PWD/.claude/skills/<name>"           ~/.claude/skills/<name>
ln -s "$PWD/.claude/agents/<name>.md"        ~/.claude/agents/<name>.md

# Antigravity
ln -s "$PWD/.agent/skills/<name>"            ~/.gemini/config/skills/<name>
```

There are no package scripts, no test runner, and no CI. Validation is "does the CLI load it without complaint."

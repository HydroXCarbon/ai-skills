---
description: Overwrite global Claude config (~/.claude) with this repo's skills, agents (01 + 04 only), and the plugins/MCP listed in INTEGRATIONS.md
allowed-tools: Bash, Read, Glob
argument-hint: "[--dry-run]"
---

Sync this repo into the user-level Claude Code config. Overwrite whatever is
already there. `$ARGUMENTS` containing `--dry-run` means: print the commands
you would run, execute nothing.

Repo root: `/Users/purinpongpanich/Desktop/Projects/ai-skills` (if missing,
use the directory containing `.claude/INTEGRATIONS.md`). Target: `~/.claude`.

## 1. Skills — overwrite all

For every folder in `<repo>/.claude/skills/` except `template`:

```bash
ln -sfn "<repo>/.claude/skills/<name>" ~/.claude/skills/<name>
```

Do not touch skills in `~/.claude/skills/` that are not in this repo.

## 2. Agents — only 01 and 04

1. Remove existing symlinks in `~/.claude/agents/` that point into
   `<repo>/.claude/agents/` (clears stale links from earlier runs).
2. For every `*.md` in `<repo>/.claude/agents/01-core-development/` and
   `<repo>/.claude/agents/04-quality-security/`, except `README.md`:

```bash
ln -sfn "<repo>/.claude/agents/<category>/<file>.md" ~/.claude/agents/<file>.md
```

Do not link any other category, and never link `template.md`.

## 3. Plugins and MCP — from `.claude/INTEGRATIONS.md`

Read the "Install commands" and "MCP servers" sections of
`<repo>/.claude/INTEGRATIONS.md` and treat them as the source of truth. For
each plugin, add its marketplace first, then install it. Re-install even if
already installed, so the latest version is pulled. Currently:

- `skill-creator`, `frontend-design`, `code-simplifier` (claude-plugins-official)
- `bm` (buildomator)
- `context-mode`
- `claude-mem`
- MCP `context7` (user scope)

Use the `claude plugin ...` / `claude mcp ...` CLI equivalents of the slash
commands. If a command fails (e.g. SSH "Host key verification failed" on a
third-party marketplace), report it and continue with the rest.

## 4. Report

Finish with a short summary: skills linked, agents linked (count per
category), plugins installed vs. failed, then tell the user to run
`/reload-plugins` or restart Claude Code. Do not edit any file in the repo.
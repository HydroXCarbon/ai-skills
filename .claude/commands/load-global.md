---
description: Overwrite global Claude config (~/.claude) with this repo's skills, agents (01 + 04 only), settings.local.json, and any missing plugins/MCP listed in INTEGRATIONS.md
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

## 3. Settings — overwrite

Copy (not symlink, so approvals Claude Code writes later don't edit the repo):

```bash
cp -f "<repo>/.claude/settings.local.json" ~/.claude/settings.json
```

Overwrite without prompting. Skip with a note if the repo file is missing.

## 4. Plugins and MCP — only what is missing

Read the "Install commands" and "MCP servers" sections of
`<repo>/.claude/INTEGRATIONS.md` and treat them as the source of truth.
Installing is slow, so check first and **skip anything already present**:

```bash
claude plugin list      # installed plugins (match on name@marketplace)
claude plugin marketplace list
claude mcp list         # configured MCP servers
```

- Plugin already listed → skip it (and skip its marketplace add). Do not
  reinstall or update.
- Plugin missing → add its marketplace if not listed, then install it.
- MCP server already listed → skip; otherwise add it.

Run the check once up front, not per item. Currently expected:

- `skill-creator`, `frontend-design`, `code-simplifier` (claude-plugins-official)
- `bm` (buildomator)
- `context-mode`
- `claude-mem`
- MCP `context7` (user scope)

Use the `claude plugin ...` / `claude mcp ...` CLI equivalents of the slash
commands. If a command fails (e.g. SSH "Host key verification failed" on a
third-party marketplace), report it and continue with the rest.

## 5. Report

Finish with a short summary: skills linked, agents linked (count per
category), settings copied, plugins installed / skipped (already present) / failed, then tell the user to run
`/reload-plugins` or restart Claude Code. Do not edit any file in the repo.
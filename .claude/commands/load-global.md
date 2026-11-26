---
description: Overwrite global Claude config (~/.claude) with this repo's skills, agents (01 + 04 only), settings.local.json (merged, keeps env/API key), and any missing plugins/MCP listed in INTEGRATIONS.md
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

## 3. Settings — merge, never hard copy

Do NOT `cp` over `~/.claude/settings.json`: it holds machine-local keys that
are not in the repo (`env` with `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL`,
`model`, etc.) and a copy would delete them. Instead deep-merge the repo file
on top of the existing one, so repo keys win and every other key is kept
(not a symlink either, so approvals Claude Code writes later don't edit the
repo):

```bash
[ -f ~/.claude/settings.json ] || echo '{}' > ~/.claude/settings.json
cp ~/.claude/settings.json ~/.claude/settings.json.bak
jq -s '.[0] * .[1]' ~/.claude/settings.json "<repo>/.claude/settings.local.json" \
  > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
```

Notes:
- Objects merge recursively; arrays (e.g. `permissions.allow`) are replaced
  by the repo's version.
- Never print `env` values in the report.
- Skip with a note if the repo file is missing or `jq` is unavailable.

## 4. Plugins and MCP — only what is missing

Read the "Install commands" section of
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
- Plugin listed but `Status: ✘ disabled` → enable it with
  `claude plugin enable <name>@<marketplace>`. Applies to every plugin in the
  expected list below, including ones that were already installed.

Run the check once up front, not per item. Currently expected:

- `skill-creator`, `frontend-design`, `code-simplifier`, `context7` (claude-plugins-official)
- `bm` (buildomator)
- `context-mode`
- `claude-mem`

Use the `claude plugin ...` / `claude mcp ...` CLI equivalents of the slash
commands. If a command fails (e.g. SSH "Host key verification failed" on a
third-party marketplace), report it and continue with the rest.

## 5. Report

Finish with a short summary: skills linked, agents linked (count per
category), settings merged, plugins installed / enabled / skipped (already present and enabled) / failed, then tell the user to run
`/reload-plugins` or restart Claude Code. Do not edit any file in the repo.
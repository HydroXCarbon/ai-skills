# ai-skills

Personal vault for Claude Code and Gemini CLI customizations — skills,
slash commands, subagents, and extensions. Versioned so they can be
synced across machines and shared.

## Layout

```
ai-skills/
├── claude/
│   ├── skills/        # Claude Code skills (folder per skill, contains SKILL.md)
│   ├── commands/      # Slash commands (.md with YAML frontmatter)
│   └── agents/        # Subagent definitions (.md with frontmatter)
└── gemini/
    ├── commands/      # Gemini CLI commands (.toml)
    └── extensions/    # Gemini extensions (folder per extension)
```

## Install (symlink into your CLI config)

Symlink an item from this repo into the CLI's config dir so edits here
propagate live.

| Source (this repo)                       | Target                                |
| ---------------------------------------- | ------------------------------------- |
| `claude/skills/<name>/`                  | `~/.claude/skills/<name>`             |
| `claude/commands/<name>.md`              | `~/.claude/commands/<name>.md`        |
| `claude/agents/<name>.md`                | `~/.claude/agents/<name>.md`          |
| `gemini/commands/<name>.toml`            | `~/.gemini/commands/<name>.toml`      |
| `gemini/extensions/<name>/`              | `~/.gemini/extensions/<name>`         |

Example:

```bash
ln -s "$PWD/claude/commands/example.md" ~/.claude/commands/example.md
```

## What goes where

- **Claude skill** — multi-step capability with its own folder and
  `SKILL.md`. Loaded on demand by Claude when its description matches.
- **Claude command** — single `.md` file invoked as `/<name>`. Use for
  reusable prompts.
- **Claude agent** — subagent system prompt + tool allowlist. Invoked
  from the Agent tool by `subagent_type`.
- **Gemini command** — single `.toml` invoked as `/<name>` in Gemini CLI.
- **Gemini extension** — folder bundling commands, MCP config, and a
  `GEMINI.md`.

## Templates

Each folder has one `example-*` template you can copy as a starting
point. Don't symlink the examples — use them as references.

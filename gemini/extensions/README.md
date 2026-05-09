# Gemini Extensions

Each subfolder is one extension. Minimum contents:

```
my-extension/
├── gemini-extension.json   # required: name, version, mcpServers, contextFileName, etc.
├── GEMINI.md               # optional: extension-scoped instructions
└── commands/               # optional: extension-scoped /commands as .toml
    └── foo.toml
```

Install by symlink:

```bash
ln -s "$PWD/my-extension" ~/.gemini/extensions/my-extension
```

Reference: https://github.com/google-gemini/gemini-cli — see the
`docs/extensions.md` in that repo for the current schema.

No extensions in this repo yet — drop the first one alongside this
README.

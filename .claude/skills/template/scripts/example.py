"""Example skill script.

Skills can call helper scripts from their SKILL.md body — typically
via `Bash` listed in `allowed-tools`. Reference the script by relative
path: `[scripts/example.py](scripts/example.py)`.

Default language is Python. /create-skills asks before using anything
else; if you do switch, replace this whole file with the equivalent
stub for the chosen language.

Replace this docstring and the `main()` body with the real logic.
"""

from __future__ import annotations

import sys


def main(argv: list[str]) -> int:
    """Skill entry point. Replace with the real implementation."""
    print("TODO: implement skill script")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
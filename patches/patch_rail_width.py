#!/usr/bin/env python3
"""Widen the collapsed sidebar rail from 56px to 68px.

The collapsed rail width is hardcoded in `dsh-client-ui-layout`'s
`computeColumns`. With the theme's 10px margins, a 56px track leaves only a
36px rail; this bump makes the rail 48px wide.

Usage:
    python3 patch_rail_width.py [path/to/@deepseek-ai]

If the path is omitted, the script locates the newest `@deepseek-ai` directory
under `~/.npm/_npx/*/node_modules/`.
"""
import os
import sys
from pathlib import Path

LAYOUT_REL = "dsh-client-ui-layout/lib/client.js"
OLD = "sidebar === 0 ? 56 :"
NEW = "sidebar === 0 ? 68 :"


def resolve_root(argv):
    if len(argv) > 1:
        return Path(argv[1]).expanduser()
    base = Path(os.path.expanduser("~/.npm/_npx"))
    if base.exists():
        candidates = sorted(
            base.glob("*/node_modules/@deepseek-ai"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for cand in candidates:
            if (cand / LAYOUT_REL).exists():
                return cand
    raise SystemExit(
        "Could not locate @deepseek-ai. Pass its path as an argument, e.g.\n"
        "    python3 patch_rail_width.py ~/.npm/_npx/<hash>/node_modules/@deepseek-ai"
    )


def main():
    root = resolve_root(sys.argv)
    target = root / LAYOUT_REL
    s = target.read_text(encoding="utf-8")
    count = s.count(OLD)
    if count != 1:
        raise SystemExit(
            f"Expected exactly one occurrence of '{OLD}', found {count}. "
            "This patch was written for dsh 0.1.0-rc.7."
        )
    target.write_text(s.replace(OLD, NEW, 1), encoding="utf-8")
    print(f"OK: {target}\n    {OLD.strip()}  ->  {NEW.strip()}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Restructure the sidebar stats card into a themed session-stats widget.

Replaces the plain-text stats block with a `dsh-stats` container, per-metric
rows, and a cache-hit progress bar. The colours, hierarchy and dots live in
`spotify-theme.css` (section 7); this script only changes the markup.

Usage:
    python3 patch_stats_card.py [path/to/@deepseek-ai]

If the path is omitted, the script locates the newest `@deepseek-ai` directory
under `~/.npm/_npx/*/node_modules/`.
"""
import os
import sys
from pathlib import Path

SIDEBAR_REL = "dsh-client-ui-sidebar/lib/client.js"


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
            if (cand / SIDEBAR_REL).exists():
                return cand
    raise SystemExit(
        "Could not locate @deepseek-ai. Pass its path as an argument, e.g.\n"
        "    python3 patch_stats_card.py ~/.npm/_npx/<hash>/node_modules/@deepseek-ai"
    )


NEW_BLOCK = (
    '(0, react_jsx_runtime.jsx)("div", {\n'
    '\t\t\t\t\t\tclassName: "dsh-stats",\n'
    '\t\t\t\t\t\tchildren: [wide && stats !== null ? (0, react_jsx_runtime.jsxs)(react_jsx_runtime.Fragment, { children: [\n'
    '\t\t\t\t\t\t\t(0, react_jsx_runtime.jsx)("div", { className: "dsh-stat dsh-stat-primary", children: `${stats.turns} 轮 · ${stats.steps} 步` }),\n'
    '\t\t\t\t\t\t\tstats.llmMs > 0 && (0, react_jsx_runtime.jsx)("div", { className: "dsh-stat", children: `LLM ${formatDuration(stats.llmMs)}` }),\n'
    '\t\t\t\t\t\t\tusage !== void 0 && usage !== null && (billedInputTokens(usage) > 0 || usage.outputTokens > 0) ? (0, react_jsx_runtime.jsx)("div", { className: "dsh-stat", children: `输入 ${formatTokens(billedInputTokens(usage))} · 输出 ${formatTokens(usage.outputTokens)}` }) : null,\n'
    '\t\t\t\t\t\t\tusage !== void 0 && usage !== null && cacheHitPercent(usage) !== null ? (0, react_jsx_runtime.jsxs)("div", { className: "dsh-cache", children: [\n'
    '\t\t\t\t\t\t\t\t(0, react_jsx_runtime.jsxs)("div", { className: "dsh-cache-label", children: ["缓存命中 ", (0, react_jsx_runtime.jsx)("strong", { children: `${cacheHitPercent(usage)}%` })] }),\n'
    '\t\t\t\t\t\t\t\t(0, react_jsx_runtime.jsx)("div", { className: "dsh-cache-bar", children: (0, react_jsx_runtime.jsx)("div", { className: "dsh-cache-fill", style: { width: `${cacheHitPercent(usage)}%` } }) })\n'
    '\t\t\t\t\t\t\t] }) : null\n'
    '\t\t\t\t\t\t] }) : null]\n'
    '\t\t\t\t\t}),'
)


def main():
    root = resolve_root(sys.argv)
    target = root / SIDEBAR_REL
    s = target.read_text(encoding="utf-8")

    anchor = s.find('padding: "8px 12px"')
    if anchor == -1:
        raise SystemExit(
            "Stats-card anchor not found. This patch was written for dsh 0.1.0-rc.7."
        )
    start = s.rfind('(0, react_jsx_runtime.jsx)("div", {', 0, anchor)
    foot = s.find("footArea", anchor)
    end = s.rfind("}),", anchor, foot) + len("}),")
    if start == -1 or end == -1:
        raise SystemExit("Could not bound the stats-card block.")

    old_block = s[start:end]
    if old_block not in s:
        raise SystemExit("Old block not found for replacement.")

    target.write_text(s.replace(old_block, NEW_BLOCK, 1), encoding="utf-8")
    print(f"OK: {target}\n    stats card restructured (dsh-stats + cache progress bar)")


if __name__ == "__main__":
    main()

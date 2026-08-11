#!/usr/bin/env python3
"""
Rewrite root-absolute href/src values ("/assets/...") to depth-correct relative
paths ("../assets/...").

Why: root-absolute paths only resolve when the site is served from a domain
root. Relative paths let the exact same files work locally, at a GitHub Pages
project URL (username.github.io/topreno/), and at the custom domain — which
means the deploy can be verified before DNS is cut over.

Only `href="..."` and `src="..."` are touched. Absolute production URLs in
canonical tags, Open Graph metadata, and JSON-LD are left alone on purpose.

Idempotent: values that are already relative are skipped, so re-running is safe.

Run from the repo root:  python3 tools/relativize.py
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Attribute values starting with a single "/" (not "//", which is protocol-relative)
PATTERN = re.compile(r'((?:href|src)=")/(?!/)([^"]*)"')


def prefix_for(depth):
    """'' at the root, '../' one level down, '../../' two levels down."""
    return "../" * depth


def relativize(html, depth):
    """Rewrite root-absolute href/src in `html` for a page nested `depth` dirs deep."""
    pre = prefix_for(depth)

    def sub(m):
        attr, path = m.group(1), m.group(2)
        # href="/" -> "./" at root, "../" below it
        if path == "":
            return f'{attr}{pre or "./"}"'
        return f'{attr}{pre}{path}"'

    return PATTERN.sub(sub, html)


def depth_of(rel_path):
    """Directory depth of a file relative to the site root."""
    return rel_path.count(os.sep)


def main():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "tools"}]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            with open(full, encoding="utf-8") as f:
                src = f.read()
            out = relativize(src, depth_of(rel))
            if out != src:
                with open(full, "w", encoding="utf-8") as f:
                    f.write(out)
                changed += 1
                print("rewrote", rel)
    print(f"\n{changed} file(s) updated." if changed else "\nNothing to do — already relative.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

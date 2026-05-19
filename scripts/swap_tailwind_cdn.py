#!/usr/bin/env python3
"""Replace the runtime Tailwind CDN with the prebuilt static stylesheet.

cdn.tailwindcss.com ships a large JS bundle that compiles CSS in the user's
browser on every visit — a render-blocking Core Web Vitals cost. We build the
exact CSS once (scripts: tailwind.config.js + `tailwindcss --minify`) and link
it instead. Idempotent: only acts where the CDN tag is still present.

Run:  python3 scripts/swap_tailwind_cdn.py
"""
import re
from pathlib import Path

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
CDN_TAG = '<script src="https://cdn.tailwindcss.com"></script>'
LINK_TAG = '<link rel="stylesheet" href="/assets/css/tailwind.css">'
DNS_PREFETCH_RE = re.compile(
    r'[ \t]*<link rel="dns-prefetch" href="https://cdn\.tailwindcss\.com">\n?'
)


def swap(path: Path) -> str:
    doc = path.read_text(encoding="utf-8")
    if CDN_TAG not in doc:
        return "unchanged"
    doc = doc.replace(CDN_TAG, LINK_TAG)
    doc = DNS_PREFETCH_RE.sub("", doc)  # no longer needed
    path.write_text(doc, encoding="utf-8")
    return "swapped"


if __name__ == "__main__":
    print("Swap Tailwind CDN -> static /assets/css/tailwind.css")
    for p in sorted(FRONTEND.glob("*.html")) + sorted(
        (FRONTEND / "examples").glob("*.html")
    ):
        print(f"  {p.name:24s} -> {swap(p)}")

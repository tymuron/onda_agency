#!/usr/bin/env python3
"""Reorder the homepage <main> sections into the research-backed order.

Buyers judge in ~10s, scan not read, and want proof of work + who you are
*before* the offer (NN/g, Orbit Media). So: hero -> value/proof band -> WORK
(high) -> the STUDIO/who -> packages -> who-it's-for -> add-ons -> FAQ ->
contact.

Keyed on the language-neutral `<!-- ===== NAME ===== -->` section comments, so
the same reorder applies identically to EN/ES/KA. Idempotent: if already in the
target order, the file is rewritten byte-identical (no-op).

Run:  python3 scripts/reorder_sections.py
"""
import re
from pathlib import Path

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
FILES = ["index_v5.html", "index_es.html", "index_ka.html"]

# Canonical order, by a stable substring of each section's comment marker.
ORDER = ["HERO", "METRICS", "PORTFOLIO", "TEAM", "PACKAGES", "BEST FIT",
         "ADD-ONS", "FAQ", "CONTACT"]

DIVIDER = '    <hr class="divider mx-auto max-w-lg">'
SECTION_RE = re.compile(r"<!--\s*=====\s*(.*?)\s*=====\s*-->")


def key_of(comment_label: str) -> str:
    u = comment_label.upper()
    for k in ORDER:
        if k in u:
            return k
    raise ValueError(f"Unrecognized section comment: {comment_label!r}")


def reorder(path: Path) -> str:
    doc = path.read_text(encoding="utf-8")
    m = re.search(r'(<main id="main-content">)(.*?)(</main>)', doc, re.DOTALL)
    if not m:
        return "skip (no main)"
    head, inner, tail = m.group(1), m.group(2), m.group(3)

    # Drop standalone divider lines; we re-insert them between units.
    inner_nohr = re.sub(
        r"\n?[ \t]*<hr class=\"divider mx-auto max-w-lg\">[ \t]*\n?", "\n", inner
    )

    # Split into units at each section comment boundary.
    marks = list(SECTION_RE.finditer(inner_nohr))
    if len(marks) != len(ORDER):
        return f"skip (found {len(marks)} sections, expected {len(ORDER)})"
    units = {}
    for i, mk in enumerate(marks):
        start = mk.start()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(inner_nohr)
        units[key_of(mk.group(1))] = inner_nohr[start:end].strip("\n")

    body = ("\n\n" + DIVIDER + "\n\n").join(units[k].strip() for k in ORDER)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    new_inner = "\n\n    " + body + "\n\n    "

    new_doc = doc[:m.start()] + head + new_inner + tail + doc[m.end():]
    if new_doc == doc:
        return "unchanged"
    path.write_text(new_doc, encoding="utf-8")
    return "reordered"


if __name__ == "__main__":
    print("Reorder homepage sections -> " + " > ".join(ORDER))
    for f in FILES:
        print(f"  {f:18s} -> {reorder(FRONTEND / f)}")

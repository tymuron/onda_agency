#!/usr/bin/env python3
"""Idempotent SEO/GEO + analytics patcher for the Onda static pages.

Safe to run repeatedly: each managed region is wrapped in sentinel comments and
fully replaced on re-run. Nothing else in the HTML is touched.

Phase 1 (this file): remove the no-cache meta tags, inject canonical +
hreflang + JSON-LD (@graph: Organization, WebSite, FAQPage, BreadcrumbList),
and a progressive-enhancement language-preference redirect on the homepages.

Phase 2 extends this with the analytics <script> tag (same sentinel pattern).

Run:  python3 scripts/site_patch.py
"""
from __future__ import annotations

import html as _html
import json
import re
from pathlib import Path

SITE_URL = "https://agencyonda.com"
# Any prior canonical domains to rewrite to SITE_URL (idempotent: SITE_URL
# never contains these). Covers pre-existing OG/Twitter/JSON-LD tags that the
# managed block does not own.
OLD_DOMAINS = ["ondaweb.es"]
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"

SEO_START = "<!-- onda-seo:start (managed by scripts/site_patch.py) -->"
SEO_END = "<!-- onda-seo:end -->"
ANALYTICS_START = "<!-- onda-analytics:start -->"
ANALYTICS_END = "<!-- onda-analytics:end -->"

# (filename, lang, page_type)
PAGES = [
    ("index_v5.html", "en", "home"),
    ("index_es.html", "es", "home"),
    ("portfolio.html", "en", "portfolio"),
    ("portfolio_es.html", "es", "portfolio"),
    ("process.html", "en", "process"),
    ("process_es.html", "es", "process"),
]

EXAMPLES = [
    "examples/aesthetic-clinic.html",
    "examples/architecture-studio.html",
    "examples/barbershop-before.html",
    "examples/barbershop.html",
    "examples/casa-serena.html",
    "examples/dental-clinic.html",
    "examples/real-estate.html",
    "examples/solo-entrepreneur.html",
]

ANALYTICS_TAG = '<script defer src="/assets/js/analytics.js"></script>'
LEAD_LINE = "document.dispatchEvent(new CustomEvent('onda:lead'));"

# URL for a (page_type, lang). 'home'/'en' is the canonical site root.
LOCALE_FILE = {
    ("home", "en"): "/",
    ("home", "es"): "/index_es.html",
    ("portfolio", "en"): "/portfolio.html",
    ("portfolio", "es"): "/portfolio_es.html",
    ("process", "en"): "/process.html",
    ("process", "es"): "/process_es.html",
}

BREADCRUMB_NAME = {
    ("portfolio", "en"): "Portfolio",
    ("portfolio", "es"): "Portfolio",
    ("process", "en"): "Process",
    ("process", "es"): "Proceso",
}
HOME_NAME = {"en": "Home", "es": "Inicio"}


def abs_url(rel: str) -> str:
    return SITE_URL if rel == "/" else SITE_URL + rel


def strip_tags(s: str) -> str:
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse_faq(doc: str):
    """Pull (question, answer) pairs straight from the visible FAQ accordion so
    the FAQPage schema always matches on-page content (a Google requirement)."""
    pattern = re.compile(
        r'<button class="faq-trigger"[^>]*>\s*<span>(.*?)</span>.*?'
        r'<div class="faq-body">\s*<p[^>]*>(.*?)</p>',
        re.DOTALL,
    )
    out = []
    for q, a in pattern.findall(doc):
        q, a = strip_tags(q), strip_tags(a)
        if q and a:
            out.append((q, a))
    return out


def hreflang_links(page_type: str) -> str:
    langs = ["en", "es"]
    lines = []
    for lg in langs:
        href = abs_url(LOCALE_FILE[(page_type, lg)])
        lines.append(f'<link rel="alternate" hreflang="{lg}" href="{href}">')
    lines.append(
        f'<link rel="alternate" hreflang="x-default" '
        f'href="{abs_url(LOCALE_FILE[(page_type, "en")])}">'
    )
    return "\n    ".join(lines)


def json_ld(page_type: str, lang: str, doc: str) -> str:
    org = {
        "@type": "Organization",
        "@id": f"{SITE_URL}/#org",
        "name": "Onda",
        "url": SITE_URL,
        "logo": f"{SITE_URL}/logo.png",
        "image": f"{SITE_URL}/og-image.png",
        "founder": {"@type": "Person", "name": "Tymur Chystiakov"},
        "areaServed": ["Spain", "Europe", "United Kingdom"],
        "knowsLanguage": ["en", "es"],
        "slogan": "Fast premium websites for service businesses.",
    }
    website = {
        "@type": "WebSite",
        "@id": f"{SITE_URL}/#website",
        "url": SITE_URL,
        "name": "Onda",
        "inLanguage": lang,
        "publisher": {"@id": f"{SITE_URL}/#org"},
    }
    graph = [org, website]

    if page_type == "home":
        faq = parse_faq(doc)
        if faq:
            graph.append({
                "@type": "FAQPage",
                "@id": f"{abs_url(LOCALE_FILE[(page_type, lang)])}#faq",
                "inLanguage": lang,
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in faq
                ],
            })
    else:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": HOME_NAME[lang],
                    "item": abs_url(LOCALE_FILE[("home", lang)]),
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": BREADCRUMB_NAME[(page_type, lang)],
                    "item": abs_url(LOCALE_FILE[(page_type, lang)]),
                },
            ],
        })

    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, ensure_ascii=False, indent=2)


def lang_redirect_script(lang: str) -> str:
    """Returning visitors who previously picked a language are sent there.
    No-JS clients and crawlers get the served content (good for SEO)."""
    targets = {"en": "/", "es": "/index_es.html"}
    js_map = json.dumps(targets)
    return (
        "<script>(function(){try{var o=localStorage.getItem('onda_lang_override');"
        f"var c={json.dumps(lang)};var m={js_map};"
        "if(o&&m[o]&&o!==c){location.replace(m[o]);}}catch(e){}})();</script>"
    )


def build_seo_block(filename: str, page_type: str, lang: str, doc: str) -> str:
    canonical = abs_url(LOCALE_FILE[(page_type, lang)])
    parts = [
        SEO_START,
        f'<link rel="canonical" href="{canonical}">',
        hreflang_links(page_type),
        f'<script type="application/ld+json">\n{json_ld(page_type, lang, doc)}\n    </script>',
    ]
    if page_type == "home":
        parts.append(lang_redirect_script(lang))
    parts.append(SEO_END)
    return "\n    ".join(parts)


def remove_nocache_meta(doc: str) -> str:
    return re.sub(
        r'[ \t]*<meta http-equiv="(?:Cache-Control|Pragma|Expires)"[^>]*>\n?',
        "",
        doc,
    )


def upsert_region(doc: str, start: str, end: str, block: str, anchor: str) -> str:
    region = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if region.search(doc):
        return region.sub(lambda _m: block, doc)
    return doc.replace(anchor, "    " + block + "\n" + anchor, 1)


def inject_analytics(doc: str) -> str:
    block = ANALYTICS_START + "\n    " + ANALYTICS_TAG + "\n    " + ANALYTICS_END
    return upsert_region(doc, ANALYTICS_START, ANALYTICS_END, block, "</body>")


def inject_lead_event(doc: str) -> str:
    """Add ONE additive line in the existing contact-form success branch so
    analytics can observe leads without touching fetch/validation/reset."""
    if LEAD_LINE in doc:
        return doc
    # insert right after the `if (response.ok) {` line, matching its indent
    m = re.search(r"\n([ \t]*)if \(response\.ok\) \{[ \t]*\n", doc)
    if not m:
        return doc
    indent = m.group(1) + "    "
    insert_at = m.end()
    return doc[:insert_at] + f"{indent}{LEAD_LINE}\n" + doc[insert_at:]


def rewrite_domain(doc: str) -> str:
    """Repoint any prior canonical domain to SITE_URL across the whole doc
    (pre-existing OG/Twitter/legacy-JSON-LD tags the managed block doesn't own).
    Idempotent: SITE_URL contains none of OLD_DOMAINS."""
    host = SITE_URL.split("//", 1)[1]
    for od in OLD_DOMAINS:
        doc = doc.replace("https://" + od, SITE_URL).replace("http://" + od, SITE_URL)
        doc = doc.replace(od, host)
    return doc


def patch_file(filename: str, lang: str, page_type: str) -> str:
    path = FRONTEND / filename
    doc = path.read_text(encoding="utf-8")
    original = doc

    doc = rewrite_domain(doc)
    doc = remove_nocache_meta(doc)
    block = build_seo_block(filename, page_type, lang, doc)
    doc = upsert_region(doc, SEO_START, SEO_END, block, "</head>")
    doc = inject_analytics(doc)
    if page_type == "home":
        doc = inject_lead_event(doc)

    if doc != original:
        path.write_text(doc, encoding="utf-8")
        return "patched"
    return "unchanged"


def patch_example(relpath: str) -> str:
    path = FRONTEND / relpath
    doc = path.read_text(encoding="utf-8")
    new = inject_analytics(rewrite_domain(doc))
    if new != doc:
        path.write_text(new, encoding="utf-8")
        return "patched"
    return "unchanged"


def main():
    for filename, lang, page_type in PAGES:
        status = patch_file(filename, lang, page_type)
        print(f"  {filename:28s} [{lang}/{page_type}] -> {status}")
    for relpath in EXAMPLES:
        status = patch_example(relpath)
        print(f"  {relpath:28s} [analytics]   -> {status}")
    # Retired loader stub: domain rewrite only.
    stub = FRONTEND / "index.html"
    if stub.exists():
        d = stub.read_text(encoding="utf-8")
        nd = rewrite_domain(d)
        if nd != d:
            stub.write_text(nd, encoding="utf-8")
        print(f"  {'index.html':28s} [domain]      -> "
              f"{'patched' if nd != d else 'unchanged'}")


if __name__ == "__main__":
    print("SEO/GEO + analytics patch:")
    main()

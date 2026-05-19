# Technical SEO & Indexing (2024–2026)

Contents: 1 robots.txt · 2 meta robots/X-Robots · 3 rendering/JS · 4 soft 404s
· 5 redirects · 6 canonicalization · 7 international/hreflang · 8 sitemaps ·
9 architecture/internal links · 10 Core Web Vitals · 11 HTTPS/mobile/schema.

## 1. Crawling: robots.txt
Controls **crawling, not indexing** — a disallowed URL can still be indexed
(URL-only) if linked. Use it to block low-value crawl paths (faceted/parameter
URLs, internal search, cart, staging). **Never** disallow a page you also want
de-indexed — Googlebot then never sees the `noindex`, so it can persist. Specs:
max **500 KiB** parsed; root only; `*`/`$` wildcards; `crawl-delay` **ignored by
Google**; on conflict Google applies the **least-restrictive / longest-path**
rule. Persistent 5xx ⇒ Google treats as "disallow all" — keep it 200/404. Add
absolute `Sitemap:` directive(s).

## 2. Indexing controls: meta robots / X-Robots-Tag
De-index via `<meta name="robots" content="noindex">` or `X-Robots-Tag` header
(header for non-HTML). Page must be crawlable for `noindex` to work. Conflicts ⇒
most restrictive wins. 2024–2026: `nosnippet`/`max-snippet:0`/
`max-image-preview:none` also **exclude content from Google AI Overviews & AI
Mode** — blocking snippets costs AI visibility. `data-nosnippet` only on
span/div/section.

## 3. Rendering / JS SEO
Googlebot = evergreen Chromium WRS: crawl → render queue → index. Only **HTTP
200** pages enter the render queue. (a) **Client-side redirects are the worst
option** — use server **301/308**; JS `location` redirects are unreliable.
(b) **SSR / static / hydration ≫ CSR**; dynamic rendering is deprecated.
(c) History API routing, never `#` fragments. (d) SPA "not found" must return
real 404/410 or `noindex` (else soft 404). (e) Static HTML is ideal — keep
title/meta/canonical/hreflang/schema in server HTML, not JS-injected.

## 4. Soft 404s & HTTP status
Soft 404 = empty/"not found" page returning 200 — wastes crawl budget, won't
index. Return real **404 or 410** (410 = strong drop signal) for dead URLs.
Check Search Console → Page indexing.

## 5. Redirects
Permanent → **301 or 308** (identical to Google; pass canonical signals).
302/307 = temporary. Server-side > instant meta-refresh > JS (avoid). Keep ≥1
year. **Avoid chains** — Googlebot follows ~5 hops; target ≤1–2. Point internal
links/canonical/sitemap at final URLs. Force one host + HTTPS via 301.

## 6. Canonicalization & duplicates
`rel="canonical"` is a **hint, not a directive**. Signal strength:
**301/308 > rel=canonical ≈ internal links > HTTPS > sitemap (weak)**. Exactly
one canonical, absolute URL, in `<head>`/header, **self-referential** on every
indexable page, → a 200 indexable URL. Keep canonical + internal links +
sitemap consistent. Duplicate content is **not a penalty** — Google clusters
and picks one. Parameters: canonical to clean URL and/or robots-block traps.

## 7. International / multilingual (hreflang)
Tells Google which language/region variant to serve. Codes = ISO 639-1 language
+ optional ISO 3166-1 Alpha-2 region (`en`, `es`, `ka`, `en-GB`; never
region-only, never `UK`/`EU`). **Bidirectional return links mandatory** (X→Y
needs Y→X). Every page lists **itself + all alternates**. One **`x-default`**
(fallback/selector). Absolute URLs. Implement via `<link rel="alternate">`,
HTTP header, **or XML sitemap** (`xmlns:xhtml`) — sitemap method scales best and
is least error-prone. **Subfolders** (`/en/ /es/`) consolidate authority for a
single gTLD; ccTLDs only for country targeting. 30–65% of multilingual sites
have hreflang errors (missing return/self links, wrong codes) — validate.

## 8. Sitemaps
≤50,000 URLs and ≤50 MB uncompressed per file (index files for more). Only
canonical, indexable, 200 URLs. UTF-8, absolute. `<lastmod>` honored only if
accurate; `<priority>`/`<changefreq>` **ignored**. Submit via Search Console +
robots `Sitemap:`. hreflang `<xhtml:link>` alternates do **not** count toward
the 50k limit.

## 9. Site architecture & internal linking
Important pages ≤3 clicks from home. Flat, lowercase, hyphenated, stable URLs.
Every indexable page needs ≥1 internal link (no orphans). Descriptive anchors;
link language equivalents. Hub→spoke structure aids crawl prioritization. (See
also offpage-links-entity.md §6 — internal linking is a major equity lever;
~66% of pages have only one internal link.)

## 10. Core Web Vitals (2024–2026)
Confirmed ranking contributor/tiebreaker; uses **field data (CrUX/Search
Console)**, **75th percentile**, mobile+desktop, all three:
- **LCP ≤ 2.5 s** (TTFB ≈40%, load delay <10%, load duration ≈40%, render
  delay <10%).
- **INP ≤ 200 ms** — **replaced FID 12 Mar 2024**; Lighthouse uses TBT proxy.
- **CLS ≤ 0.1**.
Fixes: remove render-blocking JS/CSS (defer/async, inline critical CSS); LCP
image gets `fetchpriority="high"`, never `loading="lazy"`; serve WebP/AVIF
sized via CDN; `font-display:swap` + preload; set width/height on media (CLS);
break long tasks (`scheduler.yield()`, web workers). **Avoid the Tailwind Play
CDN (`cdn.tailwindcss.com`) in production** — ships large JS and JIT-compiles
CSS in the browser, inflating LCP/INP and blocking render; precompile to static
CSS via Tailwind CLI/PostCSS. Avoid runtime CSS-in-JS and heavy third-party JS.
0.1 s faster ≈ +8% conversions (see measurement-updates-cro.md).

## 11. HTTPS, mobile-first, structured data
HTTPS = light ranking signal + canonical tiebreaker; enforce site-wide via 301,
valid cert, no mixed content. **Mobile-first indexing 100% complete (5 Jul
2024)** — Google indexes the *mobile* render only; content/links/structured
data must be equivalent and fast on mobile. **JSON-LD** in head/body, must match
visible content; eligibility ≠ guaranteed rich result; doesn't directly boost
rank but earns SERP features. For local/services: `Organization`/`LocalBusiness`
+ `WebSite`; validate with Rich Results Test + URL Inspection.

## Sources
1. developers.google.com/search/docs/crawling-indexing/robots-meta-tag — robots/X-Robots spec, AI Overviews impact.
2. .../crawling-indexing/block-indexing — noindex implementation.
3. .../crawling-indexing/robots/intro — crawl vs index.
4. developers.google.com/search/blog/2025/03/robots-refresher-page-level — 2025 page-level robots refresher.
5. developers.google.com/crawling/docs/robots-txt/robots-txt-spec — 500 KiB, wildcards, precedence, crawl-delay unsupported.
6. .../large-site-managing-crawl-budget — crawl budget thresholds/waste/fixes (Dec 2025).
7. .../crawling-indexing/canonicalization — signals, hint-not-rule, duplicates.
8. .../consolidate-duplicate-urls — rel=canonical methods/rules.
9. .../javascript/javascript-seo-basics — 3-phase render, 200-only queue, History API, SPA soft 404.
10. .../javascript/dynamic-rendering — dynamic rendering deprecated.
11. .../crawling-indexing/301-redirects — redirect types, server vs JS, canonical behavior.
12. .../specialty/international/localized-versions — hreflang methods, codes, return/self, x-default, errors.
13. developers.google.com/search/blog/2013/04/x-default-hreflang — x-default definition.
14. .../sitemaps/build-sitemap — 50k/50MB, lastmod, priority/changefreq ignored.
15. web.dev/articles/vitals — CWV thresholds, 75th pct, field vs lab.
16. web.dev/blog/inp-cwv-march-12 — INP replaced FID 12 Mar 2024.
17. developers.google.com/search/blog/2023/05/introducing-inp — INP rationale.
18. web.dev/articles/optimize-lcp — LCP subparts, fetchpriority, no-lazy.
19. web.dev/articles/optimize-inp — INP fixes (yield, workers).
20. web.dev/articles/optimize-long-tasks — long-task breakup.
21. web.dev/articles/fetch-priority — fetchpriority for LCP (2.6→1.9 s).
22. developers.google.com/search/docs/appearance/core-web-vitals — CWV in ranking, field data.
23. developers.google.com/search/blog/2024/06/mobile-indexing — mobile-first complete 5 Jul 2024.
24. .../structured-data/sd-policies — must match visible content.
25. .../intro-structured-data — JSON-LD recommended, validation.
26. aleydasolis.com — ccTLD vs subdirectory; 6-step hreflang process.
27. searchengineland.com/google-core-web-vitals-...-march-12-437072 — INP date.
28. searchenginejournal.com/google-removes-javascript-seo-warning — current JS guidance.
29. searchenginejournal.com/google-soft-404s-use-crawl-budget — soft 404 cost.
30. seroundtable.com/google-sitemap-50000-limit...33843 — xhtml alternates not counted.
31. v3.tailwindcss.com/docs/optimizing-for-production + tailwind issue 18731 — CDN is dev-only (CWV cost).

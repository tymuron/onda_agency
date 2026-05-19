# Local SEO (2024–2026), with Spain/EU specifics

Reusable both to rank a local business itself and to advise SMB clients.
Contents: 1 model · 2 factor weights · 3 GBP · 4 reviews · 5 citations/NAP ·
6 location pages · 7 schema · 8 local links · 9 Spain/EU · 10 local + AI.

## 1. Model (Google's framing)
**Relevance** (categories, services, site keywords, reviews) ·
**Distance** (proximity to searcher — fixed) · **Prominence** (links, reviews,
citations, web mentions). You cannot pay for local ranking; spam (keyword-
stuffed names, fake addresses) gets suspended.

## 2. Ranking-factor weights (Whitespark/BrightLocal 2026)
**Local Pack:** GBP signals 32% · Reviews 20% (rising) · On-page 15% ·
Behavioral 9% · Links 8% · Citations 6% · Social 5%.
**Local Organic:** On-page 33% · Links 24% · Behavioral 10% · Personalization
8% · GBP 7% · Citations 7% · Social 4%.
**AI visibility:** On-page 24% · Reviews 16% · Citations 13% · Links 13% ·
GBP 12% · Personalization 9% · Social 9% (citations matter more for AI).
Top pack factors: primary GBP category, proximity, keyword in GBP title,
address in search city, open at search time, high rating, address shown,
additional categories, native reviews with text, pin placement, review
recency, CTR, review velocity, HTML NAP matching GBP.

## 3. Google Business Profile
**Primary category = the single biggest controllable pack lever** — most
specific category describing the business as a whole; one wrong switch can
crater rankings. Add all truly-relevant additional categories (~9); re-audit
quarterly. Business name = real legal/brand name only (keyword-in-name works
but fake descriptors violate policy/risk suspension). Services/Products with
keyword-rich names+descriptions. Description ~750 chars. Exact NAP, displayed
address, correct pin (service-area businesses hide address + set areas).
Accurate hours incl. special hours ("open at search time" is a factor).
Attributes, geo-tagged branded photos, regular Posts, seeded Q&A, oldest
legitimate opening date. Complete profiles ≈ 2.7× "reputable", 70% more visits.
GBP landing URL → a unique page (not one already ranking organically), UTM-
tagged. 2024–2026 changes: chat/call history removed 31 Jul 2024; business.site
builder shut Mar 2024 (redirects ended 10 Jun 2024 — audit clients for dead
business.site URLs).

## 4. Reviews (≈20% and rising)
Drivers: volume, velocity, recency, rating, text, owner responses, keyword
content. ~10 reviews is a rough ranking threshold; consistent new reviews beat
raw count. Always respond; handle negatives calmly then offline. Prompt
customers to mention specific services → keyword justifications in the pack
(higher CTR). **Review schema rule:** since 2019 Google ignores self-serving
`review`/`aggregateRating` on `LocalBusiness`/`Organization` (no penalty, no
stars). Put ratings on **`Product`/`Service`** schema; use `LocalBusiness` for
NAP/hours/geo/FAQ. Earn stars via third-party platforms (Google, Yelp,
Doctoralia, etc.).

## 5. Citations & NAP (Spain)
GBP is canonical NAP; every citation mirrors it exactly (incl. suite/format).
Consistency ≈ +19% Maps visibility; declining as a pack factor (~6%) but more
important for AI (13%) and trust/entity. Spain priority: GBP, Bing Places,
Apple Business Connect, Páginas Amarillas, 11811.es, Facebook, Foursquare,
Yelp.es, Cylex, Europages, Informa.es; niche: Doctoralia (medical/dental),
TheFork/ElTenedor + Gastroranking (restaurants), Idealista/Fotocasa (real
estate), Houzz (architecture/interiors).

## 6. Location / service pages (avoid doorway)
Each city/service page ≥50% genuinely unique; treat as a mini-homepage (local
testimonials, area FAQs, real local projects/photos, directions). One page per
*real* service-location intent. Embed map, add LocalBusiness schema, hub-and-
spoke internal links, localized title/H1/URL. On-page local keywords trigger
the "their website mentions" justification → higher pack CTR.

## 7. Structured data
`LocalBusiness` most-specific subtype (`Dentist`, `Restaurant`, …): `name`,
`address`; recommended `telephone`, `url`, `geo` (≥5 decimals),
`openingHoursSpecification`, `priceRange`, `image`, `sameAs`. Multi-location ⇒
per-location page+markup (`department` for sub-units). Service-area ⇒
`areaServed` + `Service`/`serviceType`, omit street address if hidden on GBP.
Ratings only on Product/Service, never self-referential LocalBusiness.

## 8. Local link building
Relevance > volume: chamber of commerce (Cámara de Comercio), local
sponsorships (clubs/events/fiestas), local press/.es digital papers, supplier/
partner pages, local associations, guest content — feeds Prominence + AI
citations.

## 9. Spain / EU specifics
Google ≈ 96%+ of Spanish search. Castilian Spanish primary; regional-language
pages (Catalan/Valencian/Galician/Basque) boost relevance in those regions.
**AEPD cookies (enforced 11 Jan 2024):** banner needs Accept/Reject/Configure
parity; **Google Maps embeds set cookies** ⇒ load after consent (click-to-load
placeholder or Consent Mode v2) — same for GA4/Ads; fines up to €30,000. Bake
into every local landing page built for clients.

## 10. Local + AI ("best web designer for dentists in Spain")
~45% of consumers use genAI for local recs; ChatGPT recommends only ~1.2% of
local businesses — Google rank alone won't carry you. AI local de-emphasizes
proximity; rewards: **Bing Places + Bing organic rank**, consensus across many
complete web profiles, recent Google reviews, explicit local statements/
reviews on your own site, citations (13% AI weight), authoritative local press/
"best of" listicles. Tactic: structured factual on-page ("[Agency] is a web
design studio in [city] for dental clinics, X reviews, founded Y") + FAQ +
GBP/Bing/citation consistency + get into "best [service] in [city]" lists.

## Sources
1. support.google.com/business/answer/7091 — relevance/distance/prominence.
2. brightlocal.com/learn/google-local-algorithm-and-ranking-factors — 2026 weights + top-15 + AI factors.
3. whitespark.ca/local-search-ranking-factors — Whitespark 2026 factor survey.
4. sterlingsky.ca/ultimate-checklist-boost-gbp-profile — GBP checklist/pitfalls.
5. sterlingsky.ca/number-of-reviews-impact-ranking — review count vs ranking.
6. brightlocal.com/learn/review-schema — self-serving review-schema rule.
7. developers.google.com/search/docs/appearance/structured-data/review-snippet — review snippet spec.
8. developers.google.com/search/docs/appearance/structured-data/local-business — LocalBusiness props/departments/geo.
9. developers.google.com/search/blog/2019/09/making-review-rich-results — 2019 self-serving stars removal.
10. support.google.com/business/answer/14919056 — chat/call history removal (Jul 2024).
11. searchenginejournal.com/...google-business-profiles-shut-down/509794 — business.site shutdown.
12. brightlocal.com/research/local-consumer-review-survey — review trust thresholds/platforms.
13. brightlocal.com/resources/local-seo-statistics — pack CTR, "near me", 45% AI-for-local.
14. searchengineland.com/guide/the-current-state-of-google-local-justifications — review/website justifications.
15. searchengineland.com/guide/service-area-pages — service-area vs doorway, ≥50% unique.
16. brightlocal.com/learn/location-pages — unique location-page construction.
17. whitespark.ca/top-local-citation-sources-by-country/spain — Spain citation sources.
18. gs.statcounter.com/search-engine-market-share/all/spain — Google ~96%+ in Spain.
19. secureprivacy.ai/blog/spanish-aepd-cookie-guidelines — AEPD rules, €30k fines.
20. iubenda.com/.../google-maps-and-the-gdpr — Maps embed cookies → consent.
21. gofishdigital.com/blog/ranking-in-searchgpt — Bing/consensus/reviews for local AI.
22. joeyoungblood.com/seo/local-ranking-factors-in-chatgpt — ChatGPT local factors.
23. whitespark.ca/blog/local-businesses-say-goodbye-to-review-snippets — lost self-serving snippets.
24. ranktracker.com/blog/...local-seo-in-spain — Spain directories/regional language/geo-keywords.

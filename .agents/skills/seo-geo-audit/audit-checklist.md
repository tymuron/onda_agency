# SEO + GEO Audit Checklist

Work top to bottom. For each item record: state (pass / partial / fail / n-a),
evidence (file:line, URL, or observed behavior), fix. Pull the mechanism/number
from the matching reference file when writing the recommendation.

## A. Technical foundation (`technical-seo.md`)
- [ ] Root + key pages return HTTP 200 with full server-rendered content (test
      with a bot user-agent). No client-side-redirect or JS-only critical content.
- [ ] Permanent moves use 301/308, not JS/meta-refresh; ≤1–2 redirect hops.
- [ ] Self-referential absolute `rel=canonical` on every indexable page;
      consistent with internal links + sitemap.
- [ ] hreflang cluster: every locale lists itself + all alternates,
      bidirectional, valid ISO codes, one `x-default`. Validate.
- [ ] `robots.txt` present, not blocking needed pages, lists absolute sitemap.
- [ ] `sitemap.xml`: only canonical 200 URLs; accurate `lastmod`; submitted to
      Google + Bing webmaster tools.
- [ ] No `noindex`/`nosnippet`/`max-snippet:0` on pages you want in search/AI.
- [ ] Core Web Vitals (field/lab proxy): LCP ≤2.5s, INP ≤200ms, CLS ≤0.1.
      No production runtime CSS compiler / render-blocking JS / unsized media /
      lazy-loaded LCP image. Images WebP/AVIF.
- [ ] HTTPS enforced site-wide; mobile rendering equivalent + fast.
- [ ] No orphan pages; important pages ≤3 clicks deep.

## B. On-page, content & E-E-A-T (`onpage-content-eeat.md`)
- [ ] Target queries identified; each mapped to ONE page whose *type* matches
      the live SERP (service/landing vs blog). No "everything" doorway page.
- [ ] Unique pixel-budgeted title + matching single H1 + unique meta per page
      (and per language — not English on ES/other pages).
- [ ] Logical heading hierarchy; skimmable; sections self-contained.
- [ ] Topical clusters around real expertise; funnel coverage (TOFU/MOFU/BOFU);
      commercial/local intent pages exist, not only informational.
- [ ] E-E-A-T proof: named founder/author + real author/About page; verifiable
      contact (address/phone/email); named case studies with metrics;
      testimonials with name+company+specific result; process transparency.
- [ ] No scaled/thin/templated/duplicate content; no fake-freshness date edits.
- [ ] Portfolio/proof visuals are real `<img>` with descriptive filename+alt
      (NOT CSS background-only — invisible to Google Images).

## C. Off-page, links & entity (`offpage-links-entity.md`)
- [ ] `Organization` schema with accurate `sameAs` to every owned profile.
- [ ] Authoritative profiles exist & consistent: LinkedIn, Crunchbase,
      industry directories (Clutch/Sortlist/DesignRush…), Wikidata.
- [ ] Exact NAP consistency across all citations.
- [ ] Backlink profile: relevant editorial links + diverse referring domains;
      no spam patterns; natural anchor mix (≤5–10% exact-match). No disavow
      unless an actual manual action.
- [ ] A repeatable digital-PR / brand-mention motion exists (the top lever for
      both SEO and AI). "Built by" link on client work where applicable.
- [ ] Internal linking: hub-and-spoke; every key page ≥3 contextual links.

## D. Local (`local-seo.md`) — if the business serves a place
- [ ] Google Business Profile claimed; **primary category** exactly right;
      relevant additional categories; complete (services, photos, hours, posts,
      Q&A); landing URL is a unique page.
- [ ] Bing Places claimed (matters for ChatGPT/Copilot).
- [ ] Review engine: steady volume/recency, owner responses, keyword
      justifications. Ratings schema on Product/Service, NOT self-serving
      LocalBusiness/Organization.
- [ ] Niche + national directories for the market (Spain: Páginas Amarillas,
      Doctoralia/TheFork/Idealista per vertical).
- [ ] Location/service pages ≥50% unique, with local proof + LocalBusiness
      schema + map (consent-gated in EU).
- [ ] EU/AEPD: cookie banner with Accept/Reject parity; Maps/GA after consent.

## E. GEO / AI engines (`geo-ai-engines.md`)
- [ ] AI retrieval crawlers allowed (OAI-SearchBot, PerplexityBot, Claude bots,
      Googlebot, Bingbot); training-only bots optional to block.
- [ ] Key/service/FAQ pages answer-first (40–60-word lead answer), self-
      contained ~75–300-word chunks, declarative, explicit entity/location
      names, tables, real Q&A.
- [ ] Princeton levers present where natural: quotations, statistics, inline
      citations, fluent authoritative prose. No keyword stuffing.
- [ ] Off-site presence broad & credible (industry press, listicles "best X in
      Y", Reddit/Quora/YouTube) — the dominant AI-visibility correlate.
- [ ] Entity verifiable (Wikidata, consistent naming, sameAs) so LLMs trust it.
- [ ] Actually test target prompts in ChatGPT/Perplexity/Google AI and record
      whether/how the brand appears or is cited.

## F. Measurement & conversion (`measurement-updates-cro.md`)
- [ ] GSC + Bing Webmaster verified; GA4 with Key Events for every lead path
      (form, phone/tel, WhatsApp, thank-you).
- [ ] AI referral tracking (GA4 custom channel + server-log user-agents).
- [ ] Conversion funnel instrumented end-to-end with per-step drop-off.
- [ ] Reporting segments non-branded vs branded.
- [ ] CRO: above-the-fold value prop + single primary CTA; minimal-field form
      (consider multi-step), top-aligned labels, inline validation, parallel
      phone/WhatsApp, trust signals next to CTA, fast pages, message-match.
- [ ] No core-update/manual-action damage (check; if present, diagnose vs
      people-first/E-E-A-T, expect next-update recovery).

## Scoring
For each finding compute impact × confidence ÷ effort. Tag Foundational /
High-leverage / Incremental. Respect dependencies (crawl→content→authority;
entity→AI citation). Then write the report in the SKILL.md output format.

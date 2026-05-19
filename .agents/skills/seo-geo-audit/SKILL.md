---
name: seo-geo-audit
description: >-
  Authoritative SEO + GEO (Generative Engine Optimization) audit and strategy,
  synthesized from ~160 current (2024-2026) primary sources. Use this whenever
  the user wants to rank higher on Google/Bing, show up or get cited in AI
  answer engines (ChatGPT, Perplexity, Google AI Overviews/AI Mode, Gemini,
  Copilot), get more organic traffic or inbound leads/clients, fix why a site
  is "invisible" online, recover from a Google update, do keyword/technical/
  content/local/link audits, optimize Core Web Vitals for ranking, set up
  search/lead measurement, or improve an existing site's discoverability and
  conversion. Trigger even if the user only says things like "why isn't my site
  showing up", "get me more clients from Google", "make ChatGPT recommend us",
  "audit my site's SEO", "we're not getting leads", or names a site to review
  for visibility. Prefer this skill over ad-hoc advice for anything SEO/GEO.
---

# SEO + GEO Audit & Strategy

## Why this skill exists

Search is now two surfaces at once: classic ranked results (Google/Bing) and
generative answers (ChatGPT, Perplexity, Google AI Overviews/AI Mode, Gemini,
Copilot). They share a foundation — crawlable content, a strong brand entity,
topical authority, trust — but reward different things at the margin. Ad-hoc SEO
advice tends to be stale (pre-AI), generic, or vanity-metric driven. This skill
encodes current, sourced, quantified practice and forces every recommendation
to ladder up to the only metrics that matter for most sites: **qualified leads
and revenue**, not traffic.

The depth lives in six reference files (progressive disclosure — load what the
audit needs). This file is the operating procedure and the cross-cutting laws.

## Operating procedure (run this when invoked)

1. **Establish context before auditing anything.** You cannot prioritize
   without it. Determine: the business and what it sells; who the customer is;
   the geographic market and languages; the single primary conversion (lead
   form? call? booking? purchase?); the tech stack and how pages are served
   (static/SSR/CSR); the 5-15 queries a real prospective customer would type or
   ask an AI; current measurement (GSC/GA4/rank/AI tracking) if any. If the
   user hasn't given these, infer from the codebase/site and state your
   assumptions explicitly.

2. **Observe the current state — don't assume.** Read the actual served HTML
   (head + body), robots.txt, sitemap, structured data, key templates, and
   performance-relevant assets. Check the brand's off-site footprint (Google
   Business Profile, Bing Places, directories, review platforms, Wikipedia/
   Wikidata, social/LinkedIn, third-party mentions). Where possible, actually
   query the target prompts in Google and in AI engines and record whether/how
   the site appears or is cited. Trust but verify every prior claim — audits
   are frequently wrong about what's already present.

3. **Run `audit-checklist.md`** across all six domains. For each item record:
   state (pass / partial / fail / not-applicable), the evidence (file:line,
   URL, or observed behavior), and the fix.

4. **Score and prioritize.** Rank every finding by **impact × confidence ÷
   effort**, and tag each as Foundational (blocks everything else),
   High-leverage, or Incremental. Respect dependencies (e.g. crawlability
   before content; entity before AI citation). Be honest about time-to-effect:
   technical fixes show in days, content/authority in weeks-to-months, a
   core-update or trust recovery often only at the next update.

5. **Deliver in the output format below.** Every recommendation must say what to
   do, why (with the mechanism/number), how to verify it worked, and the
   realistic time-to-impact. No generic "write good content" filler.

## Reference map — read the files the audit actually needs

| Read this | When |
|---|---|
| `references/technical-seo.md` | Crawl/index/render, canonical, hreflang/i18n, sitemaps, Core Web Vitals/INP, site architecture, HTTPS, redirects |
| `references/onpage-content-eeat.md` | Keyword/intent, titles/meta, headings, topical authority, E-E-A-T, helpful-content/AI-content policy, content that converts |
| `references/offpage-links-entity.md` | Backlink value, digital PR, anchor/disavow reality, brand mentions, the entity (Knowledge Graph/Wikidata/sameAs) |
| `references/local-seo.md` | Google Business Profile, local pack factors+weights, reviews & review schema, citations/NAP, location pages, Spain/EU specifics |
| `references/geo-ai-engines.md` | How ChatGPT/Perplexity/AI Overviews/Gemini/Copilot retrieve & cite, the Princeton GEO findings, content structure for extraction, AI-crawler policy, measuring AI visibility |
| `references/measurement-updates-cro.md` | Google update history & recovery, GSC/GA4, AI-traffic tracking, zero-click reality, conversion-rate optimization & lead-form best practice |

Each reference is dense and ends with its source list. Cite the mechanism/number
when you make a recommendation so the user understands the why, not just the what.

## The cross-cutting laws (what most moves the needle, 2024-2026)

These are the distilled, sourced conclusions. When in doubt, weight by these.

1. **Optimize for leads, not traffic.** Segment by *non-branded* organic,
   instrument the conversion funnel, track phone/WhatsApp/form as conversions.
   AI-referred visitors convert ~4.4× organic; ~60% of Google searches are now
   zero-click — value qualified impressions and brand demand, not just clicks.

2. **The brand entity is now the master lever for both SEO and GEO.** Brand web
   mentions correlate with AI-answer visibility ~3× more than backlinks
   (Ahrefs 75k-brand study: ~0.66 vs ~0.22); YouTube mentions are the single
   highest correlate (~0.74). Build: consistent NAP everywhere, `Organization`
   schema with accurate `sameAs`, Wikidata, complete authoritative profiles,
   and *frequent third-party mentions*. This is the same motion as digital PR.

3. **Off-site presence drives AI recommendations more than your own site.**
   ~82% of AI citations are earned media; broad, repeated, credible third-party
   coverage (industry press, directories, listicles, Reddit/Quora, YouTube) is
   the unifying GEO lever. Don't treat GEO as separate from PR/brand.

4. **Crawlable, server-rendered content is non-negotiable.** Client-side
   redirects and JS-only critical content are the worst failure mode — bots may
   index nothing. Server-render; return real HTTP status codes; 301/308 not JS
   redirects; keep titles/meta/canonical/hreflang/schema in the served HTML.

5. **Match the page to intent, or it won't rank or convert.** Read the live
   SERP for each target query; build the content *type* Google already rewards
   (service/landing vs blog). Informational traffic is hit hardest by AI
   Overviews and converts worst for service businesses — prioritize
   commercial/transactional and local intent.

6. **For AI extraction: answer-first, in self-contained chunks.** Lead each
   section with a 40-60 word direct answer; keep sections ~75-300 words,
   readable out of context; use declarative factual sentences, explicit entity
   names, tables, and real Q&A. Princeton-validated on-page wins: add
   **quotations (~+28%), statistics (~+26%), citations (~+25%), fluent
   authoritative prose**. Keyword stuffing is net-negative for AI.

7. **Bing is a GEO surface.** ChatGPT Search and Copilot lean on Bing's index
   (~87% of SearchGPT citations match Bing top results). Submit to Bing
   Webmaster Tools + Bing Places, not just Google.

8. **Allow AI retrieval crawlers.** Blocking OAI-SearchBot / PerplexityBot /
   Claude bots / Googlebot removes you from those answers. Optionally block
   training-only bots (GPTBot, CCBot, Google-Extended) — that does not affect
   live citation. Don't set `nosnippet`/`max-snippet:0` if you want AI
   inclusion.

9. **Local visibility = primary GBP category + reviews + consistent NAP.**
   Primary Google Business Profile category is the single biggest local-pack
   lever; reviews are ~20% and rising (volume, recency, velocity, responses,
   keyword justifications). Never put self-serving `review`/`aggregateRating`
   schema on `LocalBusiness`/`Organization` — it's ignored; put ratings on
   `Product`/`Service`. Mirror NAP exactly across local + niche directories.

10. **Core Web Vitals are a real ranking + conversion factor.** Targets (field
    data, 75th pct): LCP ≤2.5s, **INP ≤200ms** (replaced FID Mar 2024),
    CLS ≤0.1. Runtime CSS-in-browser (e.g. the Tailwind Play CDN) and
    render-blocking JS are common, fixable killers. 0.1s faster ≈ +8% conversion.

11. **E-E-A-T is won with proof, not adjectives.** Real named author/founder,
    a specific verifiable About page, real contact details, original media,
    and case studies/testimonials with named clients and concrete numbers.
    First-hand experience now rivals formal credentials. Trust is the anchor.

12. **Links still matter but are downgraded and quality-gated.** Few relevant
    editorial links + many diverse referring domains beat volume. Digital PR /
    expert commentary is the top-ROI tactic for a small operator. Disavow is a
    "billable waste of time" unless there's an actual manual action — don't
    chase "toxic links".

13. **One idempotent technical foundation, then compound on content + entity.**
    Technical SEO is mostly do-once-correctly (canonical/hreflang/sitemap/
    render/CWV). Rankings and AI citations then compound from authority,
    freshness, and breadth of credible mention over months. Set expectations.

## Output format (use this exact structure)

```
# SEO + GEO Audit — <site> (<date>)

## Verdict
2-4 sentences: can this site realistically win search + AI visibility + leads,
the single biggest blocker, and the single highest-leverage move.

## Scorecard
Table: Domain | State (Strong/OK/Weak/Critical) | One-line reason
Domains: Technical · On-page/Content · Off-page/Entity · Local · GEO/AI · Measurement & Conversion

## Action plan (prioritized)
Group by: NOW (foundational, do first) · NEXT (high-leverage) · ONGOING (compounding).
For each item:
- **What** — the concrete action (file/page/profile, specific change)
- **Why** — mechanism + number/source from the references
- **Effort** — S/M/L  ·  **Impact** — High/Med  ·  **Time-to-impact**
- **Verify** — exactly how to confirm it worked (tool, query, metric)

## What to measure
The 3-6 metrics this site should watch and the tools/setup to capture them.

## Honest expectations
What improves in days vs weeks vs months; what is outside the user's control.
```

## Guardrails

- Recommend only sustainable, guideline-compliant tactics. Never suggest PBNs,
  bought links, mass low-quality directories, cloaking, doorway pages, scaled
  unedited AI content, fake reviews, or keyword-stuffed business names — all are
  named spam and are neutralized or penalized. Explain why when declining.
- No vanity advice. If a tactic is low-evidence (e.g. `llms.txt` for citation),
  say so and rank it accordingly rather than overselling it.
- Quantify and cite the mechanism. "Add statistics and a named-client case
  study (Princeton GEO: +~26% AI visibility; CXL: trust signals +79% conv.)"
  beats "improve your content".
- Tailor to the user's actual stack, market, and capacity (a solo operator
  cannot run an enterprise link program — give the realistic version).

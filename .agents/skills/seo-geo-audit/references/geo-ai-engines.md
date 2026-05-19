# GEO — Generative Engine Optimization (2024–2026)

Being surfaced/cited by ChatGPT, Perplexity, Google AI Overviews/AI Mode,
Gemini, Copilot. Contents: 1 Princeton findings · 2 how each engine cites ·
3 content structure for extraction · 4 off-site (dominant lever) · 5 technical
GEO · 6 entity/brand · 7 local+GEO · 8 measuring GEO · 9 solo playbook ·
10 llms.txt verdict.

## 1. Princeton/GT GEO paper (arXiv 2311.09735) — empirical bedrock
GEO-bench (10,000 queries); visibility = Position-Adjusted Word Count +
Subjective Impression. GEO methods boost visibility **up to ~40%**. Baseline
≈19.5%; what measurably worked: **adding quotations ≈27.8%** (best), **adding
statistics ≈25.9%**, **fluency optimization ≈25.1%**, **citing sources
≈24.9%**, technical terms ≈23.1%, easy-to-understand ≈22.2%, authoritative tone
≈21.8%. **Keyword stuffing ≈17.8% — below baseline (net-negative).** Method
effectiveness is domain-dependent (cite-sources wins factual/debate; statistics
wins law/finance; quotations wins history/people; authoritative tone wins
trust-heavy) — combine and tune.

## 2. How each engine retrieves & cites (and organic overlap)
- **ChatGPT Search:** Bing index + OpenAI crawl + query fan-out; ~87% of
  SearchGPT citations match Bing top organic; cites ~15% of retrieved pages;
  citation-eligibility crawler = **OAI-SearchBot**. → Bing visibility is a
  direct lever.
- **Perplexity:** own index (PerplexityBot) + live fetch (Perplexity-User);
  quality gate for entity-clarity + authority; authority-domain boosts (Reddit,
  GitHub, LinkedIn). Rewards short, verifiable, extractable passages.
- **Google AI Overviews / AI Mode:** RAG ("grounding") over Search + Gemini +
  query fan-out. Organic-overlap low (~20–26%) but ~76% of AIO citations rank
  top-10, ~97% top-20, median ≈2; pages ranking across multiple fan-out
  sub-queries ≈ +161% citation likelihood; ~58% of informational queries
  trigger AIO.
- **Copilot:** Bing index + live web; recent/authoritative/structured pages;
  Bing Webmaster Tools "AI Performance" report (per-URL Copilot citations,
  since Feb 2026).
- Cross-engine: ChatGPT vs Perplexity recommendation overlap ~8.6%; ChatGPT
  favors established/known brands (answers ~60% without web search); Perplexity
  favors live "source of truth". **Optimize each engine separately.**
Net: rank organically (esp. Bing for ChatGPT/Copilot; top-3 Google for AIO)
AND structure for extraction AND build off-site presence.

## 3. Content structure for LLM extraction (RAG-aware)
RAG = chunk → embed → retrieve → rerank → top chunks reach the LLM. So:
**answer-first** (direct answer in first 150–300 words; 40–60-word summary
under each H2); **self-contained chunks** (one question each, ~75–300 words,
readable out of context, no "as mentioned above"); grounding value plateaus
~540 words; raw word count ≈ uncorrelated with citation (~0.04) — depth/intent
over length; declarative factual sentences; explicit entity names not pronouns;
clear definitions; comparison **tables**; **Q&A/FAQ** blocks; anticipate
follow-ups (fan-out + multi-turn). Embed quotes/statistics/citations in prose
(§1).

## 4. Off-site GEO — the dominant lever (strongest data in the field)
Ahrefs 75,000-brand correlations with AI visibility: **YouTube mentions 0.737**
(highest), **branded web mentions 0.664–0.709** (≈3× backlinks), branded
anchors 0.51–0.63, branded search 0.35–0.47; Domain Rating ~0.27–0.33;
#backlinks weak; #pages ~0.19 (≈none). Most-cited domains across engines:
Reddit, Wikipedia, YouTube, LinkedIn, Forbes (UGC + authority media); ChatGPT
rebalanced Sept 2025 (don't over-index one platform). **Do:** earn third-party
mentions/PR, get listed/reviewed on directories & review platforms, genuine
Reddit/Quora presence, YouTube coverage, drive branded search. **Avoid:**
inauthentic/spam mentions; backlink-quantity thinking.

## 5. Technical GEO
**robots.txt trade-off:** allow retrieval/citation bots (OAI-SearchBot,
ChatGPT-User, PerplexityBot, Perplexity-User, Claude-SearchBot/-User,
Googlebot, Bingbot) — blocking them removes you from those answers; optionally
block training-only bots (GPTBot, ClaudeBot, Google-Extended, CCBot) without
losing live citation. For a business wanting AI recommendations: allow all
search/retrieval bots. Don't set `nosnippet`/`data-nosnippet`/`max-snippet`
(suppress AIO). Need server-rendered, indexed, snippet-eligible HTML; fast;
clean sitemap; internal links. **Structured data — balanced:** Google says
schema not required for AI features and an Ahrefs test found no major citation
uplift from JSON-LD — but it aids crawling/parsing/entity disambiguation and
Bing says it helps Copilot understand content. Do `Organization`/`LocalBusiness`
/`Person`/`Article` with accurate `sameAs` and visible-text match; don't treat
schema as a citation silver bullet.

## 6. Entity / brand for GEO
LLMs recommend entities they can verify (≈22% of training data ≈ Wikipedia;
Knowledge Graph leans on Wikidata). Consistent NAP/brand everywhere;
`Organization sameAs` linking site ⇄ Wikidata/LinkedIn/Crunchbase/GitHub/review
profiles; pursue Wikidata; grow branded search; consistent on-page entity
naming. Mention frequency + consistency > links.

## 7. Local + GEO
ChatGPT recommends ~1.2% of local businesses. Leans Bing/Bing Places +
authoritative web; Perplexity rewards complete owner-managed profiles (30+
photos, full description, replies to every review, pinned categories).
Optimize GBP **and Bing Places**; accumulate/respond to reviews; get into
local + niche directories and "best [service] in [city]" listicles (exactly
what engines synthesize); local PR; city/service pages with self-contained
answers + explicit location entities; authentic local forum mentions.

## 8. Measuring GEO
GA4: AI referrers default to "Referral" — build a custom channel group regex
(chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com, …);
undercounts (no referrer / mobile apps / pre-June-2025). Server/CDN logs:
filter AI user-agents + verified IP ranges (truest crawl picture). Consoles:
GSC (AIO folds into Web), Bing Webmaster AI Performance report. Tools: Profound,
Ahrefs Brand Radar, Semrush, Otterly; weekly manual prompt panel — KPI = **AI
Share of Voice** (your mentions ÷ total across tracked prompts).

## 9. Realistic solo-agency playbook (priority order)
1. Off-site first: brand mentions on niche/industry blogs, local press,
   podcasts; "best web design agencies in [city/Spain]" listicles &
   directories; real Reddit/Quora/LinkedIn presence; YouTube (top correlate);
   drive branded search. 2. Entity: Organization+LocalBusiness schema +
   `sameAs`; consistent NAP; Wikidata; complete GBP **and Bing Places** +
   reviews. 3. On-site for extraction: rewrite key/service/FAQ pages
   answer-first, add statistics/quotes/citations, tables, anticipate
   follow-ups, explicit entity/location naming; SSR, fast, indexed,
   snippet-eligible; clean sitemap. 4. Crawler policy: allow all retrieval/
   search bots. 5. llms.txt: optional/low-evidence. 6. Measure: GA4 custom
   channel + log monitoring + Bing AI report + one SOV tool + weekly prompt
   panel.

## 10. llms.txt — balanced verdict
Root `/llms.txt` markdown to guide LLMs. Adopted by dev-doc platforms for
coding agents; **no major answer engine consumes it** (Google won't support it;
~0.1% of AI requests hit it; no citation correlation). Harmless, cheap,
possibly useful if you ship docs/tools or for future-proofing — **not** a
current GEO lever; do not prioritize over §1–8.

## Sources
1. arxiv.org/abs/2311.09735 (+ ar5iv full) — GEO paper: per-method % lifts; keyword stuffing fails.
2. developers.google.com/search/docs/appearance/ai-features — AIO/AI Mode RAG+fan-out; nosnippet/Google-Extended.
3. developers.google.com/search/blog/2025/05/succeeding-in-ai-search — Google's AI-search guidance.
4. developers.google.com/search/docs/fundamentals/ai-optimization-guide — "AEO/GEO is still SEO"; mythbusts llms.txt.
5. searchenginejournal.com/...aeo-and-geo-still-seo/575026 — coverage of above.
6. seerinteractive.com/insights/87-percent-of-searchgpt-citations-match-bings — 87% SearchGPT–Bing overlap.
7. developers.openai.com/api/docs/bots — OAI-SearchBot vs ChatGPT-User vs GPTBot independence.
8. help.openai.com/.../chatgpt-search — Bing-powered + citations.
9. docs.perplexity.ai/guides/bots — PerplexityBot vs Perplexity-User.
10. semrush.com/blog/ai-overviews-study — ~20–26% organic overlap.
11. semrush.com/blog/most-cited-domains-ai — Reddit/Wikipedia/LinkedIn/YouTube; Sept rebalance.
12. ahrefs.com/blog/ai-brand-visibility-correlations — YouTube 0.737, mentions 0.664, backlinks weak.
13. ahrefs.com/blog/how-to-rank-in-ai-overviews — 76% top-10, median 2, fan-out +161%, word-count ~0.04.
14. ahrefs.com/blog/what-is-llms-txt + searchengineland.com/no-llms-txt... + seroundtable.com/google-does-not-endorse-llms-txt — llms.txt skeptic/balanced.
15. ahrefs.com/blog/schema-ai-citations — no major uplift from schema.
16. llmstxt.org — llms.txt spec.
17. blog.google/...google-search-ai-mode-update — AI Mode + fan-out.
18. blogs.bing.com/webmaster/February-2026/...AI-Performance — Bing AI Performance report.
19. microsoft.com/.../bringing-the-best-of-ai-search-to-copilot — Copilot citations.
20. axios.com/2025/10/16/reddit-chatgpt-google-ai-perplexity — Profound 1B+ citations (Reddit/YouTube).
21. marketingcode.com/chatgpt-recommends-1-percent-local-businesses — ~1.2% local recommend rate.
22. minneapolismade.com/...chatgpt-vs-perplexity — ~8.6% local overlap.
23. orbitmedia.com/blog/track-ai-traffic-ga4 — GA4 AI channel groups.
24. otterly.ai/blog/bing-webmaster-tools-ai-performance-report — Bing AI report; llms.txt 0.1% logs.
25. searchengineland.com/schema-markup-ai-search-no-hype-472339 — schema's limited AI role.
26. xseek.io/docs/ai-robots-txt-guide — training vs retrieval bot patterns.

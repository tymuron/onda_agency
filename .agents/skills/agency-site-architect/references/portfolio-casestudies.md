# Portfolio & Case-Study Presentation

Core thesis: for a solo studio selling to local SMBs, the work IS the product
demo and primary credibility engine. Case studies are the most persuasive B2B
asset (influence ~73% of buyers); proof should occupy ⅓–½ of a converting page.
Fix surfacing first, then depth, then honest labelling, then indexability.

## 1. Canonical case-study template (results-led, not a gallery)
1. **Outcome headline** — lead with the result, not the client name:
   `[Result] for [client/vertical] through [what you did]`. No hard numbers yet?
   headline the transformation ("From brochure site to booking machine").
2. **Client / context** (3-4 sentences) — who, vertical, situation; put the
   **"Concept project" / "Client work" label here, at the top**.
3. **Problem** — specific business pain in SMB-owner language.
4. **Approach** — process, design decisions, *rejected directions and why*
   (proves rigor for a solo studio).
5. **Solution** — the work: large real device mockups, before/after, key
   screens with captions explaining the *decision*.
6. **Measurable result** — see §2.
7. **Quote** — testimonial tied to *this* project: full name, role, business,
   photo.
Quantities: **3-5 deep** case studies (quality > quantity). Two-tier IA:
scannable cards (one hero image, vertical tag, one-line outcome) → full detail
pages (~600 words + strong visuals). Filter by vertical so the SMB self-selects.

## 2. Results without hard client metrics (Onda's reality)
Narrative + rationale outweigh raw numbers when you have none. Credible
proxies: **craft/performance you CAN measure on your own builds** (Lighthouse /
Core Web Vitals / load time / a11y — "Concept build 98/100 vs the clinic's
current 31"); **annotated before/after teardown of the SMB's existing site**
(real, honest, expertise without claiming a client); scope & craft; qualitative
(prototype walkthroughs, a real owner quote if pitched); benchmark framing
("industry avg booking-form completion is X; this targets Y").

## 3. Concept/spec work — honest presentation (critical)
Concept work is legitimate and respected; the only sin is mislabeling.
- **Label at the top** of every concept piece ("Concept project",
  "Speculative redesign", "Self-initiated") — frame as a capability demo, not a
  disclaimer.
- Strongest credible move: redesign a *real, named* local business's site as an
  explicit unsolicited concept ("Concept redesign for [Real Clinic] — not
  affiliated") or pitch it and document it live.
- **Never** invent a client, imply payment, use fake testimonials, or show
  client logos you didn't work for — fabricated testimonials are FTC false
  advertising; one exposed fake erases all credibility.
- Ethical credibility ladder: concept → free/discounted real build → named
  testimonial + metrics → repeat; supplement with educational content.

## 4. Visual presentation & indexability (SEO/GEO-critical)
Real device mockups beat flat screenshots for premium perception. **Every
portfolio image MUST be a real `<img>`, never a CSS `background-image`** —
Google does not index CSS backgrounds, so a CSS-bg portfolio is invisible to
Google Images and AI visual retrieval (lost free credibility traffic).
Descriptive **filenames** (`dental-clinic-booking-redesign.webp`) + context-rich
**alt**; place images next to relevant text; submit an image sitemap. Indexable
visual proof = ranking in Google Images for "dental website design" + AI visual
citation eligibility.

## 5. Portfolio IA & internal linking
Surface work **above the fold** (recent shot + one-line outcome). Grid of
vertical-filtered cards → hover → full detail page. Every detail page ends with
**"Next project"** + related-by-vertical links. **Cross-link case studies into
service/vertical pages** (vertical page → its case studies, and back) — kills
orphans, builds topical authority, lets the work sell on commercial pages.

## 6. Trust signals around the work
Per project: real business name, logo (only if real), testimonial with full
name + role + company + photo (the combination is what makes it believable).
Generic unnamed quotes read as fake. Awards/years/build-count fine — never
fabricated.

## 7. Performance (heavy imagery = Core Web Vitals risk)
Never `loading="lazy"` the LCP/hero (16% of sites do — bug); use
`loading="eager"` + `fetchpriority="high"` on it. Lazy-load all below-fold
images. Serve AVIF→WebP→JPEG via `<picture>` (AVIF ~50%+ smaller). `srcset` +
`sizes` ≥3 widths. Explicit `width`/`height` on every image (CLS).

## 8. Case studies → GEO
AI cites specific, named, results-bearing, structured content. Each case study
= structured page, clear H2s, results table/bullets, named entity (vertical +
city), verifiable specifics. Get into the listicles/directories AI already
cites for "best [vertical] web designer in [city]"; brand mentions outperform
backlinks ~3:1 for AI Overviews; date + refresh case studies (freshness).

## DO / AVOID
DO: lead with outcome; label concept work at the top; show process + rejected
directions; real `<img>` + alt + filenames; before/after; vertical filtering;
cross-link to service pages; named testimonials w/ photo; eager LCP / lazy
below-fold; AVIF/WebP + srcset + dimensions; structured pages for GEO.
AVOID: gallery-only with no reasoning; burying work; unlabeled concept work;
fake clients/logos/testimonials; CSS-background portfolio images; lazy LCP;
unnamed generic quotes; one giant unsegmented page; "great results" with no
specifics.

## Onda priority order
1 move work above the fold + vertical-filtered grid → 2 rebuild 3-5 concept
pieces as full results-led case studies, each labelled "Concept" → 3 all
portfolio media to real `<img>` + descriptive filenames/alt + image CWV hygiene
→ 4 owner-language problem framing + craft/performance proxy metrics +
before/after teardowns of real local sites (labelled, unaffiliated) →
5 cross-link case studies ↔ vertical/service pages; structure for GEO; EN/ES/KA
parity.

## Sources
1. nngroup.com/articles/ux-design-portfolios — 3-5 deep, 7-part structure, show messy process.
2. nngroup.com/videos/ux-design-portfolio-case-study — design+process+business impact.
3. nngroup.com/videos/presenting-ux-case-study — STAR/METEOR storytelling.
4. nngroup.com/topic/case-studies — case-studies hub.
5. orbitmedia.com/blog/evidence-webpages — 14 evidence types; ⅓–½ proof.
6. orbitmedia.com/blog/how-to-write-testimonials-examples — specific named testimonials.
7. orbitmedia.com/our-work/case-studies — impact-in-title model.
8. orbitmedia.com/blog/b2b-service-page-checklist — proof into service pages.
9. orbitmedia.com/blog/social-proof-web-design — social-proof placement.
10. blog.uxfol.io/ux-case-study-template — 7-section template; no-metrics guidance.
11. feather.so/blog/case-study-website — card galleries, vertical filtering.
12. developers.google.com/search/docs/appearance/google-images — `<img>` indexed, CSS bg NOT; filenames/alt/srcset/AVIF/sitemap.
13. creativeboom.com/tips/is-it-ethical-to-present-concept-work — label at top; pitch-to-brand framing.
14. portfolio.fandom.com/wiki/Spec_Work + hellobonsai.com/blog/spec-work — spec work legitimate; label.
15. paigebrunton.com/blog/create-web-design-portfolio-without-clients — concept projects in target industry.
16. webdesignerdepot.com/2022/10/...portfolio-with-zero-clients — credibility with zero clients.
17. rapidweblaunch.com/blog/get-web-design-clients-no-portfolio — ethical no-portfolio paths.
18. brixongroup.com/...compelling-case-studies — named clients ≈ +37% credibility.
19. fryerhq.co.nz/post/case-study-statistics-2025 — 73% influenced, 78% more likely.
20. agencypro.app/blog/agency-case-study-guide — challenge/approach/results, quantify.
21. motarme.com/anatomy-of-a-high-converting-case-study — outcome headline.
22. upliftcontent.com/blog/how-to-write-a-case-study — 8-step, outcome-led, before/after.
23. webflow.com/blog/web-design-portfolios — surface work above fold; hover→detail.
24. brandedagency.com/blog/...evaluate-webflow-agency-portfolios — quality signals (metrics, named quotes).
25. corewebvitals.io/pagespeed/optimize-images-for-core-web-vitals — never lazy LCP; AVIF/WebP; srcset+dims.
26. virayo.com/blog/generative-engine-optimization-strategies — AI cites structured/specific; mentions>backlinks 3:1.
27. demandlocal.com/blog/geo-strategies-agencies-cited-ai-answers + boast.io/testimonial-guidelines — listicle/entity GEO; fake testimonials = legal risk.

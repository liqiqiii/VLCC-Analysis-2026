---
layout: default
title: What Did AI Actually Revolutionize? — Capex vs Revenue Reality Check (Jun 1, 2026)
---

# What Did AI Actually Revolutionize?
## $1.2T Capex Has Flowed In. Where's the Real Output?
### June 1, 2026 — Industry Analysis

> **The user's question, paraphrased**: Most AI investment came from Mag7's traditional cloud/ads profits. The biggest winners are Nvidia and its suppliers (SK Hynix, Samsung, Micron — all now trillion-dollar companies). But actual AI usage is still quite limited. What did AI actually revolutionize?

> **TL;DR — Short, honest answer**:
> - **Yes** — your framing is largely correct on the financial geometry. The "picks and shovels" winners (Nvidia + memory + components) have captured most of the realized profit; end-user AI revenue is still much smaller than the capex.
> - **But** the gap is closing fast. AI-native software ARR has gone from ~$15B (early 2025) to **~$100-200B annualized (mid 2026)**, growing 100-300% per year.
> - **The honest "revolutionized" list is short**: **software engineering** is the only knowledge-work category that has been *transformed at scale* (20M+ Copilot users, 50%+ productivity gains, statistically validated). **Advertising** (Meta) and **customer service** are *meaningfully improved* but not transformed. Everything else is mostly *augmentation with modest ROI* (only 6% of enterprises report 5%+ EBIT impact from AI per McKinsey 2025).
> - **The math gap**: 2026 hyperscaler capex ~$700B vs AI software revenue ~$150-200B = $500B annual gap. Funded increasingly by **debt** ($230B+ new sector debt 2026). Free cash flow collapsing (Amazon -95%). **This is unsustainable as a 3-year trajectory** — either revenue scales into capex (Anthropic-style 30x growth continuing), or capex slows and the memory/Nvidia profit pools shrink.
> - **My honest take**: We're 2-3 years into an infrastructure buildout that requires 5-7 years of revenue scaling to justify. **Software engineering proves the revolution is possible.** Whether it scales to other knowledge work in 2026-2028 is the trillion-dollar question.

---

## ⚠️ Protocol Notice

Applies the **Two-Step Research Protocol** from `.github/copilot-instructions.md`. Section 1 = fact-base. Section 2 = Step 1 draft answering "what was revolutionized?". Section 3 = Step 2 audit. Section 4 = honest synthesis + open questions.

---

# Section 1 — Fact-Base

## 1.1 Capex Flowing IN (the spending side)

Hyperscaler AI infrastructure capex, by year:

| Year | Total ($B) | Microsoft | Google | Amazon | Meta |
|------|-----------|-----------|--------|--------|------|
| 2024 | ~$197B | ~$70-80B | ~$70-80B | ~$75B | ~$40B |
| 2025 | $300-380B | $80B | $75-93B | $125B | $60-65B |
| **2026** | **$700B+** | **$180-190B** | **$180-190B** | **$180-200B** | **up to $145B** |

**Cumulative 2024-2026: ~$1.2 trillion** from just 4 companies, plus Oracle, plus pure-play infrastructure (CoreWeave, Crusoe, etc.).

**Critical financial signals (per CreditSights, Allianz Research, Futurum)**:
- **Capex/revenue ratio: 45-57%** — utility-industrial-grade, unprecedented for tech
- **Free cash flow collapsing**: Amazon -95% to $1.2B; Alphabet -90% projected
- **Debt-financed**: $230-240B in new sector debt in 2026 alone
- ~60% of capex is now NON-CHIP infrastructure (power, cooling, land, networking)

Source: Visual Capitalist, valueaddvc, CNBC, Futurum, AICerts, CreditSights, Allianz, epoch.ai.

## 1.2 Profit Captured by Picks-and-Shovels

### Nvidia
- FY2026 revenue tracking ~$200B+, net income ~$100B+
- Captures the majority of margin in the AI value chain

### Memory (SK Hynix + Samsung + Micron) — all now $1T+ market cap

| Company | Q1 2026 Revenue | Operating Margin | HBM Share | Market Cap |
|---------|-----------------|-------------------|-----------|------------|
| **SK Hynix** | ₩52.6T ($38B) — +198% YoY | **72% (record)** | **50-59%** | **$1.06T** |
| **Samsung (DS division)** | ₩81.7T ($60B+) | 65%+ | ~22% | $1T+ |
| **Micron** | $23.86B (FQ2'26); ~$33.5B forecast Q3 | Gross 81% | ~21% | $1T+ |

- HBM now ~**50%+ of AI GPU bill of materials**
- All 2026 HBM capacity sold out; tightness through 2028
- Combined memory revenue 2026 annualized: **~$300B+**

### Components (PCB, MLCC, networking, optics, power)
- Estimated combined revenue: $150-200B+ annualized
- Major winners: Broadcom, Arista (networking), Vertiv (cooling), Lite-On (power), Murata (MLCC), Yageo, Unimicron (PCB)
- Margins healthy but lower than memory/GPU

**Estimated total value-chain capture by suppliers**: **~$650-750B annualized of value created** (revenue, not profit) — roughly matching the 2026 hyperscaler capex on the supply side.

## 1.3 What End-Customers Are Generating (the demand side)

### Pure-play AI-software ARR (mid 2026)

| Company | Jan 2025 ARR | Dec 2025 ARR | Mid 2026 ARR | Growth |
|---------|-------------|--------------|--------------|--------|
| **OpenAI** | ~$13B | ~$25B | **~$33B** (Q2'26) | ~2.5x |
| **Anthropic** | ~$1B | ~$9B | **~$45B** (May'26) | **30x** in 15 months — overtook OpenAI |
| **Combined** | ~$14B | ~$34B | **~$78B** | ~5.5x |

- Anthropic Q2 2026: first profitable quarter ($559M)
- OpenAI: ChatGPT at 900M weekly users; projected $14B loss in 2026
- 70% of Fortune 100 = Anthropic enterprise customers
- Claude Code reached $1B ARR within 6 months of launch
- 80% of Anthropic revenue is enterprise

### Embedded AI revenue inside hyperscaler stacks

| Product | Paid users / Revenue | Note |
|---------|---------------------|------|
| **Microsoft Copilot** | **15M paid seats**, $30/user/month | ~$5.4B ARR from this alone; plus Azure OpenAI |
| **Google Gemini Enterprise** | Bundled in Workspace; specific seat count undisclosed | Significant but opaque |
| **AWS Bedrock** | Infrastructure (no seat count); ~$10B+ ARR for foundation model services | Multi-model platform |
| **Meta AI-driven advertising** | Q4 2025 ad rev $58B (+24% YoY); Advantage+ at $60B+ ARR; AI attribution at $1B+ rapid run rate | Massive: AI directly attributable to several percentage points of ad lift |

**Estimated total AI software + AI-driven revenue mid-2026: $150-200B annualized**

### The math gap

| Metric | Value |
|--------|-------|
| 2026 hyperscaler capex | ~**$700B** |
| 2026 AI software revenue (broad) | ~**$150-200B** |
| **Gap** | **~$500B annually** |
| Gap funded by | Debt (+$230B 2026) + FCF cushion + existing cash |

**Capex/AI-revenue ratio: ~3.5-4.7x.** Even if revenue triples by 2028 ($450-600B), it would only catch up to the *2026* level of capex — and 2027/2028 capex is projected even higher.

## 1.4 Productivity Reality (the "did it work?" side)

McKinsey 2025 + BCG 2026 + multiple surveys:

| Metric | Result |
|--------|--------|
| % of orgs using AI in ≥1 function | **88%** |
| % scaled enterprise-wide | 33% |
| % reporting any measurable EBIT impact | **39%** |
| % "AI high performers" (5%+ EBIT from AI) | **6%** |
| Productivity gain (early adopters) | 15-22% |
| BCG-measured task-specific gains | 30-90% |
| Top performer ROI multiples | 5-10x |

**Translation**: The revolution exists for the 6%. For the median company, AI is a 15-22% productivity tool with limited bottom-line impact — better than spreadsheets in the 1980s, but not on the scale the capex implies.

---

# Section 2 — STEP 1 Draft Answer

## Core Conclusion (answering "what did AI actually revolutionize?")

**One knowledge-work category has been *revolutionized* at scale: software engineering.** Two adjacent categories — advertising and customer service — have been *meaningfully improved* but not transformed. Everything else (legal, healthcare clinical, manufacturing, education, general knowledge work) is in the **pilot-to-augmentation phase**, generating modest productivity gains for the 6% of "AI high performers" and noise for the other 94%. The financial geometry the user described is correct: ~$1.2T of cumulative capex has flowed in 2024-2026, captured first by Nvidia (~$100B+ net income) then by memory (~$300B+ revenue, $1T each in market cap), then by component suppliers (~$150B+ revenue). The end-customer AI revenue is $150-200B annualized — a real number growing fast (100-300%/yr at pure-plays), but **3-4x smaller than 2026 capex**. The 2026-2028 window will reveal whether revenue scales into the capex (justifying the supplier supercycle) or the gap widens (triggering a capex pullback and memory/Nvidia profit pool compression). **Currently the evidence points toward partial validation, not full justification** — coding is the proof-of-concept that the revolution is possible; the breadth question is unresolved.

## 3 Supporting Points (The Revolution IS Real Where It's Real)

**S1. Software engineering has been demonstrably transformed at scale.**
- 20M+ GitHub Copilot users; 90% of Fortune 100; 50,000+ orgs
- 51-55% faster task completion (controlled studies)
- 3.6 hours/week saved per developer
- 60% more PRs merged for daily AI users
- Time-to-PR cut from 9.6 days to 2.4 days in enterprise pilots
- Plus Cursor, Claude Code (~$1B ARR in 6 months), Codeium, etc. — entire new sub-industry
- **This is the clearest example of AI-as-productivity-revolution**, validated by published studies.
→ **Claim → Evidence**: GitHub research, JetBrains 2026 dev survey, Accenture-Microsoft enterprise studies; specific statistical caveat: AI-co-authored PRs have 1.7x more issues than human-only PRs (quality offset).

**S2. AI-native software revenue is growing at unprecedented speed.**
- Anthropic ARR: $1B (Jan 2025) → $45B (May 2026) = **30x in 17 months**, fastest enterprise-software ramp in history
- OpenAI ARR: $13B → $33B in 18 months (2.5x)
- 1,000+ Anthropic enterprise customers at $1M+/year (up from 500 in February 2026)
- 70% of Fortune 100 are Anthropic customers
- Claude Code at $1B ARR in 6 months from launch
- **This growth pace, if it continues, scales into the capex within 2-3 years**
→ **Claim → Evidence**: Anthropic IPO filings/secondaries; OpenAI revenue press; cross-check enterprise contract signings; risk: ARR growth slowing in 2027 would invalidate.

**S3. Existing services are getting AI-driven incremental boosts at scale.**
- Meta Q1 2026 revenue +33% YoY; Advantage+ AI ads at $60B+ ARR; new attribution model = 24% conversion lift
- Meta paid messaging on WhatsApp at $2B ARR
- Google AI Overviews changing search experience
- AWS Bedrock at ~$10B+ ARR for foundation-model API services
- **Existing business model improvements are real and measurable** even if they don't show up as "AI revenue" in standalone form
→ **Claim → Evidence**: Meta 10-Q; AdExchanger reporting; Google Cloud announcements; risk: hard to separate "AI lift" from organic growth.

## 2 Opposing Points (The Revolution Has NOT Broadly Arrived)

**O1. Median enterprise sees modest-to-zero impact; only 6% are "AI high performers".**
- McKinsey 2025: 88% use AI, but only **6% report 5%+ EBIT impact** from AI
- 39% report ANY measurable EBIT impact — meaning **61% see no bottom-line difference**
- BCG: "most enterprises aim too low with small pilots"; only the 6% redesigned workflows
- **The capex thesis requires the 94% to catch up to the 6%**, not just modest productivity gains
- Productivity gains visible at companies like Microsoft, Accenture, Goldman; not visible in median S&P 500 EBIT margins
→ **Claim → Evidence**: McKinsey State of AI 2025; BCG 2026 agents report; risk: 2026-2027 may be the inflection where the 94% catch up.

**O2. The capex-to-revenue ratio is unprecedented and partially circular.**
- $700B capex vs $150-200B revenue = **3.5-4.7x gap** for 2026
- Funded by debt: +$230B sector debt in 2026
- Free cash flow collapse: Amazon -95%, Alphabet -90% projected
- **Circular financing**: OpenAI is one of Azure's largest customers; Google Cloud has $460B in AI backlog; many AI startups' biggest expense is the hyperscaler cloud paid for by hyperscaler investment
- Capex/revenue ratio of 45-57% looks more like utilities or telecom — sectors with low ROE
- **Historical analog**: Telecom 2000-2002 (capex/revenue ratio similar), railroad 1880s
→ **Claim → Evidence**: CNBC tech-AI-cash; CreditSights; Allianz Research; risk: this time may genuinely be different given AI's strategic vs commodity nature.

## Explicit Unknowns

1. **Will Anthropic-style 30x revenue growth continue or saturate in 2027?** If the next 18 months adds another 5-10x, the math gap closes. If it slows to 2-3x, the gap widens.
2. **Will the 94% of enterprises catch up to the 6%?** The lag could be (a) early-cycle normal, or (b) genuine limit on AI's economic utility for most use cases.
3. **Will productivity gains show up in MACRO statistics (TFP, GDP per hour worked)?** As of 2026, the answer is "not yet visible at the aggregate level" — a meaningful caution flag.
4. **Are current LLM architectures hitting scaling limits?** Some signals from GPT-5/Claude 4 progression suggest diminishing returns per training-dollar; capex math depends on continued capability scaling.
5. **Will hyperscaler capex actually hit $700B+ in 2026, or will some pull back as gap widens?** Q3-Q4 2026 capex guidance revisions are the key tell.
6. **Coding revolution: does it generalize to other knowledge work, or is software special?** Code is *structured, verifiable, modular* — properties that don't apply to many other workflows.

---

# Section 3 — STEP 2 Strict Peer Review

## 3.1 Facts Still Needing Verification

| # | Claim | Best primary source |
|---|-------|---------------------|
| 1 | "Anthropic ARR $45B May 2026" | Anthropic IR / secondary market filings |
| 2 | "OpenAI ARR $33B Q2 2026" | OpenAI revenue press / SoftBank reporting |
| 3 | "Hyperscaler 2026 capex $700B+" | MSFT/GOOGL/AMZN/META latest Q1 2026 calls |
| 4 | "Memory companies all $1T+" | Bloomberg market data |
| 5 | "Microsoft 15M paid Copilot seats" | Microsoft Ignite / Q1'26 earnings |
| 6 | "Meta Advantage+ $60B ARR" | Meta Q4 2025 / Q1 2026 transcripts |
| 7 | "McKinsey 6% AI high performers" | McKinsey State of AI 2025 PDF direct |
| 8 | "GitHub Copilot 20M users" | GitHub Universe 2025/2026 |
| 9 | "FCF -95% at Amazon" | Amazon Q1 2026 10-Q |
| 10 | "$230B sector debt 2026" | CreditSights tech debt tracker |

## 3.2 Logical Leaps

1. **"Software engineering = revolution; everything else = augmentation"** — binary framing; reality is a spectrum. Customer service is being meaningfully restructured (significant headcount changes at e.g., Salesforce, Klarna). Could argue customer service is also "revolutionized".
2. **"Math gap of 3.5-4.7x is unsustainable"** — assumes 5-7 year amortization is required for justification. If GPU/asset lifespans extend (re-use across model generations) or if revenue compounds at 100%/yr, the gap could close.
3. **"Anthropic 30x growth scales to revolution"** — extrapolating from a 17-month period that includes coding-tool launch. Could be a one-time enterprise capture, not sustained.
4. **"Capex-revenue ratio looks like telecom/utilities"** — the analog isn't perfect; AI infrastructure has both networking (commodity) and strategic (cognitive) characteristics.
5. **"Only 6% high performers = mostly hype"** — same 6% statistic was true of early SaaS adoption in 2005-2010, which became universal by 2020. Inflection-point dynamics could repeat.

## 3.3 Missing Counterexamples

1. **Coding may NOT generalize**: code has unique properties (structured, verifiable, modular, syntactically constrained). The fact that AI works for code doesn't necessarily mean it'll work for legal briefs, financial analysis, or operations management.
2. **The "94% laggards" may include AI-skeptical industries (manufacturing, government, agriculture) that simply won't be AI-led**. The 6% being concentrated in tech/finance/consulting may be a feature, not a bug — and the absolute revenue from that 6% could be substantial.
3. **Productivity gains may be captured by employers**, not creating new revenue. If AI makes accountants 30% faster, firms may just hire 30% fewer accountants — that shows up in labor costs, not AI revenue.
4. **Energy bottleneck**: hyperscaler capex now constrained by power availability, not chip availability. This could naturally slow capex even if revenue keeps growing — reducing the gap from the supply side.
5. **AGI / scaling-law uncertainty**: if AI capability plateaus (GPT-6 not meaningfully better than GPT-5), the entire revenue thesis weakens. If it accelerates (genuine AGI), entire industries get displaced and revenue catches up.
6. **Compute prices falling**: GPU lifespan, model efficiency, and inference cost-per-token are all improving 2-4x/year. The "same dollar of capex" produces more output each year.

## 3.4 Most Important Primary Sources to Add

1. McKinsey State of AI 2025 PDF (direct, not summaries)
2. BCG AI Maturity Survey 2026 (full report)
3. Anthropic latest funding deck / IPO S-1 (when filed)
4. OpenAI revenue confirmed numbers (SoftBank / Microsoft cross-check)
5. Hyperscaler Q1 2026 earnings call transcripts (capex guidance)
6. GitHub Octoverse 2026 (developer metrics)
7. Federal Reserve TFP / productivity data 2024-2026
8. SemiAnalysis HBM market reports
9. Allianz / CreditSights AI capex sustainability papers
10. Independent academic studies on coding-tool productivity (CACM article)

## 3.5 Sentences That Remain Speculation

| # | Statement | Status |
|---|-----------|--------|
| 1 | "The 2026-2028 window will reveal whether revenue scales into capex" | **Conditional forecast** |
| 2 | "Anthropic 30x growth, if it continues, scales into capex within 2-3 years" | **Linear extrapolation** |
| 3 | "Only 6% are AI high performers means revolution hasn't broadly arrived" | **Interpretive claim** |
| 4 | "Capex-revenue ratio is unsustainable" | **Depends on amortization period + growth rate assumptions** |
| 5 | "Coding may not generalize to other knowledge work" | **Untested hypothesis** |
| 6 | "Software engineering is the only fully revolutionized category" | **Pattern recognition; arguable cutoffs** |
| 7 | "Meta AI lift = several percentage points of ad rev" | **Estimated from disclosed metrics** |
| 8 | "$1.2T cumulative capex" | **Summed from individual disclosures** |
| 9 | "Free cash flow -95% at Amazon" | **Quarterly figure; could revert** |
| 10 | "2027 is inflection point" | **Subjective forecast** |

---

# Section 4 — Honest Synthesis + Open Debate

## What the data actually tells us

**The bull case (steelmanned)**:
- Revenue IS scaling at unprecedented speeds (Anthropic 30x in 17 months — no SaaS company has done this)
- Coding-tool revolution proves the technology can transform knowledge work — it's a question of breadth, not capability
- Meta's $60B+ AI-driven ad ARR shows hyperscalers are recouping AI investment within their own businesses, not just selling to startups
- Memory/Nvidia margins look bubbly only if AI capability plateaus; if it keeps scaling, supplier oligopolies could persist 5-10 more years
- 6% of enterprises being "AI high performers" in mid-2026 looks like 6% being "SaaS-native" was in 2008 — early-cycle, not end-state
- AI infrastructure has 5-7 year amortization; comparing 1-year capex to 1-year revenue understates true economics

**The bear case (steelmanned)**:
- $1.2T cumulative capex vs $150-200B annualized revenue = math doesn't work without 5x revenue growth from here
- Funded increasingly by debt; FCF collapsing
- Circular financing (OpenAI → Microsoft → Azure → ...) inflates apparent revenue
- 94% of enterprises not benefiting suggests AI may be more like CRM (helpful tool) than electricity (general-purpose transformation)
- Macro productivity stats don't show AI dividend yet (concerning given the scale of investment)
- Coding-tool success doesn't generalize: code is uniquely structured
- Historical analogs (telecom 2000-02, railroad 1880s) ended badly despite real long-term utility

**My honest synthesis**:

The user's framing — *"trillion-dollar memory companies + Nvidia took the profit; actual AI usage is limited"* — captures the **balance-sheet truth** of mid-2026 but understates the **growth derivative**. The pure-play AI revenue growth (100-300%/yr) is structurally different from past tech bubbles where revenue growth slowed BEFORE the capex slowed (telecom 2001, internet 2000). Here, **revenue growth is still accelerating in mid-2026**. That said, **the math gap is genuinely unsustainable as a 3-year trajectory** — if revenue doesn't 3-5x from here by 2028, expect capex pullback and supplier-stock multiple compression.

**The single most important question**: *Will the AI-coding pattern (genuine 50% productivity gains, broad adoption) replicate in 2-3 other major knowledge-work categories by 2028?* If yes — full revolution, capex justified, supplier oligopolies durable. If no — partial revolution like internet (real but narrower than hype), capex pullback, supplier multiple compression but underlying technology persists.

**Bull/bear handicap (subjective)**: 55% bull, 35% middle, 10% bear. The Anthropic 30x growth is the single biggest argument against the bear case — that pace doesn't happen in fake revolutions.

## What I'd debate with you

1. **You said "AI actual usage is still quite limited"** — I'd push back. 900M weekly ChatGPT users + 20M Copilot seats + 70% of F100 using Anthropic = **NOT limited usage**. What IS limited is *broad enterprise EBIT impact* (only 6% see >5%). Usage ≠ economic transformation. Maybe the distinction you mean is "transformation"?
2. **You attributed the value capture to Mag7 → Nvidia → memory/components — true, but you might be UNDERVALUING the Meta AI advertising contribution**. Meta's $60B+ Advantage+ ARR and 24% YoY ad growth is AI value that *doesn't show up as separate AI revenue* — it shows up as core business revenue lift. The same is happening more subtly at Google and Amazon.
3. **You implied this is one-way circular** — but Anthropic just had its first profitable quarter and is at $45B ARR. That's not a hyperscaler subsidy; that's real customer payment by 70% of Fortune 100. The circularity argument was strong in 2023-2024; it's weakening fast.
4. **Where I 100% agree with you**: the trillion-dollar memory market caps look stretched relative to the "revolutionized" footprint. If I had to short something here, it would be memory at the next sign of capex moderation — historically the most cyclical part of the value chain.

## Open questions I'd find genuinely uncertain

- Is Anthropic's growth coding-driven (saturable) or general-knowledge-work-driven (durable)?
- Will Microsoft Copilot's 15M paid seats grow to 100M+ by 2027, or stall?
- Does Meta's AI-ads moat solidify (becomes irreplaceable) or commoditize (every ad network adopts similar tech)?
- What's the actual lifespan of an H100/B200 — 3 years or 6+? Material to capex amortization math.
- Will physical AI (robotics, autonomous vehicles) ramp in 2026-2028 to add another demand vector for compute?

---

## Primary Sources

### Capex
1. Visual Capitalist — *The Rise of AI Hyperscaler Spending*: https://www.visualcapitalist.com/the-rise-of-ai-hyperscaler-spending/
2. CNBC — *How much Google, Meta, Amazon and Microsoft are spending on AI*: https://www.cnbc.com/2025/10/31/tech-ai-google-meta-amazon-microsoft-spend.html
3. CNBC — *Tech AI spending approaches $700 billion in 2026, cash taking ...*: https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html
4. AI Certs — *Hyperscaler Capex Surge Redefines 2026 Budgets*: https://www.aicerts.ai/news/hyperscaler-capex-surge-redefines-2026-budgets/
5. Allianz Research — *AI capex cycle: war-proof for now*: https://www.allianz.com/content/dam/onemarketing/azcom/Allianz_com/economic-research/publications/specials/en/2026/march/2026_03_25_AI.pdf
6. CreditSights — *Hyperscaler Capex 2026 Estimates*: https://know.creditsights.com/insights/technology-hyperscaler-capex-2026-estimates/
7. Futurum — *AI Capex 2026: The $690B Infrastructure Sprint*: https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/
8. Introl — *Hyperscaler CapEx Hits $600B in 2026*: https://introl.com/blog/hyperscaler-capex-600b-2026-ai-infrastructure-debt-january-2026

### Memory / HBM trillion-dollar club
9. Morningstar — *SK Hynix, Micron Join Trillion-Dollar Club*: https://www.morningstar.com/news/dow-jones/202605271274/sk-hynix-micron-join-trillion-dollar-club-update
10. US News — *SK Hynix Joins $1 Trillion Club After Samsung, Micron on AI Chip Boom*: https://money.usnews.com/investing/news/articles/2026-05-26/sk-hynix-joins-1-trillion-club-after-samsung-micron-on-ai-chip-boom
11. AlphaPilot — *Micron and SK Hynix Join Trillion-Dollar Club*: https://www.alphapilot.tech/discover/micron-and-sk-hynix-join-trillion-dollar-club-as-ai-memory-demand-surges
12. CurrentAffair — *HBM Memory Chip Supercycle 2026*: https://www.currentaffair.today/blog/finance-9/hbm-memory-chip-supercycle-2026-how-sk-hynix-micron-and-samsung-formed-the-newest-1-trillion-club-747
13. KoreaInvestInsights — *SK Hynix HBM Market Share 2026*: https://koreainvestinsights.com/post/sk-hynix-hbm-market-share-ai-memory-demand-2026/
14. MomoView — *HBM Three-Way War*: https://momoview.com/blog/en/posts/hbm-industry-analysis-sk-hynix-samsung-micron-2026-ai-memory-supercycle-investment-thesis/

### AI software revenue
15. OpenTools — *Anthropic Revenue Hits $45B ARR*: https://opentools.ai/news/anthropic-revenue-surpasses-openai
16. NerdLevelTech — *Anthropic $30B ARR How Claude Overtook OpenAI*: https://nerdleveltech.com/anthropic-30-billion-arr-surpasses-openai
17. IDLEN — *Anthropic Passes OpenAI October 2026 IPO*: https://www.idlen.io/news/anthropic-overtakes-openai-30-billion-revenue-april-2026/

### Productivity / ROI
18. McKinsey — *State of AI 2025 PDF*: https://www.mckinsey.com/~/media/mckinsey/business%20functions/quantumblack/our%20insights/the%20state%20of%20ai/november%202025/the-state-of-ai-2025-agents-innovation_cmyk-v1.pdf
19. BCG via n5r — *AI Agents Deliver 30-90% ROI Gains*: https://n5r.com/en-us/blog/bcg-ai-agents-mcp-a2a-enterprise-roi-agent-economy
20. Welcome.ai — *AI Adoption Insights from McKinsey's 2025 Global Survey*: https://www.welcome.ai/content/ai-adoption-insights-from-mckinseys-2025-global-survey
21. Punku — *State of AI 2025: 78% Adoption, 74% See ROI*: https://www.punku.ai/blog/state-of-ai-2024-enterprise-adoption

### Coding tool revolution
22. GitHub — *Quantifying Copilot impact in enterprise with Accenture*: https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/
23. SecondTalent — *GitHub Copilot Statistics & Adoption Trends*: https://www.secondtalent.com/resources/github-copilot-statistics/
24. JetBrains — *Which AI Coding Tools Do Developers Actually Use at Work?* (Apr 2026): https://blog.jetbrains.com/research/2026/04/which-ai-coding-tools-do-developers-actually-use-at-work/
25. CACM — *Measuring GitHub Copilot's Impact on Productivity*: https://cacm.acm.org/research/measuring-github-copilots-impact-on-productivity/

### Meta AI advertising
26. PPC Land — *Meta's ad business hits record $58B as AI drives conversion gains*: https://ppc.land/metas-ad-business-hits-record-58b-as-ai-drives-conversion-gains/
27. FifthPerson — *Meta Q4 2025: AI driving engagement, ads and growth*: https://fifthperson.com/meta-q4-2025/
28. Facebook About — *2026: AI Drives Performance*: https://about.fb.com/news/2026/01/2026-ai-drives-performance/

### Bubble / circular financing
29. AI2.Work — *Hyperscalers Pledge $725B in AI Capex While Revenue Returns Lag Behind*: https://ai2.work/blog/hyperscalers-pledge-725b-in-ai-capex-while-revenue-returns-lag-behind
30. Cresset — *2026 Outlook: Is AI a Bubble?*: https://cressetcapital.com/articles/market-update/market-update-12-17-25-2026-outlook-is-ai-a-bubble/
31. PAASA — *AI Infrastructure Investing: How Hyperscaler Capex is Collapsing Free Cash Flow*: https://paasa.com/blog/ai-capex-supercycle

### Microsoft Copilot adoption
32. Stackmatix — *Microsoft Copilot Adoption Statistics & Trends 2026*: https://www.stackmatix.com/blog/copilot-market-adoption-trends
33. EPC Group — *Microsoft Copilot vs Google Gemini Enterprise Comparison 2026*: https://www.epcgroup.net/microsoft-copilot-vs-google-gemini-enterprise-comparison

---

*Generated using the Two-Step Research Protocol. **Not investment advice.** Personal view: 55% bull / 35% middle / 10% bear on whether the current AI capex super-cycle proves justified by revenue scaling 2026-2028. Open to update on new data.*

---

*Companion 中文版: [report_cn](report_cn)*

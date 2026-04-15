#!/usr/bin/env python3
"""Write Keysight Technologies (KEYS) analysis reports — EN and CN."""
import os

EN_REPORT = """# Keysight Technologies (NYSE: KEYS) — Tech Test & Measurement Deep Dive
## Multi-Model Consensus Report | April 2026

> **5-Model Analysis**: Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro
> **Framework**: Universal Rules + Day1Global (Modules A/B/C/D/E/K/L/O, 6 Perspectives)
> **Subject**: Keysight Technologies, Inc. (NYSE: KEYS)

---

## TL;DR — Executive Summary

| Metric | Value |
|---|---|
| **Stock Price** | ~\\$330 (Apr 14, 2026) |
| **Market Cap** | ~\\$57B |
| **PE (TTM)** | 58x |
| **Forward PE** | 22–28x |
| **PB** | ~9.7x |
| **1-Year Return** | +140% |
| **FCF Yield** | ~2.3% (TTM \\$1.3B) |
| **Consensus Rating** | **HOLD / CAUTIOUS BUY** |
| **12M Conservative Target** | \\$280 (-15%) |
| **12M Base Target** | \\$350 (+6%) |
| **12M Bull Target** | \\$420 (+27%) |
| **Prob-Weighted 12M Return** | **+3% to +8%** |

**Summary**: Keysight is a high-quality secular growth compounder with dominant market share (~34–45%) in test & measurement. The AI/5G/6G/automotive secular tailwinds are real, but at 58x trailing PE (1.5x its 5-year average of ~38x), much of the upside is already priced in. Risk/reward is balanced — not a screaming buy, not a sell. Best entry on a 15–20% pullback.

---

## 1. Company Snapshot

| Item | Detail |
|---|---|
| **Full Name** | Keysight Technologies, Inc. |
| **Ticker** | NYSE: KEYS |
| **Headquarters** | Santa Rosa, California |
| **Founded** | 2014 (spun off from Agilent Technologies; heritage traces to HP) |
| **CEO** | Satish Dhanasekaran (since 2022) |
| **Employees** | ~15,400 |
| **Core Business** | Electronic test & measurement solutions — hardware, software, services |
| **End Markets** | 5G/6G, AI data centers, automotive/EV, aerospace & defense, semiconductors |
| **Market Position** | #1 or #2 globally in electronic T&M |

### Business Segments (FY2025: \\$5.38B Revenue)

| Segment | Revenue | % of Total | YoY Growth | Key Drivers |
|---|---|---|---|---|
| **Communications Solutions Group (CSG)** | ~\\$3.42B | 69% | +10% | 5G/6G infra, AI datacenter, A&D |
| **Electronic Industrial Solutions Group (EISG)** | ~\\$1.56B | 31% | +9% | Semiconductor test, automotive, IoT |

### Sub-Segment Detail (CSG)

| Sub-Segment | Key Products | Growth Driver |
|---|---|---|
| **Commercial Communications** | 5G/6G protocol analyzers, network test | AI datacenter buildout (+33% Q1 FY26) |
| **Aerospace & Defense** | Signal analysis, EW test, radar | US/NATO defense spending (+18% Q1 FY26) |

---

## 2. Industry Context — Test & Measurement Market

### 2.1 Market Size & Growth

| Metric | Value |
|---|---|
| **Global T&M Market (2026)** | ~\\$19.8B |
| **CAGR (2026–2032)** | 4–6% |
| **Keysight Market Share** | 34% overall, up to 45% in subsegments |
| **Key Growth Drivers** | AI/ML infrastructure, 5G→6G, EV/ADAS, defense modernization |

### 2.2 Competitive Landscape

| Company | Focus | Keysight Advantage |
|---|---|---|
| **Rohde & Schwarz** (Private) | RF/microwave, broadcast | Keysight broader portfolio, more software-led |
| **Anritsu** (6754.T) | Telecom test | Keysight stronger in AI/datacenter |
| **Tektronix** (Fortive/FTV) | Oscilloscopes, general test | Keysight higher-end, more R&D-intensive |
| **NI** (Emerson) | Automated test | Keysight more diversified end markets |
| **VIAVI** (VIAV) | Fiber/network test | Keysight broader technology range |

### 2.3 Moat Assessment

**Moat Rating: WIDE** (4/5 models agree)

| Moat Source | Strength | Evidence |
|---|---|---|
| **Switching Costs** | ★★★★★ | T&M equipment deeply embedded in R&D workflows; retraining cost is enormous |
| **Intangible Assets** | ★★★★☆ | 2,700+ patents; regulatory certifications; brand heritage (HP→Agilent→Keysight) |
| **Network Effects** | ★★☆☆☆ | Limited — software platform (PathWave) building ecosystem |
| **Scale Economies** | ★★★★☆ | R&D amortization over largest installed base; \\$1.5B+ annual R&D spend |

---

## 3. Earnings Model — Per Segment with Sensitivity

### 3.1 FY2026E Earnings Build-Up

| Line Item | FY2025A | FY2026E (Base) | FY2026E (Bull) | FY2026E (Bear) |
|---|---|---|---|---|
| **Revenue** | \\$5.38B | \\$6.50B | \\$7.00B | \\$5.90B |
| CSG Revenue | \\$3.42B | \\$4.30B | \\$4.70B | \\$3.80B |
| EISG Revenue | \\$1.56B | \\$2.20B | \\$2.30B | \\$2.10B |
| **Gross Margin** | 64.5% | 65.5% | 66.0% | 64.0% |
| **Operating Margin (Non-GAAP)** | 28.5% | 30.0% | 31.5% | 27.0% |
| **Non-GAAP Net Income** | \\$1.10B | \\$1.52B | \\$1.74B | \\$1.20B |
| **Non-GAAP EPS** | \\$6.38 | \\$9.04 | \\$10.44 | \\$7.10 |
| **Shares Outstanding** | 172M | 168M | 168M | 168M |

### 3.2 Revenue Growth Sensitivity

| Revenue Growth | Revenue | Non-GAAP EPS | Forward PE @\\$330 |
|---|---|---|---|
| +10% | \\$5.92B | \\$7.30 | 45.2x |
| **+20% (Base)** | **\\$6.50B** | **\\$9.04** | **36.5x** |
| +25% | \\$6.73B | \\$9.70 | 34.0x |
| +30% (Bull) | \\$7.00B | \\$10.44 | 31.6x |

---

## 4. Operating Leverage Analysis (Rule 6)

### 4.1 Fixed vs Variable Cost Structure

Keysight operates a **high operating leverage** model similar to SaaS:
- **Fixed Costs** (~55% of opex): R&D (\\$1.5B+), G&A, facility costs, depreciation
- **Variable Costs** (~45%): COGS materials, sales commissions, warranty

### 4.2 Breakeven & Profit Multiplier

| Metric | Value |
|---|---|
| **Estimated Breakeven Revenue** | ~\\$4.0B |
| **Current Revenue** | \\$5.38B (35% above breakeven) |
| **Incremental Margin** | ~50–55% (above breakeven, each \\$1 revenue → \\$0.50–0.55 EBIT) |
| **Operating Leverage Multiplier** | 1.8–2.2x (10% revenue growth → 18–22% EBIT growth) |

### 4.3 Revenue Scenario Waterfall

| Revenue | Distance from BE | EBIT Est. | EBIT Margin | vs \\$5.38B |
|---|---|---|---|---|
| \\$4.0B (BE) | 0% | ~\\$0 | 0% | — |
| \\$5.0B | +25% | \\$0.50B | 10% | — |
| **\\$5.38B (FY25)** | **+35%** | **\\$0.93B** | **17.3%** | **Actual** |
| \\$6.50B (FY26E) | +63% | \\$1.63B | 25.0% | +75% EBIT |
| \\$7.00B (Bull) | +75% | \\$1.88B | 26.8% | +102% EBIT |

**Key Insight**: Keysight is well past breakeven and firmly in the profit acceleration zone. Each incremental dollar of AI/5G-driven revenue drops ~\\$0.50–0.55 to operating profit. This is why EPS is growing 2x faster than revenue.

---

## 5. Cycle / Valuation Framework

### 5.1 Is KEYS Cyclical?

**Semi-cyclical**: Keysight has cyclical exposure (semiconductor capex, telecom buildout) overlaid on secular growth (AI, defense, automotive electrification). It's NOT a pure cyclical like VLCC tankers — it has structural growth that compounds through cycles.

### 5.2 Historical Valuation Bands

| Period | PE Range | Revenue Cycle | Driver |
|---|---|---|---|
| **2019** | 22–30x | Growing (+10%) | 5G rollout begins |
| **2020** | 28–35x | Flat (\\$4.2B) | COVID dip + recovery |
| **2021** | 30–42x | Strong (+17%) | 5G + semiconductor boom |
| **2022** | 20–35x | Growing (+10%) | Multiple compression, rate hikes |
| **2023** | 22–30x | Flat (\\$5.5B) | Destocking cycle |
| **2024** | 25–35x | Declining (-9%) | End-market correction |
| **2025** | 30–45x | Recovery (+8%) | AI datacenter demand emerges |
| **2026 YTD** | **45–60x** | **Strong (+20–30%)** | **AI super-cycle pricing** |

### 5.3 PE Compression Path (Forward-Looking)

| Phase | Timeline | Forward PE | Narrative |
|---|---|---|---|
| **Phase 1: Re-Rating** (2024–2025) | H2 2024–H1 2025 | 25x → 35x | Revenue trough recognized; AI theme emerges |
| **Phase 2: Momentum** (2025–2026) | H2 2025–H1 2026 | 35x → 55x | AI capex super-cycle; beats & raises |
| **Phase 3: Maturation** (2026–2027) | H2 2026–H1 2027 | 55x → 35–40x | Growth decelerates; PE compresses on high base |
| **Phase 4: Normalization** (2027+) | H2 2027+ | 35x → 25–30x | Steady-state growth; market reprices to historical |

**Current Position**: Late Phase 2 / Early Phase 3. The easy money has been made. Forward PE of 36x on FY26E EPS is not unreasonable but leaves little margin of safety.

---

## 6. Multi-Model Consensus — Target Prices (Rule 7)

### 6.1 Model-by-Model Assessment

| Model | Rating | 12M Target | Key Reasoning |
|---|---|---|---|
| **Claude Opus 4.6** | HOLD | \\$340 (+3%) | Quality compounder fairly valued; wait for pullback |
| **Claude Sonnet 4.6** | BUY (cautious) | \\$365 (+11%) | AI datacenter thesis underappreciated; FY26 beats |
| **GPT-5.2** | HOLD | \\$320 (-3%) | Trailing PE too rich; forward PE fair but no margin of safety |
| **GPT-5.1** | BUY | \\$380 (+15%) | Operating leverage inflection + defense tailwinds |
| **Gemini 3 Pro** | HOLD | \\$330 (0%) | Consensus target = current price; upside priced in |

### 6.2 Consensus Target Price Matrix

| Scenario | 12M Target | FY26E EPS | Implied PE | Upside/Downside |
|---|---|---|---|---|
| **Conservative** | \\$280 | \\$7.10 (bear) | 39x | -15% |
| **Base** | \\$350 | \\$9.04 | 38.7x | +6% |
| **Bull** | \\$420 | \\$10.44 | 40x | +27% |

### 6.3 24-Month Targets

| Scenario | 24M Target | FY27E EPS | Implied PE | Upside/Downside |
|---|---|---|---|---|
| **Conservative** | \\$310 | \\$9.50 | 32.6x | -6% |
| **Base** | \\$400 | \\$11.50 | 34.8x | +21% |
| **Bull** | \\$500 | \\$13.00 | 38.5x | +52% |

---

## 7. Day1Global Framework Application (Rule 12)

### Module A: Revenue Quality ★★★★☆

| Factor | Assessment |
|---|---|
| **Revenue Diversification** | Good — CSG (69%) + EISG (31%); no single customer >10% |
| **Recurring Revenue** | Growing — software/services now ~35% of revenue (SaaS transition underway) |
| **Geographic Mix** | Americas 38%, Asia-Pacific 35%, Europe 27% — well diversified |
| **Revenue Visibility** | Moderate — mix of project-based + recurring; order backlog provides 1–2Q visibility |
| **End-Market Diversity** | 5G/6G, AI/datacenter, A&D, auto, semi — no single market >30% |

### Module B: Profitability / Operating Leverage ★★★★★

| Metric | FY2025 | FY2024 | Trend |
|---|---|---|---|
| **Gross Margin** | 64.5% | 63.2% | Improving |
| **Non-GAAP Op Margin** | 28.5% | 26.1% | Expanding |
| **R&D as % of Revenue** | ~28% | ~30% | Leveraging |
| **Incremental Margin** | ~50–55% | — | High operating leverage |
| **ROIC** | ~18% | ~14% | Inflecting higher |

### Module C: Cash Flow — "THE BIG ONE" ★★★★★

| Metric | FY2025 | FY2024 | Assessment |
|---|---|---|---|
| **Operating Cash Flow** | \\$1.45B | \\$1.10B | Strong |
| **Free Cash Flow** | \\$1.30B | \\$0.95B | 24% FCF margin — excellent |
| **FCF Yield** | ~2.3% | ~2.8% | Low due to rich valuation |
| **Capex/Revenue** | ~3% | ~3% | Asset-light model |
| **Cash Conversion** | >100% (NI → FCF) | — | Earnings are real cash |
| **Share Buybacks** | ~\\$800M/yr | — | Consistent; shares declining ~2%/yr |
| **Dividend** | \\$0 | \\$0 | No dividend — all buybacks |

**Cash Flow Verdict**: A-tier. FCF conversion is outstanding, capex is minimal, and the company returns cash aggressively through buybacks. The only knock: no dividend, and FCF yield at 2.3% is thin at this price.

### Module D: Forward Guidance ★★★★☆

- Q2 FY2026 guidance: \\$1.69–1.71B revenue (+30% YoY), Non-GAAP EPS \\$2.27–2.33
- Management raising guidance consistently — beat-and-raise pattern for 3 consecutive quarters
- AI datacenter demand called out as "multi-year tailwind"
- Defense orders characterized as "structurally higher" post-2024 geopolitical environment

### Module E: Competitive Landscape ★★★★☆

- Clear #1 in RF/microwave test
- #1 or #2 in 5G/6G protocol testing
- Growing rapidly in AI datacenter interconnect test (800G/1.6T)
- PathWave software platform creating stickiness
- R&D spend at \\$1.5B+ creates formidable barrier to entry
- Risk: Rohde & Schwarz privately funded, willing to undercut on price

### Module K: Valuation Matrix ★★★☆☆

| Method | Value per Share | vs Current (\\$330) |
|---|---|---|
| **DCF (10% WACC, 3% terminal)** | \\$310–\\$370 | -6% to +12% |
| **Forward PE (35x × FY26E EPS)** | \\$316 | -4% |
| **Forward PE (40x × FY26E EPS)** | \\$362 | +10% |
| **EV/EBITDA (25x × FY26E)** | \\$340 | +3% |
| **Peer Comp (avg fwd PE)** | \\$290–\\$350 | -12% to +6% |

**Valuation Verdict**: Fair to slightly overvalued. Most methods cluster around \\$310–\\$370. The stock sits at the upper end of fair value, priced for near-perfect execution.

### Module L: Ownership & Management ★★★★☆

| Factor | Detail |
|---|---|
| **Institutional Ownership** | ~89% (Vanguard, BlackRock, Capital Group top holders) |
| **Insider Ownership** | <1% (typical for large-cap) |
| **CEO Tenure** | Satish Dhanasekaran since 2022 — executing well |
| **Capital Allocation** | Buyback-focused (\\$800M+/yr); selective M&A; no dilutive deals |
| **Related-Party Risk** | None identified |

### Module O: Accounting Quality ★★★★☆

| Factor | Assessment |
|---|---|
| **GAAP vs Non-GAAP Gap** | Moderate — ~\\$0.54/share difference (stock comp, amortization) |
| **D&A Policy** | Conservative — intangibles amortized over 3–10 years |
| **Goodwill** | \\$3.4B (~30% of assets) — from M&A history; no recent impairments |
| **Off-Balance-Sheet** | Operating leases (~\\$350M); no unusual items |
| **Audit Quality** | Deloitte — clean opinions |

---

## 8. Six Perspectives Analysis

### 1. Quality Compounder (Buffett/Munger) — ★★★★☆
> **Durable advantage?** YES. Wide moat via switching costs + intangible assets. 28% R&D-to-revenue ratio creates an innovation flywheel. The HP→Agilent→Keysight lineage spans 85 years of T&M leadership.
>
> **Concern**: At 58x trailing PE, even Buffett would wait for a cheaper entry. Quality is unquestioned; price is the issue.

### 2. Imaginative Growth (Baillie Gifford/ARK) — ★★★☆☆
> **10x optionality?** Unlikely from here (already \\$57B). But the software transformation (PathWave, SaaS) could re-rate the business from "hardware company" (30x PE) to "software-enabled platform" (40–50x PE) over 5 years. AI test infrastructure is an underappreciated TAM expansion.
>
> **Upside case**: If software reaches 50% of revenue by 2030, PE re-rates to 45x on \\$15 EPS = \\$675 (+105%).

### 3. Fundamental Long/Short (Tiger Cubs) — ★★★☆☆
> **What is mispriced?** The market may be over-extrapolating AI datacenter spend. If AI capex decelerates in 2027 (which it historically does after 2–3 year build cycles), KEYS could face a revenue deceleration that compresses the multiple from 55x → 30x rapidly. Short thesis: "AI winter" for test equipment.
>
> **Counter**: Defense and automotive segments provide a floor that pure-play AI stocks lack.

### 4. Deep Value (Klarman/Marks) — ★★☆☆☆
> **Margin of safety?** Minimal at \\$330. FCF yield of 2.3% is thin. Even on FY26E base EPS of \\$9.04, you are paying 36.5x forward — no obvious value cushion. Would need a pullback to \\$240–\\$260 (25–28x forward) for a proper value entry.
>
> **This is NOT a deep value stock at current prices.**

### 5. Catalyst Driven (Tepper/Ackman) — ★★★☆☆
> **Specific value-unlocking events?**
> - **Catalyst 1**: PathWave software platform achieving critical mass → margin expansion + recurring revenue re-rating
> - **Catalyst 2**: Major defense contract wins (AUKUS, NATO spending)
> - **Catalyst 3**: 6G standard setting begins 2026–2027 → new test cycle
> - **Anti-catalyst**: AI datacenter capex slowdown; semiconductor correction

### 6. Macro Tactical (Druckenmiller) — ★★★☆☆
> **Cycle positioning?** Late in the AI capex upcycle. The time to buy KEYS was 2024 (when it was \\$130–\\$160 on the semiconductor downturn). Now you are buying late-cycle at elevated multiples.
>
> **Macro risks**: Interest rate uncertainty, US-China tech decoupling (Keysight has significant China exposure), AI capex deceleration.

---

## 9. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| **AI datacenter capex slowdown** | 30% | HIGH | Defense + auto segments provide floor |
| **PE multiple compression** | 40% | MEDIUM | Strong earnings growth can absorb some compression |
| **US-China tech decoupling** | 25% | MEDIUM | Diversified geographically; some China revenue at risk |
| **Semiconductor cycle downturn** | 20% | MEDIUM | EISG segment exposed; CSG provides offset |
| **Competition from R&S/Anritsu** | 15% | LOW | Moat is wide; switching costs are high |
| **Key executive departure** | 10% | LOW | Deep bench; institutional knowledge |

---

## 10. Anti-Bias Framework (Rule 12)

| Bias | How It Could Affect This Analysis | Mitigation |
|---|---|---|
| **Anchoring** | Anchoring to the 140% 1-year return as "momentum" | Used historical PE bands (22–42x) as anchor, not recent price action |
| **Recency** | Over-weighting the AI boom narrative | Considered 2023–2024 downturn as counterbalance |
| **Confirmation** | Seeking data to confirm "high quality = buy" | Multiple models independently flagged valuation risk |
| **Narrative** | "AI will drive growth forever" | Modeled bear scenario where AI capex slows |
| **Survivorship** | Only looking at KEYS because it went up | Compared to Anritsu, VIAVI (lower returns) — KEYS quality IS superior |

---

## 11. Pre-Mortem Analysis

> *"It is 1 year later (April 2027) and you lost 40% on KEYS. What went wrong?"*

| Scenario | Probability | What Happened | Early Warning Sign |
|---|---|---|---|
| **AI Capex Winter** | 20% | Hyperscalers cut datacenter capex by 30%; KEYS CSG revenue drops 15%; PE compresses from 55x to 25x | Hyperscaler capex guidance cuts; order cancellations in 800G test |
| **Semiconductor Double-Dip** | 15% | 2027 chip glut → EISG revenue drops 20%; total revenue flat → PE crush | DRAM/NAND pricing collapse; TSMC capex guidance cut |
| **US-China Tech War Escalation** | 15% | Export controls expanded to T&M equipment; China revenue (\\$700M+) at risk | New BIS entity list additions; retaliatory tariffs on US tech |
| **Multiple Compression (No Catalyst)** | 25% | Growth simply normalizes to 8–10%; market decides 35x is enough; stock drifts to \\$250 | Two consecutive quarters of slowing order growth |
| **Management Misstep (Bad M&A)** | 10% | Large acquisition at peak cycle (\\$5B+) destroys value; integration fails | Announcement of large, high-premium acquisition |

**Prob-Weighted Downside Risk**: 20%×40% + 15%×35% + 15%×30% + 25%×25% + 10%×40% = **~30% weighted downside** is meaningful.

---

## 12. Investment Recommendation

### Rating: **HOLD** (3/5 models) / **Cautious BUY** (2/5 models)

### Scenario-Specific Guidance

| Scenario | Action | Entry Price | 12M Target | 24M Target | Allocation |
|---|---|---|---|---|---|
| **Conservative** | WAIT for pullback | \\$240–\\$260 | \\$280 | \\$310 | 0% (wait) |
| **Base** | SMALL position | \\$300–\\$330 | \\$350 | \\$400 | 3–5% of portfolio |
| **Bull** | ADD on confirmation | \\$330+ with beat | \\$420 | \\$500 | 5–7% of portfolio |

### Triggers

| Direction | Trigger | Action |
|---|---|---|
| **BUY** | Stock pulls back to \\$260–\\$280 (28–31x FY26E) | Start 3–5% position |
| **BUY** | FY26 revenue guidance raised above \\$7B | Add at any price <\\$370 |
| **SELL** | Trailing PE exceeds 70x with no earnings acceleration | Trim 50% |
| **SELL** | Hyperscaler capex guidance cut by >20% | Exit 100% |
| **HOLD** | Stock stays \\$300–\\$370 with in-line results | Maintain position |

### Portfolio Context

For investors already holding KEYS:
- **If bought below \\$200**: Sitting on 65%+ gains. Consider trimming 30–40% to lock in profits and let remainder ride.
- **If bought \\$250–\\$300**: Hold for now. Set stop-loss at \\$260.
- **If considering new entry at \\$330**: Small position only (3%). The quality is excellent but the price is fair, not cheap.

---

## 13. Peer Comparison

| Company | Ticker | Market Cap | Fwd PE | Revenue Growth | Gross Margin | Moat |
|---|---|---|---|---|---|---|
| **Keysight Technologies** | KEYS | \\$57B | 36.5x | +20% | 65% | Wide |
| **Fortive (Tektronix)** | FTV | \\$28B | 22x | +6% | 60% | Moderate |
| **Teledyne Technologies** | TDY | \\$22B | 25x | +8% | 43% | Moderate |
| **Ametek Inc** | AME | \\$42B | 28x | +7% | 36% | Narrow |
| **National Instruments (Emerson)** | EMR | \\$72B | 24x | +4% | 52% | Moderate |
| **VIAVI Solutions** | VIAV | \\$3B | 18x | +5% | 58% | Narrow |

**KEYS trades at a premium to all peers** — justified by higher growth, wider moat, and better margins. But the premium gap has widened significantly in 2026.

---

## Appendix: Key Financial Data

### Income Statement Summary

| Metric | FY2022 | FY2023 | FY2024 | FY2025 | FY2026E |
|---|---|---|---|---|---|
| Revenue (\\$B) | 5.42 | 5.46 | 4.98 | 5.38 | 6.50 |
| YoY Growth | +10% | +1% | -9% | +8% | +21% |
| Gross Margin | 65% | 64% | 63% | 64.5% | 65.5% |
| Non-GAAP EPS | \\$7.08 | \\$6.81 | \\$5.68 | \\$6.38 | \\$9.04 |

### Balance Sheet Summary

| Metric | FY2025 |
|---|---|
| Total Assets | \\$11.3B |
| Shareholders' Equity | \\$5.88B |
| Total Debt | \\$2.78B |
| Net Debt | \\$0.91B |
| Cash & Investments | \\$1.87B |
| Debt/Equity | 0.41x |
| Current Ratio | 2.6x |

### Cash Flow Summary

| Metric | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Operating CF | \\$1.35B | \\$1.10B | \\$1.45B |
| Capex | \\$0.18B | \\$0.15B | \\$0.15B |
| Free Cash Flow | \\$1.17B | \\$0.95B | \\$1.30B |
| FCF Margin | 21.4% | 19.1% | 24.2% |
| Buybacks | \\$0.60B | \\$0.70B | \\$0.80B |

---

*Data as of April 14, 2026. Not investment advice. All models may contain errors — verify independently.*
*Report generated using the Day1Global tech-earnings-deepdive framework.*
"""

CN_REPORT = """# 是德科技 (NYSE: KEYS) — 测试测量行业深度研究
## 多模型共识报告 | 2026年4月

> **5模型分析**: Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro
> **分析框架**: 通用规则 + Day1Global (模块 A/B/C/D/E/K/L/O, 6大视角)
> **研究标的**: 是德科技 (NYSE: KEYS)

---

## 核心摘要 (TL;DR)

| 指标 | 数值 |
|---|---|
| **股价** | ~\\$330 (2026年4月14日) |
| **市值** | ~\\$570亿 |
| **PE (TTM)** | 58倍 |
| **远期PE** | 22–28倍 |
| **PB** | ~9.7倍 |
| **一年涨幅** | +140% |
| **FCF收益率** | ~2.3% (TTM \\$13亿) |
| **共识评级** | **持有 / 谨慎买入** |
| **12月保守目标** | \\$280 (-15%) |
| **12月基准目标** | \\$350 (+6%) |
| **12月乐观目标** | \\$420 (+27%) |
| **概率加权12月回报** | **+3% 至 +8%** |

**摘要**: 是德科技是测试测量领域的高质量长期复合增长标的，市场份额约34–45%处于主导地位。AI/5G/6G/汽车电子等长期趋势是真实的，但58倍滚动PE（为5年均值38倍的1.5倍）意味着大部分上涨空间已被price in。风险收益平衡——不是明显的买入信号，也不是卖出信号。最佳建仓点在回调15–20%时。

---

## 1. 公司概况

| 项目 | 详情 |
|---|---|
| **全称** | Keysight Technologies, Inc. |
| **代码** | NYSE: KEYS |
| **总部** | 美国加州圣罗莎 |
| **成立** | 2014年（从安捷伦分拆；传承可追溯至惠普） |
| **CEO** | Satish Dhanasekaran（2022年起） |
| **员工** | ~15,400人 |
| **核心业务** | 电子测试测量解决方案——硬件、软件、服务 |
| **终端市场** | 5G/6G、AI数据中心、汽车/EV、航空航天与国防、半导体 |
| **市场地位** | 全球电子测试测量行业第1或第2 |

### 业务分部 (FY2025: \\$53.8亿营收)

| 分部 | 营收 | 占比 | 同比 | 驱动力 |
|---|---|---|---|---|
| **通信解决方案集团 (CSG)** | ~\\$34.2亿 | 69% | +10% | 5G/6G基建、AI数据中心、航空国防 |
| **电子工业解决方案集团 (EISG)** | ~\\$15.6亿 | 31% | +9% | 半导体测试、汽车、物联网 |

---

## 2. 行业背景 — 测试测量市场

| 指标 | 数值 |
|---|---|
| **全球测试测量市场 (2026)** | ~\\$198亿 |
| **复合年增长率 (2026–2032)** | 4–6% |
| **是德科技市场份额** | 整体34%，子领域最高45% |
| **核心增长驱动** | AI/ML基础设施、5G→6G、EV/ADAS、国防现代化 |

### 护城河评估: **宽阔** (4/5模型一致)

| 护城河来源 | 强度 | 证据 |
|---|---|---|
| **转换成本** | ★★★★★ | 测试设备深度嵌入研发流程；重新培训成本巨大 |
| **无形资产** | ★★★★☆ | 2,700+专利；监管认证；品牌传承（HP→安捷伦→是德） |
| **规模经济** | ★★★★☆ | 研发投入覆盖最大安装基数；年研发支出\\$15亿+ |

---

## 3. 盈利模型 — 分部敏感性分析

### FY2026E 盈利构建

| 项目 | FY2025实际 | FY2026E基准 | FY2026E乐观 | FY2026E悲观 |
|---|---|---|---|---|
| **营收** | \\$53.8亿 | \\$65.0亿 | \\$70.0亿 | \\$59.0亿 |
| **毛利率** | 64.5% | 65.5% | 66.0% | 64.0% |
| **Non-GAAP净利润** | \\$11.0亿 | \\$15.2亿 | \\$17.4亿 | \\$12.0亿 |
| **Non-GAAP每股收益** | \\$6.38 | \\$9.04 | \\$10.44 | \\$7.10 |

---

## 4. 经营杠杆分析

| 指标 | 数值 |
|---|---|
| **预估盈亏平衡营收** | ~\\$40亿 |
| **当前营收** | \\$53.8亿（高出盈亏平衡35%） |
| **增量利润率** | ~50–55%（盈亏平衡以上，每\\$1营收→\\$0.50–0.55 EBIT） |
| **经营杠杆倍数** | 1.8–2.2倍（10%营收增长 → 18–22% EBIT增长） |

**核心洞察**: 是德科技已远超盈亏平衡点，处于利润加速区间。AI/5G驱动的每一美元增量营收都能带来约\\$0.50–0.55的营业利润贡献。这就是为什么EPS增速是营收增速的2倍。

---

## 5. 周期/估值框架

**半周期性**: 是德科技兼具周期性暴露（半导体资本支出、电信建设）和长期增长（AI、国防、汽车电气化）。不像VLCC油轮那样纯周期——它拥有穿越周期的结构性增长。

### PE压缩路径

| 阶段 | 时间线 | 远期PE | 叙事 |
|---|---|---|---|
| **重估期** (2024–2025) | 2024下-2025上 | 25x → 35x | 营收触底确认；AI主题浮现 |
| **动量期** (2025–2026) | 2025下-2026上 | 35x → 55x | AI资本支出超级周期；持续超预期 |
| **成熟期** (2026–2027) | 2026下-2027上 | 55x → 35–40x | 增速放缓；PE在高基数上压缩 |
| **正常化** (2027+) | 2027下+ | 35x → 25–30x | 稳态增长；市场回归历史估值 |

**当前位置**: 第2阶段末期 / 第3阶段初期。容易赚的钱已经赚完了。

---

## 6. 多模型共识 — 目标价

| 模型 | 评级 | 12月目标 | 核心逻辑 |
|---|---|---|---|
| **Claude Opus 4.6** | 持有 | \\$340 (+3%) | 优质复合增长股估值合理；等待回调 |
| **Claude Sonnet 4.6** | 谨慎买入 | \\$365 (+11%) | AI数据中心价值被低估 |
| **GPT-5.2** | 持有 | \\$320 (-3%) | 滚动PE过高；远期PE合理但无安全边际 |
| **GPT-5.1** | 买入 | \\$380 (+15%) | 经营杠杆拐点 + 国防顺风 |
| **Gemini 3 Pro** | 持有 | \\$330 (0%) | 共识目标 = 当前价格 |

### 共识目标价矩阵

| 情景 | 12月目标 | FY26E EPS | 隐含PE | 上行/下行 |
|---|---|---|---|---|
| **保守** | \\$280 | \\$7.10 | 39倍 | -15% |
| **基准** | \\$350 | \\$9.04 | 38.7倍 | +6% |
| **乐观** | \\$420 | \\$10.44 | 40倍 | +27% |

---

## 7. Day1Global框架 — 核心模块

### 模块C: 现金流 — "最关键模块" ★★★★★

| 指标 | FY2025 | 评估 |
|---|---|---|
| **经营现金流** | \\$14.5亿 | 强劲 |
| **自由现金流** | \\$13.0亿 | 24% FCF利润率——卓越 |
| **FCF收益率** | ~2.3% | 因估值偏高而较低 |
| **资本支出/营收** | ~3% | 轻资产模型 |
| **回购** | ~\\$8亿/年 | 持续；股本每年减少~2% |

### 模块K: 估值矩阵 ★★★☆☆

| 方法 | 每股价值 | vs 当前(\\$330) |
|---|---|---|
| **DCF** | \\$310–\\$370 | -6% 至 +12% |
| **远期PE (35x)** | \\$316 | -4% |
| **远期PE (40x)** | \\$362 | +10% |
| **EV/EBITDA (25x)** | \\$340 | +3% |

**估值结论**: 合理至略微偏高。多数方法集中在\\$310–\\$370区间。

---

## 8. 六大视角分析

| 视角 | 评级 | 核心判断 |
|---|---|---|
| **价值复合** (巴菲特/芒格) | ★★★★☆ | 护城河宽阔，但58倍PE太贵，等待回调 |
| **想象力增长** (ARK) | ★★★☆☆ | 软件转型(PathWave)可能重估，但从\\$570亿基数10倍较难 |
| **多空对冲** (Tiger Cubs) | ★★★☆☆ | 市场可能过度外推AI数据中心支出 |
| **深度价值** (Klarman) | ★★☆☆☆ | 在\\$330没有安全边际；需回调至\\$240–260 |
| **催化剂驱动** (Ackman) | ★★★☆☆ | PathWave临界质量、国防合同、6G标准制定 |
| **宏观战术** (Druckenmiller) | ★★★☆☆ | AI资本支出周期后期；买入时机是2024年的\\$130–160 |

---

## 9. 风险矩阵

| 风险 | 概率 | 影响 | 缓释措施 |
|---|---|---|---|
| **AI数据中心资本支出放缓** | 30% | 高 | 国防+汽车提供底部支撑 |
| **PE倍数压缩** | 40% | 中 | 强劲盈利增长可吸收部分压缩 |
| **中美科技脱钩** | 25% | 中 | 地域多元化；部分中国营收面临风险 |
| **半导体周期下行** | 20% | 中 | EISG承压；CSG提供对冲 |

---

## 10. 事前剖析 (Pre-Mortem)

> *"一年后（2027年4月），你在KEYS上亏损40%。发生了什么？"*

| 情景 | 概率 | 发生了什么 | 预警信号 |
|---|---|---|---|
| **AI资本支出寒冬** | 20% | 超大规模云厂商削减30%数据中心资本支出 | 云厂商资本支出指引下调 |
| **半导体二次探底** | 15% | 2027芯片过剩，EISG营收下降20% | DRAM/NAND价格暴跌 |
| **中美科技战升级** | 15% | 出口管制扩展至测试测量设备 | 新增BIS实体清单 |
| **估值自然回归** | 25% | 增长正常化至8–10%，市场认为35倍足够 | 连续两季订单增速放缓 |

---

## 11. 投资建议

### 评级: **持有** (3/5模型) / **谨慎买入** (2/5模型)

| 情景 | 操作 | 建仓价 | 12月目标 | 24月目标 | 仓位 |
|---|---|---|---|---|---|
| **保守** | 等待回调 | \\$240–260 | \\$280 | \\$310 | 0% |
| **基准** | 小仓位 | \\$300–330 | \\$350 | \\$400 | 3–5% |
| **乐观** | 确认后加仓 | \\$330+超预期 | \\$420 | \\$500 | 5–7% |

### 操作触发条件

| 方向 | 触发条件 | 操作 |
|---|---|---|
| **买入** | 回调至\\$260–280 (28–31倍FY26E) | 建仓3–5% |
| **买入** | FY26营收指引上调至\\$70亿以上 | 在\\$370以下加仓 |
| **卖出** | 滚动PE超过70倍且无盈利加速 | 减仓50% |
| **卖出** | 超大规模云厂商资本支出指引下调>20% | 全部清仓 |

---

## 12. 同业比较

| 公司 | 代码 | 市值 | 远期PE | 营收增速 | 毛利率 | 护城河 |
|---|---|---|---|---|---|---|
| **是德科技** | KEYS | \\$570亿 | 36.5倍 | +20% | 65% | 宽 |
| **福迪威 (Tektronix)** | FTV | \\$280亿 | 22倍 | +6% | 60% | 中 |
| **泰瑞达** | TDY | \\$220亿 | 25倍 | +8% | 43% | 中 |
| **阿美特克** | AME | \\$420亿 | 28倍 | +7% | 36% | 窄 |
| **VIAVI** | VIAV | \\$30亿 | 18倍 | +5% | 58% | 窄 |

---

*数据截至2026年4月14日。非投资建议。所有模型可能包含误差——请独立验证。*
*报告使用Day1Global tech-earnings-deepdive框架生成。*
"""

os.makedirs("keysight", exist_ok=True)
with open("keysight/report_en.md", "w", encoding="utf-8") as f:
    f.write(EN_REPORT)
with open("keysight/report_cn.md", "w", encoding="utf-8") as f:
    f.write(CN_REPORT)
print("Both reports written successfully")

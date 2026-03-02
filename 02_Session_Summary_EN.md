# VLCC Cycle-Peak Valuation — Session Summary
## Date: March 2, 2026

> **Updated March 2, 2026** — Market caps refreshed: DHT $3.13B, FRO $8.50B

---

## What Was Done

### Objective
Perform a rigorous VLCC cycle-peak valuation backtest comparing **DHT Holdings (DHT)** and **Frontline (FRO)**, using multiple AI models to cross-validate results and reduce model bias.

### Methodology
1. Translated Chinese analysis prompt into English
2. Ran the same structured prompt across **5 AI models** in parallel:
   - Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro Preview
3. **Run 1 (Neutral)**: Historical-based framework — 2026–28 cycle positioned between 2008 and 2020
4. **Run 2 (Enhanced Bullish)**: Incorporated structural supply thesis — targets must EXCEED 2008 inflation-adjusted peaks
5. Compiled cross-model comparative report with consensus ranges
6. **Updated** with latest market caps (DHT $3.13B, FRO $8.50B) — recalculated all upside figures

### Key Parameters
- **Fleet conversion**: VLCC=1.0, Suezmax=0.5, Aframax/LR2=0.3
- **DHT**: 24 VLCCs → 24.0 VLCC-eq (pure play)
- **FRO**: 41V + 24S + 18A → 58.4 VLCC-eq (10–12% mix discount)
- **Current prices (Mar 2026)**: DHT $3.13B ($130M/eq), FRO $8.50B ($146M/eq)
- **CPI adjustment**: 2008→2026 ≈ 1.51×, 2020→2026 ≈ 1.27×

### Bullish Supply Thesis (Run 2)
- VLCC orderbook at historic lows — no deliveries until late 2028
- Sinokor locking up large VLCC capacity
- Shadow fleet (~100+ VLCCs) exiting due to sanctions enforcement
- Aging fleet + accelerating scrapping
- Robust Asian refinery demand

---

## Key Results (Updated for Current Prices)

### Consensus Targets (Average of 5 Models)

| Scenario | DHT Target | DHT Upside | FRO Target | FRO Upside |
|----------|----------:|----------:|-----------:|----------:|
| Conservative | $3.9B | **+23%** | $8.2B | **−4%** |
| Base | $5.0B | **+58%** | $10.4B | **+23%** |
| Bullish | $6.2B | **+99%** | $13.2B | **+55%** |

### Critical Shift: FRO Has Consumed Most of Its Upside
- FRO rallied **+89%** from $4.5B to $8.5B — consumed ~83% of base-case cycle upside
- DHT rallied **+49%** from $2.1B to $3.13B — consumed ~57% of base-case cycle upside
- **DHT now has 2.5× FRO's remaining upside (+58% vs +23%)**

### Model Agreement (Updated)
- **5/5 models**: DHT has more upside elasticity (unanimous — was 4/5 before)
- **5/5 models**: DHT has better risk-adjusted value (unanimous — was 3/5 before)
- FRO's conservative case is now **negative on average (−4%)**

### Final Verdict
- **DHT**: Strong Buy — +58% base upside, pure VLCC convexity, clear winner at current prices
- **FRO**: Fairly Valued — most of the easy money has been made, only attractive in bull case (+55%)

---

## Technical Notes

### Gemini 3 Pro Fix
- **Failed in Run 1**: Could not handle complex multi-tool orchestration (web search + reasoning)
- **Fixed in Run 2**: Provided all data directly in prompt with "do NOT use tools" instruction
- **Lesson**: Gemini 3 Pro works well for direct reasoning but struggles with agentic workflows

### Model Behavioral Differences
| Model | Aggressiveness | Tool Use | Strengths |
|-------|---------------|----------|-----------|
| Opus 4.6 | Moderate-high | Excellent multi-tool | Most thorough analysis, dual-price sensitivity |
| Sonnet 4.6 | Moderate | Good | Best structured math transparency |
| GPT-5.2 | Aggressive | Good | Boldest targets, supply-shock regime framing |
| GPT-5.1 | Moderate | Good | Most balanced bull/bear consideration |
| Gemini 3 Pro | Conservative | Poor (needs self-contained prompt) | Clean premium-to-peak framework |

---

## Files in This Folder
1. `01_Full_Report_EN.md` — Complete multi-model analysis (English)
2. `02_Session_Summary_EN.md` — This file: session summary for future reference
3. `03_Full_Report_CN.md` — Complete multi-model analysis (Chinese)
4. `04_Session_Summary_CN.md` — Session summary (Chinese)

---

*Updated March 2, 2026. Market caps: DHT $3.13B, FRO $8.50B. Not investment advice.*

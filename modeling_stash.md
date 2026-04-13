---
layout: default
title: Modeling Stash — Cyclical Valuation & Sell Signal Framework
---

# Modeling Stash: Cyclical Stock Valuation & Sell Signal Framework

**Working notes from VLCC investment analysis discussions**

*Last updated: April 13, 2026*

> ⚠️ **Disclaimer:** These are analytical frameworks under development, not investment advice. All models have limitations. Past performance does not predict future results. Always consult a qualified financial advisor.

---

## 1. DCF Rules for Cyclical Stocks ("三不准")

Standard DCF models are dangerous for cyclicals because they overvalue at peaks and undervalue at troughs. Three hard rules to prevent this:

### Rule 1: Terminal Growth Rate (永续g) ≤ Nominal GDP

| Stock Type | Terminal g | Rationale |
|:-----------|:---------:|:----------|
| Growth stock | 3-5% | Can grow faster than GDP for a while |
| Stable compounder | 2-3% | GDP-like |
| **Cyclical (shipping)** | **0-1%** | Fleet grows with trade but industry is zero-sum cyclical |
| Deep cyclical (mining) | 0% | Commodity price mean-reverts, no structural growth |

For VLCC companies: **g = 0-1%**. The global fleet grows ~1-2% per year with trade, but individual companies don't structurally grow — they cycle around a flat trend.

### Rule 2: Must Use 7-10 Year Smoothed FCF

**This is the single most important rule for shipping.** Using peak-year FCF in a DCF is the #1 mistake.

Three methods to calculate smoothed FCF, all should be run:

#### Method A: Simple Historical Average (backward-looking)

```
Take 7-10 years of actual FCF → average
Pro: Uses real data, no assumptions
Con: Penalized by trough years when fleet was smaller
```

#### Method B: Forward-Normalized (mid-cycle TCE × current fleet)

```
Mid-cycle TCE assumption × operating days × current fleet - opex - capex
Pro: Reflects current fleet size and mix
Con: Requires a "mid-cycle" TCE assumption (subjective)
```

For DHT (24 VLCCs, mid-cycle $90K TCE):
```
Revenue: $90K × 335 days × 24 ships = $723M
Opex:    ~$20K/day × 365 × 24       = ($175M)
D&A + capex (net):                    = ($100M)
Interest:                             = ($50M)
Tax:                                  = (~$0, Marshall Islands)
Smoothed FCF:                         ≈ $398M
```

#### Method C: Blend (weighted)

```
Weight recent fleet-adjusted FCF higher:
  50% × Method B (forward-normalized)
  30% × Method A (last 7yr average, fleet-adjusted)
  20% × Current year estimate (recognizes cycle position)
```

**Critical adjustment**: Supply tight through mid-2028, then normalizing. The mid-cycle TCE should reflect the 2026-2030 average, not the long-term 20-year average (which includes years with very different fleet dynamics).

### Rule 3: Discount Rate Linked to Risk

| Component | Base | DHT | FRO |
|:----------|:----:|:---:|:---:|
| Risk-free rate | 4.5% | 4.5% | 4.5% |
| Equity risk premium | 5.0% | 5.0% | 5.0% |
| **Base WACC** | **~9.5%** | **~9.5%** | **~9.5%** |
| High leverage premium | +2% if net debt/EBITDA > 3x | No (< 2x) | **+2%** (higher gearing) |
| Policy uncertainty | +1% or +2% | +1% (indirect sanctions) | +1% (indirect) |
| **Total discount rate** | | **~10.5-11.5%** | **~12.5-13.5%** |

Model BOTH +1% and +2% policy premium to see sensitivity:

| Discount Rate | DHT DCF/share (Method C, g=0.5%) | FRO DCF/share |
|:---:|:---:|:---:|
| 10.5% | ~$24 | ~$38 |
| 11.5% | ~$21 | ~$33 |
| 12.5% | ~$18 | ~$29 |
| 13.5% | ~$16 | ~$26 |

---

## 2. Dividend Yield Anchor (股息率锚)

### Buy Signal: Smoothed Dividend Yield ≥ 8%

**Hard floor — will not buy below 8% smoothed yield.**

Critical: use smoothed FCF to calculate yield, NOT current year.

| Stock | Current Price | Smoothed FCF/share | Smoothed Yield | **Signal** |
|:------|:---:|:---:|:---:|:---:|
| DHT | $17.46 | ~$2.47 (Method C) | **14.1%** | ✅ BUY (well above 8%) |
| FRO | $34.34 | ~$3.20 (Method C) | **9.3%** | ✅ BUY (above 8%) |

At $60-70K normalized post-2028 TCE, smoothed yields drop to 5-6% → would NOT trigger a new buy signal. This means: buy now during the structural window, but don't add at normalized rates.

---

## 3. Sell Signals — The Hard Part

### Why Standard PE Sell Rules Don't Work for Cyclicals

The investor's original framework: "sell at PE > 25x." This is a growth-stock rule. For cyclicals:

```
Growth stock:    LOW PE = cheap = BUY    HIGH PE = expensive = SELL
Cyclical stock:  LOW PE = peak earnings  HIGH PE = trough earnings

FRO at PE 1.67 (Q3 2020) = peak earnings → stock FELL 25% in 6 months
FRO at PE 22x  (Q2 2022) = trough earnings → stock RALLIED 4x in 18 months
```

**In shipping, PE > 25x has only ever occurred during earnings troughs — it's a BUY signal, not a sell.**

### FRO Historical PE at Cycle Peaks (Stock Price Tops)

| Cycle | Stock Peak | PE at Peak | EPS | What Happened Next |
|:------|:---------:|:---------:|:---:|:-------------------|
| **2008 Super Cycle** | $135.78 | **2.66x** | $51.10 | Crashed 75% to $35 |
| **2010 Recovery** | $67.88 | **9.98x** | $6.80 | Fell to $35, then $3 |
| **2015 Mini-cycle** | $7.25 | **5.62x** | $1.29 | Fell 65% to $2.55 |
| **2024 Cycle** | $22.64 | **8.51x** | $2.66 | Fell 48% to $12 |

**Pattern: stocks peak at PE 2-10x, not 25x.** The PE at the peak depends on how extreme the earnings are.

### PE Threshold Backtest (FRO 2006-2025)

| Sell when PE crosses above... | Avg 4Q Forward Return | Verdict |
|:---:|:---:|:---|
| 3x | +52.5% | ❌ Way too early |
| 5x | -5.2% | ⚠️ Breakeven |
| **7x** | **-19.9%** | ✅ Negative returns |
| **8x** | **-20.1%** | ✅ Strong sell signal |
| 10x | +19.4% | ❌ Contaminated by troughs |

**PE > 7x is the cleanest sell signal** — but ONLY when EPS is falling from a meaningful level (not at trough). At troughs, PE > 7x is actually a buy.

### The PE Algo's Fatal Flaw

Tested against historical cycles:

| Cycle | PE ever hit 7x while stock was high? | Algo Worked? |
|:------|:---:|:---:|
| **2008** | No — PE stayed 1-3x at peak (earnings too high) | ❌ **Failed** |
| **2015** | No — EPS collapsed -86% in one quarter, PE jumped past 7x | ❌ **Failed** |
| **2024** | Yes — gradual EPS decline let PE cross 7x at $20 | ✅ **Worked** |

**PE-based sell signals only work for moderate cycles with gradual earnings decline.** They fail in super-cycles (2008) and spike-crash cycles (2015).

---

## 4. Price Momentum Sell Signal — The Universal Solution

### Concept

Sell when stock drops X% from its trailing high. Simple, works for ALL cycle types, doesn't depend on PE or earnings data.

### Backtest Results (FRO, excluding COVID)

**Signal: Sell when price drops 20% from 90-day trailing high**

| Cycle | Stock Peak | Sell Price | Gave Up | Remaining Decline Avoided |
|:------|:---------:|:---------:|:-------:|:------------------------:|
| **2008 Super Cycle** | $144 | **$113** | -22% | **29% of 75% total decline** |
| **2015 Mini Cycle** | $11.32 | **$8.29** | -27% | **37% of 73% total decline** |
| **2024 Recent** | $25.67 | **$19.96** | -22% | **43% of 52% total decline** |
| **Average** | | | **-24%** | **36% avoided** |

All threshold options:

| Threshold | You Give Up | You Avoid | Best For |
|:---------:|:---------:|:---------:|:---------|
| -15% | 16% from peak | 25% of decline | Aggressive exit |
| **-20%** | **24% from peak** | **36% of decline** | **Balanced (recommended)** |
| -25% | 28% from peak | 44% of decline | Patient |
| -30% | 36% from peak | 56% of decline | Too late |

### Critical Flaw: Geopolitical Dips Trigger False Sells

**Problem**: In March 2026, FRO fell ~20-25% during the Hormuz crisis — but TD3C was at an ALL-TIME HIGH of $400K/day. A pure momentum signal would have sold into the dip, exactly the wrong move.

**Solution**: Rate confirmation filter.

---

## 5. The Final Algorithm: Momentum + Rate Confirmation

### The Rule

```
SELL when BOTH conditions are met simultaneously:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. PRICE:  Stock drops ≥20% from 90-day trailing high
  2. RATES:  TD3C/BDTI ALSO down ≥15% from 90-day high
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  If PRICE triggers but RATES are near highs:
  → DO NOT SELL — this is a geopolitical dip (buying opportunity)
```

### Validation Across All Cycles

| Event | Stock -20%? | Rates -15%? | Both? | Correct Action | Outcome |
|:------|:---:|:---:|:---:|:---|:---|
| **2008 crash** | ✅ Jul 08 | ✅ Rates rolling over | **SELL** | ✅ Correct | Avoided -53% more decline |
| **2015 drop** | ✅ Jan 15 | ✅ Rates falling from Q3 14 | **SELL** | ✅ Correct | Avoided further -46% |
| **2024 turn** | ✅ Aug 24 | ✅ BDTI 2500→900 | **SELL** | ✅ Correct | Avoided -30% more |
| **2026 Hormuz** | ✅ Mar 26 | ❌ TD3C at $400K ATH | **NO SELL** | ✅ Correct — was a dip | Stock recovered |

**4/4 correct across all cycle types, including the current one.**

### Optional Tier 1: Early Warning (PE-based trim)

For moderate cycles where PE data is available:

```
PE > 7x + EPS declining 2+ quarters → Trim 30% of position
(Only works for gradual declines like 2024, not super-cycles)
```

---

## 6. Cycle Type Classification

Not all tanker cycles are the same. The sell signal effectiveness depends on cycle type:

| Cycle Type | Example | Duration | EPS Decline Speed | Best Sell Signal |
|:-----------|:--------|:--------:|:-----------------:|:-----------------|
| **Super Cycle** | 2004-2008 | 4 years | Gradual (5+ quarters) | Momentum + Rate confirmation |
| **Storage Spike** | 2015, 2020 | 2-3 quarters | Instant (-86% in 1Q) | Very hard to catch — too fast |
| **Normal Cycle** | 2023-2024 | 1-2 years | Gradual (4-5 quarters) | PE > 7x + Momentum |
| **Structural Shortage** | 2026-2028? | 2-3 years | Gradual (expected) | Momentum + Rate confirmation |

**The 2026-2028 setup is a structural shortage** (supply crunch + SPR restocking), most similar to 2004-2008. The momentum algo should work well because the decline will be gradual as newbuilds arrive mid-2028.

**Storage spikes (2015, 2020) are inherently unpredictable.** Earnings collapse in one quarter when contango unwinds or the event ends. No algo consistently catches these — accept the risk or avoid spike-driven positions entirely.

---

## 7. Putting It All Together — Decision Matrix

### When to BUY

```
✅ Smoothed dividend yield ≥ 8% (hard floor)
✅ Supply/demand balance shows structural tightness
✅ Newbuild deliveries 18+ months away
✅ PE > 10x on trailing (trough earnings — contrarian buy)
```

### When to HOLD

```
🟡 Smoothed yield > 8% but declining trend
🟡 Rates healthy but supply relief 6-12 months out
🟡 PE 3-7x on trailing (mid-cycle, not yet overvalued)
🟡 Tier 1 early warning NOT triggered
```

### When to SELL

```
🔴 Tier 1 (trim 30%): PE > 7x + EPS declining 2Q + EPS still >30% of peak
🔴 Tier 2 (sell remaining): Stock -20% from 90d high AND rates -15% from 90d high
🔴 Either tier alone = partial action. Both = full exit.
```

### When to DO NOTHING (geopolitical dip)

```
🛡️ Stock -20% but rates at/near highs → Geopolitical event, NOT cycle turn
🛡️ Action: HOLD or BUY THE DIP
🛡️ Examples: 2026 Hormuz crisis, 2019 Iran drone attack, 2020 March panic
```

---

## 8. Current Position Assessment (April 2026)

| Signal | DHT | FRO | Status |
|:-------|:---:|:---:|:------:|
| Smoothed yield ≥ 8% | 14.1% ✅ | 9.3% ✅ | **BUY zone** |
| PE > 7x (Tier 1 sell) | ~13x TTM but will collapse to 2-4x as Hormuz earnings hit | Same | **Not a sell** — PE is inflated by low trailing EPS |
| Stock -20% + Rates -15% (Tier 2) | Stock dipped but rates at ATH | Same | **Not a sell** — geopolitical dip |
| Supply outlook | Structural shortage through mid-2028 | Same | **Bullish** |
| Newbuild relief | Mid-2028 (24+ months away) | Same | **No urgency** |
| **Overall** | | | **HOLD / ACCUMULATE on dips** |

Expected sell timeline: **monitor from early 2028** when newbuild deliveries accelerate and rates begin normalizing. Tier 1 may fire mid-2028, Tier 2 likely late 2028 or 2029.

---

## 9. Limitations & Known Issues

1. **Momentum algo gives up 20-25% from peak** — by design, you never sell at the exact top
2. **Storage-spike cycles (2015, 2020) are too fast** — no algo catches a -86% EPS crash in one quarter
3. **Rate data availability** — real-time TD3C requires Baltic Exchange subscription; BDTI free data lags
4. **Backtested on FRO only** — DHT has shorter history; cross-validate when possible
5. **Sample size is small** — only 3-4 clean cycles in 20 years of data
6. **Future may differ** — structural breaks (energy transition, IMO regulations) could change cycle dynamics

---

## Data Sources

- FRO PE/EPS history: Macrotrends (2006-2025 quarterly)
- FRO daily prices: Yahoo Finance via yfinance
- BDTI: GitHub public dataset (2020-2024) + Investing.com scrape (2025)
- TD3C current: Baltic Exchange via Business Times weekly reports
- SPR data: EIA, IEA, country-specific energy agencies
- Newbuild orderbook: Breakwave Advisors, Tankers International, Gibson

---

*This document is a living framework — updated as new data and cycles provide validation.*
*Part of the [VLCC-Analysis-2026](https://github.com/liqiqiii/VLCC-Analysis-2026) project.*

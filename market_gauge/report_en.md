---
layout: default
title: Market Gauge — How High Is the S&P 500, and How Good Is the Quality? (Aug 4, 2026)
---

# Market Gauge: How High Is the S&P 500, and How Good Is the Quality?
## Four axes — breadth · valuation · positioning · quality
### August 4, 2026 — Market-Level Analysis

> **The user's ask:** a separate report measuring **how high the market is and how good the quality is**, across three milestones: (1) **breadth/width** of the rally (is it broadening beyond semis? — backtrack vs history); (2) a **valuation** test (PE/PS/etc. vs history); (3) **institutional/positioning** metrics (CTA + others). Plus anything else useful.

> **TL;DR — expensive and stretched, but genuinely high-quality. "Priced for perfection," not "junk bubble."**
> - **Valuation: historically extreme.** Shiller **CAPE 41.3 = the 98.9th percentile since 1881** (median 16.5; only the Dec-1999 peak of 44.2 was ever higher). Forward P/E ~21 (vs ~17–18 norm), trailing ~28, P/S ~3 (vs ~1.5), **Buffett indicator ~225% of GDP (~99th pct).** *Every* metric says expensive.
> - **Breadth: two-faced.** *Participation* is healthy (~**69% of the S&P above its 200-day MA**), but *leadership concentration* is still the **narrowest in 20 years** — equal-weight/cap-weight (RSP/SPY) sits at the **3rd percentile** of 2005–26. The "widening" is real on a 3-month view (+1.8%) but **fragile**: the last *week* re-narrowed −3.5% on mega-cap earnings, and only **3 of 11 sectors** beat the S&P over the past month.
> - **Positioning: stretched/asymmetric.** CTAs net long (~$34B S&P) with **$100B+ of *mechanical* downside** if momentum breaks; **VIX 16.5 (48th pct)** — no fear cushion.
> - **Quality: the genuine bull anchor.** **Record earnings + record net margins.** This is why it's the [AI-bubble report's](../ai_bubble/report_en) "**1998→late-1999, loaded but unlit**" market, *not* a profitless-1999 blow-off. High price, but real earnings underneath.
> - **Net: the market is HIGH (valuation ~99th pct, positioning stretched) with a THIN margin of safety — but the quality is high. Vulnerable to a positioning/rate/credit shock, not to a valuation-only collapse.**
> - **Education/analysis, NOT investment advice.**

---

## ⚠️ Protocol & data-hygiene notice

Applies the **Two-Step Research Protocol**. §1 method · §2 Step-1 draft · §3 Step-2 review · §4 breadth · §5 valuation · §6 positioning · §7 quality · §8 composite verdict.

**Rule 4 flags:** (a) yfinance columns are alphabetical → indexed **by name**. (b) **CAPE percentile, breadth (RSP/SPY), sector participation and VIX are *computed* here and reproducible**; (c) **forward/trailing P/E, P/S and the Buffett indicator are web-sourced point-in-time estimates** (ranges, not precise) and labeled as such; (d) **CTA figures conflict across dated snapshots** (net-long-adding vs earlier capitulation) — directionally "stretched," exact number provisional.

---

# Section 1 — Fact-base & method

- **Computed (reproducible, `run_market_gauge.py`):** RSP/SPY equal-vs-cap breadth ratio + percentile + 1wk→12mo trend (yfinance, 2005–26); 11-sector participation vs SPY; VIX level + percentile; **Shiller CAPE percentile** (Yale `ie_data.xls`, 1881–present).
- **Web-sourced (point-in-time, flagged):** forward P/E, trailing P/E, P/S, Buffett indicator, % above 200-day MA, CTA/positioning (Goldman/DB via trade press), profit-margin/earnings records.
- **Percentile = how expensive/narrow vs the asset's own history** (higher = more extreme). We report *level AND percentile* so outliers don't mislead.

---

# Section 2 — Step 1: Concise Research Draft

**Core conclusion:** The S&P is **expensive on every valuation axis (CAPE ~99th pct), with stretched mechanical positioning and still-narrow leadership — but underpinned by record real earnings.** It is a *high-price, high-quality, thin-margin-of-safety* market: a **priced-for-perfection late cycle**, not a low-quality bubble. Downside is more likely from a **positioning/rate/credit trigger** than from valuation alone.

*Supporting (claim → evidence):*
1. **Valuation is ~99th-percentile extreme** → CAPE 41.3 = 98.9th pct since 1881; Buffett ~225% GDP. *Evidence: §5 — obtained.*
2. **Leadership breadth is historically narrow despite better participation** → RSP/SPY 3rd pct; 69% >200dma. *Evidence: §4 — obtained.*
3. **Earnings quality is genuinely high** → record margins + record aggregate earnings. *Evidence: §7 — obtained (web).*

*Opposing (claim → evidence):*
1. **High valuation may be "justified" by margins/rates** → record profitability supports higher multiples. *Evidence: need margin-sustainability / rate path — **partly unknown**.* 
2. **Breadth is broadening → bullish, not late-cycle** → 3mo RSP/SPY +1.8%, 69% >200dma. *Evidence: obtained, but last-week reversal + 3/11 sectors argue it's early/fragile.*

---

# Section 3 — Step 2: Strict Peer Review (draft NOT rewritten)

1. **Facts to verify:** exact forward/trailing P/E and P/S (ranges, provider-dependent); the **200dma breadth number** (sources cite 69% *and* 95% — definition-sensitive); the **live CTA net exposure** (snapshots conflict by date); whether "record margins" are peak-cyclical (mean-reversion risk).
2. **Logical leaps / equivocation:** do not conflate **participation breadth** (% >200dma, healthy) with **leadership concentration** (RSP/SPY, narrow) — they say *opposite* things and the headline "breadth is fine" hides the concentration; "high margins justify high CAPE" is a **regime assumption**, not a law (margins mean-revert); CAPE is a *long-horizon return* signal, **not a timing tool**.
3. **Missing counterexamples / competing explanations:** CAPE has been "expensive" for a decade and the market kept rising (it forecasts *10-yr* returns, not the next year); index composition shifted toward higher-margin tech (some CAPE elevation is **structural**, not pure froth); a debasement regime lifts *nominal* everything.
4. **Primary sources to add:** S&P/Shiller earnings series; Yardeni/FactSet forward-P/E & margin data; Goldman/DB prime-brokerage CTA notes (primary); Fed/GDP for the Buffett denominator; NYSE/Nasdaq A-D and %>200dma primary feeds.
5. **Speculation, not fact:** "priced for perfection"; "thin margin of safety"; that the trigger will be positioning/credit rather than valuation; the "1998→late-1999" mapping (a characterization borrowed from the AI-bubble report).

---

# Section 4 — Breadth: the two faces (is the rally broadening?)

**Face A — participation is healthy (bullish):** ~**69% of S&P 500 stocks are above their 200-day MA** (some screens up to 95%), well above the long-run norm. On a 3-month view the equal-weight index is catching up (RSP/SPY **+1.8%**).

**Face B — leadership concentration is the narrowest in 20 years (cautionary):**

| RSP/SPY (equal- vs cap-weight) | Value |
|---|---|
| Level now (2005 = 1.00) | **0.845** |
| **Percentile of 2005–2026 range** | **3rd** |
| Change last 12mo | **−1.4%** (mega-caps still leading) |
| Change last 1 week | **−3.5%** (re-narrowed on mega-cap earnings) |
| Change last 3 months | **+1.8%** (broadening) |
| **Sectors beating SPY (last 1mo)** | **3 / 11** |
| Sectors beating SPY (last 3mo) | 4 / 11 |

**Read (answering the user directly):** your instinct is **partly right** — participation *is* broadening (69% >200dma, 3-month equal-weight catch-up). **But the cap-weight concentration is still near a 20-year extreme, and the improvement is early and fragile:** the *last week* actually re-narrowed −3.5% (mega-cap earnings pulled the index back up while the average stock lagged), and only **3 of 11 sectors** beat the index over the past month. **Verdict: genuine but unconfirmed broadening on top of historically narrow leadership.** A durable regime change would show RSP/SPY *rising for months* and >6/11 sectors leading — not there yet.

*(RSP/SPY is a clean, reproducible breadth proxy: when it falls, a handful of mega-caps are carrying the index; when it rises, the average stock is participating.)*

---

# Section 5 — Valuation: expensive on every axis

| Metric | Aug-2026 | Hist. avg/median | Percentile | Verdict |
|---|---|---|---|---|
| **Shiller CAPE** | **41.3** | 16.5 (median) | **98.9th** *(computed, 1881–now; all-time max 44.2 = Dec-1999)* | **Very expensive** |
| Forward P/E | ~21 | ~17–18 | >90th | Expensive |
| Trailing P/E | ~28 | ~19–20 | >90th | Expensive |
| Price/Sales | ~3.0 | ~1.5 | ~99th | 2× history |
| **Buffett (MktCap/GDP)** | **~225%** | ~100% | **99–100th** | Record |

**Read:** there is **no valuation metric that says "cheap."** The single most robust anchor — **CAPE at the 98.9th percentile of 145 years**, essentially matching the dot-com peak — says forward *10-year* real returns are likely low. **Caveat (Rule 4 / §3):** CAPE is a **long-horizon** signal, *not* a timing tool (it's been elevated for a decade); part of the elevation is **structural** (index tilted to high-margin tech) and **regime** (debasement lifts nominal valuations). But on *margin of safety*, the answer is unambiguous: **there is very little.**

---

# Section 6 — Positioning & volatility: stretched and asymmetric

- **CTAs / systematic trend-followers:** net long (~**$34B** S&P futures, ~$93B global equity). The risk is **asymmetric and mechanical**: if momentum breaks, models could dump **$100B+** globally **regardless of fundamentals** — a positioning-driven air-pocket (the same "mechanical, momentum not value" flow that can overshoot in either direction). *(Rule 4: dated snapshots conflict — spring showed capitulation/short, summer net-long-adding; treat the direction "stretched," the exact number provisional.)*
- **VIX 16.5 — 48th percentile** (1y avg 18.2, 2005–26 median 16.8): middling, **no fear cushion**. Cheap-ish protection, complacent-ish tape — consistent with the [tail_hedge](../tail_hedge/summary_en) point that hedges are best bought *before* stress, when VIX is low.
- **Net:** positioning is a **fragility amplifier**, not a trigger — it makes any exogenous shock (rate/credit/geopolitical) hit harder and faster.

---

# Section 7 — Quality: the genuine bull anchor

- **Record aggregate earnings + record net profit margins.** This is the decisive difference from a low-quality bubble: the high price sits on **real, growing profits**, not story stocks.
- It is the same signal as the [AI-bubble report](../ai_bubble/report_en) (Micron 80% margins, hyperscaler cash machines) — the **"1998→late-1999, shovels genuinely profitable"** market. Expensive *because* the earnings are real and accelerating, not detached from them.
- **The quality caveat (§3):** record margins are a **cyclical high** and can mean-revert; and quality is **concentrated** in the same mega-caps that dominate the index (see §4). So "high quality" and "narrow" are two sides of one coin — the quality is real but **not broadly distributed**.

---

# Section 8 — Composite verdict: how high, how good

**Percentile scorecard:**

| Axis | Reading | Signal |
|---|---|---|
| Valuation — CAPE | 41.3 (98.9th pct) | 🔴 EXPENSIVE |
| Valuation — Buffett | ~225% GDP (~99th) | 🔴 EXPENSIVE |
| Breadth — concentration | RSP/SPY 3rd pct | 🟠 NARROW |
| Breadth — recent trend | 3mo +1.8% / 1wk −3.5% | 🟡 broadening but fragile |
| Positioning — VIX | 48th pct | 🟡 mid / no cushion |
| Positioning — CTA | net long, $100B+ downside | 🟠 stretched/asymmetric |
| **Quality — earnings** | record earnings + margins | 🟢 HIGH (real profits) |

```
How HIGH:     Very. Valuation ~99th percentile (CAPE ~ dot-com peak), Buffett a
              record, positioning stretched. Margin of safety is THIN.
How GOOD:     Genuinely good. Record earnings + margins; participation improving.
              This is quality-led, not junk-led.
The synthesis: "PRICED FOR PERFECTION." A high-price, high-quality, thin-cushion,
              still-narrow late-cycle market. Not a profitless 1999/2000 blow-off,
              but little room for error.
Maps to:      The AI-bubble report's "1998 -> late-1999, loaded but unlit"
              (ai_bubble Addendum C): fragility preconditions present, trigger absent.
Vulnerability: A POSITIONING / RATE / CREDIT shock (CTA unwind, a Fed surprise,
              the Oracle/AI-credit canary), NOT a valuation-only collapse.
What would improve quality: RSP/SPY rising for months + >6/11 sectors leading
              (durable breadth) — would make the highs healthier and less fragile.
```

> **Bottom line for the user:** the market is **historically high** — CAPE at the 99th percentile (basically the 1999 level), Buffett at a record, positioning stretched, leadership still the narrowest in 20 years. **But the quality is genuinely good:** record earnings and margins mean this is a *priced-for-perfection, high-quality* tape, not a profitless bubble. Your read that "width is getting better" is **partly right** — participation is improving (69% >200dma) — but the cap-weight concentration is still near a two-decade extreme and last week actually re-narrowed, so treat the broadening as **real but unconfirmed.** Practically: **thin margin of safety + high quality = stay invested but hedged/diversified** (this is exactly the [30/30/40 barbell](../portfolio/report_en) and [tail-hedge](../tail_hedge/summary_en) case), and watch the **positioning/credit** triggers, not the P/E, for the turn.

---

## Reproduce it yourself

```
cd market_gauge
python run_market_gauge.py     # writes data/*.csv (breadth, sector breadth, valuation, VIX, scorecard)
```

**Data files** (`market_gauge/data/`): `breadth.csv`, `sector_breadth.csv`, `valuation.csv`, `vix.csv`, `scorecard.csv`. CAPE percentile computed from Yale `ie_data.xls` (cached locally).

**Sources (accessed Aug 4, 2026):** yfinance (RSP, SPY, ^VIX, 11 SPDR sectors); Yale/Shiller `ie_data.xls` (CAPE 1881–now); web valuation (MacroMicro, investsnips, GuruFocus, worldperatio — forward/trailing P/E, CAPE, Buffett); breadth (Stock Alarm Pro, MacroMicro, CondorEdge — %>200dma, A/D); positioning (Goldman/Deutsche Bank via Yahoo/Hedgeweek/Investing.com — CTA/sentiment). **PE/PS/Buffett are point-in-time estimates (Rule 4); CTA snapshots conflict by date.**

---

*Two-Step Research Protocol applied (§2 draft + §3 review). Computed metrics reproducible; web-sourced levels flagged. CAPE is a long-horizon, not a timing, signal. Education/analysis only — not investment advice.*

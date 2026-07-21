---
layout: default
title: Sector Convexity Hedging — Financials (XLF) & Technology (XLK) vs S&P & VLCC
---

# Sector Convexity Hedging: Financials & Technology
## Are long-term-HOLDABLE fat-tailed sectors a better "hold + tail-hedge" than VLCC?
### July 20, 2026 — Sector application of the convexity framework (backtested)

> **Why this exists**: a VLCC (DHT/FRO) position has **no long-run drift** → hedging it is a **cycle-timing bet**, not a hold-and-hedge decision ([VLCC study §8](report_vlcc_en)). The natural next question: are broad, **long-term-holdable** sectors that *also* carry fat crash tails — **Financials (XLF)** and **Technology (XLK)** — the sweet spot where tail-hedging a permanent hold actually adds geometric value? This runs the same backtest on XLF/XLK and places them on a **break-even-VRP spectrum** with the S&P and VLCC. Code: [`run_backtest_sectors.py`](run_backtest_sectors.py).

> **TL;DR verdict — a useful, counter-intuitive split:**
> 1. **For HOLDING: yes, far better than VLCC.** XLF/XLK have **positive long-run drift** (CAGR **+5.7% / +9.2%** over 1999–2024) vs VLCC's negative drift — you can hold them like an index; you don't *need* to time them.
> 2. **For systematic tail-HEDGING: mostly NO — the drift that makes them holdable makes the hedge bleed.** Break-even VRP (the max overpricing at which hedging still raises CAGR): **S&P ≈ 0%, Financials ≈ 0%, Technology ≈ 27%, VLCC-DHT ≈ 67%.**
> 3. **Technology is the one genuine sector candidate.** XLK's **multiple** deep crashes (dot-com, 2008, 2022) + lower vol give it a real break-even VRP ≈ **27%**, and **live 1-yr 20%-OTM XLK puts price a paid VRP of ≈ 24% (< 27%)** → a tactical XLK tail-hedge is *marginally* defensible **today**. **But** that edge is **crash-regime-dependent** (0% post-2010) — it only pays if big tech drawdowns keep recurring (see the [AI-bubble report §11](../ai_bubble/report_en)).
> 4. **Unifying principle:** tail-hedging pays only where crashes are **deep AND frequent relative to drift.** Broad holdable assets have too much drift and too-rare crashes → **hold, don't hedge.** Only Tech (frequent crashes) and top-of-cycle VLCC clear the bar — both are regime/timing calls.
> 5. **Quality names (JPM / AXP) — the clearest "hold, don't hedge" case (§6).** They *out-compound* XLF (**+10.3% / +10.9%** vs +5.7%) → far better **holds**. But their break-even VRP is ~0% *and* **live single-name 1-yr 20%-OTM puts price a paid VRP of ≈100% (IV roughly *double* realized)** → hedging them is a catastrophic drag. **If you must hedge a financials book, buy an INDEX put, not the name.**
>
> *Education/analysis, not investment advice.*

---

## ⚠️ Protocol Notice & Caveats

Applies the repo's **Two-Step Research Protocol**; connects to **CRule 1/5** and the [S&P](report_en) and [VLCC](report_vlcc_en) studies. §1 draft; §2 review; §3 results; §4 synthesis; §5 takeaways.

**Data**: XLF, XLK daily **adjusted** close (1998-12 → 2024-12), yfinance; S&P from the sibling study; DHT/FRO break-even reused. PASSIVE rolled put, BS-priced, IV = 63-day realized vol × (1 + VRP), canonical **20%-OTM 1-year**.
**Caveats**: options modeled on the adjusted (total-return) series; **windowed break-even VRPs are crash-dependent** (regime-conditional, not forecasts); XLF deep-OTM LEAPS puts are thin (no clean live quote); gross of tax/cost.

---

# Section 1 — Step 1: Concise Research Draft

**Core conclusion (first):** Financials and Technology are **much better long-term *holds* than VLCC** (positive drift, no timing required) but **not much better *hedge* candidates**: the same positive drift that makes them holdable makes systematic tail-hedging bleed, so their break-even VRP sits near the S&P's ~0% — **except Technology**, whose repeated deep crashes push its break-even VRP to ~27% and make a *tactical* hedge defensible when you expect elevated crash risk (e.g., an AI-bubble unwind).

**3 supporting points** *(claim → evidence needed)*:
1. **Claim:** XLF/XLK are holdable (unlike VLCC). → *Evidence:* CAGR +5.7% / +9.2% (1999–2024) vs DHT −6.2% ([profile](data/results_sector_profile.csv)).
2. **Claim:** Systematic hedging bleeds for most sectors. → *Evidence:* break-even VRP ≈ 0% for XLF and S&P; win-rate 4–7% with negative CAGR delta at VRP0 ([winrate](data/results_sector_winrate_vrp.csv)).
3. **Claim:** Tech is the exception. → *Evidence:* XLK break-even VRP ≈ 27%; hedged CAGR *rises* 9.2% → 10.85% and maxDD −82% → −68% at 20%-OTM 1yr VRP0 ([hedge_grid](data/results_sector_hedge_grid.csv)).

**2 opposing / counter points** *(claim → evidence needed)*:
1. **Claim:** Even Tech's edge is crash-regime-dependent, not durable. → *Evidence:* XLK break-even VRP collapses **26.6% → 0%** in 2010+ / 2015+ windows ([breakeven_windows](data/results_sector_breakeven_windows.csv)).
2. **Claim:** Financials' 2008 crash *should* reward hedging but doesn't. → *Evidence:* XLF maxDD −83% yet break-even VRP 0% — one big event + 29% vol (expensive premiums) don't beat the drift bleed.

**Explicitly unknown (not fabricated):** the real paid VRP on XLF deep-OTM LEAPS (no liquid quote found); whether future tech crash frequency resembles 1998–2024; results net of tax/transaction cost.

---

# Section 2 — Step 2: Strict Peer Review (draft NOT rewritten)

**1. Facts that need verification**
- XLK break-even 26.6% is a 26-yr average dominated by the dot-com and 2008 crashes; verify sensitivity to the 20%-OTM strike choice and to sub-windows (done: collapses to 0% post-2010).
- Live XLK paid VRP (24%) is one strike/expiry snapshot (OI 32) — verify against a fuller chain.
- XLF/XLK adjusted-series (total-return) as option underlying is a proxy; verify vs price-based option settlement.

**2. Logical leaps / equivocation**
- **"Holdable ⇄ good hedge candidate"** — the draft's whole point is these are *opposite* properties; don't let the reader conflate them.
- **"Break-even VRP 27% for Tech" ⇄ "hedge Tech now"** — the 27% is historical/regime-conditional; the *decision* still needs a forward crash-risk view.
- **CAGR-positive ≠ EV-positive** — XLK hedging is EV-negative above ~0% VRP; its value is the geometric/tail benefit, valid only if the crashes recur.

**3. Missing counterexamples / competing explanations**
- **Just diversify** (own the S&P, not the sector): removes the single-sector fat tail without paying any premium — the simplest "hedge."
- **The 2010–2024 bull** flatters "don't hedge"; a lost decade (2000–2010 for the S&P) would raise every break-even VRP.
- **Equal-weight vs cap-weight / factor tilts** compete with options as risk reducers.

**4. Most important primary sources to add**
- XLF/XLK full option chains (real IV/skew) for a proper paid-VRP.
- CBOE/OptionMetrics historical IV to compute *realized* VRP over time (not a proxy).

**5. Sentences that are at most speculation, not fact**
- "Technology is the one genuine candidate" as a forward statement (backward-looking, crash-dependent).
- Any implication that XLK's 27% break-even persists.
- The AI-bubble linkage as a *prediction* rather than a conditional.

---

# Section 3 — Results

## 3.1 Profile → [`results_sector_profile.csv`](data/results_sector_profile.csv)

| Asset | Years | Ann. vol | maxDD | **Long-run CAGR** | Holdable? |
|---|---|---|---|---|---|
| **XLF** Financials | 26 | 29% | **−83%** (2008) | **+5.7%** | ✅ |
| **XLK** Technology | 26 | 26% | **−82%** (dot-com) | **+9.2%** | ✅ |
| S&P 500 | 51 | 17% | −57% | +8.4% | ✅ |
| *(ref) DHT VLCC* | 19 | 48% | −97% | **−6.2%** | ❌ |

*Sectors sit **between** the S&P and VLCC: fatter tails (−82/−83%) than the index, but — unlike VLCC — a **positive long-run drift** that makes buy-and-hold viable.*

## 3.2 The break-even-VRP spectrum → [`results_breakeven_spectrum.csv`](data/results_breakeven_spectrum.csv)

| Asset | maxDD | Unhedged CAGR | **CAGR break-even VRP** |
|---|---|---|---|
| S&P 500 | −57% | +8.4% | **≈ 0%** |
| **XLF** Financials | −83% | +5.7% | **≈ 0%** |
| **XLK** Technology | −82% | +9.2% | **≈ 27%** |
| DHT (VLCC) | −97% | −6.2% | ≈ 67% |
| FRO (VLCC) | −98% | −4.7% | ≈ 0% |
| *JPM (quality name, §6)* | −74% | +10.3% | ≈ 0% |
| *AXP (quality name, §6)* | −84% | +10.9% | ≈ 0% |

*The number rises with tail depth **and** the absence of drift. A −83% crash (XLF) is **not** enough on its own; you need either **recurring** deep crashes (XLK) or **no drift** to offset (DHT). Quality compounders JPM/AXP — deepest single-name drift — sit at ~0% (see §6).*

## 3.3 Win-rate vs VRP (20%-OTM 1-yr) → [`results_sector_winrate_vrp.csv`](data/results_sector_winrate_vrp.csv)

| Asset | VRP | Win-rate | Payoff ratio | **CAGR delta** |
|---|---|---|---|---|
| **XLK** | 0% | 11.7% | 7.6 | **+1.68pp** |
| XLK | 25% | 11.7% | 3.9 | +0.11pp |
| **XLF** | 0% | 6.7% | 7.6 | −0.58pp |
| S&P | 0% | 4.3% | 9.9 | −0.42pp |

*Only **XLK** has a positive CAGR delta at realized-vol pricing; its break-even VRP (~27%) sits right where the delta crosses zero. XLF and the S&P bleed from VRP 0.*

## 3.4 Robustness — every positive break-even is crash-dependent → [`results_sector_breakeven_windows.csv`](data/results_sector_breakeven_windows.csv)

| Asset | Full | 2010+ | 2015+ |
|---|---|---|---|
| XLK | **27%** | **0%** | **0%** |
| XLF | 0% | 0% | 0% |
| S&P | 0% | 0% | 0% |

*XLK's 27% is **entirely the dot-com + 2008 crashes**; strip them out (2010+) and it is 0% like everything else. Same crash-window dependence as VLCC's 67% — a recurring theme of this whole study.*

## 3.5 Live calibration (Jul 2026) → [`results_sector_paid_vrp.csv`](data/results_sector_paid_vrp.csv)

| Ticker | Expiry (T) | Spot | ~20%-OTM put IV | Realized (63d) | **Paid VRP** | OI |
|---|---|---|---|---|---|---|
| **XLK** | 2027-06 (0.9y) | $175.7 | 41% | 33% | **≈ +24%** | 32 |
| XLF | 2027-06 (1.0y) | $56.0 | — | 13% | *no liquid deep-OTM LEAPS put* | 0 |

*XLK's live paid VRP (**24%**) is **just below** its historical break-even (**27%**) → a tactical XLK tail-hedge is *marginally* worth it **now** — but only if you believe elevated tech crash risk (AI-bubble unwind) persists; in a durable secular bull it bleeds. XLF deep-OTM LEAPS are too thin to hedge with options cleanly.*

---

# Section 4 — Synthesis: The Drift-vs-Hedge Tension

**The property that makes an asset *holdable* is the property that makes tail-hedging it *bleed*.** Positive drift means the hedge pays premium through years of gains and only wins in the rare crash. So:

| Asset | Long-term HOLD? | Systematic tail-HEDGE worth it? | Why |
|---|---|---|---|
| **S&P 500** | ✅ best (diversified) | ❌ break-even ~0% | thin tail + strong drift |
| **XLF** Financials | ✅ (with 2008-type risk) | ❌ break-even ~0% | one big crash, high vol, drift bleed |
| **XLK** Technology | ✅ (highest drift) | 🟡 **only sector with +break-even (~27%)** | recurring deep crashes; but regime-dependent |
| **VLCC** (DHT/FRO) | ❌ no drift → cycle-timing | 🟡 67% but pure **top-of-cycle** bet | catastrophic tail, no drift, thin options |

**So the answer to "are Financials/Tech a better hold-and-hedge than VLCC?" is a split decision:**
- **Better to HOLD — decisively yes.** You can own XLF/XLK (or the S&P) for the long run and let the drift compound; VLCC you cannot.
- **Better to systematically HEDGE — no, with one asterisk.** For holdable assets the drift makes hedging a drag (break-even ~0%); the cheapest "tail protection" is usually **just diversification / holding through**. **Technology is the sole exception** (~27% break-even, live 24% paid), and even that is a **tactical, crash-risk-conditional** call — precisely the kind of judgment the [AI-bubble report](../ai_bubble/report_en) is built to inform.

**The unifying rule:** *tail-hedging earns its premium only where crashes are deep **and** frequent relative to drift.* Broad holdable sectors fail the "frequent relative to drift" test (hold instead); VLCC fails the "holdable" test (time instead). **Tech is the rare asset that can fail neither — which is exactly why it, and a top-of-cycle VLCC, are the only two places convex tail-hedging has historically paid.**

---

# Section 5 — Practical Takeaways

- **Long-term holders**: own broad, drifting assets (S&P, or XLF/XLK for tilt) and **do not systematically buy tail insurance** — the break-even VRP is ~0%, so it bleeds; diversification and time are your cheaper "hedge."
- **The one place options tail-hedging holdable equities makes sense is Technology, tactically**, when you judge crash risk elevated (stretched valuations / bubble signals). Live XLK paid VRP ≈ 24% < its ~27% break-even makes a *small* long-dated deep-OTM XLK put defensible **now** — a direct, tradeable expression of the [AI-bubble §11](../ai_bubble/report_en) thesis.
- **VLCC** remains a **cycle-timing** hedge (buy protection only near a top, [VLCC §8](report_vlcc_en)); Financials, like the S&P, is best hedged by **sizing/diversification**, not options.
- **Meta-lesson across the whole `tail_hedge/` study:** convex tail-hedging is not a portfolio pillar; it is a **conditional, regime-timed tool** whose worth is decided by the tail depth, the drift, and — above all — the **VRP you pay vs a break-even that is itself a function of where you think the cycle is.**

---

# Section 6 — Individual Quality Names: JPM & AXP Instead of XLF?

A holder might reasonably prefer **quality compounders** — JPMorgan (**JPM**), American Express (**AXP**) — to the diluted XLF. Do they change the hedge calculus? → [`results_stock_profile.csv`](data/results_stock_profile.csv), [`results_stock_paid_vrp.csv`](data/results_stock_paid_vrp.csv)

| Name | Vol | maxDD | **CAGR** | Break-even VRP | **Live paid VRP** |
|---|---|---|---|---|---|
| **JPM** | 38% | −74% | **+10.3%** | ≈ 0% (all windows) | **≈ +107%** (IV 47% / rv 23%, OI 309) |
| **AXP** | 36% | −84% | **+10.9%** | ≈ 0% (all windows) | **≈ +99%** (IV 49% / rv 25%, OI 8) |
| *(ref) XLF* | 29% | −83% | +5.7% | ≈ 0% | deep-OTM LEAPS thin |

**Two decisive findings:**
1. **For HOLDING — you're right, the quality names win.** JPM/AXP compound at **+10.3% / +10.9%** vs XLF's +5.7% — the diluted sector drags in weaker constituents. **Quality > sector ETF for a long-term hold.**
2. **For HEDGING — they are the *worst* candidates, and the live options prove it.** Break-even VRP is ~0% (higher drift + higher single-name vol → the hedge bleeds even more than XLF), while **live JPM/AXP 1-yr 20%-OTM puts price a paid VRP of ~100% — IV roughly *double* realized.** Single-name options carry a large idiosyncratic/skew premium. **Paying ~100% VRP against a ~0% break-even is a catastrophic drag** ([win-rate](data/results_stock_winrate_vrp.csv): JPM CAGR delta −3.95pp even at *free* VRP0; AXP −0.95pp).

**Practical corollary — hedge the index, not the name.** Single-name paid VRP (~100%) is ~3–4× the index paid VRP (XLK ~24%). A put also cannot cleanly hedge single-name blow-ups (fraud, litigation) — only broad crashes. **So if you ever want tail protection on a quality-financials book, buy an INDEX put (SPX/XLF), not JPM/AXP puts** — and for JPM/AXP specifically, the answer is simply **HOLD** (the drift is your friend; the options are far too dear).

> **Refined verdict:** the user's instinct is right in the best possible way — **JPM/AXP are superior long-term *holds* to XLF, and precisely *because* they compound so well (and their single-name options are so expensive), they are the clearest "just hold, don't hedge" case in the entire study.**

---

# Section 7 — Crisis Playbook for Financials: Dip-Buy the Survivors, Don't Insure Them

> **The claim tested (user):** *"Even in the 1982 Volcker moment, the stability of the financial system prevailed over inflation pressure"* — with the implicit assumption that **even in a market crash the state prioritizes financial-system stability**, which would make **dip-buying financials in a crash** a strategy backed by policy. Is it right?

## 7.1 Fact-base — 1982 (cited)

- **Aug 1982**: Mexico announced it could not service its ~$80B debt; other LDCs followed. The **nine largest US money-center banks held Latin-American debt = 176% of capital** (total LDC ≈ 290%) → a systemic solvency threat. *(Federal Reserve History, "Latin American Debt Crisis of the 1980s"; FDIC, "The LDC Debt Crisis.")*
- **July–Aug 1982**: the Fed **ended tightening and began easing** — *"although inflation was still high (>7%), the risks to the financial system were deemed more urgent."* *(St. Louis Fed Review, "The Volcker Tightening Cycle: Explaining the 1982 Course Reversal," 2025.)*
- **Forbearance**: regulators did **not** force banks to write down LDC loans (which would have wiped out capital); Fed/Treasury/IMF arranged bridge loans and reschedulings. *(PIIE, "How de Larosière and Volcker contained the 1982–89 debt crisis.")*
- **Crucial nuance**: inflation had **already fallen from ~14% (1980) to ~7%** and was declining — so easing to save the system was *cheap*; the "stability vs inflation" tradeoff was **not fully binding**.

## 7.2 Step 1 — Concise draft

**Core conclusion (first):** The claim is **broadly correct but conditional.** In 1982 the Fed did put financial-system stability above the (still-elevated) inflation pressure — **but only because inflation was already falling**, making the rescue low-cost. So the durable rule is: **stability > inflation *when inflation is receding/moderate*; the rule fails when inflation is high and sticky.** For the dip-buy strategy this means it works only when (a) you buy the **quality survivor**, not the casualty, and (b) inflation is **not** the binding constraint (so the "Fed put" is live).

**3 supporting points** *(claim → evidence)*:
1. **The Fed pivots to save the system.** → 1982 pivot (above); repeated in 2008 (TARP + Fed liquidity), 2020 (unlimited QE), 2023 (SVB → BTFP + deposit backstop).
2. **Quality survivors deliver enormous crash-recovery returns.** → §7.4: JPM/AXP bought at the 2009 bottom returned ×22 / ×35 to 2024.
3. **Crises make strong banks stronger (consolidation).** → JPM acquired Bear Stearns + WaMu (2008), First Republic (2023) at fire-sale prices.

**2 opposing points** *(claim → evidence)*:
1. **1982 wasn't a clean stability>inflation trade — inflation was already broken** (14% → 7%); Volcker first inflicted the −10.8%-unemployment 1981–82 recession, i.e. he put inflation *above* stability for years.
2. **When inflation is the binding constraint, the rule reverses.** → **2022**: stocks −25%, financials fell, but the Fed **kept hiking** into 9% inflation — no rescue.

**Explicitly unknown:** whether the next crash coincides with high sticky inflation (stagflation) — which would disable the Fed put.

## 7.3 Step 2 — Strict peer review (draft NOT rewritten)

1. **Facts to verify:** exact pivot month (FOMC 1982 minutes); note the Fed can *simultaneously* hike (anti-inflation) and backstop (BTFP 2023) — the two aren't strictly exclusive.
2. **Logical leaps:** the fatal equivocation is **"save the system" ⇄ "save bank *equity*."** The state protects **depositors/creditors/payments**, routinely **wiping out or diluting equity** (Citi, AIG, WaMu, Lehman, Fannie/Freddie, SVB equity → ~0). "System stability" ≠ "your shares are backstopped." Also "financial *system*" ⇄ "financial *stock*" — the system survives; a given firm may not.
3. **Missing counterexamples:** casualties vs survivors (Citi −98%, never regained its peak — §7.4); the post-1982 bull owed as much to **inflation being tamed + rock-bottom valuations (S&P PE ~7)** as to the bank rescue.
4. **Primary sources to add:** FOMC 1982 minutes; Volcker, *Keeping At It*; 2022–23 FOMC statements + BTFP terms.
5. **Speculation, not fact:** "stability > inflation" as a *law* (it is conditional); "dip-buy financials in a crash" (a strategy hypothesis contingent on survivor-selection + a live Fed put).

## 7.4 Dip-buy evidence — survivors vs a casualty → [`results_crisis_dipbuy.csv`](data/results_crisis_dipbuy.csv)

Buying at the **2009-03-09** market bottom (our committed daily adjusted data; [`run_crisis_dipbuy.py`](run_crisis_dipbuy.py)):

| Asset | 2008–09 drawdown | +1yr | **→ 2024 (×)** | 2020 DD → +1yr | Regained 2007 peak? |
|---|---|---|---|---|---|
| **JPM** (survivor) | −68% | +168% | **×22** | −44% → +96% | ✅ yes |
| **AXP** (survivor) | −84% | +285% | **×35** | −50% → +101% | ✅ yes |
| XLF (sector) | −83% | +150% | ×13 | −43% → +92% | ✅ yes |
| **C — Citigroup (casualty)** | **−98%** | +264% | **×8** | −57% → +109% | ❌ **no** |

*The trap made concrete: **Citi bounced +264% in year one** (looks like the best dip-buy!) — yet its 15-year total (×8) badly lagged the survivors (JPM ×22, AXP ×35), and it **never regained its 2007 high**. The first-year dead-cat bounce does **not** separate survivors from casualties; the −98% vs −68% drawdown and the "regained peak" test do. **Buy the quality survivor, not "financials."***

## 7.5 Verdict + how it plugs into this study

**The claim is correct with two asterisks:** *(1)* **"stability > inflation" only holds when inflation is receding** (1982/2008/2020) and **fails when inflation is the binding constraint** (2022); *(2)* **the state saves the *system*, often by sacrificing *equity*** — so the strategy is "buy the **survivor**," not "buy financials."

**And this is the *better* convex play for a quality-financials holder than buying puts.** §6 showed live JPM/AXP puts price a paid VRP of ~100% — a catastrophic hedge. The convex alternative the crisis history endorses:

> **Hold JPM/AXP + keep dry powder + dip-buy the survivors in a Fed-backstopped (inflation-permitting) crisis.** You capture (a) the deepest discount, (b) the **consolidation premium** (strong banks eat weak ones), and (c) the system backstop — *without* paying ~100% VRP for insurance. This is **CRule 5** ("buy fear") and the reinvestment discipline of the [S&P study §7.2](report_en) applied to financials — the crash is the **buying** signal, not the hedging signal.

*(Sources: Federal Reserve History; St. Louis Fed Review 2025; PIIE; FDIC — 1982/LDC. Own data: `results_crisis_dipbuy.csv`, `results_stock_paid_vrp.csv`. Casualty Citi (C) pulled live via yfinance. Education/analysis, not investment advice.)*

## 7.6 The survivor screen — how to avoid dip-buying a "Citi"

**Good news: survivorship is largely predictable *ex ante*.** Almost every casualty (Citi, Lehman, Bear, WaMu, SVB) failed for reasons **visible in the pre-crash filings** — thin capital, fragile funding, a single toxic concentration. Don't be fooled by hindsight: you can screen for this.

**Five-factor screen (check *before* you buy):**

| Dimension | 🟢 Survivor (JPM / AXP) | 🔴 Casualty (Citi / Lehman / SVB) |
|---|---|---|
| **1. Capital** (survival factor #1) | CET1 well above minimum + buffers; low leverage | thin tangible common equity; leverage >15–20× |
| **2. Funding** (the liability side is the killer) | **sticky, diversified, insured retail deposits** | short-term wholesale/repo; **concentrated uninsured deposits**; hot money |
| **3. Asset concentration** | diversified; no exposure to the cycle's toxic asset; small unrealized losses | concentrated in subprime / CRE / long-duration; large AFS/HTM marks |
| **4. Franchise / model** | diversified earnings, closed-loop network (AXP), fee income | monoline; reliant on leverage/spread; fragile funding model |
| **5. Track record / risk culture** | came through 2008/2020 intact — **even acquired the weak** | needed a rescue/dilution *last* time (repeat offender: Citi also rescued ~1991) |

*Mnemonic: **thick capital · sticky deposits · no toxic concentration · diversified model · didn't beg for help last crisis.***

**Three process guardrails (in case the screen misses):**
1. **Buy a small BASKET (3–5 fortress names), not one stock.** This is the correct middle ground between a single name (Citi risk) and the whole ETF (diluted by the weak). Diversify away idiosyncratic blow-ups (fraud, litigation, a single-firm run).
2. **Scale in and wait for the survival signal.** The [S&P §7.2](report_en) result — averaging in over 1–6 months ≈ nailing the bottom — means you can *confirm* survival before committing: did it withstand the funding run without a **massively dilutive** raise? **A forced dilution / tapping emergency facilities / seizure = the casualty tell** (Citi's serial 2008–09 dilutions and near-nationalization were an observable "avoid" signal, even though it bounced +264% in year 1).
3. **Buy *after* the capital raise, with a margin of safety.** Don't buy before a dilutive raise (you get diluted). Distinguish a **fear** discount to tangible book (buyable) from an **insolvency** discount (a death notice — avoid).

**Live "survival signal" you can watch mid-crisis:** 🟢 needs no rescue, or *opportunistically* acquires the weak (JPM → Bear/WaMu/First Republic); 🔴 survives only via emergency facilities (discount window/BTFP), a 50%+ dilutive raise, rating cuts, unstemmed deposit flight, or seizure.

> **Net:** screen out ~90% of "Citis" *ex ante* on **capital + funding + concentration**; catch the residual tail with a **basket + scale-in + survival-signal + tangible-book margin of safety.** This maps to the Day1Global **Module C (cash flow) / L (ownership & dilution risk) / O (accounting quality: AFS/HTM marks)**.

---

## Reproduce it yourself
```
cd tail_hedge
python run_backtest_sectors.py   # pulls XLF/XLK (yfinance) -> data/results_sector_*.csv
python run_backtest_stocks.py    # JPM/AXP quality names (§6) -> data/results_stock_*.csv
python run_crisis_dipbuy.py      # crisis dip-buy evidence (§7) -> data/results_crisis_dipbuy.csv
```

## Sources
- yfinance / Yahoo Finance — XLF, XLK daily adjusted close + live option chains.
- Sibling studies: [S&P 50-yr backtest](report_en), [VLCC (DHT/FRO)](report_vlcc_en), [AI-bubble §11](../ai_bubble/report_en).
- N. N. Taleb, M. Spitznagel, AQR / Ilmanen (VRP); repo `RULES.md` CRule 1 / CRule 5.

---

*Two-Step Research Protocol applied (§1 draft + §2 review). Bilingual mirror: [中文版 →](report_sectors_cn). Data: [`data/`](data/). Education/analysis only — not investment advice.*

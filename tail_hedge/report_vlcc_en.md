---
layout: default
title: VLCC Convexity Hedging — DHT/FRO Backtest & a Win-Rate-vs-VRP Framework
---

# VLCC Convexity Hedging: DHT / FRO
## Does deep-OTM tail-hedging work on a large VLCC position — and how much can you overpay?
### July 20, 2026 — Applied convexity study (backtested)

> **Why this exists**: extends the [tail-hedging / convexity backtest](report_en) from the S&P to **VLCC equities (DHT, FRO)** — the assets a large tanker holder actually owns. Three questions: (1) does buying deep-OTM puts protect a long VLCC position? (2) how **reliable** is that protection across scenarios (fast crash vs slow cyclical grind, strike depth, tenor)? (3) how does the answer depend on the **vol-risk-premium (VRP = how overpriced the puts are)** — i.e., **how do you compute the "win-rate" of the hedge as a function of VRP?** Code: [`run_backtest_vlcc.py`](run_backtest_vlcc.py); data: [`data/`](data/).

> **TL;DR verdict**
> 1. **VLCC is a different animal.** DHT annualized vol **48%**, FRO **61%** (vs S&P 17%), with **−97% / −98%** drawdowns. Tanker downturns are **slow multi-year grinds** — the exact regime that defeats short-dated puts (report §7.5).
> 2. **The core new metric — CAGR break-even VRP.** For **DHT**, tail-hedging with a **1-year 30%-OTM rolled put raises CAGR as long as you pay a VRP below ≈ 67%** (i.e., IV up to ~1.67× realized). For the **S&P that break-even VRP is ≈ 0%.** **The fatter the tail, the more you can overpay for insurance.**
> 3. **But it is asset- and regime-specific — not universally reliable.** **FRO's** break-even VRP is **≈ 0%** (its 61% vol makes premiums brutal, and the 2011–12 restructuring + choppy grind defeat the rolled put). And **DHT's entire positive contribution came from essentially ONE year (2011, −83%)** — extreme lumpiness.
> 4. **Win-rate is the wrong headline.** The hedge "wins" only **16% (DHT) / 4% (S&P)** of one-year periods — you are "wrong" most of the time *by design*. Use **expectancy, the CAGR break-even VRP, and the insurance-value band**, conditioned on **entry vol** (buying puts *after* vol spikes is a near-guaranteed loss).
>
> *Education/analysis, not investment advice.*

---

## ⚠️ Protocol Notice & Caveats

Applies the repo's **Two-Step Research Protocol** and connects to **CRule 5** (buy protection when vol is low / everyone is greedy) and **CRule 8** (pre-committed convex exits). §1 Step-1 draft; §2 Step-2 review; §3 results; §4 the win-rate-vs-VRP framework; §5 VLCC-specific VRP thinking; §6 practical takeaways.

**Data**: DHT (2005-10 → 2024-12) and FRO (2005-01 → 2024-12) daily **adjusted** close (splits + dividends), yfinance. S&P from the sibling study for comparison. Puts priced by Black-Scholes, IV = trailing 63-day realized vol × (1 + VRP); **PASSIVE rolled** put (the design that dominated §7.5).

**Read these caveats before trusting any number:**
- **Window bias**: 2005 start is near a cyclical **peak**; the window includes the worst tanker depression in history (2009–2018). Buy-and-hold DHT/FRO **lost money** over this window (that is *why* it is a good hedge stress-test — not a claim the stocks are bad). A holder who bought in 2020–22 has a totally different experience.
- **FRO 2011–12 restructuring** is a near-total wipeout / credit-event embedded in the continuous ticker — treat FRO pre-2013 with care; **DHT is the cleaner case.**
- **VLCC options are illiquid** (thin, wide bid-ask) → the *real* VRP you pay is high and uncertain; frictions eat into the break-even cushion.
- Options modeled on the **adjusted (total-return)** series (real puts are on price — minor distortion). Gross of tax / transaction cost.

---

# Section 1 — Step 1: Concise Research Draft

**Core conclusion (first):** For a concentrated long VLCC position, deep-OTM long-dated put hedging **can raise the geometric return and is worth a *much higher* vol-risk-premium than for an index** — because the tail (−97%) is so catastrophic that avoiding it justifies a large EV-negative premium. **But the protection is neither cheap nor reliable across assets/regimes**: it works for DHT (break-even VRP ≈ 67%), fails for FRO (≈ 0%), is dominated by a single crash year, and is destroyed if you initiate after volatility has already spiked. The right decision variable is not win-rate but the **CAGR break-even VRP vs the VRP you actually pay.**

**3 supporting points** *(claim → evidence needed)*:
1. **Claim:** VLCC's fat tail raises the tolerable VRP far above an index's. → *Evidence:* DHT CAGR break-even VRP ≈ 67% vs S&P ≈ 0% ([breakeven_vrp](data/results_vlcc_breakeven_vrp.csv)); DHT mean 1-yr put payoff 4.9% vs S&P 0.4%.
2. **Claim:** Long-dated beats short-dated on these slow grinds. → *Evidence:* DHT 252-day puts beat 63-day at every strike/VRP ([hedge_grid](data/results_vlcc_hedge_grid.csv)).
3. **Claim:** Cheap protection materially cuts the VLCC drawdown. → *Evidence:* DHT maxDD −97% → −78% (k20% 1y VRP0) while lifting CAGR (−6.2% → +0.7%).

**2 opposing / counter points** *(claim → evidence needed)*:
1. **Claim:** It is not reliable — asset/regime/luck dependent. → *Evidence:* FRO break-even VRP ≈ 0% (hedge is a net drag); DHT's positive value came almost entirely from **2011** (+49% hedge P&L in a −83% year; most other years −5% to −15%) ([reliability](data/results_vlcc_reliability.csv)).
2. **Claim:** Entry timing (vol regime) can flip the sign. → *Evidence:* buying 1-yr puts in high-IV years (2009, 2015) *lost* 37–40% even as the stock fell — the "re-buy at peak IV" trap, amplified by 48–61% vol.

**Explicitly unknown (not fabricated):** the *real* VRP a VLCC holder pays (options illiquid — likely high, unmeasured here); whether the next tanker downturn is a fast crash or a slow grind; results net of the wide bid-ask on DHT/FRO options; how much of FRO's failure is the 2011–12 restructuring artifact.

---

# Section 2 — Step 2: Strict Peer Review (draft NOT rewritten)

**1. Facts that need verification**
- DHT/FRO adjusted series continuity through splits & the FRO 2011–12 restructuring (yfinance adjustment quality); verify vs company filings.
- Break-even VRP (67% DHT) is window-dependent (2005 near-peak start); verify on sub-windows (e.g., 2013+, 2019+).
- BS with IV = realized×(1+VRP) is a proxy; VLCC option skew is steep and IV is often > this — verify against real DHT/FRO option chains if obtainable.

**2. Logical leaps / equivocation**
- **"Break-even VRP 67%" ⇄ "hedging DHT is safe."** The 67% is a *historical average* dominated by one year; it is not a guarantee for the next cycle.
- **"VLCC tail is fat, so hedge" conflates DHT and FRO** — they diverge sharply; do not generalize "VLCC."
- **CAGR-positive ≠ EV-positive** — the hedge is EV-negative above ~0% VRP; its value is purely the geometric/ergodicity benefit. Don't sell it as "free."

**3. Missing counterexamples / competing explanations**
- **Just trim the position** (AQR de-risk): for an illiquid-option asset, holding less DHT/more cash may beat paying wide option spreads — untested here.
- **Dividends as a natural hedge**: DHT/FRO pay 20–40% yields at cycle peaks; the income cushion (already in the adjusted series) competes with paying put premium.
- **Freight derivatives (FFA)** hedge the *rate* (the actual earnings driver) more directly and liquidly than equity puts — a competing convex hedge not tested.

**4. Most important primary sources to add**
- DHT/FRO option chains (real IV/skew) to measure the *actual* VRP paid.
- Clarksons/Baltic TD3C to align the equity hedge with the underlying freight cycle.
- Company filings on the FRO 2011–12 restructuring and DHT/FRO split history.

**5. Sentences that are at most speculation, not fact**
- "the more you can overpay for insurance" as a forward statement (it is a backward-looking average).
- "works for DHT, fails for FRO" as a durable property (both are one 20-yr path).
- any implied prediction about the next downturn's speed.

---

# Section 3 — Results

Full tables in [`data/`](data/). All returns from **adjusted (total-return)** series.

## 3.1 Risk profile — VLCC vs S&P → [`results_vlcc_profile.csv`](data/results_vlcc_profile.csv)

| Asset | Ann. vol | maxDD | Worst day | Best day | Unhedged CAGR (window) |
|---|---|---|---|---|---|
| **DHT** | **48%** | **−97%** | −26% | +27% | **−6.2%/yr** (2005–24) |
| **FRO** | **61%** | **−98%** | −41% | +38% | **−4.7%/yr** (2005–24) |
| S&P 500 | 17% | −57% | −21% | +12% | +8.4%/yr (1974–24) |

*VLCC vol is ~3× the index and drawdowns near-total. Over this full-cycle window (starting near a peak) both names lost money — the reason a tail hedge could add so much, and the reason to read every number as window-conditional.*

## 3.2 Reliability grid — strike × tenor × VRP (DHT) → [`results_vlcc_hedge_grid.csv`](data/results_vlcc_hedge_grid.csv)

| DHT hedge | CAGR | maxDD | | FRO same | CAGR |
|---|---|---|---|---|---|
| UNHEDGED | −6.2% | −97% | | UNHEDGED | −4.7% |
| k20% **1yr** VRP0 | **+0.7%** | −78% | | k20% 1yr VRP0 | −6.2% |
| k30% 1yr VRP0 | +0.7% | −83% | | k30% 1yr VRP0 | −6.0% |
| k30% 1yr VRP50% | −4.3% | −90% | | k30% 1yr VRP50% | −14.2% |
| k30% **3mo** VRP0 | −2.1% | −91% | | k30% 3mo VRP0 | −1.6% |

*Two lessons: (i) **1-year beats 3-month** for DHT (slow grind); (ii) the **same hedge that helps DHT hurts FRO** — reliability is asset-specific, not a property of "VLCC."*

## 3.3 Win-rate vs VRP (canonical: 1-yr put, DHT/FRO 30%-OTM, S&P 20%-OTM) → [`results_vlcc_winrate_vrp.csv`](data/results_vlcc_winrate_vrp.csv)

| Asset | VRP | Win-rate | Expectancy | Payoff ratio | **CAGR delta** |
|---|---|---|---|---|---|
| **DHT** | 0% | 16% | +0.1% | 5.4 | **+6.83pp** |
| DHT | 50% | 12% | −5.4% | 2.5 | **+1.83pp** |
| DHT | 100% | 9% | −11.2% | 1.8 | −3.63pp |
| **FRO** | 0% | 18% | −2.5% | 2.8 | −1.30pp |
| FRO | 50% | 13% | −9.9% | 1.5 | −9.50pp |
| **S&P** | 0% | 4% | −0.4% | 9.9 | −0.42pp |
| S&P | 50% | 4% | −1.9% | 3.5 | −2.40pp |

*Win-rate is **4–18%** everywhere — you lose premium most years. Yet DHT's CAGR *rises* +6.8pp at VRP0: a low-win-rate, high-payoff-ratio (5.4) convex bet can be strongly geometrically positive. **This is exactly why win-rate alone is the wrong metric.***

## 3.4 The headline framework — break-even VRP → [`results_vlcc_breakeven_vrp.csv`](data/results_vlcc_breakeven_vrp.csv)

| Asset | Mean 1-yr put payoff | **Expectancy break-even VRP** | **CAGR break-even VRP** |
|---|---|---|---|
| **DHT** (30%-OTM) | 4.9% | ~0% | **≈ 67%** |
| FRO (30%-OTM) | 5.4% | ~0% | ≈ 0% |
| S&P (20%-OTM) | 0.4% | ~0% | ≈ 0% |

- **Expectancy break-even VRP** = where mean payoff = mean premium. ~0% for all → at realized vol the puts are roughly *fairly* priced to their average payoff; any overpricing makes the raw bet EV-negative.
- **CAGR break-even VRP** = where hedged CAGR = unhedged. **DHT ≈ 67%**, FRO ≈ 0%, S&P ≈ 0%.
- **The gap [0%, 67%] for DHT is the "insurance-value band"** — the range of VRP where the hedge is EV-negative *but still raises CAGR* (pure ergodicity/variance-drain value from dodging the −97% tail). For FRO and the S&P that band is ≈ zero.

## 3.5 Reliability / lumpiness — annual hedge P&L (30%-OTM 1-yr, VRP 50%) → [`results_vlcc_reliability.csv`](data/results_vlcc_reliability.csv)

| DHT year | Underlying | Hedge P&L | | Note |
|---|---|---|---|---|
| **2011** | **−83%** | **+49.4%** | | the one year that carried the whole hedge |
| 2009 | −31% | **−40.8%** | | bought puts at post-2008 **peak IV** → paid ~41%, stock only −31% |
| 2008 | −48% | +1.0% | | barely paid (slow grind, not a fast crash) |
| most other years | mixed | −5% to −15% | | steady premium bleed |

*Two brutal, honest lessons: **(a)** the hedge's value is **lumped into ~one event** (2011) — extreme fragility; **(b)** initiating in a high-IV year (2009, 2015) *lost* 37–41% even as the stock fell — the peak-IV trap, amplified by 48–61% vol. **When you buy the hedge matters more than that you buy it.***

---

# Section 4 — How to Compute the "Win-Rate" vs VRP (the framework)

Raw win-rate (4–18%) is **useless as a standalone** for a convex hedge — you are meant to lose small premiums most of the time and win big rarely. Here is the decision procedure that actually works, as a function of VRP:

**Step 1 — Estimate the VRP you actually pay.**
`paid_VRP = (market option IV / trailing realized vol) − 1`. For thin VLCC options this is high and uncertain; use a conservative (high) estimate.

**Step 2 — Compute the two break-even VRPs (from history or a model).**
- `expectancy(VRP) = mean(payoff) − mean(premium(VRP))` → **expectancy break-even VRP** (raw +EV boundary).
- `ΔCAGR(VRP) = CAGR_hedged − CAGR_unhedged` (from a backtest) → **CAGR break-even VRP** (the one that matters for a compounder).

**Step 3 — Decide by the CAGR break-even, not the win-rate.**
> **Hedge iff `paid_VRP < CAGR-break-even-VRP` (with a margin for frictions).**
> DHT ≈ 67% → lots of room; FRO ≈ 0% and S&P ≈ 0% → only hedge if you can buy at/below realized vol (rare).

**Step 4 — Report win-rate correctly (three numbers, not one):**
1. **Unconditional** win-rate (low — *ignore as a decision input*).
2. **Regime-conditional** win-rate: P(hedge pays | annual decline > X%) — high; this is the number that describes the insurance.
3. **Magnitude-weighted expectancy** = win-rate × avg-win − loss-rate × avg-loss, plus the **payoff ratio** (DHT 5.4 at VRP0). A 16%-win / 5.4-payoff-ratio bet is ≈ EV-neutral and **geometrically positive** — which the CAGR delta confirms (+6.8pp).

**Step 5 — Condition on entry vol.** Compute all of the above *only for initiations when vol is low* (cycle top). §3.5 shows initiating at high IV (mid-crash) turns the hedge into a guaranteed loss. **The single biggest lever is buying the hedge cheap, at the top of the cycle (CRule 5).**

---

# Section 5 — VLCC-Specific VRP Thinking

1. **Fatter tail → higher tolerable VRP.** The whole reason DHT's CAGR-break-even VRP (67%) dwarfs the S&P's (~0%) is that DHT can fall −97% while the S&P tops out near −57%. Dodging a −97% drawdown is worth an enormous EV-negative premium (a −90% loss needs +900% to recover; the variance/skew drain is colossal). **For catastrophic-tail cyclicals, tail insurance is *structurally* more valuable than for an index.**
2. **…but the grind and the premium fight back.** VLCC downturns are **multi-year grinds**, so you must **re-buy and re-pay** premium through the whole decline (the FRO failure). And 48–61% vol makes even 30%-OTM puts expensive. Net: the hedge only wins if the eventual drawdown is *deep enough* to overcome years of premium — true for DHT's −97%, not reliably for FRO.
3. **Entry-vol is destiny.** Because IV explodes once the cycle turns, the hedge must be **established at the top, when vol is low and complacency high** — precisely CRule 5's "buy protection when everyone is greedy." Buying after the first −30% is a near-guaranteed loss (§3.5).
4. **Dividends are a partial natural hedge.** DHT/FRO pay 20–40% yields near peaks; that income cushions the position and *competes* with paying put premium — one reason a dividend-harvesting holder may rationally under-hedge.
5. **Options are thin — consider substitutes.** Real DHT/FRO option spreads are wide, so the *paid* VRP is high and may exceed even DHT's 67% cushion. Practical convex alternatives: **trim the position at the cycle top (de-risk), hold a cash buffer, or hedge the freight rate via FFAs** (which track the actual earnings driver more liquidly than equity puts).

---

# Section 6 — Practical Takeaways for a Large VLCC Holder

- **Tail-hedging a concentrated VLCC book *can* be worth a lot** — DHT's history says you could overpay up to ~67% VRP and still raise CAGR — **but only with long-dated (≥1yr) deep-OTM puts, bought at the cycle top when vol is low.**
- **Do not trust it as reliable insurance.** It is asset-specific (DHT yes, FRO no), lumpy (one event carried DHT), and lethal if initiated mid-crash at peak IV. Size it as a *small convex sleeve*, not a portfolio pillar.
- **Compute the decision correctly:** compare your *paid* VRP to the **CAGR break-even VRP**, not the win-rate. If VLCC option spreads push your paid VRP above the break-even, **de-risk (trim) or use FFAs instead.**
- **This is CRule 5 + CRule 8 in options form:** buy cheap protection when the cycle is euphoric and vol is low; pre-commit the exit; and never chase insurance after the crash has started.

> **Bottom line:** the convexity logic that was marginal for the S&P is **materially stronger for a catastrophic-tail cyclical like DHT** — the fat tail buys you a wide VRP cushion (~67%). But VLCC's slow grinds, high premiums, thin options, and one-event lumpiness make it **fragile and timing-dependent**: worth doing *small, long-dated, and bought at the top* — or replaced by simple de-risking when the options are too dear.

---

## Reproduce it yourself
```
cd tail_hedge
python run_backtest_vlcc.py   # pulls DHT/FRO (yfinance) -> data/results_vlcc_*.csv
```

## Sources
- yfinance / Yahoo Finance — DHT, FRO daily adjusted close.
- Sibling study: [Tail-Hedging & Convexity — 50-Year Backtest](report_en) (S&P baseline, §7.5 passive-vs-ladder).
- N. N. Taleb (*Antifragile*), M. Spitznagel (*Safe Haven*), AQR / Ilmanen (VRP); repo `RULES.md` CRule 5 / CRule 8.

---

*Two-Step Research Protocol applied (§1 draft + §2 review). Bilingual mirror: [中文版 →](report_vlcc_cn). Data: [`data/`](data/). Education/analysis only — not investment advice.*

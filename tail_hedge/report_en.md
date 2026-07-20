---
layout: default
title: Tail-Hedging & Convexity — A 50-Year Backtest (1974–2024)
---

# Tail-Hedging & Convexity: A 50-Year Empirical Test
## Does buying tail protection actually raise the geometric return?
### July 20, 2026 — Framework research (backtested, not theory)

> **Why this exists**: we had discussed the Taleb/Spitznagel *tail-hedging / convexity* thesis — spend a little on deep-OTM puts, monetize the spikes, and (allegedly) **raise your geometric return (几何收益率) while cutting drawdown**, compensating for the fat-tail fragility of the Kelly criterion. Theory is cheap. This page **backtests it on 50 years of real S&P 500 total return (1974–2024)** and reports what actually happened. All result tables are committed as CSVs in [`data/`](data/) and reproduced by [`run_backtest.py`](run_backtest.py).

> **TL;DR verdict — the theory is REAL but NOT a free lunch; price is destiny.**
> 1. **Convexity genuinely reshapes the distribution.** A put overlay turned Buy&Hold's fat left tail (**skew −0.90, kurt 3.67**) into a symmetric one (**skew ≈ +0.02, kurt ≈ 0.2**) and **clipped the worst month from −19.4% to −6.3%.**
> 2. **When protection is cheap it wins on every axis.** Cheap puts raised CAGR **7.80% → 8.57%**, cut vol 12.6% → 10.7%, cut maxDD **−51.8% → −38.6%**, and lifted Sharpe 0.66 → 0.83.
> 3. **Your instinct to use LONG-dated puts is correct.** A 1-year (LEAPS) put **halved the drawdown (−40% → −21%)** while barely denting CAGR — far better than short 1-month puts, which bleed through slow bear markets.
> 4. **But at realistic option pricing it costs CAGR.** With a normal vol-risk-premium (VRP 25–50%), the hedge gives up **~0.4–1.4%/yr of CAGR** to buy that protection — and if bought *too* expensively (VRP 50%) it can **deepen** drawdown via premium bleed (−54.4% > −51.8%). This is exactly the **AQR vs Universa** debate, and the data shows *both* can be right.
> 5. **Fair fight (equal drawdown), convexity wins — but narrowly.** Tuned to the same −40% maxDD, the put hedge beat a cash barbell **6.13% vs 5.81% CAGR** — a real but thin edge.
>
> *Education/analysis, not investment advice.*

---

## ⚠️ Protocol Notice

Applies the repo's **Two-Step Research Protocol** (`.github/copilot-instructions.md`). §1 = Step-1 concise draft; §2 = Step-2 strict peer review; §3 = results (with data links); §4 = reflection; §5 = limitations; §6 = practical takeaways. This is a **cyclical/portfolio** research page, so it also leans on **Kelly / geometric-return** logic and ties back to the repo's **CRule 8** (pre-committed convex exits).

**Data**: Robert J. Shiller monthly *Real Total Return Price* (dividends reinvested, CPI-adjusted), 1974-08 → 2024-07 (600 months = 50.0y). Derived series: [`data/shiller_real_tr_monthly_1974_2024.csv`](data/shiller_real_tr_monthly_1974_2024.csv).
**Method**: rolling OTM puts priced by Black-Scholes with IV = trailing 12-month realized vol × (1 + **VRP**), where VRP is the vol-risk-premium markup (the price-of-insurance knob). Full code: [`run_backtest.py`](run_backtest.py).
**⚠️ Key caveat**: Shiller monthly prices are **month-averages**, which smooth fast intra-month crashes (1987, 2020). Measured drawdowns are therefore understated, and the hedge value reported here is **conservative (biased against the hedge)**. Results are gross of tax and transaction costs.

---

# Section 1 — Step 1: Concise Research Draft

**Core conclusion (first):** Buying tail protection **does** raise the *geometric* return and cut drawdown **when the insurance is cheap enough**, because truncating deep left-tail losses has a convex benefit to compounding that can exceed the premium bleed. But the effect is **entirely conditional on the price paid (the vol-risk-premium)**: at realistic option prices the hedge modestly *lowers* CAGR while still meaningfully cutting drawdown and tail risk — so it is best understood as **cheap, disciplined ruin-insurance that complements Kelly**, not as a standalone alpha source.

**3 supporting points** *(claim → evidence needed)*:
1. **Claim:** Convexity truncates the left tail. → *Evidence:* skew −0.90 → +0.02, kurtosis 3.67 → 0.19; worst single month −19.4% → −6.3% (see [tail_shape](data/results_tail_shape.csv)).
2. **Claim:** Cheap protection raises geometric return. → *Evidence:* cheap put (VRP 0) CAGR 8.57% > 7.80% Buy&Hold, with lower vol and drawdown (see [monthly_put_hedge](data/results_monthly_put_hedge.csv)).
3. **Claim:** Long-dated puts protect far better than short-dated. → *Evidence:* LEAPS 1y put maxDD −21% vs Buy&Hold −40% (annual frame) vs 1-month put's −45% (see [leaps_put_hedge](data/results_leaps_put_hedge.csv)).

**2 opposing / counter points** *(claim → evidence needed)*:
1. **Claim:** At realistic pricing the hedge is a net cost — cash is cheaper (AQR). → *Evidence:* at VRP 25–50% the hedge CAGR falls to 6.8% / 4.6% (from 7.8%); a cash barbell reaches similar drawdown reduction (see [baseline_barbell](data/results_baseline_barbell.csv)).
2. **Claim:** The "monetize into the crash" redeploy alpha is unproven here. → *Evidence:* redeploying payoffs into equity changed CAGR by <0.05pp in this dataset — **but** monthly-average data lacks intra-month V-bottoms, so this is **unknown / untestable on this data**, not disproven.

**Explicitly unknown (not fabricated):** the true realized VRP an investor pays (implementation-dependent); the redeploy/rebalancing alpha (needs daily data); whether the next 50 years' crash frequency resembles the last 50; results net of tax/transaction cost.

---

# Section 2 — Step 2: Strict Peer Review (draft NOT rewritten)

**1. Facts that need verification**
- The Shiller "Real Total Return Price" ends 2024-07 (CPI lag drops 2 months); confirm the exact window vs the source.
- BS pricing with IV = realized×(1+VRP) is a *proxy*; real 1-month OTM-put IV embeds skew that may exceed a flat VRP multiplier — verify against actual option chains / CBOE PPUT-style indices.
- Buy&Hold 50-yr real CAGR 7.80% is window-sensitive (1974 start = post-crash cheap; ending 2024 = elevated); verify robustness on rolling windows.

**2. Logical leaps / equivocation (concept substitution)**
- **"Raises geometric return" is true only in the VRP≈0 cell.** The headline must not generalize the cheap case to all cases.
- **"Drawdown" is conflated across frames** — monthly maxDD (−51.8%) vs annual maxDD (−40.0%) are different measures; LEAPS must be compared *within* the annual frame.
- **"Hedge vs cash" is not apples-to-apples** unless tuned to equal drawdown (done in §3.4) — otherwise you compare different risk levels.

**3. Missing counterexamples / competing explanations**
- **2018-style tightening / calm decades**: long bleed periods where the hedge only costs — the 2010s would punish it; this 50-yr window may over-sample crashes favorable to the hedge.
- **Managed futures / trend-following** provide convex "crisis alpha" with *positive* carry — a competing (possibly cheaper) convexity source not tested here.
- **The variance-drain story is incomplete**: most of the geometric gain comes from removing **negative skew/kurtosis**, not variance per se (variance drain is only ~0.6–0.8%/yr here).

**4. Most important primary sources to add**
- Shiller data page (primary series); CBOE PPUT / tail-hedge index methodology (real put-cost benchmark).
- AQR (Ilmanen) "Understanding the Volatility Risk Premium" and the 2020 AQR-vs-Universa exchange.
- Ole Peters / Taleb on ergodicity (time-average vs ensemble-average growth).

**5. Sentences that are at most speculation, not fact**
- "cheap, disciplined ruin-insurance that complements Kelly" (framing/judgment).
- Any implication that the historical crash frequency will repeat.
- The redeploy-alpha claim (untestable on monthly data).

---

# Section 3 — Results

Full tables live in [`data/`](data/); key rows reproduced below. All returns **real (inflation-adjusted), dividends reinvested**.

## 3.1 Baseline & the AQR "just de-risk" alternative → [`results_baseline_barbell.csv`](data/results_baseline_barbell.csv)

| Strategy | CAGR | Vol | maxDD | worst-12m | Sharpe | ×wealth | skew | kurt |
|---|---|---|---|---|---|---|---|---|
| **Buy & Hold 100% equity** | **7.80%** | 12.6% | **−51.8%** | −40.7% | 0.66 | ×42.8 | −0.90 | 3.67 |
| Barbell 95/5 equity/cash | 7.44% | 11.9% | −49.7% | −39.0% | 0.66 | ×36.2 | | |
| Barbell 90/10 | 7.08% | 11.3% | −47.6% | −37.3% | 0.66 | ×30.5 | | |
| Barbell 80/20 | 6.34% | 10.1% | −43.3% | −33.8% | 0.66 | ×21.6 | | |

*Holding cash lowers drawdown linearly — and lowers CAGR proportionally (Sharpe unchanged at 0.66). No convexity: it can't beat the market's risk-adjusted return, only dilute it.*

## 3.2 Rolling 1-month OTM put — price is destiny → [`results_monthly_put_hedge.csv`](data/results_monthly_put_hedge.csv)

| Hedge (1m put) | Premium/yr | Payoff/yr | CAGR | maxDD | Sharpe | skew |
|---|---|---|---|---|---|---|
| k=5% OTM, **VRP 0 (cheap)** | 1.8% | 2.3% | **8.57%** ↑ | **−38.6%** | **0.83** | +0.08 |
| k=5% OTM, VRP 25% (realistic) | 3.5% | 2.3% | 6.77% ↓ | −43.9% | 0.67 | +0.02 |
| k=5% OTM, **VRP 50% (expensive)** | 5.6% | 2.3% | **4.55%** ↓↓ | **−54.4%** ✗ | 0.47 | −0.05 |
| k=10% OTM, VRP 25% | 0.6% | 0.5% | 7.86% | −47.3% | 0.70 | −0.46 |

*The whole AQR-vs-Universa debate in one table: **cheap → wins on every axis; expensive → loses CAGR AND deepens drawdown** (the premium bleed itself carves a −54% hole).* 

## 3.3 Rolling 12-month LEAPS put — your long-dated design → [`results_leaps_put_hedge.csv`](data/results_leaps_put_hedge.csv)

Compared **within the annual frame** (Buy&Hold annual: CAGR 7.80%, vol 16.4%, maxDD **−40.0%**, ×42.8):

| Hedge (1y LEAPS put) | Premium/yr | CAGR | Vol | maxDD | ×wealth |
|---|---|---|---|---|---|
| **k=10% OTM, VRP 0** | 1.3% | **8.15%** ↑ | 14.2% | **−21.0%** | ×50.3 |
| k=10% OTM, VRP 25% | 2.0% | 7.38% | 14.2% | **−22.4%** | ×35.2 |
| k=10% OTM, VRP 50% | 2.9% | 6.52% | 14.2% | −23.9% | ×23.6 |
| **k=20% OTM, VRP 25%** | 0.6% | **7.40%** | 16.0% | −37.6% | ×35.5 |

*The standout result: a 1-year put **halves the drawdown (−40% → ~−22%)** while costing only ~0.4%/yr of CAGR at realistic pricing — dramatically better protection-per-dollar than 1-month puts, because it captures the **cumulative** decline of slow bear markets (2000-02, 2008) that a monthly put keeps re-paying premium to miss. **This validates using long-dated protection.***

## 3.4 Fair fight: equal-drawdown comparison → [`results_equal_drawdown.csv`](data/results_equal_drawdown.csv)

Both defenses tuned to the **same −40% maxDD**:

| Defense (targeted to −40% maxDD) | maxDD | CAGR | Sharpe |
|---|---|---|---|
| Cash barbell (27% cash) | −40.1% | 5.81% | 0.66 |
| **Put hedge (k=5%, VRP 25%, 1.55× notional)** | −40.0% | **6.13%** | 0.64 |

*At equal drawdown, convexity beat linear de-risking by **+0.32%/yr** — real, but thin, and it flips to the barbell if VRP is high.*

## 3.5 Left-tail shape → [`results_tail_shape.csv`](data/results_tail_shape.csv)

| | skew | kurt | Worst 6 single months |
|---|---|---|---|
| Buy & Hold | −0.90 | 3.67 | −19.4, −18.7, −12.4, −12.1, −11.6, −11.1% |
| Hedged (realistic) | +0.02 | 0.19 | all clipped to ≈ **−6.2 to −6.3%** |

*The put literally **caps the monthly loss** and converts a left-skewed, fat-tailed distribution into a symmetric one — textbook convexity.*

## 3.6 Convexity in the 5 major crashes → [`results_crash_episodes.csv`](data/results_crash_episodes.csv)

Hedge = 1-month k=10% OTM, VRP 25% (weak/short version; **understated by month-average smoothing**):

| Episode | Buy & Hold | Hedged | Protection |
|---|---|---|---|
| 1973–74 bear | −46.0% | −44.5% | +1.6pp |
| 1987 crash | −19.1% | −15.4% | +3.7pp |
| 2000–02 dot-com | −38.4% | −37.7% | +0.7pp |
| 2008 GFC | −41.9% | −36.0% | +5.8pp |
| **2020 COVID** | −12.3% | −3.5% | **+8.8pp** |

*Short-dated puts shine in **fast** crashes (2020, 1987, 2008's sharp legs) and bleed through **slow** grinds (2000-02) — the case for **long-dated** puts (§3.3).*

---

# Section 4 — Reflection & Synthesis

**What the data CONFIRMED about the theory**
1. **Convexity is real and measurable** — the hedge flipped skew from −0.90 to ≈0 and capped the worst month at −6.3%. This is the "cut the left tail" mechanism, verified.
2. **The geometric-return claim holds *when protection is cheap*** — cheap puts raised CAGR 7.80% → 8.57% *and* cut risk. The mechanism the theory describes is genuine, not a mirage.
3. **A subtler, sharper finding:** the geometric benefit comes **mostly from removing negative skew/kurtosis (deep drawdowns), not from reducing variance.** Pure variance-drain here is only ~0.6–0.8%/yr; the real prize is **truncating the fat left tail.** This refines the naïve "½σ²" story.
4. **Long-dated beats short-dated decisively** — validating the user's design (long-term puts + monetize), because LEAPS capture the *cumulative* decline of slow bears while monthly puts keep paying premium to miss them.

**What the data QUALIFIED or pushed back on (the AQR side)**
1. **No free lunch — price is destiny.** Every result hinges on the vol-risk-premium. At realistic VRP (25–50%, since OTM puts are structurally over-priced by skew) the hedge **gives up 0.4–1.4%/yr of CAGR**; bought too dear it can even **deepen** drawdown via bleed.
2. **The "buy-the-dip" redeploy alpha did not show up** (ΔCAGR < 0.05pp) — honestly, because month-average data has no intra-month V-bottoms. **Untestable here, not disproven.**
3. **This 50-yr window is crash-rich** (1973-74, 1987, 2000-02, 2008, 2020). A calm decade like the 2010s would make the hedge look far worse; survivorship of *crashes* flatters it.

**The reconciliation (both camps are partly right)**
- **Universa/Taleb are right** that convexity, bought cheaply and held long-dated, raises the geometric return and slashes tail risk — the data shows it plainly.
- **AQR/Ilmanen are right** that *systematically* buying over-priced protection is a drag, and that a cash barbell achieves much of the drawdown reduction more simply. The edge of convexity over de-risking at equal drawdown was only **+0.3%/yr** — real but fragile.
- The decisive variables are exactly the three the theory hand-waves: **(a) the price paid, (b) the tenor/strike (long & deep = cheap protection-per-dollar), (c) disciplined monetization.**

---

# Section 5 — Limitations (read before trusting any number)

1. **Month-average smoothing** understates fast crashes → hedge value here is *conservative*.
2. **VRP is modeled, not observed** — a flat multiplier on realized vol; real OTM-put skew may be steeper, worsening the realistic cases.
3. **No taxes, no transaction/roll costs, no bid-ask** — all of which hurt an active option-rolling strategy more than Buy&Hold.
4. **Monthly European settlement** ≠ a real ladder of American LEAPS monetized on +100%/+200% spikes; §3.3 is a *proxy* for that design.
5. **One market, one 50-yr path** — not a distribution of futures; the redeploy alpha and calm-decade drag are under-represented.

---

# Section 6 — Practical Takeaways

- **Convex tail-hedging is not an alpha machine; it is disciplined ruin-insurance** whose value is dominated by the *price* you pay. Buy it **cheap (deep-OTM), long-dated, and monetize with rules** — or don't bother.
- **It "compensates Kelly" in a precise sense:** by truncating the fat left tail (skew −0.90 → 0), it removes the very fragility that makes full-Kelly / leveraged / concentrated positions dangerous — letting you hold more of the growth engine safely. For an **unlevered, long-horizon** investor who can stomach −50%, AQR's "just hold some cash" is the simpler answer.
- **Repo tie-in:** this is the portfolio-level twin of **CRule 8** — a *pre-committed, convex* defense. And it rhymes with the AI-bubble report's §11: the payoff is a hedge against the *tail*, harvested with discipline, not a bet you monetize by staring at the tape.

---

## Reproduce it yourself

```
cd tail_hedge
python run_backtest.py     # re-derives the CSVs in data/ from the Shiller series
```
The script uses the committed [`data/shiller_real_tr_monthly_1974_2024.csv`](data/shiller_real_tr_monthly_1974_2024.csv); if absent it re-downloads Shiller's `ie_data.xls` and rebuilds it.

## Sources
- Robert J. Shiller, online data (S&P monthly, dividends, CPI): http://www.econ.yale.edu/~shiller/data.htm
- N. N. Taleb — *Antifragile*; *Dynamic Hedging* (convexity, tail risk).
- M. Spitznagel — *Safe Haven: Investing for Financial Storms* (geometric-return case for tail hedging).
- AQR / A. Ilmanen — *Understanding the Volatility Risk Premium*; the 2020 AQR-vs-Universa exchange.
- O. Peters & N. N. Taleb — ergodicity economics (time-average vs ensemble growth).

---

*Two-Step Research Protocol applied (§1 draft + §2 review). Bilingual mirror: [中文版 →](report_cn). Data: [`data/`](data/). Education/analysis only — not investment advice.*

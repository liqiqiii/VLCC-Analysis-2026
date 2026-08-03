---
layout: default
title: VLCC Seasonality — Is the Q4 Stock Bump the Calendar, or the Year's Rate Strength? (Aug 2, 2026)
---

# VLCC Seasonality: Does Q4 "Peak Season" Actually Lift DHT / FRO?
## Calendar effect vs. relative rate-strength — a data test
### August 2, 2026 — Cyclical / Seasonality Analysis

> **The user's question, paraphrased:** It's August, heading into Q4 when VLCC TCE is seasonally highest. Does that Q4 rate peak reliably lift the *stock* (DHT/FRO)? Or is Q4 stock performance really about the **relative strength of that particular year's Q4** rather than the calendar?

> **TL;DR — the data answers cleanly: it's the *year's rate strength*, NOT the calendar.**
> - **There is no reliable calendar "Q4 rally."** Over ~16 years, Q4 is a **coin-flip**: DHT positive **50%** of Q4s, FRO **44%** (FRO's Q4 **median = −4.3%**). If "Q4 = peak TCE = stock up" were a calendar law, Q4 would win far more than half the time. It doesn't.
> - **The genuinely strong seasonal quarter is Q1, not Q4** (DHT Q1 **+12.5%** avg, **75%** positive). And the single **worst month is November** (DHT **−5.6%**, positive only **25%** of years).
> - **But the *cross-year* Q4 return is strongly correlated with the *level* of that year's Q4 TCE: R ≈ 0.60 (DHT), 0.66 (FRO).** High-rate Q4s rip (2019 ~\$120k → +36%/+43%; 2014 ~\$75k → +19%/+99%; 2022 ~\$65k → +18%/+11%); low-rate Q4s fall (2021 ~\$12k → −20%/−25%; 2017 ~\$26k → −9%/−24%) — *regardless of it being "peak season."*
> - **Why (CRule 1):** the stock **leads the rate by 1–3 months**, so the *predictable* winter bump is priced **before** Q4 (hence Q1 confirmation strength + a "sell-the-news" November dip). What the stock **can't** pre-price is the **surprise in the level** — 2014 oil-crash floating storage, 2019 COSCO sanctions (~\$300k), 2022 Russia rerouting. Those surprises drive the big Q4 moves.
> - **2026 read:** Q1-2026 already delivered a monster move (**DHT +53%, FRO +65%**), front-running the Mar/Jun rate spikes (>\$400k). So buying into Q4 *"because it's seasonal"* is **not an edge**; the edge is a genuine winter **rate surprise above the already-elevated, already-priced base.**
> - **Education/analysis, NOT investment advice.**

---

## ⚠️ Protocol Notice

Applies the **Two-Step Research Protocol** (`.github/copilot-instructions.md`), framed through **Cyclical CRule 1** (stock-vs-rate lead/lag). §1 = fact-base/method. §2 = **Step 1** draft. §3 = **Step 2** review. §4 = seasonality tables. §5 = the correlation test (the answer). §6 = the CRule 1 mechanism. §7 = 2026 positioning. All stock figures are exact (yfinance total return); Q4 TCE levels are **approximate** and clearly flagged (Rule 4).

---

# Section 1 — Fact-base & method

- **Stock data:** DHT & FRO monthly **total-return** series (dividend-adjusted), yfinance, 2010–2026. Quarterly and monthly returns computed from month-end closes. *(Exact.)*
- **Rate data:** approximate **Q4-average VLCC TD3C (MEG→China) TCE**, \$k/day, compiled from public reports (Clarksons / Baltic Exchange / company IR / trade press). **These are estimates** used to illustrate the cross-year *level* relationship; exact figures vary by source, but the qualitative ranking (2019 ≫ 2014 > 2022 > 2015 > … > 2020 > 2021) is well established. *(Rule 4: cross-checked as directional, not precise.)*
- **Sample caveat:** ~16 completed years → small sample; a few outlier years (FRO Q4 2014 +99%) heavily skew *means*, which is exactly why we report **median and win-rate** alongside the mean.
- Reproduce: `vlcc_seasonality/run_seasonality.py` → writes all CSVs to `vlcc_seasonality/data/`.

---

# Section 2 — Step 1: Concise Research Draft

**Core conclusion:** Q4 stock outperformance in VLCC names is driven by **the relative strength of that year's rate level, not by the calendar.** A "buy-for-Q4-seasonality" rule has **no historical edge**; a "buy-when-the-Q4-rate-surprises-high" rule does.

*Supporting (claim → evidence needed):*
1. **No calendar Q4 rally** → Q4 win-rate is ~44–50% (coin-flip), FRO Q4 median negative. *Evidence: quarterly seasonality table (§4) — obtained.*
2. **Q4 return tracks the Q4 rate level across years** → Pearson R ≈ 0.60 (DHT), 0.66 (FRO). *Evidence: §5 correlation table — obtained.*
3. **Seasonal stock strength sits in Q1/late-winter, not Q4** → DHT Q1 75% positive, +12.5% avg; Nov is the worst month. *Evidence: monthly seasonality (§4) — obtained.*

*Opposing (claim → evidence needed):*
1. **Q4 mean IS positive (FRO +5.1%), so a seasonal tilt might still exist** → but it is **outlier-driven** (2013/2014/2019); the median says otherwise. *Evidence: mean-vs-median gap — obtained; need bigger sample to settle.*
2. **TCE levels are estimates, so the 0.6 correlation may be soft** → *Evidence: exact quarterly TD3C history (Clarksons) would tighten R — **not fully obtained** (approximate).* 

---

# Section 3 — Step 2: Strict Peer Review (draft NOT rewritten)

1. **Facts that need verification:** the **exact quarterly TD3C TCE** history (mine are approximations); whether total-return adjustment fully captures FRO/DHT's large special dividends; the **2018 anomaly** (Q4 rates spiked but stocks fell with the Dec-2018 equity crash — a macro override, worth isolating).
2. **Logical leaps / equivocation:** "correlation with the level" must not be re-read as "the calendar works" — they are *opposite* claims; also, R ≈ 0.6 on n≈13 is **suggestive, not conclusive**; do not treat it as a tradeable certainty.
3. **Missing counterexamples / competing explanations:** **macro years** (2018 crash, 2020 COVID) can swamp the rate signal in either direction; **company-specific** events (FRO fleet/debt changes, DHT buybacks) add noise; the November weakness could be a **tax-loss / risk-off** artifact rather than a shipping fact.
4. **Most important primary sources to add:** Clarksons/Baltic **quarterly TD3C series**; DHT & FRO **10-Q/press** for realized quarterly TCE; a longer stock history (pre-2010) for a bigger seasonal sample.
5. **Sentences that are at most speculation, not fact:** "the stock front-ran the spike" (a characterization consistent with CRule 1, not proof); the "November = sell-the-news" causal story; and the claim that Q4-2026 *needs* a surprise to outperform (a projection).

---

# Section 4 — The seasonality tables

**Quarterly total returns, average / median / % of years positive (2010–2026):**

| Ticker | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| **DHT** avg | **+12.5%** | −1.3% | +0.1% | +0.2% |
| DHT median | +14.2% | −5.4% | +0.7% | +0.8% |
| DHT % positive | **75%** | 47% | 53% | **50%** |
| **FRO** avg | +10.2% | −3.5% | +2.5% | +5.1%* |
| FRO median | +5.6% | −2.2% | +4.1% | **−4.3%** |
| FRO % positive | 56% | 47% | 59% | **44%** |

*\*FRO Q4 mean is positive but **outlier-driven** (2014 +99%, 2019 +43%, 2013 +41%); the **median is −4.3%** and only 44% of Q4s are up. There is no dependable Q4 rally.*

**Monthly average return / % positive — where the "winter bump" actually sits:**

| | Jan | Feb | Mar | … | Sep | Oct | **Nov** | Dec |
|---|---|---|---|---|---|---|---|---|
| **DHT** avg | +5.2% | **+6.6%** | +2.0% | … | +2.0% | +2.1% | **−5.6%** | +2.3% |
| DHT % pos | 65% | 59% | 53% | … | 69% | 56% | **25%** | 50% |
| **FRO** avg | +1.8% | +4.5% | +3.9% | … | +1.9% | +2.8% | **−3.6%** | +7.5% |

**Read:** the seasonal strength clusters in **Jan–Feb (Q1)** and a bit of **Sep–Oct anticipation**. **November is the worst month for both** — the exact *opposite* of a "Q4 peak-season rally." (Full monthly CSVs in `data/`.)

---

# Section 5 — The correlation test (the actual answer)

**Each year's Q4 stock return vs. that year's approximate Q4 TD3C TCE (\$k/day):**

| Year | Q4 TCE (~\$k/day) | DHT Q4 | FRO Q4 |
|---|---|---|---|
| 2019 | **~120** | **+35.5%** | **+42.6%** |
| 2014 | ~75 | +19.1% | **+99.2%** |
| 2022 | ~65 | +17.9% | +11.1% |
| 2015 | ~55 | +11.8% | +13.0% |
| 2013 | ~45 | +57.1% | +41.1% |
| 2023 | ~42 | −3.0% | +8.5% |
| 2024 | ~40 | −13.9% | −36.4% |
| 2016 | ~38 | −0.7% | +0.5% |
| 2018 | ~38 | −16.2% | −4.8% |
| 2025 | ~38 | +2.2% | −4.3% |
| 2017 | ~26 | −9.3% | −24.0% |
| 2020 | ~18 | +5.2% | −4.3% |
| 2021 | ~12 | −20.3% | −24.5% |

> **Pearson correlation (Q4 TCE level vs Q4 stock return): DHT = 0.60, FRO = 0.66.**

The pattern is unmistakable: **the level of the rate, not the calendar, sorts the winners from the losers.** Every big Q4 stock year is a high-rate year; every deep Q4 drawdown is a low-rate year (2021, 2017) or a macro override (2018, 2024). *(2013 is the one high-residual — DHT +57% on a merely-good rate — reflecting a deep-value re-rate off the 2011–12 trough.)*

---

# Section 6 — Why the calendar is weak but the level is strong (CRule 1)

The apparent paradox — "Q4 has the highest rates but no stock edge" — is resolved by **CRule 1: the stock leads the rate by 1–3 months.**

1. **The predictable part is pre-priced.** The winter demand bump (Nov–Feb) is *known every year*. A forward-looking stock discounts it **before** Q4 → the seasonal stock strength shifts **earlier** (Sep–Oct anticipation) and into **Q1** (confirmation via Q4 earnings + the actual Jan–Feb rate peak). By the time "peak season" headlines arrive, it's in the price → the **November "sell-the-news" dip**.
2. **The unpredictable part is what pays.** What the market *can't* pre-price is an **exogenous surprise to the level**: 2014 oil-price-war floating storage, 2019 COSCO sanctions (spot ~\$300k), 2022 Russia rerouting. These make a given year's Q4 *abnormally* strong → that's where the +40–99% quarters come from, and why the return correlates with the **level**, not the calendar.
3. **Corollary:** a calendar rule ("own VLCC for Q4") harvests a coin-flip; a **surprise rule** ("own it when the winter rate breaks *above* what's priced") is where the historical edge lives.

---

# Section 7 — 2026 read & positioning

**Where 2026 sits (as of Aug 2, 2026):**
- **Q1-2026 already delivered the monster move: DHT +53%, FRO +65%.** Per CRule 1 this *front-ran* the Mar/Jun spot spikes (MEG→China printed **>\$400k/day** intraday in Mar & Jun). The seasonal + surprise upside of early-2026 is **largely already in the price.**
- **Current backdrop:** spot \$25–65k/day with sharp spikes; **Q4 FFA ~\$60k+ (a 3-yr high)**; utilization heading to **~92% (highest since 2019)**; structural bull intact (shadow-fleet segmentation, low orderbook, zero material VLCC supply until late-2028 — P-Rule 2/3).
- **The emerging offset:** **record newbuild deliveries late-2026 into 2027** — the classic supply response that historically ends VLCC cycles (CRule 3).

**Framework implication (not advice):**
- **Do NOT add "for the Q4 seasonal."** The data says that's a coin-flip, and 2026's seasonal/surprise leg already fired in Q1.
- **The bar for Q4-2026 stock outperformance is a genuine rate *surprise above* the elevated, already-priced base** — e.g., a fresh sanctions/geopolitical tonne-mile shock — not merely "winter arriving."
- **Watch the calendar tells:** historically, **Sep–Oct anticipation strength → November fade** is the seasonal shape; **Q1-2027 confirmation** is where a *sustained* winter surprise would actually pay in the stock.
- **Exit discipline (CRule 8):** with the stock already +50–65% YTD and newbuilds arriving, treat rate spikes as **trim** opportunities unless a new exogenous surprise resets the level higher.

---

## Reproduce it yourself

```
cd vlcc_seasonality
python run_seasonality.py     # writes data/*.csv (quarterly + monthly seasonality, Q4 corr)
```

**Data files** (`vlcc_seasonality/data/`): `quarterly_returns_DHT.csv`, `quarterly_returns_FRO.csv`, `quarterly_seasonality.csv`, `monthly_seasonality_DHT.csv`, `monthly_seasonality_FRO.csv`, `q4_tce_vs_stock.csv`, `q4_correlation.csv`.

**Sources (accessed Aug 2, 2026):** yfinance (DHT, FRO total-return); Baltic Exchange / Clarksons / company IR & trade press for TD3C TCE ranges (Lloyd's List, Breakwave Advisors, Kpler, Tankers International, Offshore-Industry, Maritime-Hub). **Q4 TCE levels are approximate estimates (Rule 4).**

---

*Two-Step Research Protocol applied (§2 draft + §3 review). Stock data exact; rate levels approximate and flagged. Education/analysis only — not investment advice.*

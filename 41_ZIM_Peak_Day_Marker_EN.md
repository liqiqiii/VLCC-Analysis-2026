---
layout: default
title: "ZIM March 2022 Peak: Volume, Dividends, Rates — and What It Does (and Does Not) Tell Us About the VLCC Top"
---

# 🔎 ZIM's March-2022 Peak — Volume Anatomy, Dividend Mechanics, Rate Timing, and a Back-Test of "Top Flags"

### Using the container-shipping peak as a template for the VLCC equity top — with every claim tested against data

*October 13, 2026 — VLCC Analysis Series #41 (v2: fully rebuilt; replaces the earlier hypothesis-only draft)*

> **Disclaimer**: Research only, not investment advice. All numbers come from `zim_peak/run_zim_peak_volume.py` (reproducible; outputs in `zim_peak/data/`, charts in `zim_peak/charts/`). Prices: Yahoo Finance daily bars via yfinance (`Close` is split-adjusted only). **Total return (TR) here is a gross wealth index built from prices plus dividends, W_t = W_{t−1}·(P_t + D_t)/P_{t−1}, before withholding tax** — *not* Yahoo's "Adj Close", which overstates ex-date returns. Primary sources: ZIM press releases (9-Mar-2022, 23-Mar-2022), FINRA consolidated short-interest API, Shanghai Shipping Exchange SCFI (two independent GitHub copies, identical except 3 weeks of 2012), Drewry WCI (Drewry text via worldports.org / airfreight.news). In-sample study of 14 hand-picked listed shipping names; delisted firms excluded (survivorship bias possible).

---

## Step 1 — Research draft (core conclusion first)

**Core conclusion.** ZIM's top was not a single "+8% day on 3/31". It was a six-session price high (Mar 14–21, 2022). Its **total-return high was recorded on the $17 ex-dividend date (Mar 22)**. All of this happened **10 weeks after the SCFI freight index had peaked and while SCFI fell nine weeks in a row**. Volume was elevated around the results/dividend window but was **not** a climax. None of eight volume or price "top flags" I back-tested over 2004–2026 showed predictive lift against state-matched comparisons. **There is no validated early-warning signal here.** The transferable lessons are structural: rates and equities diverging, and dividend timing. They are not trading triggers. **Applying the repo's Day1Global and cyclical framework retrospectively to inputs published by 16-Mar-2022 (§7)** gives a reading *consistent with late-cycle risk*: PE 2.27×, orderbook 24.6% of fleet, 36 newbuild charters, and the spot index down 9.5% after 8 straight weekly declines. But the supply-side signals were already present months earlier, and no false-alarm test exists. This is not a validated timing tool.

**Supporting points (claim → evidence needed)**

1. *Equities kept rising after the freight peak* → SCFI weekly series vs equity peak dates. **Have it:** SCFI peaked 7-Jan-2022 and fell 9/9 weeks to 18-Mar (−11.1%). 6 of 9 container equities made their window-high 9–19 weeks *after* the SCFI peak (§5).
2. *The ZIM top was a dividend event in total-return terms* → gross-TR series + ex-date study. **Have it:** the gross ex-day return was +7.12%. The TR high was on 22-Mar. Across 26 tops of dividend-paying shipping stocks, 8 gross-TR highs fell on or within 5 sessions after an ex-date vs ~1.5 under a displaced-calendar comparison (descriptive, §6).
3. *Volume told a story only in hindsight* → RVOL/OBV/distribution measures + back-test. **Have it:** 9 of 10 sessions from 3/9 to 3/22 had RVOL ≥1.5. Price-signed up/down volume flipped from 2.14 (25 sessions before the peak) to 0.40 (25 after). But volume flags did not beat comparable non-volume days (§4, §7).

**Opposing points (claim → evidence needed)**

1. *Consensus-vs-guidance disappointment could have caused the top* → a primary consensus series for FY22 EBITDA as of 8-Mar-2022. **Unknown** (not accessed). The market reaction (+6.3% on 3/9, RVOL 3.0) argues against an immediate disappointment, but it does not rule out one.
2. *VLCC demand is inelastic and the orderbook small, so the container template may not transfer* → a VLCC-specific rate/equity series across several cycles. **Partly unknown:** daily TD3C/BDTI history is not in the repo; BWET is quarantined (§8).

---

## 0. Premise check

| Assumption | Data |
|---|---|
| Peak on 2022-03-31 | **Price close high $88.62 on 3/16; intraday high $91.23 on 3/17; gross-TR high on 3/22 (ex-date).** 3/31 closed $72.71 (−0.2%) on the 409th-largest volume of 734 sessions |
| "+8% hike" on the peak day | No +8% *price* day near the top. **One plausible match:** on a Yahoo-style adjusted chart, 3/22 shows **+8.83%**. The gross TR that day was +7.12%; the raw price change was −12.19%. 3/22 is also where the TR high is recorded. We cannot identify the chart actually seen |
| From ~$100 | Never above $91.23 |
| To ~$6 | **Close $6.59 and intraday $6.39 on 2023-11-28.** Price-only −92.6% from the close high; **gross-TR maximum drawdown −85.0%** (3/22/2022 → 11/28/2023) |

---

## 1. Day-by-day tape, Mar 9 – Apr 6, 2022 (RVOL = volume ÷ prior-20-session average)

| Date | Close | Price % | Volume | RVOL | Vol. rank (of 734) | Note |
|---|---:|---:|---:|---:|---:|---|
| 3/9 | 75.14 | +6.3% | 10.1M | 3.00 | #21 | Q4/FY21 results, $17 dividend, FY22 guide |
| 3/10 | 76.77 | +2.2% | 6.2M | 1.66 | | |
| 3/11 | 78.81 | +2.7% | 7.8M | 2.03 | | |
| 3/14 | 82.54 | +4.7% | 8.8M | 2.15 | #30 | Shenzhen lockdown (news-reported date) |
| 3/15 | 85.24 | +3.3% | 8.3M | 1.94 | | FINRA short interest 5.56M |
| **3/16** | **88.62** | +4.0% | 7.1M | 1.57 | #60 | **Price close high**; Fed's first hike |
| **3/17** | 86.95 | −1.9% | 9.8M | 2.07 | #25 | **Intraday high 91.23**, open 89.30 → close 86.95 |
| 3/18 | 84.50 | −2.8% | 7.3M | 1.42 | | |
| 3/21 | 88.01 | +4.2% | 12.0M | 2.22 | #12 | Last cum-dividend day |
| **3/22** | 77.28 | **−12.2%** (gross TR **+7.1%**) | 12.3M | 2.10 | #11 | **Ex-dividend $17.00; gross-TR high** |
| 3/24–25 | 71.86 / 68.40 | −5.5% / −4.8% | | 1.23 / 0.94 | | |
| 3/28 | 72.34 | +5.8% | 6.3M | 0.92 | #80 | Shanghai lockdown (news-reported date) |
| 3/31 | 72.71 | −0.2% | 2.8M | **0.40** | #409 | Quarter-end; volume dried up |
| 4/4–4/5 | 67.18 / 61.86 | −5.9% / −7.9% | | 1.03 / 1.25 | | $17 paid 4/4 |
| 4/6 | 59.23 | −4.3% | 9.5M | 1.32 | | First gross-TR close below the rally's anchored VWAP; MOM20 trigger |

Closes afterwards: 6/30/2022 $47.23 → 12/30/2022 $17.19 → **11/28/2023 $6.59**.

![ZIM price, gross TR, SCFI, volume, OBV](zim_peak/charts/zim_2022_price_volume_scfi.png)

---

## 2. Verified facts around the peak

| Item | Value | Source / status |
|---|---|---|
| Q4-21 / FY21 net income | $1.71B ($14.17/sh) / $4.65B ($39.02/sh) | ZIM PR 9-Mar-2022 ✅ |
| FY21 adj. EBITDA | $6,597M vs FY20 $1,036M (**+537%**) | ZIM PR table ✅ |
| FY22 guidance | adj. EBITDA $7.1–7.5B (**+7.6% to +13.6%**), adj. EBIT $5.6–6.0B | ZIM PR ✅ |
| Dividend | $17.00/sh (~$2.04B, implying ~120.0M shares). $17 + $2.50 Q3 interim = $19.50 = ~50% of FY21 NI; plus a $2.00 special in Sep-2021 | ZIM PR ✅ |
| Dates | ex 3/22, record 3/23, paid 4/4 | ZIM PR ✅ |
| Withholding | Israeli withholding: 25% general, 30% for substantial holders; reduced rates possible under an ITA ruling | ZIM PR 23-Mar-2022 ✅ |
| Ex-date drop ratio | (3/21 close − 3/22 open)/$17 = **0.82**; close basis 0.63. Withholding may affect ex-dividend pricing; these observations do not identify its contribution | computed |
| Market reaction to results | 3/9 +6.3% (RVOL 3.00), 3/10 +2.2% (RVOL 1.66) | computed |
| Consensus FY22 EBITDA before 3/9 | **Unknown.** Search-engine claims of analyst downgrades could not be sourced and were not used | — |
| Short interest (FINRA, settlement dates) | 2/28 5.01M (4.2% of ~120M shares outstanding) → **3/15 5.56M (4.6%), days-to-cover 1.0** → 3/31 3.79M → 6/30 9.16M (7.6%) → 12/30 17.74M (14.8%, DTC 5.1) | FINRA API ✅ |

**Short interest.** Reported short interest was 4.6% of roughly 120M outstanding shares on 3/15 (float unknown). These observations do **not** establish a short squeeze. Net short interest fell through 3/31 and then rose substantially through the decline. *(The earlier draft's "heavily shorted / short squeeze" is withdrawn.)*

---

## 3. Volume anatomy — what volume did and did not show

| Measure | Reading | Interpretation (descriptive) |
|---|---|---|
| Rally leg 2021-12-20 ($50.67) → 3/16 ($88.62), +74.9% in 59 sessions | RVOL ≥1.5 on **11 sessions through 3/16**: 4 in January (1/11, 1/12, 1/21, 1/24), then 3/7, 3/9–3/11, 3/14–3/16 | Volume expansion was concentrated in the results/dividend window, not spread across the whole rally |
| 3/9 → 3/22 | RVOL ≥1.5 on **9 of 10** sessions (all but 3/18); ≥1.4 on 10 of 10 | Ten straight sessions of elevated volume around results → peak → ex-date |
| Turnover 3/14–3/21 (6 sessions) | **44.4% of ~120M shares outstanding** (free float unknown, so the float figure is higher) | Very heavy turnover at the top |
| Size of peak-day volume | Ranks #11–#60 of 734 (top 1.5–8.2%) | Unusually high, but **all ten largest-volume days came later** (5/2022–12/2023), 7 of them down days, e.g. 6/8/2022 −14.7%, 5/22/2023 −16.2% |
| Up/down volume, price-signed | 25 sessions before peak **2.14** → 25 after **0.40** → 50 after 0.81 | Positive volume imbalance before, negative after. Visible only once the peak was known |
| OBV, price-signed | **Max on 3/16, together with price** → −31.1M by 3/31, −68.8M by 4/29 | **No bearish OBV divergence at the price peak** |
| OBV, gross-return-signed | Max on 3/22 (ex-date counts as an up day) | Same conclusion; the peak shifts with the return convention |
| A/D line (CLV-weighted) | New high on 3/16; series max 2022-05-27 | No divergence at the top |
| Distribution days (down ≥0.2% on higher volume, last 25 sessions) | 6 at the peak; max 9 on 4/21 | The cluster peaked *after* the top |
| Anchored VWAP from the 12/20 low (gross TR) | First close below on **4/6** (15 sessions after the price peak) | Confirms the trend break late |
| Relative, 3/16 → 3/31 | SPY gross +4.0%; ZIM gross **+0.1%**; ZIM price −18.0% | In total-return terms ZIM went flat while the market rallied |

**Takeaway.** Volume described the top well *after the fact*: a burst of turnover around results, peak and ex-date, then a flip to selling volume. At the peak itself, OBV and A/D confirmed price rather than diverging. The largest volume came months later, on down days. §7 tests whether such patterns predict tops in general.

---

## 4. Freight rates vs equity peaks

**SCFI (weekly, Shanghai Shipping Exchange):**

- Peak **2022-01-07 at 5,109.60**. Weekly declines in **9 of 9 weeks** to 3/18 (4,540.31, −11.1%).
- First print ≥5% below the peak: 2/25 (4,818.47). ≥10% below: 3/18.
- Later prints: 3/25 4,434.07 → 6/30 4,216.13 → 12/30 1,107.55 → 3/31/2023 923.78.
- SCFI year-on-year growth peaked on 2021-05-21 (+305%).

**Drewry WCI:** peak $10,377/FEU (Sep-2021) → $8,832.23 on 3/17/2022 (−14.9%) → $8,152.09 on 3/31.

**Equity peaks, window from 2021-06-01 (weeks after the SCFI peak; price | gross TR):**

| Name | Price-peak date | Lag (price) | Lag (gross TR) |
|---|---|---:|---:|
| ZIM | 2022-03-16 | +9.7 | +10.6 |
| GSL | 2022-03-11 | +9.0 | +9.0 |
| DAC | 2022-03-17 | +9.9 | +9.9 |
| MATX | 2022-03-29 | +11.6 | +11.6 |
| Hapag-Lloyd | 2022-05-17 | +18.6 | +18.6 |
| Maersk-B | 2022-01-13 | **+0.9** | +10.4 (TR high 3/21) |
| Evergreen 2603.TW | 2021-07-06 | −26.4 | −26.4 |
| Yang Ming 2609.TW | 2021-07-06 | −26.4 | −26.4 |
| COSCO 1919.HK | 2021-07-07 | −26.3 | −26.3 |

![Peaks vs SCFI](zim_peak/charts/container_peaks_vs_scfi.png)

**Reading.** In this one selected cycle, peak timing was **heterogeneous**: the SCFI level peak did not uniformly precede the equity peaks.

- Within the Jun-2021 to Dec-2022 search window, the three Asian carriers' maxima came in July 2021, about 7 weeks after the SCFI YoY-growth peak.
- Starting the window in Oct-2021 instead, they show secondary highs on 3/4–3/14/2022. On a price-only basis, **7 of 9 names then have their window highs between 3/4 and 3/29/2022**.
- Maersk's price high (1/13) came almost with the SCFI peak.

The one robust observation is that **several equities made new highs while the freight index had already been falling for two months**.

---

## 5. Dividend mechanics — event study and tops

### 5a. Ex-dividend event study

The sample is 465 events in 9 US-listed shipping names, 2004–2026. All figures are gross TR over symmetric 10-return windows, minus the same-segment peer basket (self excluded). Brackets are 95% moving-block bootstrap intervals: 6-month blocks, synchronized across firms.

| Sample | n | 10 sessions before ex-date | ex-date + 9 sessions |
|---|---:|---|---|
| All | 465 | +0.83% [+0.02, +1.75] | −0.95% [−1.83, −0.15] |
| Yield <2% | 275 | −0.37% [−1.33, +0.53] | −0.68% [−1.81, +0.28] |
| Yield 2–5% | 157 | +1.90% [+0.80, +3.11] | −1.10% [−2.35, +0.10] |
| Yield ≥5% | 33 | +5.71% [+0.45, +10.66] | −2.48% [−5.66, +1.13] |
| **Tankers, yield ≥2%** | 167 | **+2.78% [+1.40, +4.42]** | **−1.42% [−2.62, −0.26]** |
| US containers, yield ≥2% | 23 | +0.92% [−3.81, +5.04] | −0.75% |
| Earnings-date coverage available | 422 | +0.75% [−0.14, +1.79] | −0.97% [−1.91, −0.10] |
| … of which no earnings release in the window | 82 | +0.59% [−0.79, +2.27] | **−0.01% [−1.52, +1.25]** |
| Covered, yield ≥2% | 161 | +2.25% [+0.67, +4.13] | −1.33% [−2.75, +0.02] |
| … earnings-clean, yield ≥2% | 36 | +2.24% [+0.14, +5.26] | −0.34% [−2.61, +1.97] |

- **Yield dependence**, estimated as a slope with firm and year fixed effects: pre-ex 0.42 per unit of yield, 95% block CI [−0.17, +1.25]. **Not established.**
- **ZIM 3/22** (yield 19.3%), vs US container peers: +14.4% before the ex-date, +3.1% after (+9 sessions), −3.0% after 20 sessions. Cum-day and ex-day RVOL were 3.7 and 3.8.
- **ZIM's other mega-dividends** did not show the same pattern:
  - 4/4/2023 (yield 27.3%): +1.1% before / +12.8% after.
  - 12/2/2024 (yield 16.6%): −5.9% / +7.9%.
  - 3/24/2025 (yield 17.8%): −13.2% / −0.4%.

![Event study](zim_peak/charts/exdiv_event_study.png)

**Reading.**

- In this sample the mean return before the ex-date, relative to same-segment peers, was positive. It is clearest in tankers.
- The negative post-ex mean was **not reproduced** in a small, compositionally different earnings-clean subset. That limits interpretation; it neither identifies earnings as the cause nor establishes a zero effect.
- How the effect varies with yield is not established.

### 5b. Do tops cluster around ex-dates?

Tops are defined objectively: the series maximum over ±252 sessions, followed by a ≥40% decline within 252 sessions, with complete horizons. The scan covers 14 names in 2004–2026 and finds 49 gross-TR tops and 54 price tops. "Active payer" means a dividend was paid in the prior 126 sessions.

| Series | Active-payer tops | Peak 1–5 sessions **before** an ex-date | Peak on or 0–5 sessions **after** an ex-date |
|---|---:|---:|---:|
| Gross TR | 26 | 0 (displaced-calendar mean 1.37) | **8** (displaced-calendar mean 1.55; 0 of 3,000 displaced draws ≥8) |
| Price only | 27 | 3 (1.51; 633/3,000 draws ≥3) | 4 (2.03; 467/3,000) |

The eight gross-TR cases are:

- ZIM 3/22/2022 (day 0)
- Maersk 3/21/2022 (day 3)
- Maersk 4/8/2015 (day 3)
- MATX 11/6/2015 (day 3)
- MATX 11/13/2024 (day 4)
- Yang Ming 10/2/2007 (day 2)
- DHT 2/2/2011 (day 0)
- TNK 10/20/2015 (day 4)

**Reading.** Eight of 26 selected gross-return tops fell on an ex-date or within the next five sessions, compared with four of 27 price-only tops. Shifting each issuer's dividend calendar by 6–40 sessions produced fewer coincidences. That comparison is descriptive: it is not a calibrated chance expectation, and it does not separate dividend-related return behavior (a price drop smaller than the dividend gives a genuinely positive gross return) from selection effects.

**Price-only tops show no detectable ex-date clustering.** *(The earlier "price peaks 3–4 sessions before the ex-date" idea is not supported.)* At ZIM and at Maersk in March 2022, **the biggest payout of the cycle was where the total-return high was recorded**.

---

## 6. Back-test of the "top flags" (including volume)

**Design:**

- **Universe:** 14 names, 2004–2026, on gross-TR OHLC.
- **Outcome ("hit"):** within the next 126 sessions, the stock falls ≥25% below the next session's close before ever rising 10% above it.
- **Follow-up:** every trigger and every comparison day has the full 128 sessions of follow-up. There is no right-censoring.
- **De-duplication:** 20-session cooldown per signal per name.
- **Comparisons:** days within 10% of the 52-week closing high for near-high signals; days 15–25% below the 90-day high for MOM20 (depth-matched).
- **Incremental-volume tests:** the same price pattern with vs without the volume condition.
- **Intervals:** joint moving-block bootstrap over calendar months, synchronized across names, with 6- and 12-month blocks.

| Signal | Triggers | Hit rate | Comparison | Difference, pp [95% CI, 6-mo blocks] |
|---|---:|---:|---:|---|
| F5 reversal at 52-wk high, RVOL ≥1.3 | 175 | 12.0% | 15.1% | −3.1 [−8.1, +2.5] |
| same pattern, RVOL <1.3 | 208 | 11.5% | 15.1% | −3.5 [−7.8, +1.0] |
| Distribution cluster (≥6 in 25) | 439 | 16.2% | 15.1% | +1.1 [−2.7, +5.1] |
| Down-day cluster, no volume rule | 702 | 16.8% | 15.1% | +1.7 [−0.6, +4.2] |
| New 63-day high with OBV below its 63-day high | 398 | 12.1% | 15.1% | −3.0 [−6.5, +0.3] |
| New 63-day high with OBV confirming | 459 | 15.0% | 15.1% | 0.0 [−3.1, +2.9] |
| Break of 50-day MA, RVOL ≥1.5 | 187 | 16.0% | 15.1% | +1.0 [−5.2, +7.6] |
| Break of 50-day MA, RVOL <1.5 | 416 | 15.9% | 15.1% | +0.8 [−2.3, +4.3] |
| Gap-down ≥5%, RVOL ≥1.5 | 73 | 12.3% | 15.1% | −2.7 [−9.9, +5.2] |
| −8% day near the high | 131 | 17.6% | 15.1% | +2.5 [−4.7, +10.1] |
| **MOM20** (repo rule: close <80% of 90-day high) | 608 | 21.2% | **21.4% (depth-matched)** | **−0.2 [−2.4, +1.9]** |

**Incremental-volume comparisons** (with minus without the volume condition, same price pattern):

| Pair | Difference, pp [95% CI] |
|---|---|
| Reversal at high | +0.5 [−5.3, +6.7] |
| Distribution vs plain down-day clusters | −0.6 [−4.0, +2.5] |
| 50-day MA break | +0.2 [−5.6, +6.2] |
| Gap-down | −9.4 [−24.9, +5.9] |
| OBV divergence vs OBV confirmation (two OBV states, not a with/without-volume test) | −3.0 [−6.4, +0.6] |

**Robustness splits.** Results look the same excluding ZIM, tankers only, 2004–2015 and 2016–2026, with 12-month blocks. Of roughly 85 comparisons, only two intervals exclude zero (in at least one block length), and both point the *wrong* way for a top-warning:

- In tankers, reversals without high volume were followed by *fewer* declines (−7.4 pp).
- In 2016–26, OBV divergence was followed by *fewer* declines than OBV confirmation (−4.0 pp, 12-month blocks only).

That is about what chance would produce.

**ZIM itself:**

- The F5 volume-reversal fired on 3/17 (a correct day), but also on 2/11, 22 sessions before the price high.
- Distribution clusters fired on 12/8, 2/18 and 3/7.
- MOM20 fired on 12/14/2021 (false) and then on **4/6/2022 at $59.23**: −23.4% from the 3/22 gross-TR high, before the remaining fall to $6.59.

**Reading.**

- These prespecified implementations did **not demonstrate** predictive lift for the barrier outcome against state-matched comparisons.
- Adding the volume condition did not demonstrably change hit rates.
- This is "no demonstrated advantage", not proof that volume carries no information.
- Untested: executable strategy economics (re-entry, costs, gaps, dividend entitlement) and out-of-universe validation.
- **MOM20** is a drawdown-triggered exit heuristic whose incremental forecasting advantage was not established against this depth-matched comparison. This qualifies the "4/4 correct" back-test in `modeling_stash.md` §5.

---

## 7. Day1Global framework and cyclical rules — retrospective application (Rule 12, Rules 5–7, CRules 1–5, 7, 9, 10)

**What this section is.** It is a **retrospective framework application using a reconstructed contemporaneous input set** for 16-Mar-2022 (US market close), the price close high. It is **not** a hindsight-free back-test: the author and all three models (§7.9) knew the outcome.

- Each input is tagged **[as-of]** (published by the cutoff) or **[later]** (published or observed after it).
- Outcomes are kept in separate columns.
- Company figures: ZIM press releases of 9-Mar-2022 and 13-Mar-2024 unless marked secondary.
- Code: `zim_peak/run_zim_day1_replay.py` → `zim_peak/data/day1_replay.json`.

### 7.1 Day1Global modules

| Module | Inputs at the cutoff | Outcome [later] |
|---|---|---|
| **A Revenue quality** | [as-of] FY21 revenue $10.73B (+169%). Freight revenue (volume × rate) rose $6.21B; attributed **87% to rate** under volume-first ordering (71% rate-first; 79% symmetric). Rate-driven, cyclical; contract and route mix shape how SCFI passes through to realized rates | FY22 rate $3,240/TEU; FY23 $1,203 |
| **B Profitability** | [as-of] EBIT margin 54% (Q4 61%). Net operating cost incl. depreciation, before finance and tax: $1,411/TEU. **EBIT breakeven ≈ $1,276/TEU** (other revenue assumed proportional to freight); pretax ≈ $1,317. FY21 rate 2.18× EBIT breakeven; Q4 2.85×. This is **not a cash breakeven**: lease cash payments and depreciation differ | Net operating cost $1,899/TEU in FY22. FY23 adj. EBIT −$422M |
| **C Cash flow** | [as-of] OCF $5,971M − net capex $1,094M (ZIM's reconciliation) = **reported FCF $4,877M = 46.0% of the $10.61B market cap, before financing outflows**. Below FCF: repayments of borrowings and lease liabilities $1,191M (combined line, incl. early repayments), a short-term-loan reduction of $16M and interest paid $160M. The residual after these displayed principal repayments and interest ≈ $3.51B (33%). A lease-only bridge is not separable from the published lines. Distributions $21.50/sh since IPO = 24.3% of price | FCF FY22 $5.80B; FY23 $0.92B (also pre-financing). Net debt $2.3B at end-2023 |
| **D Forward guidance** | [as-of] FY22 adj. EBITDA $7.1–7.5B (+7.6% to +13.6%), adj. EBIT $5.6–6.0B. The ~$1.5B EBITDA–EBIT gap (vs $0.78B in FY21) already signalled higher depreciation/charter cost | Delivered $7.54B (above the range). Price −80.6% from the peak to 2022 year-end (calendar 2022: −70.8%) |
| **E Competitive landscape** | [as-of] Price-taker. 118 operated ships, predominantly chartered-in (~99%, secondary). **Alphaliner (1-Feb-2022): orderbook 6.15M TEU = 24.6% of the 25.0M TEU cellular fleet.** ZIM signed 36 newbuild charters in 2021–early 2022, 3 of them from a Kenon affiliate (related party) | BIMCO, early April 2022: ~26%. ZIM programme grew to 46 ships |
| **K Valuation** | [as-of price; Dec-21 balance sheet] **PE 2.27×** (FY21 EPS $39.02); P/B 2.31× (BV $38.35/sh). Mechanical post-$17 P/B 3.35×, assuming price and book both fall $17 and nothing else changes. EV $10.10B (lease-inclusive net cash netted) → EV/EBITDA 1.53× FY21, 1.38× FY22 guide | PE on FY22 EPS $38.35: 2.31×. One year later 0.64×, then a loss |
| **L Ownership** | [as-of] Israeli State special share (consent needed for ≥35%, notice above 24%). Payout policy 30–50% of NI. Related-party charters (Kenon affiliate, 3 ships). Kenon's stake at the cutoff: **unknown** (the 20.7% figure is from Kenon's 31-Mar-2022 release, after March sales) | — |
| **O Accounting quality** | [as-of] IFRS 16 moves charter hire out of opex into depreciation and interest, so **adj. EBITDA does not measure cash available after vessel financing and capital-use costs**. Comparisons with peers need consistent lease, capex and financing treatment. Lease liabilities $3.07B; reported net cash $509M nets leases. Long-term charters create future fixed commitments | $2.06B non-cash impairment in Q3-2023 |

### 7.2 Six perspectives — judgments, not established facts

| Perspective | Bear reading (as-of) | Competing argument |
|---|---|---|
| Quality Compounder | Price-taker; no evident durable moat | Niche-trade agility; record service metrics claimed by management |
| Imaginative Growth | No 10× optionality | LNG newbuilds cut fuel cost/carbon and replace expiring charters (ZIM's own argument) |
| Fundamental Long/Short | 2.27× PE is "cheap" only if rates stay above ~$2,400/TEU (EPS $27.9 → 3.2×) | Net cash, 46% pre-financing FCF yield |
| Deep Value | P/B is not liquidation value; little owned tonnage | Cash and investments $3.81B; containers and handling equipment $1.37B (owned + right-of-use) |
| Catalyst Driven | Known catalysts were distributions (ex 3/22, pay 4/4) | Further dividends under the 30–50% policy |
| Macro Tactical | Fed's first hike (decision 16-Mar); US CPI +7.9% y/y (Feb, released 10-Mar); war-driven energy shock; China lockdowns | Lockdowns could tighten capacity again |

### 7.3 CRule 5 — contrarian sell signals at the cutoff

| Signal | Status [as-of] |
|---|---|
| Low trailing PE | ✅ 2.27× on 16-Mar (1.93× on 9-Mar; not established as a historical minimum) |
| Industry orderbook surging | ✅ 24.6% of fleet (Alphaliner, 1-Feb-2022) |
| Company expanding aggressively | ✅ 36 newbuild charters |
| Spot ≥3× cash breakeven | **Not established.** SCFI was ~4.6–5× its pre-pandemic *index level* (not a cost threshold). ZIM's Q4 *realized* rate was 2.85× the modelled *EBIT* breakeven. No cash-breakeven series |
| Sell-side >70% Buy | Unknown |
| "Super-cycle" headlines | Unknown |

The orderbook and expansion signals were already present during 2021, when the stock still had substantial upside. No pre-declared rule or false-alarm test is shown, so this is consistent with late-cycle risk but is **not a validated zone or timing signal**.

### 7.4 CRule 4 — operating leverage (conditional on the FY2021 cost base)

Assumptions: 3.4M TEU; net operating cost $1,411/TEU fixed; other revenue 10.63% of freight revenue (9.61% of total revenue); net finance $157M; tax 17.9% on positive pretax income, no tax credit on losses; 119.74M shares.

| Rate | × EBIT breakeven | EBIT | Net income | EPS | EBIT margin |
|---:|---:|---:|---:|---:|---:|
| $1,276 | 1.0× | $0M | −$157M | −$1.31 | 0% |
| $1,914 | 1.5× | $2.40B | $1.84B | $15.37 | 33% |
| $2,552 | 2.0× | $4.80B | $3.81B | $31.82 | 50% |
| $3,189 | 2.5× | $7.20B | $5.78B | $48.28 | 60% |
| $3,827 | 3.0× | $9.60B | $7.75B | $64.73 | 67% |

**Breakeven is assumption-sensitive.** With the same method on later cost bases, the EBIT breakeven is $1,655 (FY22) and $1,301 (FY23). But the other-revenue share moved from 10.6% to 14.7% to 30.8% of freight revenue, so these are not like-for-like cost comparisons. Holding residual revenue *per TEU* constant instead gives $1,115 / $1,422 / $1,332.

### 7.5 CRule 7 — FY(T+1) sensitivity (fixed FY21 cost base) and the forecast-error bridge

| Freight rate | EPS | PE at $88.62 |
|---:|---:|---:|
| $1,200 | −$3.69 | n.m. |
| $1,800 | $12.44 | 7.1× |
| $2,400 | $27.92 | 3.2× |
| $3,000 | $43.39 | 2.0× |
| $3,630 | $59.64 | 1.5× |

Consensus at the cutoff: **unknown**.

**Error bridge [later]**, actual minus model at the actual rate and volume:

| | FY22 | FY23 |
|---|---:|---:|
| Additional residual (non-freight) revenue | +$447M | +$795M |
| Additional net operating cost | −$1,647M | −$953M |
| **Net EBIT difference** | **−$1,200M** | **−$158M** |

The small FY23 miss is the **net of large offsetting errors**. It does not validate the cost/revenue structure. This table is a fixed-cost-base sensitivity, not a forecast model.

### 7.6 CRule 2 — PE snapshots

| Date | Price | Trailing EPS | PE | Phase |
|---|---:|---:|---:|---|
| 31-Mar-2021 | $24.34 | $4.96 (FY20) | 4.9× | Early/mid |
| **16-Mar-2022** | **$88.62** | $39.02 (FY21) | **2.27×** | Late (peak earnings) |
| 16-Mar-2023 | $24.53 | $38.35 (FY22) | 0.64× | Downturn |
| 15-Mar-2024 | $9.45 | −$22.42 (FY23) | n.m. | Trough |

These are four snapshots, not a full phase path. No reasoned PE floor is derived. At a loss-making trough, P/B is one possible cross-check, subject to asset recoverability (right-of-use impairment) and future charter obligations. No valuation floor is established.

### 7.7 CRule 1 — two-cycle backtrack, ZIM vs SCFI (descriptive; partial)

| | Cycle 1 | Cycle 2 (Red Sea) |
|---|---|---|
| Window (monthly) | Feb-2021 – Dec-2023 (starts at the IPO, so it misses the 2020 upswing) | Oct-2023 – Feb-2025 (overlaps cycle 1 in Oct–Dec 2023) |
| SCFI weekly peak | 2022-01-07, 5,109.60 | 2024-07-05, 3,733.80 |
| ZIM price close peak / gross-TR peak | 2022-03-16 / 2022-03-22 | 2024-11-20 / 2025-01-02 |
| Weeks after the SCFI peak (price / TR) | **9.7 / 10.6** | **19.7 / 25.9** |
| Drawdown after the price peak | −92.6% (Nov-2023) | −56.6% (2025-04-08, outside the window) |
| R², monthly log levels (price / TR) | 0.80 / 0.51 | 0.57 / 0.47 |
| Correlation of monthly changes (n = 34 / 16) | 0.50 / 0.47 | 0.52 / 0.53 |
| Lag with the highest correlation (−3…+3 months) | 0 | 0 |

ZIM's price-close maxima occurred **about 10 and 20 weeks** after the SCFI maxima in these two selected windows.

- The level R² is trend-prone (spurious-regression risk) and descriptive only.
- The best lag was chosen among seven candidates, with no stability test.
- This does not generalize to other equities or to total-return peaks.

**Cycle positioning (2022 information set only):**

- **Position:** late cycle.
- **Evidence:** SCFI 4,625.06 on 11-Mar, −9.5% after **8** consecutive weekly declines; PE 2.27×; orderbook 24.6%.
- **Analog:** container 2020–22 (P-Rule 2).
- **Key risk:** a renewed disruption.

The second ZIM cycle is retrospective comparison only.

**Monthly-chart footnote (data-verified):** ZIM's highest month-end close is the March-2022 bar, closing 3/31 at $72.71. Earlier month-ends: Sep-21 $50.70, Oct-21 $51.22, Dec-21 $58.86, Feb-22 $69.79. The highest daily close in 2021 was $60.65. This is a *plausible* source of the "3/31" in the original question; the chart actually viewed is unknown.

### 7.8 CRules 3, 9, 10

- **CRule 3:** orderbook 24.6% of fleet on 1-Feb-2022 [as-of], mostly delivering 2023–24 on a 2–3-year lead time. Net additions vs scrapping and demand were **not assessed** (partial).
- **CRule 9** (FRED CPIAUCSL; ex-post comparison):
  - Mar-2022 → Aug-2026 factor 1.1615: peak close $88.62 = **$102.93** in 2026 dollars; market cap $12.3B.
  - Cycle-2 peak $27.01 (Nov-2024) × 1.0556 = **$28.51**.
  - Freight-rate dollar figures remain nominal.
- **CRule 10:** no meaningful shadow-fleet analogue in container shipping. N/A.

### 7.9 Rule 5 multi-model replay — uncorrected, hindsight-contaminated outputs

Three models received an identical anonymized data pack. The prompt and verbatim responses are in `zim_peak/data/multimodel/`.

- **The pack itself contained leakage:** 9 SCFI declines and a 26% orderbook figure.
- **All three recognized ZIM (2022).** Their outputs are therefore **not evidence of forecasting ability**.
- They are shown here as a critique of the framework's mechanics.

| | Claude Opus 4.8 | GPT-5.5 | Gemini 3.7 Flash |
|---|---|---|---|
| Recognized company | Yes | Yes | Yes |
| Phase / rating | Late; Trim→Sell (sell 60–80%) | Late/entering downturn; Trim/Sell | Late; Sell/Trim (sell 75–100%) |
| 12-month target: Cons / Base / Bull | $19 / $45 / $75 | $28 / $63 / $105 | $25 / $45 / $80 |
| 24-month target: Cons / Base / Bull | $15 / $28 / $55 | $35 / $35 / $84 | $12 / $22 / $55 |
| Valuation basis | P/B 0.5–1.5× | PE 3–4× on scenario EPS | P/B 0.3–0.5×; PE 2.5–4.5× |
| Input errors found | EV adds leases on top of lease-inclusive net cash (2.0× vs 1.53×) | — | — |

**Common to all three models:**

- "Cash breakeven" ≈ $1,200/TEU uses opex + G&A only and **omits lease cash payments**. The figure is an operating-cash breakeven before charter payments, not wrong per se, but mislabelled.
- Non-freight revenue is ignored.

The scenario labels are not common quantiles, so no aggregated or "corrected consensus" target is published.

**Realized [later]:**

| Horizon | Price | Dividends received | Price return | TR, dividends as cash | Gross TR, reinvested at ex-date |
|---|---:|---:|---:|---:|---:|
| 12 months (16-Mar-2023) | $24.53 | $27.55 | −72.3% | −41.2% | −55.3% |
| 24 months (15-Mar-2024) | $9.45 | $33.95 | −89.3% | −51.0% | −77.1% |

All figures are gross and pre-tax. The 12-month price was numerically close to the models' conservative cases ($19–28). The 24-month price was below all three conservative targets. **Neither is evidence of a successful forecast**, given the contamination.

### 7.10 Anti-bias review of this study

| Bias | Threat | Mitigation |
|---|---|---|
| Hindsight | §7.2 and §7.9 were written knowing the outcome | Inputs tagged [as-of]/[later]; quantitative tests in §5–6 use objective rules |
| Anchoring | "$100 → $6", "+8% on 3/31" | §0 premise check; chart explanations labelled plausible |
| Simplification | A single "breakeven" and a fixed cost base | Breakeven definitions separated; error bridge shown (§7.4–7.5) |
| Narrative | "Dividend magnet", "blow-off" | Tested; price tops show no ex-date clustering |
| Confirmation | Counting only flags that fired at ZIM | All-day precision vs state-matched comparisons; nulls reported |
| Survivorship | 14 hand-picked listed names | Stated limitation |
| Recency | The 2026 tanker rally | VLCC section limited to observations |

### 7.11 Pre-mortems

**ZIM, scored within one year of the cutoff (to 16-Mar-2023).** The realized total return with dividends as cash was −41.2%. These are events that occurred in that window, not demonstrated causes:

- SCFI fell to ~900–1,100 (Dec-2022 to Mar-2023).
- FY22 net operating cost/TEU rose to $1,899 (reported 13-Mar-2023).
- The share price de-rated (PE 0.64× on FY22 EPS).

The Q3-2023 impairment and the 2023–24 deliveries fall **outside** the one-year window.

**VLCC equities, 13-Oct-2026 → 13-Oct-2027 ("the holder lost 40%").** Probabilities are subjective, uncalibrated judgments: the probability that the event occurs within 12 months. Scenarios overlap and do not sum to 100%.

| Scenario | P(occurs within 12 months), judgment | Early-warning sign |
|---|---|---|
| Hormuz normalization releases trapped tonnage; TCE resets | 40–60% | Transits toward ~15+ mb/d; 1-yr TC < $85k for 4 consecutive weeks |
| Realized TCE keeps falling while equities hold highs, then equities catch down | 30–50% | Q/Q TCE declines continue (repo: Q2 $126.7K → Q3 $94.3K) |
| Supply response earlier than expected | 10–20% | 2028 deliveries confirmed above ~125 VLCCs |
| Income-holder exit after record payouts | 20–35% | Post-ex underperformance vs peers after the next large distribution |
| Macro / oil-demand shock | 10–25% | Falling crude export volumes; recession signals |

---

## 8. What this means for the VLCC top

**Lessons from the ZIM template (descriptive, not trading triggers):**

1. **Watch for rates and equities to diverge.** In 2022 the US/EU-listed names made new highs while SCFI fell nine straight weeks. When realized freight is falling and the equity is still making highs, you are in the zone where the container top formed. In one cycle the equity highs came 9–19 weeks after the rate peak. This is not a timing law.
2. **The record dividend matters for *how* you measure the top.** Measured correctly, the total-return high for ZIM and Maersk in March 2022 was recorded at the cycle's biggest ex-date. Track positions on gross total return, and know each ex-date.
3. **Pre-ex outperformance in tankers.** Over 10 sessions it averaged +2.8% vs peers (interval excludes zero). A post-ex giveback of −1.4% appears in the full sample but is not robust to excluding earnings windows.
4. **Do not rely on volume-reversal, OBV-divergence, distribution-day or −8%-day flags to call the top.** None showed an advantage. At ZIM, OBV *confirmed* the high.

**Current observations (13-Oct-2026; observations only, not a validated system, no recommendation):**

| | FRO | DHT | INSW |
|---|---|---|---|
| Close | $59.04 | $26.59 | $125.04 |
| vs 52-wk closing gross-TR high | −0.25% (high 10/12) | at high (10/13) | at high (10/13) |
| Last three quarterly dividend yields | 3.1% → 4.2% → **6.3%** (ex 9/18) | 2.5% → 3.5% → **6.25%** (ex 8/17) | 3.0% → 5.5% → 4.8% (ex 9/10) |
| Up/down volume, 25 sessions (price-signed) | 2.06 | 2.60 | 2.82 |
| Flags fired, last 20 sessions | reversal 9/17 and 9/21; OBV states mixed | reversal 10/5 | reversal 9/18 |
| MOM20 | not triggered | not triggered | not triggered |
| Next earnings (yfinance vendor estimate) | 11/30 | 10/28 | 11/5 |

- Repo data (DHT-disclosed, definitions not re-verified here): TCE Q2-2026 $126.7K/day → Q3 $94.3K/day. If confirmed, falling realized TCE with equities at highs is the same *configuration* as ZIM in Feb–Mar 2022 (§4). One cycle cannot say how long it lasts.
- **BWET is quarantined.** Its price path (about $19 at end-2025 to $999 now, with no recorded split) needs corporate-action/NAV validation before use as a rate proxy.

**CRule 8 — exit framework.** This report does not create new exit triggers. The operative VLCC exit framework is the repo's existing dashboard (`vlcc_cycles/data/final_exits.csv`, vlcc_cycles report §20.7). Below is a **selected mapping**; conditions and sizing are copied exactly. **None of these thresholds is validated by this study.**

| Repo exit trigger (verbatim) | Action (verbatim) | What the ZIM study says |
|---|---|---|
| 1-yr TC below US$85,000 for 4 consecutive weeks | TRIM 25% | Direction consistent with ZIM (the equity topped after the rate index rolled over, in two selected cycles). Thresholds not tested |
| 1-yr TC below US$75,000 | TRIM to half | as above |
| 1-yr TC below US$60,000 | EXIT | as above |
| Hormuz transit normalises toward ~15+ mb/d | TRIM 25% on the news | Analogous to congestion clearing; not time-tested here |
| P/NAV rises above 2.0x (DHT) / 2.2x (FRO) | TRIM 25% | No ZIM analogue (chartered fleet, no NAV) |
| P/NAV falls back below 1.2x on a rising fleet value | EXIT | No ZIM analogue |
| A dividend cut while the TC rate is UNCHANGED | EXIT the name | Not tested |
| 2028 deliveries confirmed above ~125 VLCCs | begin scaling out | Analogous to the container orderbook, visible at the peak (§7.8) |
| Repo momentum leg (MOM20; `modeling_stash.md`) | — | No forecasting advantage vs a depth-matched comparison (§6) |

The dashboard has other rows (second-hand values, FRO leverage) that are not mapped here.

**Rule 7 note.** No new VLCC target prices are set here. The repo's existing VLCC targets are in Report #37 (June-2026 prices, 12-month horizon) and vlcc_cycles §20.4, and they are **not refreshed** to October 2026 in this report. The ZIM model targets in §7.9 are contaminated replay outputs, not Rule-7 coverage.

---

## Step 2 — Strict peer review (of the Step-1 draft above)

**1. Facts that need verification**

- SCFI/WCI values come from secondary copies of primary publications (two SCFI copies agree; the WCI March values come from reposts). Shenzhen/Shanghai lockdown dates are news-reported.
- The TCE figures in §7 come from the repo and were not re-verified here.
- Earnings dates are vendor (yfinance) data with partial coverage. Free float is unknown, so the short-interest and turnover denominators use shares outstanding.

**2. Logical leaps / equivocation**

- "The TR top was a dividend event" mixes *where the high is recorded* (mechanics) with *why investors sold* (behavior). The data support only the former.
- "Rates lead equities" generalizes from one cycle with heterogeneous lags, and Asian names peaked earlier.

**3. Missing counterexamples / competing explanations**

- Maersk's price high almost coincided with the SCFI peak. The Asian carriers peaked in 2021.
- ZIM's later 16–27% yield dividends showed no pre-ex run-up/post-ex fall.
- Macro factors were not isolated: Fed hikes, the Russia–Ukraine war, the March-2022 bear-market rally.
- Consensus expectations are unknown.

**4. Most important primary sources to add**

- The Shanghai Shipping Exchange SCFI archive and the Drewry WCI archive.
- Bloomberg/LSEG consensus for ZIM FY22 EBITDA as of 8-Mar-2022.
- Free-float data.
- Daily TD3C/BDTI history for tanker cycles.
- Issuer-confirmed earnings dates.

**5. Sentences that are at most speculation**

- "ZIM's top was a dividend-capture top" in a behavioral sense.
- "Falling TCE with equities at highs means the VLCC top is near."
- Any statement about *how many weeks* after a rate peak the VLCC equity top will come.

**Step 2 coverage of §7 (Day1Global section)**

6. **Facts to verify:**
   - Kenon's stake as of 16-Mar-2022 (unknown).
   - ~99% chartered fleet (secondary).
   - Sell-side rating distribution (unknown).
   - The separate lease-principal component of the $1,191M repayment line (not published separately).
7. **Logical leaps:**
   - An EBIT breakeven is not a cash breakeven.
   - A fixed-FY21-cost sensitivity is not a forecast model.
   - A model replay by models that recognized the company is not validation.
8. **Competing explanations:**
   - Fleet renewal as a fuel-cost and flexibility benefit.
   - Cash and equipment backing.
   - Contract coverage dampening SCFI pass-through.
9. **At most speculation:**
   - "The framework identified the zone."
   - Any reading of the model targets as a forecast.
   - Any pre-mortem probability.

---

## 9. Repo-rule compliance (`.github/copilot-instructions.md`)

| Rule | Status | Where / note |
|---|---|---|
| Two-step protocol (draft + strict review) | ✅ | Step 1 / Step 2 (Step 2 covers §7, items 6–9) |
| Rule 1 bilingual, Rule 2 logs, Rule 3 push | ✅ | #41/#42 in sync; Prompt 78 in both logs; committed and pushed |
| Rule 4 cross-check, Rule 4b Astra review | ✅ | §10 rounds 0–3 plus a round-3 confirmation pass, each finding with an action |
| Rule 5 multi-model | ⚠️ partial | §7.9: three models, identical prompt; all recognized ZIM; no corrected-input weighting or consensus target |
| Rule 6 / CRule 4 operating leverage | ⚠️ partial | §7.4: conditional EBIT-breakeven table; no cash-breakeven series |
| Rule 7 target prices | ⚠️ partial | No new VLCC targets; Report #37 targets (June-2026) not refreshed |
| Rule 8 report structure | ⚠️ partial | Case study, not a company initiation |
| Rule 8B dual format | ⏸ exception | **User-granted scope exception (13-Oct-2026)**; this file is the detailed working report only |
| Rule 9 latest data | ✅ | Prices to 13-Oct-2026; FRED CPI to Aug-2026 |
| Rule 12 Day1Global | ⚠️ partial | Modules, 6 perspectives (as judgments), anti-bias (incl. simplification), pre-mortems present. As-of inputs reconstructed, not hindsight-free; Kenon stake at the cutoff unknown; consensus unknown |
| CRule 1 two cycles | ⚠️ partial | §7.7: descriptive; truncated/overlapping windows; no phase-by-phase valuation anatomy |
| CRule 2 PE path | ⚠️ partial | §7.6: four snapshots; no reasoned PE floor |
| CRule 3 supply duration | ⚠️ partial | §7.8: orderbook 24.6% (as-of); net additions vs demand not assessed |
| CRule 5 contrarian checklist | ✅ (corrected) | §7.3: "3× breakeven" marked not established |
| CRule 6 cross-cycle reference | ✅ | Whole report |
| CRule 7 sensitivity | ⚠️ partial | §7.5: five rates + error bridge; consensus unknown; no target link |
| CRule 8 exit framework | ✅ by reference | §8 selected verbatim mapping; thresholds not validated |
| CRule 9 inflation | ⚠️ partial | Both ZIM price peaks adjusted; freight-rate dollars nominal |
| CRule 10 shadow supply | N/A | §7.8 |
| P-Rule 1/3 | N/A | No VLCC earnings model in this report |

---

## 10. Adversarial review record (Rule 4b — gpt-6-astra)

**Round 0 (first draft, Oct 13):** 10 findings. Those included the "2-week blow-off" wording, the "dividend magnet" causality, the hindsight "flags 1–6" claim, the "−54% total drawdown" label and overfit trade rules. All were actioned in the intermediate draft.

**Round 1 (v1 of this data study) — "not safe to publish":**

| # | Finding | Verdict | Action |
|---|---|---|---|
| 1 | Yahoo Adj Close is not gross TR (ex-day +8.83% vs +7.13%) | Wrong | Rebuilt gross TR index; all TR numbers recomputed |
| 2 | TR-signed OBV counts the ex-day as an up day; "accumulation" overstated | Unsupported | Price- and gross-signed OBV both shown; "positive volume imbalance" wording |
| 3 | "Not heavily shorted"; covering as a bound on squeeze buying | Unsupported | Reviewer's wording adopted; bound removed |
| 4 | Mixed price/TR conventions; "market-dependent" claim | Wrong | One convention at a time, three search windows; "heterogeneous timing" |
| 5 | Asymmetric windows; SPY-only benchmark; naive t-stats; "yield-scaled" untested | Unsupported | Symmetric windows, segment benchmark, FE slope, earnings exclusion, block bootstrap |
| 6 | Ex-date test used TR tops for a price-top claim; weak null | Wrong | Price and TR tops tested separately; complete horizons |
| 7 | MOM20 lift measured against the wrong (near-high) base | Wrong | Depth-matched comparison: lift disappears |
| 8 | "Volume flags rejected" overstated | Wrong | Incremental-volume pairs; "no demonstrated advantage" wording |
| 9 | BWET path unvalidated; exit recommendation untested | Unsupported | BWET quarantined; recommendation removed |
| 10 | Selection, in-sample, censoring, reproducibility | Valid | Universe and limits stated; complete follow-up enforced; data/code committed |

**Round 2 (v2) — "not safe unchanged":**

| # | Finding | Verdict | Action |
|---|---|---|---|
| 1 | Calendar placebo is not a calibrated null (it removes the same-event matches; eligibility not re-simulated) | Wrong as significance | p-values withdrawn; reported as a descriptive contrast |
| 2 | One-month bootstrap ignores overlap of 126-session outcomes | Unsupported | Synchronized moving-block bootstrap (3/6/12-month blocks), joint resampling |
| 3 | Event counts did not reconcile (189 vs 190 at ≥2%) | Wrong | Bucket boundary fixed (yield = 2% exactly); now 157+33 = 167+23 = 190 |
| 4 | Rally-volume count mislabeled | Wrong | Exact date bounds given |
| 5 | Earnings-clean subset over-interpreted | Unsupported | All / covered / clean reported separately; narrow wording |
| 6 | Withholding offered as an explanation | Unsupported | "May affect; not identified" |
| 7 | "Loss-limiting / not a forecaster" wording for MOM20 | Overstated | Reviewer's wording adopted |
| 8 | INSW yields described as rising; vendor earnings dates; FRO high | Wrong / unsupported | Corrected; dates labeled vendor estimates; FRO −0.25% below its 10/12 closing high |
| 9 | End-of-sample handling unstated | Unsupported | All observations require full follow-up; stated in §6 |

**Round 3 (Day1Global / cyclical-rule section) — "not safe unchanged":**

| # | Finding | Verdict | Action |
|---|---|---|---|
| 1 | "As-of 16-Mar" leaked later data: 9th SCFI decline (18-Mar), 26% orderbook (April), Kenon 20.7% (31-Mar), March CPI (12-Apr), "guidance beaten" | Wrong | Section re-titled a *retrospective application with reconstructed inputs*; [as-of]/[later] tags; SCFI 8 declines / 4,625.06; Alphaliner 24.6% (1-Feb-2022, verified from the PDF); Kenon at cutoff = unknown; Feb CPI +7.9% (released 10-Mar); outcome moved to "later" columns |
| 2 | FCF equation false (5,971 − 1,010 ≠ 4,877); FCF is pre-financing | Wrong | ZIM reconciliation used (net capex $1,094M); labelled pre-financing; residual after the displayed $1,191M combined repayments, $16M short-term-loan reduction and $160M interest ≈ $3.51B (33%) |
| 3 | "Cash breakeven" ≠ EBIT breakeven; "other revenue 10.6% of revenue" | Wrong | EBIT $1,276 / pretax $1,317 separated; 10.63% of freight = 9.61% of total |
| 4 | FY22/FY23 breakevens not like-for-like; "structure was right" contradicted by offsetting errors | Unsupported | Alternative residual-per-TEU breakevens ($1,115/$1,422/$1,332); error bridge (FY23: +$795M revenue vs −$953M cost); claim withdrawn |
| 5 | CRule 5 "spot ≥3× breakeven" invalid; "PE at historic low" | Wrong | Marked not established; "low trailing PE" (1.93× on 9-Mar) |
| 6 | Multi-model consensus used as validation; median targets not meaningful | Unsupported | Outputs labelled uncorrected and contaminated; medians and success language removed; prompt and verbatim responses archived |
| 7 | CRule 1 overstated; lags | Overstated | "About 10 and 20 weeks" (price); TR 10.6/25.9; R² descriptive; n = 34/16 changes; window overlap disclosed |
| 8 | FY22 EPS "a record"; "−80.6% during 2022" | Wrong | Removed; peak-to-year-end −80.6% vs calendar −70.8% |
| 9 | Perspectives stated as facts; missing related-party charters; fleet renewal one-sided | Unsupported | Judgments table with competing arguments; Kenon-affiliate charters (3 ships) added |
| 10 | Pre-mortem: undefined High/Medium; ZIM scored with post-window events | Incomplete | Subjective numeric ranges with a definition; ZIM pre-mortem restricted to 12 months |
| 11 | Exit mapping dropped conditions/sizing | Wrong | Conditions copied verbatim; labelled a selected mapping |
| 12 | Compliance table overstated | Wrong | Statuses downgraded to partial where applicable; Rule 8B exception recorded |

**Round-3 confirmation pass:** 10 of 12 fixed; 2 partly fixed, now resolved:
- The cash bridge now includes the $16M short-term-loan reduction ($3.51B).
- The IFRS 16 wording was corrected (EBITDA ≠ cash after vessel financing).
- "Book value is the anchor" became "one possible cross-check".
- The commit/push status was certified only after the push.


**Not done (stated limits):** formal calibrated null for the ex-date clustering; executable strategy back-test with re-entry and costs; out-of-universe validation; primary consensus data.

---

## 11. Data & reproducibility

- **Code:**
  - `zim_peak/run_zim_peak_volume.py` (§1–6, §8). Needs Python 3.12, yfinance, pandas, numpy, scipy, matplotlib. Prices are cached on first run; data retrieved 13-Oct-2026.
  - `zim_peak/run_zim_day1_replay.py` (§7) → `day1_replay.json`, `crule1_two_cycles.csv`. Uses `fred_cpiaucsl.csv`.
  - Multi-model prompt and verbatim responses: `zim_peak/data/multimodel/`.
- **Outputs (`zim_peak/data/`):**
  - `summary.json` (all headline numbers)
  - `zim_daily_yahoo.csv`, `zim_peak_window.csv`
  - `container_peaks_vs_scfi.csv`
  - `exdiv_event_study.csv`
  - `major_tops.csv`
  - `flag_triggers.csv`, `flag_backtest.csv`
  - `finra_short_interest_zim.csv`
  - `scfi_weekly_source{A,B}_*.csv`
  - `earnings_dates_yfinance.csv`
- **Universe:** ZIM, MATX, DAC, GSL, Hapag-Lloyd, Maersk-B, Evergreen, Yang Ming, COSCO; FRO, DHT, INSW, TNK, NAT; benchmark SPY.

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

**Core conclusion.** ZIM's top was not a single "+8% day on 3/31". It was a six-session price high (Mar 14–21, 2022). Its **total-return high was recorded on the $17 ex-dividend date (Mar 22)**. All of this happened **10 weeks after the SCFI freight index had peaked and while SCFI fell nine weeks in a row**. Volume was elevated around the results/dividend window but was **not** a climax. None of eight volume or price "top flags" I back-tested over 2004–2026 showed predictive lift against state-matched comparisons. **There is no validated early-warning signal here.** The transferable lessons are structural: rates and equities diverging, and dividend timing. They are not trading triggers.

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

## 7. What this means for the VLCC top

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

---

## 8. Adversarial review record (Rule 4b — gpt-6-astra)

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

**Not done (stated limits):** formal calibrated null for the ex-date clustering; executable strategy back-test with re-entry and costs; out-of-universe validation; primary consensus data.

---

## 9. Data & reproducibility

- **Code:** `zim_peak/run_zim_peak_volume.py`. It needs Python 3.12, yfinance, pandas, numpy, scipy and matplotlib. Prices are cached on first run; data retrieved 13-Oct-2026.
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

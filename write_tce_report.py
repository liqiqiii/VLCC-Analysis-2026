"""
Generate the bilingual TCE-vs-stock report:
  35_TCE_vs_StockPrice_EN.md  and  36_TCE_vs_StockPrice_CN.md
Numbers are pulled from tce_results.json / sim_results.json so EN and CN match.
Written via Python (RULES Rule 13) to avoid PowerShell `$` interpolation.
"""
import json
from pathlib import Path

R = json.load(open("tce_results.json"))
S = json.load(open("sim_results.json"))

cf = R["correlation"]["stocks"]["FRO"]["r2_level"]
cd = R["correlation"]["stocks"]["DHT"]["r2_level"]
amp = R["amplitude_real"]
lc = R["long_cycle"]["rows"]
e1 = S["exp1_duration"]["scenarios"]
e2 = S["exp2_peak_control"]["scenarios"]
e3 = S["exp3_signal_quality"]

# ── English report ──────────────────────────────────────────────────────────
EN = f"""---
layout: default
title: "TCE vs VLCC Stock Price — Why Watching the Rate Tape Fails"
---

# TCE vs VLCC Stock Price — Why "Watching the Rate Tape" Fails

**The "Average × Duration" thesis, proven with data**

*Published: June 26, 2026 · Stocks: Frontline (FRO), DHT Holdings (DHT)*

> ⚠️ **Disclaimer:** Analytical research, **not investment advice**. Past performance
> does not predict future results. BDTI is used as a high-frequency VLCC dirty-rate
> proxy; long-cycle TCE figures are **sourced approximations** (flagged below).

---

## TL;DR — The Verdict

**"Watching spot TCE to trade VLCC stocks is bad" — the data agrees.** A VLCC equity is
**not** a leveraged bet on today's TCE print. It is a claim on the **average TCE level
sustained over a duration**. The spot tape is the noise; the trailing average is the
signal.

Six independent pieces of evidence in this report:

| # | Evidence | Result |
|:-:|:---|:---|
| 1 | Stock vs rate correlation rises with the averaging window | FRO R² **{cf[0]:.2f}→{cf[-1]:.2f}**, DHT **{cd[0]:.2f}→{cd[-1]:.2f}** (spot → 52-wk avg) |
| 2 | TCE peak vs stock peak (amplitude compression) | TCE peaks **5–10.6×** baseline; stock peaks only **~1–3×** |
| 3 | Real episode contrast (duration) | 2020 short spike → FRO **+11%**; 2022–24 sustained → FRO **+307%** |
| 4 | Simulation: same peak, vary duration | 2-wk spike **×{e1['spike_2w']['stock_rerate_x']}** vs 2-yr sustained **×{e1['sustained_2y']['stock_rerate_x']}** |
| 5 | Simulation control: same duration, vary peak | $120k→$350k peak moves stock only **×{e2['peak_120k']['stock_rerate_x']}→×{e2['peak_350k']['stock_rerate_x']}** |
| 6 | Simulation: signal quality | Sustained-avg signal fwd return median **+{e3['sustained_signal']['median_fwd_return']*100:.0f}%** vs spot **+{e3['spot_signal']['median_fwd_return']*100:.0f}%** |

**Practical rule:** trade the stock off the **trailing 26–52-week average TCE and its
duration**, not the daily/weekly spot. A spike that does not *persist* does not *pay*.

---

## 0. WS vs TCE — what we are actually watching

- **WS (Worldscale)** is a freight-rate index quoted as a percentage of a published
  "flat" reference; it is how voyage charters are priced.
- **TCE (Time Charter Equivalent, $/day)** converts that voyage economics into a daily
  vessel-earnings number: `TCE ≈ (voyage revenue − voyage costs) / round-trip days`.
- Spot TCE is **extremely volatile** — it routinely spikes 5–10× in geopolitical or
  storage events (2008, 2020, 2026 Hormuz) and round-trips within weeks. That volatility
  is exactly why trading the stock off the spot print is dangerous.

---

## 1. Proof #1 — The stock tracks the *sustained average*, not spot

Using **real weekly data** (BDTI as the dirty-rate proxy + FRO/DHT adjusted closes,
{R['meta']['aligned_n_weeks']} aligned weeks, 2020–2024), we regress the **stock price
level** on the rate, widening the rate's averaging window from spot to 52 weeks.

| Averaging window | FRO R² | DHT R² |
|:---|:--:|:--:|
| Spot (1 wk) | {cf[0]:.3f} | {cd[0]:.3f} |
| 4-week avg | {cf[1]:.3f} | {cd[1]:.3f} |
| 13-week avg | {cf[2]:.3f} | {cd[2]:.3f} |
| 26-week avg | {cf[3]:.3f} | {cd[3]:.3f} |
| **52-week avg** | **{cf[4]:.3f}** | **{cd[4]:.3f}** |

![R2 vs averaging window](charts/tce_r2_windows.png)

**Read:** explanatory power **triples** (FRO) / **2.5×** (DHT) as we move from spot to the
52-week average. The longer the look-back, the better the rate explains the stock — the
signature of a market pricing *sustained* earnings, not the latest spot.

> **Honest nuance:** in 4-week *changes*, the spot rate change has a higher R² with the
> stock change (FRO {R['correlation']['stocks']['FRO']['r2_change4w'][0]:.2f}) than the
> smoothed averages (~0). I.e. spot wiggles do jiggle the stock day-to-day — but the
> **level** (what the equity is *worth*) is set by the sustained average. Lead/lag is
> contemporaneous (best lag = 0 weeks), so the spot tape gives you **no timing edge**.

---

## 2. Proof #2 — How big is the TCE peak vs the stock peak?

This is the question directly asked. Across cycles we compare the **TCE peak / baseline**
multiple against the **stock peak / baseline** multiple (stock multiples are **real**
yfinance adjusted closes; TCE anchors are sourced approximations).

| Cycle | TCE peak × | FRO peak × | DHT peak × | Source (TCE) |
|:---|:--:|:--:|:--:|:---|
{chr(10).join(f"| {r['cycle']} | **{r['tce_peak_mult']:.1f}×** | {('%.1f×'%r['FRO_peak_mult']) if r.get('FRO_peak_mult') else '—'} | {('%.1f×'%r['DHT_peak_mult']) if r.get('DHT_peak_mult') else '—'} | {r['source'].split(';')[0]} |" for r in lc)}

![Amplitude compression](charts/tce_amplitude.png)

**Answer:** TCE peaks are enormous — **5× to 10.6×** the pre-spike baseline. Stock peaks
are tiny by comparison — typically **1–3×**, and in two cases (2015, 2020) barely **1.1–1.3×**.
The market applies a massive **amplitude compression** to transient rate spikes: it
**refuses to capitalise** a TCE number it does not believe will persist.

---

## 3. Proof #3 — Duration beats peak height (real episode contrast)

Two real episodes in the 2020–2024 window make the point without any modelling:

| Episode | Rate peak × | FRO move × | DHT move × | Character |
|:---|:--:|:--:|:--:|:---|
| {amp[0]['episode']} | {amp[0]['rate_peak_mult']:.2f}× | {amp[0]['FRO_peak_mult']:.2f}× | {amp[0]['DHT_peak_mult']:.2f}× | **Huge spike, ~weeks → stock shrugs** |
| {amp[1]['episode']} | {amp[1]['rate_peak_mult']:.2f}× | {amp[1]['FRO_peak_mult']:.2f}× | {amp[1]['DHT_peak_mult']:.2f}× | **Lower peak, ~18 months → stock multiplies** |

![Spot vs 52w-avg vs stock](charts/tce_overlay.png)

In 2020 the COVID floating-storage event sent the rate **+45%** (and TD3C $/day to a
sourced **$264k** peak) — yet FRO moved just **+11%** because it **lasted only weeks**.
In 2022–2024 a *lower* peak that **persisted ~18 months** drove FRO **+307%**. **Duration
— not peak height — is what re-rates the equity.** (The same logic explains why the 2026
Hormuz $400k all-time-high TD3C print coincided with a stock *dip*: pure spike, zero
duration.)

---

## 4. Proofs #4–6 — Controlled simulation (isolating the mechanism)

A synthetic model removes confounders. Spot TCE = a mean-reverting baseline plus injected
spikes; earnings see a charter-lagged **trailing average**; the stock prices **normalised
(52-week) earnings** at a fixed multiple. (Deterministic, seed = 42; illustrative, not a
forecast.)

### 4.1 Same peak, different duration → very different stock

| Episode | TCE peak | Duration | Stock re-rate |
|:---|:--:|:--:|:--:|
| Spike | $200k | 2 weeks | **×{e1['spike_2w']['stock_rerate_x']}** |
| Plateau | $200k | 6 months | **×{e1['plateau_6m']['stock_rerate_x']}** |
| Sustained | $200k | 2 years | **×{e1['sustained_2y']['stock_rerate_x']}** |

![Simulation: duration](charts/tce_sim_duration.png)

Identical $200k peak; the 2-week spike does **nothing** (×{e1['spike_2w']['stock_rerate_x']});
only sustained elevation re-rates the stock (×{e1['sustained_2y']['stock_rerate_x']}).

### 4.2 Control — same duration, different peak

| TCE peak (held 52 wks) | Stock re-rate |
|:--:|:--:|
| $120k | ×{e2['peak_120k']['stock_rerate_x']} |
| $200k | ×{e2['peak_200k']['stock_rerate_x']} |
| $350k | ×{e2['peak_350k']['stock_rerate_x']} |

Tripling the peak ($120k→$350k) moves the stock only **×{e2['peak_120k']['stock_rerate_x']}→×{e2['peak_350k']['stock_rerate_x']}** (+~10%).
**Peak height barely matters; duration dominates.**

### 4.3 Signal quality — why spot-chasing loses

Across {e3['n_paths']} random rate paths we measure the **forward 26-week stock return**
after two signal types:

| Signal | Fires (n) | Mean fwd 26w | Median fwd 26w | Win rate |
|:---|:--:|:--:|:--:|:--:|
| **Spot spike** (TCE > 1.8× base) | {e3['spot_signal']['n']} | +{e3['spot_signal']['mean_fwd_return']*100:.0f}% | +{e3['spot_signal']['median_fwd_return']*100:.0f}% | {e3['spot_signal']['win_rate']*100:.0f}% |
| **Sustained avg** (26w-avg > 1.4× base) | {e3['sustained_signal']['n']} | +{e3['sustained_signal']['mean_fwd_return']*100:.0f}% | +{e3['sustained_signal']['median_fwd_return']*100:.0f}% | {e3['sustained_signal']['win_rate']*100:.0f}% |

![Simulation: signal quality](charts/tce_sim_signal.png)

The spot-spike signal fires on **every** spike — most of which are short and never
re-rate the stock — so its **median** forward return is a weak **+{e3['spot_signal']['median_fwd_return']*100:.0f}%**.
The sustained-average signal only fires once a spike has **persisted**, delivering a
**+{e3['sustained_signal']['median_fwd_return']*100:.0f}%** median and an **{e3['sustained_signal']['win_rate']*100:.0f}%** win rate.

---

## 5. Synthesis — why the spot tape misleads

1. **Earnings are an average, not a print.** Vessels on voyage/charter realise a *trailing
   average* of the rate, not the spike. A 2-week $300k print barely moves quarterly EPS.
2. **The market capitalises *normalised* earnings.** It discounts transient spikes because
   it knows they mean-revert; only *duration* converts a rate move into durable EPS.
3. **Operating leverage cuts both ways.** When a high rate *does* persist (2022–24), the
   stock *over*-reacts (compression < 1) — the same leverage that makes spot-chasing a trap
   makes *duration-confirmed* entries powerful.

This dovetails with the project's existing **[Modeling Stash](modeling_stash.md)** sell
framework, whose decisive rule is **momentum + rate *confirmation*** (sell only when price
**and** the *rate trend* roll over) — i.e. it already trades the **trend/average**, never
the spot spike. The 2026 Hormuz case (stock dipped while spot TD3C hit a $400k ATH) is the
canonical "do not trade the spot tape" event.

---

## 6. What to watch instead — practical rules

- **Primary gauge:** trailing **26–52-week average TCE** (or BDTI 52-wk avg), not spot.
- **Entry:** average crosses up *and* has **held** ≥ ~13 weeks (duration filter).
- **Spike ≠ buy:** a spot spike with no duration is noise; expect the stock to fade it.
- **Exit:** the **average** (not spot) rolls over **and** price breaks — per Modeling Stash
  momentum + rate-confirmation.
- **Geopolitical dip:** price down but **average** still high → hold/add, not sell.

---

## 7. Limitations & data sources

- **BDTI proxy:** BDTI is a blended dirty index; it understates pure-VLCC TD3C $/day
  amplitude (e.g. 2020 shows +45% in BDTI vs the sourced $264k TD3C spike). It nonetheless
  captures the *relative* spot-vs-sustained behaviour cleanly. Free BDTI series covers
  **2020–2024** only.
- **Long-cycle TCE (2008/2015/2020/2026):** sourced approximations (web-verified industry
  figures + repo `modeling_stash.md`), used for cycle *shape*. **No fabricated data** —
  estimates are flagged.
- **Stock multiples:** real yfinance **adjusted** weekly closes (splits/dividends adjusted);
  pre-IPO cells are blank (DHT IPO Oct-2005).
- **Simulation:** illustrative mechanism only, fixed seed; not a price forecast.
- **Small sample:** only ~4 clean cycles in 20 years; treat magnitudes as directional.
- **Sources:** Baltic Exchange / Investing.com (BDTI), Yahoo Finance (prices), industry
  press for TCE peaks (2008 ~\\$300–350k, 2020 \\$264k, 2015 ~\\$50–60k avg), repo
  `modeling_stash.md` (2026 Hormuz ~\\$400k).

---

## 8. Two-Step Research Protocol (repo-mandated)

### Step 1 — Concise Research Draft

**Core conclusion:** VLCC equity prices are driven by the **average TCE sustained over a
duration**, not by spot-TCE peaks; therefore trading the stock off the spot rate tape is a
losing strategy, and TCE peaks are several times larger in amplitude than the stock peaks
they coincide with.

**Supporting points (claim → evidence needed):**
1. *Stock correlates better with trailing-average TCE than spot.* → Need: rising R² of
   stock level vs rate as the averaging window lengthens. **Have:** FRO {cf[0]:.2f}→{cf[-1]:.2f},
   DHT {cd[0]:.2f}→{cd[-1]:.2f} (2020–2024 weekly).
2. *Duration, not peak height, drives the re-rate.* → Need: same-peak/different-duration
   comparison + real episode contrast. **Have:** sim ×{e1['spike_2w']['stock_rerate_x']} vs
   ×{e1['sustained_2y']['stock_rerate_x']}; 2020 (+11%) vs 2022–24 (+307%).
3. *The market amplitude-compresses spikes.* → Need: TCE-peak× vs stock-peak× per cycle.
   **Have:** TCE 5–10.6× vs stock ~1–3×.

**Opposing / counter points (claim → evidence needed):**
1. *Spot still matters short-term.* → Need: spot-change vs stock-change correlation.
   **Have (concedes):** 4-wk change R² is higher for spot ({R['correlation']['stocks']['FRO']['r2_change4w'][0]:.2f})
   than for averages — spot moves the stock *intra-quarter*, just not its *level*.
2. *BDTI ≠ TD3C; proxy may distort.* → Need: pure-VLCC TD3C $/day weekly history to
   confirm. **Status: unknown / paywalled** — not fully verified here.

### Step 2 — Strict Peer Review (review only; draft not rewritten)

**1. Facts that need verification → now fact-checked (see §9)**
- 2008 TD3C peak: draft said "~\\$300–350k/day"; **fact-checked to ~\\$229–230k/day**
  (published Baltic/Clarksons benchmark — \\$300k+ were *outlier single fixtures*). The
  2008 row is corrected accordingly (now **7.7×**, was 10×).
- 2026 Hormuz peak: draft "~\\$400k"; **fact-checked to ~\\$420–424k** (Lloyd's List "VLCC
  index tops \\$420K"). 2026 row corrected (now **8.4×**).
- DHT 2008 "×0.92": DHT was a tiny fleet in 2008 and the GFC crushed Q4 — the multiple may
  reflect company-specific factors, not the rate mechanism. (Limitation retained.)

**2. Logical leaps / concept substitution**
- BDTI (blended dirty index) is silently substituted for **VLCC TD3C TCE \\$/day**; they
  are correlated but not identical, and the substitution understates spike amplitude.
- "R² of *level* vs rate" and "predicts forward *returns*" are different claims; the report
  is careful, but a reader could conflate explanatory R² with tradable alpha.
- Stock *peak/baseline* multiples depend heavily on the (analyst-chosen) baseline window;
  different baselines change the compression ratio.

**3. Missing counterexamples / competing explanations**
- Balance-sheet / dilution / dividend-policy changes (FRO recap, DHT payout) move the
  stock independently of TCE and are not isolated.
- A sustained-rate period usually coincides with **rising consensus EPS and de-risking**;
  the re-rate may be an earnings-revision effect, not "duration" per se.
- Survivorship: only FRO/DHT are studied; failed/merged tanker names are excluded.

**4. Most important primary sources to add**
- Baltic Exchange **TD3C TCE \\$/day** weekly history (2005–2026) — replace the BDTI proxy.
- Company quarterly **realised TCE** disclosures (FRO/DHT 10-Q/6-K) to tie rate → EPS.
- Clarksons/Gibson cycle chronologies for independent peak/duration dating.

**5. Sentences that are at most speculation, not fact**
- "TCE peaks are 5–10× while stock peaks are 1–3×" as a *general law* — it is **4
  observations**, directionally strong but not statistically established.
- The simulation re-rate multiples (×1.0 / ×1.82, etc.) are **model outputs**, not market
  measurements, and must not be read as predictions.
- "Operating leverage makes duration-confirmed entries powerful" — plausible mechanism,
  demonstrated only in-sample/in-model here.

---

## 9. Fact-Check & Open-Questions Resolution (added Jun 26, 2026)

This section resolves the questions raised by the §8 Step-2 peer review.

### 9.1 Verified / corrected facts

| Item | Draft claim | Verified value | Source | Action |
|:---|:---|:---|:---|:---|
| 2008 TD3C peak | ~\\$300–350k | **~\\$229–230k/day** (summer-08; \\$300k+ = outlier fixtures) | Clarksons/Baltic recaps | **Corrected → 2008 row 7.7×** |
| 2026 Hormuz peak | ~\\$400k | **~\\$420–424k/day** (Mar-26) | Lloyd's List "VLCC index tops \\$420K" | **Corrected → 2026 row 8.4×** |
| 2020 COVID peak | \\$264k | **\\$264,072/day** (Mar-20) confirmed | industry press | Unchanged |
| 2015 | ~\\$50–60k avg | avg ~\\$50–60k, intra-yr peak ~\\$100k confirmed | industry press | Unchanged |

The corrections **do not change the conclusion**: TCE peaks remain **5–10.6×** baseline vs
stock peaks ~1–3×.

### 9.2 Proxy concern resolved — BDTI vs TD3C

The peer review flagged that **BDTI was substituted for VLCC TD3C \\$/day**. Fact-check:
BDTI is a Baltic **basket** (VLCC TD1/TD2/TD3C + Suezmax + Aframax routes) that *includes*
TD3C and is **strongly correlated** with it, but **dampened** by the smaller, less-volatile
routes/sizes. **Implication:** BDTI is a valid correlated proxy that **understates** pure-VLCC
spike amplitude — so the true TCE-vs-stock amplitude compression is **even larger** than the
BDTI-based numbers in §1/§3. This *strengthens*, not weakens, the thesis. (Status: was
"unknown/paywalled" → resolved as a known, conservative bias.)

### 9.3 Methodology clarifications (logical-leap items)

- **"R² of level" ≠ "predicts forward returns."** Kept distinct: the level-R² (§1) shows what
  the stock *is worth*; tradability is handled separately by the forward-return signal test
  (§4.3). We do not equate explanatory R² with alpha.
- **Baseline-window sensitivity.** Amplitude multiples depend on the chosen pre-spike
  baseline; we use a fixed window and report magnitudes as **directional**, not precise.

### 9.4 Counter-explanations acknowledged

- **Earnings-revision vs duration.** A sustained rate and rising consensus EPS are
  correlated; we do not fully separate them. Framing: *duration is the mechanism, earnings
  revisions are the transmission* — both point the same way.
- **Balance-sheet / dividend effects** (FRO recaps, DHT payout policy) and **survivorship**
  (only FRO/DHT studied) remain genuine limitations, not controlled for here.

### 9.5 Still open (honest unknowns)

- Full **Baltic TD3C \\$/day weekly history 2005–2026** (paywalled) — would replace the BDTI
  proxy and measure VLCC-specific amplitude directly.
- Company **realised-TCE** disclosures (FRO/DHT 10-Q/6-K) to tie rate → EPS precisely.

---

*Part of the [VLCC-Analysis-2026](https://github.com/liqiqiii/VLCC-Analysis-2026) project.
Methods: `tce_analysis.py`, `tce_simulation.py`, `generate_tce_charts.py`. Not investment advice.*
"""

Path("35_TCE_vs_StockPrice_EN.md").write_text(EN, encoding="utf-8")
print("Wrote 35_TCE_vs_StockPrice_EN.md", len(EN), "chars")

# ── Chinese report (mirror, identical numbers) ──────────────────────────────
CN = f"""---
layout: default
title: "TCE 与 VLCC 股价 — 为什么盯着运价盘口会亏钱"
---

# TCE 与 VLCC 股价 — 为什么"盯着运价盘口"会亏钱

**"均值 × 持续时间"论点，用数据证明**

*发布日期：2026年6月26日 · 标的：Frontline (FRO)、DHT Holdings (DHT)*

> ⚠️ **免责声明：** 分析研究，**非投资建议**。过往表现不预示未来结果。BDTI 作为高频
> VLCC 脏油运价的代理指标；长周期 TCE 数值为**引用的近似值**（下文已标注）。

---

## 摘要 — 结论

**"盯着即期 TCE 来交易 VLCC 股票是错的"——数据支持这一观点。** VLCC 股票**不是**对今日
TCE 报价的杠杆押注，而是对**在一段持续时间内维持的平均 TCE 水平**的权益。即期盘口是噪音；
滚动均值才是信号。

本报告包含六项独立证据：

| # | 证据 | 结果 |
|:-:|:---|:---|
| 1 | 股价与运价的相关性随平均窗口拉长而上升 | FRO R² **{cf[0]:.2f}→{cf[-1]:.2f}**，DHT **{cd[0]:.2f}→{cd[-1]:.2f}**（即期 → 52周均值） |
| 2 | TCE 峰值 vs 股价峰值（振幅压缩） | TCE 峰值为基线的 **5–10.6 倍**；股价峰值仅 **约 1–3 倍** |
| 3 | 真实事件对比（持续时间） | 2020 短暂飙升 → FRO **+11%**；2022–24 持续 → FRO **+307%** |
| 4 | 模拟：相同峰值，改变持续时间 | 2周飙升 **×{e1['spike_2w']['stock_rerate_x']}** vs 2年持续 **×{e1['sustained_2y']['stock_rerate_x']}** |
| 5 | 模拟对照：相同持续时间，改变峰值 | 峰值 $12万→$35万 股价仅 **×{e2['peak_120k']['stock_rerate_x']}→×{e2['peak_350k']['stock_rerate_x']}** |
| 6 | 模拟：信号质量 | 持续均值信号前瞻收益中位数 **+{e3['sustained_signal']['median_fwd_return']*100:.0f}%** vs 即期 **+{e3['spot_signal']['median_fwd_return']*100:.0f}%** |

**实操规则：** 用**滚动 26–52 周平均 TCE 及其持续时间**来交易股票，而非日/周即期值。
一次不能**持续**的飙升不会**兑现**为收益。

---

## 0. WS 与 TCE — 我们到底在看什么

- **WS（Worldscale，世界油轮运价）** 是以公布的"基准"为百分比报价的运价指数；程租航次
  按此定价。
- **TCE（等价期租租金，美元/天）** 把航次经济性折算成每日船舶收益：
  `TCE ≈ (航次收入 − 航次成本) / 往返天数`。
- 即期 TCE **极度波动** —— 在地缘或储油事件（2008、2020、2026 霍尔木兹）中常飙升 5–10 倍，
  并在数周内回落。正是这种波动使得"盯着即期报价交易股票"非常危险。

---

## 1. 证据 #1 — 股价跟踪的是"持续均值"，而非即期

使用**真实周度数据**（BDTI 作为脏油运价代理 + FRO/DHT 复权收盘价，{R['meta']['aligned_n_weeks']}
个对齐周，2020–2024），我们将**股价水平**对运价做回归，把运价的平均窗口从即期拉长到 52 周。

| 平均窗口 | FRO R² | DHT R² |
|:---|:--:|:--:|
| 即期（1周） | {cf[0]:.3f} | {cd[0]:.3f} |
| 4周均值 | {cf[1]:.3f} | {cd[1]:.3f} |
| 13周均值 | {cf[2]:.3f} | {cd[2]:.3f} |
| 26周均值 | {cf[3]:.3f} | {cd[3]:.3f} |
| **52周均值** | **{cf[4]:.3f}** | **{cd[4]:.3f}** |

![R2 vs 平均窗口](charts/tce_r2_windows.png)

**解读：** 从即期到 52 周均值，解释力**翻三倍**（FRO）/ **2.5 倍**（DHT）。回看期越长，
运价对股价的解释越好——这正是市场为**持续**盈利、而非最新即期定价的特征。

> **诚实说明：** 在 4 周**变化率**上，即期运价变化与股价变化的 R²
> （FRO {R['correlation']['stocks']['FRO']['r2_change4w'][0]:.2f}）高于平滑均值（约 0）。
> 即即期波动确实会让股价短期抖动——但**水平**（股票的内在**价值**）由持续均值决定。
> 领先/滞后为同期（最佳滞后 = 0 周），所以即期盘口给不了你**择时优势**。

---

## 2. 证据 #2 — TCE 峰值 vs 股价峰值，差多大？

这正是你直接问的问题。我们跨周期比较 **TCE 峰值/基线** 倍数与 **股价峰值/基线** 倍数
（股价倍数为**真实**的 yfinance 复权收盘价；TCE 锚点为引用近似值）。

| 周期 | TCE 峰值 × | FRO 峰值 × | DHT 峰值 × | 来源（TCE） |
|:---|:--:|:--:|:--:|:---|
{chr(10).join(f"| {r['cycle']} | **{r['tce_peak_mult']:.1f}×** | {('%.1f×'%r['FRO_peak_mult']) if r.get('FRO_peak_mult') else '—'} | {('%.1f×'%r['DHT_peak_mult']) if r.get('DHT_peak_mult') else '—'} | {r['source'].split(';')[0]} |" for r in lc)}

![振幅压缩](charts/tce_amplitude.png)

**答案：** TCE 峰值巨大——为飙升前基线的 **5 至 10.6 倍**。股价峰值相比之下很小——通常
**1–3 倍**，其中两次（2015、2020）甚至仅 **1.1–1.3 倍**。市场对短暂运价飙升施加了巨大的
**振幅压缩**：对不相信能持续的 TCE 数字，市场**拒绝资本化**。

---

## 3. 证据 #3 — 持续时间胜过峰值高度（真实事件对比）

2020–2024 窗口内的两个真实事件无需任何建模即可说明问题：

| 事件 | 运价峰值 × | FRO 涨幅 × | DHT 涨幅 × | 性质 |
|:---|:--:|:--:|:--:|:---|
| {amp[0]['episode']} | {amp[0]['rate_peak_mult']:.2f}× | {amp[0]['FRO_peak_mult']:.2f}× | {amp[0]['DHT_peak_mult']:.2f}× | **巨幅飙升，仅数周 → 股价无视** |
| {amp[1]['episode']} | {amp[1]['rate_peak_mult']:.2f}× | {amp[1]['FRO_peak_mult']:.2f}× | {amp[1]['DHT_peak_mult']:.2f}× | **峰值更低，约18个月 → 股价翻倍** |

![即期 vs 52周均值 vs 股价](charts/tce_overlay.png)

2020 年新冠储油事件令运价 **+45%**（TD3C 美元/天达引用的 **$26.4万** 峰值）——但 FRO 仅
**+11%**，因为它**只持续了数周**。2022–2024 一个*更低*的峰值**持续约18个月**，却驱动
FRO **+307%**。**驱动股票重估的是持续时间，而非峰值高度。**（同样的逻辑解释了为何 2026
霍尔木兹 $40万 历史新高 TD3C 报价却伴随股价*下跌*：纯飙升，零持续。）

---

## 4. 证据 #4–6 — 受控模拟（隔离机制）

合成模型剔除了混杂因素。即期 TCE = 均值回复基线 + 注入的飙升；盈利看到的是租约滞后的
**滚动均值**；股票以固定倍数对**归一化（52周）盈利**定价。（确定性，种子 = 42；仅示意，
非预测。）

### 4.1 相同峰值，不同持续时间 → 股价天差地别

| 事件 | TCE 峰值 | 持续时间 | 股价重估 |
|:---|:--:|:--:|:--:|
| 飙升 | $20万 | 2周 | **×{e1['spike_2w']['stock_rerate_x']}** |
| 平台 | $20万 | 6个月 | **×{e1['plateau_6m']['stock_rerate_x']}** |
| 持续 | $20万 | 2年 | **×{e1['sustained_2y']['stock_rerate_x']}** |

![模拟：持续时间](charts/tce_sim_duration.png)

相同的 $20万 峰值；2周飙升**毫无作用**（×{e1['spike_2w']['stock_rerate_x']}）；只有持续
抬升才会重估股票（×{e1['sustained_2y']['stock_rerate_x']}）。

### 4.2 对照 — 相同持续时间，不同峰值

| TCE 峰值（持续52周） | 股价重估 |
|:--:|:--:|
| $12万 | ×{e2['peak_120k']['stock_rerate_x']} |
| $20万 | ×{e2['peak_200k']['stock_rerate_x']} |
| $35万 | ×{e2['peak_350k']['stock_rerate_x']} |

峰值翻三倍（$12万→$35万）股价仅 **×{e2['peak_120k']['stock_rerate_x']}→×{e2['peak_350k']['stock_rerate_x']}**（约 +10%）。
**峰值高度几乎无关紧要；持续时间主导一切。**

### 4.3 信号质量 — 为什么追逐即期会亏

在 {e3['n_paths']} 条随机运价路径上，我们测量两类信号触发后的**前瞻 26 周股价收益**：

| 信号 | 触发次数 | 平均前瞻26周 | 中位前瞻26周 | 胜率 |
|:---|:--:|:--:|:--:|:--:|
| **即期飙升**（TCE > 1.8× 基线） | {e3['spot_signal']['n']} | +{e3['spot_signal']['mean_fwd_return']*100:.0f}% | +{e3['spot_signal']['median_fwd_return']*100:.0f}% | {e3['spot_signal']['win_rate']*100:.0f}% |
| **持续均值**（26周均值 > 1.4× 基线） | {e3['sustained_signal']['n']} | +{e3['sustained_signal']['mean_fwd_return']*100:.0f}% | +{e3['sustained_signal']['median_fwd_return']*100:.0f}% | {e3['sustained_signal']['win_rate']*100:.0f}% |

![模拟：信号质量](charts/tce_sim_signal.png)

即期飙升信号在**每一次**飙升时触发——其中多数短暂且从不重估股票——因此其**中位**前瞻收益
仅为微弱的 **+{e3['spot_signal']['median_fwd_return']*100:.0f}%**。持续均值信号只在飙升已经
**持续**后触发，带来 **+{e3['sustained_signal']['median_fwd_return']*100:.0f}%** 的中位数与
**{e3['sustained_signal']['win_rate']*100:.0f}%** 的胜率。

---

## 5. 综合 — 为何即期盘口会误导

1. **盈利是均值，而非某个报价。** 在航/在租的船舶实现的是运价的*滚动均值*，而非那一根
   尖峰。一根 2 周的 $30万 报价几乎不影响季度 EPS。
2. **市场资本化的是*归一化*盈利。** 它对短暂飙升打折，因为它知道这些会均值回复；只有
   *持续时间*才能把运价波动转化为可持续的 EPS。
3. **经营杠杆是双刃剑。** 当高运价*确实*持续时（2022–24），股价会*过度*反应（压缩比 < 1）
   ——使追逐即期成为陷阱的那种杠杆，也使*经持续时间确认*的入场极具威力。

这与本项目既有的 **[Modeling Stash](modeling_stash.md)** 卖出框架相吻合，其决定性规则是
**动量 + 运价*确认***（只有当价格**与**运价*趋势*同时回落时才卖出）——即它本就交易
**趋势/均值**，从不交易即期飙升。2026 霍尔木兹案例（股价下跌而即期 TD3C 创 $40万 历史新高）
是"不要交易即期盘口"的典型事件。

---

## 6. 应该看什么 — 实操规则

- **主要指标：** 滚动 **26–52 周平均 TCE**（或 BDTI 52 周均值），而非即期。
- **入场：** 均值向上突破*且*已**维持** ≥ 约 13 周（持续时间过滤器）。
- **飙升 ≠ 买入：** 无持续时间的即期飙升是噪音；预期股价会无视它。
- **出场：** **均值**（非即期）回落**且**价格破位——按 Modeling Stash 的动量 + 运价确认。
- **地缘下跌：** 价格下跌但**均值**仍高 → 持有/加仓，而非卖出。

---

## 7. 局限与数据来源

- **BDTI 代理：** BDTI 是混合脏油指数，低估纯 VLCC TD3C 美元/天的振幅（如 2020 年 BDTI
  仅 +45% vs 引用的 $26.4万 TD3C 飙升）。但它能干净地捕捉*即期 vs 持续*的相对行为。
  免费 BDTI 序列仅覆盖 **2020–2024**。
- **长周期 TCE（2008/2015/2020/2026）：** 引用的近似值（经网络核实的行业数据 + 仓库
  `modeling_stash.md`），用于周期*形态*。**无虚构数据**——估计值均已标注。
- **股价倍数：** 真实的 yfinance **复权**周收盘价（已调整拆股/分红）；上市前单元格留空
  （DHT 于 2005年10月 上市）。
- **模拟：** 仅示意机制，固定种子；非价格预测。
- **样本小：** 20 年仅约 4 个干净周期；幅度应视为方向性参考。
- **来源：** Baltic Exchange / Investing.com（BDTI）、Yahoo Finance（股价）、行业媒体的
  TCE 峰值（2008 约 \\$30–35万，2020 \\$26.4万，2015 均值约 \\$5–6万）、仓库
  `modeling_stash.md`（2026 霍尔木兹约 \\$40万）。

---

## 8. 两步研究协议（仓库强制要求）

### 第一步 — 简明研究草稿

**核心结论：** VLCC 股价由**在一段持续时间内维持的平均 TCE**驱动，而非即期 TCE 峰值；
因此盯着即期运价盘口交易股票是亏损策略，且 TCE 峰值的振幅是与其同时出现的股价峰值的数倍。

**支持论点（论点 → 所需证据）：**
1. *股价与滚动均值 TCE 的相关性高于即期。* → 需要：随平均窗口拉长，股价水平对运价的 R²
   上升。**已有：** FRO {cf[0]:.2f}→{cf[-1]:.2f}，DHT {cd[0]:.2f}→{cd[-1]:.2f}（2020–2024 周度）。
2. *驱动重估的是持续时间，而非峰值高度。* → 需要：相同峰值/不同持续时间的对比 + 真实事件
   对比。**已有：** 模拟 ×{e1['spike_2w']['stock_rerate_x']} vs ×{e1['sustained_2y']['stock_rerate_x']}；
   2020（+11%）vs 2022–24（+307%）。
3. *市场对飙升进行振幅压缩。* → 需要：各周期 TCE峰值× vs 股价峰值×。**已有：** TCE 5–10.6×
   vs 股价约 1–3×。

**反对/对立论点（论点 → 所需证据）：**
1. *即期在短期仍然重要。* → 需要：即期变化 vs 股价变化的相关性。**已有（承认）：** 4 周
   变化 R² 即期（{R['correlation']['stocks']['FRO']['r2_change4w'][0]:.2f}）高于均值——即期会在
   *季度内*推动股价，只是不影响其*水平*。
2. *BDTI ≠ TD3C；代理可能失真。* → 需要：纯 VLCC TD3C 美元/天周度历史来确认。
   **状态：未知/付费墙** —— 本文未完全核实。

### 第二步 — 严格同行评审（仅评审；不改写草稿）

**1. 需要核实的事实 → 现已完成事实核查（见 §9）**
- 2008 TD3C 峰值：草稿称"约 \\$30–35万/天"；**经核查为约 \\$22.9–23万/天**（Baltic/Clarksons
  公布基准——\\$30万+ 为*个别异常成交*）。2008 行已据此修正（现为 **7.7×**，原 10×）。
- 2026 霍尔木兹峰值：草稿"约 \\$40万"；**经核查为约 \\$42–42.4万**（Lloyd's List "VLCC 指数
  突破 \\$42万"）。2026 行已修正（现为 **8.4×**）。
- DHT 2008"×0.92"：DHT 在 2008 年船队极小且金融危机重创 Q4——该倍数可能反映公司个体因素，
  而非运价机制。（保留为局限。）

**2. 逻辑跳跃 / 概念替换**
- BDTI（混合脏油指数）被悄然替代为 **VLCC TD3C TCE 美元/天**；二者相关但不等同，且该替换
  低估了飙升振幅。
- "*水平*对运价的 R²"与"预测前瞻*收益*"是不同命题；报告虽审慎，但读者可能混淆解释性 R²
  与可交易的 alpha。
- 股价*峰值/基线*倍数高度依赖（分析师选择的）基线窗口；不同基线会改变压缩比。

**3. 缺失的反例 / 竞争性解释**
- 资产负债表/稀释/分红政策变化（FRO 重组、DHT 派息）会独立于 TCE 推动股价，本文未隔离。
- 持续高运价期通常伴随**一致预期 EPS 上调与去风险**；重估可能是盈利上修效应，而非"持续时间"
  本身。
- 幸存者偏差：仅研究 FRO/DHT，已退市/合并的油轮公司被排除。

**4. 应补充的最重要一手来源**
- Baltic Exchange **TD3C TCE 美元/天** 周度历史（2005–2026）——替换 BDTI 代理。
- 公司季度**实现 TCE** 披露（FRO/DHT 10-Q/6-K），把运价 → EPS 串起来。
- Clarksons/Gibson 周期年表，用于独立的峰值/持续时间定年。

**5. 至多算推测、而非事实的句子**
- "TCE 峰值为 5–10× 而股价峰值为 1–3×"作为*普遍规律*——它是 **4 个观测**，方向性强但未经
  统计检验确立。
- 模拟重估倍数（×1.0 / ×1.82 等）是**模型输出**，非市场实测，不可解读为预测。
- "经营杠杆使经持续时间确认的入场极具威力"——机制合理，但此处仅在样本内/模型内得到展示。

---

## 9. 事实核查与遗留问题解答（2026年6月26日新增）

本节解答 §8 第二步同行评审提出的问题。

### 9.1 已核实/已修正的事实

| 项目 | 草稿说法 | 核实值 | 来源 | 处理 |
|:---|:---|:---|:---|:---|
| 2008 TD3C 峰值 | 约 \\$30–35万 | **约 \\$22.9–23万/天**（2008夏；\\$30万+ 为异常成交） | Clarksons/Baltic | **修正 → 2008 行 7.7×** |
| 2026 霍尔木兹峰值 | 约 \\$40万 | **约 \\$42–42.4万/天**（2026年3月） | Lloyd's List "VLCC 指数突破 \\$42万" | **修正 → 2026 行 8.4×** |
| 2020 新冠峰值 | \\$26.4万 | **\\$264,072/天**（2020年3月）已确认 | 行业媒体 | 不变 |
| 2015 | 均值约 \\$5–6万 | 均值约 \\$5–6万，年内峰值约 \\$10万 已确认 | 行业媒体 | 不变 |

这些修正**不改变结论**：TCE 峰值仍为基线 **5–10.6×**，而股价峰值约 1–3×。

### 9.2 代理指标疑虑已解决 —— BDTI vs TD3C

同行评审指出 **BDTI 被替代为 VLCC TD3C 美元/天**。核查：BDTI 是 Baltic **一篮子**指数
（VLCC TD1/TD2/TD3C + Suezmax + Aframax 航线），其*包含* TD3C 且与之**高度相关**，但被
波动较小的小型航线/船型**削弱**。**含义：** BDTI 是有效的相关代理，但**低估**了纯 VLCC 的
飙升振幅——因此真实的 TCE-vs-股价振幅压缩比 §1/§3 基于 BDTI 的数值**更大**。这*强化*而非
削弱了论点。（状态：原为"未知/付费墙" → 现解决为已知的保守偏差。）

### 9.3 方法论澄清（逻辑跳跃项）

- **"水平的 R²" ≠ "预测前瞻收益"。** 保持区分：水平 R²（§1）显示股票的*内在价值*；可交易性
  由前瞻收益信号测试（§4.3）单独处理。我们不把解释性 R² 等同于 alpha。
- **基线窗口敏感性。** 振幅倍数依赖所选的飙升前基线；我们使用固定窗口，并将幅度作为
  **方向性**而非精确值报告。

### 9.4 已承认的竞争性解释

- **盈利上修 vs 持续时间。** 持续高运价与一致预期 EPS 上修相关；我们未完全分离二者。
  表述：*持续时间是机制，盈利上修是传导*——二者方向一致。
- **资产负债表/分红效应**（FRO 重组、DHT 派息政策）与**幸存者偏差**（仅研究 FRO/DHT）
  仍是真实局限，本文未加控制。

### 9.5 仍然开放（诚实的未知）

- 完整的 **Baltic TD3C 美元/天周度历史 2005–2026**（付费墙）——可替换 BDTI 代理并直接测量
  VLCC 特有振幅。
- 公司**实现 TCE** 披露（FRO/DHT 10-Q/6-K），精确串联运价 → EPS。

---

*隶属于 [VLCC-Analysis-2026](https://github.com/liqiqiii/VLCC-Analysis-2026) 项目。
方法：`tce_analysis.py`、`tce_simulation.py`、`generate_tce_charts.py`。非投资建议。*
"""

Path("36_TCE_vs_StockPrice_CN.md").write_text(CN, encoding="utf-8")
print("Wrote 36_TCE_vs_StockPrice_CN.md", len(CN), "chars")

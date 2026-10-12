---
layout: default
title: "DHT Q4 2026 Bookings: A $520m Profit Scenario, Annualized-Quarter P/E, and Frontline 2008"
lang: en
---

# DHT's $509,100/day bookings: a profit step-change, but which P/E?

**Research snapshot: October 12, 2026**

> **Charter-anchor extension:** [Static/dynamic P/E, 2006-2008 period fixtures and what a term charter actually locks](charter_anchor_en) adds the $230,000/day broker assessment, recent owner-disclosed contracts and conditional single-ship profit/calendar-year calculations.

> **Historical extension:** [Frontline 2007Q1-2009Q2: original prices, quarterly TTM/full-year P/E and crisis timing](fro_2007_2009_en) adds the quarterly reconstruction, exact vendor peak dates, an explicitly approximate reporting-lag series, and the distinction between quarterly, ex-items and TTM earnings peaks.

[中文报告](report_cn) | [Research hub](../) | [Cycle research](../vlcc_cycles/report_en) | [Calculation script](https://github.com/liqiqiii/VLCC-Analysis-2026/blob/master/dht_q4_2026/run_analysis.py)

> **Conclusion:** DHT's own bookings materially strengthen near-term earnings visibility. Approximately **$520 million of Q4 profit is plausible if the remaining fixtures stay near $500,000/day**, under the assumptions below. But approximately **2x is an annualized-quarter P/E, not reported TTM P/E**. Frontline's original filings do not establish a clean "2x P/E at the 2007-2008 share-price peak" precedent; prices around 2x FY2008 earnings are visible in March 2009, after the crash.
>
> **Scenario overview:** remaining-day TCE of **$100,000 / $250,000 / $500,000** produces illustrative Q4 profit of **$346.2m / $414.0m / $527.0m**. At the dated **$26.22** reference price, reported trailing P/E is approximately **8.9x**; an illustrative FY2026 estimate incorporating a $520m Q4 gives **3.7x**; annualizing that hypothetical quarter gives **2.0x**. These are different earnings periods, not three competing estimates of the same metric.

**Scope and protocol.** This is a focused earnings and historical-multiple fact-check, not a new full-company valuation or trade instruction. It follows the repository's two-step research protocol, separates disclosures from assumptions, provides matching bilingual tables and records adversarial-review findings. Unsupported price targets, probabilities and cycle-top dates remain **unknown**, rather than being invented to fill a template. No existing forecast curve or chart is recalibrated by this note. Analysis only; not personalized investment advice.

## Step 1 — Concise research draft

### Core conclusion and evidence requirements

| Type | Claim → evidence needed | Status |
|---|---|---|
| Support | High rates have reached DHT's own business, not just an industry assessment → company-specific fixtures and coverage | Obtained: the October 12 update reports approximately 50% of Q4 spot days booked at $509,100/day [S1] |
| Support | A $520m quarter is arithmetically plausible → covered revenue, remaining-day rates, revenue days and accounting costs | Conditional: the model requires approximately $484,466/day on uncovered days, with the day and cost assumptions below |
| Support | The historical 2x-top analogy needs qualification → original-basis prices, matching EPS and dated financial statements | Obtained: Frontline's filed year-end ratios and historical trading ranges; exact peak-day information-available TTM P/E remains unconstructed [S4] |
| Counter | The remaining fixtures can be materially weaker → further booking updates and final quarterly accounts | Unknown: the reported $509,100 is not the rate for every Q4 spot day |
| Counter | A low run-rate multiple can reflect temporary earnings rather than cheap shares → subsequent-quarter earnings, contracts and asset values | Unresolved: a single exceptional quarter establishes neither undervaluation nor a sell signal |

### 1. What DHT disclosed

The company's October 12 business update reports the following [S1]:

| Metric | Disclosure | Interpretation |
|---|---:|---|
| Q3 estimated fleet TCE | $141,300/day | Operating estimate, not a reported net-profit result |
| Q3 estimated spot TCE | $167,100/day | Company spot earnings estimate |
| Q3 estimated term-charter TCE | $114,200/day | Not the user's assumed $80,000/day blend |
| Q3 revenue days | 2,055 | Includes 1,054 spot days |
| Q4 available spot days booked | Approximately 50% | Not full-quarter coverage |
| Rate on booked Q4 spot days | $509,100/day | Discharge-to-discharge basis |
| Q4 total revenue days covered | Approximately 78% | Includes spot and term-charter days |
| Average rate on that covered portion | $225,200/day | The model's company-disclosed blended anchor |

**This is a genuine improvement in evidence quality:** company bookings are more informative about DHT's earnings than an isolated TD3C panel assessment. Nevertheless, booked voyages still need to be performed; bookings are not collected cash or finalized accounting income.

The calculation does **not** assume a fixed number of term-chartered ships at a uniform daily rate. A roster at one date is not a quarter's revenue-day allocation, and some term arrangements include profit sharing. Using the disclosed covered blend avoids inserting an unverified vessel-count mix. The model covers DHT's combined spot and term business; it is not a spot-only fleet model.

### 2. Reconstructing the $520m case

Let `R` be the TCE achieved on the remaining uncovered revenue days:

```text
Illustrative Q4 net profit
  = 2,055 × [0.78 × $225,200 + 0.22 × R] − $60,000,000
```

| Input | Value | Classification |
|---|---:|---|
| Q4 revenue days | 2,055 | Assumption: Q3 proxy, not Q4 guidance |
| Covered fraction | 78% | Rounded company disclosure |
| Covered TCE | $225,200/day | Company estimate, held unchanged across scenarios |
| Uncovered fraction | 22% | Remainder, treated as unbooked spot exposure |
| Post-TCE accounting charges | $60.0m | Assumption, not a fixed-cost guarantee |
| Exceptional Q4 gains/losses | Modeled as $0 | Actual amount unknown; not a prediction that none will occur |

The cost reference is DHT's Q2 disclosure [S2]:

| Post-TCE item | Q2 amount |
|---|---:|
| Vessel operating expenses | $18.6m |
| Depreciation and amortization | $27.8m |
| General and administrative expenses | $5.6m |
| Net financial expenses | $4.8m |
| **Total** | **$56.8m** |

The illustrative $60.0m deduction rounds that reference upward, but is **not demonstrated to be conservative**. Off-hire, operating costs, depreciation, financing, tax, profit sharing and non-operating items can change. TCE already deducts voyage expenses: do not subtract bunkers and port costs again. Debt principal repayments are not accounting expenses. This bridge deliberately avoids the unresolved cash-breakeven/EPS specification in the older cycle model.

#### Five-rate sensitivity

All P/E figures in this table use **four times the hypothetical quarter's profit**. None is TTM P/E or a forecast of four identical quarters.

| Uncovered-day TCE | Illustrative Q4 profit | Illustrative Q4 EPS | Annualized-Q4 P/E at $26.22 |
|---:|---:|---:|---:|
| $100,000/day | $346.2m | $2.15 | 3.05x |
| $150,000/day | $368.8m | $2.29 | 2.87x |
| $250,000/day | $414.0m | $2.57 | 2.55x |
| $350,000/day | $459.2m | $2.85 | 2.30x |
| $500,000/day | $527.0m | $3.27 | 2.01x |

These are sensitivity cases, **not probabilities or a consensus/base/bull forecast**.

- The covered portion represents approximately **$361.0m of modeled TCE revenue**, not a guaranteed profit floor.
- The uncovered portion represents approximately **452.1 modeled revenue days**.
- Each **$100,000/day** change on those days changes modeled profit by **$45.21m**, holding all other inputs constant.
- A **$520m** result requires approximately **$484,466/day** on those uncovered days.

This is operating leverage: much of additional TCE revenue reaches profit if costs remain stable. The response is linear in this simplified model; it is not evidence of an independently validated nonlinear profit engine. The covered blend may also change with profit sharing, which is not varied here.

### 3. Reported TTM, estimated full year and annualized quarter

The valuation reference is **$26.22**, quoted in the October 12 market report [S3], not a claimed live terminal price or closing price. Using **161,235,573 shares**, last reported at June 30 [S2], gives approximate market capitalization of **$4,227.6m**. These are market-cap/net-income approximations, not a vendor's exact weighted-average-EPS P/E.

| Denominator | Earnings | Approximate P/E | Status |
|---|---:|---:|---|
| Latest four reported quarters through Q2 2026 | $473.7m | 8.9x | Reported-income trailing comparison |
| Illustrative FY2026, with a $520m Q4 | $1,147.4m | 3.7x | Estimate, not reported TTM |
| Hypothetical $520m Q4 repeated four times | $2,080.0m | 2.0x | Annualized run-rate comparison only |

The reported trailing bridge [S2]:

```text
Q3 2025 $44.8m + Q4 2025 $66.1m
  + Q1 2026 $164.5m + Q2 2026 $198.3m = $473.7m
```

The full-year illustration:

```text
Q3 net-income proxy before the sale gain
  = 2,055 × $141,300 − $60.0m = $230.4m
Q3 reported-income proxy
  = $230.4m + anticipated $34.2m vessel-sale gain = $264.6m
FY2026 illustration
  = Q1 $164.5m + Q2 $198.3m + Q3 $264.6m + Q4 $520.0m
  = $1,147.4m, using unrounded inputs
```

The net-income proxy is **after the modeled financing and other post-TCE charges**. Final Q3 net income was not supplied in the October 12 operating update. The anticipated Q3 sale gain comes from the previously announced DHT Bauhinia sale. Q1 reported income also includes a **$60.0m vessel-sale gain**. Therefore, the FY2026 illustration is **not normalized or purely freight-derived earnings** [S2].

A hypothetical **$520m** quarter would generate approximately **$3.23 EPS**, or a **12.3% quarterly earnings yield** at the reference price. Repeating that quarter four times is a separate assumption. DHT's ordinary-income payout policy does not make this a declared Q4 dividend, and accounting earnings are not free cash flow.

### 4. Frontline's original 2007-2008 record

The primary reference is Frontline's FY2008 annual report, printed pages **5-6** and **62** [S4]. Values below are on the original historical share basis, before the later reverse split.

| Fiscal year | Reported net income | Basic EPS | Company-reported year-end P/E |
|---|---:|---:|---:|
| 2007 | $570.418m | $7.62 | 6.3x |
| 2008 | $698.770m | $9.15 | 3.2x |

The filing explicitly defines P/E as **closing year-end share price divided by basic earnings per share**. These are retrospective ratios using the fiscal year's earnings, not proof of what an investor knew at year-end.

The listing table records:

| Period | Original NYSE price range |
|---|---:|
| Q2 2008 | $46.34-$72.36 |
| Full year 2008 | $25.00-$72.36 |
| March 2009 | $15.78-$20.75 |

Thus, **$72.36 was the 2008 high, reached during Q2**. The precise peak trading day and its contemporaneously available TTM denominator have not been reconstructed here.

#### What if the peak quarter is annualized, as in the DHT case?

Frontline's Q2 release [S5] reports:

| Q2 2008 item | Amount |
|---|---:|
| Reported net income | $318.4m |
| Reported EPS | $4.25 |
| Company-identified gains | $155.4m |
| Net income excluding those gains | $163.0m |
| Weighted-average shares | 74,837,257 |

The identified gains were approximately **48.8%** of reported profit. They included asset/lease-related gains, a settlement and a mark-to-market gain; they were not all recurring freight earnings.

| Retrospective calculation at the $72.36 high | Multiple |
|---|---:|
| Price / (Q2 reported EPS × 4) | 4.3x |
| Price / (Q2 EPS excluding company-identified gains × 4) | 8.3x |

**Both calculations use subsequently reported Q2 earnings and are hindsight comparisons, not observed peak-day valuation ratios.** Excluding the specified gains is not a complete normalization of earnings.

#### Where does approximately 2x appear?

```text
March 2009 price / FY2008 basic EPS:
  $15.78 / $9.15 = 1.72x
  $20.75 / $9.15 = 2.27x
```

This establishes a **post-crash example** near 2x earnings. It does not establish when that multiple first appeared or rule out every other definition of peak-period P/E. The narrow conclusion is that the remembered **"2x at the 2007-2008 price peak" claim is not supported by these original-source comparisons**.

### 5. What this changes in the repository

The older [Modeling Stash](../modeling_stash) lists a **2.66x** FRO peak multiple using **$135.78 / $51.10**. That calculation remains **unreconciled** with the original-basis prices and EPS above. It should not be used as an established sell threshold.

Potential historical-data pitfalls include:

- Applying a split adjustment to the price but not EPS, or vice versa. Adjusting both consistently preserves P/E.
- Dividing a dividend-adjusted historical price by unadjusted EPS; total-return prices are not historical valuation prices.
- Combining a price peak with later-released earnings without labeling the look-ahead.
- Treating gains as recurring operating profit.

The exact cause of the old 2.66x discrepancy has **not** been traced. This note flags the unsupported benchmark without inventing a specific data bug.

The [cycle report](../vlcc_cycles/report_en) also documents Frontline's historical charter-in, lease and profit-sharing structure. Those obligations, earnings mix and accounting differences make direct comparisons with DHT imperfect. This note does not revive withdrawn NAV claims or equate total liabilities with interest-bearing debt.

### 6. Cycle interpretation and decision boundaries

**Current position:** exceptional company-specific booked rates and stronger near-term earnings visibility. **Unknown:** the final cycle top and whether the rate environment will persist into subsequent quarters.

Three observations matter next:

1. Does Q4 coverage progress from the current **50% of spot days** at similarly strong rates?
2. Do new **Q1 2027** bookings support a continuation, rather than just recognition of old high-rate voyages?
3. Do comparable term-charter fixtures and asset values support durable economics? A single contract is not a market floor.

The broader historical lesson survives: a cyclical stock can show a low earnings multiple because earnings are temporarily high, because the share price has already fallen, or both. A fixed P/E line alone does not identify which process is occurring.

**This update neither validates, invalidates nor by itself triggers the previously discussed staged-exit template.** No automatic sale or purchase follows from the 2x calculation. Large cash generation may benefit shareholders before rates normalize, but high reported profit is not proof of safety.

#### Day1Global checks, uncertainty and pre-mortem

| Lens | Application to this focused note |
|---|---|
| Revenue quality and forward guidance | Own-company bookings improve visibility; uncovered days and subsequent quarters remain open |
| Profitability and operating leverage | Show the rate-to-profit bridge and fixed-input sensitivity, rather than extrapolating a headline rate to every ship |
| Cash flow | Net income differs from cash collection, maintenance/newbuild spending, financing cash flows and distributable income |
| Ownership and management | No new ownership conclusion; a payout policy is not a declaration of this hypothetical dividend |
| Accounting quality | Keep TCE, post-TCE costs, sale gains and earnings periods separate; do not expense debt principal |
| Valuation and competition | Historical FRO is an imperfect comparator; no fresh full-company or fleet-NAV target is established |
| Quality/growth versus value perspectives | One exceptional quarter proves neither a durable moat nor a long-term growth regime; margin of safety is not identifiable from run-rate P/E alone |
| Long/short, catalyst and macro perspectives | Subsequent fixtures, normalization and financing conditions can move earnings and valuation in different directions |

**Pre-mortem:** if the investment disappoints, candidate explanations are weaker remaining fixtures, a short-lived earnings pulse, operational/cost surprises, or asset-value and market-multiple compression. Early warnings are new booking rates, actual revenue days/costs, cash conversion and comparable ship transactions. Their probabilities are **unknown**; no artificial weights are assigned.

**Anti-bias check:** do not anchor on 2x, cherry-pick a historical peak, confuse a subsequent earnings release with information available then, or assume a headline equals the whole fleet's realized rate.

| Requested-style output | Publication decision |
|---|---|
| 12-month conservative/base/bull price targets | Not established: no validated forward full-company valuation is supplied |
| 24-month conservative/base/bull price targets | Not established: rate duration, capital allocation and terminal asset values remain uncertain |
| Time to cycle peak | Unknown; no calendar mapping or fitted countdown |
| New two-cycle correlation/lead-lag estimate | Not calculated in this focused fact-check; existing cycle research is background, not new validation |
| Inflation adjustment | The comparison is between dimensionless P/E ratios. Historical dollar prices/EPS are identified on their original nominal basis, not used to claim equal real purchasing power |

## Step 2 — Strict peer review

### 1. Facts that need verification

Final Q4 revenue days, uncovered fixtures, post-TCE charges and final Q3/Q4 net income remain unknown. The reference share price is a dated media quote, not live data. The historical peak-day, information-available TTM P/E has not been reconstructed.

### 2. Logical leaps / equivocation (concept substitution)

Annualizing one quarter is not TTM or a next-year forecast. Bookings are not cash collected. A hypothetical EPS is not earned income or a declared dividend. Market-charter conditions do not exactly determine DHT's existing contract profits. Retrospective historical ratios do not establish contemporaneous investor expectations.

### 3. Missing counterexamples / competing explanations

High earnings can create shareholder value before normalizing. A low P/E can arise after a share-price crash rather than at a top. Fixed contracts can cushion declining spot rates. Frontline's identified gains and contractual structure weaken a direct comparison.

### 4. The most important primary sources that should be added

DHT's next operating update and final quarterly financial statements; details of remaining fixtures, revenue days and profit sharing; and a point-in-time Frontline daily price/reporting-date series to reconstruct a true peak-day trailing multiple. The existing primary and reproduced company disclosures are listed below.

### 5. Which sentences can at most be classified as speculation, not fact

"Q4 profit will be $520m," "the remaining fixtures will stay near $500,000/day," "2x marks the top," and "the next year will repeat Q4" are not established facts. Scenario outputs are conditional arithmetic, not probability-weighted forecasts.

### Adversarial-review record

The underlying research was submitted to a **GPT-6-Astra rubber-duck reviewer** on October 12 before this bilingual publication. The reviewer was asked to find errors, not encouragement, using the complete numerical bridge and original-source historical figures. The following findings were accepted and applied; no multi-model consensus is claimed.

| Finding | Verdict | Action in this publication |
|---|---|---|
| Retaining a prior exit plan can sound like validating it | Correct | No recommendation or trigger is inferred from the new multiple |
| Hypothetical EPS must not be described as earned income or a dividend | Correct | Use conditional EPS and quarterly earnings yield; no Q4 dividend assumed |
| Revenue days, costs and the covered blend are not guarantees | Correct | Put assumptions beside the scenario table; do not claim a profit floor |
| TTM and FY2026 comparisons require different labels and treatment of gains | Correct | Separate periods, dated price/share count and one-off gains |
| Year-end P/E and later-reported Q2 earnings cannot reconstruct peak-day valuation | Correct | Label hindsight calculations and leave the contemporaneous multiple unknown |
| The old 2.66x benchmark's exact error is unproven | Correct | Mark it unreconciled, not a diagnosed split-adjustment bug |

**Publication review:** a further GPT-6-Astra check of both completed pages and the calculator found no blocking issues and identified the following presentation corrections. It did not constitute a new audit of the external sources.

| Finding | Verdict | Action |
|---|---|---|
| A standalone page title could lose the scenario and earnings-period qualifiers | Correct | Both titles now specify a profit scenario and annualized-quarter P/E |
| The Chinese exceptional-item row could imply that no assumption was made | Correct | Both versions now state a $0 model input and an unknown actual outcome |

## Sources and reproducibility

All research references were consulted on **October 12, 2026**. Company releases republished by a newswire host are identified as such, rather than represented as independent corroboration.

| ID | Source | Used for |
|---|---|---|
| S1 | [DHT business update, October 12, 2026 — company release via GlobeNewswire/FinancialContent](https://www.financialcontent.com/article/gnwcq-2026-10-12-dht-holdings-inc-business-update) | Q3 operating estimates and Q4 booking coverage/rates |
| S2 | [DHT Q2 2026 results, August 5 — SEC 6-K exhibit reproduced by StockTitan](https://www.stocktitan.net/sec-filings/DHT/6-k-dht-holdings-inc-current-report-foreign-issuer-ad17bec30560.html) | Reported quarterly income, costs, shares, gains and payout policy |
| S3 | [StockStory market report, October 12 — FinancialContent](https://markets.financialcontent.com/stocks/article/stockstory-2026-10-12-why-dht-holdings-dht-stock-is-up-today) | $26.22 reference price only; secondary market source |
| S4 | [Frontline FY2008 annual report — AnnualReports copy](https://www.annualreports.com/HostedData/AnnualReportArchive/f/NYSE_FRO_2008.pdf) | Original financial table on printed pages 5-6 and price ranges on printed page 62 |
| S5 | [Frontline Q2 and six-month 2008 results — company website](https://www.frontlineplc.cy/fro-second-quarter-and-six-months-2008-results/) | Quarterly EPS, company-identified gains and weighted-average shares |

Reproduce all arithmetic from the repository root; Python's standard library is sufficient:

```bash
python3 dht_q4_2026/run_analysis.py
```

The script uses dated inputs and exact decimal arithmetic, prints the scenario and valuation results, does not fetch live prices and does not modify other models.

[中文报告](report_cn) | [Back to research hub](../)

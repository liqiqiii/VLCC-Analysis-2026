# Reusable Prompt Templates for Stock/Industry Analysis

> **Generic prompt templates extracted from the VLCC Analysis Project (19 prompts).**
> Replace `[COMPANY]`, `[INDUSTRY]`, `[METRIC]` placeholders with your specifics.
> Each template includes: purpose, when to use, and the prompt itself.
> Last updated: March 4, 2026.

---

## Template 1: Cycle-Peak Valuation Backtest
> *Origin: VLCC Prompts 1-2*

**When to use**: Cyclical industries (shipping, commodities, semiconductors, real estate) where historical cycle peaks inform current valuation.

```
Perform a cycle-peak valuation backtest for [COMPANY_A] and [COMPANY_B] in the [INDUSTRY] sector:

1. Data standards:
   - Use latest real [ASSET] counts (e.g., fleet size, fab capacity, store count).
   - If mixed portfolios, convert to [PRIMARY_ASSET]-equivalents with appropriate ratios.
   - Account for scale effects: smaller units have higher per-unit costs.
   - All historical market caps CPI-adjusted to [CURRENT_YEAR] USD.

2. Cycle positioning:
   - [YEAR_1]: [Description of cycle type] (e.g., super cycle, demand-driven)
   - [YEAR_2]: [Description of cycle type] (e.g., pulse, supply shock)
   - [CURRENT_PERIOD]: [Description] — positioned between [YEAR_1] and [YEAR_2].
   - Use mid-to-upper-range per-asset market cap for target valuation.

3. Calculate:
   - Inflation-adjusted per-[ASSET]-equivalent market cap at each cycle peak.
   - Current [ASSET] count × equivalent factor.
   - Conservative / Neutral / Optimistic target market caps.
   - Upside vs current market cap.
   - Conclusion: Who has more elasticity? Who has better risk/reward?

4. Enhance with current thesis:
   - [SUPPLY_CONSTRAINT_1]
   - [SUPPLY_CONSTRAINT_2]
   - [DEMAND_DRIVER]
   - Consider whether current prices will break inflation-adjusted historic highs.

5. Output: Concise, model-ready, no contradictions.
```

---

## Template 2: Fundamental Deep-Dive (Model Divergence)
> *Origin: VLCC Prompt 6*

**When to use**: When your initial model shows unexpected results (e.g., two similar stocks with very different implied upside).

```
[COMPANY_A] and [COMPANY_B] have very similar [TIMEFRAME] price trajectories
(both [PATTERN]). But my model shows [COMPANY_A] has significantly higher
upside than [COMPANY_B], which doesn't match market behavior.

Do a deep dive on both companies:
1. Fetch latest public filings, earnings reports, and industry data.
2. Compare: [KEY_METRICS] (e.g., fleet composition, debt levels, contract
   structure, management quality, capex pipeline).
3. Identify structural differences that explain the model divergence.
4. Propose 3-5 potential explanations ranked by likelihood.
5. Recommend model adjustments.
```

---

## Template 3: Operating Leverage / SaaS Economics Analysis
> *Origin: VLCC Prompt 8 (Part 1)*

**When to use**: Any high-fixed-cost industry where profit scales non-linearly above breakeven.

```
Analyze the operating leverage (SaaS-like economics) of [INDUSTRY]:

1. [ASSET_TYPE] profit behaves like SaaS — a [X]% revenue increase can lead
   to exponentially higher profit because [FIXED_COST_COMPONENTS] are
   essentially fixed.

2. For each asset type in the industry:
   - [ASSET_TYPE_1]: Calculate breakeven [RATE/PRICE], current [RATE/PRICE],
     and profit multiplier at 1x, 1.5x, 2x, 3x breakeven.
   - [ASSET_TYPE_2]: Same analysis.
   - [ASSET_TYPE_3]: Same analysis.

3. Show the non-linear profit curve:
   - At breakeven: $0 profit
   - At 2x breakeven: [X]% margin
   - At 3x breakeven: [Y]% margin (demonstrate the acceleration)

4. Apply this to [COMPANY_A] and [COMPANY_B]:
   - Current operating rates vs breakeven
   - Incremental profit per $[UNIT] rate increase
   - Which company benefits more from operating leverage and why?
```

---

## Template 4: Supply-Side Reality Check
> *Origin: VLCC Prompt 8 (Part 2 — OPEC check, generalized)*

**When to use**: When a major supply-side announcement (OPEC, TSMC capex, housing starts) needs verification against actual data.

```
Reality-check [ENTITY]'s announced [SUPPLY_ACTION]:

1. Announced vs actual: [ENTITY] announced [SPECIFIC_ACTION], but announced
   changes don't always materialize. Check:
   - Historical pattern: How often do announced [CHANGES] become actual?
   - Compensatory adjustments (e.g., offsetting cuts, delays, cancellations).
   - The "frontloading" gap between announcement and execution.

2. Compare to historical cycles:
   - [CYCLE_1]: What did [ENTITY] actually do vs announce?
   - [CYCLE_2]: Same comparison.
   - Current: What is ACTUALLY happening?

3. Find real [OUTPUT/SUPPLY] numbers from primary sources.

4. Impact on [INDUSTRY] thesis: Does the reality support or undermine the
   current investment case?
```

---

## Template 5: Charter / Contract Structure Comparative Analysis
> *Origin: VLCC Prompts 12-13*

**When to use**: Comparing companies with different revenue lock-in strategies (spot vs contract, fixed vs variable, hedged vs unhedged).

```
Analyze the contract/revenue structure differences between [COMPANY_A] and
[COMPANY_B]:

1. Revenue mix:
   - [COMPANY_A]: [X]% spot / [Y]% contract / [Z]% hedged
   - [COMPANY_B]: [X]% spot / [Y]% contract / [Z]% hedged

2. For each company, calculate:
   - Sensitivity to [PRICE/RATE] changes (per $[UNIT] move)
   - Earnings elasticity (% change in earnings per % change in rate)
   - Revenue stability (standard deviation of quarterly earnings)
   - Breakeven rate under each contract structure

3. Generate comparison:
   - Rate sensitivity chart (earnings vs rate scenarios)
   - Upside capture: Who benefits more when rates surge?
   - Downside protection: Who is more protected when rates collapse?

4. Cross-check: If other sources show different contract splits, reconcile
   the data. Distinguish between:
   - Booking rate (% of near-term days contracted)
   - Structural split (long-term spot/contract ratio)
   - These are different metrics that are often confused.
```

---

## Template 6: Cross-Market Peer Comparison (Different Exchanges)
> *Origin: VLCC Prompts 15, 16b*

**When to use**: Comparing companies listed on different exchanges (e.g., A-share vs NYSE) where valuation premiums/discounts exist.

```
Compare [COMPANY_A] ([EXCHANGE_A]) with [COMPANY_B] ([EXCHANGE_B]):

1. CRITICAL: Both companies are diversified — do NOT divide total market cap
   by [PRIMARY_SEGMENT] count alone.

2. Use 4 methods:
   a. **Per-total-asset**: Market cap ÷ total [ASSET] count (all segments).
   b. **Sum-of-Parts (SOTP)**: Estimate each segment's value, isolate
      [PRIMARY_SEGMENT] for apples-to-apples comparison.
   c. **PE Comparison**: Forward PE under same assumptions.
   d. **Hidden Value**: Identify assets invisible in single-segment metrics
      (e.g., long-term contracts, IP, real estate).

3. Calculate the TRUE cross-market premium/discount:
   - Raw premium (misleading): [X]x
   - SOTP-adjusted premium (correct): [Y]x
   - Explain the residual with structural factors:
     [FACTOR_1], [FACTOR_2], [FACTOR_3]

4. Conclusion: Is the premium justified, excessive, or actually a discount?
```

---

## Template 7: Full-Portfolio Earnings Recalculation
> *Origin: VLCC Prompt 16*

**When to use**: When initial earnings model only covered one segment of a diversified company.

```
The [YEAR] earnings model for [COMPANY] only accounted for [PRIMARY_SEGMENT]
uplift. But [COMPANY] has [N] total [ASSETS] across [N] segments:
- [SEGMENT_1]: [COUNT] units, [RATE/PRICE] characteristics
- [SEGMENT_2]: [COUNT] units, [RATE/PRICE] characteristics
- [SEGMENT_N]: ...

Recalculate earnings using:
1. Each segment separately with current market rates.
2. Segment-specific sensitivities (per $[UNIT] rate change).
3. Different spot/contract exposure per segment.
4. Conservative / Base / Bull scenarios for EACH segment.

Show:
- Old model (single-segment) vs New model (full portfolio)
- % difference and which segments were missed
- Updated target prices on full-portfolio basis
```

---

## Template 8: Alternative Scenario Modeling
> *Origin: VLCC Prompts 17-18*

**When to use**: When current market conditions diverge significantly from sell-side consensus.

```
Current [METRIC] is [CURRENT_VALUE]. Sell-side consensus assumes
[CONSENSUS_VALUE]. Model the alternative scenario where [CURRENT_VALUE]
is the real baseline.

1. Rationale for alternative baseline:
   - [SUPPLY_REASON]
   - [DEMAND_REASON]
   - [STRUCTURAL_REASON]
   - Current [METRIC] is already at [CURRENT_VALUE]

2. Side-by-side comparison:
   | | [CONSENSUS] Base | [ALTERNATIVE] Base | Delta |
   | Earnings | | | |
   | EPS | | | |
   | PE | | | |
   | Target Price | | | |

3. CRITICAL: Update EVERY section of the report (Rule 11):
   - TL;DR, target prices, investment recommendation, peer comparison
   - Do NOT just add a standalone section

4. Key question: When will sell-side re-anchor to [ALTERNATIVE]?
   What are the catalysts?
```

---

## Template 9: Day1Global Framework Application
> *Origin: VLCC Prompts 7, 19*

**When to use**: Every stock analysis. This is the master analytical framework.

```
Apply the Day1Global tech-earnings-deepdive framework to [COMPANY]:

MODULE C — Cash Flow ("THE BIG ONE"):
- Operating Cash Flow, Capex, Free Cash Flow (3-year history + forecast)
- FCF Yield at current market cap
- Dividend coverage ratio
- FCF after dividend — what's left for reinvestment or debt reduction?
- Grade: A/B/C/D/F

MODULE L — Ownership & Management:
- Top shareholders and their strategic motivation
- Management alignment with minority shareholders
- Related-party transaction risk
- Key person risk
- Grade: A/B/C/D/F

MODULE O — Accounting Quality:
- Revenue recognition (clean or aggressive?)
- D&A policy (standard or aggressive?)
- Impairment risk (asset values vs market)
- Off-balance-sheet obligations
- Red flags to watch
- Grade: A/B/C/D/F

6 INVESTMENT PERSPECTIVES:
1. Quality Compounder (Buffett) — durable advantage?
2. Imaginative Growth (ARK) — 10x optionality?
3. Long/Short (Tiger Cubs) — what's mispriced?
4. Deep Value (Klarman) — margin of safety?
5. Catalyst Driven (Ackman) — what unlocks value, when?
6. Macro Tactical (Druckenmiller) — cycle positioning?

ANTI-BIAS: What 6 cognitive traps apply here? How do we mitigate each?

PRE-MORTEM: "It's [TIMEFRAME] later and you lost 40%. What went wrong?"
List 3-5 specific scenarios with probabilities and early warning signs.
```

---

## Template 10: Historical Cycle PE/PB Reference
> *Origin: VLCC Prompts 1, 9, 15 — container cycle parallel*

**When to use**: When a comparable sector has gone through a similar cycle and you want to use its PE/PB compression pattern as a reference.

```
Use the [REFERENCE_INDUSTRY] cycle ([YEAR_START]-[YEAR_END]) as a valuation
reference for [TARGET_INDUSTRY]:

1. [REFERENCE_COMPANY] PE/PB compression pattern:
   - Pre-boom: PE [X]x, PB [Y]x
   - Peak earnings: PE [X]x, PB [Y]x
   - Key lesson: Stock went up [X]x while PE crashed from [A]x to [B]x

2. Critical differences between [REFERENCE] and [TARGET]:
   | Factor | [REFERENCE] | [TARGET] | Implication |
   | Supply response | | | |
   | Driver type | | | |
   | Duration | | | |
   | PE floor estimate | | | |

3. Based on this, estimate:
   - PE floor for [TARGET_INDUSTRY]: [X]-[Y]x
   - Will PE compress to [REFERENCE] levels? Why or why not?
   - Timeline for PE compression path (Phase 1→5)
```

---

*These templates are living documents. Update as new analytical patterns emerge.*
*For project-specific prompt history, see the project's own Prompt_Log files.*

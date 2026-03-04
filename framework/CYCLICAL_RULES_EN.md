# Cyclical Stock Analysis Rules

> **Rules specific to cyclical industries: shipping (VLCC, container, dry bulk), metals (steel, copper, tungsten), energy (oil & gas, coal), semiconductors, etc.**
> These extend the universal rules in `UNIVERSAL_RULES_EN.md`. Apply both together.
> Last updated: March 4, 2026.

---

## 🔴 CYCLE-SPECIFIC MANDATORY RULES

### CRule 1: Two-Cycle Backtrack with Price-Rate Correlation

**For every cyclical stock analysis, you MUST:**

1. **Identify the two most recent complete cycles** for the commodity/rate that drives the company's earnings (e.g., VLCC TD3C rate, tungsten APT price, DRAM spot price, container freight index).

2. **Backtrack stock price vs underlying rate/price** over both cycles:
   - Plot or tabulate: commodity rate on one axis, stock price on the other, over time.
   - Calculate correlation coefficient (R²) between rate and stock price at weekly/monthly frequency.
   - Note the **lead/lag relationship**: Does the stock move before or after the rate? By how many weeks/months?
   - Identify divergence points: When did stock price decouple from the rate, and why? (e.g., market sentiment, leverage, hedging)

3. **Cycle anatomy for each of the two cycles:**

   | Phase | Rate Behavior | Stock Behavior | PE Behavior | Duration |
   |---|---|---|---|---|
   | Trough | Below breakeven | Depressed, high PE or negative earnings | High or N/A | |
   | Early upturn | Rising past breakeven | Stock leads rate by 1-3 months | PE declining rapidly | |
   | Mid-cycle | Sustained above average | Stock accelerating, sell-side upgrading | PE compressing | |
   | Peak | Historic highs | Stock may plateau or lag rate | PE at cycle lows | |
   | Downturn | Rate declining | Stock leads decline by 1-3 months | PE expanding (earnings falling) | |

4. **Compare the two cycles:**
   - What drove each? (Demand shock, supply constraint, geopolitical, structural)
   - How long did each last? (Trough-to-peak, peak-to-trough)
   - Peak rate vs peak stock price — what multiple did the market assign?
   - What was the max drawdown from peak? How fast?

5. **Based on historical patterns, determine where we are NOW:**
   - Which phase of the current cycle? (Trough / Early upturn / Mid-cycle / Peak / Downturn)
   - How does the current rate compare to the two historical peaks?
   - Is the stock leading or lagging the rate relative to historical patterns?
   - What does the lead/lag pattern predict for the next 3-6-12 months?

6. **Output a cycle positioning summary:**

   ```
   Current cycle position: [Phase] (e.g., "Mid-cycle, approaching peak")
   Evidence: [Rate at X vs historical peak Y, stock at Z vs historical peak W]
   Historical analog: Most similar to [Cycle N, Phase M]
   Predicted next move: [Rate likely to X, stock likely to Y]
   Time to peak (est.): [N months based on historical duration]
   Key risk: [What ended the comparable cycle]
   ```

> **This rule exists because cyclical stocks are NOT valued on current earnings — they are valued on where we are in the cycle.** Getting the cycle position wrong is the #1 cause of losses in cyclical investing.

---

### CRule 2: Cycle-Peak PE/PB Compression Pattern

For every cyclical stock:
- Document the PE/PB at cycle troughs (typically high PE or negative earnings).
- Document the PE/PB at cycle peaks (typically lowest PE despite highest earnings).
- Estimate the PE floor for the current cycle with reasoning.
- Show the full PE compression timeline (Phase 1→5).

**Reference template** (adapt per industry):

```
Phase 1 (Trough):     PE [HIGH]x — Low earnings, market prices recovery hope
Phase 2 (Early):      PE [MID]x  — Earnings rising, sell-side skeptical
Phase 3 (Mid-cycle):  PE [LOW]x  — Earnings strong, market debates sustainability
Phase 4 (Late cycle): PE [LOWER]x — Peak earnings, market prices decline
Phase 5 (Downturn):   PE [HIGH]x — Earnings collapsing, stock falling
```

### CRule 3: Supply-Demand Cycle Duration Analysis

Cyclical industries have predictable supply response timelines. Always include:

| Industry | Order-to-Delivery Lead Time | Current Order Book | Implication |
|---|---|---|---|
| VLCC | 3-4 years | Near-zero until 2028 | Extended cycle |
| Container ships | 2-3 years | Heavy post-2021 orders | Shorter cycle |
| Semiconductors (fab) | 2-3 years | Varies by node | |
| Metals (mine) | 5-10 years | | Very extended cycles |
| Real estate | 1-3 years | | |

- Longer lead times = longer cycles = more time for stock appreciation.
- Heavy order books = earlier cycle turns = shorter window for profits.
- **Always check: How many [ASSETS] are on order? When do they deliver? Is this enough to break the cycle?**

### CRule 4: Operating Leverage Multiplier Table

Cyclical businesses have high fixed costs. Always show:

| Rate/Price Level | vs Breakeven | Revenue | Profit | Margin | Stock Implication |
|---|---|---|---|---|---|
| Below breakeven | <1.0x | X | Negative | N/A | Trough valuation |
| At breakeven | 1.0x | Y | ~$0 | ~0% | Inflection point |
| 1.5x breakeven | 1.5x | Z | Moderate | 20-30% | Early re-rate |
| 2.0x breakeven | 2.0x | | High | 40-50% | Mid-cycle |
| 3.0x breakeven | 3.0x | | Very high | 60%+ | Near peak |

This demonstrates that a 2x rate increase can produce a 5-10x profit increase — the core reason cyclical stocks are so volatile.

### CRule 5: Contrarian Timing Indicators

Cyclical investing requires buying when fundamentals look terrible and selling when they look amazing. Track these:

**Buy signals (accumulate):**
- PE is very high or negative (trough earnings)
- Industry capex is at multi-year lows (future supply constraint)
- Sell-side has few "buy" ratings (<30%)
- Companies are scrapping/retiring [ASSETS]
- Spot rates/prices below cash breakeven

**Sell signals (reduce):**
- PE is at historic lows (peak earnings — this is the trap!)
- Industry capex surging, order books filling
- Sell-side has majority "buy" ratings (>70%)
- Companies launching aggressive expansion
- Spot rates/prices at 3x+ breakeven
- Media headlines about "super cycle" (contrarian signal)

### CRule 6: Cross-Cycle Comparable Reference

Always find a reference cycle from a comparable industry. Examples:

| Current Analysis | Reference Cycle | Why Comparable |
|---|---|---|
| VLCC 2026 | Container 2020-22 (中远海控) | Same sector, PE compression pattern |
| VLCC 2026 | VLCC 2008, 2020 | Same asset, different cycle drivers |
| Copper 2024 | Copper 2006-08 | Supply-driven super cycle |
| Semiconductors 2025 | DRAM 2017-18, 2021 | Capacity-driven cycle |
| Steel 2024 | Steel 2016-18 (China supply reform) | Policy-driven cycle |

For each reference:
- What was the peak PE/PB/EV multiple?
- How long from first rate breakout to stock peak?
- What caused the cycle to end?
- What was the max drawdown from peak?

### CRule 7: Earnings Sensitivity Matrix (Multi-Rate)

Always present earnings across at least 5 rate/price scenarios:

| Rate/Price | vs Consensus | Net Income | EPS | PE at Current Price | Upside to Target |
|---|---|---|---|---|---|
| Bear (below consensus) | | | | | |
| Consensus | | | | | |
| Current spot | | | | | |
| Bull | | | | | |
| Super-bull | | | | | |

**Critical**: Highlight the gap between consensus and current spot. In cyclical stocks, this gap is often where the alpha lives — sell-side is slow to upgrade.

### CRule 8: Exit Strategy Framework

Cyclical investments need explicit exit criteria (not just buy targets):

| Exit Trigger | Action | Rationale |
|---|---|---|
| Rate falls below [X] for >2 weeks | Reduce 30% | Cycle may be turning |
| New [ASSET] orders surge past [threshold] | Begin trimming | Supply response = future rate decline |
| PE drops below [Y]x at peak earnings | Take profits on 50% | Market pricing terminal decline |
| Geopolitical/structural catalyst reverses | Full exit | Bull thesis invalidated |
| Stock decouples from rate (stock down, rate flat) | Investigate — may be early exit signal | Market may see something rate doesn't show |

### CRule 9: Inflation-Adjusted Historical Comparison

All historical cycle peak data must be inflation-adjusted to current dollars:
- Use CPI adjustments for all historical market caps, rates, and prices.
- This prevents underestimating historical peaks (e.g., 2008 rates in 2026 dollars are ~40% higher than nominal).
- Show both nominal and real (inflation-adjusted) figures.

### CRule 10: Shadow/Grey Market Monitoring

Many cyclical industries have unofficial supply that affects pricing:
- **Shipping**: Shadow fleet (old tankers operating under sanctions evasion)
- **Metals**: Chinese unofficial smelters, stockpile releases
- **Energy**: Sanctioned oil production (Iran, Venezuela, Russia)
- **Semiconductors**: Grey-market chips, inventory hoarding

Always assess:
- How large is the shadow/unofficial supply? (% of total market)
- Is it growing or shrinking?
- What regulatory/geopolitical changes could bring it into or out of the market?
- Impact on pricing if shadow supply exits (+) or returns (-)

---

## 📋 CYCLICAL STOCK CHECKLIST (In Addition to Universal Checklist)

```
[ ] Two most recent cycles identified and documented
[ ] Stock price vs rate/price correlation analyzed (R², lead/lag)
[ ] Current cycle phase determined with evidence
[ ] PE/PB compression path documented (Phase 1→5)
[ ] Supply-demand duration analysis included (order book, lead times)
[ ] Operating leverage multiplier table included
[ ] Earnings sensitivity matrix (5+ rate scenarios)
[ ] Cross-cycle reference identified (comparable industry)
[ ] Exit strategy with explicit triggers defined
[ ] Historical data inflation-adjusted
[ ] Shadow/grey market supply assessed
[ ] Contrarian indicators checked (are we buying fear or selling greed?)
```

---

## 📊 EXAMPLES FROM VLCC PROJECT (For Reference)

These rules were derived from our VLCC shipping analysis. Here's how they applied:

**CRule 1 applied**: Two cycles identified — 2008 (super cycle, demand-driven) and 2020 (floating storage pulse). Stock prices led VLCC rates by 1-2 months on both upswings and downswings. Current cycle (2026) most resembles 2008 in structure but with tighter supply constraints.

**CRule 2 applied**: Container cycle (中远海控 2020-22) used as PE compression reference — PE went from 16x to 1x as profits surged 55x. VLCC PE floor estimated at 3-8x (not 1x) due to zero new supply until 2028.

**CRule 4 applied**: VLCC breakeven ~$25K/day, current spot $150K+ = 6x breakeven. At this level, ~75% of revenue is pure profit. A $10K/day rate increase adds RMB 730M net income for a 52-VLCC fleet.

**CRule 7 applied**: 5 scenarios ($100K consensus / $120K conservative / $150K base / $200K bull / $250K super-bull) with full earnings, PE, and target price impact for each.

**CRule 10 applied**: Shadow fleet (old tankers evading sanctions) estimated at 5-8% of effective supply. Currently exiting the market = positive for rates. Monitored as a risk factor if sanctions ease.

---

*This file extends `UNIVERSAL_RULES_EN.md`. Use both together for cyclical stock analysis.*
*For industry-specific data (fleet numbers, rate history), see the project's own RULES.md.*

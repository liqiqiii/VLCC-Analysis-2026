# Copilot Instructions — Equity Research Skill

> **This file is automatically read by GitHub Copilot when working in this repository.**
> It contains all analysis rules organized in a hierarchy: Universal → Cyclical → Project-Specific.
> Copilot: follow ALL applicable rules on EVERY action. No reminders needed.
>
> Last updated: March 4, 2026.

---

## How This File Works

```
┌─────────────────────────────────────────────────┐
│  LAYER 1: UNIVERSAL RULES (always apply)        │
│  Any stock, any industry, any market             │
├─────────────────────────────────────────────────┤
│  LAYER 2: CYCLICAL RULES (auto-detect)          │
│  Shipping, metals, energy, semiconductors, etc.  │
│  ► Apply IF the company's earnings are driven    │
│    by commodity prices, freight rates, or other  │
│    cyclical demand/supply dynamics.              │
├─────────────────────────────────────────────────┤
│  LAYER 3: PROJECT-SPECIFIC RULES                │
│  VLCC fleet data, file maps, this repo only      │
└─────────────────────────────────────────────────┘
```

**Auto-detection logic for Layer 2:**
Before starting analysis, assess the company:
1. Is the company's primary revenue driver a commodity price, freight rate, or cyclical demand?
2. Does the industry have boom/bust cycles with >50% revenue swings?
3. Are earnings highly sensitive to a single external rate/price?

→ If **YES** to any: activate **all Cyclical Rules (CRule 1–10)** in addition to Universal Rules.
→ Examples: tanker shipping, container shipping, dry bulk, steel, copper, tungsten, oil & gas, coal, DRAM/NAND, airlines.

---

# ═══════════════════════════════════════════════════
# LAYER 1: UNIVERSAL RULES
# (Apply to EVERY stock analysis, every action)
# ═══════════════════════════════════════════════════

## 🔴 WORKFLOW (Every Single Time)

### Rule 1: Bilingual Output
Every report change must be applied to **both** the English AND Chinese (or other target language) versions simultaneously. Never update one without the other.
- Check that numbers, tables, and conclusions are **identical** across languages.

### Rule 2: Prompt & Decision Logging
After every conversation turn that introduces new analysis, corrections, or data:
- Update the prompt log with what was asked, what was found, and key decisions.
- Maintain logs in all target languages.
- Include date and key findings for each entry.

### Rule 3: Version Control Discipline
After any file change, stage → commit → push. Don't leave local-only changes.
- Commit messages should summarize what changed and why.
- Use meaningful commit messages, not "update files."
- Include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer.

### Rule 4: Cross-Check All Data
Before publishing any number:
- Verify sensitivity figures with back-of-envelope math.
- Sanity-check: `units × rate × time × margin × tax × FX = result`
- Compare across models — flag when models disagree significantly (>20%).
- If data from different sources conflicts, note the discrepancy explicitly.

---

## 🟡 ANALYTICAL STANDARDS

### Rule 5: Multi-Model Consensus Approach
Run analysis across 3–5 models when doing new research:
- Use identical, self-contained prompts across all models.
- Compile consensus + note disagreements.
- Flag which models used correct vs incorrect assumptions.
- Weight results toward models that correctly interpreted the data.

**Suggested model mix** (as of 2026): Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro.
> *Tip: For models like Gemini that may return empty, add "do NOT use tools" to the prompt.*

### Rule 6: Operating Leverage Analysis
For any high-fixed-cost business (shipping, airlines, semiconductors, SaaS, telecom):
- Calculate breakeven points (revenue level where profit turns positive).
- Show the non-linear profit multiplier at different revenue/rate scenarios.
- Demonstrate that above breakeven, incremental revenue ≈ pure profit.
- This framework applies to ANY business with high fixed costs and variable pricing.

### Rule 7: Target Prices Are Required
Every stock analysis MUST include:
- Conservative / Base / Bull scenarios (minimum 3).
- 12-month and 24-month targets.
- Explicit PE (or relevant multiple) assumptions with reasoning.
- Clear upside/downside percentages vs current price.
- Scenario-specific investment advice (see Rule 11).

### Rule 8: Report Structure
Each company/comparative analysis should include:
1. **Executive Summary / TL;DR** — key metrics, rating, target prices
2. **Company Profile** — business model, segments, key financials
3. **Industry/Market Context** — current conditions, historical comparison
4. **Earnings Model** — per-segment with sensitivity tables
5. **Operating Leverage Analysis** — breakeven, profit multiplier
6. **Cycle/Valuation Framework** — historical PE/PB compression patterns
7. **Multi-Model Consensus** — target prices from all models
8. **Risk Matrix** — with probabilities and impact levels
9. **Investment Recommendation** — scenario-specific targets, allocation, triggers
10. **Day1Global Framework** — Modules C/L/O, 6 Perspectives, Anti-Bias, Pre-Mortem
11. **Cross-Market Peer Comparison** — if applicable

### Rule 9: Fetch Latest Market Data
Before any valuation work:
- Get current stock prices and market caps (they change fast in volatile sectors).
- Get current operating rates / prices for ALL relevant business segments.
- Don't reuse stale data from prior sessions without verifying.

### Rule 10: Full Portfolio / Multi-Segment Modeling
When analyzing a diversified company:
- Model EVERY business segment separately — never use total market cap ÷ primary segment count.
- Account for different margin profiles, growth rates, and cyclicality per segment.
- Use Sum-of-Parts (SOTP) for cross-company comparison when segment mixes differ.

### Rule 11: Whole-File Scenario Consistency
When adding a new scenario or assumption (e.g., different price/rate baseline):
- **Update EVERY section** of the report that references the affected metrics — not just add a standalone section.
- TL;DR must show all scenarios.
- All target price tables must show multi-scenario columns.
- Investment recommendation MUST include scenario-specific advice, targets, and allocation.
- Any section with PE, NI, EPS, or target prices must reflect all modeled scenarios.

> **Rationale**: A standalone "Section 4B" is insufficient if Section 9 still only references the old assumption. The reader of Section 9 (the most important section) must see the full picture without scrolling back.

### Rule 12: Day1Global Framework Application
Every stock analysis report MUST apply the [Day1Global tech-earnings-deepdive](https://github.com/webleon/tech-earnings-deepdive-openclaw-skill) framework:

**Required modules:**
| Module | Name | Focus |
|---|---|---|
| A | Revenue Quality | Revenue drivers, mix, sustainability |
| B | Profitability | Margins, operating leverage, cost structure |
| C | Cash Flow | **"THE BIG ONE"** — FCF, FCF yield, capex discipline |
| D | Forward Guidance | Management outlook, PE compression path |
| E | Competitive Landscape | Peers, moats, market share |
| K | Valuation Matrix | Multi-scenario target prices, EV/EBITDA, P/NAV |
| L | Ownership & Management | Shareholder structure, alignment, related-party risk |
| O | Accounting Quality | D&A policy, impairment risk, off-balance-sheet items |

**Required perspectives (6):**
1. **Quality Compounder** (Buffett/Munger) — durable advantage?
2. **Imaginative Growth** (Baillie Gifford/ARK) — 10x optionality?
3. **Fundamental Long/Short** (Tiger Cubs) — what's mispriced?
4. **Deep Value** (Klarman/Marks) — margin of safety?
5. **Catalyst Driven** (Tepper/Ackman) — specific value-unlocking events?
6. **Macro Tactical** (Druckenmiller) — cycle/macro positioning?

**Required frameworks:**
- **Anti-Bias**: Identify and mitigate anchoring, simplification, recency, confirmation, survivorship, and narrative biases.
- **Pre-Mortem**: "It's 1 year later and you lost 40%. What went wrong?" — 3–5 specific scenarios with probabilities and early warning signs.

---

## 🟢 TECHNICAL / OUTPUT

### Rule 13: Write Files via Python
Use Python scripts (not shell heredocs) to write .md files containing `$` or other shell-interpreted characters. PowerShell double-quoted strings interpret `$` as variables.

### Rule 14: Chart Updates
When underlying data changes, regenerate any affected charts. Don't leave stale visualizations.

---

## 📋 UNIVERSAL CHECKLIST (Before Every Push)

```
[ ] EN report updated
[ ] CN report updated
[ ] GitHub Pages / web files synced
[ ] Prompt log updated (all languages)
[ ] Numbers consistent across languages
[ ] Full portfolio / all segments modeled
[ ] Latest market data used
[ ] All scenarios reflected in ALL sections (Rule 11)
[ ] Day1Global framework applied (Rule 12)
[ ] Git commit + push completed
```

---

# ═══════════════════════════════════════════════════
# LAYER 2: CYCLICAL STOCK RULES
# (Auto-activate for cyclical industries)
# ═══════════════════════════════════════════════════

> **Applies to**: Shipping (VLCC, container, dry bulk), metals (steel, copper, tungsten),
> energy (oil & gas, coal), semiconductors, airlines, real estate, etc.
>
> **Detection**: If the company's earnings are primarily driven by a commodity price,
> freight rate, or other cyclical demand/supply dynamic → these rules are ACTIVE.

---

### CRule 1: Two-Cycle Backtrack with Price-Rate Correlation ⭐

**For every cyclical stock analysis, you MUST:**

1. **Identify the two most recent complete cycles** for the commodity/rate that drives the company's earnings (e.g., VLCC TD3C rate, tungsten APT price, DRAM spot price, container freight index).

2. **Backtrack stock price vs underlying rate/price** over both cycles:
   - Plot or tabulate: commodity rate on one axis, stock price on the other, over time.
   - Calculate correlation coefficient (R²) between rate and stock price at weekly/monthly frequency.
   - Note the **lead/lag relationship**: Does the stock move before or after the rate? By how many weeks/months?
   - Identify divergence points: When did stock price decouple from the rate, and why?

3. **Cycle anatomy for each of the two cycles:**

   | Phase | Rate Behavior | Stock Behavior | PE Behavior | Duration |
   |---|---|---|---|---|
   | Trough | Below breakeven | Depressed, high PE or negative earnings | High or N/A | |
   | Early upturn | Rising past breakeven | Stock leads rate by 1–3 months | PE declining rapidly | |
   | Mid-cycle | Sustained above average | Stock accelerating, sell-side upgrading | PE compressing | |
   | Peak | Historic highs | Stock may plateau or lag rate | PE at cycle lows | |
   | Downturn | Rate declining | Stock leads decline by 1–3 months | PE expanding (earnings falling) | |

4. **Compare the two cycles:**
   - What drove each? (Demand shock, supply constraint, geopolitical, structural)
   - How long did each last? (Trough-to-peak, peak-to-trough)
   - Peak rate vs peak stock price — what multiple did the market assign?
   - What was the max drawdown from peak? How fast?

5. **Based on historical patterns, determine where we are NOW:**
   - Which phase of the current cycle? (Trough / Early upturn / Mid-cycle / Peak / Downturn)
   - How does the current rate compare to the two historical peaks?
   - Is the stock leading or lagging the rate relative to historical patterns?
   - What does the lead/lag pattern predict for the next 3–6–12 months?

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

**Reference template:**
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
| VLCC | 3–4 years | Near-zero until 2028 | Extended cycle |
| Container ships | 2–3 years | Heavy post-2021 orders | Shorter cycle |
| Semiconductors (fab) | 2–3 years | Varies by node | |
| Metals (mine) | 5–10 years | | Very extended cycles |
| Real estate | 1–3 years | | |

- Longer lead times = longer cycles = more time for stock appreciation.
- Heavy order books = earlier cycle turns = shorter window for profits.
- **Always check: How many [ASSETS] are on order? When do they deliver? Is this enough to break the cycle?**

### CRule 4: Operating Leverage Multiplier Table

Cyclical businesses have high fixed costs. Always show:

| Rate/Price Level | vs Breakeven | Revenue | Profit | Margin | Stock Implication |
|---|---|---|---|---|---|
| Below breakeven | <1.0x | X | Negative | N/A | Trough valuation |
| At breakeven | 1.0x | Y | ~$0 | ~0% | Inflection point |
| 1.5x breakeven | 1.5x | Z | Moderate | 20–30% | Early re-rate |
| 2.0x breakeven | 2.0x | | High | 40–50% | Mid-cycle |
| 3.0x breakeven | 3.0x | | Very high | 60%+ | Near peak |

This demonstrates that a 2x rate increase can produce a 5–10x profit increase — the core reason cyclical stocks are so volatile.

### CRule 5: Contrarian Timing Indicators

Cyclical investing requires buying when fundamentals look terrible and selling when they look amazing.

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

Always find a reference cycle from a comparable industry:

| Current Analysis | Reference Cycle | Why Comparable |
|---|---|---|
| VLCC 2026 | Container 2020–22 (中远海控) | Same sector, PE compression pattern |
| VLCC 2026 | VLCC 2008, 2020 | Same asset, different cycle drivers |
| Copper 2024 | Copper 2006–08 | Supply-driven super cycle |
| Semiconductors 2025 | DRAM 2017–18, 2021 | Capacity-driven cycle |
| Steel 2024 | Steel 2016–18 (China supply reform) | Policy-driven cycle |

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
- Impact on pricing if shadow supply exits (+) or returns (−)

---

## 📋 CYCLICAL CHECKLIST (In Addition to Universal)

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
[ ] Contrarian indicators checked (buying fear or selling greed?)
```

---

# ═══════════════════════════════════════════════════
# LAYER 3: PROJECT-SPECIFIC RULES
# (This repository: VLCC / Tanker Shipping Analysis)
# ═══════════════════════════════════════════════════

### P-Rule 1: Fleet Data (Current as of March 2026)

| Company | VLCCs | Other Vessels | Total Fleet | Notes |
|---|---|---|---|---|
| **DHT Holdings** | 24 | 0 | 24 | Pure VLCC play |
| **Frontline (FRO)** | 42 VLCC | 21 Suezmax + 18 LR2 | 81 | Mixed fleet; VLCC equiv = 42 + 21×0.5 + 18×0.3 = 57.9 |
| **CMES (招商轮船)** | 52 VLCC | 93 dry bulk + 40–60 LNG + 19 container + Ro-Ro | ~280 | Highly diversified |
| **COSCO Energy (中远海能)** | 55 VLCC | 18 Suezmax + 50 Aframax/LR2 + 30 MR/LR1 + 65 LNG | ~185 | Tanker + LNG portfolio |

**VLCC Equivalence Formula** (for mixed fleets):
`VLCC_equiv = VLCC×1.0 + Suezmax×0.5 + Aframax×0.3`

### P-Rule 2: Cycle Context for This Analysis

| Cycle | Year | Driver | Character |
|---|---|---|---|
| Super cycle | 2008 | Demand + high valuation | Peak earnings + peak multiples |
| Floating storage pulse | 2020 | COVID contango, short-lived | High rates, low multiples |
| Container reference | 2020–22 | 中远海控 PE compression 16x→1x | Same-sector PE pattern reference |
| **Current** | **2026–28** | **Supply-driven (zero new VLCC until late 2028, shadow fleet exit, Sinokor hoarding)** | **Extended strong cycle** |

### P-Rule 3: Rate Scenarios for VLCC

| Scenario | Avg Rate ($/day) | Context |
|---|---|---|
| Bear / Consensus | $100,000 | Sell-side base case |
| Conservative | $120,000 | Moderate bull |
| **Base** | **$150,000** | Current spot-implied |
| Bull | $200,000 | Inflation-adjusted near-2008 levels |
| Super-bull | $250,000 | New nominal high |

### P-Rule 4: File Map

| File | Purpose | Update When |
|---|---|---|
| `05_Deep_Dive_Day1Global_Framework.md` | DHT vs FRO (EN) | Any DHT/FRO change |
| `06_Deep_Dive_Day1Global_Framework_CN.md` | DHT vs FRO (CN) | Mirror of 05 |
| `07_CN_AShare_VLCC_Report_EN.md` | CMES vs COSCO (EN) | Any A-share change |
| `08_CN_AShare_VLCC_Report_CN.md` | CMES vs COSCO (CN) | Mirror of 07 |
| `index.md` | GitHub Pages hub | When adding new pages |
| `dht-fro.md` | GH Pages: DHT/FRO | Copy of 06 |
| `cn-ashare.md` | GH Pages: A-share | Copy of 08 |
| `Prompt_Log_EN.md` | Prompt tracking (EN) | **Every conversation** |
| `Prompt_Log_CN.md` | Prompt tracking (CN) | **Every conversation** |
| `charts/` | Matplotlib charts | When underlying data changes |

### P-Rule 5: GitHub Pages Structure

- Hub: `/` → `index.md`
- DHT/FRO report: `/dht-fro` → `dht-fro.md`
- A-share report: `/cn-ashare` → `cn-ashare.md`
- Repo: `https://github.com/liqiqiii/VLCC-Analysis-2026`
- Pages: `https://liqiqiii.github.io/VLCC-Analysis-2026/`

---

## 📋 PROJECT CHECKLIST (Full — Combines All Layers)

```
═══ UNIVERSAL ═══
[ ] EN report updated
[ ] CN report updated
[ ] GitHub Pages / web files synced
[ ] Prompt log updated (all languages)
[ ] Numbers consistent across languages
[ ] Full portfolio / all segments modeled
[ ] Latest market data used
[ ] All scenarios reflected in ALL sections (Rule 11)
[ ] Day1Global framework applied (Rule 12)
[ ] Git commit + push completed

═══ CYCLICAL ═══
[ ] Two most recent cycles identified and documented
[ ] Stock vs rate correlation analyzed (R², lead/lag)
[ ] Current cycle phase determined with evidence
[ ] PE/PB compression path documented
[ ] Supply-demand duration analysis included
[ ] Operating leverage multiplier table
[ ] Earnings sensitivity matrix (5+ scenarios)
[ ] Cross-cycle reference identified
[ ] Exit strategy with explicit triggers
[ ] Historical data inflation-adjusted
[ ] Shadow/grey market supply assessed

═══ PROJECT ═══
[ ] Fleet numbers match P-Rule 1
[ ] Rate scenarios match P-Rule 3
[ ] All files in P-Rule 4 updated
[ ] GitHub Pages synced (P-Rule 5)
```

---

# ═══════════════════════════════════════════════════
# APPENDIX: REUSABLE PROMPT TEMPLATES
# ═══════════════════════════════════════════════════

> Use these templates when running multi-model analysis. Replace `[PLACEHOLDER]` values.

### Template 1: Cyclical Stock Valuation

```
You are an equity research analyst specializing in cyclical industries.
Analyze [COMPANY_NAME] ([TICKER]) listed on [EXCHANGE].

Fleet/Capacity: [DETAILS]
Current [RATE/PRICE]: [VALUE]
Historical cycles: [CYCLE_1_YEAR] ([DRIVER]), [CYCLE_2_YEAR] ([DRIVER])

Tasks:
1. Calculate 2026 net income under [SCENARIO_COUNT] rate scenarios: [LIST_RATES]
2. Apply PE compression framework (trough PE → peak PE path)
3. Set 12-month and 24-month target prices (conservative/base/bull)
4. Compare to historical cycle-peak valuations (inflation-adjusted to 2026 USD)
5. Identify current cycle phase using CRule 1 two-cycle backtrack

Output: Structured markdown with tables. Show all math.
Do NOT use any external tools. Use only the data provided.
```

### Template 2: Head-to-Head Comparison

```
Compare [COMPANY_A] vs [COMPANY_B] for a [INDUSTRY] cycle investment:

Company A: [FLEET/CAPACITY_A], market cap [MCAP_A], current price [PRICE_A]
Company B: [FLEET/CAPACITY_B], market cap [MCAP_B], current price [PRICE_B]

Analyze:
1. Rate sensitivity: Who benefits more from a $[X] rate increase?
2. Operating leverage: Breakeven points, profit at [RATE_SCENARIOS]
3. Charter/hedge strategy: Spot vs time-charter vs FFA exposure
4. Valuation gap: Per-[ASSET] market cap, PE, P/NAV
5. Risk profile: Fleet age, leverage, dividend policy, hedging
6. Verdict: Who has more upside? Who has more certainty?

Output: Structured markdown with comparison tables.
Do NOT use any external tools.
```

### Template 3: Cross-Market Peer Valuation

```
Compare [MARKET_A]-listed [COMPANIES_A] with [MARKET_B]-listed [COMPANIES_B].
All operate in [INDUSTRY].

Key data: [FLEET/CAPACITY per company]
Current rates: [RATES]
FX rate: [FX]

Tasks:
1. Normalize to common currency ([USD/RMB])
2. Calculate per-[ASSET] market cap for each company
3. Identify valuation discount/premium across markets
4. Model earnings under [RATE_SCENARIOS] — full portfolio, all segments
5. Apply Day1Global framework (Modules C, L, O minimum)
6. Investment recommendation with scenario-specific targets

Output: Structured markdown. Show all math. Do NOT use external tools.
```

### Template 4: Day1Global Deep Dive

```
Apply the Day1Global tech-earnings-deepdive framework to [COMPANY] ([TICKER]):

Latest financials: [KEY_METRICS]
Industry context: [CONTEXT]

Required:
1. Module C (Cash Flow): FCF, FCF yield, capex discipline, shareholder returns
2. Module L (Ownership): Major shareholders, management alignment, related-party risk
3. Module O (Accounting Quality): D&A policy, impairment risk, off-balance-sheet items
4. Six perspectives: Buffett, Baillie Gifford, Tiger Cubs, Klarman, Tepper, Druckenmiller
5. Anti-Bias: Check for anchoring, simplification, recency, confirmation, survivorship, narrative
6. Pre-Mortem: "1 year later, lost 40% — what went wrong?" 3-5 scenarios with probabilities

Grade each module (A/B/C/D/F) with justification.
Output: Structured markdown. Do NOT use external tools.
```

### Template 5: Cycle Position Assessment

```
Determine where [COMPANY/INDUSTRY] is in the current cycle:

Two most recent cycles:
- Cycle 1: [YEAR_RANGE], driven by [DRIVER], [RATE] went from [LOW] to [HIGH]
- Cycle 2: [YEAR_RANGE], driven by [DRIVER], [RATE] went from [LOW] to [HIGH]

Current data:
- Current [RATE]: [VALUE] (as of [DATE])
- Current stock price: [PRICE]
- Current PE: [PE]
- Order book / new supply: [DETAILS]

Tasks:
1. Map both historical cycles using the 5-phase anatomy (trough→downturn)
2. Calculate R² correlation between rate and stock price for each cycle
3. Identify lead/lag pattern
4. Determine current phase with evidence
5. Predict next 3-6-12 month trajectory based on historical pattern
6. Output cycle positioning summary (CRule 1 format)

Do NOT use external tools.
```

---

*End of Copilot Instructions. This file combines Universal Rules (14), Cyclical Rules (10), Project Rules (5), and 5 Prompt Templates into a single auto-loaded skill.*

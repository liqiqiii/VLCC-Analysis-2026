# Universal Stock Analysis Rules

> **Industry-agnostic rules for AI-assisted equity research.**
> Extracted from 19+ iterative prompts across VLCC shipping analysis.
> Apply these to ANY sector — then add industry-specific rules on top.
> Last updated: March 4, 2026.

---

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

### Rule 4: Cross-Check All Data
Before publishing any number:
- Verify sensitivity figures with back-of-envelope math.
- Sanity-check: `units × rate × time × margin × tax × FX = result`
- Compare across models — flag when models disagree significantly (>20%).
- If data from different sources conflicts, note the discrepancy explicitly.

---

## 🟡 ANALYTICAL STANDARDS

### Rule 5: Multi-Model Consensus Approach
Run analysis across 3-5 models when doing new research:
- Use identical, self-contained prompts across all models.
- Compile consensus + note disagreements.
- Flag which models used correct vs incorrect assumptions.
- Weight results toward models that correctly interpreted the data.

**Suggested model mix** (as of 2026): Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro.
> *Tip: For models like Gemini that may return empty, add "do NOT use tools" to the prompt.*

### Rule 6: Operating Leverage / SaaS Economics
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

> **Rationale**: A standalone "Section 4B" is insufficient if Section 9 still only references the old assumption.

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
- **Pre-Mortem**: "It's 1 year later and you lost 40%. What went wrong?" — 3-5 specific scenarios with probabilities and early warning signs.

---

## 🟢 TECHNICAL / OUTPUT

### Rule 13: Write Files via Python
Use Python scripts (not shell heredocs) to write .md files containing `$` or other shell-interpreted characters.

### Rule 14: Chart Updates
When underlying data changes, regenerate any affected charts. Don't leave stale visualizations.

---

## 📋 UNIVERSAL CHECKLIST (Copy-Paste Before Every Push)

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

*This is a universal framework. For project-specific rules (fleet data, cycle history, file maps), see the project's own RULES.md.*

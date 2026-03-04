# VLCC Analysis Project — Standing Rules

> **These rules are distilled from 16+ prompts across this project.**
> Follow ALL of them on EVERY action. No reminders needed.
> Last updated: March 4, 2026.

---

## 🔴 MANDATORY (Every Single Time)

### Rule 1: Always Update BOTH Languages
Every report change must be applied to **both** the English AND Chinese versions simultaneously. Never update one without the other.
- EN report → CN report → cn-ashare.md (GitHub Pages) / dht-fro.md (if DHT/FRO)
- Check that numbers, tables, and conclusions are **identical** across languages.

### Rule 2: Always Update Prompt Logs
After every conversation turn that introduces new analysis, corrections, or data:
- Update `Prompt_Log_EN.md` with the new prompt
- Update `Prompt_Log_CN.md` with the Chinese translation
- Include date, what was asked, and key findings

### Rule 3: Always Push to GitHub
After any file change, stage → commit → push. Don't leave local-only changes.
- Commit message should summarize what changed and why
- Include `Co-authored-by: Copilot` trailer

### Rule 4: Always Use Full Portfolio
Both A-share companies are **diversified fleets**, not pure VLCC plays:
- **CMES**: 52 VLCC + 93 dry bulk + 40-60 LNG + 19 container + Ro-Ro (~280 total)
- **COSCO Energy**: 55 VLCC + 18 Suezmax + 50 Aframax/LR2 + 30 MR/LR1 + 65 LNG (~185 total)
- **FRO**: 42 VLCC + 21 Suezmax + 18 LR2 (81 total)
- **DHT**: 24 VLCC (pure play)

When calculating earnings, valuations, or comparisons: **model every segment separately**. Never divide total market cap by VLCC count alone.

### Rule 5: Cross-Check All Data
Before publishing any number:
- Verify sensitivity figures (e.g., RMB 730M per **$10K**/day, NOT per $1K)
- Sanity-check with back-of-envelope: ships × rate × days × tax × FX
- Compare across models — flag when models disagree significantly
- If data from different sources conflicts, note the discrepancy explicitly

---

## 🟡 ANALYTICAL STANDARDS

### Rule 6: Multi-Model Approach
Run analysis across 5 models when doing new research:
- Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro
- Use identical prompts (self-contained, "do NOT use tools")
- Compile consensus + note disagreements
- Flag which models used correct vs incorrect assumptions

### Rule 7: Operating Leverage / SaaS Economics
Always include the operating leverage analysis:
- Shipping has fixed costs (crew, D&A, finance) — above breakeven, incremental revenue ≈ pure profit
- Calculate breakeven points per vessel type
- Show the non-linear profit multiplier at different rate scenarios
- This applies to ALL tanker types, not just VLCCs

### Rule 8: Target Prices Are Required
Every stock analysis MUST include:
- Conservative / Base / Bull scenarios
- 12-month and 24-month targets
- Explicit PE assumptions with reasoning
- Clear upside/downside percentages vs current price

### Rule 9: Cycle Context
Always position current rates within historical cycle framework:
- 2008: Super cycle (demand + high valuation)
- 2020: Floating storage pulse (high rates, short, low valuation)
- 2020-2022 container (中远海控): PE compression reference
- 2026-2028: Supply-driven strong cycle
- Show PE compression path timeline

### Rule 10: Fetch Latest Market Data
Before any valuation work:
- Get current stock prices and market caps (they change fast)
- Get current spot rates for ALL relevant vessel types
- Don't reuse stale data from prior sessions without verifying

---

## 🟢 OUTPUT FORMAT

### Rule 11: Report Structure
Each company analysis should include:
1. Company snapshot (price, mcap, fleet, key metrics)
2. Fleet breakdown by segment (not just headline VLCC count)
3. Earnings model — **per segment** with sensitivity tables
4. Operating leverage analysis
5. Cycle-peak valuation framework
6. Multi-model consensus + target prices
7. Risk matrix
8. Investment recommendation + portfolio allocation
9. Cross-market peer comparison (if applicable)

### Rule 12: Write Files via Python
Use Python scripts (not PowerShell heredocs) to write .md files containing `$` signs. PowerShell double-quoted strings interpret `$` as variables.

### Rule 13: Chart Updates
When data changes, regenerate any affected charts. Don't leave stale visualizations.

### Rule 14: Whole-File Scenario Consistency
When adding a new scenario or assumption (e.g., $150K base vs $100K consensus), **update EVERY section of the report** that references the affected metrics — not just add a standalone section. Specifically:
- TL;DR / executive summary must show all scenarios
- All target price tables must show dual/triple scenario columns
- Investment recommendation (Section 9) MUST include scenario-specific advice, target prices, and allocation
- Cross-market comparisons must show forward PE under all scenarios
- Any section with PE, NI, EPS, or target prices must reflect all modeled scenarios

**Rationale**: A standalone "Section 4B" is insufficient if Section 9 still only references the old assumption. The reader of Section 9 (the most important section) must see the full picture without scrolling back.

---

## 📋 CHECKLIST (Copy-Paste Before Every Push)

```
[ ] EN report updated
[ ] CN report updated
[ ] GitHub Pages files synced (cn-ashare.md / dht-fro.md / index.md)
[ ] Prompt_Log_EN.md updated
[ ] Prompt_Log_CN.md updated
[ ] Numbers consistent across EN/CN
[ ] Full portfolio modeled (not just VLCC)
[ ] Latest market data used
[ ] Git commit + push completed
```

---

## 📂 File Map

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

---

*This file lives in the session workspace and is read at the start of every action.*

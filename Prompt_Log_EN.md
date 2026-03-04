# Prompt Tracking Log — VLCC Analysis Project

> This file tracks every analytical prompt/directive from the user throughout the project.
> Updated after each conversation turn. Last updated: **March 3, 2026**.

---

## Prompt 1: Initial Multi-Model VLCC Cycle-Peak Valuation
**Date**: March 1, 2026

Translate the following Chinese prompt into English and run it across multiple AI models (GPT, Opus 4.6, and other good models), then compile a comparative report:

Rules for VLCC cycle-peak valuation backtest of DHT and FRO:
1. **Data standards**: Use latest real fleet numbers. Frontline is a mixed fleet — convert to VLCC-equivalents (VLCC=1.0, Suezmax=0.5, Aframax=0.3). Account for scale effects. All historical market caps CPI-adjusted to 2026 USD.
2. **Cycle positioning**: 2008 = super cycle; 2020 = floating storage pulse; 2026-2028 = supply-driven strong cycle between 08 and 20. Use mid-to-upper-range per-vessel market cap.
3. **Calculate**: Inflation-adjusted per-VLCC-eq market cap at cycle peaks. Current fleet × VLCC-eq. Conservative/neutral/optimistic target market caps. Upside vs current price. Conclusion: who has more elasticity, who has better risk/reward.
4. **Output**: Concise, model-ready, no contradictions.

---

## Prompt 2: Bullish Thesis Enhancement
**Date**: March 1, 2026

Fix Gemini 3 Pro's empty output. Enhance the analysis with current bullish market conditions:
- VLCC supply is very limited
- Sinokor is holding a large portion of fleet
- No new VLCC supply until late 2028
- Shadow fleet is exiting the market
- Market price will keep going up and break historic highs after inflation adjustment

---

## Prompt 3: Documentation & Translation
**Date**: March 1, 2026

Summarize the conversation into .md files. Create a Chinese version of the .md and translate results into Chinese. Put everything in one folder.

---

## Prompt 4: Market Cap Update
**Date**: March 1, 2026

Market cap has changed significantly since beginning of 2026. Fetch the latest market cap of FRO and DHT and update all files.

---

## Prompt 5: Cross-Language Data Alignment
**Date**: March 1, 2026

Chinese version report has bad data. Compare English vs Chinese version. English looks more accurate but do a self-check. Make sure numbers are aligned across both languages.

---

## Prompt 6: Fundamental Deep-Dive
**Date**: March 2, 2026

Both stocks have incredibly similar 3-month stock price trajectories (bottomed then doubled in 2 months). But the model shows DHT has significantly higher upside than FRO, which doesn't make sense. Do a deep dive on both companies — fetch public reports on both companies and the VLCC industry — and figure out why. Propose potential explanations.

---

## Prompt 7: Day1Global Framework Application
**Date**: March 2, 2026

Search for `tech-earnings-deepdive` skill on GitHub and add its framework to the analysis.

---

## Prompt 8: Operating Leverage ("SaaS Economics") + OPEC Reality Check
**Date**: March 2, 2026

Two new analytical dimensions:

1. **Operating leverage / SaaS economics**: VLCC profit behaves like SaaS — 10% revenue increase can lead to exponentially higher profit because TCO (total cost of ownership) is essentially fixed. Do a back-trace on VLCC, Suezmax, and LR2. Think deeply and adjust the report.

2. **OPEC production reality check**: OPEC announced production increases don't mean actual increases — like Fed liquidity, there are monthly adjustments and compensatory cuts that offset announcements. The "frontloading" of announced vs actual production. Do a thorough check on actual production, compare to 2008/2020 big cycles, and find the real OPEC output numbers.

---

## Prompt 9: Target Price Section
**Date**: March 2, 2026

The report is missing the most important part: **target prices**. Use the current report as reference, run across different models, and add a target price section with guidance.

---

## Prompt 10: GitHub Deployment
**Date**: March 2, 2026

Push the whole repo to GitHub (`liqiqiii`). Create a GitHub Page for the Chinese deep-dive report (`06_Deep_Dive_Day1Global_Framework_CN.md`).

---

## Prompt 11: Session History Summary
**Date**: March 2, 2026

Go through the chat history in this project. Summarize exactly what I proposed for the report, list them out. Then translate the summary into Chinese.

---

## Prompt 12: Charter Strategy Analysis
**Date**: March 2-3, 2026

Analyze the charter structure differences between DHT and FRO — spot/TC/FFA strategy differences. Generate charts comparing sensitivity, elasticity, and stability of both companies to VLCC rate changes. Run across multiple models. Summarize conclusions and add to existing report framework.

---

## Prompt 13: Charter Data Cross-Check
**Date**: March 3, 2026

Data discrepancy: Other sources show booking rates as DHT 66/34 and FRO 92/8 (locked = TC + spot long-term bookings + FFA). Cross-check this data against the charter type split used in the model.

**Findings**: Two different metrics were being confused — booking rate (% of Q1 days contracted) vs charter type (structural spot/TC split). Also discovered DHT is shifting from 54% spot to 75% spot by Q2 2026. Update all reports with corrected data.

---

## Prompt 14: Prompt Tracking
**Date**: March 3, 2026

Keep a .md file tracking all prompts used throughout the project. Maintain both English and Chinese versions. Push to GitHub and update after every conversation.

---

## Prompt 15: Chinese A-Share VLCC Analysis (招商轮船 vs 中远海能)
**Date**: March 4, 2026

Using the same prompt framework, same report structure, and same skills (Day1Global, multi-model, operating leverage, target prices), run the same analysis for 招商轮船 (CMES, 601872.SH) and 中远海能 (COSCO Energy, 600026.SH). Create a separate report since these are from a different stock market (A-share). Additionally:
- Take the 中远海控 (COSCO Holdings, 601919.SH) container cycle (2020-2022) into consideration, focusing on PE/PB ratio compression at cycle peaks as a reference
- Predict the annual income for 2026 for both VLCC companies
- Run across 5 models (Opus 4.6, Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro) and summarize

**Key findings**:
- Both rated STRONG BUY by all 5 models
- CMES: 12M base target RMB 25 (+41%), dividend safety (40% payout)
- COSCO Energy: 12M base target RMB 32 (+35%), LNG defensive floor
- Critical sensitivity correction: RMB 730M per $10K/day (not $1K/day)
- A-share VLCC stocks trade at 2.5-3x premium per VLCC vs US-listed peers (DHT/FRO)

---

*This file will be updated as new prompts are added. Last updated: March 4, 2026.*

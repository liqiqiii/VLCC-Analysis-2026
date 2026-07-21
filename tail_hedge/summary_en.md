---
layout: default
title: Tail-Hedge Cheat-Sheet — Cross-Asset Decision Table (S&P · Sectors · Quality Names · VLCC)
---

# Tail-Hedging Cheat-Sheet
## When (and what) to hedge — one table across 7 assets
### July 20, 2026 — Cover / hub for the `tail_hedge/` study

> The whole `tail_hedge/` study reduces to one decision: **compare the VRP you *pay* to the asset's *break-even* VRP.** This page is the scannable summary; the [S&P](report_en), [VLCC](report_vlcc_en) and [Sectors + quality names](report_sectors_en) reports have the full work. *Education/analysis, not investment advice.*

---

## The master table

| Asset | Ann. vol | maxDD | Long-run CAGR | **Hold?** | **Break-even VRP** | **Live paid VRP** | **Hedge verdict** |
|---|---|---|---|---|---|---|---|
| **S&P 500** | 17% | −57% | **+8.4%** | ✅ best (diversified) | ≈ 0% | — (index, cheapest) | ❌ **Hold / diversify** |
| **XLF** Financials | 29% | −83% | +5.7% | ✅ | ≈ 0% | LEAPS puts thin | ❌ **Hold** |
| **JPM** (quality) | 38% | −74% | **+10.3%** | ✅✅ | ≈ 0% | **≈ 107%** | ❌❌ **Hold** (puts far too dear) |
| **AXP** (quality) | 36% | −84% | **+10.9%** | ✅✅ | ≈ 0% | **≈ 99%** | ❌❌ **Hold** (puts far too dear) |
| **XLK** Technology | 26% | −82% | +9.2% | ✅ | **≈ 27%** | **≈ 24%** | 🟡 **Tactical** — hedge only when crash risk is elevated (AI-bubble) |
| **DHT** VLCC | 48% | −97% | **−6.2%** | ❌ cyclical | **≈ 67%** | **≈ 33%** | 🟡 **Only near a cycle TOP** (CRule 1/5) |
| **FRO** VLCC | 61% | −98% | −4.7% | ❌ cyclical | ≈ 0% | ≈ 26–31% | ❌ **Trim / FFA, not puts** |

*Break-even VRP = the max option over-pricing (IV/realized − 1) at which hedging still raises CAGR. Paid VRP = live option IV / trailing realized − 1 (Jul 2026 snapshot). All break-even numbers are **crash-regime-dependent** — the positive ones (XLK 27%, DHT 67%) come almost entirely from the 2000/2008 (XLK) and 2008–12 (DHT) crashes and fall to ~0% in calmer sub-windows.*

---

## The one decision rule

> **Hedge only if BOTH hold:**
> 1. **`paid VRP < the asset's CAGR break-even VRP`** (with a margin for frictions), AND
> 2. you have a **regime reason** — a *holdable* asset in an elevated-crash-risk regime (Tech / AI-bubble), or a *cyclical near its top* (VLCC).
>
> For **5 of the 7** assets both fail → **HOLD, don't hedge.** Only **XLK (tactically)** and **top-of-cycle DHT** clear the bar today (XLK paid 24% < 27%; DHT paid 33% < 67% *if* you believe a big downturn is ahead).

---

## Why: "deep AND frequent *relative to drift*"

> **What is "drift μ"?** Drift is an asset's **deterministic upward trend over time** — the directional part of the return once you strip out the random wobble. In the standard model `dS/S = μ·dt + σ·dW`, **μ is the drift** (the trend) and **σ is the volatility** (the noise). Picture someone walking randomly *on an escalator*: their side-to-side sway is σ, but the escalator's speed (μ) decides where they end up. Practically, **the "Long-run CAGR" column above *is* the realized drift** (`CAGR ≈ μ − ½σ²`): JPM/AXP/S&P have strong positive drift (a fast up-escalator you should just ride); DHT/FRO have **negative** drift (a down-escalator — holding only loses, so you must time it).

Tail-hedging is a race between **premium bled while waiting** (grows with the asset's **drift** and its **vol × VRP**) and **payoff harvested in crashes** (grows with crash **depth × frequency**). The hedge only pays when the harvest beats the bleed:

- **High drift raises the bar twice** — it is the CAGR you must beat, *and* it pushes the underlying up and away from the strike so rolled puts expire worthless more often. That is why **quality compounders (JPM/AXP, +10%) and the S&P are the *worst* hedge candidates** despite deep 2008 tails.
- **The same crash frequency is "enough" for a no-drift asset (VLCC) but "not enough" for a high-drift one (JPM).** VLCC's break-even is 67% because there is *no drift to bleed against*; but that also means there is no reason to *hold* it — so hedging it is pure **cycle timing.**
- **Only Technology clears the bar as a hold-and-hedge asset** — recurring deep crashes (2000, 2008, 2022) make the harvest frequent enough relative to its drift — and even that is regime-conditional (0% post-2010).

**Net:** convex tail-hedging is **not a portfolio pillar**; it is a **conditional, regime-timed tool.** For everything you'd actually want to *hold*, the drift is your friend and the cheapest "hedge" is **diversification + time**. Options tail-hedging earns its keep in only two places: **Tech when you expect a drawdown**, and **a cyclical (VLCC) near its top** — and if you must hedge a single quality name, **hedge the index, not the name** (single-name VRP ~100% vs index ~24%).

---

## The full study
- **[S&P — 50-year backtest](report_en)** — the theory, passive-vs-ladder, why price (VRP) is destiny.
- **[VLCC (DHT/FRO)](report_vlcc_en)** — win-rate-vs-VRP framework, break-even VRP, live options, cycle-position decision.
- **[Sectors + quality names (XLF/XLK, JPM/AXP)](report_sectors_en)** — hold-vs-hedge suitability, the drift-vs-hedge tension.
- **[AI-bubble report §11](../ai_bubble/report_en)** — the crash-risk view that would justify a tactical XLK hedge.

*Cross-asset cheat-sheet. Bilingual mirror: [中文版 →](summary_cn). Data + code: [`tail_hedge/`](https://github.com/liqiqiii/VLCC-Analysis-2026/tree/master/tail_hedge). Education/analysis only — not investment advice.*

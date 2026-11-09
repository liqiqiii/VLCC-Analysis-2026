---
layout: default
title: "Lennar vs Mitsui Fudosan: Is Berkshire's Homebuilder at a Cycle Turning Point?"
---

# 🏠 Lennar (LEN) vs Mitsui Fudosan: Is Berkshire's Homebuilder at a Cycle Turning Point?

*November 9, 2026 — VLCC Analysis Series #55 (Chinese version: #56). Follows [#53](53_Mitsui_Fudosan_Turnaround_EN.md).*

> **Disclaimer**: research only, not investment advice.
>
> **Tags**:
> - **[P]** primary source or official statistics.
> - **[S]** secondary source.
> - **[U]** unverified.
> - **[E]** author's calculation.
> - **[H]** hypothesis.
>
> **Reproduce**: `python lennar_cycle/run_lennar.py`. Data and sources are in [`lennar_cycle/data/`](lennar_cycle/data/). Prices run to the 9-Nov-2026 close.
>
> **Conventions**:
> - Lennar's fiscal year ends 30 November.
> - Prices are split-adjusted and price-only.
> - Yahoo treats the Feb-2025 Millrose spin-off as a 1.033 "split". The script undoes that factor so pre-2025 prices match the book values reported at the time.
> - "Holder value" adds back the 0.5 Millrose (MRP) share each LEN share received.
>
> **Revision**: v2. gpt-6-astra rated v1 **"not safe to publish"** (3 blockers); see §8.

---

## Step 1 — Research Draft

**Core conclusion**

- **Lennar's share price may have already touched a trough-type valuation, but the operating trough is not confirmed.**
  - At its 14-Oct-2026 low ($73.53), LEN traded at about **0.84x** the book value published at that point.
  - That is at or below the point-in-time lows of the 2011, 2018 and 2022 downturns (**0.88–0.90x**) [E].
  - It has since bounced **+25%** to about **1.0x** book.
  - The operating data are mixed:

  | Area | Improving | Still deteriorating |
  |---|---|---|
  | **Supply** | Single-family starts **−32.5%** from the Dec-2020 peak. Completed new homes for sale peaked at **128k (Jan-2026)** and have fallen to **111k (−13%)**, down in 6 of the last 8 months [P] | Inventory is still high: 111k vs 78k in 2019; months' supply **8.4** (87th percentile since 1963) [P] |
  | **Demand** | — | Orders **−9%** YoY. Mortgage rate peaked at **7.40%** in Oct-2026. Management cites "deterioration in market conditions through the quarter" [P/S] |
  | **Margins** | Gross margin on home sales **15.8%** (Q3 FY2026), up for two quarters from 15.6% (Q2 figure is secondary) [P/S] | Q4 guide flat (15.5–16.0%); incentives about 12% of price [P] |
  | **Earnings** | — | Trailing EPS **$5.29**, −63% from FY2024. P/E **17x** [E] |

- **Lennar is not a Mitsui-type turnaround.** The mechanics differ:
  - **Business**: Mitsui is a landlord with recurring rent and land on its balance sheet. Lennar is a homebuilder that sells each house once. Fewer than 2.5% of its homesites are owned; the rest are controlled through options and land banks [P].
  - **Downturn**: Mitsui needed four years of net losses, a land revaluation and a bank clean-up. Lennar's current downturn shows up as **margin compression with no net losses** (FY2025 net income $2.1bn) [P]. Impairment amounts were not checked.
  - **Book value**: the 2025 drop in equity (−21%) came from the **Millrose spin-off**, which moved $5.5bn of land and $1.0bn of cash to shareholders, not from write-downs [P].
  - **Off-balance-sheet risk**: the land-light model does **not** remove exposure. Lennar still bears option deposits and land-bank commitments, which are not quantified here.
- **What carries over from Mitsui is how the share price behaved.** The stock turned before the real economy:
  - Mitsui's stock bottomed two years before land prices.
  - LEN's daily low (Nov-2008) came 4 months before single-family starts bottomed (Mar-2009); on month-end closes the lead was only 1 month (Feb-2009).
  - At the 2005 peak, LEN led starts by about 6 months.
  - So a confirmed turn in starts and margins would probably come **after** the stock bottoms [H].
- **Berkshire's buying is an indicator, not a timing signal.**
  - Berkshire added Class A shares from Q1 2025 and held **13.11m** by 30-Jun-2026 (6.2% of Class A) [S]. It has held LEN.B since 2023 [S].
  - Approximate cost is **~$101** (share adds × actual quarter-end closes) [E]; LEN is now about 9% below that.
  - The Q3 13F (due Monday 16-Nov-2026) shows holdings at **30-Sep**, so it cannot show trading around the October low.

**Supporting points (claim → evidence needed)**

1. *The October low reached past trough valuations* → point-in-time P/B at past lows. **Available [E]**, with book value as published at the time of each low (§3):
   - 2011: 0.89x; 2018: 0.88x; 2022: 0.90x; Oct-2026: **0.84x**.
   - Crisis lows were lower: 2008 0.15x, 2020 0.58x.
2. *Supply is adjusting* → inventory and starts. **Available [P]**: completed inventory −13% from its January peak; starts −32.5% from peak.
3. *The stock tends to turn before starts* → turning points and lagged correlation. **Available [E]**:
   - 12-month changes correlate +0.69 at lag 0 and +0.57 with starts 6 months later (1996–2019).
   - The windows overlap, so this is an association only.

**Opposing points (claim → evidence needed)**

1. *Earnings have not bottomed* → orders, margins, guidance. **Available [P]**: orders −9%; FY2026 deliveries cut to 80–81k; Q4 margins flat; rates rose in October.
2. *Book-value support is uncertain* → land-bank and option exposure, impairments. **Not quantified.** In 2007–09 book per share fell 63%.
3. *Lennar's underperformance may reflect its strategy rather than the cycle* → peer margins and returns. **Not checked**:
   - Holder value is −46% from the 2024 high, vs D.R. Horton −21%, PulteGroup −9% and Toll −7% (price only).
   - Lennar's volume-first strategy may justify a lower P/B than its own history.

---

## 1. Lennar vs Mitsui Fudosan

| Dimension | Mitsui Fudosan (1989–2009, #53) | Lennar (2005–2026) |
|---|---|---|
| Business | Landlord and developer; recurring rent; REIT sponsor | Homebuilder; sells each home once; mortgage and title arm |
| Land | Owned on the balance sheet (revalued 2002) | Fewer than 2.5% of homesites owned; options and land banks; Millrose spin (Feb-2025) |
| Cycle driver | Land deflation, bad debts, bank recapitalisation | Mortgage rates and affordability; inventory absorption |
| Bust length | ~13 years (1991–2003/05) | 2006–2011 (~5 years); current downturn since 2022 |
| Loss recognition | Four years of net losses (−¥170bn) | 2007–09 net losses (−$3.47bn); **none now** |
| Book value, peak to trough | Equity −35% (FY1995–FY2000) | BPS −63% (FY2006 $36.05 → FY2009 $13.22) |
| Stock, peak to trough | −83% (1989 → 2003) | −95% (2005 → 2008); current episode so far: **−62%** to the Oct-2026 low (price only; −56% including Millrose at $21.22) |
| P/B at the trough (point-in-time) | 0.77x revalued book (Apr-2003) | 2008: 0.15x; 2011: 0.89x; 2018: 0.88x; 2022: 0.90x; **Oct-2026: 0.84x**; now ~1.0x |
| P/B at the peak | 3.7x (2007) | 2.6x (2005); 2.0x (2024) |
| Stock vs the real economy | Led land prices by ~2 years at the trough | Led starts by ~1–4 months at the trough and ~6 months at the peak |
| Notable buyer | — | **Berkshire** |

**Reading**:
- Lennar's cycles are **shorter and sharper**. With no rent income to cushion it, earnings fall with prices and volumes.
- Its land-light balance sheet *may* reduce a 2008-style collapse in book value [H]. The exposure has moved into option deposits and land-bank commitments, which are not quantified here.

---

## 2. CRule 1 — two-cycle backtrack

| | Cycle 1 (2005–2012) | Cycle 2 (2020–now) |
|---|---|---|
| Driver | Subprime credit, speculation, overbuilding | Pandemic demand and 2–3% mortgages, then a rate shock (2.65% → 7%+) |
| Single-family starts (SAAR) | 1,823k (Jan-2006) → 353k (Mar-2009), −81% | 1,273k (Dec-2020) → **859k** (Sep-2026), **−32.5%**; about 2.0x the 2011 average |
| Completed new homes for sale | Peak 194k (Sep-2007) | 31k (2021–22 low) → **128k** (Jan-2026) → **111k** (Sep-2026) |
| Months' supply | Peak 12.2 | **8.4** |
| LEN gross margin on home sales | 26.0% (2005) → 6.0% (2007; 13.9% ex write-downs) → 19.7% (2010) | 27.5% (2022) → 17.7% (2025) → **15.8%** (Q3 FY2026) |
| LEN stock | $67.13 (Jul-2005) → $3.58 (Nov-2008), −95% | $192.45 (Sep-2024) → $73.53 (14-Oct-2026), −62% → **$91.58** (holder value $104.89, −46% from the peak) |
| How it ended | Starts at multi-decade lows; inventory cleared; Fed QE | **Not yet** |

**Lead/lag** (`run_lennar.py` §C) [E] — 12-month log changes of LEN vs single-family starts k months later (monthly, overlapping windows):

| Window | k=0 | k=3 | k=6 | k=9 | k=12 |
|---|---|---|---|---|---|
| 1996–2019 | +0.69 | +0.64 | +0.57 | +0.43 | +0.30 |
| 2000–2012 | +0.83 | +0.76 | +0.68 | +0.52 | +0.37 |
| 2013–2026 | +0.46 | +0.50 | +0.33 | +0.18 | −0.14 |

- Because the windows overlap, the effective sample is much smaller than n. These are associations, not rules.
- LEN mostly moves **with** starts, slightly ahead.
- The link has been weaker since 2013.

---

## 3. CRule 2 — valuation path

**Point-in-time P/B at trough episodes** — one low per episode; book = the latest quarterly equity *published by that date* ÷ approximate share count [E]:

| Episode | Low (date) | Book published by then | Book per share | P/B |
|---|---|---|---|---|
| 2008 crisis | $3.58 (21-Nov-2008) | FY2007 annual | 23.91 | **0.15** |
| 2011 | $12.50 (22-Aug-2011) | May-2011 quarter | 14.07 | **0.89** |
| 2018–19 | $38.06 (24-Dec-2018) | Aug-2018 quarter | 43.28 | **0.88** |
| 2020 Covid | $29.35 (23-Mar-2020) | Nov-2019 quarter | 50.49 | 0.58 |
| 2022 | $64.49 (16-Jun-2022) | Feb-2022 quarter | 71.38 | **0.90** |
| **2025–26** | **$73.53 (14-Oct-2026)** | Aug-2026 quarter | 87.29 | **0.84** |
| Now (9-Nov-2026) | $91.58 | Aug-2026 quarter (Yahoo BPS) | 90.62 | **1.01** |

- Share counts are FY-end equity ÷ BPS of the same FY, because quarterly share counts are not in XBRL. This is approximate.
- Peaks: 2005 at 2.6x book and 11.8x P/E; 2024 at 2.0x book and 14.0x P/E.

**Annual ranges** (same-year FY book; retrospective; pre-2025 prices with the spin factor undone) [E]:

| Year | Low–high | BPS | P/B | P/E | Gross margin |
|---|---|---|---|---|---|
| 2005 | 50–67 | 33.33 | 1.49–2.01 | 6.0–8.2 | 26.0% |
| 2008 | 3.6–21 | 16.34 | 0.22–1.31 | loss | 12.3% |
| 2011 | 12.5–21 | 14.31 | 0.87–1.47 | 26–44 | 19.9% |
| 2018 | 38–72 | 44.97 | 0.85–1.60 | 7.0–13.2 | 19.6% |
| 2022 | 64–113 | 83.19 | 0.78–1.35 | 4.1–7.2 | 27.5% |
| 2024 | 136–192 | 104.96 | 1.30–1.83 | 9.5–13.4 | 22.3% |
| 2025 | 103–142 | 88.91 | 1.16–1.60 | — | 17.7% |

BPS is published to FY2020. For FY2021–FY2025 it is calculated as November equity ÷ December cover-page shares; if shares fell in December through buybacks, this slightly overstates BPS.

**Reading**:
- In non-crisis downturns since 2011, the **point-in-time** lows clustered at **0.88–0.90x** book. Only crises (2008, 2020) went far below.
- **P/E is not a useful trough signal for homebuilders.** At the 2022 low, P/E was 4x on peak earnings; it is 17x today on depressed earnings.

---

## 4. Current position (CRule 1.5)

```
Current cycle position: Downturn; valuation reached a past-trough level in Oct-2026; operating trough not confirmed
Evidence:
  - Point-in-time P/B 0.84x at the 14-Oct low (past non-crisis lows 0.88–0.90x); now ~1.0x after +25%
  - Supply adjusting: completed homes for sale −13% from the Jan-2026 peak; starts −32.5%
  - Demand weak: orders −9%; mortgage rate 7.18% (peaked at 7.40% in Oct)
  - Gross margin 15.8%, Q4 guide flat
Historical analog: 2011 / 2018–19 (stock bottomed near ~0.9x book while operations were still soft)
Key risk: rates staying above 7% → more incentives, margins in the mid-teens or lower; land-bank commitments
```

**Signals that would confirm a turn**:

| Signal | Now | Turn if | Status |
|---|---|---|---|
| Completed new homes for sale | 111k, falling | Falling for 3+ months | **Met** (Jun–Sep: 113 → 114 → 112 → 111; down in 6 of 8 months) |
| LEN gross margin | 15.8% | Two quarters above 17% with incentives below 10% | Not met |
| New orders YoY | −9% | Positive | Not met |
| Months' supply, new | 8.4 | Below 7 | Not met |
| 30-year mortgage rate | 7.18% | Below 6.5% | Not met |
| Single-family starts | 859k | Stop falling | Not checked |

---

## 5. Berkshire's position

| Quarter (13F, Class A) | Shares | Change | Actual quarter-end close |
|---|---|---|---|
| Q1 2025 | ~1.9m | New Class A position | $114.78 |
| Q2 2025 | ~7.0m | +265% | $110.61 |
| Q3–Q4 2025 | ~7.1m | ~0 | — |
| Q1 2026 | ~10.1m | +43% | $86.84 |
| Q2 2026 | **13.11m** | +30% | $90.49 |

Source: 13F history via HoldingsIntel and TheStreet [S]. Berkshire also holds LEN.B (since Q2 2023 per HoldingsIntel; 298k shares in Q2 2026).

- **Cost**: the proxy average is **~$101** [E], using quarter-end closes; the actual cost is unknown.
- **Size**: about $1.2bn, roughly 0.4% of Berkshire's 13F portfolio.
- **Timing**: the next 13F (Q3 2026, due 16-Nov-2026) reports **30-Sep** holdings. Trading around the October low would show up only in the Q4 filing (Feb-2027).
- **Pattern**: Berkshire added at about 1x book while earnings were falling, which resembles the logic of Mitsui's best entry in 2003. It is not evidence of the turning point.

---

## 6. Scenarios (Rule 8; illustrative, not a recommendation) [E]

**Assumptions**:
- Start: price $91.58; BPS $90.62 (Aug-2026).
- BPS rolls forward by a constant EPS less a ~$2 dividend; buybacks are ignored.
- Price-only returns.

| Scenario | EPS / year | P/B (12m / 24m) | 12-month value | 24-month value |
|---|---|---|---|---|
| Bear: rates stay above 7%, margins ~14% | ~$4.0 | 0.80x / 0.90x | ~$74 (−19%) | ~$85 (−7%) |
| Base: margins stabilise at 16–17%, rates 6.5–7% | ~$5.5 | 1.05x / 1.20x | ~$99 (+8%) | ~$117 (+28%) |
| Bull: rates below 6.5%, margins above 19% | ~$7.5 | 1.30x / 1.60x | ~$125 (+36%) | ~$163 (+78%) |

- The bear case P/B of 0.8x is about the October-2026 low (0.84x).
- A 2008-style crisis (0.15x) is not modelled.

---

## 7. Day1Global (condensed)

| Module | Assessment |
|---|---|
| A — Revenue quality | One-time home sales; volume-first strategy; incentives ~12% |
| B — Operating leverage | Gross margin 27.5% → 15.8%; SG&A 9.2% |
| C — Cash flow | Homebuilding debt-to-capital 16.6%; buybacks ($256m in Q3); ~2.2% dividend yield |
| D — Guidance | Q4: 22–23k deliveries, gross margin 15.5–16.0%, ASP $370–380k |
| E — Competition | Peers have held up better on price; margin comparison not checked |
| L — Ownership | Miller family (Class B votes); Berkshire ~6% of Class A |
| O — Accounting | Millrose spin cut equity 21%; option and land-bank commitments off balance sheet (not quantified) |

**Perspectives**:

| Perspective | View |
|---|---|
| Buffett | Scale and cost leader, bought near book |
| Klarman | ~1.0x book; safety depends on book holding |
| Tepper | Catalyst: mortgage rates |
| Druckenmiller | The Fed path dominates |
| Tiger Cubs | Short thesis: volume-first erodes margins |
| Baillie Gifford | No 10x case |

**Pre-mortem** (down 30% in a year):
1. Mortgage rates above 7.5%.
2. A recession in jobs.
3. Land-bank or option take-downs at high prices.
4. A price war on completed inventory.

---

## Step 2 — Strict Peer Review (of the Step-1 draft)

**1. Facts that need verification**
- Berkshire share counts and LEN.B history (aggregator data).
- Q2 FY2026 gross margin of 15.6% (secondary).
- Q4 FY2025–Q2 FY2026 EPS (Yahoo).
- The approximate share counts used for point-in-time BPS.

**2. Logical leaps / equivocation**
- "Trough valuation reached" assumes book value is reliable.
- Leading relationships rest on a few turning points.
- Berkshire's buying is not a timing signal.

**3. Missing counterexamples / competing explanations**
- Strategy-driven underperformance.
- Off-balance-sheet land commitments.
- Existing-home inventory and regional mix.

**4. Most important primary sources to add**
- Lennar Q4 FY2026 results (mid-December).
- 10-K land-bank and option commitments.
- Berkshire Q3 13F (16-Nov).
- Peers' margins and ROE.

**5. Sentences that can at most be classified as speculation**
- "May have touched a trough valuation."
- The scenarios.
- "The operating turn will follow the stock."

---

## 8. gpt-6-astra adversarial review — findings and actions

The review was scoped to 6 web lookups. Verdict on v1: **"not safe to publish"**. The reviewer confirmed:
- the valuation table, correlations, peer moves and scenario outputs;
- the 2007–09 losses ($3.47bn);
- the Q3 FY2026 figures;
- the Millrose ratio and its $5.5bn of land plus $1.0bn of cash.

| # | Finding | Verdict | Action |
|---|---|---|---|
| B1 | Inventory misread: completed homes for sale **peaked at 128k in Jan-2026** and fell to 111k; "most since 2009" and "supply still building" were wrong | Correct | Corrected; the "falling for 3+ months" signal is marked **met** |
| B2 | "In the trough range" failed: 1.01x is above 0.75–0.87x; episodes were duplicated; P/B used future book; the 1.033 factor was only footnoted | Correct | One low per episode; point-in-time book from XBRL quarterly equity (0.88–0.90x); 1.033 factor undone in the script. New finding: the Oct-2026 low was at 0.84x |
| B3 | Berkshire timeline: the Q3 13F shows 30-Sep holdings; it is due Mon 16-Nov; LEN.B has been held since 2023 | Correct | Fixed |
| m1 | Cost proxy used wrong quarter-end prices | Correct | Actual closes used; ~$101 |
| m2 | Scenario EPS secretly grew 10% in year two | Correct | Constant EPS; price-only; Aug-2026 starting book noted |
| m3 | BPS date mismatch (Nov equity vs Dec shares) | Correct | Disclosed |
| m4 | Months' supply percentile; starts peak 1,273k (Dec-2020, −32.5%); "2.4x 2011" | Correct | 87th percentile (full history); −32.5%; 2.0x |
| m5 | Lead time: 4 months on the daily low, 1 month on month-end closes; the −46% is not a completed trough | Correct | Both shown; current episode labelled "so far" |
| m6 | "No impairments" and "book is sturdier" were unsupported | Correct | Now "no net losses"; land-light benefit labelled [H] |

No further review round was run after these fixes.

---

*Files: `lennar_cycle/run_lennar.py`, `lennar_cycle/data/*.csv`.*

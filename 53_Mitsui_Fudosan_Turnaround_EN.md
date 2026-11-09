---
layout: default
title: "Mitsui Fudosan 1989–2009: Anatomy of a Quality Real-Estate Turnaround"
---

# 🏙️ Mitsui Fudosan 1989–2009: Anatomy of a Quality Real-Estate Turnaround

*November 6, 2026 — VLCC Analysis Series #53 (Chinese version: #54). Follows [#47](47_PAG_Distressed_Playbook_EN.md), [#49](49_PAG_Track_Record_EN.md) and [#51](51_PAG_Follow_Backtest_EN.md).*

> **Disclaimer**: research only, not investment advice.
>
> **Tags**:
> - **[P]** primary source or official statistics.
> - **[P†]** primary document cited by the gpt-6-astra review, not re-read by the author.
> - **[S]** secondary source.
> - **[U]** unverified.
> - **[E]** author's calculation.
> - **[H]** hypothesis.
>
> **Reproduce**: `python mitsui_turnaround/run_mitsui.py`. Data and sources are in [`mitsui_turnaround/data/`](mitsui_turnaround/data/).
>
> **Conventions**:
> - Share prices are split-adjusted for the 2024 3:1 split; pre-2024 per-share figures are divided by 3 to match.
> - Prices are nominal and exclude dividends unless marked "real" (deflated by Japan CPI to 2020 yen).
> - FY = fiscal year **ending** March (Japanese "FY1996" = this report's FY1997).
>
> **Revision**: v2. gpt-6-astra rated v1 **"not safe to publish"** (6 blockers); see §10.

---

## Step 1 — Research Draft

**Core conclusion**

- **Mitsui Fudosan's 2003–2007 rebound (6.9x from the low) came at the end of a 13-year sequence.** It is not evidence that buying a quality name in a downturn works by itself. The sequence:
  1. **Recognise the losses**: four straight net losses, FY1997–FY2000, ¥169.7bn in total [P].
  2. **Reset the accounts**: a 2002 land revaluation (a +¥166.8bn accounting uplift), then FY2005 impairment of ¥33.8bn [P].
  3. **Take part counter-cyclically in prime land**: Mitsui led the 2001 consortium for the Roppongi former Defense Agency site, which became Tokyo Midtown. Mitsui's economic share is **unknown** [P].
  4. **A new exit channel**: the first J-REITs listed in 2001, with Mitsui as sponsor of Nippon Building Fund [S].
  5. **An occupancy turn**: Tokyo office vacancy went from 8.1% (end-2003) to 2.7% (end-2007) [S].
- **The share price bottomed on 11-Apr-2003, before most of the "turn" evidence existed:**
  - before the Resona recapitalisation (May-2003 [S]);
  - before the vacancy peak was known (end-2003);
  - about two years before land prices bottomed (March 2005).

  Using only information published by then, it traded at **~0.77x book** (revalued book, FY ending Mar-2002) and **~16x earnings** [E].
- **It was a cyclical rebound, not a permanent re-rating.**
  - The stock fell **−78%** from its 2007 high to its 2009 low, while FY2009 net income fell only **−4%**.
  - In this single-company, price-only sample, the entry point mattered greatly. A buyer at the 1989 high had 1.18x at the 2007 high and 1.43x by November 2026, about 1% a year over 37 years. A 2003-low buyer had 6.9x by 2007 [E].
  - Dividends are excluded, so this is not a total-return comparison.

**Supporting points (claim → evidence needed)**

1. *Loss recognition came before the rebound* → audited results and equity over time. **Available [P]**:
   - Net losses FY1997–FY2000: −¥44.0bn, −¥31.5bn, −¥35.8bn, −¥58.4bn.
   - Equity fell from ¥606bn (Mar-1995) to ¥395bn (Mar-2000), −35%; the equity ratio bottomed at 13.2%.
2. *The share price moved ahead of land prices* → stock vs land index timing. **Available, but weak [E]**:
   - At every one of the four turns, the share price turned before the land index (§3).
   - Annual changes correlate most with land about **15 months later**: r = +0.52 (n=33, naive 95% CI +0.21..+0.73) for 1981–2014.
   - The 2004–2014 figure (r = +0.72) has **n = 10**, with CI +0.17..+0.93.
   - Serial correlation and lag selection are not treated, so this is an association, not a rule.
3. *Earnings and valuation both drove 2003–2007* → EPS, operating income and P/B path. **Available [P]/[E]**:
   - Operating income +64% on revenue +23% (FY2004 → FY2008).
   - Net income rose 6x, but most of the step-up came from below operating income (the bridge was not compiled).
   - P/B went from 0.77x (2003 low, point-in-time) to 3.72x (2007 high).

**Opposing points (claim → evidence needed)**

1. *The rebound was mainly sector beta* → peer comparison. **Partly available [P]**:
   - Mitsubishi Estate rose 6.04x from its 2003 low to its 2006–07 high, vs Mitsui's 6.65x (daily closes).
   - BOJ easing, bank clean-up, foreign capital and the new J-REIT market were common to both [S].
   - Mitsui-specific alpha is **not demonstrated**.
2. *"Quality survives" is survivorship* → the outcomes of all comparable developers. **Not available.**
   - Emerging developers that grew on fund money failed in 2008 (Urban Corp, Suruga) [S].
   - A full sample of 1990s developers was not compiled.

---

## 1. The case at a glance

| Item | Bubble (1985–1991) | Bust (1991–2003/05) | Rebound (2003–2007/08) | Crash (2007–2009/12) |
|---|---|---|---|---|
| 6-city commercial land (end-March, 2000=100) | 128.9 → **519.4** (Mar-1991), 4.0x | → **68.4** (Mar-2005), **−86.8%** | → 101.3 (Mar-2008), +48% | → 71.2 (Mar-2012), −30% |
| Tokyo 5-ward office vacancy (year-end) | 0.39% (1990) | 8.08% (1994) → 3.17% (2000) → **8.12% (2003)** | → **2.65% (2007)** | → 9.01% (2011) |
| Tokyo 5-ward avg rent (¥/tsubo, year-end) | 44,193 (1991) | → **17,577 (2004)**, −60% | → 22,186 (2008), +26% | → 16,207 (2013) |
| 8801 share price (adjusted) | 313.9 (1985) → **1,129.9 (1989 high)** | → **193.6 (2003 low)**, −82.9% nominal / −84.4% real | → **1,333.3 (2007 high)**, 6.9x | → 288.9 (2009 low), −78% |
| Net income | ¥41.4bn (FY1991) | Losses FY1997–FY2000 (total −¥169.7bn) | ¥14.5bn (FY2004) → ¥87.4bn (FY2008) | ¥83.6bn (FY2009), ¥60.1bn (FY2010) |

Sources: [P] land (JREI via the Statistics Bureau), annual reports, Kabutan prices; [S] Miki Shoji office data (transcribed from an image table); [E] ratios.

**Note**: the 2007 nominal high (1,333.3) was 18% above the 1989 high (+7.4% real), while land in 2008 was still 80% below its 1991 peak. The share price and land values **decoupled**.

**Candidate explanations** [H]:
- earnings growth (operating income +64%);
- fee businesses and REIT sponsorship;
- a revalued book;
- near-zero interest rates;
- foreign capital flows.

They are not separated here.

---

## 2. What Mitsui actually did (FY1997–FY2008)

| Period | Action | Why it matters | Tag |
|---|---|---|---|
| FY1997–FY2000 | Four consecutive net losses (¥169.7bn total); dividend cut from ¥9 to ¥5 (pre-split) | Booked the losses instead of carrying them | [P] |
| 1998–2004 | Shift from owning to managing (an "assets under management" model); securitisation with AIG on the Shin-Nikko building (1999) | Recycles capital and earns fees | [S] |
| 17-Sep-2001 | Led a consortium (Zenkyoren, Yasuda Life, Fukoku Life, Sekisui House, Daido Life) that won the government tender for the Roppongi Defense Agency site (78,394 m²); paid Feb-2002 | Prime land bought near the trough. Price, Mitsui's share and funding are **unknown** here | [P] |
| 10-Sep-2001 | Nippon Building Fund (Mitsui-sponsored) listed as one of the first two J-REITs | A recurring buyer for stabilised buildings | [S] |
| Mar-2002 | Land revaluation: ¥156.4bn reserve plus ¥10.4bn retained earnings; equity rose from ¥411bn to ¥610bn | **An accounting uplift, not new capital.** The reserve was **25.8% of equity** at Mar-2003 | [P] |
| Oct-2002 | Mitsui Fudosan Hanbai becomes a wholly owned subsidiary | Simplifies the group | [S] |
| FY2005 | Early adoption of impairment accounting: **¥33.8bn actual** (¥34bn forecast) | Small, partly because the land was already revalued | [P] |
| FY2006 | Shares rose from 823.4m to 881.4m, mainly through **convertible-bond conversion (55.9m shares, non-cash)** | Debt became equity; this was **not** a cash raise | [P]/[P†] |
| Jul-2005 / Jan-2007 | Nihonbashi Mitsui Tower; Tokyo Midtown completed | Delivered as rents rose | [P] |

**Correction to #49**:
- #49 said Mitsui's 2001–03 asset purchases were "not examined".
- They are now examined: Mitsui **did** take part in buying distressed-era prime land, as consortium leader for the Defense Agency site.
- Whether this was funded from Mitsui's own balance sheet, and how large its share was, is unknown. A "permanent-capital" contrast with PAG is plausible but **not demonstrated** for this asset.

---

## 3. CRule 1 — two-cycle backtrack: share price vs land and rents

**Correlation and lead/lag** (`run_mitsui.py` §B) [E]. Lag k pairs the December close of year Y with land at end-March of year Y+1+k: k=0 means 3 months later, k=+1 means 15 months, k=+2 means 27 months.

| Window | R² log level (k=0) | Year-on-year correlation (n, naive 95% CI) | Reading |
|---|---|---|---|
| 1981–2014 | 0.01 (n=34) | k=0: +0.33 (34; −0.01..+0.60); **k=+1: +0.52 (33; +0.21..+0.73)**; k=+2: +0.43 (32; +0.10..+0.68) | Levels decoupled after 2003; changes associate with land 15–27 months later |
| Cycle 1, 1985–2004 | 0.40 (n=20) | k=+1: +0.52 (20; +0.10..+0.78); k=+2: +0.51 (20; +0.08..+0.78) | Same direction |
| Cycle 2, 2004–2014 | 0.11 (n=11) | k=+1: +0.72 (**n=10**; +0.17..+0.93) | Wide interval |
| Stock vs Tokyo rent, 2004–2013 | — | k=+1: +0.61; k=+2: +0.77 (n=10) | Small sample |
| Stock vs Tokyo rent, 2013–2024 | — | k=+1: +0.15 (n=11) | No link in the latest cycle |

**Caveats**:
- The confidence intervals assume independent observations, but annual changes are serially correlated, so the true uncertainty is wider.
- The lag was chosen after looking at the results.
- Read this as "the stock tended to move ahead of land", not as a rule with a fixed lead time.

**Turning points** (annual granularity):

| Turn | Stock | Land (6-city commercial) | Rent (Tokyo 5 wards) | Stock relative to land |
|---|---|---|---|---|
| Peak 1 | 1989 high | Mar-1991 (JREI semiannual peak Sep-1990) | 1991 | Earlier |
| Trough 1 | **11-Apr-2003 low** | Mar-2005 | 2004 | Earlier by ~2 years |
| Peak 2 | 4-Jun-2007 high | Mar-2008 | 2008 | Earlier by ~1 year |
| Trough 2 | Mar-2009 low | Mar-2012 | 2013 | Earlier by ~3 years |

**Cycle comparison**:

| | Cycle 1 (1985–2005) | Cycle 2 (2005–2012) |
|---|---|---|
| Driver | Credit bubble, then bad-debt deflation | Fund and J-REIT inflows, foreign capital, low rates; ended by the global credit freeze |
| Land, peak to trough | −86.8% over 14 years | −30% over 4 years |
| Stock, peak to trough | −82.9% over 14 years | −78% over 2 years |
| What ended it | Loss recognition, bank recapitalisation, a new REIT market (association, not proven cause) | Lehman; refinancing failures of emerging developers and one J-REIT (New City Residence, Oct-2008) [S] |

---

## 4. CRule 2 — the valuation path

**Point-in-time at the turning points** — using only the latest balance sheet and earnings already published on each date [E]:

| Date | Price | BPS (FY) | P/B | EPS (FY) | P/E |
|---|---|---|---|---|---|
| 2003 low (11-Apr-2003) | 193.6 | 250.1 (Mar-2002) | **0.77** | 12.2 (Mar-2002) | **15.8** |
| 2007 high (4-Jun-2007) | 1,333.3 | 357.9 (Mar-2007) | **3.72** | 28.5 (Mar-2007) | **46.8** |
| 2008 low (Oct-2008) | 328.6 | 368.4 (Mar-2008) | 0.89 | 33.1 (Mar-2008) | 9.9 |
| 2009 low (Mar-2009) | 288.9 | 368.4 (Mar-2008) | **0.78** | 33.1 (Mar-2008) | **8.7** |

**Retrospective annual table** — uses the FY ending in March of the same calendar year, so prices from January to May use a balance sheet that was not yet published:

| Year | Low–high | BPS (basis) | P/B | P/E | Equity ratio |
|---|---|---|---|---|---|
| 1991 | 380–530 | ~235 (approx.) | 1.62–2.26 | 22–31 | 16.4% |
| 1998 | 213–487 | 212 (equity ÷ shares) | 1.00–2.30 | loss | 16.6% |
| 2000 | 230–459 | 162 (equity ÷ shares) | 1.42–2.83 | loss | **13.2%** |
| 2003 | 194–395 | 255 (published) | 0.76–1.55 | 19–38 | 21.5% |
| 2005 | 384–830 | 279 (published) | 1.38–2.98 | 33–72 | 23.5% |
| 2006 | 672–1,017 | 325 (published) | 2.07–3.13 | 30–45 | 28.7% |
| 2007 | 780–1,333 | 358 (published) | 2.18–3.72 | 27–47 | 28.7% |
| 2008 | 329–942 | 368 (published) | 0.89–2.56 | 10–28 | 26.7% |
| 2012 | 373–713 | 408 (IRBANK) | 0.91–1.75 | — | — |
| 2026 (to 6-Nov) | 1,400–2,158 | 1,188 (IRBANK) | 1.18–1.82 | — | — |

**BPS basis**:
- From FY2002: "net assets per share" as published.
- FY1997–FY2001: equity ÷ shares issued (812.6m; treasury stock negligible).
- FY1991–FY1996: approximate (shares implied by net income ÷ EPS).
- Before and after March 2002, book value is on different bases because of the land revaluation. The revalued book is an accounting uplift, not proven recoverable value.

**Reading**:
- **The trough was about 0.8x revalued book** (2003, 2009). Before 2002, P/B was distorted by land at historical cost, and P/E meant little in 1993–2001 because profits were near zero or negative.
- **P/E on annual highs fell from about 80x (2004) and 72x (2005) to about 47x at the 2007 high** as earnings rose. It then compressed to about 9–10x at the 2008–09 lows on flat earnings.
- The 2008 crash was **valuation compression**: P/B 3.7x → 0.8x, with net income −4%.

**Valuation template for this cycle** (descriptive):

| Phase | P/B | P/E | Earnings |
|---|---|---|---|
| Phase 1 (trough, Apr-2003) | ~0.8x | ~16x | Low |
| Phase 2 (2004–05) | 1.2–3.0x | 56–80x | Earnings depressed by special items |
| Phase 3 (2006) | 2.1–3.1x | 30–45x | Rising |
| Phase 4 (peak, Jun-2007) | 3.7x | ~47x | Rising |
| Phase 5 (2008–09) | ~0.8–0.9x | ~9–10x | Still near the peak |

---

## 5. CRules 3–10, condensed

- **CRule 3 — supply**:
  - New buildings in the central 5 wards: above 100 a year in 1990–93; 18–24 a year in 1996–2000; 49 in 2003 (a supply wave); 18 in 2005.
  - Vacancy peaked with the 2003 wave and fell to 2.65% by 2007 [S].
- **CRule 4 — operating leverage**:
  - Revenue +23% produced operating income +64% (FY2004 → FY2008) [P]/[E].
  - Net income rose 6.0x, but that larger step-up came from below operating income (extraordinary items, interest, tax). The bridge was **not compiled**.
- **CRule 5 — signals available at the 11-Apr-2003 low** (point-in-time only):
  - P/B about 0.77 on the published revalued book, and P/E about 16x.
  - Vacancy at end-2002 was 7.36% and rising, with a known 2003 supply wave.
  - Land was still falling.
  - FY1997–FY2000 losses were already booked.
  - BOJ quantitative easing had been in place since 2001 [S].
  - **Not yet available**: the Resona rescue (May-2003) and the end-2003 vacancy peak. The low therefore came **before** the clearest relief signals.
- **CRule 5 — signals at the 2007 high**:
  - Vacancy below 3%.
  - P/B 3.7x, P/E about 47x.
  - Emerging developers growing "3x in 3 years" on fund money [S].
- **CRule 6 — cross-cycle reference**: China property 2021–2026. §7 lists where it fits and where it does not.
- **CRule 7 — earnings sensitivity**: not modelled (historical case; no segment model).
- **CRule 8 — exit signals visible in 2007** (descriptive):
  - vacancy below 3%, with new supply rising (44 buildings in 2008);
  - P/B above 3x;
  - credit stress (not quantified here).
- **CRule 9 — inflation**: 1989 high to 2003 low −84.4% real; the 2007 high was +7.4% above the 1989 high in real terms.
- **CRule 10 — shadow supply**: the analog is the private funds and fund-fed developers of 2005–08, whose forced selling deepened the 2008 fall [S].

---

## 6. Entry-point outcomes (single company, price only)

| Bought at | Price | To the 2007 high | To the 6-Nov-2026 close | Price CAGR to 2026 |
|---|---|---|---|---|
| 1989 high | 1,129.9 | 1.18x | 1.43x | +1.0% (37 yrs) |
| 1992 low | 239.9 | 5.56x | 6.72x | +5.7% |
| 1998 low | 212.6 | 6.27x | 7.58x | +7.4% |
| **2003 low** | **193.6** | **6.89x** | 8.33x | +9.5% |
| 2007 high | 1,333.3 | — | 1.21x | +1.0% (19 yrs) |
| **2009 low** | 288.9 | — | 5.58x | +10.4% |

Nominal, dividends excluded [E].

- The entry points were picked with hindsight.
- Holding periods differ.
- This is one surviving company.

**What the table shows**: for this company, buying at the 1989 or 2007 high produced about 1% a year in price for 19–37 years; buying near the 2003 or 2009 low produced 9–10% a year. **What it does not show**: that valuation at entry determines outcomes in general.

---

## 7. Lessons for China property in 2026 (hypotheses)

| Japan sequence | Date | Closest China 2026 feature | Fit |
|---|---|---|---|
| Large landowners book losses | FY1997–FY2000 | Developer defaults, liquidations, write-downs | Partial. Depth **unknown**; the actors differ (Japan's surviving landlord vs China's failing developers) |
| **Bank** recapitalisation by the state | 1998–2003 (Resona 2003) | No direct recap of Wanda or Evergrande (#47). **Bank** recapitalisation is a different question and not assessed here | Not equivalent |
| New exit channel | J-REITs from 2001 | Consumer C-REITs from 2024 | Present, but small; eligibility case by case (#47) |
| Counter-cyclical prime-asset buyers | Mitsui-led consortium (2001); foreign funds | PAG (Wanda malls, 6666), SOE platforms | Present |
| Occupancy or rent turn | Tokyo vacancy peaked 2003 | China mall rents and NOI | **Unknown** |
| Share price ahead of land | 2003 vs 2005 | Listed HK/China property-services stocks (operators, not landowners) | Different asset type; test D in #51 tracks a related hypothesis |

[H] If a Japan-like sequence applies, listed prices could bottom **before** land prices stop falling, and possibly before the relief signals are visible (as in April 2003). This needs:
- loss recognition by the major owners;
- a working exit channel;
- an occupancy turn.

China currently shows the first two only in part, and the third is unverified.

---

## 8. Current positioning (CRule 1.5) — Mitsui in 2026

```
Current cycle position: Undetermined
Evidence (with dates): office vacancy 4.00% at end-2024 (down from 6.47% at end-2022); rent ¥20,296 at end-2024 vs the
          ¥22,206 peak at end-2019 — the latest office data are ~10 months old.
          Share price: 2,158 (Feb-2026 high) -> 1,400 (Oct-2026 low, −35%) -> 1,612 close on 6-Nov-2026 (−7.2% that day).
          1H results showing ordinary profit −25.3% were released at 15:30 JST, after the close, so they do not explain
          that day's fall [S]. P/B ~1.36x on BPS ¥1,188 (Mar-2026).
Historical analog: none clean — Japanese rates rising in 2024–26 vs falling or near zero in 2003–07 and 2013–19
Key risk: refinancing cost and cap-rate expansion if rates keep rising (not quantified here)
```

**Historical P/B reference** (not a target) [E]:

| P/B | Price at BPS ¥1,188 | vs ¥1,612 | Where it occurred |
|---|---|---|---|
| 0.8–0.9x | ~950–1,070 | −41% to −34% | Cycle troughs (2003, 2008–09) |
| 1.36x | ~1,612 | 0% | 6-Nov-2026 |
| 1.8x | ~2,139 | +33% | 2026 high |
| 3.7x | ~4,396 | +173% | The 2007 peak; an outlier |

No 12- or 24-month targets are given (case study).

---

## 9. Day1Global (condensed; Mitsui at the 2003 low)

| Module | Assessment |
|---|---|
| C (cash) | Dividend cut to ¥5 (FY1998–FY2000); equity ratio 13.2% (2000) → 21.5% (2003), partly from revaluation |
| L (ownership) | Domestic, with cross-shareholdings; in 2024 Elliott pushed for buybacks and cutting cross-holdings (#47) |
| O (accounting) | Revaluation reserve 25.8% of equity (2003); impairments ¥33.8bn (FY2005) |

**Six perspectives** — hindsight reconstructions [H]:

| Perspective | View |
|---|---|
| Buffett | Prime Tokyo land and brand |
| Baillie Gifford | REIT sponsorship as an option |
| Tiger Cubs | Revalued book under-priced |
| Klarman | ~0.77x P/B, ~16x P/E |
| Tepper | Later catalysts: Resona, J-REITs, Midtown |
| Druckenmiller | BOJ easing, bank clean-up |

**Anti-bias**:
- **Survivorship**: Mitsui survived; many developers did not.
- **Hindsight**: the trough is obvious only afterwards, and it came before the relief signals.
- **Narrative**: Mitsubishi Estate did about as well (6.04x vs 6.65x).

**Pre-mortem for a China investor copying this** (qualitative):
1. No bank-level backstop.
2. The C-REIT channel stays small.
3. Rents keep falling.
4. Entry at a 1989-style rather than a 2003-style valuation.

---

## Step 2 — Strict Peer Review (of the Step-1 draft)

**1. Facts that need verification**
- The Defense Agency site price, Mitsui's share and its funding.
- NBF's listing date and Mitsui's asset sales to it.
- The Resona date.
- Miki Shoji figures (transcribed from an image table).
- Kabutan split adjustment before 2000.
- The FY2006 convertible-bond conversion (cited from the reviewer).
- The ~¥750bn extraordinary-loss total (secondary).

**2. Logical leaps / equivocation**
- "Turnaround" applies to the share price and earnings, not to land values.
- A correlation at a chosen lag is not a lead-time rule.
- A revalued book is not a recoverable value.

**3. Missing counterexamples / competing explanations**
- Sector beta (Mitsubishi Estate).
- Foreign capital flows.
- Failed developers.
- Mitsui's 1990s overseas losses and changes in consolidation (not examined).
- Dividend-inclusive returns.

**4. Most important primary sources to add**
- FY2004 net-income bridge (extraordinary items).
- Ministry of Finance tender results.
- J-REIT index history.
- BOJ policy timeline.
- Miki Shoji original data.
- Annual reports for FY1992–FY1996.

**5. Sentences that can at most be classified as speculation**
- All of §7.
- The Day1Global perspectives.
- The candidate explanations for the decoupling between share price and land.

---

## 10. gpt-6-astra adversarial review — findings and actions

The review was scoped to 6 web lookups. Verdict on v1: **"not safe to publish"**. The reviewer reproduced the arithmetic and confirmed:
- Mitsubishi Estate's 6.04x;
- the fiscal-year naming;
- the 1989 split adjustment;
- the 6-Nov-2026 results.

| # | Finding | Verdict | Action |
|---|---|---|---|
| B1 | BPS was derived from net income ÷ EPS (a weighted-average denominator); published FY2006 BPS is ¥975.6 raw / ¥325.2 adjusted, not ¥341.6 | Correct | Uses published BPS for FY2002–FY2008 and equity ÷ issued shares for FY1997–FY2001; FY1991–FY1996 marked approximate. FY2006 P/B is now 2.07–3.13x |
| B2 | "No look-ahead" was false: March accounts are published in May; Resona (May) and the year-end vacancy peak came after the April low | Correct | Annual table labelled retrospective; point-in-time table added; the CRule 5 signals are now limited to information available on 11-Apr-2003 |
| B3 | The FY2006 share increase was a non-cash convertible-bond conversion (55.9m shares), not a cash raise | Correct | Fixed (§2); source M20 [P†] |
| B4 | Lead time was overstated: k=+1 is 15 months; the 0.72 has n=10, CI 0.17–0.93; lag selection and serial correlation are untreated | Correct | Actual lags, n and CI shown; "1–2 year rule" replaced with an association |
| B5 | "Clean book" was unsupported: the revaluation added ¥166.8bn, and the reserve was ~26% of equity in 2003 | Correct | Now "revalued book; accounting uplift" with the 25.8% figure |
| B6 | The 6x net income was attributed to fixed costs, but operating income rose only 64% | Correct | Operating income bridge added; the remainder attributed to items below operating income (bridge not compiled) |
| m1 | The ¥34bn impairment was a forecast | Correct | Actual ¥33.8bn from AR2005 [P] |
| m2 | "P/E did not compress at the peak" — annual-high P/E was ~80x (2004) and ~72x (2005) | Correct | Rephrased (§4) |
| m3 | Current positioning used stale data and implied causality; the results came after the close | Correct | Data dated; causal claim removed |
| m4 | `sources.csv` was not valid CSV (unquoted commas) | Correct | Rewritten with proper quoting |

No further review round was run after these fixes.

---

*Files: `mitsui_turnaround/run_mitsui.py`, `mitsui_turnaround/data/*.csv`.*

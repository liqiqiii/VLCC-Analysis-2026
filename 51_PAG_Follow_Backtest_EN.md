---
layout: default
title: "Can Investors Follow PAG? A Pre-Registered Event Study and an Out-of-Sample Paper Portfolio"
---

# 🧪 Can Investors Follow PAG? Event Study of PAG Entries, Descriptive Exit Cases, and a Live Paper Portfolio

*November 6, 2026 — VLCC Analysis Series #51 (Chinese version: #52). Follows [#47](47_PAG_Distressed_Playbook_EN.md) and [#49](49_PAG_Track_Record_EN.md).*

> **Disclaimer**: research only, not investment advice.
>
> **Tags**:
> - **[P]** primary source or market data.
> - **[S]** secondary source.
> - **[E]** author's calculation.
> - **[H]** hypothesis (not tested here).
>
> **Reproduce**:
> - `python pag_distressed/run_follow_backtest.py` reproduces tests A and C. It uses Yahoo total-return data with a fixed cutoff of 6-Nov-2026; output goes to `pag_distressed/data/follow_backtest_results.csv`.
> - `python pag_distressed/paper_portfolio.py mark [date]` updates test D.
>
> **Revision**: v2, after a gpt-6-astra review rated v1 **"not safe to publish"** (6 blockers; see §8). The rules were fixed in code before the final run. The reviewer noted that pre-registration **cannot be proven** for tests A and C, because results were viewed while the code was being corrected. Only test D is genuinely out-of-sample.

---

## Step 1 — Research Draft

**The question**:
- Can an investor treat PAG's entries as a signal that a sector is about to turn, and follow them?
- Can an investor keep holding after PAG sells?

**Core conclusion**

- **Your reading needs two corrections.**
  1. **PAG buys at the *seller's* low, not necessarily the *industry's* low.** Its entries follow forced sellers: liquidators, receivers, redemption deadlines, founder fights. The sector can keep falling afterwards (Goldin tower, 2023; Lexmark, 2016).
  2. **PAG's exit timing is set by buyers and the fund clock, not necessarily by a completed turnaround** [H, from #49's cases].
- **Following PAG's entries (test A, n=5, total-return benchmarks)**:

  | Horizon | Average excess | Positive cases |
  |---|---|---|
  | 3 months | **+8.6pp** | 4 of 5 |
  | 12 months | **−9.6pp** | 0 of 4 |
  | 36 months | −20.4pp | 0 of 2 |

  In this small sample, early relative gains did not last, and no PAG entry was followed by 12-month sector outperformance.
- **The "hold after PAG sells" question cannot be tested with public data yet (test C).**
  - The cases with listed securities are not clean PAG exits:
    - CWK's IPO was a primary issue;
    - PAG's TME sale dates are unknown;
    - Xerox is the acquirer's whole business.
  - Their returns (−42pp average excess at 12 months, 0 of 3 positive) are reported only as **descriptive**. No exit-timing inference is drawn.
- **The sample is far too small for statistical inference.** No placebo dates or matched controls were run.
- **Test D starts today** and is the only genuinely out-of-sample check:
  - an equal-weight basket of six HK-listed property-services stocks, including 6666.HK;
  - benchmark: the Tracker Fund (2800.HK);
  - fixed review dates;
  - a hashed starting file.

**Supporting points (claim → evidence needed)**

1. *Early gains after PAG entries did not persist* → event-window excess returns. **Available [E]**: test A, §2.
2. *A public follower cannot buy at PAG's price* → deal terms vs public prices. **Available [P]**: on 6-Nov, 6666 closed at **HK$0.995**, **19% above** PAG's HK$0.8359 offer. That offer is not yet executable.

**Opposing points (claim → evidence needed)**

1. *The results may be noise or regime-driven* → more events, placebo dates, pre-event returns. **Not done.**
   - A3 and A4 use the same basket; their 12-month windows do not overlap, but they are not independent evidence about the sector.
   - The 2023–25 sector decline had its own causes.
2. *Proxies are not PAG's investments* → returns on PAG's actual holdings. **Unavailable.**
   - Ninestar's whole listed return is not a Lexmark measure.
   - HK office landlords are not the Goldin tower.

---

## 1. Rules

| Rule | Test A (follow entry) | Test C (descriptive) |
|---|---|---|
| Event date | First public disclosure | IPO trading date or acquirer's announcement |
| Entry | First close **after** the event date (T+1) | First close after the event date (T+1) |
| Prices | Total return for instruments **and** benchmarks: HK = 2800.HK (not the ^HSI price index), CN = 510300.SS, JP = 1306.T | US = SPY; China internet = KWEB |
| Basket | Equal weight; aligned on a common start, then normalised; no rebalancing | Single names |
| Excess | Instrument return minus benchmark return (simple difference) | Same |
| Horizons | 63 / 252 / 756 trading days; no partial windows; "to date" uses the 6-Nov-2026 cutoff | Same |

---

## 2. Test A — following PAG's entries

| # | Event (first disclosure) | Instrument (relation) | Benchmark | 3m | 12m | 36m | To 6-Nov-2026 (total / excess) |
|---|---|---|---|---|---|---|---|
| A1 | Lexmark buyout with Ninestar (19-Apr-2016) | 002180.SZ (listed partner; PAG was a JV minority) | CSI 300 ETF | +26.1 | −5.1 | −23.6 | −35.1% / −90.2pp |
| A2 | Goldin tower bought from receivers (12-Jan-2023) | Champion REIT + Swire Properties (office proxies) | 2800.HK | +5.5 | −7.9 | −17.1 | +23.8% / −5.1pp |
| A3 | Wanda new agreement (12-Dec-2023) | 7 HK-listed China property-services / commercial names | 2800.HK | −1.1 | −17.5 | — | +25.9% / −40.3pp |
| A4 | 48 malls: SAMR clearance published (20-May-2025; approved 6-May) | Same basket as A3 | 2800.HK | +12.3 | −7.8 | — | −10.3% / −18.1pp |
| A5 | Sapporo Real Estate (24-Dec-2025) | Sapporo HD + Mitsui Fudosan + Mitsubishi Estate | TOPIX ETF | +0.1 | — | — | +10.4% / 0.0pp |
| **Avg** | | | | **+8.6 (4/5 positive)** | **−9.6 (0/4)** | **−20.4 (0/2)** | |

Figures are excess returns in percentage points [E].

- **Excluded**:
  - China Music and USJ (2013): unlisted targets.
  - DTZ (2014): no data for the seller, UGL.
  - Yingde (2017): delisted, with its ticker reused by another company. PAG's strongest outcomes may be among the exclusions, which biases the test.
  - Evergrande Services (2026): tracked in test D.
- **Not checked independently**: the Lexmark, Goldin and Sapporo announcement dates.

---

## 3. Test C — descriptive only: listed vehicles linked to PAG exits

| # | Event | Instrument | Benchmark | 3m | 12m | 36m | Why it is not a clean PAG exit |
|---|---|---|---|---|---|---|---|
| C1 | Cushman & Wakefield NYSE IPO (2-Aug-2018) | CWK | SPY | −8.5 | −8.9 | −60.5 | Primary issue; PAG still held shares |
| C2 | Tencent Music NYSE IPO (12-Dec-2018) | TME | KWEB | +27.3 | −29.6 | −53.3 | PAG's sale dates unknown |
| C3 | Xerox agrees to buy Lexmark (23-Dec-2024) | XRX | SPY | −35.5 | −87.4 | — | The acquirer's whole business, not Lexmark |
| **Avg** | | | | −5.6 (1/3) | −42.0 (0/3) | −56.9 (0/2) | |

Figures are excess returns in percentage points [E]. These are post-IPO and post-acquisition outcomes, not a test of holding after PAG sells. A real test needs PAG's documented disposal dates, for example from selling-shareholder filings.

---

## 4. Interpretation (hypotheses)

| Observation | Possible reason | Status |
|---|---|---|
| Early relative gains that did not persist to 12 months (n=4) | PAG bought from forced sellers at negotiated prices, not at sector bottoms | [H] |
| A follower pays more than PAG | 6666 closed at HK$0.995 vs PAG's HK$0.8359 offer (+19%) | [P] |
| Mitsui-style holding is a different trade | Mitsui's 2003→2007 6.65x went to holders of a survivor bought at a market-wide trough, followed by −73% (#47) | [P] prices |

---

## 5. What an investor can take away (hypotheses, not tested rules)

The test supports only one narrow statement: **in five PAG entries, buying related listed stocks the day after the announcement did not beat the market over 12 months.** Everything else below is a hypothesis to examine, not a result:

1. Look at PAG's *method*: buying from forced sellers. In listed markets that suggests liquidator sales, index deletions, rights issues and spin-offs [H].
2. Use PAG's price as a valuation reference rather than a timing signal. 6666 at ~7.5x TTM (#47) is what a control buyer paid. Note that the listed share already trades above it [H].
3. Underwrite a lower exit multiple (Shan's stated rule) [H].
4. An individual has no fund clock, which allows Mitsui-shareholder-style holding. That also means sitting through drawdowns like Mitsui's −73% in 2008 [H].

---

## 6. Test D — out-of-sample paper portfolio (live from today)

| Item | Rule |
|---|---|
| Hypothesis | PAG's control bid for Evergrande Services (30-Oct-2026) signals a turn for HK-listed China property-services stocks |
| Inception | Official HK close on **6-Nov-2026**, captured after the close settled |
| Manifest | `pag_distressed/data/paper_portfolio_start.csv`, SHA-256 `5FB6CAFB707095EB99FFAEFC10A8548932F0A5B4096D16CB0884C336E64397EE`. The script refuses to overwrite it and checks re-fetched prices against it (0.5% tolerance) |
| Basket (HK$100k each, total return, no rebalancing) | 6666.HK @0.995, 1209.HK @41.64, 6049.HK @27.24, 2669.HK @3.365, 6098.HK @5.02, 1516.HK @0.67 |
| Benchmark | 2800.HK @24.60, HK$600k |
| Valuation | First common HK trading close **on or after** each review date: 6-Feb-2027, 6-Nov-2027, 6-Nov-2028, 6-Nov-2029 |
| Success test | The basket beats 2800.HK at **both** +12m and +36m |
| Prior from test A | 12-month outperformance was 0 of 4 |

**Command**: `python pag_distressed/paper_portfolio.py mark 2027-02-06` and so on for each review date. Results append to `paper_portfolio_log.csv`. Failures will be reported as prominently as successes.

**Note**: an earlier initialisation captured provisional pre-settlement prices (6666 at 0.985). It was discarded **before publication** and replaced with the settled closes above.

---

## 7. Anti-bias and pre-mortem

- **Anti-bias**:
  - Small n.
  - Shared basket (A3 and A4).
  - Proxies instead of targets.
  - The 2023–25 sector regime.
  - Survivorship: only listed instruments can be tested, and likely winners are excluded.
  - No placebo test.
- **Pre-mortem for test D** (qualitative):
  1. Property-services multiples keep compressing.
  2. Developer-related receivables cause new impairments.
  3. SAMR blocks or delays the 6666 deal.
  4. HK investors rotate out of China property.

---

## Step 2 — Strict Peer Review (of the Step-1 draft)

**1. Facts that need verification**
- The Lexmark, Goldin and Sapporo announcement dates.
- PAG's actual disposal dates for CWK and TME.
- Whether Yahoo's total-return adjustments for HK and China small caps are complete.

**2. Logical leaps / equivocation**
- Public proxies stand in for PAG's private investments.
- Acquirer and IPO returns are not post-exit holding returns (now labelled descriptive).

**3. Missing counterexamples / competing explanations**
- Sector-wide shocks.
- Excluded likely winners (Yingde, USJ).
- No placebo dates, matched controls or pre-event returns.

**4. Most important additions**
- PAG selling-shareholder filings.
- More events (test B).
- Placebo and bootstrap tests.

**5. Sentences that can at most be classified as speculation**
- All of §4 and §5 except the narrow test-A statement.
- Test D's outcome.

---

## 8. gpt-6-astra adversarial review — findings and actions

The review was scoped to 6 web lookups. Verdict on v1: **"not safe to publish as written."**

| # | Finding | Verdict | Action |
|---|---|---|---|
| B1 | HK benchmark ^HSI is a price index while the baskets are total return, which inflates excess returns | Correct | Switched to 2800.HK; all of test A rerun. 12m average −7.9 → **−9.6pp**; 36m −13.4 → −20.4pp |
| B2 | The A4 date was wrong: SAMR approved on 6-May and published on 20-May | Correct | Uses 20-May (first public disclosure) |
| B3 | Test C does not measure post-PAG-exit returns (CWK primary IPO; TME sale dates unknown; XRX is the acquirer) | Correct | Relabelled descriptive; exit-timing inference withdrawn |
| B4 | The paper-portfolio inception file was not enforced, and its prices were provisional | Correct | Re-initialised from settled closes; the script validates against the file; SHA-256 published |
| B5 | Mixed valuation dates and repeated fetches; review dates fall on weekends | Correct | One fetch per ticker; one common date; "on or after" rule |
| B6 | §5's prescriptions exceed what was tested | Correct | Narrowed to one tested statement; the rest labelled [H] |
| m1 | Basket normalised before the common start (latent bias) | Correct | Aligned first, then normalised |
| m2 | "To date" figures were not reproducible without a fixed cutoff | Correct | Cutoff fixed at 6-Nov-2026 |
| m3 | Pre-registration of A and C is unverifiable | Correct | Disclosed in the header |

No further review round was run after these fixes.

---

*Files: `pag_distressed/run_follow_backtest.py`, `pag_distressed/paper_portfolio.py`, `pag_distressed/data/follow_backtest_results.csv`, `pag_distressed/data/paper_portfolio_start.csv`, `pag_distressed/data/paper_portfolio_log.csv`.*

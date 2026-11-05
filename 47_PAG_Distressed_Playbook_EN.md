---
layout: default
title: "PAG's Distressed-Asset Playbook: Wanda, Evergrande Services, the 2005 Big-Four Bank Reform and Japan"
---

# 🏦 PAG's Distressed-Asset Playbook: Wanda, Evergrande Services, and the Big-Four-Bank / Japan Analogs

*November 5, 2026 — VLCC Analysis Series #47 (Chinese version: #48)*

> **Disclaimer**: research only, not investment advice. Tags:
> - **[P]** primary source, read directly.
> - **[P†]** primary document cited page-by-page by the gpt-6-astra review, not re-read by the author.
> - **[S]** secondary summary.
> - **[U]** unverified.
> - **[E]** author's estimate.
>
> Market data are Yahoo Finance closes to 4-Nov-2026. `python pag_distressed/run_model.py` reproduces the core computed numbers: Wanda proxies, 6666 deal maths and P/Es, the sensitivity grid, the mall-stack algebra, the bank per-share prices and the Mitsui multiples. Simple ratios quoted from sources are not re-computed. Sources are in [`pag_distressed/data/sources.csv`](pag_distressed/data/sources.csv).
>
> **Scope**: this is a deal-strategy study, not a stock initiation. §8 gives a sensitivity grid for 6666.HK, not a target price.
>
> **Revision**: v2 after a gpt-6-astra review that rated v1 **"not safe to publish"** (9 blocking issues). §11 lists every finding and the action taken.

---

## Step 1 — Research Draft

**Core conclusion (stated as a hypothesis, not a proven rule)**

- **PAG's recent China deals are consistent with one pattern: buy operating cash flow from sellers under time or legal pressure, ring-fence what is acquired, and use structure (control, tranching) to shape the risk.**
  - This pattern has not been shown to drive returns. **No realised deal-level IRR or MOIC has been established from the sources reviewed.**
- **Whether these prices contain a distress discount is not established.**
  - Evergrande Services at the HK$0.8359 offer is **~7.8x FY2025 / ~7.5x trailing-12-month (TTM) attributable profit** [E, deal FX]. SOE-backed peers' Yahoo trailing P/E is 7.6–20.6x [P]. These figures are descriptive only: they are not normalised for period, growth, cash conversion or governance.
  - Competing explanations for the price:
    - seller pressure from the court liquidation;
    - weak cash conversion: H1-2026 operating cash flow was RMB 81.9m against RMB 517m of profit [P];
    - no dividend;
    - legacy related-party risk.
- **The 2003–06 big-four bank reform and Japan's 1998–2004 bank clean-ups used one template**:
  - The state first absorbed or ring-fenced bad assets (AMCs, Huijin recapitalisation, put-backs, defect warranties).
  - Foreign capital then bought stakes: in China, minority stakes at **about 1.2x book** (BOC/ICBC prospectus figures [P†]); in Korea and Japan, control.
  - China's investors gained liquidity at the IPO and exited later through secondary sales. KFB was sold to a trade buyer; Shinsei listed.
- **China property in 2026 lacks the state backstop of the bank template, and its exit route is untested.** Exits depend on:
  - consumer C-REITs (issue cap rates 5.4–5.6% [S]; eligibility of Wanda assets not established);
  - a Wanda IPO whose 2026 filing status is **unverified**;
  - the 6666 minority market.

**Supporting points (claim → evidence needed)**

1. *Sellers were under time or legal pressure* → dated deadlines and process documents. **Available**:
   - Wanda faced a redemption right if there was no IPO by end-2023; the new deal was signed 18 days before that deadline [P/S].
   - Evergrande Services' controlling block was sold by court-appointed liquidators in a competitive auction [P/S].
   - **Not available**: evidence that this pressure, rather than risk repricing, set the price.
2. *Separation from legacy losses varies by deal* → who keeps the legacy liabilities. **Available, deal by deal**:
   - **Documented state protection**:
     - Banks: 1999 RMB 1.4tn NPLs to AMCs [S]; Huijin US$45bn (Dec-2003) [S].
     - KFB: government absorbs bad loans found within 2 years [S].
     - LTCB: 3-year defect warranty on eligible claims [S].
   - **Corporate separation only**: Wanda 2024. Group debt sits at the parent [P/S]. Target-level debt, guarantees or security are **unknown**.
   - **None**: Evergrande Services is a share purchase, so the target keeps its liabilities. The RMB 13.4bn deposit loss is an accounting write-off, **not an indemnity** [S].
   - **Counterexample**: PAG entered Wanda in **2021, before** any clean-up.
3. *Structure allocates risk* → term sheets. **Partly available**:
   - 48 malls, as **planned and anonymously reported**: PAG ~RMB 5bn **first-loss** junior under ~RMB 45bn of mezzanine and senior claims [S]. This protects the lenders, not PAG.
   - 6666: the block purchase gives control; the later mandatory offer is an obligation, not protection [P].
   - 2024 Wanda governance and preference terms are **unknown**.

**Opposing points (claim → evidence needed)**

1. *China 2026 may resemble Japan 1991–2003 more than China 2005* → 48-mall NOI trend, C-REIT price/NAV, retail sales. **Mall NOI unknown.**
   - Mitsui Fudosan's listed shares troughed in April 2003, about 13 years after the bubble [P for the 2003 low; pre-2000 prices not retrieved].
   - This is an analogy; it cannot date China's bottom.
2. *The "discount" may be fair* → like-for-like peer comparison. **Partly available**:
   - 6666 at ~7.5–7.8x sits at the low end of SOE peers (Yahoo, unnormalised).
   - Its H1-2026 operating cash flow covered only 16% of profit (seasonal) [P].
   - 2021's ~34x headline Wanda proxy may have been the anomaly.

---

## 1. Wanda: from Pre-IPO investor to controlling-bloc owner

| Date | Event | Key numbers | Tag |
|---|---|---|---|
| Aug-2021 | Zhuhai Wanda Commercial Management (asset-light Opco) Pre-IPO; ~22 institutions incl. PAG, Tencent, Ant, CITIC Capital | ~RMB 38bn for 21.17% (denominator includes management holders). PAG US$2.8bn = **US$1.9bn equity + US$933m syndicated loan** (Reuters). Redemption right if no IPO by end-2023 | [P]/[S] |
| 12-Dec-2023 | PAG–Wanda new agreement | 2021 investors redeemed and reinvest. Wanda's stake **78.83% → 40%** (another source says 70.15%: direct vs indirect definitions not reconciled) | [P]/[S] |
| 30-Mar-2024 | PAG, CITIC Capital, Ares, ADIA (Platinum Peony), Mubadala sign into Dalian Xindameng (new holding company) | **~RMB 60bn for 60%**; reportedly **no IPO undertaking** | [S] |
| May-2025 | SAMR clears JV to buy **48 Wanda Plazas** | Reported RMB 50bn; **planned** stack ~5bn PAG junior / ~15bn mezzanine / ~30bn bank syndicate (anonymous sources). Membership conflicts: Gaohe (SAMR) vs Taikang (Mingtiandi) | [S] |
| Jan-2026 | Wanda US$400m 11% bond (due Feb-2026) extended to Feb-2028 | Stated repayment sources: disposals, operating cash and Opco dividends | [S] |
| Jul-2026 | PAG-led "Shanghai Anya" vehicle takes Zhanjiang plaza | Market tally: >80 plazas sold since 2023 | [S] |

**Headline proxies, not a like-for-like markdown** (`run_model.py` §A) [E]:

| Round | Headline proxy for 100% | Profit basis | Implied P/E | Yield |
|---|---|---|---|---|
| 2021 | ~RMB 179bn (38/0.2117) | 2021 NPAT 5.3bn (actual) | ~34x | ~2.6% |
| 2024 | ~RMB 100bn (60/0.60) | 2023E NPAT 9.5bn (**estimate** in the Dec-2023 announcement) | ~10.5x | ~8.5% (on 2023E dividend) |

- The two figures differ by about **−44%**, but they are **not comparable**:
  - The entities differ (Zhuhai Wanda vs the new Xindameng holding company).
  - Redemption proceeds were reinvested.
  - Preferences, performance compensation, debt and the primary/secondary split are not reconciled.
- So this is **not** evidence of a 44% distress discount on unchanged assets.
- **The PAG ticket cannot be reconciled.**
  - Reuters splits PAG's US$2.8bn into US$1.9bn of equity plus a US$933m loan.
  - That does **not** show that only US$1.9bn was consideration for the stake: the loan may have funded PAG's acquisition vehicle.
  - So the 1.9/6.4285% ratio (~US$29.6bn) is a funding/stake ratio, **not a valuation**.

**What PAG has, on public facts**:
1. In the 2024 holding company, PAG and its co-investors hold 60% of the Opco group's holding company.
2. PAG is in a separate JV with other partners that is buying 48 malls Wanda continues to operate. PAG was **reported (anonymously) to plan** taking the first-loss junior; final funding is **unverified**.
3. The Opco's fees are an expense of the Propco. Different PAG funds and co-investors have different economics, so "owning both sides" is **not automatically** extra profit for PAG.

---

## 2. Evergrande Property Services (6666.HK): a conditional purchase from liquidators

**Deal terms** (joint announcement, 30-Oct-2026) [P]:

| Item | Value |
|---|---|
| Buyer | Everest Holdings I Ltd (PAG). Funding: acquisition debt + **PAG Fund IV** equity [S] |
| Sellers | China Evergrande, 147.2m shares (1.361%) at **HK$0.8359**; CEG Holdings, 5,368.1m shares (49.655%) at **HK$0.7271**. Both act via liquidators |
| Block | **51.016% for HK$4.026bn** |
| Side payment | **RMB 500m** for CEG Holdings' taxes, fees and liabilities. At the announcement's **HK$1 = RMB 0.85621** (PBOC, 28-Oct) this is HK$584.0m, making CEG Holdings' effective price HK$0.83589 ≈ 0.8359 |
| All-in for control [E] | **HK$4.610bn ≈ HK$0.8359/share** |
| Conditions | **Not yet complete.** SAMR merger filing is a non-waivable condition. The unconditional cash offer at **HK$0.8359 ("will not be increased")** arises **after completion** |
| Stated intentions | PAG intends to **maintain the listing**, **not use compulsory-acquisition powers**, and restore public float if needed [P] |
| Offer vs market | −29.5% vs the HK$1.185 last close; −9.1% vs HK$0.920 on 10-Sep-2025 |
| Process | Competitive auction; Guangdong Tourism Holding also bid [S] |

**Financials** [P, FY2025 results and H1-2026 interim report]:

| RMB m | FY2025 | H1-2026 |
|---|---|---|
| Revenue | 13,680 | 6,940 [S] |
| Profit attributable | 986.6 | 517.0 (H1-2025: 472.3) |
| Operating cash flow | — | **81.9** (H1-2025: −326.2) |
| Cash and cash equivalents | 4,189.5 | **3,691.7** |
| Restricted cash (separate line) | 120.9 | 127.6 |
| Contract liabilities | 2,623.7 | 2,317.0 |
| Net current assets | 87.5 | 645.2 |

- TTM attributable profit is **RMB 1,031.3m** [E].
- Cash fell RMB 498m in H1-2026, but the company also reports **RMB 425m of financial assets at fair value**. Total available funds were ~RMB 4.24bn vs ~4.31bn, down only ~RMB 66m [P]. Distributability is still not established.
- About RMB 510m a year of services to Evergrande's idle units is **not recognised as revenue** [P].
- The RMB 13.4bn deposits seized in 2022 were lost [S].

**Pricing** (`run_model.py` §B) [E]:

| Price point | FX (RMB per HK$) | P/E FY2025 | P/E TTM |
|---|---|---|---|
| Offer HK$0.8359 | 0.85621 (deal) | **7.84x** | **7.50x** |
| 4-Nov close HK$0.945 | 0.85009 (4-Nov) | 8.80x | 8.42x |

**Peers** (Yahoo trailing P/E on 4-Nov; periods, FX and impairment treatment **not normalised**) [P]:

| Ownership | Company | Trailing P/E |
|---|---|---|
| SOE-backed | Poly Services 6049 | 8.5x |
| SOE-backed | China Overseas Property 2669 | 7.6x |
| SOE-backed | China Resources Mixc 1209 | 20.6x |
| Private | Country Garden Services 6098 | 26.6x (depressed earnings) |

- **Withdrawn**: the v1 "4.0x ex-cash P/E" margin-of-safety claim.
  - Net current assets are only RMB 645m.
  - The cash funds customer prepayments and payables.
  - Distributable surplus is **not established**.
- **Market signal**: 6666 closed at HK$0.945 on 4-Nov, **above** the future offer price. Why the market pays more is **unknown**.

---

## 3. The business logic of large distressed-asset deals

### 3.1 The return equation (a framework, not a measurement)

`Return = entry price vs intrinsic value + (cash yield − funding cost) × time + exit re-rating − legacy leakage − fees and taxes`

| Lever | Wanda Opco (2024) | 48 Wanda Plazas | Evergrande Services |
|---|---|---|---|
| Seller pressure | End-2023 IPO redemption | Group debt, bond maturities | Court liquidation |
| Ring-fencing | Opco only; debt stays at parent | Asset-level SPVs (details unknown) | Share purchase. Target liabilities remain; no indemnity known |
| Cash yield | 8.5% on 2023E dividend [E] | NOI − interest (unknown) | Profitable; no dividend; weak H1 cash conversion |
| Risk allocation | Unknown | Planned: PAG **first loss** below ~45bn of claims (final funding unverified) | Control via block; the offer is an obligation |
| Exit route | IPO (not promised; 2026 status unverified), trade sale | C-REIT (eligibility not established), asset sales | 6666 stake sale; listing to be maintained |

### 3.2 Hypothetical fixed-priority stack for the 48 malls [E]

- **Inputs**: the reported, **planned** stack (50 = 5 junior + 15 mezzanine + 30 senior). Whether the mezzanine is debt is unverified.
- **NOI is not disclosed.** The 6–8% figure in the press is an analyst's estimate of **annual return**, not an acquisition cap rate.
- **Excluded**: capex, leasing costs, fees, tax, amortisation and holding period.
- This is algebra, **not** an estimate of PAG's return.

| Hypothetical NOI yield | Exit cap 5.0% | Exit cap 5.5% | Exit cap 6.5% | Exit cap 8.0% |
|---|---|---|---|---|
| 5% (RMB 2.5bn) | 1.00x | 0.09x | 0.00x | 0.00x |
| 6% (RMB 3.0bn) | 3.00x | 1.91x | 0.23x | 0.00x |
| 7% (RMB 3.5bn) | 5.00x | 3.73x | 1.77x | 0.00x |

- **Leverage**: assets / junior = **10x**; claims / junior = **9x**; bank debt / value = **60%**.
- At an unchanged cap rate, a **10% fall in NOI** wipes out the junior tranche. So this is a trade on **both rent and cap rate**.
- **C-REIT benchmark**:
  - Consumer C-REITs issued at 5.36–5.55% cap rates (CR Mixc, Yinli, Jinmao) [S].
  - They paid 2025 cash yields of 3.7–5.2% [S].
  - Eligibility under NDRC rules depends on the sponsor, title, encumbrances, compliance and use of proceeds. It is **not established** for these malls.

---

## 4. Analog 1 — the big-four bank reform (1998–2006)

**Sequence: clean first, sell second** [S]:

| Year | Step | Size |
|---|---|---|
| 1998 | Special treasury bonds recapitalise the big four | RMB 270bn |
| 1999 | NPLs moved **at book value** to Cinda / Huarong / Orient / Great Wall | ~RMB 1.4tn |
| Dec-2003 | Huijin injects FX reserves into BOC and CCB | US$45bn (RMB 372.5bn) |
| 2004–05 | Second-round NPL disposals | ~RMB 779bn |
| Apr/May-2005 | Huijin US$15bn into ICBC; ICBC strips RMB 246bn of loss assets | |
| Jun-2005 → Jan-2006 | Strategic investors enter | |
| Oct-2005 / Jun-2006 / Oct-2006 | CCB / BOC / ICBC IPOs | CCB IPO at 1.96x book [S] |

**Strategic investors** (prospectus figures [P†] where available):

| Bank | Investor | Terms | Outcome |
|---|---|---|---|
| BoCom (2004) — not a big-four bank | HSBC | 19.9% at RMB 1.86 (1.76x year-end-2003 book) | Still held as of 2013 — **genuinely strategic** |
| CCB (Jun-2005) | Bank of America | **US$2.5bn pre-IPO + US$0.5bn at IPO**, 9% | Options exercised in 2008. Reported pre-tax gains incl. US$7.3bn (May-2009). Fully out Sep-2013 [S]. **Entry price per share withdrawn**: the newspaper figure is not reconciled to the deal documents |
| CCB (2005) | Temasek | US$1.466bn for 5.1% [S] | — |
| BOC (2005) | RBS consortium (RBS, Merrill Lynch, Li Ka-shing) | Consortium: US$3.048bn for 20.94bn shares ≈ **US$0.1455/share, 1.17x 2004 book** [P†] | RBS itself sold its remaining 4.26% on 13-Jan-2009 |
| BOC (2005) | Temasek | 10% proposed; **~5% implemented** (4.80% pre-IPO, US$1.524bn, plus US$0.5bn at IPO) [P†] | — |
| BOC (total) | 4 investors | ≈US$5.137bn for ≈16.19% pre-IPO [P†] | UBS sold Dec-2008 |
| ICBC (Jan-2006) | Goldman Sachs | US$2,582.2m for 16.48bn shares ≈ **RMB 1.2586/share, 1.22x P/B** [P†] | **US$10.1bn gross proceeds** from six sales to May-2013, a **3.9x gross proceeds/cost ratio** — not net profit or fund return [S] |

**Lessons**:
1. **The state absorbed the losses first.** Investors bought recapitalised banks, not NPLs, and the AMCs' later losses (Huarong 2021) fell on the state.
2. **BOC and ICBC entry was at about 1.2x book, not below book.** The IPO gave liquidity; actual exits were later secondary sales. Returns came over 3–8 years, from a mix of IPO valuations, credit growth, regulated margins and RMB appreciation. Their shares are **not decomposed**.
   - **Withdrawn**: v1's "+70% re-rating in four months". The book dates and bases differed, and IPO value was not immediately realisable.
3. **Most "strategic" stakes became financial** (2008–13 sales for the investors' own capital needs). **HSBC/BoCom is the exception.**
4. **The "selling cheap" (贱卖) debate**: Ba Shusong argued that few bidders came in 2003–05, and RBS shares fell 15% on its BOC announcement [S].

---

## 5. Analog 2 — Japan and Korea: banks bought with put-backs, and Mitsui Fudosan's listed recovery

**Distressed banks bought with put-backs** [S]:

| Deal | Entry | Downside protection | Exit |
|---|---|---|---|
| Korea First Bank (Newbridge, 1999) | 51% for **KRW 500bn (~US$417m)** | Government absorbs bad loans found within 2 years | StanChart paid **US$3.3bn for 100%** (2005). Newbridge's ~48.6% fetched ~KRW 1.65tn, a **~3.3x gross won** ratio; net fund return unknown |
| LTCB → Shinsei (Ripplewood-led, Mar-2000) | ¥121bn (¥1bn shares + ¥120bn capital) | 3-year defect warranty on **eligible acquired claims** that fell ~20%+ (not a blanket loss guarantee) | Listed 19-Feb-2004; political backlash over the warranty |
| Shenzhen Development Bank (Newbridge, 2004) | ~17.9% stake | — | Swapped into Ping An shares in 2010; ~US$2.4bn and "16.5x" reported [S, not verified] |

**Mitsui Fudosan — a listed quality landlord's equity recovery, not a distressed acquisition** [P prices; S narrative]:

| Phase | Data (8801.T, split-adjusted Yahoo closes, nominal, price only) |
|---|---|
| Asset deflation | Land prices collapse after 1991 [S]; pre-2000 share prices **not retrieved** |
| Trough | **¥196.00 on 11-Apr-2003** (Japan's bank crisis) |
| Capital recycling | J-REIT law Nov-2000; the Mitsui-sponsored Nippon Building Fund was among the first J-REITs in 2001 [U] |
| Peak | **¥1,303.33 on 4-Jun-2007 = 6.65x** the trough |
| Crash | ¥356.67 on 20-Nov-2008 (**−73%**) |
| Governance | Elliott (Feb-2024) demanded a ¥1tn buyback and an Oriental Land sell-down [S]. Mitsui's own plan: ROE ≥10% around FY2030; **total payout ≥50%** (dividend payout ~35%); cut strategic shareholdings ~50% over FY2024–26 [P†]. This is not Elliott's full proposal |
| Long run | ¥2,147.50 on 12-Feb-2026 = 11.0x the 2003 low |

**Caveat**: a perfectly timed trough-to-peak in a listed share is **not** an achievable investment return, and it says nothing about asset-level recovery.

**PAG's Japan link**:
- PAG's real-assets arm descends from Secured Capital Japan (founded Sep-1997) [P, PAG profile].
- In 2009 PAG agreed to invest **up to ¥4.5bn (US$46m) in convertible bonds**, with ¥3bn paid initially [S]. The resulting equity percentage is **unverified**.

---

## 6. Synthesis — the observed PAG / foreign-capital playbook

*These are observed patterns, not proven causes of return.*

| # | Pattern | Banks 2005 | KFB / LTCB | Wanda | Evergrande Services |
|---|---|---|---|---|---|
| 1 | Buy from a seller under time or legal pressure | IPO timetable | State-owned seller | End-2023 redemption | Liquidators |
| 2 | Legacy losses carried by someone else (documented?) | Yes: AMCs + Huijin | Yes: put-back / warranty | Partly: group debt at parent; target-level recourse unknown | **No**: target keeps its liabilities; no indemnity |
| 3 | Buy current cash flow | Partial | — | 8.5% on 2023E dividend | Profit yes, cash conversion weak |
| 4 | Control or blocking stake ("with control, exit is never an obstacle" — Shan, a claim [S]) | Minority | 51% | Bloc 60% | 51% (on completion) |
| 5 | Keep the operator | — | Management replaced | Wanda operates | Listed Opco |
| 6 | Local and sovereign co-investors | Temasek | — | Tencent, JD, ADIA, Mubadala, CITIC | — |
| 7 | Tranching | — | — | PAG is **first loss** (planned) | Acquisition debt |
| 8 | Capital-market exit | IPO | Trade sale / IPO | IPO or C-REIT (unproven) | Stake sale (listing kept) |

**Strategy summary** (prescriptions suggested by the pattern; none is proven to produce returns):
- Identify sellers with binding constraints. An IPO timetable or state ownership alone does not prove pressure.
- Seek contractual protection against legacy losses where it can be obtained. Corporate separation alone is weaker.
- Take governance rights.
- Bring local or sovereign co-investors. Their presence identifies who invested; it does not prove political protection.
- Plan the exit before entry.

**What the pattern does *not* show**:
- that PAG has outperformed on these deals;
- if it has, whether structure or local and political partners explain it;
- that its 2021 Wanda entry made money.

---

## 7. Where the analogies break

| Factor | China banks 2005 | Japan 2001–03 | China property 2026 |
|---|---|---|---|
| State backstop | Explicit (Huijin, AMCs) | Explicit (put-backs; 2003 Resona injection [S]) | **No direct recap of Wanda or Evergrande** |
| Growth | ~10% **real** GDP | Deflation | Low inflation; mall rents unknown |
| Exit window | IPOs | J-REITs from 2001 | C-REITs from 2024 (eligibility case by case); Wanda IPO unproven |
| Political risk | "Selling cheap" debate | "Vulture fund" debate | Foreign-capital sensitivity |
| Buyer protection | Pre-cleaned balance sheets | Contractual put-backs | Perimeter carve-outs only |

---

## 8. 6666.HK sensitivity (replaces v1's scenario table)

**Withdrawn**: v1's bear/base/bull values, the 50% payout assumption and the special-dividend case. Distributable cash is not established.

The grid below shows **share price = TTM EPS (HK$0.1122 at 4-Nov FX) × P/E**, with no dividends (`run_model.py` §B) [E]. Percentages are vs the HK$0.945 close.

| EPS change | 6x | 7.5x | 9x | 11x |
|---|---|---|---|---|
| −20% | 0.54 (−43%) | 0.67 (−29%) | 0.81 (−14%) | 0.99 (+5%) |
| −10% | 0.61 (−36%) | 0.76 (−20%) | 0.91 (−4%) | 1.11 (+18%) |
| 0% | 0.67 (−29%) | 0.84 (−11%) | 1.01 (+7%) | 1.23 (+31%) |
| +10% | 0.74 (−22%) | 0.93 (−2%) | 1.11 (+18%) | 1.36 (+44%) |

**Reading the grid**:
- At HK$0.945, the market is pricing roughly 8.4x TTM earnings. Upside needs a re-rating towards 9–11x or EPS growth.
- No 12- or 24-month target is given: the payout policy is unknown.
- The offer is **not yet executable**. It needs completion, including SAMR clearance.

**Watch list**:
- completion and the composite offer document;
- PAG's dividend policy;
- receivable impairments;
- full-year cash conversion;
- any new related-party exposure.

---

## 9. Day1Global (condensed, applied to the 6666 control deal)

- **Module C (cash flow)**:
  - H1-2026 operating cash flow RMB 81.9m vs RMB 517m of profit (seasonal).
  - Cash fell from RMB 4.19bn to RMB 3.69bn, with RMB 425m moved into financial assets; total funds fell ~RMB 66m. No dividend. Grade **C**.
- **Module L (ownership)**: PAG ~51% (Fund IV plus acquisition debt) on completion; liquidators exit. A leveraged buyer may favour upstreaming cash, but this is **unproven**. Grade **B−**.
- **Module O (accounting)**:
  - RMB 510m/yr of services is not recognised.
  - Legacy RMB 13.4bn loss; risk on related-party receivables. Grade **C**.
- **Six perspectives**:

  | Perspective | View |
  |---|---|
  | Buffett | Recurring fees, thin moat |
  | Baillie Gifford | No 10x case |
  | Tiger Cubs | Mispricing would need a catalyst: distributable cash, earnings growth or lower perceived risk |
  | Klarman | Margin of safety **not demonstrated** (ex-cash claim withdrawn) |
  | Tepper/Ackman | Catalysts: completion, first dividend |
  | Druckenmiller | Sector multiples depressed; no macro tailwind identified |

- **Anti-bias**:
  - Survivorship: winners are cited (Goldman/ICBC, SDB); 2005–07 Japan property funds are under-sampled.
  - Narrative: "PAG = smart money" is not evidence.
  - Anchoring: the −90% from IPO is irrelevant.
  - Hindsight: Mitsui's extrema are perfectly timed.
- **Pre-mortem** (one year later, down 40%) — qualitative; v1's probabilities were withdrawn as unsupported:
  1. No payout; cash retained.
  2. A new legacy claim.
  3. Sector de-rating.
  4. SAMR delay or deal failure.

---

## 10. Repo-rule applicability

- **Applied**:
  - bilingual output, sources CSV and a reproducible script (computed numbers only);
  - Rule 4 cross-checks (source conflicts flagged);
  - Rule 6 leverage (§3.2);
  - Day1Global (§9).
- **Partly applied**:
  - The Japan cycle is shown for 2003 → 2007 → 2008.
  - **No rent series, so no R² or lead/lag** analysis.
  - **No inflation adjustment** (CRule 9).
- **Rule 5 (multi-model)**: not run; one gpt-6-astra review instead (§11).
- **Rule 7 (target prices)**: deliberately not given (§8).

---

## Step 2 — Strict Peer Review (of the Step-1 draft)

**1. Facts that need verification**
- The 48-mall stack (5/15/30) is planned and anonymously sourced. Membership conflicts (Gaohe vs Taikang).
- The PAG 2021 ticket (US$1.9bn equity) vs the round total does not reconcile.
- The "12% redemption interest" comes from a single source.
- CCB per-share entry price.
- Temasek CCB terms.
- The SDB "16.5x".
- NBF listing date.
- Secured Capital conversion terms.
- 6666 distributable cash.
- Completion timing and SAMR outcome.

**2. Logical leaps / equivocation**
- "Seller pressure" is inferred from a context, not measured against risk repricing.
- "Strategic investor" (minority bank stakes) and "control buyer" (PAG) are compared as one class.
- Separation from legacy liabilities is treated as one category, although state protection, corporate separation and a plain share purchase differ.
- A listed-share recovery (Mitsui) is used as an analogy for private distressed real-asset returns.

**3. Missing counterexamples / competing explanations**
- PAG's own 2021 Wanda entry, before clean-up.
- Japan 2005–07 vintage property funds.
- BBVA/CITIC options exercised above market.
- Huarong's 2021 losses.
- Local or political sponsorship as the real edge.
- 6666 trading above the offer because of thin float or arbitrage.

**4. Most important primary sources to add**
- 6666 composite offer document.
- SAMR filing; Xindameng articles of association / shareholder agreement.
- Wanda bond prospectuses.
- CCB/BOC/ICBC prospectuses (re-read by the author).
- BofA/Goldman/RBS annual reports.
- Shinsei 2004 IPO prospectus.
- Mitsui FY1990–2003 annual reports.
- Any C-REIT filing for Wanda-type assets.

**5. Sentences that can at most be classified as speculation**
- All five prescriptions in the §6 strategy summary.
- "A leveraged buyer may favour upstreaming cash."
- Everything in §3.2 and §8.
- "China 2026 may resemble Japan 1991–2003."

---

## 11. gpt-6-astra adversarial review — findings and actions

Verdict on v1: **"not safe to publish"**, with 9 blocking issues. Spot-checks by the author against primary PDFs:
- deal FX 0.85621 — **confirmed** (EN joint announcement);
- the listing / no-squeeze-out intention — **confirmed**;
- H1-2026 cash, operating cash flow and profit — **confirmed** (interim report).

| # | Finding | Verdict | Action |
|---|---|---|---|
| B1 | Side payment converted at the 31-Dec-2025 NAV-date FX (0.90322) instead of the deal FX (0.85621); all-in HK$4.58bn wrong | **Correct** | Deal FX used; all-in HK$4.610bn; P/E 8.3x → 7.84x (FY2025) / 7.50x (TTM) |
| B2 | Wanda "−44%" is not a like-for-like distress discount (different entity, reinvestment, 2023E estimates, 70.15% vs 78.83% stake definitions) | **Correct** | Removed from the core conclusion; relabelled as headline proxies; caveats added |
| B3 | "4.0x ex-cash P/E" is not a surplus-cash multiple; H1-2026 data omitted | **Correct** | Withdrawn; H1-2026 balance sheet and cash flow added |
| B4 | Mall table: the 6–8% is an analyst's return estimate, not a cap rate; PAG is first loss; "not a rent trade" is wrong | **Correct** | Rebuilt as hypothetical algebra; first-loss wording; 10% NOI sensitivity added |
| B5 | Bank entry prices and the "+70% re-rating" are unsupported or wrong; the BofA "conflict" is really US$2.5bn + US$0.5bn | **Correct** | Prospectus figures used [P†]; CCB per-share price and +70% withdrawn; Temasek BOC fixed to ~5%; RBS exit dated |
| B6 | CR Mixc is SOE-backed, not private; peers not normalised | **Correct** | Reclassified; unnormalised basis disclosed |
| B7 | Scenario table assumptions unsupported and not reproduced by the script | **Correct** | Withdrawn; replaced with the EPS × multiple grid in `run_model.py` |
| B8 | Deal is conditional; the offer comes after completion; PAG intends to keep the listing and not squeeze out; float rules misstated | **Correct** | §2/§8 rewritten; privatisation pre-mortem removed |
| B9 | The core thesis is stated as a universal; PAG's 2021 Wanda entry contradicts "enter only after clean-up" | **Correct** | Restated as a hypothesis with counterexamples |
| m1 | KFB: US$3.3bn was for 100%; Newbridge ~3.3x gross, not "6x" | Correct | Fixed |
| m2 | Mitsui: dates; total payout vs dividend payout; "turnaround" equivocation | Correct | Fixed; relabelled as a listed-equity recovery |
| m3 | Secured Capital: CB up to ¥4.5bn, ¥3bn paid; "40%" not verified | Correct | Fixed |
| m4 | "Nominal growth" row contained real GDP growth | Correct | Fixed |
| m5 | BoCom / SDB are not big-four banks | Correct | Labelled |

**Not independently re-read by the author**: the bank prospectus page figures and the Mitsui plan figures cited by the reviewer, tagged [P†]. The reviewer **could not verify any 2026 Wanda IPO filing**, so its status is recorded as unverified.

**Confirmation round on v2** — verdict **"publish with fixes"**.
- Arithmetic independently re-checked: 4-Nov FX 0.85009, TTM EPS HK$0.1122, every P/E, the grid and the mall algebra are correct. B1, B2, B3, B5, B7 and B8 are resolved.

| # | Remaining finding | Verdict | Action |
|---|---|---|---|
| C1 | "Not fire-sale prices" is unsupported by unnormalised peers (B6 residual) | Correct | Withdrawn; replaced with "whether a distress discount exists is not established" |
| C2 | Planned mall financing still stated as fact in §1 and §3.1 (B4 residual) | Correct | Made conditional throughout |
| C3 | Ring-fencing asserted as universal; "no realised return" unsupported (B9 residual) | Correct | Split into documented protection / corporate separation / none; return-status wording narrowed |
| C4 | US$1.9bn/6.4285% presented as a valuation | Correct | Relabelled as a funding/stake ratio, not a valuation |
| c5 | TTM rounding (1,031.3m); RMB 425m financial assets omitted; "1.2x book" scope; IPO ≠ exit; BOC row mixes consortium and RBS; "CEG" naming; "repaid" wording; source register lagging; reproducibility claim too broad; "mispricing only if" too exclusive | Correct | All fixed; `sources.csv` rows S34–S43 added |

No further review round was run after these wording-level fixes.

---

*Files: `pag_distressed/run_model.py`, `pag_distressed/data/sources.csv`.*

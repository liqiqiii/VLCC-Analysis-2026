---
layout: default
title: "PAG's Track Record and Playbook: Case Studies, and Is It a Mitsui Fudosan?"
---

# 🧭 PAG's Track Record and Playbook: Case Studies, Wanda / Evergrande, and the Mitsui Fudosan Question

*November 6, 2026 — VLCC Analysis Series #49 (Chinese version: #50). Follows [#47](47_PAG_Distressed_Playbook_EN.md).*

> **Disclaimer**: research only, not investment advice.
>
> **Tags**:
> - **[P]** primary source, read directly.
> - **[S]** secondary summary.
> - **[U]** unverified or company-sourced claim.
> - **[E]** author's arithmetic.
>
> **Reproduce**: `python pag_distressed/run_track_record.py` reproduces the computed multiples. Sources are rows S44–S61 of [`pag_distressed/data/sources.csv`](pag_distressed/data/sources.csv).
>
> **Caveats**:
> - All "x" multiples are **gross deal-level** ratios of reported entry and proceeds. They are not fund returns.
> - KFB and SDB are **Weijian Shan's Newbridge deals before PAG**. They show his method, not PAG's returns.
>
> **Revision**: v2, after a gpt-6-astra review rated v1 **"not safe to publish"** (4 blockers; see §7).

---

## Step 1 — Research Draft

**Core conclusion**

- **PAG and Mitsui Fudosan run different business models.**
  - Mitsui Fudosan is a listed company with permanent capital. It develops, owns, operates and sponsors REITs for decades.
  - PAG's private-equity and real-assets arms invest through **closed-end funds** that must exit within a fund life. PAG also has a separate credit and markets arm.
- **PAG uses at least three distinct strategies.** It is not a single "bottom-fishing" playbook:

  | Strategy | Cases | Pattern |
  |---|---|---|
  | **A. Control / special situations** | Yingde, Goldin tower, Evergrande Services; Wanda, which moved from a redemption right to control | A seller under a clock or a dispute; buy control; fix the company; sell to long-term capital |
  | **B. Carve-out / roll-up** | Baosteel Gases (a profitable SOE unit, ROE >10%), DTZ → Cushman & Wakefield, Sapporo Real Estate | A non-core business released by a parent; consolidate it; exit by sale or IPO |
  | **C. Minority growth / co-investment** | China Music → Tencent Music, USJ, Lexmark | Back a recovering or growing asset; the exit depends on a strategic buyer or on contractual rights |

- **Wanda and Evergrande Services fit Strategy A.** They may also be assembling Mitsui-like *components*: a mall operator (Opco), a mall portfolio (Propco, planned) and a property-services platform. Whether PAG intends to build an integrated platform, or will sell the parts, is **speculation**.
- **Aggregate performance is not established.** Outcomes differ by case:
  - Tencent Music: a reported 19x gross [S].
  - Yingde: sold at a US$6.8bn EV, a **partial** exit [S].
  - Lexmark: contested; PAG's lifetime result is unknown.
  - Fund-level figures exist only as **unverified aggregator data** [U].

**Supporting points (claim → evidence needed)**

1. *Strategy A uses sellers under a clock or a dispute* → seller context for each deal. **Available [S]**:
   - Yingde: founder boardroom fight, 2016–17.
   - Goldin tower: sold by receivers after failed sales, 2023.
   - Wanda: IPO redemption deadline, 2023.
   - Evergrande Services: liquidators, 2026.
2. *PAG prefers control or contractual exit rights* → deal terms. **Available [S]**:
   - Control: Yingde ~98% acquired; Baosteel Gases 51%; Evergrande Services 51% (conditional); Sapporo Real Estate staged to 100% with KKR.
   - Contractual exit rights: Lexmark, where PAG alleges Pantum failed to complete the agreed purchase of its exit interests; Wanda 2021 redemption right.
   - Shan's stated view: control lets the owner choose the exit.
3. *Exits often go to strategic or long-term buyers* → buyer identity. **Available [S]**:
   - USJ → Comcast.
   - China Music → Tencent.
   - AirPower industrial gases → a Chinese consortium of insurers and funds.

**Opposing points (claim → evidence needed)**

1. *Case selection is biased towards visible wins* → a full deal list with outcomes. **Unknown.** PitchBook counts ~170 investments and ~57 exits, and most outcomes are private.
2. *PAG's China real-estate bets may need Mitsui-length holding periods* → mall NOI trend, C-REIT eligibility, platform buyers. **Unknown.** A closed-end fund cannot hold indefinitely. Without a buyer within the fund life, PAG must extend the holding or sell at a discount.

---

## 1. Who PAG is

| Item | Fact | Tag |
|---|---|---|
| Origins | Pacific Alliance Group: a hedge fund founded in 2002 (Chris Gradel, Horst Geicke); now PAG's Credit & Markets arm | [S] |
| Real Assets | Grew out of **Secured Capital Japan** (1997, Jon-Paul Toppino); TSE-listed in 2004; PAG took it over in 2009–10 | [S] |
| Private Equity | Started in July 2010 by **Weijian Shan**, formerly of Newbridge/TPG (KFB, SDB) | [S] |
| Brand / backer | Renamed PAG in 2011; Blackstone minority stake in 2018 | [S] |
| Size | ~US$55–60bn AUM; private equity ~US$21bn | [S] |
| Fund figures (aggregator, **unverified**) | PAG Asia I (2012): ~17% net IRR, 1.80x TVPI, 1.75x DPI (as of 30-Sep-2025). II (2016): ~9% / 1.60x / 0.99x. III (2019): ~9% / 1.40x / 0.37x (as of 31-Dec-2025). Seedtable, citing CalPERS/WSIB; the raw LP rows were not checked. **Not benchmarked** against vintage peers | [U] |

**Shan's stated rules** (NBD interview, Jun-2026) [S]:
- "Cheap" is a hindsight label.
- Underwrite the exit at a **lower** multiple than entry (buy at 10x, assume 8x).
- A minority investor waits for an IPO; a controlling owner chooses when and to whom to sell.

These are **stated policies**. Their execution across PAG deals is not demonstrated here.

---

## 2. Case studies

### Case 0 — Before PAG: Shan at Newbridge (KFB, SDB) — the method, not PAG returns

| | Korea First Bank (1999→2005) | Shenzhen Development Bank (2004→2010) |
|---|---|---|
| Seller | Korean government after the Asian crisis | Shenzhen state shareholders |
| Entry | 51% for KRW 500bn | ~17.9% |
| Protection | 2-year government put-back of bad loans | — |
| Exit | 100% sold to StanChart for US$3.3bn. Newbridge's ~48.6% fetched ~KRW 1.65tn, **3.3x gross** | Swapped into Ping An shares; ~15x (Shan) / 16.5x (PEI) |
| Tag | [S] | [S] |

### Case 1 — Universal Studios Japan (2013→2017) — Strategy C

- **Entry**: PAG invested ¥25bn (US$242m) in Dec-2013 alongside Goldman, MBK and Owl Creek [S]. Whether these were new or existing shares, and PAG's stake, are **unknown**.
- **Operations**: the operating turnaround, including the Harry Potter area opened in 2014, was already under way.
- **Exit**: Comcast bought 51% in 2015 (EV about ¥745–750bn), then the remaining 49% in 2017 for ¥254.8bn (EV about ¥840bn) [S].
- **PAG's return is unverified.** A company-sourced claim of "US$1.25bn, 9.42x" is inconsistent with itself: 1.25 / 0.242 = 5.2x [E/U].

### Case 2 — Yingde Gases + Baosteel Gases → AirPower (2017→2025) — Strategies A and B

| Step | Facts | Tag |
|---|---|---|
| Trigger | Founder boardroom fight (Nov-2016); impairment-driven loss in 2016 | [S] |
| Entry | 42.1% from founders for HK$4.7bn. Offer at HK$6.00 vs Air Products' non-binding HK$5.50; commitments for 98.11%. ~HK$11.3bn for 100% (~US$1.45bn) | [S]/[E] |
| Add-on (Strategy B) | 2018: 51% of **Baosteel Gases** (a profitable SOE unit) won at RMB 4.166bn, **2.13x the reserve price**, in a contested auction | [S]/[E] |
| Fix | PAG-appointed CEO; bolt-on acquisitions; merged into AirPower (2021) | [S] |
| IPO | 2021 Hong Kong filing did not proceed | [S] |
| Exit | Industrial gases sold at a reported **US$6.8bn EV** (agreed Nov-2024). PAG keeps ~25% plus clean energy (reported >US$2bn). A **partial** exit | [S] |
| Multiple | Aggregate transaction equity consideration ~US$2.06bn [E]. This is not PAG-funded capital; it excludes debt and co-investors. Exit equity is **not disclosed**, so "8x" talk is **not reproducible** | [U] |

### Case 3 — DTZ → Cushman & Wakefield (2014→2018) — Strategy B

- **Entry**: TPG, PAG and OTPP bought DTZ from UGL for A$1.215bn in 2014. It was a non-core business for its parent, not a distressed one.
- **Build**: added Cassidy Turley, then Cushman & Wakefield at a US$2bn EV (2015).
- **Exit**: NYSE IPO in 2018 [S].
- PAG's share and return are **unknown**.

### Case 4 — China Music → Tencent Music (2013→2021) — Strategy C

- PAG invested **US$137m** in 2013.
- China Music merged with Tencent's music arm (2016), which listed as TME (2018).
- Reported proceeds: **US$2.6bn, 19x gross** [S, one anonymous source].
- This was not a distressed deal.

### Case 5 — Lexmark (2016→2025) — Strategy C with contractual exit rights

- **Entry**: PAG paid **US$652m** for 42.94% of the JV (with Apex/Ninestar, now Pantum) that bought Lexmark at an EV of ~US$3.9bn [S].
- **Earlier partial exits**: repurchases had already cut PAG's stake to **32.02%** [S].
- **Shock**: Ninestar was put on the US entity list (2023), followed by impairments.
- **Sale**: Xerox closed the purchase on **1-Jul-2025** for **US$1.5bn, including net debt and assumed liabilities** [P]. That is −62% vs the 2016 EV [E].
  - A separately reported US$70.6m equity consideration is a **different valuation layer**, not a conflict.
- **Disputes**:
  - At HKIAC, PAG claims **≥US$689m**, **alleging** that Pantum failed to complete the agreed purchase of its exit interests [S].
  - Separately, in a Zhuhai court, Pantum's amended claim (Jul-2026) for **RMB 4.95bn** is in **tort** [S].
  - Neither has been adjudicated.
- **PAG's lifetime result is unknown.** The original cheque, earlier repurchases and the arbitration outcome are not reconciled.
- **Lesson**: contractual exit rights are worth only what can be enforced against the counterparty.

### Case 6 — Goldin Financial Global Centre (2023) — Strategy A, real estate

- PAG and Mapletree (50:50) bought the tower from receivers for **HK$5.6bn** [S/E]:
  - 18% below the HK$6.8bn secured debt;
  - 16% below a failed HK$6.7bn sale;
  - ~HK$6,316 per sq ft.
- Not exited. Hong Kong office rents have been weak since, so the outcome is **unknown**.

### Case 7 — Sapporo Real Estate (2025→2029) — Strategy B, Japan

- PAG and KKR agreed to buy Sapporo's property arm (Yebisu Garden Place) at a **¥477bn EV** [S].
- The equity transfers in stages: 51% in 2026, 29% in 2028, 20% in 2029.
- The seller faced pressure from the TSE's 2023 capital-efficiency push and from an activist, 3D Investment Partners [S].
- **Context**: Mitsui Fudosan faces the same pressure (Elliott, 2024) and is cutting cross-holdings. In 2020s Japan, PAG is a **buyer** of corporate real estate that listed owners are pressed to release.

### Case 8 — Wanda and Evergrande Services (2021→) — Strategy A, with a minority start

| Pattern | Wanda Opco | 48 malls | Evergrande Services |
|---|---|---|---|
| Seller under a clock | IPO redemption (2023) | Group deleveraging | Liquidators |
| Control or exit rights | 2021 redemption right → 60% investor bloc (2024) | JV; PAG first loss (planned) | 51% (conditional on SAMR) |
| Operator | Wanda keeps operating | Wanda keeps operating | Listed Opco; related-party clean-up expected |
| Exit candidates | IPO (not promised), trade sale | C-REIT (eligibility unproven), insurers in the JV | Stake sale; listing kept |

---

## 3. How the moves map to the cases

| Move | Applies to | Contradicted or not shown by |
|---|---|---|
| Seller under a clock or dispute | Yingde, Goldin, Wanda, Evergrande Services, Sapporo (activist) | TME, DTZ, Baosteel (a profitable SOE unit sold by auction) |
| Win on certainty, not only price | Evergrande Services (reported funding certainty) | Baosteel and Yingde: PAG paid **above** rivals |
| Underwrite multiple compression | Stated policy (Shan) | Not demonstrated case by case |
| Control or contractual exit | Yingde, Baosteel, Evergrande Services, Sapporo, Lexmark (contract) | USJ, TME (minority with no stated rights) |
| Fix and build | Yingde + Baosteel, DTZ + C&W | USJ (turnaround already under way) |
| Exit to strategic or long-term capital | USJ, TME, AirPower | DTZ (IPO); Goldin and Wanda (not exited) |
| Partners for scale and fit | DTZ (TPG/OTPP), Goldin (Mapletree), Sapporo (KKR), Wanda (Tencent, ADIA, CITIC) | — |

---

## 4. Is PAG "like Mitsui Fudosan"?

| Dimension | Mitsui Fudosan | PAG |
|---|---|---|
| Capital | Permanent, listed balance sheet | Closed-end funds (PE and real assets) with fund lives and LP clocks |
| Core activity | Develop, own, lease, sell to REITs, manage. Segments: Leasing / Property Sales / Management / Facility Operations [P] | Buy, fix or combine, **sell** |
| Development risk | Yes (urban redevelopment) | Generally avoided ("no land, no construction" [S]) |
| REITs | **Sponsor**, earning asset-management fees [P] | Possible future **seller into** C-REITs (not shown) |
| Japan 1998–2005 | A long-term owner that survived; stock low in Apr-2003. Its asset purchases in that period were **not examined** | Predecessor Secured Capital was a distressed-asset buyer [S] |
| Japan 2020s | **Under pressure** (Elliott: buybacks, cutting cross-holdings) | **Buyer** of carve-outs (Sapporo Real Estate) |

**Answer**:
- **The business model is different.** Mitsui's listed-share rebound from 2003 to 2007 (6.65x, #47) belonged to its shareholders, through a surviving balance sheet, policy easing and the new J-REIT market. That is not what PAG's funds do.
- **The closer Japanese analog is the 1998–2005 foreign opportunity funds**, including PAG's own predecessor Secured Capital, Lone Star and Goldman [S]. They bought from banks and distressed owners, then sold into the J-REIT and long-term-owner market as it formed.
- **In China, the long-term-owner role is plausibly played by SOE platforms, insurers and C-REIT sponsors.** China Resources' group, for example, owns malls and sponsors a C-REIT. CR Mixc Lifestyle (1209.HK) is its listed operating company.
  - The P/E gap between CR Mixc (~20.6x) and Evergrande Services (~7.5x) shows that the market values the two businesses differently. Their growth, assets and risks differ, so the gap does **not** show who will buy what.
  - Whether these players will buy PAG's assets is **speculation**.

---

## 5. Risks to this reading

| Risk | Evidence | Status |
|---|---|---|
| Survivorship | Only visible deals are covered; most of ~57 exits are private | Open |
| Fund data | Aggregator figures only; no vintage benchmark | Unverified |
| Counterparty / enforcement | Lexmark: HKIAC claim and separate tort suit | Pending |
| Political / regulatory | SAMR approval for 6666; scrutiny of foreign buyers | Pending |
| Exit market | AirPower's IPO failed and the business was sold to domestic capital instead; property exits untested | Open |
| Hong Kong office | Goldin tower bought in 2023; rents weak since | Unknown |

---

## 6. Day1Global framing (PAG as deal sponsor; no listed PAG security)

| Item | Assessment |
|---|---|
| Module L (alignment) | GP economics (fees and carry) favour exits within the fund life, not Mitsui-style holding |
| Module C (cash) | Strongest where a strategic or long-term buyer exists (USJ, TME, AirPower). Fund III's DPI is reported at 0.37x (unverified, not benchmarked) |
| Module O (accounting) | Headline multiples (19x, "8x", "9.42x") are gross or unverified |
| Buffett | The edge is process, access and partners — hard to measure as a moat |
| Baillie Gifford | Not applicable |
| Tiger Cubs | The edge is control and process, not cheapness |
| Klarman | Margin of safety is a stated underwriting rule, not demonstrated |
| Tepper | Catalysts: SAMR approval, a C-REIT exit, a strategic sale |
| Druckenmiller | China property's capital cycle is still contracting |

**Anti-bias**:
- Survivorship.
- Narrative ("king of bottom-fishing").
- Authority: media-attributed Shan book quotes are not verified [U].
- Attribution: Newbridge wins are not PAG returns.

**Pre-mortem** (qualitative): PAG's China property bets disappoint if:
1. mall NOI keeps falling;
2. C-REIT channels stay closed to these assets;
3. SAMR or politics delays the 6666 deal;
4. the fund clock forces sales at a discount.

---

## Step 2 — Strict Peer Review (of the Step-1 draft)

**1. Facts that need verification**
- TME 19x (one anonymous source).
- USJ: stake and proceeds.
- AirPower: exit equity.
- Raw CalPERS/WSIB fund rows.
- Lexmark: repurchase proceeds and cash flows.
- Which PAG fund holds which deal.
- 48-mall JV terms.
- Goldin tower's current value.
- Zhuhai Wanda's post-2024 financials (only an unverified 2025 revenue figure, ~RMB 28.5bn [U]).

**2. Logical leaps / equivocation**
- "Seller under a clock" can fit almost any deal, so it is only defined by the listed triggers.
- Lineage (Secured Capital) is used as evidence of current strategy.
- China Resources group vs CR Mixc: kept distinct.

**3. Missing counterexamples / competing explanations**
- PAG's private losses.
- Credit-side exposure to Chinese developers (not covered).
- Relationships and political access as the edge.
- Blackstone and KKR running the same Japan carve-out playbook.
- Mitsui's own 2000s acquisitions (not examined).

**4. Most important primary sources to add**
- CalPERS/WSIB performance reports.
- AirPower sale filings.
- The HKIAC award and the Zhuhai court rulings.
- Sapporo Holdings' TSE disclosure.
- Mitsui FY2002–07 annual reports.
- *Money Games* (to verify quotes).
- Zhuhai Wanda bond filings.

**5. Sentences that can at most be classified as speculation**
- "Mitsui-like components."
- SOEs, insurers or C-REITs as buyers.
- The pre-mortem.

---

## 7. gpt-6-astra adversarial review — findings and actions

The review was scoped to 12 web checks after two earlier attempts timed out. Verdict on v1: **"not safe to publish as written."**

| # | Finding | Verdict | Action |
|---|---|---|---|
| B1 | Lexmark: US$1.5bn (incl. net debt and liabilities) vs US$70.6m equity is not a conflict; PAG's stake was already 32.02%; Pantum's claim is a tort suit in Zhuhai, not an HKIAC counterclaim; the loss inference is unsupported | Correct | Fixed in the case, the script and the sources (S59, S60) |
| B2 | Fund data is from an aggregator and unverified; "average" is not benchmarked | Correct | Labelled [U] with as-of dates; "average" withdrawn |
| B3 | KFB/SDB are Newbridge deals, not PAG returns; gross and net were mixed | Correct | Moved to Case 0 and labelled; the script tags each case |
| B4 | "Mitsui did not buy distressed assets" is unsupported; China Resources group vs CR Mixc conflated; the P/E gap does not identify a buyer | Correct | Absolute claim removed; entities separated; P/E reframed |
| m1 | USJ "recap" and stake unknown; AirPower is a partial exit | Correct | Qualified |
| m2 | Lexmark close date 1-Jul-2025 | Correct | Fixed |
| m3 | The 7-move playbook is overfit (TME and DTZ are not distressed; Baosteel was profitable) | Correct | Replaced with three strategies and a move-to-case map (§3) |
| m4 | "No moat: deal flow depends on crises" is contradicted by the non-distressed deals | Correct | Reworded (§6) |

No further review round was run after these fixes.

---

*Files: `pag_distressed/run_track_record.py`, `pag_distressed/data/sources.csv` (S44–S61). Previous: [#47](47_PAG_Distressed_Playbook_EN.md).*

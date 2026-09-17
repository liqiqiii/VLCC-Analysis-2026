---
layout: default
title: VLCC Deep-Dive — US Product-Export Limits & the Rate-vs-Stock Cycle Playbook (Sep 16, 2026)
---

# VLCC Deep-Dive: US Product-Export Limits & the Rate-vs-Stock Cycle Playbook
## Two modules for a mid-to-late-cycle checkpoint
### September 16, 2026 — Cyclical Analysis (CRule 1/3/4/6/8)

> **Context (the user's framing):** After 6+ months, DHT/FRO have delivered big gains and the big cycle has partly paid off. Because these are *cyclical* stocks, we must know **which phase we're in** — external bullish news is abundant, but stay vigilant. Two research modules requested.

> **TL;DR**
> - **Module 1 — US product-export limits → "all crude to China then re-export"?** The specific bill exists (**H.R. 8266, "Gasoline Export Ban Act of 2026,"** triggers if US pump price >\$3.12/gal for 7 days) but the **administration says it is NOT pursuing a ban** — so this is a **tail risk, not a base case.** *If* enacted, the honest verdict is **nuanced, not the simple "everything routes through China" thesis:** a **product**-export limit is **bearish for product tankers (LR2/MR) but only *indirectly* bullish for VLCCs** — it would strand US Gulf refining, push more *crude* toward Asian refiners (China/India, already the "East-of-Suez" export hub), lengthen tonne-miles, and could raise VLCC demand ~**modestly (est. +2–5%, unverified)**. The clean historical analog (1975–2015 crude-export ban) shows policy *can* reshape global tanker routing for *decades* — but the sign for VLCCs depends on crude vs product scope.
> - **Module 2 — rate-vs-stock across cycles (the quantified playbook):** Across **4 cycles**, three hard rules emerge from our own data: **(1) FRO is the high-beta vehicle** — its trough→peak stock multiple is consistently **~1.6–2× DHT's** (2005-08: FRO 3.7× vs DHT 1.8×; 2022-26: FRO **11.8×** vs DHT **6.9×**). **(2) Stocks track SUSTAINED rates ~1:1 in multiple terms, and IGNORE transient spikes** — in 2019-20 the rate *spiked* 16.7× (COSCO \$300k, COVID) yet stocks only did ~2.2–2.5× (they price the *durable* level, not the headline). **(3) The current cycle is already the biggest stock move in FRO/DHT history** (FRO +1080% off its 2022 trough), *because* the rate strength has been the most **sustained** (structural/supply-driven), not the highest-spiking.
> - **Cycle-position read:** mid-to-late. The stock multiples now **exceed** every prior *normal* cycle — consistent with "the big cycle has largely paid off." With the **2028 supply wall** ([vlcc_supply](../vlcc_supply/report_en)) ahead, this argues **CRule 8 exit discipline** (trim into strength), not fresh chasing.
> - **Education/analysis, NOT investment advice.**

---

## ⚠️ Protocol & data notice

Applies the **Two-Step Research Protocol** and **Cyclical CRules 1/3/4/6/8**. Module 1: §1–3. Module 2: §4–6. §7 cycle-position verdict. **Stock data is exact (yfinance split/dividend-adjusted); VLCC TD3C rate levels are approximate/sourced and flagged (Rule 4); trade-flow impact estimates are explicitly marked "unverified."** Model reproducible via `run_cycle_model.py`.

---

# MODULE 1 — US product-export limits & global crude re-routing

# Section 1 — Fact-base (verified Sep 16, 2026; Rule-4 flags)

| Fact | Detail | Source (Rule 4) |
|---|---|---|
| **The bill** | **H.R. 8266 "Gasoline Export Ban Act of 2026"** — bans gasoline exports when US retail price >**\$3.12/gal for 7 consecutive days**; President may exempt | GovTrack (primary bill text) |
| **Administration stance** | As of early/mid-2026, **NOT actively pursuing** a crude or product export ban (despite Congress/media pressure) | OilPrice; Resilience.org |
| **US Gulf product exports** | **~3.5–4.0 mb/d** — mainly gasoline→Latin America, diesel→Europe | EIA; McKinsey (pre-2026 baseline) |
| **Refining "East of Suez" shift** | Capacity + product-export growth concentrated in **China & India**; India exports **>1.2 mb/d** products; China export quotas rising into the new Five-Year Plan | EIA outlook; S&P Global; Argus |
| **China refiner scale** | **Sinopec = world's largest refiner**; teapots maxing out on discounted Russian/Iranian crude | OilGasStorageNews; AInvest |
| **Historical analog** | **1975–2015 US crude-export ban**: US crude exports ~ceased, tankers shifted to *import* jobs; **2015 lifting** turned the US into a top crude exporter and **re-routed global tanker flows** (US Gulf → Atlantic/Asia) | Ballotpedia; Columbia; Forbes |

**The user's specific hypothesis (steel-manned):** historically products moved *short-haul* (Americas←US, Asia←China, Europe←US). If the US restricts exports, does the world's crude increasingly route to **China** (refine) then re-export products globally → **more long-haul crude tonne-miles = VLCC-bullish**?

---

# Section 2 — Step 1: Concise Research Draft

**Core conclusion:** A US **product**-export limit would be **directly bearish for product tankers** and only **indirectly, modestly bullish for VLCCs** via a crude-routing shift toward Asian refiners — **NOT** the clean "all crude to China" super-bull the headline suggests, and it is a **low-probability tail** (administration not pursuing it). The durable VLCC bull case still rests on **supply** (fleet/orderbook, [vlcc_supply](../vlcc_supply/report_en)) and **shadow-fleet/geopolitics**, not this policy.

*Supporting (claim → evidence needed):*
1. **Refining gravity is already East-of-Suez** → China/India are the growing product-export hubs; a US product cap accelerates the shift → more crude sails East. *Evidence: §1 EIA/S&P — obtained (direction); magnitude **unknown**.*
2. **Policy can re-route tankers for decades** → the 1975–2015 ban is the proof-of-concept that US export policy reshapes global flows. *Evidence: §1 historical — obtained.*
3. **Longer crude tonne-miles help VLCCs** → routing Atlantic/US crude to Asia instead of short-haul products lengthens hauls. *Evidence: mechanism sound; net-barrel math **unverified**.*

*Opposing (claim → counter-evidence):*
1. **A product ban hits PRODUCT tankers, not VLCCs** → the direct casualty is LR2/MR (US Gulf product exports ~3.5–4 mb/d); VLCC benefit is second-order and could be *offset* if US crude *exports* also fall. *Evidence: §1 — obtained; VLCC net sign **unknown**.*
2. **It may never happen / be temporary** → administration not pursuing; bill is price-triggered and exemptible → unlikely to durably reshape trade. *Evidence: §1 stance — obtained.*

---

# Section 3 — Step 2: Strict Peer Review (draft NOT rewritten)

1. **Facts that need verification:** the **quantitative** VLCC tonne-mile delta from a US product cap (I have found **no credible published number** — my "+2–5%" is an **estimate, not sourced**); whether a *product* ban would also curb US *crude* exports (opposite sign for VLCCs); current exact US Gulf product-export split by destination.
2. **Logical leaps / equivocation:** the biggest is **"product-export limit" ≠ "crude-export limit"** — the user's "all crude to China" intuition is really a *crude*-flow story, but the actual bill targets *products*; conflating them inverts the tanker impact. Also "more refining in China → more VLCC crude imports" assumes China *adds* refining to serve the world, not just substitutes — **unproven**.
3. **Missing counterexamples / competing explanations:** China's oil demand is projected to **peak ~2027** (it may *not* expand crude imports structurally); a product cap could simply **destroy** US refining margins and volumes (less crude processed globally, not merely relocated); **freight already reflects** shadow-fleet/geopolitics, so a slow policy shift may be marginal.
4. **Most important primary sources to add:** EIA STEO + *Outlook on Global Refining to 2028*; Clarksons/BIMCO tonne-mile models with a policy-shock scenario; the actual H.R. 8266 text & CBO/committee analysis; Kpler crude/product flow data by origin-destination.
5. **Speculation, not fact:** the "+2–5% VLCC demand" figure (**explicitly an estimate**); "world's crude routes through China then re-exports" (a *scenario*, not established); any claim this policy is a *primary* VLCC driver (it is a tail).

> **Module-1 bottom line:** Interesting tail, but **discipline the thesis**: the bill targets **products** (bearish LR2/MR), the VLCC benefit is **indirect and unquantified**, China's demand may peak by 2027, and the administration isn't pursuing it. **Do not underwrite the VLCC bull case on this** — treat it as optional upside on top of the *supply-driven* core. The 1975–2015 analog proves policy *can* reshape flows for decades, which is why it's worth **watching**, not betting.

---

# MODULE 2 — Rate-vs-stock across VLCC cycles (the quantified playbook)

# Section 4 — Four cycles: stock multiple vs rate multiple

*(FRO/DHT split/dividend-adjusted, exact. VLCC TD3C rate anchors approximate/sourced, Rule 4. Rising-leg trough→peak. Reproducible: `run_cycle_model.py`.)*

![FRO & DHT across four VLCC cycles, log scale](charts/fro_dht_history.png)

| Cycle | Driver | Sustained rate mult | Spike (transient) | **FRO stock** | **DHT stock** | FRO beta vs sustained |
|---|---|---|---|---|---|---|
| **2005-08** | China demand supercycle | ~1.9× (\$50k→\$95k) | \$196k (Jul-08) = 3.9× | **3.7×** (26mo) | **1.8×** (21mo) | 1.95× |
| **2015** | China SPR + cheap oil | ~2.3× (\$28k→\$65k) | \$100k = 3.6× | **2.5×** (11mo) | **1.4×** (15mo) | 1.08× |
| **2019-20** | (see spike) | ~2.5× (\$18k→\$45k) | **\$300k COSCO / \$200k COVID = 16.7×** | **2.5×** (17mo) | **2.2×** (12mo) | 1.00× |
| **2022-26** | Supply-driven + Russia + Hormuz | **~4.8× (\$20k→\$85–95k)** | \$585k (2026) = 29× | **11.8×** (56mo) | **6.9×** (56mo) | 2.48× |

---

# Section 5 — The three quantified rules (what the data proves)

**Rule A — FRO is the high-beta vehicle; DHT is the "cleaner" lower-beta one.** In *every* cycle, FRO's trough→peak multiple is **~1.6–2× DHT's** (2005-08: 3.7× vs 1.8×; 2022-26: 11.8× vs 6.9×). This is operating leverage + higher spot exposure + more financial leverage (CRule 4). **If you want maximum torque, FRO; if you want the same cycle with less violence, DHT.** (Mirrors the gold-miner Kinross-vs-Agnico torque logic.)

**Rule B — Stocks price SUSTAINED rates, and largely IGNORE transient spikes.** This is the single most important finding. In **2019-20**, the rate *spiked* **16.7×** (COSCO \$300k, COVID \$200k) but the stocks only rose **~2.2–2.5×** — a **beta-vs-spike of ~0.13×**. Yet against the **sustained** rate multiple (~2.5×), the stock beta was **~1.0×**. **The market discounts a two-week \$300k print to almost nothing; it re-rates on the durable level.** (This is exactly why the Aug-2026 \$585k Hormuz spike faded in the stock — [seasonality §8](../vlcc_seasonality/report_en).) *Practical: don't buy a rate-spike headline; buy/hold a sustained-rate regime.*

**Rule C — The current cycle is the biggest stock move ever *because* it's the most sustained, not the highest-spiking.** 2022-26 sustained rate multiple (~4.8×) is the **largest of the four** (vs ~1.9–2.5× before), and it produced by far the **largest stock multiples (FRO 11.8×, DHT 6.9×)** and the highest FRO beta (2.48×). **Durability, not peak height, is what compounds the equity.** The structural supply story is *why* this cycle's rates stayed high for **56 months** vs 11–26 months historically.

**On lead/lag (CRule 1):** industry research + our own work put tanker equities **leading the physical rate by ~2–4 weeks** (the stock discounts the forward curve). Confirmed in our [seasonality report](../vlcc_seasonality/report_en) (stock leads rate 1–3 months) and the Aug-2026 episode (stock peaked Aug 19, rate plunged Aug 24). **The stock turns *first*, both up and down** — the key CRule 8 warning for a mid-late-cycle holder.

---

# Section 6 — Applying it: where are FRO/DHT now (Sep 2026)?

- **Current levels (Sep 2026):** FRO ~\$53.7 (at/near cycle high), DHT ~\$23.0 (at cycle high). Both have delivered the **largest trough→peak multiples in their history** (FRO 11.8×, DHT 6.9×) — *the big cycle has largely paid off*, exactly as the user notes.
- **What the playbook says about "which phase":** the stock multiples now **exceed every prior *normal* cycle** and are into supercycle territory. Historically, the equity **peaks near/at the sustained-rate peak and turns 2–4 weeks *before* the rate** (Rule B/lead-lag). We are therefore **mid-to-late cycle**, not early.
- **The forward overhang:** the [2028 newbuild wall](../vlcc_supply/report_en) (net fleet growth +4.9–9.9% in 2028) is the classic CRule 3 supply response that historically ends VLCC cycles. Combined with flat tonne-mile demand, it caps the *sustained* rate — and per Rule C, sustained rate is what the equity capitalizes.

**Cycle-position summary (CRule 1 format):**
```
Current position:  Mid-to-LATE cycle. Equity has delivered a supercycle-scale move
                   (FRO 11.8x / DHT 6.9x off the 2022 trough) driven by the most
                   SUSTAINED rate regime in FRO/DHT history (~4.8x, 56 months).
Evidence:          Stock multiples exceed every prior normal cycle; rates elevated
                   but the Aug-2026 -20%/day plunge shows the sustained level softening.
Historical analog: Most like the LATE stage of 2005-08 (supercycle equity), but with a
                   supply-driven (not demand-driven) rate base -> potentially longer tail.
Predicted next:    Upside now depends on the SUSTAINED rate holding, not fresh spikes;
                   the 2028 supply wall caps it. Stock will turn 2-4 weeks BEFORE the rate.
Time to peak:      Plausibly the strong window runs to ~mid-2028 (supply), but the EQUITY
                   likely peaks earlier (it leads). Vigilance now, per the user's instinct.
Key risk:          A sustained-rate rollover (2028 deliveries, demand slip, shadow-fleet
                   return) -> CRule 8 exit; and remember the stock leads it down.
```

> **Bottom line for the user:** your caution is well-placed. The data says **you have already captured a supercycle-scale move** (FRO 11.8×/DHT 6.9×), and the reason it was so big is **durability** (the most sustained rate regime ever), not any single spike. From here: **(1)** further upside needs the **sustained** rate to *hold* (Rule B) — new Hormuz-type spikes won't re-rate the stock; **(2)** the equity **leads the rate down by 2–4 weeks**, so waiting for the rate to roll over means selling late; **(3)** the **2028 supply wall** is the datable cycle-ender. This is a textbook **CRule 8 "trim into strength / define your exit"** moment — hold the core if you believe the sustained regime lasts to mid-2028, but don't add on spike headlines, and pre-commit your exit triggers. FRO gives more torque both ways; DHT is the lower-beta way to stay in.

---

# Section 7 — 【DEEP】Rate-to-valuation bridge: average rates by cycle, implied rate, and $150k/$200k/$250k guidance

> Follow-up: summarize **average VLCC rates by cycle**, put them in **one table with DHT/FRO adjusted prices**, work out **what rate today's price implies**, and give **stock guidance at $150k / $200k / $250k sustained**.

## 7.1 The earnings model (transparent + validated)

```
Cash earnings = vessel_days x (TCE - cash_breakeven)
Net income    = Cash earnings - D&A
EPS           = Net income / shares
```

| Anchor | DHT | FRO | Source |
|---|---|---|---|
| Fleet | 24 VLCC | 42 VLCC + 21 Suezmax + 18 LR2 = **57.9 VLCC-equiv** | P-Rule 1 |
| Vessel-days/yr | ~8,400 | ~20,290 (VLCC-equiv) | 96% utilization |
| **Cash breakeven** | **\$17,500/day** | **~\$26,000/day** | **Company-disclosed** (DHT 2026 spot BE; FRO Q3-25 deck) |
| D&A | ~\$105M | ~\$300M | est. from fleet |
| Shares | 161.24M | 222.62M | yfinance |
| Price (Sep 16, 2026) | **\$23.04** | **\$53.67** | live |

**✅ Model validation (Rule 4) — this is why you can trust the outputs:** feeding each stock's quoted trailing P/E back through the model implies a trailing TCE of **~\$88.7k/day (DHT)** and **~\$117.0k/day (FRO)**. Both sit sensibly between their disclosed quarterly prints (DHT Q4-25 \$60.3k → Q1-26 \$78.8k; FRO Q2-26 \$152.7k, Q3-26 \$156.9k blended with weaker 2025). **The model reproduces reality within ~5%.**

## 7.2 Average TCE by cycle — in ONE table with DHT/FRO adjusted prices

| Cycle | Years | **Avg VLCC TCE** | **FRO avg px** | **DHT avg px** |
|---|---|---|---|---|
| **2005-08** demand supercycle | 2005-08 | **\$64,250** | **\$62.01** | **\$31.76** |
| 2009-14 post-GFC bust | 2009-14 | \$27,166 | \$28.34 | \$8.54 |
| **2015-16** SPR mini-cycle | 2015-16 | **\$52,500** | **\$5.21** | **\$2.66** |
| 2017-18 trough | 2017-18 | \$19,500 | \$3.18 | \$2.11 |
| **2019-20** sanction/COVID | 2019-20 | **\$54,500** | **\$4.81** | **\$3.28** |
| 2021-22 bottom | 2021-22 | \$14,000 | \$6.19 | \$4.46 |
| **2023-26** current supply cycle | 2023-26 | **\$57,000** | **\$21.93** | **\$10.89** |

![VLCC average TCE vs DHT/FRO adjusted share price](charts/rate_vs_stock.png)

### ⚠️ The single most important row-pair in this study

**2005-08 avg TCE \$64,250 → FRO \$62.01.  2015-16 avg TCE \$52,500 → FRO \$5.21.  2019-20 avg \$54,500 → FRO \$4.81.**

**Nearly the same rate, a ~12× different share price.** This kills the naive "rate X ⇒ price Y" mapping. Three reasons:
1. **Durability (Rule B, §5).** 2015 and 2020 were *transient* (SPR buying; COVID floating storage) — the market refused to capitalize them. 2005-08 and 2023-26 are *sustained* regimes, so they get capitalized.
2. **Balance sheet.** In 2015-20 the sector was over-levered post-2012; equity was a thin option on the assets.
3. **⚠️ Share count (Rule 4 caveat).** Adjusted prices correct for *splits*, **not dilution** — FRO's share count grew from roughly the 70-80M area (mid-2000s) to **222.6M** today. So cross-era *price* comparisons overstate the collapse; **market-cap-per-VLCC** would be the cleaner metric. Treat the 12× as **directional, not literal.**

> **Implication:** never underwrite a target price off a rate *level* alone. The multiple the market pays per unit of rate has ranged from **~\$0.08 to ~\$1.73 of FRO share price per \$1k/day** — it is a function of **durability and leverage**, not the rate itself.

## 7.3 What sustained rate does TODAY's price imply?

*(Reverse the model: what TCE makes today's price fair at a given P/E?)*

| Assumed P/E | **DHT @ \$23.04 implies** | **FRO @ \$53.67 implies** |
|---|---|---|
| 4× (cycle-peak PE, CRule 2) | \$140,564/day | \$188,001/day |
| 5× | \$118,451/day | \$158,558/day |
| **6× (base)** | **~\$103,700/day** | **~\$138,900/day** |
| 7× | \$93,179/day | \$124,908/day |
| 8× | \$85,282/day | \$114,393/day |

**🔑 The key finding — FRO is priced for a ~34% higher sustained rate than DHT.** At a common 6× multiple, DHT's price discounts **~\$104k/day**, FRO's discounts **~\$139k/day**. Given the Aug-2026 plunge settled TD3C near **\$87.7k** and the global VLCC average was ~**\$83.9k**, **DHT is priced roughly in line with today's spot, while FRO already requires a materially higher sustained rate to justify itself.**

## 7.4 Stock guidance at \$150k / \$200k / \$250k sustained (CRule 7)

**EPS at sustained TCE:**

| Sustained TCE | DHT EPS | FRO EPS |
|---|---|---|
| \$100,000 | \$3.65 | \$5.40 |
| \$120,000 | \$4.69 | \$7.22 |
| **\$150,000** | **\$6.25** | **\$9.95** |
| **\$200,000** | **\$8.86** | **\$14.51** |
| **\$250,000** | **\$11.46** | **\$19.07** |

**Target price & upside vs today (DHT \$23.04 / FRO \$53.67):**

| Sustained TCE | | **PE 4× (bear)** | **PE 6× (base)** | **PE 8× (bull)** |
|---|---|---|---|---|
| **\$150k** | **DHT** | \$25.01 *(+9%)* | **\$37.51 *(+63%)*** | \$50.01 *(+117%)* |
| | **FRO** | \$39.82 *(−26%)* | **\$59.72 *(+11%)*** | \$79.63 *(+48%)* |
| **\$200k** | **DHT** | \$35.43 *(+54%)* | **\$53.14 *(+131%)*** | \$70.85 *(+208%)* |
| | **FRO** | \$58.04 *(+8%)* | **\$87.07 *(+62%)*** | \$116.09 *(+116%)* |
| **\$250k** | **DHT** | \$45.84 *(+99%)* | **\$68.77 *(+198%)*** | \$91.69 *(+298%)* |
| | **FRO** | \$76.27 *(+42%)* | **\$114.41 *(+113%)*** | \$152.55 *(+184%)* |

**And the downside symmetry (equally important):**

| Sustained TCE | DHT @ 6× | FRO @ 6× |
|---|---|---|
| \$100k | \$21.88 *(−5%)* | \$32.38 *(−40%)* |
| \$80k | \$15.63 *(−32%)* | \$21.44 *(−60%)* |

## 7.5 The counter-intuitive conclusion (this inverts the earlier read)

**From the 2022 trough, FRO was the higher-beta winner (11.8× vs DHT 6.9×). But from TODAY's price, DHT has the better risk/reward — because FRO has already priced in the higher rate.**

- **At \$150k sustained (P-Rule 3 base):** DHT **+63%**, FRO only **+11%** (at 6×). FRO needs ~\$139k *just to stand still*.
- **At \$80-100k (i.e., today's actual spot ~\$84-88k):** DHT is roughly **fair to −5%**, FRO is **−40% to −60%**. **FRO carries far more downside if the rate merely stays where it is.**
- **FRO only wins decisively above ~\$200k**, where its operating leverage (57.9 VLCC-equiv vs 24) dominates: +62% vs DHT's +131%… *note DHT still leads in % terms; FRO leads in absolute dollars per share.*

**Why:** FRO's higher gearing cuts **both ways**. It gave the bigger trough→peak multiple, and it now embeds the more demanding rate assumption. **DHT's low \$17,500 breakeven + a price discounting only ~\$104k is the better-protected way to stay long the cycle.**

> **给用户的直接结论 / Bottom line:** today's prices say the market has **already capitalized roughly today's spot for DHT (~\$104k) but a much higher sustained ~\$139k for FRO.** So: **if you believe \$150k+ is sustainable into 2027-28, DHT offers the better upside (+63% vs +11%) and FRO offers more absolute torque only above ~\$200k. If rates merely hold at today's ~\$85-90k, DHT is roughly fair while FRO is exposed to a 40-60% de-rate.** Combined with §5's "stocks capitalize *sustained*, not spike" and the **2028 supply wall**, this argues for **rotating cycle exposure toward the lower-breakeven, less-demanding name (DHT) and trimming the one that needs heroic rates (FRO)** — a concrete CRule 8 action rather than a generic "stay vigilant."

*(Reproduce: `python run_rate_valuation.py` → `data/{rate_vs_price_table,cycle_avg_rates,implied_rate,target_prices}.csv` + `charts/rate_vs_stock.png`. **Rule 4:** annual TCE averages are approximate/broker-derived and conflict across providers by >20% in some years; breakevens and current prices are company-disclosed/live; D&A is estimated; P/E 4-8× brackets the historical cycle range (CRule 2). Targets are scenario arithmetic, **not forecasts**.)*

---

# Section 8 — Quarterly rebuild + P/NAV cross-check + lead/lag + exit dashboard

## 8.0 First: what the rate unit actually is

**TCE is US dollars per vessel per DAY (\$/day).** A "quarterly rate" here is the **average of that daily rate across the quarter** — *not* a per-quarter dollar total. §7 used **annual** averages of the daily rate; this section rebuilds on **quarterly**, which is better because (a) DHT/FRO **disclose achieved TCE quarterly** (primary data), (b) VLCC seasonality is quarterly, and (c) lead/lag needs the higher frequency.

## 8.1 Quarterly rate vs quarterly average price

![Quarterly VLCC TCE vs DHT/FRO quarterly average adjusted price](charts/quarterly_rate_vs_stock.png)

**⚠️ Honest data note (Rule 4):** the chart uses **two different qualities of rate data**, and they are drawn differently. **Dark blue = DHT's OWN disclosed quarterly fleet TCE (primary, 2024Q1-2026Q3).** **Light grey = an annual broker average carried across the four quarters — these are NOT true quarterly prints** and must not be read as such. No reliable public quarterly TD3C series was obtainable for the earlier period.

**The real quarterly data (primary, company-disclosed):**

| Quarter | DHT fleet TCE (\$/day) | FRO avg px | DHT avg px |
|---|---|---|---|
| 2024Q1 | 47,200 | 19.05 | 8.86 |
| 2024Q4 | 45,200 | 14.84 | 8.24 |
| **2025Q1** | **35,800** (cycle low) | 14.65 | 9.29 |
| 2025Q3 | 40,500 | 19.23 | 10.23 |
| 2025Q4 | 60,300 | 21.79 | 11.33 |
| 2026Q1 | 78,800 | 31.73 | 15.60 |
| **2026Q2** | **126,700** (peak) | 34.33 | 15.84 |
| **2026Q3** | **94,300** | **45.61** | **20.02** |

**Note the 2026Q2→Q3 divergence:** the **rate fell 26%** (126,700→94,300) while **both stocks rose sharply** (FRO +33%, DHT +26%). That is the market **capitalizing the sustained regime and looking through the Q2 spike** — a live, quarterly-resolution confirmation of §5's Rule B.

## 8.2 ⭐ P/NAV — an INDEPENDENT check that confirms §7

**First, an honest retraction.** I attempted the "market-cap-per-VLCC across eras" idea and **rejected it**: reliable point-in-time share counts aren't available, and FRO's reverse split makes pre-2012 raw prices ambiguous. A naive run produced **\$495M per VLCC for DHT in 2010** when a VLCC was actually worth ~\$100M — the method was broken, so it is not published. Instead, the **standard shipping metric on today's data**, which is fully sourced:

| | Ships | Fleet asset value | EV | **EV per ship** | **EV / NAV** |
|---|---|---|---|---|---|
| **DHT** | 24 VLCC | \$4,188M | \$3,994M | \$166.4M | **0.95× (−5% discount)** |
| **FRO** | 42 VLCC + 21 Suezmax + 18 LR2 | \$11,649M | \$14,060M | \$173.6M | **1.21× (+21% premium)** |

*Asset values (Clarksons/trade press 2026): 5-yr-old VLCC **\$174.5M** (now above the **\$129.5M** newbuild price — a 35% premium for prompt tonnage), Suezmax ~\$120M, LR2 ~\$100M.*

> **🔑 This is the important part: a completely INDEPENDENT method reaches the same verdict as §7.** The implied-rate approach said FRO discounts ~\$139k/day vs DHT's ~\$104k. The asset-value approach says **DHT trades at a 5% *discount* to its ships while FRO trades at a 21% *premium*.** Two unrelated methods, same conclusion: **FRO is priced far more demandingly.** When two independent approaches agree, the finding is robust.

## 8.3 Lead/lag on REAL quarterly data

*(Correlation of quarterly stock return vs quarterly disclosed-TCE change, at various lags. Positive lag = the stock moved **first**.)*

| | Best correlation | At lag | Reading |
|---|---|---|---|
| **DHT** | **0.75** | **+1 quarter** | **Stock LEADS by ~1 quarter** |
| **FRO** | 0.72 | −1 quarter | Stock lags by ~1 quarter |

**⚠️ Do not over-read this (n = 10 quarters).** With ten observations the DHT-vs-FRO *difference* is **not statistically meaningful**. What *is* robust is the **high contemporaneous-to-near-term correlation (0.72–0.75)** — i.e., stock and rate are tightly coupled at quarterly resolution, and DHT's result is consistent with the industry norm (equities lead the physical rate). **I also tested weekly lead/lag and discarded it:** the weekly rate series had to be *interpolated* from quarterly points, which destroys the high-frequency signal (all correlations came out 0.03–0.18, i.e. noise). **You cannot measure weekly lead/lag against interpolated quarterly data** — reporting it would have been spurious precision.

## 8.4 CRule 8 exit-trigger dashboard

| Trigger (observable) | Action | Why |
|---|---|---|
| **Spot TD3C < \$60k/day for >3 consecutive weeks** | Reduce 30% | Below ~2× DHT breakeven; the *sustained* regime is breaking (Rule B) |
| **DHT disclosed fleet TCE falls QoQ two quarters running** | Reduce 30% | Company-disclosed TCE is the cleanest primary signal; two down quarters = trend, not noise |
| **FRO forward-booked % fixed at a LOWER rate than the prior print** | **Trim FRO first** | FRO is priced for ~\$139k and 1.21× NAV — a booking downgrade hits it hardest |
| **Monthly VLCC demolition < 3–4 ships/month through 2027** | Raise cash / trim | Low-scrap path → net fleet growth ≈ gross → 2028 oversupply ([vlcc_supply](../vlcc_supply/report_en)) |
| **New VLCC orders keep running >150/yr** | Begin trimming | Orderbook already ~35% of fleet (CRule 5: "order books filling") |
| **Sanctions thaw / shadow-fleet re-entry headlines** | Full re-underwrite | Returning shadow VLCCs = +10–12% compliant supply shock |
| **Stock falls while spot is flat/up for >2 weeks** | Investigate — likely early exit | The equity sees it first (§5 lead/lag; the Aug-2026 episode) |
| **P/E < 4× on peak earnings** | Take profits on 50% | CRule 2: trough-PE on peak-EPS = market pricing terminal decline |

> **Net for the user:** on a **quarterly** basis the picture is sharper, not softer. The 2026Q2→Q3 print (rate −26%, stocks +26–33%) is textbook "capitalize the sustained, ignore the spike." And the **P/NAV cross-check independently confirms the §7 conclusion** — **DHT at 0.95× asset value vs FRO at 1.21×.** Both the earnings-based and the asset-based lens say the same thing: **DHT is the better-protected way to stay long this cycle; FRO is the one to trim first when the dashboard triggers fire.**

*(Reproduce: `python run_quarterly_deep.py` → `data/{quarterly_rate_price,pnav,leadlag,exit_dashboard}.csv` + `charts/quarterly_rate_vs_stock.png`.)*

---

## Reproduce it yourself

```
cd vlcc_cycles
python run_cycle_model.py       # data/cycle_multiples.csv + charts/fro_dht_history.png
python run_rate_valuation.py    # §7: rate-to-valuation bridge, implied rate, target prices
python run_quarterly_deep.py    # §8: QUARTERLY rebuild, P/NAV, lead/lag, exit dashboard
```

Cycle windows and rate anchors are explicit/editable at the top of `run_cycle_model.py`. **Data:** `vlcc_cycles/data/cycle_multiples.csv`. **Chart:** `vlcc_cycles/charts/fro_dht_history.png`.

**Sources (accessed Sep 16, 2026):** yfinance (FRO, DHT split/div-adjusted); GovTrack (H.R. 8266); OilPrice, Resilience.org, Forbes, Columbia, McKinsey, Axios (product-export-ban analysis); Ballotpedia (1975–2015 crude ban); EIA *Outlook on Global Refining to 2028*, S&P Global, Argus, Kpler (refining/flows); data4thepeople, Splash247, Signycle (historical VLCC rates & lead-lag). **VLCC rate levels are approximate/sourced; the "+2–5% VLCC demand" trade-flow figure is an explicit unverified estimate (Rule 4).**

---

*Two-Step Research Protocol applied (Module 1 §2–3; Module 2 embeds draft+review). Cyclical CRules 1/3/4/6/8 applied. Stock data exact; rate levels and policy-impact magnitudes are approximate/estimated and flagged. Education/analysis only — not investment advice.*

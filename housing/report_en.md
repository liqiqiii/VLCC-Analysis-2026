---
layout: default
title: Bellevue Buy vs Rent — Opportunity Cost, Price-to-Rent, and the Lifestyle Premium
---

# Bellevue: Buy or Rent?
## A seven-year wealth model for a $1.8M purchase versus $4,300–$8,000 monthly rent
### August 16, 2026

> **Core conclusion:** For this household, buying a $1.8M Bellevue home is best understood as a **housing-consumption upgrade plus a leveraged, geographically and tech-sector-concentrated real-estate position**, not automatically as an investment superior to financial assets. If the same home rents for about **$5,200/month**, the stated assumptions require roughly **4.31% nominal annual appreciation** over seven years to match renting. At 3% appreciation, ownership's lifestyle premium is about **$1,960/month** relative to renting the same home.
>
> **Important distinction:** The annual "user cost" lens includes the after-tax opportunity cost of the down payment. The terminal-wealth model instead invests the renter's retained down payment and **does not add opportunity cost again**, avoiding double counting.
>
> *Education and decision analysis only; not tax, legal, or investment advice.*

---

# Section 1 — Fact base and model boundaries

## 1.1 Core inputs

| Input | Base case | Status |
|---|---:|---|
| Home price / down payment / loan | $1.8M / $900K / $900K | User scenario |
| Mortgage | 30-year fixed at 6% | Assumption |
| Holding period | 7 years | Assumption |
| Alternative after-tax return | 4% | User's 5% pre-tax, 20% effective-tax assumption |
| Property tax | $15,400/year | Midpoint approximation from Bellevue 2026 levy range |
| Insurance | $4,000/year | Estimate for roughly $1M replacement coverage; quote required |
| Maintenance reserve | $13,500/year | 0.75% of value; not an actual bill |
| Purchase / sale costs | 1% / 7% | Modeling assumptions; commissions are negotiable |
| Tax rate | 20% | User-specified effective marginal assumption, not a statutory bracket |
| Same-home rent | $5,200/month | User observation, not MLS-pair verified |

King County's published 2026 combined Bellevue levies vary by tax district from roughly **0.743%–0.969%** of assessed value. The model uses about **$15.4K** on a $1.8M assessment, near the midpoint. A real decision should use the specific parcel.

## 1.2 Two lenses that must not be mixed

1. **Annual user cost:** down-payment opportunity cost + interest + tax + insurance + maintenance − tax benefit. Useful for intuition.
2. **Terminal wealth:** the renter invests the retained down payment, avoided purchase cost, and annual cash-flow savings; the buyer sells, pays transaction costs, and repays the mortgage. Appropriate for formal break-even analysis.

The terminal model does **not** add the $36K opportunity cost again; the renter's investment account already captures it.

Reproduce with `python housing/run_buy_vs_rent.py`.

---

# Section 2 — Step 1: Concise Research Draft

**Core conclusion:** For this household, buying a $1.8M Bellevue home should be viewed as a housing-consumption upgrade plus a leveraged real-estate position, not automatically as superior to renting and investing. If the same home rents for about $5,200/month and alternative investments earn 4% after tax, the modeled seven-year break-even appreciation rate is about 4.31%. At 3% appreciation, buying produces about $1,960/month less wealth than renting the same home.

**Supporting points (claim → evidence needed):**

1. **High-end Bellevue housing appears rent-favorable** → user-observed $1.8M/$5.2K and $3M/$7K pairs imply only 3.47% and 2.80% gross yields. **Evidence needed:** address-matched MLS sale and rental comparables.
2. **Ownership's unrecoverable costs exceed rent before appreciation** → opportunity cost, interest, property tax, insurance, maintenance, and transaction costs jointly create the hurdle. **Evidence needed:** mortgage schedule, parcel tax bill, insurance quotes, maintenance history, and the household's tax return.
3. **Transactions and compounding materially raise required appreciation** → the renter can invest both the down payment and annual cash-flow savings. **Evidence needed:** lender/title estimate, Washington REET, negotiated brokerage fees, and a reproducible cash-flow model.

**Opposing points (claim → evidence needed):**

1. **Ownership can still outperform** → constrained Bellevue supply, schools and amenities, rent growth, refinancing, and appreciation above 4.31% could erase the gap. **Evidence needed:** repeat-sales, zoning/new-supply, and matched-rent growth data.
2. **Renting may not deliver identical consumption** → the $4,300 townhouse and detached home can differ in space, privacy, school assignment, stability, and customization rights. **Evidence needed:** matched property characteristics and household willingness-to-pay.

---

# Section 3 — Step 2: Strict Peer Review (draft not rewritten)

1. **Facts that need verification:** The $5,200 and $7,000 rents are user observations and require same-address or closely matched MLS comparables; $4,000 insurance, $13,500 maintenance, and 7% sale costs are assumptions; the specific parcel assessment and levy code are unknown; 2026 tax parameters need confirmation at filing; EU HPI and HICP must use matching geographies and dates.
2. **Logical leaps / equivocation:** Annual imputed opportunity cost cannot be added to the renter's invested down payment in the same model; the terminal code uses only the latter. A terminal wealth gap is not current cash spending; "monthly lifestyle premium" is an equivalent monthly contribution that compounds to the terminal gap at 4%. A townhouse and detached home are not automatically identical housing services, and citywide median income is not this household's purchasing power.
3. **Missing counterexamples / competing explanations:** Refinancing optionality, rent growth faster than expenses, constrained Bellevue supply, and inflation eroding fixed-rate debt favor buyers. A tech slowdown may also lower interest rates and partially offset demand weakness. Conversely, high-end transaction costs, concentration risk, and major repairs may exceed the model.
4. **The most important primary sources to add:** The property's King County tax bill; insurance and lender/title quotes; Washington DOR REET; IRS Pub. 936, Schedule A, and §121; address-matched NWMLS rent/sale pairs; FHFA/Case-Shiller Seattle repeat-sales; Bellevue zoning, permits, and completions.
5. **Which sentences can at most be classified as speculation, not fact:** "High-end Bellevue is structurally more rent-favorable"; "a tech slowdown will gradually erase Bellevue's premium"; and any future 3%, 4.31%, or higher appreciation path. The 4.31% figure is a **conditional model output**, not a forecast.

---

# Section 4 — Annual user cost: why the intuitive figure is about $117K

First-year approximation:

| Item | Annual amount |
|---|---:|
| After-tax down-payment opportunity cost ($900K × 4%) | $36,000 |
| Mortgage interest | $53,699 |
| Property tax | $15,400 |
| Insurance | $4,000 |
| Maintenance reserve | $13,500 |
| Less: estimated federal tax benefit | −$5,645 |
| **Annual user cost** | **about $116,954** |
| **Monthly equivalent** | **about $9,746** |

A $900K, 30-year, 6% mortgage has a monthly payment of about **$5,396**. Roughly **$11,052** of the first year's payments reduce principal. Principal is cash outflow but not economic cost because it becomes home equity.

The tax model uses:

- an average first-year mortgage balance near $894K;
- approximately $45.0K of deductible interest under the $750K acquisition-debt cap;
- about $28.2K of incremental itemized deductions above the $32.2K standard deduction after adding $15.4K property tax;
- about $5.65K of benefit at the user's hypothetical 20% effective marginal rate.

This assumes itemization and that the modeled property tax remains usable after the 2026 SALT cap and income phase-out. Actual tax results may differ materially.

---

# Section 5 — Seven-year terminal wealth: the actual break-even

The renter invests:

1. the $900K down payment;
2. the assumed $18K avoided purchase cost;
3. each year's ownership cash outflow minus rent;
4. all at 4% after tax.

The buyer sells after seven years, pays a 7% sale cost, and repays the mortgage. Tax benefits are recalculated using each year's average mortgage balance. The model does not add the $36K opportunity cost separately.

## 5.1 Appreciation hurdle by rent

| Monthly rent | Annual rent | Seven-year break-even appreciation | Monthly ownership premium at 3% appreciation |
|---:|---:|---:|---:|
| $4,300 | $51,600 | **4.86%** | **+$2,843** |
| **$5,200** | **$62,400** | **4.31%** | **+$1,962** |
| $6,000 | $72,000 | **3.80%** | **+$1,178** |
| $8,000 | $96,000 | **2.45%** | **−$781** |

Positive means the buyer accumulates less wealth; negative means the buyer leads. If the same $1.8M home truly rents for $5,200:

- at 3% appreciation, the renter finishes roughly **$190K** ahead after seven years;
- converted to a monthly contribution compounding at 4%, that is about **$1,960/month**;
- the buyer's equivalent economic housing cost is therefore roughly **$5,200 + $1,960 ≈ $7,160/month**.

Because $5,200 already rents the same home, the $1,960 does not purchase space, yard, or schools. It primarily purchases **ownership, customization rights, protection from non-renewal, and tenure certainty**.

## 5.2 Key sensitivities

| $5,200 monthly-rent scenario | Required appreciation |
|---|---:|
| 6% sale cost | 4.15% |
| **7% sale cost** | **4.31%** |
| 8% sale cost | 4.47% |
| Rent and expenses +3%, standard deduction +2.5% | about 4.18% |

The model does not include refinancing. It also excludes capital-gains tax; under 3% or roughly 4.31% appreciation, gains after selling expenses and eligible basis additions would generally remain near or within the $500K §121 exclusion for qualifying married joint filers, but actual basis and tax status control.

---

# Section 6 — Bellevue high-end price-to-rent: value rises faster than rent

| User observation | Price / annual rent | Gross rental yield |
|---|---:|---:|
| $1.8M home / $5,200 monthly rent | **28.8×** | **3.47%** |
| $3M home / $7,000 monthly rent | **35.7×** | **2.80%** |

Moving from the $1.8M home to the $3M home consumes another $1.2M of housing value for only $1,800 more monthly rent:

$$
\frac{1{,}800 \times 12}{1{,}200{,}000}=1.8\%
$$

That **1.8% is a marginal gross yield inferred from two user observations, not a matched-property regression**. It nevertheless illustrates a common high-end pattern: land scarcity and ownership preference capitalize into sale prices more strongly than rents. Renting can therefore consume a large upgrade in housing quality at a low marginal cost.

Aggregate Bellevue medians imply a rough price-to-rent ratio of **37–45×**, versus roughly **16–17×** nationally. These ratios mix apartments, townhouses, and detached homes and are directional only; they do not replace matched-property comparables.

---

# Section 7 — Affordability and tech-concentration risk

The latest available Census measures put Bellevue owner-occupied housing value near **$1.34M** and median household income near **$165.6K**, or about **8.1× income**. At 2026 market prices around $1.45M–$1.55M, the ratio is roughly **8.8–9.4×**, versus about **4–5×** nationally. A $1.8M home is approximately **10.9×** Bellevue median household income.

This does not measure this household's affordability, but it shows that Bellevue's premium depends heavily on high-income demand. A sustained combination of tech layoffs, weaker RSUs, slower hiring, and reduced in-migration could first appear as:

1. lower sales volume and longer listing times;
2. more buyer concessions and softer rents;
3. nominal price stagnation while inflation and national prices erode the relative premium;
4. outright nominal declines if job outflows, rising inventory, and high rates coincide.

Schools, limited land, community quality, and established employment centers are structural and do not disappear after one tech cycle. A tech slowdown may also lower rates, partly offsetting demand weakness. Premium compression is therefore a scenario, not a conclusion.

---

# Section 8 — Housing and inflation: nominal preservation is not real growth

$$
\text{Real house-price growth}
=\frac{1+\text{nominal growth}}{1+\text{inflation}}-1
$$

If nominal prices are flat for seven years while inflation runs at 3%:

$$
1-\frac{1}{1.03^7}=18.7\%
$$

The statement price is unchanged, but real purchasing value falls **18.7%**.

Eurostat reports EU nominal house prices rose roughly **60.5%** from 2010 through 2025Q2. Using approximately **42.6%** cumulative consumer-price inflation from the matching Eurostat HICP/FRED series:

$$
\frac{1.605}{1.426}-1\approx12.6\%
$$

That is approximately **0.8% annualized real house-price growth**. Country paths diverged sharply: Germany and Sweden experienced low-rate booms and rate-driven corrections, while Italy was roughly flat nominally for a long period and declined materially in real terms. Europe demonstrates that housing is not a mechanical inflation hedge: inflation raises replacement costs and rents, but the central-bank response can simultaneously reduce affordability and asset values.

---

# Section 9 — An actionable decision rule

For the same $1.8M home renting at $5,200:

> **If risk-adjusted expected seven-year Bellevue appreciation is below roughly 4.3%, buying is a consumption upgrade with an identifiable price.**

At 3% appreciation, that price is about **$1,960/month**. The decision can therefore be stated as:

1. Are ownership, customization, and tenure certainty worth about **$2,000/month**?
2. Is the household comfortable concentrating roughly $900K of net worth in Bellevue real estate?
3. Is the holding period long enough to absorb 6%–8% sale friction?
4. Would the household still be satisfied if nominal prices stagnate or local tech employment weakens?

If yes, buying can be a rational consumption choice. If the decision only works by assuming appreciation above 4.3%, it is fundamentally a leveraged bet on Bellevue rather than merely the purchase of housing services.

---

## Data and sources

- Reproducible model and CSVs: [`housing/run_buy_vs_rent.py`](https://github.com/liqiqiii/VLCC-Analysis-2026/blob/master/housing/run_buy_vs_rent.py) · [`housing/data/`](https://github.com/liqiqiii/VLCC-Analysis-2026/tree/master/housing/data)
- King County 2026 levies: [Taxing districts codes and levies](https://kingcounty.gov/en/dept/assessor/buildings-and-property/property-value-and-information/reports/levy-rate-reports/taxing-districts-codes-and-levies)
- IRS mortgage interest: [Publication 936](https://www.irs.gov/forms-pubs/about-publication-936)
- IRS 2026 standard deduction: [2026 inflation adjustments](https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill)
- IRS SALT: [Topic No. 503](https://www.irs.gov/taxtopics/tc503)
- IRS home-sale exclusion: [Topic No. 701](https://www.irs.gov/taxtopics/tc701)
- Washington REET: [Department of Revenue](https://dor.wa.gov/taxes-rates/other-taxes/real-estate-excise-tax)
- Bellevue Census profile: [U.S. Census](https://data.census.gov/profile/Bellevue_city,_Washington?g=160XX00US5305210)
- Bellevue housing market: [Zillow](https://www.zillow.com/home-values/3619/bellevue-wa/) · [Redfin](https://www.redfin.com/city/1387/WA/Bellevue/housing-market)
- EU housing: [Eurostat](https://ec.europa.eu/eurostat/web/housing-price-statistics)
- EU HICP series: [FRED / Eurostat](https://fred.stlouisfed.org/series/CP0000EU272020M086NEST)
- Euro-area housing cycle: [ECB](https://www.ecb.europa.eu/press/economic-bulletin/articles/2025/html/ecb.ebart202502_01~2f59dafb26.en.html)

---

*The model is conditional analysis, not a forecast. The highest-value missing inputs are matched sale/rent comps for the actual property, its parcel tax bill, insurance quote, maintenance condition, and the household's actual tax return.*

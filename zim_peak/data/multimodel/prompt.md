# Rule 5 multi-model replay — identical prompt (sent 13-Oct-2026)

Models: claude-opus-4.8, gpt-5.5, gemini-3.7-flash (general-purpose agents, instructed not to use tools).
All three stated that they recognized the company (ZIM, March 2022), so their outputs are hindsight-contaminated.
Responses: `response_<model>.md` in this folder, written verbatim by each model on request.

---

Do NOT use any tools. Answer from the data below only. You are a cyclical-equity research analyst.

The company is anonymized as "Liner L". It is a global container-shipping liner. The analysis date is "Day 0" (a mid-March, in year T). If you think you recognize the company or the year, SAY SO in one line. Then deliberately do NOT use any knowledge of what happened after Day 0. Judge only on what follows.

DATA AS OF DAY 0 (all USD)
- Fleet: 118 operated vessels, roughly 99% chartered-in, with almost none owned. The company has committed to long-term charters for 36 newbuild ships (28 LNG dual-fuel) delivering in years T+1 and T+2.
- FY(T-1) results, released 5 trading days ago:
  - Volume: 3.48M TEU (+23% y/y).
  - Average freight rate: $2,786/TEU (+127%); Q4 rate $3,630/TEU.
  - Revenue: $10.73B. Opex and cost of services: $3.91B. D&A: $0.76B. G&A: $0.27B.
  - EBIT: $5.82B (54% margin; Q4 61%). Adj. EBITDA: $6.60B (prior year $1.04B). Net income: $4.65B; diluted EPS $39.02.
  - Operating cash flow: $5.97B. Capex: $1.01B. FCF: $4.88B.
  - Cash and investments: $3.81B. Net cash: $0.51B. Lease liabilities: $3.07B. Total equity: $4.60B. Shares: 119.7M.
- Prior year FY(T-2): volume 2.84M TEU, rate $1,229/TEU, revenue $3.99B, EBIT $0.72B, EPS $4.96.
- Guidance FY(T): adj. EBITDA $7.1–7.5B; adj. EBIT $5.6–6.0B.
- Dividend policy: 30–50% of annual net income. A $17.00/sh final dividend was just declared (ex-date in 4 trading sessions, ≈19% of the share price), bringing the FY total to $19.50; a $2 special was paid earlier. Cumulative distributions since the IPO 14 months ago are $21.50/sh.
- Stock: $88.62, an all-time closing high. It is up 75% in the last 59 sessions and about 7.7x the IPO price.
  - Volume over the last 6 sessions has run at 1.6–3.0x its 20-day average.
  - Short interest: 4.6% of shares outstanding, 1.0 days to cover.
  - Market cap: ~$10.6B. Largest holder: ~21%. The government holds a golden share that blocks any stake of 35% or more.
- Freight indices:
  - Spot composite index A peaked 9 weeks ago at 5,110 and has fallen for 9 straight weeks to 4,625 (−9.5%). Its pre-pandemic level was roughly 900–1,000, and its year-on-year growth peaked about 10 months ago.
  - Index B peaked 6 months ago at $10,377/FEU and is now about 12–15% below that peak.
- Industry orderbook: about 26% of fleet capacity, the highest in about 8 years. It delivers mainly in T+1 to T+2, with a 2–3-year order-to-delivery lead time.
- Macro:
  - The central bank is starting a hiking cycle this week, with inflation near 8%.
  - A war has just caused an energy-price shock.
  - A major export hub has just announced a COVID lockdown.
  - The equity market is in a drawdown but bouncing.

TASKS (concise, use tables, show math):
1. Day1Global modules, 1–2 lines each:
   - A Revenue quality
   - B Profitability and operating leverage: estimate the cash breakeven freight rate per TEU and show profit at rate = 1.0x / 1.5x / 2.0x / 2.5x / 3.0x breakeven.
   - C Cash flow: FCF yield and dividend yield.
   - D Forward guidance
   - E Competitive landscape
   - K Valuation: PE, P/B, EV/EBITDA.
   - L Ownership/management
   - O Accounting quality: chartered-in fleet under IFRS 16, and the effect on EBITDA comparability and future fixed costs.
2. Six perspectives, each with a one-line verdict:
   - Quality Compounder (Buffett/Munger)
   - Imaginative Growth (Baillie Gifford/ARK)
   - Fundamental Long/Short (Tiger Cubs)
   - Deep Value (Klarman/Marks)
   - Catalyst Driven (Tepper/Ackman)
   - Macro Tactical (Druckenmiller)
3. Contrarian sell-signal checklist: PE at a cycle low; orderbook surging; company expanding aggressively; spot rate at 3x+ breakeven; sell-side >70% Buy (unknown here); "super-cycle" headlines (unknown). Mark each as present, absent or unknown.
4. Cycle phase on this 5-phase scale: Trough / Early / Mid / Late (peak earnings, market prices decline) / Downturn.
5. Earnings sensitivity for FY(T+1) EPS at freight rates of $1,200 / $1,800 / $2,400 / $3,000 / $3,630 per TEU. Assume volume 3.4M TEU, a cost base ~ FY(T-1), net finance cost ~$0.16B, and tax ~18%.
6. 12-month and 24-month target prices (Conservative / Base / Bull), each with an explicit PE or P/B assumption and the dividends you expect to be received. Give a final rating (Buy / Hold / Sell / Trim) and a position action for an investor who holds the stock at a 5x gain.
7. Pre-mortem: "It is one year later and the holder lost 40% (total return)." Give 3–5 causes, each with a probability and an early-warning sign.
8. Anti-bias check: anchoring, recency, narrative, confirmation, survivorship. One line each on how it could mislead this call.

Keep the whole answer under 1,200 words.

---

**Known leakage in this data pack (per gpt-6-astra review round 3):**
- The 9th SCFI decline (published 18-Mar) was included; only 8 declines were public on 16-Mar.
- The 26% orderbook figure was published in early April (Alphaliner showed 24.6% on 1-Feb-2022).
- Short interest was settled 15-Mar and published later.

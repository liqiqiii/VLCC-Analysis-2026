# VLCC-Analysis-2026

Multi-model AI-powered deep dive into the VLCC (Very Large Crude Carrier) super cycle.

## 🌐 [View on GitHub Pages →](https://liqiqiii.github.io/VLCC-Analysis-2026/)

## Reports

### ZIM March 2022 Peak — Volume, Dividends, Rates & Top-Flag Back-Test (v2, October 13, 2026)
- **[ZIM Peak Study EN](41_ZIM_Peak_Day_Marker_EN.md) | [ZIM见顶研究 CN](42_ZIM_Peak_Day_Marker_CN.md)** — code and data in [`zim_peak/`](zim_peak/)
- Price high 3/16 ($88.62), intraday 3/17 ($91.23), gross total-return high on the $17 ex-date 3/22 (not 3/31); SCFI had already fallen 9 straight weeks
- Volume elevated (RVOL ≥1.5 on 9 of 10 sessions 3/9–3/22) but OBV confirmed the high. None of 8 volume/price top flags beat state-matched comparisons across 14 shipping names, 2004–2026
- Qualifies `modeling_stash.md`: MOM20 shows no forecasting advantage vs a depth-matched comparison

### DHT Q4 2026 Bookings & Frontline 2008 P/E Fact-Check (October 12, 2026)
- **Charter anchor: [EN](dht_q4_2026/charter_anchor_en.md) | [期租锚点中文](dht_q4_2026/charter_anchor_cn.md)** — static/dynamic P/E, historical and recent 1/2/3-year fixtures, $230k one-year broker assessment versus signed contracts, and the conditional $80m single-vessel profit example.
- **Historical extension: [FRO 2007Q1-2009Q2 EN](dht_q4_2026/fro_2007_2009_en.md) | [FRO 原始股价与逐季 PE 中文](dht_q4_2026/fro_2007_2009_cn.md)** — original-share prices, period-TTM versus reporting-lag versus final-year P/E, distinct earnings peaks, and the financial-crisis timeline.
- **[Report EN](dht_q4_2026/report_en.md) | [中文报告](dht_q4_2026/report_cn.md)**
- **[GitHub Pages EN](https://liqiqiii.github.io/VLCC-Analysis-2026/dht_q4_2026/report_en) | [GitHub Pages 中文](https://liqiqiii.github.io/VLCC-Analysis-2026/dht_q4_2026/report_cn)**
- $509,100/day applies to approximately 50% of Q4 spot days already booked; $520m profit remains conditional on subsequent fixtures and modeled days/costs.
- Approximately 2.0x annualized-quarter P/E is not reported TTM (approximately 8.9x at the dated reference price); original FRO filings do not establish 2x as a peak-timing rule.
- Reproduce the five-rate scenarios and historical calculations: `python3 dht_q4_2026/run_analysis.py`.

### 🏡 Bellevue Buy vs Rent (NEW — August 16, 2026)
- **[Buy vs Rent EN](housing/report_en.md) | [Bellevue 买房还是租房 CN](housing/report_cn.md)**
- Seven-year terminal-wealth model: $1.8M home, $900K down, $4,300–$8,000 rent scenarios
- Same-home result at $5,200 rent: ~4.31% annual appreciation required to break even
- Reproducible model: `housing/run_buy_vs_rent.py`

### 📊 Sinokor 40% Dominance & Container Shipping Analog (NEW — April 23, 2026)
- **[Sinokor & Container Analog EN](19_Sinokor_Container_VLCC_Analog_EN.md) | [兴高海运与集运类比 CN](20_Sinokor_Container_VLCC_Analog_CN.md)** ← NEW
- How Maersk's 2020–2022 container boom maps onto the 2026 VLCC super-cycle
- Sinokor at 40% spot control vs Maersk's 2M Alliance at 33%: stronger unilateral pricing power
- Stock mapping: FRO=ZIM (+693%), DHT=Hapag (+632%), INSW=Maersk (+164%)
- VLCC stocks only +50-66% so far — potentially 10-20% through the cycle
- Base case: +150-400% further upside with 30-40% annual dividend yields

### 🚢 VLCC Market: Supply Shortage & SPR Restocking (NEW — April 10, 2026)
- **[Supply Shortage EN](13_VLCC_Supply_Shortage_EN.md) | [供给短缺分析 CN](14_VLCC_Supply_Shortage_CN.md)** ← NEW: Shadow fleet exit, SPR restocking 3-scenario model, supply/demand 2026-2030
- Regulated fleet ~650-700 (not 900), 1.1B barrel restocking need, structural deficit by 2027

### 7-Company Peer Universe (April 2026)
- [Peer Universe EN](09_Tanker_Peer_Universe_EN.md) | [Peer Universe CN](10_Tanker_Peer_Universe_CN.md)
- Covers: DHT, FRO, INSW, ECO, TNK, NAT, CMBT
- Hormuz crisis scenarios + $75K–$250K rate sensitivity

### US-Listed: DHT Holdings vs Frontline (FRO)
- **[April 2026 Update EN](11_DHT_FRO_April_Update_EN.md) | [April 2026 Update CN](12_DHT_FRO_April_Update_CN.md)** ← UPDATED: Structural supply thesis added
- [Deep Dive EN](05_Deep_Dive_Day1Global_Framework.md) | [Deep Dive CN](06_Deep_Dive_Day1Global_Framework_CN.md) (March 2026)
- [Full Report EN](01_Full_Report_EN.md) | [Full Report CN](03_Full_Report_CN.md) (March 2026)

### A-Share: 招商轮船 vs 中远海能
- [A-Share Report EN](07_CN_AShare_VLCC_Report_EN.md) | [A-Share Report CN](08_CN_AShare_VLCC_Report_CN.md)

### 🔬 Tech T&M: Keysight Technologies (KEYS) — NEW
- [Keysight Report EN](keysight/report_en.md) | [是德科技研究 CN](keysight/report_cn.md)
- Wide moat T&M leader, 58x trailing PE, AI/5G/defense tailwinds
- Consensus: HOLD / Cautious BUY — quality excellent, price fair not cheap
- 12M base target $350 (+6%), best entry on 15–20% pullback

### Cyclical Metals: 中钨高新 (Tungsten)
- [Tungsten EN](tungsten/report_en.md) | [Tungsten CN](tungsten/report_cn.md)

### 🔴 Hormuz Transit Tracker — LIVE Dashboard (NEW)
- **[Hormuz Tracker](hormuz_tracker.html)** — Daily VLCC transit/waiting/Yanbu counts, TD3C rate overlay, vessel sightings
- Manual-input dashboard: enter data from Lloyd's List / Bloomberg / VesselFinder daily
- 30-day trend charts, fleet reference panel, CSV/JSON export

### 🧮 Modeling Stash — Valuation & Sell Signal Framework (NEW)
- **[Modeling Stash](modeling_stash.md)** — DCF rules for cyclicals, PE backtest (FRO 2006-2025), momentum sell algo with rate confirmation, cycle classification
- Backtested: 4/4 correct across 2008, 2015, 2024, 2026 Hormuz

### Project Tracking
- [Prompt Log EN](Prompt_Log_EN.md) | [Prompt Log CN](Prompt_Log_CN.md)

## Methodology
- 5 AI models: Claude Opus 4.6, Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro
- Day1Global tech-earnings-deepdive framework
- Operating leverage / SaaS economics for shipping
- Container cycle (中远海控 2020-2022) PE compression as valuation reference
- VLCC-equivalent fleet comparison (rate-corrected ratios)
- Hormuz-open normalization scenario modeling
- Live AIS vessel tracking for fleet positioning analysis

## Key Findings (April 2026 Update)

| Stock | Market | Profile | P/B | Best For |
|---|---|---|:---:|---|
| DHT Holdings | NYSE | 24 VLCC pure play | 2.63x | VLCC pure beta, hedged income |
| Frontline (FRO) | NYSE | 81 ships, 83% spot | 3.36x | Maximum upside leverage |
| **INSW** | NYSE | 73 ships, diversified | **1.84x** | **Best overall value** |
| Okeanis (ECO) | NYSE | 16 eco ships, 100% spot | 3.15x | Modern fleet, max sensitivity |
| Teekay (TNK) | NYSE | 34 ships, net cash | 1.39x | Safest balance sheet |
| Nordic (NAT) | NYSE | 20 Suezmax | 1.07x | Income play, cheapest/eq |
| CMB.TECH (CMBT) | NYSE | Diversified, transitioning | 0.96x | Below book value |

*Data as of April 8, 2026. Not investment advice.*

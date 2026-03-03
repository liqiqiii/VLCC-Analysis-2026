#!/usr/bin/env python3
"""
Update all reports with corrected charter mix data:
1. DHT shifting from 54% spot to 75% spot by Q2 2026
2. Clarify booking rate vs charter type distinction
3. Recalculate all sensitivity tables
4. Update EN (05), CN (06), index.md
"""
import os
import re

base = r'C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026'
D = '$'

# ============================================================
# RECALCULATED DATA (DHT 75% spot / 25% TC going forward)
# ============================================================

def calc_dht_old(rate):
    """DHT at 54% spot / 46% TC (Q4 2025 - STALE)"""
    days = 365
    return ((rate - 25000) * 24 * 0.54 + (49400 - 25000) * 24 * 0.46) * days

def calc_dht_new(rate):
    """DHT at 75% spot / 25% TC (Q2 2026 target - FORWARD)"""
    days = 365
    return ((rate - 25000) * 24 * 0.75 + (49400 - 25000) * 24 * 0.25) * days

def calc_fro(rate):
    """FRO multi-segment (unchanged)"""
    days = 365
    suez_r = rate * 0.716
    lr2_r = rate * 0.583
    vlcc = (rate - 25000) * 42 * 0.85 + (85000 - 25000) * 42 * 0.15
    suez = (suez_r - 23700) * 21 * 0.85 + (55000 - 23700) * 21 * 0.15
    lr2 = (lr2_r - 23800) * 18 * 0.80 + (45000 - 23800) * 18 * 0.20
    return (vlcc + suez + lr2) * days

# ============================================================
# NEW MODULE P SECTION (ENGLISH)
# ============================================================

en_new_module_p = r"""

---

## Module P: Charter Strategy & Rate Sensitivity Analysis (5-Model Consensus)

> **The Question**: DHT runs ~54% spot / 46% TC historically, but is shifting to **75% spot / 25% TC by Q2 2026**.
> FRO runs ~83% spot / 17% TC. How do these charter strategies affect earnings, dividends, and positioning?

### P0. Critical Data Clarification: Booking Rate vs Charter Type

Our analysis uncovered two distinct metrics that are often confused:

| Metric | Definition | DHT | FRO (VLCC) |
|--------|-----------|-----|-----------|
| **Booking Rate (锁定率)** | % of Q1 days already contracted (TC + spot fixtures + FFA) | **66% (Jan 14) → 85%+ (later)** | **92%** |
| **Charter Type (租约类型)** | % of fleet on spot market vs time charter (structural) | **54% spot → 75% by Q2** | **83% spot** |

**Key insight**: FRO's 92% Q1 booking rate means near-ZERO short-term revenue risk despite 83% spot charter type.
High spot exposure ≠ high near-term uncertainty. Spot vessels get booked voyage-by-voyage before the quarter starts.
The real sensitivity is to NEXT quarter's re-fixing rates, not this quarter's open days.

**FRO fleet-wide Q1 2026 booking**: VLCC 92% @ $107,100 | Suezmax 83% @ $76,700 | LR2 67% @ $62,400 → Fleet-wide ~84%

### P0.1 DHT Strategy Shift (Critical Model Update!)

DHT management announced on the Q4 2025 earnings call a **strategic pivot from ~50/50 to ~75% spot by Q2 2026**.
This is driven by: (1) historically strong rate environment, (2) fleet renewal with 4 newbuilds arriving H1 2026,
(3) conviction that supply constraints will sustain high rates through 2028.

| Period | DHT Spot % | DHT TC % | Rate Sensitivity (per $1K) |
|--------|-----------|---------|---------------------------|
| Q4 2025 (actual) | 54% | 46% | $4.7M / $0.029 per share |
| Q2 2026 (target) | **75%** | **25%** | **$6.6M / $0.041 per share (+39%)** |

This narrows the DHT-FRO sensitivity gap significantly from 4.4x to **3.2x** (per $1K rate move).

### P1. Charter Mix Overview (UPDATED)

| Metric | DHT Holdings | Frontline (FRO) |
|--------|:---:|:---:|
| **Fleet** | 24 VLCCs (pure play) | 42V + 21S + 18LR2 (81 ships) |
| **Spot exposure (forward)** | **75% (Q2 2026 target)** | ~83% fleet-wide |
| **TC coverage (forward)** | **25%** | ~17% (VLCC: 8-24% by quarter) |
| **TC policy** | Shifting from 50/50 → spot-heavy | "Golden rule": TC < 30% |
| **Q1 Booking rate** | 66% (Jan 14) → 85%+ (later) | VLCC 92% / Fleet 84% |
| **TC rate (VLCC)** | $43,300-49,400/day | $76,900-93,500/day (recent) |
| **Profit-sharing TC** | Yes — index-linked upside on some long TCs | Some |
| **FFA hedging** | None disclosed | Tactical derivatives (undisclosed) |
| **D/E ratio** | 0.38x | 1.31x |

### P2. Earnings Sensitivity to VLCC Rates (CORRECTED: DHT at 75% spot)

| VLCC Rate | DHT Profit | DHT EPS | FRO Profit | FRO EPS | FRO/DHT Profit | FRO/DHT EPS |
|-----------|-----------|---------|-----------|---------|---------------|-------------|
| $25K (BE) | $54M | $0.33 | $116M | $0.52 | 2.17x | 1.57x |
| $40K (Bear) | $152M | $0.95 | $427M | $1.91 | 2.80x | 2.02x |
| $75K (Mid) | $382M | $2.37 | $1,154M | $5.17 | 3.02x | 2.18x |
| **$107K (Q1 2026)** | **$592M** | **$3.68** | **$1,820M** | **$8.16** | **3.07x** | **2.22x** |
| $120K | $678M | $4.21 | $2,090M | $9.37 | 3.08x | 2.22x |
| $150K (Bull) | $875M | $5.43 | $2,710M | $12.15 | 3.10x | 2.24x |
| $200K (Super) | $1,203M | $7.47 | $3,748M | $16.81 | 3.12x | 2.25x |

**vs Old Model (54% spot)**: DHT EPS at $107K was $3.02, now $3.68 (+22%). The FRO/DHT EPS ratio
narrows from 2.70x to 2.22x — FRO still earns more per share, but the gap is significantly smaller.

**Per $1K VLCC rate increase:**
- DHT (75% spot): **$6.6M** additional profit → **$0.041/share** (was $0.029 at 54% spot)
- FRO: **$20.8M** additional profit → **$0.093/share**
- Ratio: 3.2x (was 4.4x) — DHT's strategy shift captures 39% more rate upside

### P3. Earnings Elasticity (+10% Rate → Profit Change, CORRECTED)

| Base VLCC Rate | DHT Profit Change | FRO Profit Change | Who Benefits More |
|----------------|-------------------|-------------------|-------------------|
| $50K | +15.2% | +16.4% | FRO (barely) |
| $75K | +12.7% | +13.5% | FRO (slight) |
| $100K | +11.8% | +12.4% | FRO (slight) |
| $150K | +11.2% | +11.5% | FRO (marginal) |
| $200K | +10.8% | +11.1% | FRO (marginal) |

**Key change**: At 75% spot, DHT's elasticity converges much closer to FRO's. Above $100K,
the difference is only ~0.5-0.6 percentage points. DHT is no longer a "dampened" version of FRO.

### P4. TC Earnings Floor & Downside Protection (CORRECTED)

| Metric | DHT (75% spot) | DHT (old 54% spot) | FRO |
|--------|:-:|:-:|:-:|
| **TC floor (gross)** | $54M/yr ($0.33/sh) | $98M/yr ($0.61/sh) | $202M/yr ($0.90/sh) |
| **Annual interest cost** | ~$20M | ~$20M | ~$155M |
| **TC floor (net of interest)** | **$34M ($0.21/sh)** | $78M ($0.49/sh) | **$47M ($0.21/sh)** |
| **Minimum sustainable yield** | **1.1%** | 2.5% | **0.6%** |

**Critical update**: DHT's move to 75% spot REDUCES its downside protection significantly.
The TC floor drops from $98M to $54M — now **below FRO's gross TC floor**.
Net of interest, DHT and FRO converge at ~$0.21/share minimum — essentially identical.

**This means DHT is sacrificing its defensive advantage to chase upside.** The "bond with equity kicker"
characterization no longer fully applies. DHT is evolving into a "smaller, lower-leverage FRO."

### P5. Stability Scorecard (CORRECTED, 5-Model Consensus)

| Dimension | DHT (75% spot) | DHT (old 54%) | FRO | Comment |
|-----------|:-:|:-:|:-:|---|
| Revenue Predictability | **5** | 7.4 | **3** | DHT drops 2+ pts with less TC |
| Dividend Stability | **6** | 7.8 | **4** | Smaller TC floor = less cushion |
| Earnings Volatility (low=good) | **4** | 6.6 | **2** | More spot = more volatile |
| Downside Protection | **6** | 8.0 | **3.5** | D/E 0.38 still helps, but TC floor halved |
| Upside Capture | **7** | 5.2 | **10** | Significant improvement from 5→7 |
| **Composite** | **5.6** | 7.0 | **4.5** | Gap narrows from 2.5pts to 1.1pts |

**The story changes**: DHT is no longer the clear "defensive" choice. It's moving toward a middle ground —
more upside capture but less downside cushion. FRO remains the pure cycle play.

### P6. FFA Impact Assessment (unchanged)

FRO's "tactical derivatives" likely represent 5-10% effective hedge coverage:
- **Stated physical TC coverage**: ~17% fleet-wide
- **Estimated FFA overlay**: +5-10% synthetic coverage
- **Effective total coverage**: ~22-27% (now closer to DHT's forward 25% TC)

With DHT at 25% TC and FRO at ~22-27% effective coverage, the two companies are
**converging in risk profile** — a fact that supports the similar stock price movements observed.

### P7. Model Characterizations (How Each AI Model Described the Stocks)

| Model | DHT | FRO |
|-------|-----|-----|
| **Opus 4.6** | "Bond with equity kicker" | "Leveraged call option on rates" |
| **Sonnet 4.6** | "Balanced Fortress" | "Pure Cycle Leverage" |
| **GPT-5.2** | "Volatility-managed spot name" | "High-beta freight instrument" |
| **GPT-5.1** | "Collared VLCC play" | "Levered call option on supercycle" |
| **Gemini 3 Pro** | "Hedged Yield strategy" | "Operating Leverage Monster" |

**Post-correction note**: With 75% spot, DHT descriptions shift from "bond+equity kicker" toward
"moderate-leverage VLCC pure play" — still lower risk than FRO due to lower D/E, but no longer defensive.

### P8. Scenario Recommendation (UPDATED with corrected charter mix)

| Market Scenario | VLCC Rate | Winner | Rationale |
|-----------------|-----------|--------|-----------|
| Extended downcycle | $25-40K | **DHT** | Lower leverage (D/E 0.38 vs 1.31) is the remaining edge |
| Recovery | $40-65K | **DHT (slight)** | D/E advantage matters more than TC coverage here |
| Normal market | $65-90K | **Toss-up** | Both now similarly spot-exposed; FRO has scale |
| Bull market | $90-120K | **FRO** | Scale (81 vs 24 ships) + multi-segment |
| Super cycle | $120-150K+ | **FRO** | Absolute earnings power dominates |
| Demand shock spike | $200K+ | **FRO** | $16.81 vs $7.47 EPS — 2.25x per share |

### P9. Key Valuation at Current Rates ($107K, CORRECTED)

| Metric | DHT (corrected) | FRO | Advantage |
|--------|:---:|:---:|:---:|
| Annual profit | $592M | $1,820M | FRO (3.1x) |
| EPS | $3.68 | $8.16 | FRO (2.2x) |
| P/E | **5.3x** | **4.7x** | FRO (cheaper) |
| EV/Profit | 5.9x | 6.2x | **DHT (cheaper on EV)** |
| Dividend yield (80% payout) | **15.1%** | **17.1%** | FRO (2pp higher) |
| EPS per $10K rate increase | **+$0.41** | **+$0.93** | FRO (2.3x more) |

**DHT is now significantly more attractive than old model suggested.** At $107K, DHT's corrected P/E
drops from 6.4x to 5.3x. On EV/Profit (which adjusts for leverage), DHT is actually CHEAPER than FRO.

### P10. Charter Strategy Conclusion (REVISED)

**The convergence thesis**: DHT is evolving FROM a defensive hedge play INTO a lower-leverage
version of FRO's strategy. With both companies now at ~75-83% spot:

- **FRO advantage**: Scale (3.4x more ships), multi-segment diversification, higher absolute earnings
- **DHT advantage**: Lower leverage (D/E 0.38 vs 1.31), cheaper on EV basis, less financial risk

**Updated portfolio allocation for 2026-2028 super cycle:**

| Allocation | Rationale |
|------------|-----------|
| **FRO: 55-60%** | Still the higher-beta play, but advantage over DHT narrower than previously modeled |
| **DHT: 40-45%** | Better risk-adjusted returns than before; lower leverage + near-FRO upside capture |

*Previous allocation was FRO 65-70% / DHT 30-35%. DHT's strategy shift warrants higher weight.*

**Risk management rule**: If rates sustain below $40K for 2+ quarters, DHT's lower D/E becomes
the critical differentiator. Shift to 65% DHT / 35% FRO.

**The charter mix now tells us**: Both companies are betting on the super cycle.
DHT just does it with a safety margin (0.38x D/E). FRO does it all-in (1.31x D/E).

*Charts: See /charts/ folder for 6 visualization files. Note: charts reflect old 54% spot model;
corrected 75% spot curves would show DHT's line steeper and closer to FRO.*

"""

# ============================================================
# NEW MODULE P SECTION (CHINESE)
# ============================================================

cn_new_module_p = r"""

---

## 模块P：租约策略与运价敏感性分析（5模型共识·修正版）

> **核心问题**：DHT历史上运营约54%现货/46%期租，但**正在转向Q2 2026目标75%现货/25%期租**。
> FRO运营约83%现货/17%期租。这些租约策略如何影响盈利、分红和投资定位？

### P0. 关键数据澄清：锁定率 vs 租约类型

分析中发现两个经常被混淆的不同指标：

| 指标 | 定义 | DHT | FRO (VLCC) |
|------|------|-----|-----------|
| **锁定率** | Q1已签约天数占比（期租+现货长单+FFA） | **66%（1月14日）→ 85%+（后续）** | **92%** |
| **租约类型** | 船队在现货市场vs期租的结构性比例 | **54%现货 → Q2目标75%** | **83%现货** |

**关键洞察**：FRO的92%锁定率意味着尽管83%为现货船，近期收入风险几乎为零。
高现货占比 ≠ 高近期不确定性。现货船在季初就已逐航次签约。
真正的敏感性在于下一季度的重新定价，而非本季度的未签天数。

**FRO全船队Q1 2026锁定率**：VLCC 92% @ $107,100 | Suezmax 83% @ $76,700 | LR2 67% @ $62,400 → 船队加权约84%

### P0.1 DHT战略转型（关键模型更新！）

DHT管理层在Q4 2025电话会上宣布**从约50/50转向Q2 2026目标75%现货**。
驱动因素：(1) 历史性强劲运价环境，(2) 4艘新造船H1 2026交付的船队更新，
(3) 对供给约束将支撑高运价至2028年的信念。

| 时期 | DHT现货% | DHT期租% | 运价敏感度（每$1K） |
|------|---------|---------|-------------------|
| Q4 2025（实际） | 54% | 46% | $4.7M / 每股$0.029 |
| Q2 2026（目标） | **75%** | **25%** | **$6.6M / 每股$0.041（+39%）** |

这显著缩小了DHT-FRO敏感度差距，从4.4倍降至**3.2倍**（每$1K运价变动）。

### P1. 租约结构对比（已更新）

| 指标 | DHT Holdings | Frontline (FRO) |
|------|:---:|:---:|
| **船队** | 24艘VLCC（纯VLCC） | 42V + 21S + 18LR2（81艘） |
| **现货敞口（前瞻）** | **75%（Q2 2026目标）** | ~83%（全船队） |
| **期租覆盖（前瞻）** | **25%** | ~17%（VLCC: 按季度8-24%） |
| **Q1锁定率** | 66%（1月14日）→ 85%+ | VLCC 92% / 全船队 84% |
| **期租费率（VLCC）** | $43,300-49,400/日 | $76,900-93,500/日（近期） |
| **利润分享期租** | 有 — 部分长期租约含指数挂钩上行参与 | 部分有 |
| **FFA对冲** | 未披露 | 战术性衍生品（规模未公开） |
| **杠杆率（D/E）** | 0.38x | 1.31x |

### P2. 盈利对VLCC运价的敏感性（已修正：DHT按75%现货）

| VLCC运价 | DHT利润 | DHT每股收益 | FRO利润 | FRO每股收益 | FRO/DHT利润 | FRO/DHT EPS |
|----------|---------|-------------|---------|-------------|------------|-------------|
| $25K（盈亏平衡） | $54M | $0.33 | $116M | $0.52 | 2.17x | 1.57x |
| $40K（悲观） | $152M | $0.95 | $427M | $1.91 | 2.80x | 2.02x |
| $75K（中性） | $382M | $2.37 | $1,154M | $5.17 | 3.02x | 2.18x |
| **$107K（2026年Q1）** | **$592M** | **$3.68** | **$1,820M** | **$8.16** | **3.07x** | **2.22x** |
| $120K | $678M | $4.21 | $2,090M | $9.37 | 3.08x | 2.22x |
| $150K（牛市） | $875M | $5.43 | $2,710M | $12.15 | 3.10x | 2.24x |
| $200K（超级周期） | $1,203M | $7.47 | $3,748M | $16.81 | 3.12x | 2.25x |

**对比旧模型（54%现货）**：DHT在$107K的EPS从$3.02升至$3.68（+22%）。FRO/DHT EPS比率
从2.70x收窄至2.22x — FRO每股仍赚更多，但差距明显缩小。

**每$1K VLCC运价上涨：**
- DHT（75%现货）：**$6.6M**额外利润 → **每股$0.041**（原54%现货时为$0.029）
- FRO：**$20.8M**额外利润 → **每股$0.093**
- 比率：3.2x（原为4.4x）— DHT的战略转型多捕获39%的运价上行

### P3. 盈利弹性（运价+10% → 利润变化，已修正）

| 基础VLCC运价 | DHT利润变化 | FRO利润变化 | 谁受益更多 |
|-------------|-------------|-------------|-----------|
| $50K | +15.2% | +16.4% | FRO（微弱） |
| $75K | +12.7% | +13.5% | FRO（略） |
| $100K | +11.8% | +12.4% | FRO（略） |
| $150K | +11.2% | +11.5% | FRO（边际） |
| $200K | +10.8% | +11.1% | FRO（边际） |

**关键变化**：在75%现货下，DHT的弹性大幅趋近FRO。$100K以上差异仅0.5-0.6个百分点。

### P4. 期租底线与下行保护（已修正）

| 指标 | DHT（75%现货） | DHT（旧54%现货） | FRO |
|------|:-:|:-:|:-:|
| **期租底线（毛）** | $54M/年（每股$0.33） | $98M/年（每股$0.61） | $202M/年（每股$0.90） |
| **年利息成本** | ~$20M | ~$20M | ~$155M |
| **期租底线（扣利息）** | **$34M（每股$0.21）** | $78M（每股$0.49） | **$47M（每股$0.21）** |
| **最低可持续股息率** | **1.1%** | 2.5% | **0.6%** |

**关键更新**：DHT转向75%现货**大幅削弱了其下行保护**。期租底线从$98M降至$54M。
扣除利息后，DHT和FRO的每股最低保障趋同至~$0.21——本质上相同。
**DHT正在牺牲防御优势换取上行空间。**"债券+权益上行"的定位不再完全适用。

### P5. 稳定性评分（已修正）

| 维度 | DHT（75%现货） | DHT（旧54%） | FRO | 变化说明 |
|------|:-:|:-:|:-:|---|
| 收入可预测性 | **5** | 7.4 | **3** | DHT减少期租，可预测性下降 |
| 分红稳定性 | **6** | 7.8 | **4** | 期租底线缩减=更少缓冲 |
| 盈利波动性 | **4** | 6.6 | **2** | 更多现货=更高波动 |
| 下行保护 | **6** | 8.0 | **3.5** | D/E 0.38仍有优势，但底线减半 |
| 上行捕获 | **7** | 5.2 | **10** | 从5→7显著提升 |
| **综合评分** | **5.6** | 7.0 | **4.5** | 差距从2.5分收窄至1.1分 |

### P6. FFA影响评估

FRO的"战术性衍生品"估计覆盖5-10%有效对冲。
DHT 25%期租 vs FRO ~22-27%有效覆盖——两家公司**风险敞口正在趋同**。
这解释了为何两只股票近3个月走势高度相似。

### P7. 各模型定性描述

| 模型 | DHT | FRO |
|------|-----|-----|
| **Opus 4.6** | "附带权益上行的债券" | "运价的杠杆看涨期权" |
| **Sonnet 4.6** | "均衡堡垒" | "纯周期杠杆" |
| **GPT-5.2** | "波动性管理的现货标的" | "运力市场的高贝塔工具" |
| **GPT-5.1** | "领口期权式VLCC" | "超级周期杠杆看涨期权" |
| **Gemini 3 Pro** | "对冲收益策略" | "经营杠杆怪兽" |

**修正后**：DHT在75%现货下更接近"低杠杆VLCC纯现货标的"，不再是防御型。

### P8. 场景推荐（已更新）

| 市场场景 | VLCC运价 | 优选 | 理由 |
|---------|---------|------|------|
| 持续下行 | $25-40K | **DHT** | 低杠杆（D/E 0.38 vs 1.31）是剩余优势 |
| 复苏 | $40-65K | **DHT（略）** | 杠杆优势此时权重更大 |
| 正常市场 | $65-90K | **平手** | 两者现货敞口相近；FRO有规模优势 |
| 牛市 | $90-120K | **FRO** | 规模（81 vs 24船）+ 多船型 |
| 超级周期 | $120-150K+ | **FRO** | 绝对盈利能力主导 |
| 需求冲击飙升 | $200K+ | **FRO** | $16.81 vs $7.47 EPS（2.25x） |

### P9. 当前运价估值对比（$107K，已修正）

| 指标 | DHT（修正） | FRO | 优势 |
|------|:---:|:---:|:---:|
| 年利润 | $592M | $1,820M | FRO（3.1x） |
| 每股收益 | $3.68 | $8.16 | FRO（2.2x） |
| 市盈率 | **5.3x** | **4.7x** | FRO（更便宜） |
| EV/利润 | **5.9x** | **6.2x** | **DHT（EV口径更便宜）** |
| 股息率（80%派息） | **15.1%** | **17.1%** | FRO（高2pp） |
| 每$10K运价增EPS | **+$0.41** | **+$0.93** | FRO（2.3x） |

**DHT在EV/利润口径下实际比FRO更便宜。**

### P10. 租约策略结论（修订版）

**趋同论点**：DHT正从防御型对冲策略进化为低杠杆版FRO策略。
两家公司现货敞口75-83%，差异仅在：

- **FRO优势**：规模（3.4倍船数）、多船型分散、更高绝对盈利
- **DHT优势**：低杠杆（D/E 0.38 vs 1.31）、EV口径更便宜、更低金融风险

**修订后的配置建议（2026-2028超级周期）：**

| 配置 | 理由 |
|------|------|
| **FRO: 55-60%** | 仍为高贝塔标的，但DHT差距缩小 |
| **DHT: 40-45%** | 风险调整后回报优于此前模型；低杠杆+接近FRO的上行捕获 |

*此前配置为FRO 65-70% / DHT 30-35%。DHT战略转型值得更高配置。*

**风控规则**：若运价持续低于$40K超过2季度，DHT低杠杆成为关键差异化因素，
调整为65% DHT / 35% FRO。

**租约结构现在告诉我们**：两家公司都在押注超级周期。
DHT带安全边际做（0.38x D/E），FRO全押（1.31x D/E）。

"""

# ============================================================
# APPLY UPDATES TO FILES
# ============================================================

def replace_module_p(content, new_section, lang='en'):
    """Replace the old Module P section with new one"""
    # Find the start of Module P
    if lang == 'en':
        markers = ['## Module P: Charter Strategy', '## Module P:']
    else:
        markers = ['## 模块P：租约策略', '## 模块P:']
    
    start_idx = -1
    for marker in markers:
        idx = content.find(marker)
        if idx > 0:
            # Find the --- before it
            dash_idx = content.rfind('\n---\n', 0, idx)
            if dash_idx > 0:
                start_idx = dash_idx
            else:
                start_idx = idx
            break
    
    if start_idx < 0:
        print(f"  WARNING: Module P not found in {lang} file, appending instead")
        # Find the last --- before the disclaimer
        disclaimer_markers = ['*Analysis date', '*分析日期']
        for dm in disclaimer_markers:
            di = content.rfind(dm)
            if di > 0:
                dash_before = content.rfind('\n---\n', 0, di)
                if dash_before > 0:
                    return content[:dash_before] + new_section + content[dash_before:]
        return content + new_section
    
    # Find the end of Module P (next major section or disclaimer)
    end_markers = ['*Analysis date', '*分析日期', '*Charts available', '*图表']
    end_idx = len(content)
    
    # Look for the next section that starts with ## and is NOT part of Module P
    # Module P subsections start with ### P
    lines = content[start_idx:].split('\n')
    in_module_p = True
    char_count = 0
    for i, line in enumerate(lines):
        char_count += len(line) + 1
        # If we find a ## that's not ### P (subsection), it's a new module
        if i > 2 and line.startswith('## ') and not line.startswith('### P'):
            # Check if it's a new major section (not Module P)
            if 'Module P' not in line and '模块P' not in line:
                end_idx = start_idx + char_count - len(line) - 1
                # Go back to include the --- before
                dash_before = content.rfind('\n---\n', start_idx, end_idx)
                if dash_before > start_idx:
                    end_idx = dash_before
                break
    
    # Also check for disclaimer at end
    for dm in ['*Analysis date', '*分析日期']:
        di = content.find(dm, start_idx)
        if di > 0 and di < end_idx:
            # Find --- before disclaimer
            dash_before = content.rfind('\n---\n', start_idx, di)
            if dash_before > start_idx:
                end_idx = dash_before
            else:
                end_idx = di
            break
    
    # Also check for "*Charts" or chart references at end of Module P
    charts_markers = ['*Charts available', '*Charts:', '*图表：', '*图表']
    for cm in charts_markers:
        ci = content.find(cm, start_idx)
        if ci > 0 and ci < end_idx + 500:
            # Find end of this line
            newline = content.find('\n', ci)
            if newline > 0:
                end_idx = max(end_idx, newline + 1)
    
    result = content[:start_idx] + new_section + content[end_idx:]
    return result

# Process EN file
en_path = os.path.join(base, '05_Deep_Dive_Day1Global_Framework.md')
with open(en_path, 'r', encoding='utf-8') as f:
    en_content = f.read()

en_new = replace_module_p(en_content, en_new_module_p, 'en')
with open(en_path, 'w', encoding='utf-8') as f:
    f.write(en_new)
print(f"EN report: {len(en_content)} -> {len(en_new)} chars, {en_new.count(D)} $ signs")

# Process CN file
cn_path = os.path.join(base, '06_Deep_Dive_Day1Global_Framework_CN.md')
with open(cn_path, 'r', encoding='utf-8') as f:
    cn_content = f.read()

cn_new = replace_module_p(cn_content, cn_new_module_p, 'cn')
with open(cn_path, 'w', encoding='utf-8') as f:
    f.write(cn_new)
print(f"CN report: {len(cn_content)} -> {len(cn_new)} chars, {cn_new.count(D)} $ signs")

# Update index.md (copy of CN)
index_path = os.path.join(base, 'index.md')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(cn_new)
print(f"index.md updated (copy of CN)")

# Verify $ counts match
en_d = en_new.count(D)
cn_d = cn_new.count(D)
print(f"\n$ sign check: EN={en_d}, CN={cn_d}")

# Quick sanity: check key numbers appear
for label, content_check in [('EN', en_new), ('CN', cn_new)]:
    checks = ['75%', '$3.68', '$0.041', '3.2x', '$592M', '5.3x']
    missing = [c for c in checks if c not in content_check]
    if missing:
        print(f"WARNING {label}: missing {missing}")
    else:
        print(f"{label}: all key corrected numbers present")

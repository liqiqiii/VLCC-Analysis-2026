#!/usr/bin/env python3
"""Append charter strategy section to both EN and CN reports"""
import os

base = r'C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026'

# ============================================================
# ENGLISH SECTION
# ============================================================
en_section = r"""

---

## Module P: Charter Strategy & Rate Sensitivity Analysis (5-Model Consensus)

> **The Question**: DHT runs ~54% spot / 46% TC (time charter). FRO runs ~83% spot / 17% TC.
> How does this charter mix difference affect earnings sensitivity, dividend stability,
> and investment positioning in a supply-driven super cycle?

### P1. Charter Mix Overview

| Metric | DHT Holdings | Frontline (FRO) |
|--------|:---:|:---:|
| **Fleet** | 24 VLCCs (pure play) | 42V + 21S + 18LR2 (81 ships) |
| **Spot exposure** | 54% | ~83% fleet-wide |
| **TC coverage** | 46% | ~17% (VLCC: 15%) |
| **TC policy** | ~50/50 balanced target | "Golden rule": TC < 30% |
| **TC rate (VLCC)** | $49,400/day avg | $85,000/day avg (recent) |
| **Profit-sharing TC** | Yes — index-linked upside on long TCs | Some, less structural |
| **FFA hedging** | None disclosed | Tactical derivatives (undisclosed) |
| **D/E ratio** | 0.38x | 1.31x |

**Key Insight**: DHT's profit-sharing TCs are NOT traditional hedges. They provide a $41-52K floor
PLUS proportional upside participation — making DHT's effective spot exposure ~60-65% in bull markets.

### P2. Earnings Sensitivity to VLCC Rates (Quantitative Model)

| VLCC Rate | DHT Profit | DHT EPS | FRO Profit | FRO EPS | FRO/DHT | FRO EPS/DHT EPS |
|-----------|-----------|---------|-----------|---------|---------|-----------------|
| $25K (BE) | $98M | $0.61 | $116M | $0.52 | 1.18x | 0.85x |
| $40K (Bear) | $169M | $1.05 | $427M | $1.91 | 2.52x | 1.82x |
| $75K (Mid) | $335M | $2.08 | $1,154M | $5.17 | 3.44x | 2.49x |
| **$107K (Q1 2026)** | **$487M** | **$3.02** | **$1,820M** | **$8.16** | **3.74x** | **2.70x** |
| $120K | $548M | $3.40 | $2,090M | $9.37 | 3.81x | 2.75x |
| $150K (Bull) | $690M | $4.29 | $2,710M | $12.15 | 3.93x | 2.83x |
| $200K (Super) | $926M | $5.75 | $3,748M | $16.81 | 4.05x | 2.92x |

**The Math**: For every $1K increase in VLCC rates:
- DHT captures **$4.7M** additional profit → **$0.029/share**
- FRO captures **$20.8M** additional profit → **$0.093/share** (3.2× more per share)

### P3. Earnings Elasticity (+10% Rate → Profit Change)

| Base VLCC Rate | DHT Profit Change | FRO Profit Change | Who Benefits More |
|----------------|-------------------|-------------------|-------------------|
| $50K | +10.9% | +16.4% | FRO |
| $75K | +10.6% | +13.5% | FRO |
| $100K | +10.4% | +12.4% | FRO |
| $150K | +10.3% | +11.5% | FRO |
| $200K | +10.2% | +11.1% | FRO |

FRO always benefits more, with the elasticity gap widest at lower rates (where operating leverage
is highest) and converging at very high rates.

### P4. TC Earnings Floor & Downside Protection

| Metric | DHT | FRO |
|--------|-----|-----|
| **TC floor (gross)** | $98M/yr ($0.61/sh) | $202M/yr ($0.90/sh) |
| **Annual interest cost** | ~$20M | ~$155M |
| **TC floor (net of interest)** | **$78M ($0.49/sh)** | **$47M ($0.21/sh)** |
| **Minimum sustainable yield** | **2.5%** | **0.6%** |

*This is the single most important downside metric.* Despite FRO's higher gross TC floor ($202M vs $98M),
its 3.4× higher debt leverage consumes most of that cushion. At zero spot revenue:
- **DHT can maintain a $0.49/share dividend** — a livable 2.5% floor yield
- **FRO drops to $0.21/share** — likely triggering a dividend cut to zero

### P5. Stability Scorecard (5-Model Consensus, 1-10 Scale)

| Dimension | DHT (Avg) | FRO (Avg) | Range DHT | Range FRO |
|-----------|:---------:|:---------:|:---------:|:---------:|
| Revenue Predictability | **7.4** | **3.0** | 7-8 | 3 |
| Dividend Stability | **7.8** | **4.0** | 7-9 | 4 |
| Earnings Volatility (low=good) | **6.6** | **2.0** | 6-7 | 2-3 |
| Downside Protection | **8.0** | **3.6** | 7-9 | 3-5 |
| Upside Capture | **5.2** | **10.0** | 5-6 | 10 |
| **Composite** | **7.0** | **4.5** | | |

All 5 models unanimously rate FRO 10/10 on upside capture and DHT 7-9 on downside protection.

### P6. FFA Impact Assessment

FRO's "tactical derivatives" likely represent 5-10% effective hedge coverage:
- **Stated physical TC coverage**: ~17% fleet-wide
- **Estimated FFA overlay**: +5-10% synthetic coverage
- **Effective total coverage**: ~22-27% (still well below DHT's 46%)

The FFA program is a **tactical overlay, not a strategic hedge** — it provides quarter-to-quarter
smoothing, not cycle-level protection. In a super-cycle, FFAs could actually *cost* FRO 3-5% of
peak earnings via opportunity cost on hedged forward positions.

### P7. Model Characterizations (How Each Model Described the Stocks)

| Model | DHT Characterization | FRO Characterization |
|-------|---------------------|---------------------|
| **Opus 4.6** | "Bond with an equity kicker" | "Leveraged call option on tanker rates" |
| **Sonnet 4.6** | "Balanced Fortress" / "Structured compounding" | "Pure Cycle Leverage, Maximum Asymmetry" |
| **GPT-5.2** | "Volatility-managed spot name" | "High-beta instrument on freight" |
| **GPT-5.1** | "Collared VLCC play — floor + partial upside" | "Levered call option on a supercycle" |
| **Gemini 3 Pro** | "Hedged Yield strategy" | "Operating Leverage Monster" |

### P8. Scenario Recommendation Matrix (5-Model Consensus)

| Market Scenario | VLCC Rate | Winner | Consensus |
|-----------------|-----------|--------|-----------|
| Extended downcycle | $25-40K | **DHT** | 5/5 models |
| Recovery | $40-65K | **DHT (slight)** | 4/5 models |
| Normal market | $65-90K | **FRO (slight)** | 3/5 models |
| Bull market | $90-120K | **FRO decisively** | 5/5 models |
| Super cycle | $120-150K+ | **FRO overwhelmingly** | 5/5 models |
| Demand shock spike | $200K+ | **FRO only choice** | 5/5 models |

### P9. Key Valuation at Current Rates ($107K)

| Metric | DHT | FRO | Advantage |
|--------|-----|-----|-----------|
| P/E | 6.4x | 4.7x | FRO (cheaper) |
| EV/Profit | 7.2x | 6.2x | FRO (cheaper) |
| Dividend yield (80% payout) | 12.4% | 17.1% | FRO (higher) |
| EPS sensitivity per $10K rate | +$0.29 | +$0.93 | FRO (3.2× more) |

**FRO is already cheaper than DHT at current rates** — the market is either discounting leverage risk
or hasn't fully priced in the super-cycle thesis.

### P10. Charter Strategy Conclusion

**For the 2026-2028 supply-driven super cycle:**

| Allocation | Rationale |
|------------|-----------|
| **FRO: 65-70%** | Maximum earnings leverage. At $150K sustained, FRO yields 25.5% dividend on current price. 4.4× upside capture per $1K rate move. |
| **DHT: 30-35%** | Portfolio insurance + income anchor. TC floor protects against cycle disappointment. Profit-sharing TCs still capture 30-50% upside. |

**Risk management rule**: If rates sustain below $50K for 2+ quarters, flip to 60% DHT / 40% FRO.

**The charter mix reveals management's letter to shareholders:**
- **DHT's letter says**: "Trust us to protect your capital while participating in the upside"
- **FRO's letter says**: "Trust us to make you rich — if the market cooperates"

*Charts available: See /charts/ folder for 6 visualization files (profit sensitivity, EPS curves, elasticity bars, profit ratio, charter mix pies, scenario comparison).*

"""

# ============================================================
# CHINESE SECTION
# ============================================================
cn_section = r"""

---

## 模块P：租约策略与运价敏感性分析（5模型共识）

> **核心问题**：DHT运营约54%现货/46%期租组合。FRO运营约83%现货/17%期租。
> 这种租约结构差异如何影响盈利敏感性、分红稳定性以及在供给驱动超级周期中的投资定位？

### P1. 租约结构对比

| 指标 | DHT Holdings | Frontline (FRO) |
|------|:---:|:---:|
| **船队** | 24艘VLCC（纯VLCC） | 42V + 21S + 18LR2（81艘） |
| **现货敞口** | 54% | ~83%（全船队） |
| **期租覆盖** | 46% | ~17%（VLCC: 15%） |
| **期租策略** | ~50/50均衡目标 | "黄金法则"：期租<30% |
| **期租费率（VLCC）** | 日均$49,400 | 日均$85,000（近期） |
| **利润分享期租** | 有 — 与指数挂钩的上行参与 | 部分有，非结构性 |
| **FFA对冲** | 未披露 | 战术性衍生品（规模未公开） |
| **杠杆率（D/E）** | 0.38x | 1.31x |

**关键洞察**：DHT的利润分享期租并非传统对冲。它们提供$41-52K的保底
加上按比例的上行参与——使DHT在牛市中的实际现货敞口约为60-65%，而非54%。

### P2. 盈利对VLCC运价的敏感性（量化模型）

| VLCC运价 | DHT利润 | DHT每股收益 | FRO利润 | FRO每股收益 | FRO/DHT | 每股收益比 |
|----------|---------|-------------|---------|-------------|---------|-----------|
| $25K（盈亏平衡） | $98M | $0.61 | $116M | $0.52 | 1.18x | 0.85x |
| $40K（悲观） | $169M | $1.05 | $427M | $1.91 | 2.52x | 1.82x |
| $75K（中性） | $335M | $2.08 | $1,154M | $5.17 | 3.44x | 2.49x |
| **$107K（2026年Q1）** | **$487M** | **$3.02** | **$1,820M** | **$8.16** | **3.74x** | **2.70x** |
| $120K | $548M | $3.40 | $2,090M | $9.37 | 3.81x | 2.75x |
| $150K（牛市） | $690M | $4.29 | $2,710M | $12.15 | 3.93x | 2.83x |
| $200K（超级周期） | $926M | $5.75 | $3,748M | $16.81 | 4.05x | 2.92x |

**核心数学**：VLCC运价每上涨$1K：
- DHT捕获**$4.7M**额外利润 → **每股$0.029**
- FRO捕获**$20.8M**额外利润 → **每股$0.093**（每股多3.2倍）

### P3. 盈利弹性（运价+10% → 利润变化）

| 基础VLCC运价 | DHT利润变化 | FRO利润变化 | 谁受益更多 |
|-------------|-------------|-------------|-----------|
| $50K | +10.9% | +16.4% | FRO |
| $75K | +10.6% | +13.5% | FRO |
| $100K | +10.4% | +12.4% | FRO |
| $150K | +10.3% | +11.5% | FRO |
| $200K | +10.2% | +11.1% | FRO |

FRO始终受益更多，弹性差距在低费率时最大（经营杠杆最高），在极高费率时趋于收敛。

### P4. 期租收益底线与下行保护

| 指标 | DHT | FRO |
|------|-----|-----|
| **期租底线（毛）** | $98M/年（每股$0.61） | $202M/年（每股$0.90） |
| **年利息成本** | ~$20M | ~$155M |
| **期租底线（扣除利息）** | **$78M（每股$0.49）** | **$47M（每股$0.21）** |
| **最低可持续股息率** | **2.5%** | **0.6%** |

*这是最重要的下行风险指标。*尽管FRO毛期租底线更高（$202M vs $98M），
但其3.4倍的债务杠杆消耗了大部分缓冲。在现货收入为零时：
- **DHT可维持每股$0.49分红** — 2.5%的最低股息率
- **FRO降至每股$0.21** — 可能触发分红归零

### P5. 稳定性评分（5模型共识，1-10分制）

| 维度 | DHT（均值） | FRO（均值） | DHT范围 | FRO范围 |
|------|:---------:|:---------:|:-------:|:-------:|
| 收入可预测性 | **7.4** | **3.0** | 7-8 | 3 |
| 分红稳定性 | **7.8** | **4.0** | 7-9 | 4 |
| 盈利波动性（低=好） | **6.6** | **2.0** | 6-7 | 2-3 |
| 下行保护 | **8.0** | **3.6** | 7-9 | 3-5 |
| 上行捕获 | **5.2** | **10.0** | 5-6 | 10 |
| **综合评分** | **7.0** | **4.5** | | |

全部5个模型一致给FRO上行捕获10/10分，给DHT下行保护7-9分。

### P6. FFA影响评估

FRO的"战术性衍生品"可能代表5-10%的有效对冲覆盖：
- **物理期租覆盖（公开）**：~17%全船队
- **估算FFA覆盖**：+5-10%合成覆盖
- **有效总覆盖**：~22-27%（仍远低于DHT的46%）

FFA是**战术层面的叠加，而非战略对冲**——提供季度间的平滑，
而非周期级保护。在超级周期中，FFA可能实际*消耗*FRO 3-5%的峰值盈利。

### P7. 各模型定性描述

| 模型 | DHT定性 | FRO定性 |
|------|---------|---------|
| **Opus 4.6** | "附带权益上行的债券" | "运价的杠杆看涨期权" |
| **Sonnet 4.6** | "均衡堡垒/结构化复利" | "纯周期杠杆，最大非对称性" |
| **GPT-5.2** | "波动性管理的现货标的" | "运力市场的高贝塔工具" |
| **GPT-5.1** | "领口期权式VLCC——有底+部分上行" | "超级周期的杠杆看涨期权" |
| **Gemini 3 Pro** | "对冲收益策略" | "经营杠杆怪兽" |

### P8. 场景推荐矩阵（5模型共识）

| 市场场景 | VLCC运价 | 优选 | 共识 |
|---------|---------|------|------|
| 持续下行周期 | $25-40K | **DHT** | 5/5模型 |
| 复苏期 | $40-65K | **DHT（略优）** | 4/5模型 |
| 正常市场 | $65-90K | **FRO（略优）** | 3/5模型 |
| 牛市 | $90-120K | **FRO明显优** | 5/5模型 |
| 超级周期 | $120-150K+ | **FRO压倒性优势** | 5/5模型 |
| 需求冲击飙升 | $200K+ | **只有FRO** | 5/5模型 |

### P9. 当前运价下的估值对比（$107K）

| 指标 | DHT | FRO | 优势 |
|------|-----|-----|------|
| 市盈率 | 6.4x | 4.7x | FRO（更便宜） |
| EV/利润 | 7.2x | 6.2x | FRO（更便宜） |
| 股息率（80%派息） | 12.4% | 17.1% | FRO（更高） |
| 每$10K运价的EPS敏感度 | +$0.29 | +$0.93 | FRO（多3.2倍） |

**FRO在当前运价下已经比DHT便宜**——市场要么在折价其杠杆风险，
要么尚未完全定价超级周期论点。

### P10. 租约策略结论

**针对2026-2028供给驱动超级周期：**

| 配置 | 理由 |
|------|------|
| **FRO: 65-70%** | 最大盈利杠杆。$150K持续时，FRO以当前价格计的股息率达25.5%。每$1K运价变动捕获4.4倍于DHT。 |
| **DHT: 30-35%** | 组合保险+收益锚。期租底线防范周期不达预期。利润分享期租仍捕获30-50%上行。 |

**风险管理规则**：若运价持续低于$50K超过2个季度，调整为60% DHT / 40% FRO。

**租约结构揭示了管理层写给股东的信：**
- **DHT的信说**："相信我们能保护你的资本，同时参与上行"
- **FRO的信说**："相信我们能让你致富——如果市场配合的话"

*图表：参见/charts/文件夹，包含6个可视化文件（利润敏感性、EPS曲线、弹性柱状图、利润比率、租约组合饼图、场景对比）。*

"""

# Append to EN report
en_path = os.path.join(base, '05_Deep_Dive_Day1Global_Framework.md')
with open(en_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove trailing disclaimer to append before it
disclaimer = "\n---\n\n*Analysis date: March 2, 2026."
if disclaimer in content:
    idx = content.index(disclaimer)
    before_disclaimer = content[:idx]
    after_disclaimer = content[idx:]
    new_content = before_disclaimer + en_section + after_disclaimer
else:
    new_content = content + en_section

with open(en_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify $ count
en_dollars = new_content.count('$')
print(f"EN report updated: {len(new_content)} chars, {en_dollars} $ signs")

# Append to CN report
cn_path = os.path.join(base, '06_Deep_Dive_Day1Global_Framework_CN.md')
with open(cn_path, 'r', encoding='utf-8') as f:
    cn_content = f.read()

cn_disclaimer_markers = ["*分析日期", "*Analysis date", "---\n\n*"]
cn_split_done = False
for marker in cn_disclaimer_markers:
    if marker in cn_content:
        idx = cn_content.rindex(marker)
        # Find the --- before it
        dash_idx = cn_content.rfind('\n---\n', 0, idx)
        if dash_idx > 0:
            before = cn_content[:dash_idx]
            after = cn_content[dash_idx:]
            cn_new = before + cn_section + after
            cn_split_done = True
            break

if not cn_split_done:
    cn_new = cn_content + cn_section

with open(cn_path, 'w', encoding='utf-8') as f:
    f.write(cn_new)

cn_dollars = cn_new.count('$')
print(f"CN report updated: {len(cn_new)} chars, {cn_dollars} $ signs")

# Also update the index.md for GitHub Pages
index_path = os.path.join(base, 'index.md')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(cn_new)
print(f"index.md updated (copy of CN report)")

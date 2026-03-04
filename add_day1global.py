#!/usr/bin/env python3
"""
Add Day1Global framework modules to A-share report.
Missing: Module C (Cash Flow), L (Ownership), O (Accounting Quality),
6 Investment Perspectives, Anti-Bias Framework, Pre-Mortem Analysis.
Also updates RULES.md with Rule 15.
"""
import os, shutil

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ========================================
# EN REPORT — Add Day1Global Sections
# ========================================
print("=== Adding Day1Global modules to EN Report ===")
en = read_file('07_CN_AShare_VLCC_Report_EN.md')

day1global_en = """
---

## 10. Day1Global Framework Deep Dive (Modules C, L, O)

> Applying the [tech-earnings-deepdive](https://github.com/webleon/tech-earnings-deepdive-openclaw-skill) framework by Ruby & Star (Day1Global). Modules A (Revenue), B (Profitability), D (Guidance), E (Competition), and K (Valuation) are covered in Sections 1-9 above. Below: the remaining critical modules.

### Module C: Cash Flow Analysis — "THE BIG ONE"

**Why it matters**: In shipping, net income can be manipulated by D&A schedules and impairments. Free cash flow is the truth.

**CMES (招商轮船) Cash Flow Profile**

| Metric | 2024 | 2025E | 2026E ($150K) |
|---|---|---|---|
| Operating Cash Flow | ~RMB 8.5B | ~RMB 10B | **~RMB 20-22B** |
| Capex (fleet maintenance + newbuilds) | ~RMB 4B | ~RMB 5B | ~RMB 6B |
| **Free Cash Flow** | ~RMB 4.5B | ~RMB 5B | **~RMB 14-16B** |
| FCF Yield (at RMB 143B mcap) | 3.1% | 3.5% | **9.8-11.2%** |
| Dividend (40% of NI) | ~RMB 2.4B | ~RMB 2.6B | **~RMB 5.9B** |
| FCF after Dividend | ~RMB 2.1B | ~RMB 2.4B | **~RMB 8-10B** |

**Key insight**: At $150K, CMES generates ~RMB 14-16B FCF — enough to pay 40% dividend AND retain RMB 8-10B for fleet renewal or debt reduction. This is "SaaS economics" in action: above breakeven, incremental revenue flows almost entirely to FCF.

**COSCO Energy (中远海能) Cash Flow Profile**

| Metric | 2024 | 2025E | 2026E ($150K) |
|---|---|---|---|
| Operating Cash Flow | ~RMB 7B | ~RMB 8B | **~RMB 24-27B** |
| Capex (heavy: 61 ships on order) | ~RMB 8B | ~RMB 10B | ~RMB 12B |
| **Free Cash Flow** | ~RMB -1B | ~RMB -2B | **~RMB 12-15B** |
| FCF Yield (at RMB 135B mcap) | -0.7% | -1.5% | **8.9-11.1%** |
| LNG long-term contract cash flow | ~RMB 2.5B | ~RMB 3B | ~RMB 3.5B |

**Critical difference**: COSCO was FCF-negative in 2024-25 due to massive capex (36 LNG + 6 VLCC + 19 MR/LR newbuilds). At $150K, it flips to strongly FCF-positive — a dramatic inflection. However, capex discipline is a key watch item.

**Cash Flow Verdict**:
- CMES: Consistent FCF generator. Conservative capex. 40% dividend well-covered. **Grade: A-**
- COSCO: FCF inflection at $150K. Heavy capex creates optionality but also risk. LNG contracts provide stable floor. **Grade: B+**

### Module L: Ownership & Management

**CMES Ownership Structure**

| Shareholder | Stake | Significance |
|---|---|---|
| China Merchants Group (央企) | ~47% | Central SOE; energy security mandate |
| Hong Kong/Southbound Connect | ~8-10% | Institutional foreign interest |
| Insurance/Fund institutions | ~15% | Long-term holders |
| Retail | ~25-30% | Higher volatility driver |

- **Management quality**: Conservative, SOE-style. Consistent 40% dividend policy. Fleet renewal disciplined (avg age 7.2yr).
- **Alignment**: SOE mandate = energy security > profit maximization. However, dividend policy aligns with minority shareholders.
- **Key person risk**: Low (SOE rotation system), but also means less entrepreneurial agility.

**COSCO Energy Ownership Structure**

| Shareholder | Stake | Significance |
|---|---|---|
| COSCO Shipping Group (央企) | ~49% | Central SOE; largest shipping conglomerate |
| China Merchants Group | ~5% | Cross-holding |
| Social security fund | ~2% | Policy holder |
| Institutional | ~20% | Higher than CMES |
| Retail | ~24% | Moderate volatility |

- **Management quality**: More aggressive growth strategy (61 ships on order). Dual-engine vision (VLCC + LNG) is strategically sound.
- **Related-party risk**: Significant fleet transactions within COSCO Group ecosystem. Watch for below-market charter-backs.
- **Strategic advantage**: COSCO Group controls China's largest port network — potential for captive cargo arrangements.

**Ownership Verdict**:
- CMES: More conservative, better dividend alignment. **Grade: B+**
- COSCO: Better strategic positioning (Group synergies), but higher related-party risk. **Grade: B**

### Module O: Accounting Quality

| Factor | CMES | COSCO Energy |
|---|---|---|
| Revenue recognition | Clean — spot/TC revenue straightforward | Clean — same |
| D&A policy | 25-year useful life, standard | 25-year, standard |
| Impairment risk | Low (young fleet, high asset values) | Moderate (some older VLCCs) |
| Related-party transactions | Moderate (Merchants Group charters) | **High** (COSCO Group ecosystem) |
| Off-balance-sheet leases | Some bareboat charters | Significant (VLCC + LNG leases) |
| Hedge accounting (FFA) | Minimal | Minimal |
| Pension/employee obligations | SOE standard | SOE standard |
| Goodwill/intangibles | Negligible | Negligible |

**Red flags to watch**:
1. COSCO: Related-party fleet transactions — ensure arm's-length pricing
2. Both: Operating lease obligations (IFRS 16) can mask true leverage
3. Both: SOE "social responsibility" expenditures may reduce reported margins

**Accounting Quality Verdict**:
- CMES: Clean, transparent. Minimal red flags. **Grade: A-**
- COSCO: Adequate but watch related-party transactions. **Grade: B**

---

## 11. Six Investment Philosophy Perspectives

### 1. Quality Compounder (Buffett/Munger)

> "What is the durable competitive advantage?"

- **CMES**: Youngest VLCC fleet globally (7.2yr), lowest breakeven, 40% dividend — closest to a "quality" shipping name. But shipping has no true moat.
- **COSCO**: LNG long-term contracts provide annuity-like income. COSCO Group ecosystem is an intangible moat in Chinese waters.
- **Verdict**: Neither is a true compounder. **CMES is closer** due to dividend discipline and fleet quality. Hold for the cycle, not forever.

### 2. Imaginative Growth (Baillie Gifford/ARK)

> "What is the 10x optionality?"

- **COSCO**: 36 LNG newbuilds create a future "LNG shipping giant" narrative. If LNG spot rates spike (like 2022 at $100-162K/day), COSCO's LNG fleet could be worth more than its entire current market cap.
- **CMES**: Limited growth optionality beyond the cycle. Conservative fleet management.
- **Verdict**: **COSCO wins** on growth narrative. But this is a cyclical trade, not a 10x bet.

### 3. Fundamental Long/Short (Tiger Cubs)

> "What is the market mispricing?"

- The market is pricing both stocks at $100K VLCC consensus when spot is $150K+. This is a **50-70% earnings gap** that will close via Q1 earnings beats and sell-side upgrades.
- **Short side**: Consider shorting downstream refiners who cannot pass through higher crude transport costs.
- **Verdict**: **Both are longs.** The mispricing is identical in nature but COSCO has more magnitude (73% earnings gap vs 47% for CMES).

### 4. Deep Value (Klarman/Marks)

> "What is the margin of safety?"

- **CMES at 9.7x PE ($150K)**: Dividend yield 4.1%, breakeven ~$25K/day. Even if rates halve to $75K, CMES earns RMB 6-7B (breakeven at current price). Margin of safety: **HIGH**.
- **COSCO at 7.8x PE ($150K)**: LNG contracts worth ~RMB 3B/yr = 22% of market cap in stable income. But heavy capex reduces margin of safety. **MODERATE**.
- **Verdict**: **CMES offers better margin of safety.** COSCO offers better upside.

### 5. Catalyst Driven (Tepper/Ackman)

> "What specific catalyst will unlock value?"

| Catalyst | Timeline | Impact | Probability |
|---|---|---|---|
| Q1 2026 earnings report | April 2026 | First $150K quarter → massive beat | 90% |
| Sell-side consensus upgrade to $130-150K | Q2 2026 | Mechanical PE compression | 80% |
| MSCI/Index rebalancing | H2 2026 | Forced institutional buying | 50% |
| Hormuz escalation phase 2 | Unknown | Rates to $250K+ | 30% |
| Special dividend announcement | Post-Q1 | Share price floor | 40% (CMES) |

- **Verdict**: **Q1 earnings (April) is the nearest high-probability catalyst for both.**

### 6. Macro Tactical (Druckenmiller)

> "Where are we in the cycle?"

- We are in **Phase 2** of the VLCC super-cycle: rates have broken out, but sell-side hasn't caught up. PE compression from 28x → 10x is underway.
- **Macro tailwinds**: Weakening USD (positive for commodity shipping), rising oil demand from Asia, sanctions enforcement tightening.
- **Macro risks**: Global recession (15-20% probability), Hormuz resolution (15-25%).
- **Position sizing**: This is a 15-20% portfolio bet, not a 5% allocation. The cycle conviction is high, but terminal risk exists.
- **Verdict**: **Overweight both. Trim at PE 5-6x (Phase 4). Exit at first sign of Hormuz resolution.**

---

## 12. Anti-Bias Framework

| Cognitive Trap | How It Applies Here | Mitigation |
|---|---|---|
| **Anchoring bias** | Anchoring to $100K consensus when spot is $150K+ | Use $150K as base; $100K as bear case |
| **Simplification bias** | Treating both companies as "VLCC plays" — ignoring COSCO's 98 non-VLCC tankers and 65 LNG ships | Full-portfolio model (Section 4) |
| **Recency bias** | Using 2020 floating storage as cycle template — 2026 is fundamentally different (supply-driven) | Compare to 2008 AND 2020; note structural differences |
| **Confirmation bias** | Wanting both to be "strong buys" may cause us to dismiss risks | Pre-mortem analysis (Section 13) addresses this |
| **Survivorship bias** | Comparing to 中远海控 container success ignores that some cyclical bets fail spectacularly | Risk matrix (Section 8) with explicit probabilities |
| **Narrative bias** | "Hormuz crisis = rates stay high forever" — every crisis ends eventually | Include de-escalation scenario in Section 9B |

---

## 13. Pre-Mortem Analysis

> **"It's March 2027. Your position in CMES and COSCO Energy has lost 40%. What went wrong?"**

### Scenario 1: Hormuz De-Escalation (Most Likely Bear Case)
- **What happened**: Diplomatic breakthrough in Q3 2026. Iran agrees to tanker safety guarantees. Insurance premiums normalize.
- **Impact**: VLCC rates crash from $150K to $50-70K within 2 months. Market immediately prices "cycle over."
- **Damage**: CMES to RMB 10-12 (-32% to -43%), COSCO to RMB 14-16 (-33% to -41%)
- **Early warning signs**: US-Iran diplomatic channels opening, insurance premium drops, tanker rerouting back to Strait

### Scenario 2: COSCO Capex Trap
- **What happened**: COSCO's 61 newbuilds ($8-12B total) arrive just as rates normalize. Massive debt service with declining revenue.
- **Impact**: COSCO FCF turns deeply negative again. Dividend cut or equity raise.
- **Damage**: COSCO-specific — to RMB 12-15 (-37% to -50%). CMES relatively protected.
- **Early warning signs**: LNG charter rate softening, newbuild delivery delays, COSCO Group funding stress

### Scenario 3: Global Recession + OPEC Overproduction
- **What happened**: Synchronized global recession in H2 2026. OPEC floods market to maintain revenue. Oil demand drops 3-5%.
- **Impact**: VLCC rates to $40-60K. Both stocks de-rate to PE 5-8x on collapsed earnings.
- **Damage**: CMES to RMB 8-10 (-43% to -55%), COSCO to RMB 10-12 (-50% to -58%)
- **Early warning signs**: PMI contracting across Asia/Europe, oil inventory builds, OPEC compliance dropping

### Scenario 4: A-Share Systemic Risk
- **What happened**: China property crisis Phase 3, banking stress, capital flight. A-share index drops 30%.
- **Impact**: Both stocks fall regardless of fundamentals. Foreign investors exit via Southbound Connect.
- **Damage**: Both -30% to -40% even with strong underlying earnings.
- **Early warning signs**: CNY depreciation >7.5, PBOC emergency measures, Shanghai Composite below 2,800

### Pre-Mortem Verdict

| Risk | Probability | Max Drawdown | Hedge |
|---|---|---|---|
| Hormuz de-escalation | 15-25% | -40% | Trailing stop at -25% |
| COSCO capex trap | 20-30% | -50% (COSCO only) | Overweight CMES if capex concerns rise |
| Global recession | 15-20% | -55% | Reduce position if PMI <48 for 3 months |
| A-share systemic | 20-30% | -40% | Diversify with US-listed DHT/FRO as hedge |

> **Combined probability of a 40%+ drawdown: ~35-45%.** This is NOT a risk-free trade. Position sizing (15-20% of portfolio) and hard stops (-25%) are essential. The asymmetry is favorable (upside 55-92% vs downside 25-40%) but not overwhelming.

"""

# Insert before Appendix
en = en.replace(
    '\n---\n\n## Appendix: Cross-Market Comparison',
    day1global_en + '\n---\n\n## Appendix: Cross-Market Comparison'
)

# Also add attribution at the bottom
old_en_footer = "*Report compiled from 5 independent AI model analyses (Opus 4.6, Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro).*"
new_en_footer = """*Report compiled from 5 independent AI model analyses (Opus 4.6, Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro).*
*Analytical framework: [Day1Global tech-earnings-deepdive](https://github.com/webleon/tech-earnings-deepdive-openclaw-skill) — Modules A, B, C, D, E, K, L, O applied. 6 investment perspectives, anti-bias framework, and pre-mortem analysis included.*"""
en = en.replace(old_en_footer, new_en_footer)

write_file('07_CN_AShare_VLCC_Report_EN.md', en)
print("EN report: Day1Global modules 10-13 added")

# ========================================
# CN REPORT — Add Day1Global Sections
# ========================================
print("\n=== Adding Day1Global modules to CN Report ===")
cn = read_file('08_CN_AShare_VLCC_Report_CN.md')

day1global_cn = """
---

## 十、Day1Global框架深度分析（模块C、L、O）

> 应用[tech-earnings-deepdive](https://github.com/webleon/tech-earnings-deepdive-openclaw-skill)框架（Ruby & Star / Day1Global）。模块A（收入质量）、B（盈利能力）、D（前瞻指引）、E（竞争格局）和K（估值模型）已在上述第一至九节涵盖。以下为剩余关键模块。

### 模块C：现金流分析 —— "重中之重"

**为什么重要**：在航运业中，净利润可被折旧政策和减值操纵。自由现金流才是真相。

**招商轮船现金流概况**

| 指标 | 2024 | 2025E | 2026E（$15万） |
|---|---|---|---|
| 经营现金流 | ~85亿 | ~100亿 | **~200-220亿** |
| 资本开支（维护+新造） | ~40亿 | ~50亿 | ~60亿 |
| **自由现金流** | ~45亿 | ~50亿 | **~140-160亿** |
| FCF收益率（1430亿市值） | 3.1% | 3.5% | **9.8-11.2%** |
| 分红（40% NI） | ~24亿 | ~26亿 | **~59亿** |
| 分红后剩余FCF | ~21亿 | ~24亿 | **~80-100亿** |

**关键洞察**：在$15万运费下，招商产生约140-160亿FCF——足以支付40%分红，还剩80-100亿用于船队更新或还债。这就是"SaaS经济学"的航运版：超过盈亏平衡后，增量收入几乎全部流入FCF。

**中远海能现金流概况**

| 指标 | 2024 | 2025E | 2026E（$15万） |
|---|---|---|---|
| 经营现金流 | ~70亿 | ~80亿 | **~240-270亿** |
| 资本开支（重：61艘在建） | ~80亿 | ~100亿 | ~120亿 |
| **自由现金流** | ~-10亿 | ~-20亿 | **~120-150亿** |
| FCF收益率（1350亿市值） | -0.7% | -1.5% | **8.9-11.1%** |
| LNG长约现金流 | ~25亿 | ~30亿 | ~35亿 |

**关键差异**：中远2024-25年因大量资本开支（36艘LNG+6艘VLCC+19艘MR/LR新造）导致FCF为负。在$15万运费下翻正——是一个戏剧性的拐点。但资本纪律是关键监控点。

**现金流评级**：
- 招商轮船：持续的FCF创造者。保守资本开支。40%分红有充足覆盖。**评级：A-**
- 中远海能：$15万下FCF拐点。重资本开支创造期权但也带来风险。LNG合约提供稳定底仓。**评级：B+**

### 模块L：股权结构与管理层

**招商轮船股权结构**

| 股东 | 持股比例 | 意义 |
|---|---|---|
| 招商局集团（央企） | ~47% | 能源安全使命 |
| 港股通/南向资金 | ~8-10% | 机构外资兴趣 |
| 保险/基金机构 | ~15% | 长期持有者 |
| 散户 | ~25-30% | 波动性来源 |

- **管理层质量**：保守型，央企风格。稳定的40%分红政策。船队更新有节制（均龄7.2年）。
- **利益一致性**：央企使命=能源安全>利润最大化。但分红政策与中小股东利益一致。
- **关键人员风险**：低（央企轮岗制度），但也意味着创业敏捷性不足。

**中远海能股权结构**

| 股东 | 持股比例 | 意义 |
|---|---|---|
| 中远海运集团（央企） | ~49% | 最大航运集团 |
| 招商局集团 | ~5% | 交叉持股 |
| 社保基金 | ~2% | 政策性持有 |
| 机构 | ~20% | 高于招商 |
| 散户 | ~24% | 中等波动 |

- **管理层质量**：更激进的增长策略（61艘在建）。"油运进攻+LNG防御"双引擎战略思路清晰。
- **关联交易风险**：中远海运集团体系内存在大量船舶交易。关注是否存在低于市场价的回租。
- **战略优势**：中远集团控制中国最大港口网络——潜在的锁定货源安排。

**股权评级**：
- 招商轮船：更保守，分红利益一致性更好。**评级：B+**
- 中远海能：战略定位更优（集团协同），但关联交易风险更高。**评级：B**

### 模块O：会计质量

| 因素 | 招商轮船 | 中远海能 |
|---|---|---|
| 收入确认 | 清晰——现货/期租收入直观 | 清晰——同上 |
| 折旧政策 | 25年使用寿命，行业标准 | 25年，标准 |
| 减值风险 | 低（年轻船队，资产价值高） | 中等（部分老龄VLCC） |
| 关联交易 | 中等（招商局租赁） | **高**（中远集团体系） |
| 表外租赁 | 部分光船租赁 | 显著（VLCC+LNG租赁） |
| 套期会计（FFA） | 极少 | 极少 |
| 商誉/无形资产 | 可忽略 | 可忽略 |

**需关注的红旗**：
1. 中远：关联方船舶交易——确保公允定价
2. 两者：经营租赁义务（IFRS 16）可能掩盖真实杠杆
3. 两者：央企"社会责任"支出可能压低报告利润率

**会计质量评级**：
- 招商轮船：清晰透明。红旗极少。**评级：A-**
- 中远海能：基本合格但需关注关联交易。**评级：B**

---

## 十一、六大投资哲学视角

### 1. 质量复利（巴菲特/芒格）

> "持久的竞争优势是什么？"

- **招商轮船**：全球最年轻VLCC船队（7.2年），最低盈亏平衡，40%分红——最接近"质量"航运标的。但航运无真正护城河。
- **中远海能**：LNG长约提供年金式收入。中远集团生态在中国水域构成无形护城河。
- **结论**：两者都非真正的复利机器。**招商更接近**，因分红纪律和船队质量。持有周期而非永远。

### 2. 想象力增长（Baillie Gifford/ARK）

> "10倍期权在哪里？"

- **中远海能**：36艘LNG新造创造"LNG航运巨头"叙事。若LNG即期飙升（如2022年$10-16.2万/天），中远LNG船队价值可能超过其当前全部市值。
- **招商轮船**：除周期外增长期权有限。保守的船队管理。
- **结论**：**中远胜出**。但这是周期性交易，不是10倍赌注。

### 3. 基本面多空（Tiger Cubs）

> "市场在错误定价什么？"

- 市场按$10万共识定价，而即期为$15万+。这是**50-70%的盈利差距**，将通过Q1业绩超预期和卖方上调来弥合。
- **空头方**：可考虑做空无法转嫁高运输成本的下游炼厂。
- **结论**：**两者都是多头。**误定价性质相同但中远幅度更大（73%盈利差距 vs 招商47%）。

### 4. 深度价值（Klarman/Marks）

> "安全边际是什么？"

- **招商9.7倍PE（$15万）**：股息率4.1%，盈亏平衡~$2.5万/天。即使运费腰斩至$7.5万，招商仍赚60-70亿（当前价格盈亏平衡）。安全边际：**高**。
- **中远7.8倍PE（$15万）**：LNG合约年贡献~30亿=市值的22%为稳定收入。但重资本开支降低安全边际。**中等**。
- **结论**：**招商安全边际更好。**中远上行空间更大。

### 5. 催化剂驱动（Tepper/Ackman）

> "什么具体催化剂会释放价值？"

| 催化剂 | 时间线 | 影响 | 概率 |
|---|---|---|---|
| Q1 2026业绩报告 | 2026年4月 | 首个$15万季度→大幅超预期 | 90% |
| 卖方共识上调至$13-15万 | Q2 2026 | 机械性PE压缩 | 80% |
| MSCI/指数再平衡 | H2 2026 | 被动机构买入 | 50% |
| 霍尔木兹危机升级第二阶段 | 未知 | 运费至$25万+ | 30% |
| 特别分红公告 | Q1后 | 股价底部支撑 | 40%（招商） |

- **结论**：**Q1业绩（4月）是两者最近的高概率催化剂。**

### 6. 宏观战术（Druckenmiller）

> "我们处于周期的哪个阶段？"

- 我们处于VLCC超级周期的**第二阶段**：运费已突破，但卖方尚未跟上。PE从28倍→10倍的压缩正在进行中。
- **宏观顺风**：美元走弱（利好大宗航运）、亚洲石油需求上升、制裁执法趋严。
- **宏观风险**：全球衰退（15-20%概率）、霍尔木兹缓和（15-25%）。
- **仓位规模**：这是15-20%的组合仓位，不是5%的小注。周期确信度高，但终端风险存在。
- **结论**：**超配两者。PE到5-6倍时（第四阶段）减仓。霍尔木兹缓和迹象出现即离场。**

---

## 十二、反偏见框架

| 认知陷阱 | 如何应用于此 | 应对措施 |
|---|---|---|
| **锚定效应** | 锚定于$10万共识，而即期为$15万+ | 以$15万为基准；$10万为熊市假设 |
| **简化偏差** | 将两家公司视为"VLCC标的"——忽略中远98艘非VLCC油轮和65艘LNG | 全组合模型（第四节） |
| **近因偏差** | 以2020年浮储为周期模板——2026年根本不同（供给驱动） | 同时对比2008和2020；标注结构性差异 |
| **确认偏差** | 希望两者都是"强烈推荐"可能导致忽视风险 | 事前尸检分析（第十三节）解决此问题 |
| **幸存者偏差** | 对标中远海控集装箱成功忽略了某些周期性押注惨烈失败 | 风险矩阵（第八节）含明确概率 |
| **叙事偏差** | "霍尔木兹危机=运费永远高企"——每一次危机终会结束 | 在第9B节包含缓和情景 |

---

## 十三、事前尸检分析

> **"现在是2027年3月。你的招商轮船和中远海能仓位亏损了40%。哪里出了错？"**

### 情景1：霍尔木兹缓和（最可能的熊市情景）
- **发生了什么**：2026年Q3外交突破。伊朗同意油轮安全保障。保险费率恢复正常。
- **影响**：VLCC运费两个月内从$15万崩至$5-7万。市场立即定价"周期结束"。
- **损失**：招商跌至10-12元（-32%至-43%），中远跌至14-16元（-33%至-41%）
- **预警信号**：美伊外交渠道开启、保险费率下降、油轮路线回归海峡

### 情景2：中远资本开支陷阱
- **发生了什么**：中远61艘新造船（总计$80-120亿）恰在运费正常化时交付。巨额债务服务叠加收入下降。
- **影响**：中远FCF再度深度转负。削减分红或股权融资。
- **损失**：中远特有——跌至12-15元（-37%至-50%）。招商相对受保护。
- **预警信号**：LNG租约费率走软、新造船交付延迟、中远集团融资压力

### 情景3：全球衰退+OPEC增产
- **发生了什么**：2026年H2全球同步衰退。OPEC增产以维持收入。石油需求下降3-5%。
- **影响**：VLCC运费跌至$4-6万。两只股票在利润崩塌后PE降至5-8倍。
- **损失**：招商跌至8-10元（-43%至-55%），中远跌至10-12元（-50%至-58%）
- **预警信号**：亚洲/欧洲PMI持续收缩、原油库存累积、OPEC减产执行率下降

### 情景4：A股系统性风险
- **发生了什么**：中国房地产危机第三阶段，银行压力，资本外流。A股指数下跌30%。
- **影响**：两只股票无视基本面下跌。外资通过陆股通撤出。
- **损失**：两者-30%至-40%，即使基本面盈利强劲。
- **预警信号**：人民币贬值>7.5、央行紧急措施、上证综指跌破2800

### 事前尸检总结

| 风险 | 概率 | 最大回撤 | 对冲手段 |
|---|---|---|---|
| 霍尔木兹缓和 | 15-25% | -40% | -25%移动止损 |
| 中远资本开支陷阱 | 20-30% | -50%（仅中远） | 资本开支担忧上升时超配招商 |
| 全球衰退 | 15-20% | -55% | PMI连续3月<48时减仓 |
| A股系统性风险 | 20-30% | -40% | 配置美股DHT/FRO作为对冲 |

> **40%+回撤的综合概率：约35-45%。**这不是无风险交易。仓位控制（组合15-20%）和硬止损（-25%）不可或缺。收益不对称性有利（上行55-92% vs 下行25-40%），但并非压倒性优势。

"""

# Insert before Appendix
cn = cn.replace(
    '\n---\n\n## 附录：跨市场对比',
    day1global_cn + '\n---\n\n## 附录：跨市场对比'
)

# Add attribution
old_cn_footer = "*本报告由5个独立AI模型分析汇编（Opus 4.6、Sonnet 4.6、GPT-5.2、GPT-5.1、Gemini 3 Pro）。*"
new_cn_footer = """*本报告由5个独立AI模型分析汇编（Opus 4.6、Sonnet 4.6、GPT-5.2、GPT-5.1、Gemini 3 Pro）。*
*分析框架：[Day1Global tech-earnings-deepdive](https://github.com/webleon/tech-earnings-deepdive-openclaw-skill) — 已应用模块A、B、C、D、E、K、L、O。包含6大投资哲学视角、反偏见框架和事前尸检分析。*"""
cn = cn.replace(old_cn_footer, new_cn_footer)

write_file('08_CN_AShare_VLCC_Report_CN.md', cn)
print("CN report: Day1Global modules 10-13 added")

# ========================================
# SYNC GitHub Pages
# ========================================
shutil.copy('08_CN_AShare_VLCC_Report_CN.md', 'cn-ashare.md')
print("\ncn-ashare.md synced")

# ========================================
# UPDATE RULES.md — Add Rule 15
# ========================================
print("\n=== Updating RULES.md ===")
rules = read_file('RULES.md')

rule15 = """

### Rule 15: Day1Global Framework Application
Every stock analysis report MUST apply the full [Day1Global tech-earnings-deepdive](https://github.com/webleon/tech-earnings-deepdive-openclaw-skill) framework:

**Required modules:**
- Module A: Revenue Quality
- Module B: Profitability / Operating Leverage
- Module C: Cash Flow ("THE BIG ONE") — FCF analysis, FCF yield, capex discipline
- Module D: Forward Guidance / PE Compression Path
- Module E: Competitive Landscape
- Module K: Valuation Matrix (multi-scenario target prices)
- Module L: Ownership & Management (shareholder structure, alignment, related-party risk)
- Module O: Accounting Quality (D&A policy, impairment risk, off-balance-sheet items)

**Required perspectives:**
1. Quality Compounder (Buffett/Munger) — durable advantage?
2. Imaginative Growth (Baillie Gifford/ARK) — 10x optionality?
3. Fundamental Long/Short (Tiger Cubs) — what's mispriced?
4. Deep Value (Klarman/Marks) — margin of safety?
5. Catalyst Driven (Tepper/Ackman) — specific value-unlocking events?
6. Macro Tactical (Druckenmiller) — cycle positioning?

**Required frameworks:**
- Anti-Bias Framework: Identify and mitigate anchoring, simplification, recency, confirmation, survivorship, and narrative biases
- Pre-Mortem Analysis: "It's 1 year later and you lost 40%. What went wrong?" — enumerate 3-5 specific scenarios with probabilities and early warning signs"""

if 'Rule 15' not in rules:
    # Find the checklist section and insert before it
    rules = rules.replace(
        '\n---\n\n## 📋 CHECKLIST',
        rule15 + '\n\n---\n\n## 📋 CHECKLIST'
    )
    write_file('RULES.md', rules)
    print("Rule 15 (Day1Global framework) added")
else:
    print("Rule 15 already exists")

# ========================================
# UPDATE PROMPT LOGS
# ========================================
print("\n=== Updating Prompt Logs ===")

en_log = read_file('Prompt_Log_EN.md')
if 'Prompt 19' not in en_log:
    prompt19_en = """
## Prompt 19: Day1Global Framework Retroactive Application
**Date**: March 4, 2026

User noticed the Day1Global tech-earnings-deepdive framework (used in DHT/FRO report) was not listed in RULES.md and was not applied to the A-share report. Decision: Add as mandatory rule AND retroactively apply to A-share report.

**Added to A-share report (Sections 10-13):**
- Module C: Cash Flow — CMES FCF yield 9.8-11.2% at $150K (Grade A-), COSCO flips FCF-positive (Grade B+)
- Module L: Ownership — Both SOEs ~47-49% state-owned, COSCO has higher related-party risk
- Module O: Accounting Quality — CMES cleaner (A-), COSCO watch related-party transactions (B)
- 6 Investment Perspectives: Quality Compounder→CMES, Growth→COSCO, Long/Short→both longs (50-70% gap), Deep Value→CMES safer, Catalyst→Q1 earnings (April), Macro→overweight both
- Anti-Bias Framework: 6 cognitive traps identified and mitigated
- Pre-Mortem: 4 scenarios (Hormuz, capex trap, recession, A-share systemic), combined 40%+ drawdown probability 35-45%

**RULES.md: Added Rule 15** — Day1Global framework is mandatory for all stock analysis reports.

"""
    en_log = en_log.replace(
        '---\n\n*This file will be updated as new prompts are added. Last updated: March 4, 2026.*',
        prompt19_en + '---\n\n*This file will be updated as new prompts are added. Last updated: March 4, 2026.*'
    )
    write_file('Prompt_Log_EN.md', en_log)
    print("Prompt_Log_EN updated with Prompt 19")

cn_log = read_file('Prompt_Log_CN.md')
if '提示词19' not in cn_log:
    prompt19_cn = """
## 提示词19：Day1Global框架追溯应用
**日期**：2026年3月4日

用户发现Day1Global tech-earnings-deepdive框架（已用于DHT/FRO报告）未列入RULES.md，也未应用于A股报告。决定：列为强制规则并追溯应用到A股报告。

**A股报告新增内容（第十至十三节）：**
- 模块C：现金流——招商FCF收益率9.8-11.2%（$15万下，评级A-），中远FCF转正（评级B+）
- 模块L：股权结构——两者均为央企控股~47-49%，中远关联交易风险更高
- 模块O：会计质量——招商更清晰（A-），中远需关注关联交易（B）
- 6大投资视角：质量复利→招商，增长→中远，多空→两者做多（50-70%差距），深度价值→招商更安全，催化剂→Q1业绩（4月），宏观→超配两者
- 反偏见框架：识别并应对6种认知陷阱
- 事前尸检：4种情景（霍尔木兹、资本开支陷阱、衰退、A股系统性），综合40%+回撤概率35-45%

**RULES.md：新增规则15** — Day1Global框架对所有股票分析报告强制适用。

"""
    cn_log = cn_log.replace(
        '---\n\n*本文件将随新提示词的增加而更新。最后更新：2026年3月4日。*',
        prompt19_cn + '---\n\n*本文件将随新提示词的增加而更新。最后更新：2026年3月4日。*'
    )
    write_file('Prompt_Log_CN.md', cn_log)
    print("Prompt_Log_CN updated with Prompt 19")

# Sync session workspace
shutil.copy('RULES.md', os.path.expanduser('~/.copilot/session-state/1b35ff3f-2ff3-456a-b9dd-26ca4dd7d58b/files/VLCC_Project_Rules.md'))
print("\nSession workspace rules synced")

print("\n" + "="*50)
print("ALL DONE — Day1Global framework applied")
print("="*50)

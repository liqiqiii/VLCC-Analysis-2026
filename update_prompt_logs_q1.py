#!/usr/bin/env python3
"""Append prompt log entries for DHT Q1 2026 earnings analysis."""

en_entry = r"""

---

### Prompt 31 — DHT Holdings Q1 2026 Earnings Deep Dive (May 5, 2026)

**User Request**: Analyze DHT Holdings Q1 2026 earnings report and earnings call, create bilingual GitHub Pages with full Day1Global framework analysis.

**Data Gathered**:
- DHT Q1 2026 press release (May 5, 2026): Revenue $186.5M (+134% YoY), GAAP EPS $1.02 (beat $0.61 consensus by 67%)
- Adjusted EBITDA $133.3M (71.5% margin), operating margin 89.9%, FCF margin 52.9%
- Fleet avg TCE $78,800/day; spot TCE $106,000/day (IFRS 15 discharge-to-discharge); TC rate $61,300/day
- Revenue days: 1,994 total (1,152 spot + 842 TC)
- Q2 2026 bookings: 49% of spot days at $189,500/day; 71% total days at $115,400/day
- Balance sheet: $79M cash, $429.7M debt, $349.7M net debt, $189M total liquidity, 17.6% leverage
- Spot cash breakeven: $17,500/day; P&L breakeven: $18,300/day
- Dividend: $0.41/share (64th consecutive quarterly dividend, 100% net income payout)
- Fleet renewal: DHT Antelope, DHT Gazelle (5-7yr TC), DHT Addax delivered; 4th Antilope-class due June 2026
- 3 vessel sales (2007-built): $153M proceeds, ~$94M gains; newbuild program $235M fully funded
- Current TD3C: $423,736/day (all-time record) due to Hormuz crisis
- DHT stock: $19.10 close (+2.74%), market cap $3.08B, 52-wk range $10.61-$20.55
- Shares outstanding: 160,799,407

**Key Findings**:
- Operating leverage: At $106K spot TCE (5.8x breakeven), DHT earns ~$4.78 annualized EPS; at current $420K+ spot, annualized EPS would be $21.88 (>stock price)
- Q2 tracking 2x+ Q1 earnings based on bookings already locked
- Base case FY2026: $3.98 EPS at $150K avg rate = 4.8x PE, 20.8% dividend yield
- Cycle position: Mid-cycle (Phase 3), matching or exceeding 2008 inflation-adjusted peak rates
- Key difference vs 2008/2020: supply-driven (not demand), structurally longer duration
- Day1Global grades: A/A+ across Revenue, Profitability, Cash Flow, Guidance, Valuation
- Pre-mortem: 25% probability-weighted chance of >30% loss (Hormuz de-escalation primary risk at 20%)
- 12M base target: $27.90 (+46%), bull: $32.80 (+72%), super-bull: $43.50 (+128%)

**Files Created**: 21_DHT_Q1_2026_Earnings_EN.md, 22_DHT_Q1_2026_Earnings_CN.md, dht-q1-2026.md (GH Pages), write_dht_q1_earnings.py
**Files Updated**: index.md, Prompt_Log_EN.md, Prompt_Log_CN.md
"""

cn_entry = r"""

---

### 提示词 31 — DHT Holdings Q1 2026财报深度分析（2026年5月5日）

**用户请求**: 分析DHT Holdings Q1 2026财报和财报电话会议，创建中英双语GitHub Pages，包含完整Day1Global框架分析。

**收集数据**:
- DHT Q1 2026新闻稿（2026年5月5日）: 营收$186.5M（同比+134%），GAAP EPS $1.02（超预期$0.61达67%）
- 调整后EBITDA $133.3M（71.5%利润率），经营利润率89.9%，FCF利润率52.9%
- 船队平均TCE $78,800/天；现货TCE $106,000/天（IFRS 15）；期租$61,300/天
- 营运天数: 1,994天（1,152现货 + 842期租）
- Q2 2026签约: 49%现货天数以$189,500/天签约；71%总天数以$115,400/天签约
- 资产负债表: $79M现金，$429.7M债务，$349.7M净债务，$189M总流动性，17.6%杠杆
- 现货现金盈亏平衡: $17,500/天
- 分红: $0.41/股（连续第64个季度分红，100%净利润派息）
- 船队更新: DHT Antelope、DHT Gazelle（5-7年期租）、DHT Addax已交付；第4艘Antilope级预计2026年6月交付
- 3艘售船（2007年建造）: $153M收入，~$94M利润；新造船$235M全额内部资金覆盖
- 当前TD3C: $423,736/天（历史新高），霍尔木兹危机驱动
- DHT股价: $19.10收盘（+2.74%），市值$30.8亿，52周范围$10.61-$20.55

**核心发现**:
- 经营杠杆: 现货TCE $106K（盈亏平衡5.8倍），年化EPS ~$4.78；当前$420K+现货下年化EPS $21.88（超股价）
- Q2追踪2倍以上Q1盈利
- 基准情景FY2026: $3.98 EPS，4.8x PE，20.8%股息率
- 周期定位: 中周期（Phase 3），达到或超越2008年通胀调整后峰值
- vs 2008/2020核心区别: 供给驱动（非需求），结构性更长持续时间
- Day1Global评分: 收入/盈利/现金流/指引/估值全A/A+
- 事前验尸: 25%概率加权>30%亏损风险（霍尔木兹缓和为主要风险20%）
- 12个月基准目标价: $27.90（+46%），乐观: $32.80（+72%），极度乐观: $43.50（+128%）

**创建文件**: 21_DHT_Q1_2026_Earnings_EN.md, 22_DHT_Q1_2026_Earnings_CN.md, dht-q1-2026.md（GH Pages）, write_dht_q1_earnings.py
**更新文件**: index.md, Prompt_Log_EN.md, Prompt_Log_CN.md
"""

with open('Prompt_Log_EN.md', 'a', encoding='utf-8') as f:
    f.write(en_entry)
print("EN prompt log updated")

with open('Prompt_Log_CN.md', 'a', encoding='utf-8') as f:
    f.write(cn_entry)
print("CN prompt log updated")

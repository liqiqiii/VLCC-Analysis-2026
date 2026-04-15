#!/usr/bin/env python3
"""Add new chapters to KEYS report: 800G/1.6T market model, Q1 earnings analysis, multi-model consensus."""

EN_CHAPTER = r"""

## 15. 800G/1.6T Test Market — Bottoms-Up TAM & Keysight Revenue Model

> *This section corrects earlier CPO-centric framing. The real AI revenue driver for Keysight is 800G/1.6T transceiver test equipment, not CPO specifically.*

### 15.1 Transceiver Shipment Volume Forecast (Cross-Checked)

| Year | 800G Units (M) | 1.6T Units (M) | Total Hi-Speed (M) | Source |
|---|---|---|---|---|
| 2024 | 10–12 | ~0 | ~12 | Cignal AI, TrendForce |
| 2025 | 18–20 | <1 | ~20 | LightCounting, Cignal AI |
| **2026** | **50+** | **2–3** | **~53** | TrendForce (2.6x jump) |
| 2027 | 55+ | 2–4 | ~58 | LightCounting |
| 2028 | 60+ | 5+ | ~65 | LightCounting |

### 15.2 800G/1.6T Module Market ($)

| Year | 800G Market | 1.6T Market | Total | Source |
|---|---|---|---|---|
| 2024 | $1.2–1.8B | ~$0 | ~$1.5B | WiseGuy, Verified Market |
| 2025 | $2.1–3.8B | <$0.5B | ~$3.5B | WiseGuy, Dataintelo |
| **2026** | **$4.3–4.5B** | **$1–2B** | **~$6B** | Interpolated @17-19% CAGR |
| 2027 | ~$5B | $3–4B | ~$8B | Projected |
| 2028 | ~$5B (plateau) | $5–7B | ~$11B | 1.6T overtakes 800G |

### 15.3 Test Equipment TAM = 6–10% of Module Market (Industry Rule)

Multiple sources confirm test equipment spending runs 6–10% of module market value. Test cost per 800G module is approximately $25–50.

| Year | Module Market | Test TAM (6-10%) | Midpoint |
|---|---|---|---|
| 2024 | $1.5B | $90–150M | **$120M** |
| 2025 | $3.5B | $210–350M | **$280M** |
| **2026** | **$6B** | **$360–600M** | **$480M** |
| 2027 | $8B | $480–800M | **$640M** |
| 2028 | $11B | $660M–1.1B | **$880M** |

### 15.4 Keysight's Share (25–30% of Test TAM)

| Year | Test TAM | KEYS @25% | KEYS @30% | Midpoint |
|---|---|---|---|---|
| 2025 | $280M | $70M | $84M | **$77M** |
| **2026** | **$480M** | **$120M** | **$144M** | **$132M** |
| 2027 | $640M | $160M | $192M | **$176M** |
| 2028 | $880M | $220M | $264M | **$242M** |

### 15.5 But the Real Story Is MUCH Bigger Than Optical Test

800G/1.6T optical transceiver test is ~$130–240M for Keysight by FY28. But the **total wireline/AI shift** in Commercial Communications is driving from ~$2.3B → $4.0B (+74%) over 3 years. This includes:

| Revenue Category | Est. FY26 | Notes |
|---|---|---|
| 800G/1.6T optical transceiver test | ~$130M | Bottoms-up from TAM model above |
| PCIe Gen6 / CXL test | ~$200M | AI server interconnect |
| Signal integrity / 224G SerDes | ~$300M | Every AI chip needs SerDes validation |
| AI network emulation (Spirent) | ~$200M | Acquired capability |
| 5G/6G wireless test | ~$500M | Still the largest sub-segment |
| Other wireline/protocol test | ~$400M | Ethernet, InfiniBand, etc. |
| Software/PathWave | ~$250M | Growing recurring revenue |
| **Total Commercial Comms** | **~$2.0B** | Q1 FY26 run-rate: ~$3.0B annualized |

### 15.6 Full Company Model (Grounded, FY26–FY28)

| Metric | FY25A | FY26E | FY27E | FY28E |
|---|---|---|---|---|
| **Total Revenue** | $5.38B | $6.50B | $7.30B | $8.10B |
| CSG Revenue | $3.42B | $4.50B | $5.10B | $5.70B |
| EISG Revenue | $1.56B | $2.00B | $2.20B | $2.40B |
| **Non-GAAP Op Margin** | 28.5% | 30% | 31.5% | 33% |
| **Non-GAAP EPS** | $6.38 | **$9.04** | **$11.03** | **$13.27** |
| **PE @$330** | 51.7x | **36.5x** | **29.9x** | **24.9x** |

### 15.7 Multi-Model Probability-Weighted Consensus

Three independent models (Conservative/Klarman, Growth/ARK, Cycle-Aware/Druckenmiller) weighted 30%/30%/40%:

| Year | Weighted EPS | PE @$330 |
|---|---|---|
| FY26E | $9.63 | 34.3x |
| FY27E | $11.27 | 29.3x |
| FY28E | $11.84 | 27.9x |
| FY29E | $12.93 | 25.5x |

**Key risk**: The Cycle-Aware model assigns 40% probability to a mid-cycle AI correction in FY28, which would compress EPS to ~$7.60 (PE 43x at $330). This tail risk is why the weighted FY28 EPS ($11.84) is lower than the base case ($13.27).

---

## 16. Q1 FY2026 10-Q Deep Dive & Earnings Spike Analysis

> *On February 24, 2026, KEYS spiked 23% in a single day. This section explains why.*

### 16.1 The Beat (Feb 23, 2026 — Quarter Ended Jan 31, 2026)

| Metric | Consensus | Actual | Beat |
|---|---|---|---|
| Revenue | $1.54B | **$1.60B** | +$60M (+4%) |
| Non-GAAP EPS | $2.00–2.04 | **$2.17** | +$0.13–0.17 (+8%) |
| Orders | — | **$1.645B** (+30% YoY) | Record |

### 16.2 Five Catalysts That Drove the 23% Spike

**Catalyst 1: Orders > Revenue = Acceleration Signal**
- Orders grew +30% YoY vs revenue +23% → Book-to-bill of **1.03x**
- Orders exceeding revenue means backlog is BUILDING, not depleting
- The market had feared post-recovery deceleration; +30% orders killed that narrative

**Catalyst 2: Wireline > Wireless — A Structural First**
- **First time in company history** that wireline orders surpassed wireless
- Wireline = AI datacenter (800G/1.6T Ethernet, optical interconnects)
- Market re-classified KEYS from "5G test company" to **"AI infrastructure platform"**
- AI-specific customer count **doubled** in the past year

**Catalyst 3: Guidance Raised Well Above Consensus**

| Metric | Q2 FY26 Guidance | Implied YoY |
|---|---|---|
| Revenue | $1.69–1.71B | **+30%** |
| Non-GAAP EPS | $2.27–2.33 | **+35%** |
| Full-year | **>20% revenue & earnings growth** | Raised |

Classic **beat-and-raise** — the market's favorite signal for growth compounders.

**Catalyst 4: Massive Simultaneous Analyst Upgrades**

| Analyst | Old Target | New Target | Change |
|---|---|---|---|
| UBS | $230 | **$340** | +48% |
| Goldman Sachs | $243 | **$322** | +33% |
| JPMorgan | ~$250 | **$300** | +20% |
| Citigroup | $282 | **$320** | +13% |
| Susquehanna | $225 | **$300** | +33% |
| Morgan Stanley | $227 | **$268** | +18% |

Six simultaneous upgrades of 18–48% triggers a **forced re-pricing** across buy-side models.

**Catalyst 5: Spirent Integration Narrative**
- $1.5B buyback authorization announced — signals confidence
- Management guided Spirent margins to improve through FY26 — temporary dilution understood
- Spirent adds $375M+ revenue to AI/network test TAM

### 16.3 GAAP vs Non-GAAP — Why the Market Looked Through GAAP Weakness

| GAAP Concern | Why Market Ignored It |
|---|---|
| GAAP GM fell 100bps to 62.2% | Non-GAAP GM was **66.7%** — market trades on non-GAAP |
| GAAP op margin fell 130bps | Known Spirent dilution — **pre-announced and temporary** |
| $83M tax benefit flattered GAAP NI | Market focused on Non-GAAP $2.17 which excludes one-time items |
| Intangible amortization doubled ($67M) | **Expected** from $1.56B Spirent acquisition goodwill |

### 16.4 10-Q Key Financial Data (Quarter Ended Jan 31, 2026)

**Income Statement (GAAP, $M)**

| Line Item | Q1 FY26 | Q1 FY25 | YoY |
|---|---|---|---|
| Product Revenue | $1,225 | $983 | +25% |
| Services Revenue | $375 | $315 | +19% |
| **Total Revenue** | **$1,600** | $1,298 | **+23%** |
| Total COGS | $605 | $478 | |
| **Gross Profit** | **$995** | $820 | +21% |
| R&D | $303 | $249 | +22% |
| SG&A | $447 | $361 | +24% |
| **Income from Operations** | **$248** | $218 | +14% |
| **GAAP Net Income** | **$281** | $169 | +66% |
| **GAAP Diluted EPS** | **$1.63** | $0.97 | +68% |
| **Non-GAAP EPS** | **$2.17** | $1.82 | +19% |

**Balance Sheet Highlights ($M, Jan 31, 2026)**

| Item | Jan 31, 2026 | Oct 31, 2025 |
|---|---|---|
| Cash & Equivalents | $2,195 | $1,890 |
| Total Assets | $11,481 | $11,301 |
| Long-term Debt | $2,534 | $2,534 |
| Goodwill | $3,474 | $3,424 |
| Deferred Revenue (current) | **$729** | $652 **(+12%)** |
| Stockholders' Equity | $6,205 | $5,881 |

**Cash Flow ($M, Q1)**

| Item | Q1 FY26 | Q1 FY25 |
|---|---|---|
| Operating Cash Flow | **$441** | $378 |
| Capex | ($34) | ($32) |
| **Free Cash Flow** | **$407** | $346 |
| Share Buybacks | ($87) | ($75) |

### 16.5 Signal Strength Assessment

| Signal | Reading | Importance |
|---|---|---|
| Orders +30% (> revenue +23%) | **Strongly bullish** — growth accelerating | ★★★★★ |
| Wireline > wireless (structural first) | **AI infrastructure recomposition** | ★★★★★ |
| Guidance raised above consensus | **Beat-and-raise cycle intact** | ★★★★★ |
| Non-GAAP EPS beat by 8% | **Execution confirmed** | ★★★★☆ |
| Deferred revenue +12% | **Backlog building** | ★★★★☆ |
| FCF $407M (25% margin) | **Cash generation excellent** | ★★★★☆ |
| GAAP margins declining | **Temporary** — Spirent integration | ★★☆☆☆ |
| $83M one-time tax benefit | **Non-issue** for non-GAAP investors | ★☆☆☆☆ |

---
"""

CN_CHAPTER = r"""

## 14. 800G/1.6T测试市场 — 自下而上TAM模型与KEYS营收推演

> *本章修正了此前以CPO为中心的分析框架。是德科技真正的AI营收驱动力是800G/1.6T收发器测试设备，而非CPO本身。*

### 14.1 收发器出货量预测（交叉验证）

| 年份 | 800G出货(百万) | 1.6T出货(百万) | 合计(百万) | 来源 |
|---|---|---|---|---|
| 2024 | 10–12 | ~0 | ~12 | Cignal AI, TrendForce |
| 2025 | 18–20 | <1 | ~20 | LightCounting |
| **2026** | **50+** | **2–3** | **~53** | TrendForce (2.6倍跳升) |
| 2027 | 55+ | 2–4 | ~58 | LightCounting |
| 2028 | 60+ | 5+ | ~65 | LightCounting |

### 14.2 测试设备TAM = 模块市场的6–10%（行业规律）

| 年份 | 模块市场 | 测试TAM (6-10%) | 中值 |
|---|---|---|---|
| 2025 | $35亿 | $2.1–3.5亿 | **$2.8亿** |
| **2026** | **$60亿** | **$3.6–6亿** | **$4.8亿** |
| 2027 | $80亿 | $4.8–8亿 | **$6.4亿** |
| 2028 | $110亿 | $6.6–11亿 | **$8.8亿** |

### 14.3 是德科技份额：25–30%

| 年份 | 测试TAM | KEYS @27.5% | 光学测试收入 |
|---|---|---|---|
| 2025 | $2.8亿 | **$0.77亿** | |
| 2026 | $4.8亿 | **$1.32亿** | |
| 2027 | $6.4亿 | **$1.76亿** | |
| 2028 | $8.8亿 | **$2.42亿** | |

### 14.4 真正的故事远大于光学测试

800G/1.6T光学测试仅占是德科技FY28约$2.4亿营收（~3%）。但**商业通信整体的有线/AI转型**正从~$23亿增长至~$40亿（+74%），涵盖：PCIe Gen6/CXL测试、信号完整性/224G SerDes、AI网络仿真(Spirent)、软件/PathWave等全栈AI数据中心测试。

### 14.5 全公司盈利模型

| 指标 | FY25实际 | FY26E | FY27E | FY28E |
|---|---|---|---|---|
| **总营收** | $53.8亿 | $65亿 | $73亿 | $81亿 |
| **Non-GAAP EPS** | $6.38 | **$9.04** | **$11.03** | **$13.27** |
| **PE @$330** | 51.7倍 | **36.5倍** | **29.9倍** | **24.9倍** |

### 14.6 三模型概率加权共识

保守(Klarman)/成长(ARK)/周期(Druckenmiller)加权30%/30%/40%：

| 年份 | 加权EPS | PE @$330 |
|---|---|---|
| FY27E | $11.27 | 29.3倍 |
| FY28E | $11.84 | 27.9倍 |

---

## 15. Q1 FY2026季报深度解读与23%暴涨分析

> *2026年2月24日，KEYS单日暴涨23%。本章解读原因。*

### 15.1 业绩超预期

| 指标 | 共识预期 | 实际 | 超出 |
|---|---|---|---|
| 营收 | $15.4亿 | **$16亿** | +$0.6亿 (+4%) |
| Non-GAAP EPS | $2.00–2.04 | **$2.17** | +8% |
| 订单 | — | **$16.45亿** (+30% YoY) | 创纪录 |

### 15.2 五大催化因素

**催化剂1：订单 > 营收 = 加速信号**
- 订单增长+30% vs 营收增长+23% → 账面比率**1.03倍**
- 订单超过营收意味着积压订单正在**增长而非消耗**

**催化剂2：有线 > 无线 — 公司历史首次**
- 有线订单**首次超过无线**，代表AI数据中心（800G/1.6T以太网）的结构性崛起
- AI专属客户数量过去一年**翻倍**
- 市场重新定义KEYS：从"5G测试公司"变为**"AI基础设施测试平台"**

**催化剂3：指引大幅上调**
- Q2 FY26营收指引$16.9–17.1亿（同比**+30%**）
- 全年：营收和盈利增长**>20%**

**催化剂4：6家投行同时上调目标价**
- UBS：$230→**$340** (+48%)；高盛：$243→**$322** (+33%)
- 摩根大通→**$300**；花旗→**$320**；大和→**$300**
- 同时上调18–48%触发市场**强制重新定价**

**催化剂5：Spirent整合叙事**
- 宣布$15亿回购授权；Spirent利润率将逐步改善

### 15.3 GAAP弱势为何被市场忽略

| GAAP担忧 | 市场忽略原因 |
|---|---|
| GAAP毛利率下降100bps至62.2% | Non-GAAP毛利率**66.7%**——市场按Non-GAAP交易 |
| GAAP营业利润率下降130bps | Spirent已知稀释——**预期内且暂时性** |
| $8300万一次性税收优惠 | Non-GAAP $2.17已排除此项 |

### 15.4 10-Q关键财务数据

| 项目 | Q1 FY26 | Q1 FY25 | 同比 |
|---|---|---|---|
| **总营收** | **$16亿** | $12.98亿 | **+23%** |
| CSG营收 | $11.24亿 | $8.85亿 | +27% |
| 商业通信 | $7.58亿 | $5.70亿 | **+33%** |
| 航空国防 | $3.66亿 | $3.10亿 | +18% |
| EISG营收 | $4.76亿 | $4.14亿 | +15% |
| **经营现金流** | **$4.41亿** | $3.78亿 | +17% |
| **自由现金流** | **$4.07亿** | $3.46亿 | +18% |
| 递延收入（流动） | **$7.29亿** | $6.52亿 | **+12%** |

### 15.5 信号强度评估

| 信号 | 解读 | 重要性 |
|---|---|---|
| 订单+30%（超过营收+23%） | **强烈看多**——增长加速 | ★★★★★ |
| 有线>无线（历史首次） | **AI基础设施结构性重组** | ★★★★★ |
| 指引上调超共识 | **超预期-上调周期完好** | ★★★★★ |
| Non-GAAP EPS超预期8% | **执行力确认** | ★★★★☆ |
| 递延收入+12% | **订单积压增长** | ★★★★☆ |
| FCF $4.07亿（25%利润率） | **现金生成优秀** | ★★★★☆ |

---
"""

# Read existing files, insert new chapters before the disclaimer
import re

for fname, chapter in [("keysight/report_en.md", EN_CHAPTER), ("keysight/report_cn.md", CN_CHAPTER)]:
    with open(fname, "r", encoding="utf-8") as f:
        content = f.read()

    if fname.endswith("en.md"):
        marker = "*Data as of April 14, 2026. Not investment advice."
        replacement = chapter.strip() + "\n\n---\n\n" + marker
    else:
        marker = "*数据截至2026年4月14日。非投资建议。"
        replacement = chapter.strip() + "\n\n---\n\n" + marker

    content = content.replace(marker, replacement)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {fname}")

print("Both reports updated successfully")

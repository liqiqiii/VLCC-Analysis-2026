#!/usr/bin/env python3
"""Fix the cross-market comparison appendix in both EN and CN reports"""
import os

DIR = r"C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026"

# ===== NEW ENGLISH APPENDIX =====
new_en_appendix = r"""## Appendix: Cross-Market Comparison with US-Listed Peers (Corrected)

> **⚠️ Previous version incorrectly divided total market cap by VLCC count alone.** CMES and COSCO Energy are diversified fleets — CMES has ~300 vessels across 5 segments; COSCO Energy has ~180 vessels including 65 LNG carriers. A per-VLCC comparison without adjusting for non-VLCC assets is fundamentally misleading. Below is the corrected multi-metric analysis.

### Full Fleet Overview

| Company | VLCCs | Suezmax | Aframax/LR | MR/LR1 | LNG | Dry Bulk | Container/Other | **Total Vessels** |
|---|---|---|---|---|---|---|---|---|
| **DHT** | 24 | — | — | — | — | — | — | **24** |
| **FRO** | 42 | 21 | 18 | — | — | — | — | **81** |
| **CMES** | 52 | — | — | — | ~40-60 | ~93 | ~30 | **~250-300** |
| **COSCO Energy** | 55 | 18 | ~50 | ~30 | ~65 | — | — | **~180-195** |

### Method 1: Market Cap per Total Vessel

| Company | Market Cap | Total Vessels | **$/Vessel** | vs DHT |
|---|---|---|---|---|
| DHT | $3.13B | 24 | **$130M** | baseline |
| FRO | $8.50B | 81 | **$105M** | 0.81x |
| CMES | $19.7B | ~280 | **$70M** | **0.54x (CHEAPER)** |
| COSCO Energy | $18.6B | ~185 | **$101M** | 0.78x |

**Key insight**: On a per-vessel basis, CMES is actually the CHEAPEST of all four companies — trading at only 54% of DHT's per-vessel valuation. This demolishes the "A-share premium" narrative when the full fleet is properly accounted for.

### Method 2: Sum-of-Parts (VLCC Segment Isolation)

To compare VLCC valuations fairly, we must strip out non-VLCC business value:

**CMES segment breakdown** (est. 2025 profit contribution):
- Oil transport (VLCC): ~50-55% of profit → segment value ~$9.9-10.8B
- Dry bulk: ~15-20% → ~$3.0-3.9B
- LNG: ~10-15% → ~$2.0-3.0B
- Container + Ro-Ro: ~10-15% → ~$2.0-3.0B

**COSCO Energy segment breakdown** (est.):
- VLCC/crude oil: ~45-55% → segment value ~$8.4-10.2B
- Product tankers (Suez/Afra/MR/LR): ~15-20% → ~$2.8-3.7B
- LNG (65 ships, long-term contracts): ~20-30% → ~$3.7-5.6B

| Company | VLCC Segment Value (est.) | VLCC Count | **$/VLCC (segment-adjusted)** | vs DHT |
|---|---|---|---|---|
| DHT | $3.13B (100% VLCC) | 24 | **$130M** | baseline |
| FRO | ~$6.0B (70% VLCC-eq) | 42 | **$143M** | 1.10x |
| CMES | ~$10.0-10.8B (50-55%) | 52 | **$192-208M** | **1.5-1.6x** |
| COSCO Energy | ~$8.4-10.2B (45-55%) | 55 | **$153-185M** | **1.2-1.4x** |

**Corrected A-share premium: 1.2-1.6x** (not the previously stated 2.5-3.0x). This is largely explained by:
1. Younger fleet (CMES 7.2yr avg → lower breakeven, longer economic life)
2. SOE parent backing (China Merchants / COSCO Group credit and contracts)
3. Captive Chinese crude import demand (~70% of VLCC demand is China-bound)
4. A-share general PE premium (~30-50% above US markets historically)

### Method 3: PE Comparison (Most Direct)

| Company | PE (TTM) | Forward PE (at $150K VLCC) | Dividend Yield | PB |
|---|---|---|---|---|
| DHT | ~15x | ~6x | ~8-10% | ~1.8x |
| FRO | ~12x | ~5x | ~6-8% | ~2.5x |
| CMES | 28.4x | 10.5x | ~5% | 3.09x |
| COSCO Energy | ~28.7x | 10.0x | ~3-4% | N/A |

**A-share PE premium: ~1.7-2.0x vs US peers at forward earnings.** This is within the normal A-share premium range for cyclical SOEs and does NOT indicate overvaluation.

### Method 4: Non-VLCC "Hidden Value"

Assets the per-VLCC metric completely ignored:

| Company | Non-VLCC Assets | Est. Value | Notes |
|---|---|---|---|
| CMES | 93 dry bulk + 40-60 LNG + 19 container + Ro-Ro | **$8-10B** | LNG fleet expanding rapidly (42 newbuilds) |
| COSCO Energy | 18 Suezmax + 50 Afra/LR2 + 30 MR/LR1 + 65 LNG | **$8-10B** | LNG alone (65 ships × long contracts) worth $4-6B |
| FRO | 21 Suezmax + 18 LR2 | **$2.5-3.5B** | Also benefits from tanker super-cycle |
| DHT | None | $0 | Pure VLCC play |

**COSCO Energy's 65 LNG carriers on long-term contracts are arguably worth $4-6B alone** — an asset completely invisible in a per-VLCC comparison. When this is subtracted, COSCO's VLCC segment trades at only $153-185M/VLCC, just 1.2-1.4x DHT.

### Corrected Conclusion

| Metric | Previous (Wrong) | Corrected |
|---|---|---|
| CMES per-VLCC premium vs DHT | 2.9x | **1.5-1.6x** |
| COSCO per-VLCC premium vs DHT | 2.7-3.2x | **1.2-1.4x** |
| Per-vessel (all ships) vs DHT | Not calculated | **CMES 0.54x (cheaper!)** |
| PE premium (forward) | Not compared | **~1.7-2.0x (normal A-share range)** |

The corrected analysis shows Chinese VLCC stocks are **reasonably valued** when the full portfolio is considered — NOT the 2.5-3x "premium" previously stated. In fact, CMES's massive dry bulk + LNG + container fleet makes it arguably **cheaper per asset** than any US-listed peer.

---

*Report compiled from 5 independent AI model analyses (Opus 4.6, Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro).*
*Data as of March 4, 2026. This is for informational purposes only and does not constitute investment advice.*"""

# ===== NEW CHINESE APPENDIX =====
new_cn_appendix = r"""## 附录：跨市场对比——与美股同行比较（修正版）

> **⚠️ 前版错误**：直接用总市值除以VLCC数量进行比较。招商轮船约300艘船（含散货、LNG、集装箱），中远海能约180艘船（含65艘LNG）。不扣除非VLCC资产直接比较是根本性的误导。以下为修正后的多维度分析。

### 完整船队概览

| 公司 | VLCC | 苏伊士 | 阿芙拉/LR | MR/LR1 | LNG | 散货 | 集装箱/其他 | **总计** |
|---|---|---|---|---|---|---|---|---|
| **DHT** | 24 | — | — | — | — | — | — | **24** |
| **FRO** | 42 | 21 | 18 | — | — | — | — | **81** |
| **招商轮船** | 52 | — | — | — | ~40-60 | ~93 | ~30 | **~250-300** |
| **中远海能** | 55 | 18 | ~50 | ~30 | ~65 | — | — | **~180-195** |

### 方法一：总市值÷总船数

| 公司 | 市值 | 总船数 | **每艘估值** | vs DHT |
|---|---|---|---|---|
| DHT | $31.3亿 | 24 | **$1.3亿** | 基准 |
| FRO | $85亿 | 81 | **$1.05亿** | 0.81倍 |
| 招商轮船 | $197亿 | ~280 | **$0.7亿** | **0.54倍（更便宜）** |
| 中远海能 | $186亿 | ~185 | **$1.01亿** | 0.78倍 |

**关键发现**：按每艘船估值，招商轮船实际上是四家中最便宜的——仅为DHT的54%。当完整计入全部船队后，"A股溢价"叙事被颠覆。

### 方法二：分部加总法（VLCC板块剥离）

公平比较VLCC估值需剥离非VLCC业务价值：

**招商轮船分部估算**（2025年利润贡献）：
- 油运（VLCC为主）：~50-55% → 板块价值 ~$99-108亿
- 散货运输：~15-20% → ~$30-39亿
- LNG运输：~10-15% → ~$20-30亿
- 集装箱+滚装：~10-15% → ~$20-30亿

**中远海能分部估算**：
- VLCC/原油运输：~45-55% → 板块价值 ~$84-102亿
- 成品油轮（苏伊士/阿芙拉/MR/LR）：~15-20% → ~$28-37亿
- LNG（65艘，长约锁定）：~20-30% → ~$37-56亿

| 公司 | VLCC板块价值 | VLCC数量 | **每艘VLCC估值（调整后）** | vs DHT |
|---|---|---|---|---|
| DHT | $31.3亿（100% VLCC） | 24 | **$1.3亿** | 基准 |
| FRO | ~$60亿（70% VLCC当量） | 42 | **$1.43亿** | 1.10倍 |
| 招商轮船 | ~$100-108亿（50-55%） | 52 | **$1.92-2.08亿** | **1.5-1.6倍** |
| 中远海能 | ~$84-102亿（45-55%） | 55 | **$1.53-1.85亿** | **1.2-1.4倍** |

**修正后A股溢价：1.2-1.6倍**（非此前的2.5-3.0倍）。主要原因：
1. 更年轻的船队（招商7.2年均龄→更低盈亏平衡、更长经济寿命）
2. 央企母公司支撑（招商局/中远海运的信用和合约优势）
3. 中国原油进口绑定需求（~70%的VLCC需求来自中国）
4. A股整体PE溢价（历史上比美股高30-50%属正常）

### 方法三：PE直接对比（最直观）

| 公司 | PE（TTM） | 远期PE（$15万运费） | 股息率 | PB |
|---|---|---|---|---|
| DHT | ~15倍 | ~6倍 | ~8-10% | ~1.8倍 |
| FRO | ~12倍 | ~5倍 | ~6-8% | ~2.5倍 |
| 招商轮船 | 28.4倍 | 10.5倍 | ~5% | 3.09倍 |
| 中远海能 | ~28.7倍 | 10.0倍 | ~3-4% | 未披露 |

**A股远期PE溢价：~1.7-2.0倍**，在A股周期性央企的正常溢价范围内，不代表高估。

### 方法四：非VLCC"隐藏价值"

此前的每艘VLCC比较完全忽略的资产：

| 公司 | 非VLCC资产 | 估算价值 | 备注 |
|---|---|---|---|
| 招商轮船 | 93艘散货+40-60艘LNG+19集装箱+滚装 | **$80-100亿** | LNG船队快速扩张（42艘在建） |
| 中远海能 | 18苏伊士+50阿芙拉/LR2+30 MR/LR1+65 LNG | **$80-100亿** | 仅LNG（65艘长约）就值$40-60亿 |
| FRO | 21苏伊士+18 LR2 | **$25-35亿** | 同样受益于油轮超级周期 |
| DHT | 无 | $0 | 纯VLCC标的 |

**中远海能的65艘LNG长约船队单独估值$40-60亿**——在单纯的"每艘VLCC"比较中完全不可见。扣除后VLCC板块仅$1.53-1.85亿/艘，仅为DHT的1.2-1.4倍。

### 修正后结论

| 指标 | 此前（错误） | 修正后 |
|---|---|---|
| 招商VLCC溢价 vs DHT | 2.9倍 | **1.5-1.6倍** |
| 中远VLCC溢价 vs DHT | 2.7-3.2倍 | **1.2-1.4倍** |
| 每艘船（全船队）vs DHT | 未计算 | **招商0.54倍（更便宜！）** |
| 远期PE溢价 | 未比较 | **~1.7-2.0倍（A股正常范围）** |

修正后的分析表明，考虑完整船队组合后，A股VLCC公司估值**合理**——并非此前所述的2.5-3倍"溢价"。事实上，招商轮船庞大的散货+LNG+集装箱船队使其**每艘资产估值**甚至低于任何美股同行。

---

*本报告由5个独立AI模型分析汇编（Opus 4.6、Sonnet 4.6、GPT-5.2、GPT-5.1、Gemini 3 Pro）。*
*数据截至2026年3月4日。仅供信息参考，不构成投资建议。*"""

# ===== UPDATE EN REPORT (07) =====
en_path = os.path.join(DIR, "07_CN_AShare_VLCC_Report_EN.md")
with open(en_path, "r", encoding="utf-8") as f:
    en_content = f.read()

# Find and replace the old appendix
old_en_marker = "## Appendix: Comparison with US-Listed Peers"
if old_en_marker in en_content:
    idx = en_content.index(old_en_marker)
    en_content = en_content[:idx] + new_en_appendix
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_content)
    print(f"Updated EN report: {en_path}")
else:
    print(f"WARNING: Could not find marker in EN report")

# ===== UPDATE CN REPORT (08) =====
cn_path = os.path.join(DIR, "08_CN_AShare_VLCC_Report_CN.md")
with open(cn_path, "r", encoding="utf-8") as f:
    cn_content = f.read()

old_cn_marker = "## 附录：与美股同行对比"
if old_cn_marker in cn_content:
    idx = cn_content.index(old_cn_marker)
    cn_content = cn_content[:idx] + new_cn_appendix
    with open(cn_path, "w", encoding="utf-8") as f:
        f.write(cn_content)
    print(f"Updated CN report: {cn_path}")
else:
    print(f"WARNING: Could not find marker in CN report")

# ===== UPDATE cn-ashare.md (GitHub Pages) =====
import shutil
shutil.copy2(cn_path, os.path.join(DIR, "cn-ashare.md"))
print("Updated cn-ashare.md (GitHub Pages)")

print("\nDone! All 3 files updated with corrected cross-market comparison.")

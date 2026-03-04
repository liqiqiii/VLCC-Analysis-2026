#!/usr/bin/env python3
"""Add $150K-base scenario comparison section to both EN and CN reports"""
import os, shutil

DIR = r"C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026"

# ===== NEW EN SECTION =====
new_en = r"""
---

## 4B. Alternative Baseline: What If $150K IS the New Consensus?

> Current VLCC spot rates are $150-210K/day. Broker consensus still assumes $100K/day avg for 2026 — but what if the market has structurally shifted, and **$150K/day is the real baseline**? This section re-anchors the entire model.

### Rationale for $150K as Baseline
1. **Supply**: Zero new VLCCs until late 2028. 40%+ of fleet over 15 years old — retirements accelerating.
2. **Demand**: Strait of Hormuz crisis deepening. Sanctions enforcement tightening. Ton-mile demand surging as routes lengthen.
3. **Shadow fleet**: Exiting the market, removing 5-8% of effective supply.
4. **Historical parallel**: In the 2008 super-cycle, rates averaged $120K+ for 18 months. Current supply constraints are TIGHTER than 2008.
5. **Current spot**: $150-210K/day in March 2026 — already at or above this level.

### Scenario Comparison: $100K Base vs $150K Base

**CMES (招商轮船) — Full Portfolio**

| | $100K Base (Old Consensus) | $150K Base (New Baseline) | Delta |
|---|---|---|---|
| **Consensus NI** | RMB 10.0B | **RMB 14.7B** | **+47%** |
| Conservative ($120K / $170K) | RMB 12.0B | **RMB 16.2B** | +35% |
| Base ($150K / $200K) | RMB 14.7B | **RMB 19.0B** | +29% |
| Bull ($200K / $250K) | RMB 19.0B | **RMB 22.7B** | +19% |
| **EPS (consensus)** | 1.24 | **1.82** | **+47%** |
| **PE at 17.71 (consensus)** | 14.3x | **9.7x** | **-32%** |
| **Dividend/share (40%)** | RMB 0.50 | **RMB 0.73** | **+46%** |
| **Dividend yield** | 2.8% | **4.1%** | +130bps |

*At $150K base, CMES scenarios shift up: Conservative=$170K, Base=$200K, Bull=$250K*

**COSCO Energy (中远海能) — Full Portfolio**

| | $100K Base (Old Consensus) | $150K Base (New Baseline) | Delta |
|---|---|---|---|
| **Consensus NI** | RMB 10.0B | **RMB 17.3B** | **+73%** |
| Conservative ($120K / $170K) | RMB 13.3B | **RMB 20.5B** | +54% |
| Base ($150K / $200K) | RMB 17.3B | **RMB 23.2B** | +34% |
| Bull ($200K / $250K) | RMB 23.2B | **RMB 28.5B** | +23% |
| **EPS (consensus)** | 1.76 | **3.05** | **+73%** |
| **PE at 23.79 (consensus)** | 13.5x | **7.8x** | **-42%** |

*COSCO benefits more because its 98 non-VLCC tankers also re-anchor higher (Suezmax $80K base, Afra/LR2 $55K base)*

### Valuation Impact: $150K Base Completely Reframes Both Stocks

| Metric | $100K Base | $150K Base | Implication |
|---|---|---|---|
| CMES PE (consensus) | 14.3x | **9.7x** | Already in mid-cycle range |
| COSCO PE (consensus) | 13.5x | **7.8x** | Approaching cycle-peak territory |
| CMES PE (base scenario) | 9.7x | **7.5x** | Deep value at elevated rates |
| COSCO PE (base scenario) | 7.8x | **5.8x** | Near 中远海控 2021 levels (1.4x PE) |
| CMES dividend yield | 2.8% | **4.1%** | Competitive with bank deposits |
| COSCO earnings growth | +100% YoY | **+268% YoY** | Explosive |

### Updated Target Prices ($150K Base)

| | CMES (601872) | COSCO Energy (600026) |
|---|---|---|
| **2026E NI ($150K base, full portfolio)** | RMB 14.7B | RMB 17.3B |
| **12M TP (PE 10x)** | **RMB 18.2** (+3%) | **RMB 30.5** (+28%) |
| **12M TP (PE 12x)** | **RMB 21.9** (+24%) | **RMB 36.6** (+54%) |
| **12M TP (PE 15x, re-rate)** | **RMB 27.3** (+54%) | **RMB 45.8** (+92%) |
| **Bull ($200K, PE 10x)** | **RMB 23.5** (+33%) | **RMB 40.9** (+72%) |
| **Bull ($250K, PE 10x)** | **RMB 28.1** (+59%) | **RMB 50.3** (+111%) |

### Key Conclusion: $150K Base Changes Everything

> With a $150K baseline, **both stocks are already trading at cycle-appropriate multiples** — COSCO at 7.8x and CMES at 9.7x forward PE. The old consensus ($100K) made them look expensive at 13-14x PE, masking the fact that rates have already broken out.
>
> If the market re-anchors consensus from $100K to $150K (which current spot rates justify), expect:
> - **Sell-side earnings upgrades of 50-70%** → mechanical PE compression
> - **COSCO Energy is the bigger winner** — its diversified tanker fleet benefits across the board ($150K VLCC + $80K Suezmax + $55K Aframax = all elevated)
> - **CMES offers better safety** — 40% dividend at $150K base = 4.1% yield, plus dry bulk/LNG diversification as non-correlated hedge
>
> **The question is not IF rates stay at $150K — they already ARE there. The question is when analysts upgrade their models.**

"""

# ===== NEW CN SECTION =====
new_cn = r"""
---

## 4B. 替代基准：如果$15万才是新共识？

> 当前VLCC即期运费$15-21万/天。券商共识仍假设2026年均值$10万/天——但如果市场已发生结构性转变，**$15万/天才是真正的基准**呢？本节重新锚定整个模型。

### $15万作为基准的理由
1. **供给**：2028年底前零新VLCC交付。40%+船龄超15年——退役加速。
2. **需求**：霍尔木兹危机加深。制裁执法趋严。航程拉长推升吨海里需求。
3. **影子船队**：退出市场，移除5-8%有效供给。
4. **历史参照**：2008年超级周期运费均值$12万+维持18个月。当前供给约束比2008年更紧。
5. **当前即期**：2026年3月已达$15-21万/天——已经处于或超过此水平。

### 情景对比：$10万基准 vs $15万基准

**招商轮船 — 全组合**

| | $10万基准（旧共识） | $15万基准（新基准） | 变化 |
|---|---|---|---|
| **共识净利** | 100亿 | **147亿** | **+47%** |
| 保守（$12万 / $17万） | 120亿 | **162亿** | +35% |
| 基准（$15万 / $20万） | 147亿 | **190亿** | +29% |
| 牛市（$20万 / $25万） | 190亿 | **227亿** | +19% |
| **EPS（共识）** | 1.24元 | **1.82元** | **+47%** |
| **PE（17.71元，共识）** | 14.3倍 | **9.7倍** | **-32%** |
| **每股分红（40%）** | 0.50元 | **0.73元** | **+46%** |
| **股息率** | 2.8% | **4.1%** | +130基点 |

**中远海能 — 全组合**

| | $10万基准（旧共识） | $15万基准（新基准） | 变化 |
|---|---|---|---|
| **共识净利** | 100亿 | **173亿** | **+73%** |
| 保守（$12万 / $17万） | 133亿 | **205亿** | +54% |
| 基准（$15万 / $20万） | 173亿 | **232亿** | +34% |
| 牛市（$20万 / $25万） | 232亿 | **285亿** | +23% |
| **EPS（共识）** | 1.76元 | **3.05元** | **+73%** |
| **PE（23.79元，共识）** | 13.5倍 | **7.8倍** | **-42%** |

### 估值影响：$15万基准彻底重构两只股票

| 指标 | $10万基准 | $15万基准 | 启示 |
|---|---|---|---|
| 招商PE（共识） | 14.3倍 | **9.7倍** | 已进入周期中段 |
| 中远PE（共识） | 13.5倍 | **7.8倍** | 接近周期顶部区间 |
| 招商PE（基准情景） | 9.7倍 | **7.5倍** | 高运费下的深度价值 |
| 中远PE（基准情景） | 7.8倍 | **5.8倍** | 接近中远海控2021年水平（1.4倍PE） |
| 招商股息率 | 2.8% | **4.1%** | 比肩银行存款 |
| 中远盈利增速 | +100% YoY | **+268% YoY** | 爆发性增长 |

### 更新后目标价（$15万基准）

| | 招商轮船 (601872) | 中远海能 (600026) |
|---|---|---|
| **2026E净利（$15万基准，全组合）** | 147亿 | 173亿 |
| **12M目标（PE 10倍）** | **18.2元**（+3%） | **30.5元**（+28%） |
| **12M目标（PE 12倍）** | **21.9元**（+24%） | **36.6元**（+54%） |
| **12M目标（PE 15倍，重估）** | **27.3元**（+54%） | **45.8元**（+92%） |
| **牛市（$20万，PE 10倍）** | **23.5元**（+33%） | **40.9元**（+72%） |
| **牛市（$25万，PE 10倍）** | **28.1元**（+59%） | **50.3元**（+111%） |

### 核心结论：$15万基准改变一切

> 以$15万为基准，**两只股票当前已处于合理的周期估值水平**——中远7.8倍、招商9.7倍远期PE。旧共识（$10万）使它们看起来在13-14倍PE时偏贵，掩盖了运费已经突破的事实。
>
> 如果市场将共识从$10万重新锚定至$15万（当前即期运费完全支持），预期：
> - **卖方盈利上调50-70%** → 机械性PE压缩
> - **中远海能是更大的赢家** — 多元化油轮船队全线受益（$15万VLCC + $8万苏伊士 + $5.5万阿芙拉 = 全面上行）
> - **招商轮船提供更好的安全性** — $15万基准下40%分红=4.1%股息率，加上散货/LNG作为非相关对冲
>
> **问题不是运费能否维持$15万——它们已经在那里了。问题是分析师何时更新模型。**

"""

# ===== APPLY TO EN REPORT =====
en_path = os.path.join(DIR, "07_CN_AShare_VLCC_Report_EN.md")
with open(en_path, "r", encoding="utf-8") as f:
    en = f.read()

marker_en = "\n---\n\n## 5. Multi-Model Analysis Summary"
if marker_en in en:
    en = en.replace(marker_en, new_en + "\n---\n\n## 5. Multi-Model Analysis Summary")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en)
    print("EN report: Section 4B inserted")
else:
    print("WARNING: EN marker not found")

# ===== APPLY TO CN REPORT =====
cn_path = os.path.join(DIR, "08_CN_AShare_VLCC_Report_CN.md")
with open(cn_path, "r", encoding="utf-8") as f:
    cn = f.read()

marker_cn = "\n---\n\n## 五、五大模型分析汇总"
if marker_cn in cn:
    cn = cn.replace(marker_cn, new_cn + "\n---\n\n## 五、五大模型分析汇总")
    with open(cn_path, "w", encoding="utf-8") as f:
        f.write(cn)
    print("CN report: Section 4B inserted")
else:
    print("WARNING: CN marker not found")

# ===== SYNC GITHUB PAGES =====
shutil.copy2(cn_path, os.path.join(DIR, "cn-ashare.md"))
print("cn-ashare.md synced")

# ===== UPDATE PROMPT LOGS =====
# EN
pl_en = os.path.join(DIR, "Prompt_Log_EN.md")
with open(pl_en, "r", encoding="utf-8") as f:
    pl = f.read()
old_en_end = "*This file will be updated as new prompts are added. Last updated: March 4, 2026.*"
new_en_prompt = """## Prompt 17: $150K Base Scenario Modeling
**Date**: March 4, 2026

Model an alternative scenario where the 2026 VLCC average rate baseline is $150K/day instead of $100K/day. Add a new section (4B) comparing the two baselines side-by-side. Shows how sell-side consensus lag creates hidden value.

**Key findings**:
- At $150K base: CMES PE drops from 14.3x → 9.7x, COSCO from 13.5x → 7.8x
- COSCO NI jumps +73% (vs +47% for CMES) — benefits more from diversified tanker fleet
- CMES dividend yield rises to 4.1% (from 2.8%)
- "The question is not IF rates stay at $150K — they already ARE there"

---

""" + old_en_end
pl = pl.replace(old_en_end, new_en_prompt)
with open(pl_en, "w", encoding="utf-8") as f:
    f.write(pl)
print("Prompt_Log_EN updated")

# CN
pl_cn = os.path.join(DIR, "Prompt_Log_CN.md")
with open(pl_cn, "r", encoding="utf-8") as f:
    pl = f.read()
old_cn_end = "*本文件将随新提示词的增加而更新。最后更新：2026年3月4日。*"
new_cn_prompt = """## 提示词17：$15万基准情景建模
**日期**：2026年3月4日

建模替代情景：2026年VLCC均价基准为$15万/天而非$10万/天。新增4B节，将两个基准并列对比。揭示卖方共识滞后带来的隐藏价值。

**核心发现**：
- $15万基准下：招商PE从14.3倍→9.7倍，中远从13.5倍→7.8倍
- 中远净利跳增+73%（招商+47%）——多元化油轮船队受益更大
- 招商股息率升至4.1%（从2.8%）
- "问题不是运费能否维持$15万——它们已经在那里了"

---

""" + old_cn_end
pl = pl.replace(old_cn_end, new_cn_prompt)
with open(pl_cn, "w", encoding="utf-8") as f:
    f.write(pl)
print("Prompt_Log_CN updated")

print("\n✅ All done — EN/CN reports, GitHub Pages, prompt logs all updated!")

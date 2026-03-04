#!/usr/bin/env python3
"""
Comprehensive dual-scenario update for VLCC A-share reports.
Updates ALL sections (TL;DR, Section 5, Section 9, Appendix) in both EN and CN.
Also updates RULES.md, prompt logs, and syncs GitHub Pages.
"""
import os, shutil

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_between(text, start_marker, end_marker, new_content):
    """Replace text between start_marker (inclusive) and end_marker (exclusive)."""
    si = text.find(start_marker)
    if si == -1:
        print(f"  WARNING: start not found: {start_marker[:80]}")
        return text
    ei = text.find(end_marker, si + len(start_marker))
    if ei == -1:
        print(f"  WARNING: end not found: {end_marker[:80]}")
        return text
    return text[:si] + new_content + text[ei:]

# ========================================
# EN REPORT
# ========================================
print("=== Updating EN Report ===")
en = read_file('07_CN_AShare_VLCC_Report_EN.md')

# 1. TL;DR: Replace from "| **2026E NI (consensus" to "**All 5 models"
en_tldr_new = """| **2026E NI (consensus $100K)** | ~RMB 10.0B | RMB 9-11B |
| **2026E NI ($150K base — current spot)** | **RMB 14.7B** | **RMB 17.3B** |
| **PE (TTM)** | 28.38x | ~28.7x |
| **PE ($100K consensus)** | 14.3x | 13.5x |
| **PE ($150K base)** | **9.7x** | **7.8x** |
| **Consensus Rating** | ⭐⭐⭐⭐ STRONG BUY | ⭐⭐⭐⭐ STRONG BUY |
| **12M Target ($100K, PE 12x)** | RMB 15 (-15%) | RMB 21 (-12%) |
| **12M Target ($150K, PE 12x)** | **RMB 22 (+24%)** | **RMB 37 (+55%)** |
| **12M Bull ($150K, PE 15x)** | **RMB 27 (+54%)** | **RMB 46 (+92%)** |
| **Key Strength** | Higher VLCC leverage + 40% div (4.1% at $150K) | LNG defense + diversified tanker upside |

**All 5 models agree: Both stocks are significantly UNDERVALUED for a cycle peak. At current spot rates ($150K+), sell-side consensus is 50-70% behind reality.**

"""

en = replace_between(en,
    '| **2026E NI (consensus $100K)** |',
    '\n---\n\n## 1.',
    en_tldr_new)
print("  TL;DR updated")

# 2. Section 5 Corrected Consensus
en_s5_new = """### Corrected Consensus Target Prices — Dual Scenario

**Scenario A: $100K Consensus (Sell-Side Base)**

| | CMES (601872) | COSCO Energy (600026) |
|---|---|---|
| **2026E NI** | RMB 10.0B | RMB 10.0B |
| **12M TP (PE 10x)** | RMB 12.4 (-30%) | RMB 17.6 (-26%) |
| **12M TP (PE 12x)** | RMB 14.9 (-16%) | RMB 21.2 (-11%) |
| **12M TP (PE 15x)** | RMB 18.6 (+5%) | RMB 26.5 (+11%) |

**Scenario B: $150K Base (Current Spot Reality)**

| | CMES (601872) | COSCO Energy (600026) |
|---|---|---|
| **2026E NI (full portfolio)** | RMB 14.7B | RMB 17.3B |
| **12M TP (PE 10x)** | **RMB 18.2** (+3%) | **RMB 30.5** (+28%) |
| **12M TP (PE 12x)** | **RMB 22** (+24%) | **RMB 37** (+55%) |
| **12M TP (PE 15x, re-rate)** | **RMB 27** (+54%) | **RMB 46** (+92%) |

> **The $50K consensus gap ($100K vs $150K) creates a 47-73% hidden earnings upside.** Target prices under Scenario A look unattractive; under Scenario B, massive upside remains. The key investment question: when will sell-side re-anchor to $150K?

"""

en = replace_between(en,
    '### Corrected Consensus Target Prices',
    '\n---\n\n## 6.',
    en_s5_new)
print("  Section 5 updated")

# 3. Section 9 (THE KEY)
en_s9_new = """## 9. Investment Recommendation — Multi-Model Consensus (Dual Scenario)

### 9A. Target Prices: $100K Consensus vs $150K Base vs $200K Bull

> The single biggest variable in valuing these stocks is the VLCC rate assumption. Sell-side consensus uses ~$100K/day; current spot is $150-210K/day. **Your target price depends entirely on which you believe.**

| | $100K Consensus | $150K Base | $200K Bull |
|---|---|---|---|
| **CMES 2026E NI** | RMB 10.0B | **RMB 14.7B** | RMB 19.0B |
| **COSCO 2026E NI** | RMB 10.0B | **RMB 17.3B** | RMB 23.2B |
| | | | |
| **CMES PE at 17.71** | 14.3x | **9.7x** | 7.5x |
| **COSCO PE at 23.79** | 13.5x | **7.8x** | 5.8x |
| | | | |
| **CMES TP (PE 10x)** | RMB 12.4 (-30%) | **RMB 18.2 (+3%)** | RMB 23.5 (+33%) |
| **CMES TP (PE 12x)** | RMB 14.9 (-16%) | **RMB 22 (+24%)** | RMB 28.2 (+59%) |
| **CMES TP (PE 15x)** | RMB 18.6 (+5%) | **RMB 27 (+54%)** | RMB 35.3 (+99%) |
| | | | |
| **COSCO TP (PE 10x)** | RMB 17.6 (-26%) | **RMB 30.5 (+28%)** | RMB 40.9 (+72%) |
| **COSCO TP (PE 12x)** | RMB 21.2 (-11%) | **RMB 37 (+55%)** | RMB 49.1 (+106%) |
| **COSCO TP (PE 15x)** | RMB 26.5 (+11%) | **RMB 46 (+92%)** | RMB 61.4 (+158%) |
| | | | |
| **CMES Div Yield (40% payout)** | 2.8% | **4.1%** | 5.3% |
| **COSCO Earnings Growth YoY** | +100% | **+268%** | +400%+ |

### 9B. Investment Verdict by Scenario

**If you believe $100K consensus (sell-side base):**
- CMES is fairly valued to slightly expensive at 14.3x forward PE
- COSCO has mild upside if PE re-rates to 10-12x, but limited
- Allocation: Underweight both, wait for cheaper entry below RMB 15 / RMB 20
- This scenario assumes rates halve from current spot — requires Hormuz de-escalation + demand collapse

**If you believe $150K base (current spot supports this):**
- CMES: 24-54% upside at PE 12-15x. 4.1% dividend yield provides income floor
- COSCO: 55-92% upside at PE 12-15x. Diversified tanker fleet captures broad cycle
- Allocation: Overweight both. CMES for safety, COSCO for growth
- This is the **base case** — spot is already here, supply gap lasts until 2028

**If you believe $200K bull (Hormuz escalation persists):**
- CMES: 59-99% upside. Dividend yield 5.3%. Deep value territory
- COSCO: 106-158% upside. PE could compress to 5.8x at peak — approaching COSCO Holdings 2021 territory
- Allocation: Maximum overweight. Both become "must-own" positions
- Requires: Hormuz crisis sustained + shadow fleet fully exits + rate momentum continues

### 9C. Final Ratings

| | CMES (601872) | COSCO Energy (600026) |
|---|---|---|
| **Consensus Rating** | **STRONG BUY** (5/5 models) | **STRONG BUY** (5/5 models) |
| **Scenario** | $100K / $150K / $200K | $100K / $150K / $200K |
| **12M TP (PE 12x)** | 14.9 / **22** / 28.2 | 21.2 / **37** / 49.1 |
| **12M TP (PE 15x)** | 18.6 / **27** / 35.3 | 26.5 / **46** / 61.4 |
| **Upside (PE 12x)** | -16% / **+24%** / +59% | -11% / **+55%** / +106% |
| **Downside Risk** | RMB 12-14 (-20% to -33%) | RMB 16-18 (-25% to -33%) |
| **Our Base Case** | **$150K, PE 12x = RMB 22** | **$150K, PE 12x = RMB 37** |

### 9D. Portfolio Allocation

| Strategy | CMES | COSCO | Rationale |
|---|---|---|---|
| **Conservative ($100K)** | 60% | 40% | Dividend safety, lower risk |
| **Balanced ($150K base)** | 50% | 50% | Equal upside, hedged |
| **Aggressive ($150K+)** | 40% | 60% | COSCO fleet growth + LNG + diversified tanker leverage |
| **Max Bull ($200K)** | 35% | 65% | COSCO's 98 non-VLCC tankers amplify cycle |
| **Tactical (Today)** | 70% | 30% | CMES limit-down = forced-selling entry point |

### 9E. Key Triggers & Milestones to Watch

| Trigger | Impact on Thesis | Action |
|---|---|---|
| **Sell-side upgrades from $100K to $130-150K** | Mechanical PE compression, stock re-rate | Hold / add |
| **Q1 2026 earnings (April)** | First quarter of $150K+ rates, massive beat | Buy ahead of earnings |
| **Hormuz resolution** | $150K to $50-70K, thesis collapses | Stop-loss, exit 50%+ |
| **New VLCC orders** | Long-dated, no impact until 2030 | Ignore short-term noise |
| **Shadow fleet re-entry** | 5-8% supply return, rates -15-20% | Reduce if >10% capacity |
| **COSCO LNG delivery schedule** | Cash flow certainty, PE re-rate | Positive for COSCO |

### 9F. Summary

> **Our base case: VLCC $150K/day for 2026 (current spot supports this).**
>
> At $150K: CMES trades at 9.7x PE with 4.1% dividend yield — a classic mid-cycle value play. COSCO trades at 7.8x PE with 268% earnings growth — a cycle-peak compressor. Both are **STRONG BUYs**.
>
> Under the old $100K consensus, neither stock looks attractive (14x PE, limited upside). This is precisely the opportunity — **the market is still pricing $100K when reality is $150K+**. As analysts upgrade, expect 30-90% mechanical upside.
>
> **Key differentiation:**
> - **CMES = "Dividend + Safety"**: 4.1% yield at $150K, younger VLCCs, dry bulk hedge. Best for income-oriented portfolios.
> - **COSCO = "Growth + Optionality"**: 55-92% upside, 98 non-VLCC tankers capturing broad cycle, LNG defensive floor. Best for total-return portfolios.
>
> **Recommended action**: Accumulate both at current levels. CMES 50%, COSCO 50%. Combined: 15-20% of portfolio. Hard stop at -25%. Add on any dip below RMB 16 (CMES) / RMB 22 (COSCO).

"""

en = replace_between(en,
    '## 9. Investment Recommendation',
    '\n---\n\n## Appendix',
    en_s9_new)
print("  Section 9 updated")

# 4. Appendix PE table
en_app_new = """| Company | PE (TTM) | Fwd PE ($100K) | Fwd PE ($150K) | Fwd PE ($200K) | Div Yield | PB |
|---|---|---|---|---|---|---|
| DHT | ~15x | ~8x | ~6x | ~4x | ~8-10% | ~1.8x |
| FRO | ~12x | ~7x | ~5x | ~3.5x | ~6-8% | ~2.5x |
| CMES | 28.4x | 14.3x | **9.7x** | **7.5x** | 2.8-4.1% | 3.09x |
| COSCO Energy | ~28.7x | 13.5x | **7.8x** | **5.8x** | ~3-4% | N/A |

**A-share PE premium: ~1.7-2.0x vs US peers at $150K forward earnings.** At $100K consensus the gap looks wider (14x vs 6-8x), but this overstates the "premium" because sell-side hasn't re-anchored to $150K yet. At $150K, the premium narrows to 1.3-1.6x — within normal A-share range for cyclical SOEs.
"""

en = replace_between(en,
    '| Company | PE (TTM) | Forward PE (at $150K VLCC)',
    '\n### Method 4',
    en_app_new)
print("  Appendix PE updated")

write_file('07_CN_AShare_VLCC_Report_EN.md', en)
print("EN report saved")

# ========================================
# CN REPORT
# ========================================
print("\n=== Updating CN Report ===")
cn = read_file('08_CN_AShare_VLCC_Report_CN.md')

# 1. CN TL;DR
cn_tldr_new = """| **2026E净利润（共识$10万）** | ~100亿元 | 90-110亿元 |
| **2026E净利润（$15万基准——当前即期）** | **147亿元** | **173亿元** |
| **PE（TTM）** | 28.38倍 | ~28.7倍 |
| **PE（$10万共识）** | 14.3倍 | 13.5倍 |
| **PE（$15万基准）** | **9.7倍** | **7.8倍** |
| **一致评级** | ⭐⭐⭐⭐ 强烈推荐 | ⭐⭐⭐⭐ 强烈推荐 |
| **12M目标（$10万，PE 12倍）** | 14.9元（-16%） | 21.2元（-11%） |
| **12M目标（$15万，PE 12倍）** | **22元（+24%）** | **37元（+55%）** |
| **12M牛市（$15万，PE 15倍）** | **27元（+54%）** | **46元（+92%）** |
| **核心优势** | 高VLCC弹性 + 40%分红（$15万下4.1%） | LNG防御 + 多元化油轮弹性 |

**五大模型一致认为：两只股票在周期顶部均显著低估。以当前即期运费（$15万+）计算，卖方共识落后现实50-70%。**

"""

cn = replace_between(cn,
    '| **2026E净利润（共识$10万）** |',
    '\n---\n\n## 一',
    cn_tldr_new)
print("  TL;DR updated")

# 2. CN Section 5 Corrected Consensus
cn_s5_new = """### 修正后一致目标价 — 双情景对比

**情景A：$10万共识（卖方基准）**

| | 招商轮船 (601872) | 中远海能 (600026) |
|---|---|---|
| **2026E净利** | 100亿 | 100亿 |
| **12M目标（PE 10倍）** | 12.4元（-30%） | 17.6元（-26%） |
| **12M目标（PE 12倍）** | 14.9元（-16%） | 21.2元（-11%） |
| **12M目标（PE 15倍）** | 18.6元（+5%） | 26.5元（+11%） |

**情景B：$15万基准（当前即期支持）**

| | 招商轮船 (601872) | 中远海能 (600026) |
|---|---|---|
| **2026E净利（全组合）** | 147亿 | 173亿 |
| **12M目标（PE 10倍）** | **18.2元**（+3%） | **30.5元**（+28%） |
| **12M目标（PE 12倍）** | **22元**（+24%） | **37元**（+55%） |
| **12M目标（PE 15倍，重估）** | **27元**（+54%） | **46元**（+92%） |

> **$5万的共识差距（$10万 vs $15万）创造了47-73%的隐藏盈利上行空间。**情景A下目标价吸引力不足；情景B下仍有巨大上行空间。核心投资问题：卖方何时将基准重新锚定至$15万？

"""

cn = replace_between(cn,
    '### 修正后一致目标价',
    '\n---\n\n## 六',
    cn_s5_new)
print("  Section 5 updated")

# 3. CN Section 9
cn_s9_new = """## 九、投资建议 — 多模型一致结论（双情景分析）

### 9A. 目标价格：$10万共识 vs $15万基准 vs $20万牛市

> 估值这两只股票的最大变量是VLCC运费假设。卖方共识约$10万/天；当前即期$15-21万/天。**你的目标价完全取决于你相信哪个。**

| | $10万共识 | $15万基准 | $20万牛市 |
|---|---|---|---|
| **招商2026E净利** | 100亿 | **147亿** | 190亿 |
| **中远2026E净利** | 100亿 | **173亿** | 232亿 |
| | | | |
| **招商PE（17.71元）** | 14.3倍 | **9.7倍** | 7.5倍 |
| **中远PE（23.79元）** | 13.5倍 | **7.8倍** | 5.8倍 |
| | | | |
| **招商目标（PE 10倍）** | 12.4元（-30%） | **18.2元（+3%）** | 23.5元（+33%） |
| **招商目标（PE 12倍）** | 14.9元（-16%） | **22元（+24%）** | 28.2元（+59%） |
| **招商目标（PE 15倍）** | 18.6元（+5%） | **27元（+54%）** | 35.3元（+99%） |
| | | | |
| **中远目标（PE 10倍）** | 17.6元（-26%） | **30.5元（+28%）** | 40.9元（+72%） |
| **中远目标（PE 12倍）** | 21.2元（-11%） | **37元（+55%）** | 49.1元（+106%） |
| **中远目标（PE 15倍）** | 26.5元（+11%） | **46元（+92%）** | 61.4元（+158%） |
| | | | |
| **招商股息率（40%派息）** | 2.8% | **4.1%** | 5.3% |
| **中远盈利增速（同比）** | +100% | **+268%** | +400%+ |

### 9B. 分情景投资判断

**如果你相信$10万共识（卖方基准）：**
- 招商轮船在14.3倍远期PE下估值合理甚至偏贵
- 中远海能若PE重估至10-12倍有温和上行，但空间有限
- 配置建议：低配两者，等待15元/20元以下更便宜的入场价
- 该情景假设运费从当前即期腰斩——需要霍尔木兹缓和+需求崩塌

**如果你相信$15万基准（当前即期支持）：**
- 招商轮船：PE 12-15倍下有24-54%上行空间，4.1%股息率提供收入安全垫
- 中远海能：PE 12-15倍下有55-92%上行空间，多元化油轮船队捕获广泛周期红利
- 配置建议：超配两者。招商用于安全，中远用于增长
- 这是**基准情景**——即期已在此水平，供给缺口持续至2028年

**如果你相信$20万牛市（霍尔木兹危机持续）：**
- 招商轮船：59-99%上行空间。股息率5.3%。深度价值区间
- 中远海能：106-158%上行空间。PE可压至5.8倍——接近中远海控2021年水平
- 配置建议：最大超配。两者均成为"必须持有"的仓位
- 需要：霍尔木兹危机持续 + 影子船队完全退出 + 运费动能延续

### 9C. 最终评级

| | 招商轮船 (601872) | 中远海能 (600026) |
|---|---|---|
| **一致评级** | **强烈推荐**（5/5模型） | **强烈推荐**（5/5模型） |
| **情景** | $10万 / $15万 / $20万 | $10万 / $15万 / $20万 |
| **12M目标（PE 12倍）** | 14.9 / **22** / 28.2 | 21.2 / **37** / 49.1 |
| **12M目标（PE 15倍）** | 18.6 / **27** / 35.3 | 26.5 / **46** / 61.4 |
| **上行空间（PE 12倍）** | -16% / **+24%** / +59% | -11% / **+55%** / +106% |
| **下行风险** | 12-14元（-20%至-33%） | 16-18元（-25%至-33%） |
| **我们的基准判断** | **$15万，PE 12倍 = 22元** | **$15万，PE 12倍 = 37元** |

### 9D. 组合配置

| 策略 | 招商 | 中远 | 理由 |
|---|---|---|---|
| **保守型（$10万）** | 60% | 40% | 分红安全，风险较低 |
| **均衡型（$15万基准）** | 50% | 50% | 上行均衡，相互对冲 |
| **进取型（$15万+）** | 40% | 60% | 中远船队增长+LNG+多元化油轮杠杆 |
| **最大牛市（$20万）** | 35% | 65% | 中远98艘非VLCC油轮放大周期效应 |
| **当日战术** | 70% | 30% | 招商跌停=被迫卖出的最佳买点 |

### 9E. 关键触发因素与监控指标

| 触发因素 | 对论点的影响 | 操作建议 |
|---|---|---|
| **卖方上调预期从$10万到$13-15万** | 机械性PE压缩，股价重估 | 持有/加仓 |
| **Q1 2026业绩（4月）** | $15万+运费下的首个完整季度，大幅超预期 | 业绩前买入 |
| **霍尔木兹缓和** | $15万降至$5-7万，核心逻辑崩塌 | 止损，减仓50%+ |
| **新VLCC订单** | 远期交付，2030年前无影响 | 忽略短期噪音 |
| **影子船队回归** | 5-8%供给回归，运费-15-20% | 若回归>10%运力则减仓 |
| **中远LNG交付进度** | 现金流确定性，PE重估 | 利好中远 |

### 9F. 总结

> **我们的基准判断：2026年VLCC均价$15万/天（当前即期完全支持）。**
>
> 在$15万基准下：招商轮船以9.7倍PE交易，股息率4.1%——经典的周期中段价值标的。中远海能以7.8倍PE交易，盈利增速268%——周期顶部的PE压缩标的。两者均为**强烈推荐**。
>
> 在旧的$10万共识下，两只股票都不具吸引力（14倍PE，上行有限）。这恰恰是机会所在——**市场仍在按$10万定价，而现实是$15万+**。随着分析师上调预期，预计有30-90%的机械性上行空间。
>
> **核心差异化：**
> - **招商轮船 = "分红+安全"**：$15万下4.1%股息率，更年轻的VLCC，散货对冲。最适合追求收入的组合。
> - **中远海能 = "增长+期权"**：55-92%上行空间，98艘非VLCC油轮捕获广泛周期红利，LNG防御底仓。最适合追求总回报的组合。
>
> **建议操作**：当前价位两者均可建仓。招商50%，中远50%。合计仓位：组合15-20%。硬止损-25%。招商跌破16元/中远跌破22元加仓。

"""

cn = replace_between(cn,
    '## 九、投资建议',
    '\n---\n\n## 附录',
    cn_s9_new)
print("  Section 9 updated")

# 4. CN Appendix PE table
cn_app_new = """| 公司 | PE（TTM） | 远期PE（$10万） | 远期PE（$15万） | 远期PE（$20万） | 股息率 | PB |
|---|---|---|---|---|---|---|
| DHT | ~15倍 | ~8倍 | ~6倍 | ~4倍 | ~8-10% | ~1.8倍 |
| FRO | ~12倍 | ~7倍 | ~5倍 | ~3.5倍 | ~6-8% | ~2.5倍 |
| 招商轮船 | 28.4倍 | 14.3倍 | **9.7倍** | **7.5倍** | 2.8-4.1% | 3.09倍 |
| 中远海能 | ~28.7倍 | 13.5倍 | **7.8倍** | **5.8倍** | ~3-4% | 未披露 |

**A股远期PE溢价：$15万下约1.7-2.0倍。**在$10万共识下差距看起来更大（14倍 vs 6-8倍），但这高估了"溢价"，因为卖方尚未将基准调至$15万。在$15万下溢价收窄至1.3-1.6倍——处于A股周期性央企的正常范围内。
"""

cn = replace_between(cn,
    '| 公司 | PE（TTM） | 远期PE（$15万运费）',
    '\n### 方法四',
    cn_app_new)
print("  Appendix PE updated")

write_file('08_CN_AShare_VLCC_Report_CN.md', cn)
print("CN report saved")

# ========================================
# SYNC GITHUB PAGES
# ========================================
shutil.copy('08_CN_AShare_VLCC_Report_CN.md', 'cn-ashare.md')
print("\ncn-ashare.md synced")

# ========================================
# UPDATE RULES.md
# ========================================
print("\n=== Updating RULES.md ===")
rules = read_file('RULES.md')

rule14 = """

### Rule 14: Whole-File Scenario Consistency
When adding a new scenario or assumption (e.g., $150K base vs $100K consensus), **update EVERY section of the report** that references the affected metrics — not just add a standalone section. Specifically:
- TL;DR / executive summary must show all scenarios
- All target price tables must show dual/triple scenario columns
- Investment recommendation (Section 9) MUST include scenario-specific advice, target prices, and allocation
- Cross-market comparisons must show forward PE under all scenarios
- Any section with PE, NI, EPS, or target prices must reflect all modeled scenarios

**Rationale**: A standalone "Section 4B" is insufficient if Section 9 still only references the old assumption. The reader of Section 9 (the most important section) must see the full picture without scrolling back."""

if 'Rule 14' not in rules:
    # Insert after Rule 13
    rules = rules.replace(
        "### Rule 13: Chart Updates\nWhen data changes, regenerate any affected charts. Don't leave stale visualizations.",
        "### Rule 13: Chart Updates\nWhen data changes, regenerate any affected charts. Don't leave stale visualizations." + rule14
    )
    write_file('RULES.md', rules)
    print("Rule 14 added")
else:
    print("Rule 14 already exists")

# ========================================
# UPDATE PROMPT LOGS
# ========================================
print("\n=== Updating Prompt Logs ===")

# EN
en_log = read_file('Prompt_Log_EN.md')
if 'Prompt 18' not in en_log:
    prompt18_en = """

## Prompt 18: Full-Report Dual-Scenario Consistency
**Date**: March 4, 2026

Section 4B was added for the $150K scenario, but the rest of the report (TL;DR, Section 5, Section 9 especially) was NOT updated to include $100K/$150K/$200K comparison. Go through the WHOLE report and update every section with dual-scenario target prices, PE, and investment advice. Section 9 (investment recommendation) is the most important — must show scenario-specific targets, buy/sell triggers, and allocation advice.

Also add this as a standing rule in RULES.md: whenever a new scenario or assumption is added, update ALL sections referencing affected metrics, not just a standalone section.

**Key changes**:
- TL;DR: Now shows $100K and $150K PE side-by-side, dual target prices
- Section 5: Dual-scenario consensus targets (Scenario A vs B)
- Section 9: Completely overhauled into 9A-9F with full $100K/$150K/$200K matrix
- Section 9B: Scenario-specific investment verdict (what to do under each assumption)
- Section 9E: Key triggers and milestones to watch
- Appendix: Forward PE table now shows 3 scenarios across 4 companies
- RULES.md: Added Rule 14 (whole-file scenario consistency)

"""
    en_log = en_log.replace(
        '*This file will be updated as new prompts are added. Last updated: March 4, 2026.*',
        prompt18_en + '---\n\n*This file will be updated as new prompts are added. Last updated: March 4, 2026.*'
    )
    write_file('Prompt_Log_EN.md', en_log)
    print("Prompt_Log_EN updated with Prompt 18")

# CN
cn_log = read_file('Prompt_Log_CN.md')
if '提示词18' not in cn_log:
    prompt18_cn = """

## 提示词18：全报告双情景一致性更新
**日期**：2026年3月4日

4B节新增了$15万情景，但报告其余部分（核心结论、第五节、尤其是第九节）未同步更新为$10万/$15万/$20万双情景对比。全面检查报告，更新所有章节的目标价、PE和投资建议。第九节（投资建议）是最重要的部分——必须展示分情景目标价、买卖触发条件和配置建议。

同时将此规则写入RULES.md：每当新增情景或假设时，必须更新所有引用相关指标的章节，而非仅新增一个独立章节。

**核心变更**：
- 核心结论：现在并列展示$10万和$15万两个PE和目标价
- 第五节：双情景一致目标价（情景A vs 情景B）
- 第九节：完全重写为9A-9F，包含$10万/$15万/$20万完整矩阵
- 第9B节：分情景投资判断（每个假设下的操作建议）
- 第9E节：关键触发因素与监控指标
- 附录：远期PE表现在展示4家公司在3个情景下的PE
- RULES.md：新增规则14（全文件情景一致性）

"""
    cn_log = cn_log.replace(
        '*本文件将随新提示词的增加而更新。最后更新：2026年3月4日。*',
        prompt18_cn + '---\n\n*本文件将随新提示词的增加而更新。最后更新：2026年3月4日。*'
    )
    write_file('Prompt_Log_CN.md', cn_log)
    print("Prompt_Log_CN updated with Prompt 18")

# Sync session workspace
shutil.copy('RULES.md', os.path.expanduser('~/.copilot/session-state/1b35ff3f-2ff3-456a-b9dd-26ca4dd7d58b/files/VLCC_Project_Rules.md'))
print("Session workspace synced")

print("\n" + "="*50)
print("ALL DONE - Full dual-scenario update complete")
print("="*50)

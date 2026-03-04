#!/usr/bin/env python3
"""Update Section 4 (earnings) with full-portfolio model for both EN and CN reports"""
import os, shutil

DIR = r"C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026"

# ========== NEW ENGLISH SECTION 4 ==========
new_en_s4 = r"""## 4. 2026 Earnings Scenarios — Full Portfolio Model (CORRECTED)

> **⚠️ Previous version only modeled VLCC segment uplift.** Both CMES and COSCO Energy are diversified fleets. This corrected model calculates each segment separately using current market rates.

### Current Market Rates (March 2026)

| Vessel Type | Spot Rate | Consensus 2026 Avg | Breakeven (est.) |
|---|---|---|---|
| VLCC | $150-210K/day | ~$100K/day | ~$25K/day |
| Suezmax | $84-100K/day | ~$60K/day | ~$24K/day |
| Aframax/LR2 | $47-62K/day | ~$40K/day | ~$24K/day |
| MR/LR1 | $30-38K/day | ~$25K/day | ~$18K/day |
| Capesize (dry bulk) | ~$26K/day | ~$20K/day | ~$12K/day |
| LNG (long-term contract) | $30-50K/day (contract) | ~$40K/day | ~$20K/day |

### Sensitivity Per $10K/Day Rate Increase (per segment)

Formula: Ships × $10K × 365 days × ~70% spot exposure × (1-25% tax) ÷ 7.3 CNY/USD ≈ RMB 20M per ship per $10K

| Segment | CMES Ships | CMES Sensitivity | COSCO Ships | COSCO Sensitivity |
|---|---|---|---|---|
| VLCC | 52 | RMB 730M / $10K | 55 | RMB 770M / $10K |
| Suezmax | — | — | 18 | RMB 360M / $10K |
| Aframax/LR2 | — | — | 50 | RMB 1,000M / $10K |
| MR/LR1 | — | — | 30 | RMB 300M / $10K |
| Dry Bulk (VLOC/Cape) | 93 | RMB 650M / $10K* | — | — |
| LNG | 40-60 | ~RMB 200M (new deliveries) | 65 | ~RMB 300M (new deliveries) |

*CMES dry bulk sensitivity is lower per ship (~RMB 7M) because VLOCs are on long-term COA contracts (Vale/BHP), limiting spot exposure to ~35%.

### CMES (招商轮船) 2026E Full-Portfolio Earnings

**Consensus baseline: RMB 10.0B at $100K VLCC avg (all segments included)**

| Segment | Ships | 2025E NI | Consensus 2026E | Conservative | Base | Bull |
|---|---|---|---|---|---|---|
| **VLCC** | 52 | ~5.0B | ~5.5B | 6.9B (+$20K) | 9.2B (+$50K) | 12.8B (+$100K) |
| **LNG** | 40-60 | ~0.8B | ~1.5B | 1.7B | 1.8B | 2.0B |
| **Dry Bulk** | 93 | ~1.2B | ~1.5B | 1.8B | 2.0B | 2.3B |
| **Container** | 19 | ~0.6B | ~0.8B | 0.8B | 0.8B | 0.9B |
| **Ro-Ro/Other** | ~10 | ~0.3B | ~0.7B | 0.8B | 0.9B | 1.0B |
| **Total** | **~280** | **~6.3B** | **~10.0B** | **12.0B** | **14.7B** | **19.0B** |
| **EPS** | | 0.78 | 1.24 | **1.49** | **1.82** | **2.35** |
| **PE at 17.71** | | 22.7x | 14.3x | **11.9x** | **9.7x** | **7.5x** |

**Key assumptions for scenarios:**
- Conservative: VLCC $120K, Suez/Afra in line with consensus, dry bulk BDI ~2,400, LNG fleet growth (+10 ships)
- Base: VLCC $150K, Suez $80K, dry bulk BDI ~2,600, LNG fleet growth
- Bull: VLCC $200K, Suez $100K+, dry bulk BDI ~3,000, LNG spot contribution from crisis

### COSCO Energy (中远海能) 2026E Full-Portfolio Earnings

**Consensus baseline: RMB 10.0B at $100K VLCC avg (all segments included)**

> **Critical change**: COSCO's Suezmax (18) + Aframax/LR2 (50) + MR/LR1 (30) fleets are ALSO surging with the tanker super-cycle. The old VLCC-only model missed ~RMB 1.5-4.5B of additional tanker earnings.

| Segment | Ships | 2025E NI | Consensus 2026E | Conservative | Base | Bull |
|---|---|---|---|---|---|---|
| **VLCC** | 55 | ~3.5B | ~4.5B | 6.0B (+$20K) | 8.4B (+$50K) | 12.2B (+$100K) |
| **Suezmax** | 18 | ~1.0B | ~1.5B | 2.2B (+$20K) | 2.9B (+$40K) | 3.6B (+$60K) |
| **Aframax/LR2** | 50 | ~1.0B | ~1.5B | 2.3B (+$8K) | 3.0B (+$15K) | 4.0B (+$25K) |
| **MR/LR1** | 30 | ~0.3B | ~0.5B | 0.6B | 0.7B | 0.9B |
| **LNG** | 65 | ~1.5B | ~2.0B | 2.2B | 2.3B | 2.5B |
| **Total** | **~185** | **~4.7B** | **~10.0B** | **13.3B** | **17.3B** | **23.2B** |
| **EPS** | | 0.83 | 1.76 | **2.35** | **3.05** | **4.09** |
| **PE at 23.79** | | 28.7x | 13.5x | **10.1x** | **7.8x** | **5.8x** |

### Full-Portfolio vs VLCC-Only Comparison

| | CMES Old (VLCC only) | CMES New (Full) | COSCO Old (VLCC only) | COSCO New (Full) |
|---|---|---|---|---|
| Base NI ($150K) | 13.7B | **14.7B (+7%)** | 13.5B | **17.3B (+28%)** |
| Bull NI ($200K) | 17.3B | **19.0B (+10%)** | 16.9B | **23.2B (+37%)** |
| Base PE | 10.5x | **9.7x** | 10.0x | **7.8x** |
| Bull PE | 8.3x | **7.5x** | 8.0x | **5.8x** |

> **COSCO Energy benefits dramatically more from the full-portfolio model** — its 98 non-VLCC tankers (Suezmax + Aframax/LR2 + MR/LR1) are ALL surging with the tanker super-cycle, adding ~RMB 2-5B in earnings that the VLCC-only model completely missed. This makes COSCO's earnings upside **28-37% higher** than previously calculated.

### Updated Target Prices (Full-Portfolio Basis)

| | CMES (601872) | COSCO Energy (600026) |
|---|---|---|
| **2026E NI (Base, $150K avg)** | RMB 14.7B | RMB 17.3B |
| **12M Conservative TP (PE 10x)** | **RMB 18** (+2%) | **RMB 31** (+30%) |
| **12M Base TP (PE 8x)** | **RMB 15** (-15%)* | **RMB 24** (+1%)* |
| **12M Base TP (PE 10x)** | **RMB 18** (+2%) | **RMB 31** (+30%) |
| **12M Base TP (PE 12x)** | **RMB 22** (+24%) | **RMB 37** (+55%) |
| **12M Bull TP (PE 10x)** | **RMB 24** (+35%) | **RMB 41** (+72%) |

*Note: PE 8x on peak earnings is very aggressive (approaching 中远海控's 2022 terminal level). PE 10-12x is more realistic for mid-cycle pricing while rates remain elevated and supply is constrained.

> **Revised conclusion**: The full-portfolio model significantly favors COSCO Energy over CMES on pure earnings upside. COSCO's diversified tanker fleet captures the BROAD tanker super-cycle, not just VLCCs. CMES's advantage remains in dividend yield, younger VLCCs, and dry bulk diversification as a hedge."""

# ========== NEW CHINESE SECTION 4 ==========
new_cn_s4 = r"""## 四、2026年盈利情景测算——全组合模型（修正版）

> **⚠️ 前版仅计算了VLCC板块的运费弹性。**两家公司均为多元化船队。本修正版分别计算各板块盈利贡献。

### 当前市场运费（2026年3月）

| 船型 | 即期运费 | 共识2026年均值 | 盈亏平衡（估） |
|---|---|---|---|
| VLCC | $15-21万/天 | ~$10万/天 | ~$2.5万/天 |
| 苏伊士型 | $8.4-10万/天 | ~$6万/天 | ~$2.4万/天 |
| 阿芙拉/LR2 | $4.7-6.2万/天 | ~$4万/天 | ~$2.4万/天 |
| MR/LR1 | $3-3.8万/天 | ~$2.5万/天 | ~$1.8万/天 |
| 好望角散货 | ~$2.6万/天 | ~$2万/天 | ~$1.2万/天 |
| LNG（长约） | $3-5万/天（合约） | ~$4万/天 | ~$2万/天 |

### 各板块运费敏感性（每$1万/天涨幅）

| 板块 | 招商船数 | 招商敏感性 | 中远船数 | 中远敏感性 |
|---|---|---|---|---|
| VLCC | 52 | 7.3亿/$1万 | 55 | 7.7亿/$1万 |
| 苏伊士型 | — | — | 18 | 3.6亿/$1万 |
| 阿芙拉/LR2 | — | — | 50 | 10亿/$1万 |
| MR/LR1 | — | — | 30 | 3亿/$1万 |
| 散货（VLOC/好望角） | 93 | 6.5亿/$1万* | — | — |
| LNG | 40-60 | ~2亿（新交付） | 65 | ~3亿（新交付） |

*招商散货敏感性较低因VLOC签有长约（淡水河谷/必和必拓），现货敞口仅~35%。

### 招商轮船 2026E全组合盈利

**共识基准：100亿元（$10万VLCC均价，含全部板块）**

| 板块 | 船数 | 2025E | 共识2026E | 保守 | 基准 | 牛市 |
|---|---|---|---|---|---|---|
| **VLCC** | 52 | ~50亿 | ~55亿 | 69亿 | 92亿 | 128亿 |
| **LNG** | 40-60 | ~8亿 | ~15亿 | 17亿 | 18亿 | 20亿 |
| **散货** | 93 | ~12亿 | ~15亿 | 18亿 | 20亿 | 23亿 |
| **集装箱** | 19 | ~6亿 | ~8亿 | 8亿 | 8亿 | 9亿 |
| **滚装/其他** | ~10 | ~3亿 | ~7亿 | 8亿 | 9亿 | 10亿 |
| **合计** | **~280** | **~63亿** | **~100亿** | **120亿** | **147亿** | **190亿** |
| **EPS** | | 0.78元 | 1.24元 | **1.49元** | **1.82元** | **2.35元** |
| **PE（17.71元）** | | 22.7倍 | 14.3倍 | **11.9倍** | **9.7倍** | **7.5倍** |

### 中远海能 2026E全组合盈利

**共识基准：100亿元（$10万VLCC均价，含全部板块）**

> **关键变化**：中远的苏伊士（18艘）+ 阿芙拉/LR2（50艘）+ MR/LR1（30艘）同样受益于油轮超级周期。旧的VLCC单一模型遗漏了约15-45亿元的额外油轮收益。

| 板块 | 船数 | 2025E | 共识2026E | 保守 | 基准 | 牛市 |
|---|---|---|---|---|---|---|
| **VLCC** | 55 | ~35亿 | ~45亿 | 60亿 | 84亿 | 122亿 |
| **苏伊士型** | 18 | ~10亿 | ~15亿 | 22亿 | 29亿 | 36亿 |
| **阿芙拉/LR2** | 50 | ~10亿 | ~15亿 | 23亿 | 30亿 | 40亿 |
| **MR/LR1** | 30 | ~3亿 | ~5亿 | 6亿 | 7亿 | 9亿 |
| **LNG** | 65 | ~15亿 | ~20亿 | 22亿 | 23亿 | 25亿 |
| **合计** | **~185** | **~47亿** | **~100亿** | **133亿** | **173亿** | **232亿** |
| **EPS** | | 0.83元 | 1.76元 | **2.35元** | **3.05元** | **4.09元** |
| **PE（23.79元）** | | 28.7倍 | 13.5倍 | **10.1倍** | **7.8倍** | **5.8倍** |

### 全组合 vs 仅VLCC对比

| | 招商旧（仅VLCC） | 招商新（全组合） | 中远旧（仅VLCC） | 中远新（全组合） |
|---|---|---|---|---|
| 基准NI（$15万） | 136.5亿 | **147亿（+8%）** | 134.5亿 | **173亿（+29%）** |
| 牛市NI（$20万） | 173亿 | **190亿（+10%）** | 169亿 | **232亿（+37%）** |
| 基准PE | 10.5倍 | **9.7倍** | 10.0倍 | **7.8倍** |
| 牛市PE | 8.3倍 | **7.5倍** | 8.0倍 | **5.8倍** |

> **中远海能在全组合模型中受益巨大**——其98艘非VLCC油轮（苏伊士+阿芙拉/LR2+MR/LR1）同样随油轮超级周期暴涨，增加约15-45亿元被VLCC单一模型完全遗漏的收益。这使中远的盈利上行空间比此前计算**高出29-37%**。

### 更新后目标价（全组合基础）

| | 招商轮船 (601872) | 中远海能 (600026) |
|---|---|---|
| **2026E净利（基准，$15万均价）** | 147亿 | 173亿 |
| **12M保守目标（PE 10倍）** | **18元**（+2%） | **31元**（+30%） |
| **12M基准目标（PE 10倍）** | **18元**（+2%） | **31元**（+30%） |
| **12M基准目标（PE 12倍）** | **22元**（+24%） | **37元**（+55%） |
| **12M牛市目标（PE 10倍）** | **24元**（+35%） | **41元**（+72%） |

> **修正后结论**：全组合模型显著利好中远海能。其多元化油轮船队捕获了广泛的油轮超级周期红利，而非仅仅VLCC。招商轮船优势在于分红收益率、年轻VLCC船队和散货对冲。"""

# ========== APPLY UPDATES ==========
# EN report
en_path = os.path.join(DIR, "07_CN_AShare_VLCC_Report_EN.md")
with open(en_path, "r", encoding="utf-8") as f:
    en = f.read()

# Replace Section 4 (from "## 4." to "## 5.")
old_s4_start = "## 4. 2026 Earnings Scenarios (CORRECTED Sensitivity)"
old_s4_end = "\n---\n\n## 5. Multi-Model"
if old_s4_start in en:
    idx_start = en.index(old_s4_start)
    idx_end = en.index(old_s4_end)
    en = en[:idx_start] + new_en_s4 + "\n\n---\n\n## 5. Multi-Model" + en[idx_end + len(old_s4_end):]

    # Also update the consensus target prices table in Section 5
    old_consensus = """| | CMES (601872) | COSCO Energy (600026) |
|---|---|---|
| **2026E NI (Base, $150K avg)** | RMB 13.7B | RMB 13.5B |
| **12M Conservative TP** | **RMB 22** (+24%) | **RMB 28** (+18%) |
| **12M Base TP** | **RMB 25** (+41%) | **RMB 32** (+35%) |
| **12M Bull TP** | **RMB 35** (+98%) | **RMB 42** (+77%) |"""

    new_consensus = """| | CMES (601872) | COSCO Energy (600026) |
|---|---|---|
| **2026E NI (Base, $150K avg, full portfolio)** | RMB 14.7B | RMB 17.3B |
| **12M Conservative TP (PE 10x)** | **RMB 18** (+2%) | **RMB 31** (+30%) |
| **12M Base TP (PE 12x)** | **RMB 22** (+24%) | **RMB 37** (+55%) |
| **12M Bull TP (PE 10x)** | **RMB 24** (+35%) | **RMB 41** (+72%) |"""
    en = en.replace(old_consensus, new_consensus)

    # Update Section 9 final ratings
    old_final = """| **12M Base Target** | **RMB 25** (+41%) | **RMB 32** (+35%) |
| **12M Bull Target** | **RMB 35** (+98%) | **RMB 42** (+77%) |
| **Downside Risk** | RMB 12-14 (-20% to -33%) | RMB 16-18 (-25% to -33%) |"""
    new_final = """| **12M Base Target (PE 12x)** | **RMB 22** (+24%) | **RMB 37** (+55%) |
| **12M Bull Target (PE 10x)** | **RMB 24** (+35%) | **RMB 41** (+72%) |
| **Downside Risk** | RMB 12-14 (-20% to -33%) | RMB 16-18 (-25% to -33%) |"""
    en = en.replace(old_final, new_final)

    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en)
    print(f"Updated EN report (Section 4 + targets)")
else:
    print("WARNING: EN Section 4 marker not found")

# CN report
cn_path = os.path.join(DIR, "08_CN_AShare_VLCC_Report_CN.md")
with open(cn_path, "r", encoding="utf-8") as f:
    cn = f.read()

old_cn_s4_start = "## 四、2026年盈利情景测算（修正后敏感性）"
old_cn_s4_end = "\n---\n\n## 五、五大模型"
if old_cn_s4_start in cn:
    idx_start = cn.index(old_cn_s4_start)
    idx_end = cn.index(old_cn_s4_end)
    cn = cn[:idx_start] + new_cn_s4 + "\n\n---\n\n## 五、五大模型" + cn[idx_end + len(old_cn_s4_end):]

    # Update CN consensus targets
    old_cn_consensus = """| | 招商轮船 (601872) | 中远海能 (600026) |
|---|---|---|
| **2026E净利（基准，$15万均价）** | 136.5亿 | 134.5亿 |
| **12M保守目标** | **22元**（+24%） | **28元**（+18%） |
| **12M基准目标** | **25元**（+41%） | **32元**（+35%） |
| **12M牛市目标** | **35元**（+98%） | **42元**（+77%） |"""
    new_cn_consensus = """| | 招商轮船 (601872) | 中远海能 (600026) |
|---|---|---|
| **2026E净利（基准，$15万均价，全组合）** | 147亿 | 173亿 |
| **12M保守目标（PE 10倍）** | **18元**（+2%） | **31元**（+30%） |
| **12M基准目标（PE 12倍）** | **22元**（+24%） | **37元**（+55%） |
| **12M牛市目标（PE 10倍）** | **24元**（+35%） | **41元**（+72%） |"""
    cn = cn.replace(old_cn_consensus, new_cn_consensus)

    # Update CN final ratings
    old_cn_final = """| **12M基准目标** | **25元**（+41%） | **32元**（+35%） |
| **12M牛市目标** | **35元**（+98%） | **42元**（+77%） |
| **下行风险** | 12-14元（-20%至-33%） | 16-18元（-25%至-33%） |"""
    new_cn_final = """| **12M基准目标（PE 12倍）** | **22元**（+24%） | **37元**（+55%） |
| **12M牛市目标（PE 10倍）** | **24元**（+35%） | **41元**（+72%） |
| **下行风险** | 12-14元（-20%至-33%） | 16-18元（-25%至-33%） |"""
    cn = cn.replace(old_cn_final, new_cn_final)

    with open(cn_path, "w", encoding="utf-8") as f:
        f.write(cn)
    print(f"Updated CN report (Section 4 + targets)")
else:
    print("WARNING: CN Section 4 marker not found")

# Update cn-ashare.md (GitHub Pages)
shutil.copy2(cn_path, os.path.join(DIR, "cn-ashare.md"))
print("Updated cn-ashare.md (GitHub Pages)")

# Also update the TL;DR in both reports
for path, old_tldr, new_tldr in [
    (en_path,
     "| **12M Base Target** | RMB 25-29 (+41% to +64%) | RMB 32-38 (+35% to +60%) |",
     "| **12M Base Target** | RMB 18-22 (+2% to +24%) | RMB 31-37 (+30% to +55%) |"),
    (cn_path,
     "| **12M基准目标价** | 25-29元（+41%至+64%） | 32-38元（+35%至+60%） |",
     "| **12M基准目标价** | 18-22元（+2%至+24%） | 31-37元（+30%至+55%） |"),
]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old_tldr in content:
        content = content.replace(old_tldr, new_tldr)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated TL;DR in {os.path.basename(path)}")

# Copy updated CN to pages again
shutil.copy2(cn_path, os.path.join(DIR, "cn-ashare.md"))

print("\nAll reports updated with full-portfolio earnings model!")

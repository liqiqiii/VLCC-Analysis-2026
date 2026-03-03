#!/usr/bin/env python3
"""Add prominent correction notice near top of reports + fix stale references"""
import os

base = r'C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026'

# ============================================================
# EN CORRECTION NOTICE (after TL;DR section)
# ============================================================
en_notice = r"""
---

## ⚠️ IMPORTANT UPDATE: Charter Strategy Correction (March 3, 2026)

> This report was originally modeled with DHT's Q4 2025 charter mix (54% spot / 46% TC).
> Cross-checking against actual company guidance revealed **two critical corrections**:

### Correction 1: Booking Rate vs Charter Type — Two Different Metrics

Our original analysis confused **charter type** (structural spot/TC split) with **booking rate** (% of days already contracted). These are fundamentally different:

| Metric | What It Measures | DHT | FRO (VLCC) |
|--------|-----------------|-----|-----------|
| **Booking Rate** (Q1 2026) | Days already contracted for the quarter | **66% → 85%+** | **92%** |
| **Charter Type** (structural) | Fleet on spot market vs time charter | **54% → 75%** | **83%** |

FRO's 92% booking rate means **near-zero short-term revenue uncertainty** despite being 83% spot. "Spot" ≠ "unbooked." Spot vessels get fixed voyage-by-voyage BEFORE the quarter starts.

### Correction 2: DHT Is Shifting to 75% Spot by Q2 2026

DHT management announced on the Q4 2025 earnings call a **strategic pivot from ~50/50 balanced to 75% spot exposure** by Q2 2026. Our model used the stale 54% figure. The corrected numbers:

| Metric | Old (54% spot) | Corrected (75% spot) | Change |
|--------|:-:|:-:|:-:|
| **EPS at $107K** | $3.02 | **$3.68** | **+22%** |
| **P/E at $107K** | 6.4x | **5.3x** | More attractive |
| **EPS per $1K rate increase** | $0.029 | **$0.041** | **+39%** |
| **FRO/DHT sensitivity ratio** | 4.4x | **3.2x** | Gap narrows |
| **TC earnings floor** | $98M/yr | **$54M/yr** | Less downside cushion |
| **Stability score** | 7.0 | **5.6** | Closer to FRO (4.5) |
| **Recommended allocation** | FRO 65-70% / DHT 30-35% | **FRO 55-60% / DHT 40-45%** | DHT weight ↑ |

### What This Means

**DHT is converging toward FRO's strategy.** Both companies are now ~75-83% spot-exposed, betting on the super cycle. The remaining differentiation is:
- **FRO**: Scale advantage (81 vs 24 ships), multi-segment diversification, higher absolute earnings
- **DHT**: Lower leverage (D/E 0.38 vs 1.31), cheaper on EV/Profit basis, lower financial risk

All tables in **Module P** (at the end of this report) reflect the corrected 75% spot parameters.
All charts in `/charts/` have been regenerated with corrected data.

"""

# ============================================================
# CN CORRECTION NOTICE
# ============================================================
cn_notice = r"""
---

## ⚠️ 重要更新：租约策略数据修正（2026年3月3日）

> 本报告最初使用DHT的Q4 2025租约结构（54%现货/46%期租）建模。
> 经交叉验证公司实际指引后，发现**两项关键修正**：

### 修正1：锁定率 vs 租约类型 — 两个不同指标

原始分析混淆了**租约类型**（结构性现货/期租比例）与**锁定率**（已签约天数占比）。两者本质不同：

| 指标 | 衡量内容 | DHT | FRO (VLCC) |
|------|---------|-----|-----------|
| **锁定率**（Q1 2026） | 当季已签约天数占比 | **66% → 85%+** | **92%** |
| **租约类型**（结构性） | 船队在现货市场vs期租比例 | **54% → 75%** | **83%** |

FRO的92%锁定率意味着尽管83%是现货船，**近期收入不确定性几乎为零**。"现货" ≠ "未签约"。现货船在季初就逐航次签约完毕。

### 修正2：DHT正转向Q2 2026目标75%现货

DHT管理层在Q4 2025电话会上宣布**从约50/50均衡转向75%现货敞口**。我们的模型使用了过时的54%数据。修正后：

| 指标 | 旧（54%现货） | 修正后（75%现货） | 变化 |
|------|:-:|:-:|:-:|
| **$107K时EPS** | $3.02 | **$3.68** | **+22%** |
| **$107K时P/E** | 6.4x | **5.3x** | 更具吸引力 |
| **每$1K运价增EPS** | $0.029 | **$0.041** | **+39%** |
| **FRO/DHT敏感度比** | 4.4x | **3.2x** | 差距收窄 |
| **期租收益底线** | $98M/年 | **$54M/年** | 下行缓冲减少 |
| **稳定性评分** | 7.0 | **5.6** | 趋近FRO（4.5） |
| **建议配置** | FRO 65-70% / DHT 30-35% | **FRO 55-60% / DHT 40-45%** | DHT权重↑ |

### 这意味着什么

**DHT正在向FRO的策略趋同。**两家公司现在都是~75-83%现货敞口，都在押注超级周期。剩余的差异化在于：
- **FRO**：规模优势（81 vs 24船）、多船型分散、更高绝对盈利
- **DHT**：低杠杆（D/E 0.38 vs 1.31）、EV/利润口径更便宜、更低金融风险

报告末尾**模块P**中的所有表格均已按修正后的75%现货参数更新。
`/charts/`中的所有图表均已用修正数据重新生成。

"""

# ============================================================
# INSERT INTO REPORTS
# ============================================================

def insert_after_tldr(content, notice, lang='en'):
    """Insert the correction notice right after the TL;DR section"""
    if lang == 'en':
        # Find the end of TL;DR section (next ## header after TL;DR)
        tldr_start = content.find('## TL;DR')
        if tldr_start < 0:
            tldr_start = content.find('## TL')
    else:
        tldr_start = content.find('## TL;DR')
        if tldr_start < 0:
            tldr_start = content.find('## 执行摘要')
    
    if tldr_start < 0:
        print(f"  WARNING: TL;DR not found in {lang}, inserting after first ---")
        first_hr = content.find('\n---\n')
        if first_hr > 0:
            insert_at = first_hr + 5
        else:
            insert_at = 0
    else:
        # Find the next ## section after TL;DR
        next_section = content.find('\n## ', tldr_start + 10)
        if next_section < 0:
            next_section = len(content)
        # Find the --- before the next section
        dash_before = content.rfind('\n---\n', tldr_start, next_section)
        if dash_before > 0:
            insert_at = dash_before
        else:
            insert_at = next_section
    
    return content[:insert_at] + notice + content[insert_at:]

# Process EN
en_path = os.path.join(base, '05_Deep_Dive_Day1Global_Framework.md')
with open(en_path, 'r', encoding='utf-8') as f:
    en_content = f.read()

# Check if notice already exists
if 'IMPORTANT UPDATE: Charter Strategy Correction' not in en_content:
    en_new = insert_after_tldr(en_content, en_notice, 'en')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_new)
    print(f"EN: Inserted correction notice ({len(en_content)} -> {len(en_new)} chars)")
else:
    print("EN: Correction notice already present, skipping")
    en_new = en_content

# Process CN
cn_path = os.path.join(base, '06_Deep_Dive_Day1Global_Framework_CN.md')
with open(cn_path, 'r', encoding='utf-8') as f:
    cn_content = f.read()

if '重要更新：租约策略数据修正' not in cn_content:
    cn_new = insert_after_tldr(cn_content, cn_notice, 'cn')
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(cn_new)
    print(f"CN: Inserted correction notice ({len(cn_content)} -> {len(cn_new)} chars)")
else:
    print("CN: Correction notice already present, skipping")
    cn_new = cn_content

# Update index.md
index_path = os.path.join(base, 'index.md')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(cn_new)
print("index.md updated")

# Fix the stale chart reference in Module P
en_path2 = os.path.join(base, '05_Deep_Dive_Day1Global_Framework.md')
with open(en_path2, 'r', encoding='utf-8') as f:
    c = f.read()
old_chart_ref = 'charts reflect old 54% spot model;\ncorrected 75% spot curves would show'
new_chart_ref = 'charts have been regenerated with corrected 75% spot parameters.\nOld vs new DHT curves shown'
if old_chart_ref in c:
    c = c.replace(old_chart_ref, new_chart_ref)
    with open(en_path2, 'w', encoding='utf-8') as f:
        f.write(c)
    print("EN: Fixed stale chart reference")

# Verify
for label, path in [('EN', en_path), ('CN', cn_path)]:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    # Find the correction notice
    for i, line in enumerate(lines):
        if 'IMPORTANT UPDATE' in line or '重要更新' in line:
            print(f"{label}: Correction notice at line {i+1}")
            break
    else:
        print(f"{label}: WARNING - correction notice NOT FOUND")

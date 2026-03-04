#!/usr/bin/env python3
"""Create GitHub Pages: hub index, A-share page, README"""
import os, shutil

DIR = r"C:\Users\liqiqi\Documents\VLCC_Analysis_Mar2026"

# 1. Copy CN A-share report as the separate page
shutil.copy2(
    os.path.join(DIR, "08_CN_AShare_VLCC_Report_CN.md"),
    os.path.join(DIR, "cn-ashare.md")
)
print("Created cn-ashare.md from CN report")

# 2. New hub index.md (landing page)
index_content = r"""---
layout: default
title: VLCC Analysis Hub
---

# VLCC 超级周期深度分析 | VLCC Super Cycle Deep Dive
### Multi-Model AI Valuation Research — 2026

---

## 📊 研究报告 | Research Reports

### 🇺🇸 US-Listed: DHT Holdings vs Frontline (FRO)

Deep-dive comparative analysis of the two largest US-listed pure-play VLCC operators, using the Day1Global tech-earnings-deepdive framework across 5 AI models.

**[📄 DHT vs FRO 深度分析（中文）→](dht-fro)**

Key findings:
- DHT: 12M base target $28 (+44%), pure VLCC play with 75% spot exposure
- FRO: 12M base target $49.50 (+30%), higher leverage + mixed fleet
- Operating leverage: LR2 has 3.45x multiplier, VLCC 2.79x above breakeven
- Charter strategy corrected: DHT shifting to 75% spot by Q2 2026

📎 English version: [05_Deep_Dive_Day1Global_Framework.md](05_Deep_Dive_Day1Global_Framework)

---

### 🇨🇳 A-Share: 招商轮船 (CMES) vs 中远海能 (COSCO Energy)

Comprehensive analysis of China's two largest VLCC operators on the A-share market, with 中远海控 container cycle (2020-2022) PE/PB compression as valuation reference.

**[📄 招商轮船 vs 中远海能 深度分析（中文）→](cn-ashare)**

Key findings:
- 招商轮船: 12M base target ¥25 (+41%), 40% dividend payout, youngest fleet
- 中远海能: 12M base target ¥32 (+35%), "VLCC attack + LNG defense" dual engine
- Container parallel: PE will compress from 28x → 5-10x (but NOT to 1x like containers)
- A-share VLCC premium: ~2.5-3x per VLCC vs US-listed peers

📎 English version: [07_CN_AShare_VLCC_Report_EN.md](07_CN_AShare_VLCC_Report_EN)

---

## 📁 All Reports

| # | File | Language | Content |
|---|---|---|---|
| 01 | [Full Report EN](01_Full_Report_EN) | English | Initial multi-model DHT vs FRO |
| 02 | [Session Summary EN](02_Session_Summary_EN) | English | Methodology summary |
| 03 | [Full Report CN](03_Full_Report_CN) | 中文 | 初始多模型DHT vs FRO |
| 04 | [Session Summary CN](04_Session_Summary_CN) | 中文 | 方法论摘要 |
| 05 | [Deep Dive EN](05_Deep_Dive_Day1Global_Framework) | English | DHT vs FRO Day1Global framework |
| 06 | [Deep Dive CN](06_Deep_Dive_Day1Global_Framework_CN) | 中文 | DHT vs FRO Day1Global框架 |
| 07 | [A-Share Report EN](07_CN_AShare_VLCC_Report_EN) | English | CMES vs COSCO Energy |
| 08 | [A-Share Report CN](08_CN_AShare_VLCC_Report_CN) | 中文 | 招商轮船 vs 中远海能 |

## 📝 Project Tracking

- [Prompt Log (EN)](Prompt_Log_EN) — All 15 analytical prompts documented
- [Prompt Log (CN)](Prompt_Log_CN) — 所有15条分析提示词记录

---

## 🔬 Methodology

- **5 AI Models**: Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro
- **Framework**: Day1Global tech-earnings-deepdive (16 modules, 6 perspectives)
- **Key Innovations**: Operating leverage / SaaS economics applied to shipping, OPEC production reality check, charter strategy sensitivity modeling
- **Data**: Real-time market data, broker consensus, company filings

---

*Last updated: March 4, 2026 | Created by [liqiqiii](https://github.com/liqiqiii)*
"""

# 3. README.md
readme_content = r"""# VLCC-Analysis-2026

Multi-model AI-powered deep dive into the VLCC (Very Large Crude Carrier) super cycle.

## 🌐 [View on GitHub Pages →](https://liqiqiii.github.io/VLCC-Analysis-2026/)

## Reports

### US-Listed: DHT Holdings vs Frontline (FRO)
- [Deep Dive EN](05_Deep_Dive_Day1Global_Framework.md) | [Deep Dive CN](06_Deep_Dive_Day1Global_Framework_CN.md)
- [Full Report EN](01_Full_Report_EN.md) | [Full Report CN](03_Full_Report_CN.md)

### A-Share: 招商轮船 vs 中远海能
- [A-Share Report EN](07_CN_AShare_VLCC_Report_EN.md) | [A-Share Report CN](08_CN_AShare_VLCC_Report_CN.md)

### Project Tracking
- [Prompt Log EN](Prompt_Log_EN.md) | [Prompt Log CN](Prompt_Log_CN.md)

## Methodology
- 5 AI models: Claude Opus 4.6, Sonnet 4.6, GPT-5.2, GPT-5.1, Gemini 3 Pro
- Day1Global tech-earnings-deepdive framework
- Operating leverage / SaaS economics for shipping
- Container cycle (中远海控 2020-2022) PE compression as valuation reference

## Key Findings

| Stock | Market | 12M Base Target | Upside | Rating |
|---|---|---|---|---|
| DHT Holdings | NYSE | $28 | +44% | STRONG BUY |
| Frontline (FRO) | NYSE | $49.50 | +30% | STRONG BUY |
| 招商轮船 (CMES) | A-Share | ¥25 | +41% | STRONG BUY |
| 中远海能 (COSCO Energy) | A-Share | ¥32 | +35% | STRONG BUY |

*Data as of March 4, 2026. Not investment advice.*
"""

with open(os.path.join(DIR, "index.md"), "w", encoding="utf-8") as f:
    f.write(index_content)
print("Updated index.md (hub landing page)")

with open(os.path.join(DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)
print("Created README.md")

# 4. Update _config.yml
config = """theme: jekyll-theme-cayman
title: "VLCC Super Cycle Analysis 2026"
description: "Multi-Model AI Deep Dive: DHT vs FRO (NYSE) | 招商轮船 vs 中远海能 (A-Share)"
"""
with open(os.path.join(DIR, "_config.yml"), "w", encoding="utf-8") as f:
    f.write(config)
print("Updated _config.yml")

print("\nAll pages ready!")

# Universal Stock Analysis Framework

> **Reusable rules and prompt templates extracted from the VLCC Analysis Project.**
> These are industry-agnostic — apply them to ANY equity deep-dive (shipping, tech, energy, biotech, etc.).
> For VLCC/shipping-specific rules, see the project root `RULES.md`.

---

## Contents

| File | Description |
|---|---|
| [UNIVERSAL_RULES_EN.md](UNIVERSAL_RULES_EN.md) | Common analytical rules (English) |
| [UNIVERSAL_RULES_CN.md](UNIVERSAL_RULES_CN.md) | 通用分析规则（中文） |
| [REUSABLE_PROMPTS_EN.md](REUSABLE_PROMPTS_EN.md) | Prompt templates for any stock analysis (English) |
| [REUSABLE_PROMPTS_CN.md](REUSABLE_PROMPTS_CN.md) | 可复用提示词模板（中文） |

## How to Use

1. **Starting a new analysis**: Copy `UNIVERSAL_RULES_EN.md` into your project, then add industry-specific rules on top.
2. **Running multi-model research**: Pick relevant prompt templates from `REUSABLE_PROMPTS_EN.md`, fill in `[COMPANY]` / `[INDUSTRY]` placeholders, and run across 5 models.
3. **Building a report**: Follow the report structure in Rule 8, applying Day1Global modules (Rule 12).

## Relationship to Project Files

```
VLCC-Analysis-2026/
├── RULES.md                 ← Project-specific (inherits from framework + adds VLCC rules)
├── Prompt_Log_EN/CN.md      ← Project-specific prompt history
├── framework/               ← THIS FOLDER (reusable across ANY project)
│   ├── UNIVERSAL_RULES_EN.md
│   ├── UNIVERSAL_RULES_CN.md
│   ├── REUSABLE_PROMPTS_EN.md
│   └── REUSABLE_PROMPTS_CN.md
└── [report files]
```

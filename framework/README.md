# Universal Stock Analysis Framework

> **Reusable rules and prompt templates extracted from the VLCC Analysis Project.**
> These are industry-agnostic — apply them to ANY equity deep-dive (shipping, tech, energy, biotech, etc.).
> For VLCC/shipping-specific rules, see the project root `RULES.md`.

---

## Contents

| File | Description |
|---|---|
| [UNIVERSAL_RULES_EN.md](UNIVERSAL_RULES_EN.md) | Common analytical rules — any industry (English) |
| [UNIVERSAL_RULES_CN.md](UNIVERSAL_RULES_CN.md) | 通用分析规则（中文） |
| [CYCLICAL_RULES_EN.md](CYCLICAL_RULES_EN.md) | **Cyclical stock rules** — shipping, metals, energy, semis (English) |
| [CYCLICAL_RULES_CN.md](CYCLICAL_RULES_CN.md) | **周期股分析规则**（中文） |
| [REUSABLE_PROMPTS_EN.md](REUSABLE_PROMPTS_EN.md) | Prompt templates for any stock analysis (English) |
| [REUSABLE_PROMPTS_CN.md](REUSABLE_PROMPTS_CN.md) | 可复用提示词模板（中文） |

## Rule Hierarchy

```
UNIVERSAL_RULES (any stock)
  └── CYCLICAL_RULES (shipping, metals, energy, semis)
        └── Project RULES.md (VLCC-specific fleet data, cycle dates)
```

## How to Use

1. **Any stock analysis**: Start with `UNIVERSAL_RULES` + `REUSABLE_PROMPTS`.
2. **Cyclical industries**: Add `CYCLICAL_RULES` on top (two-cycle backtrack, PE compression, exit strategy, etc.).
3. **Specific project**: Add a project-level `RULES.md` with company/industry-specific data.
4. **Running multi-model research**: Pick relevant prompt templates, fill in `[COMPANY]` / `[INDUSTRY]` placeholders, run across 5 models.

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

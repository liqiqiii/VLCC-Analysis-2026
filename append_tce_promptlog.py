"""Append TCE-report prompt-log entries (EN + CN). Run once."""
from pathlib import Path

EN = """

---

## Prompt 33: TCE/WS vs VLCC stock price — the "Average x Duration" thesis
**Date**: June 26, 2026

User: discuss the relationship between TCE/WS and VLCC stock prices. People say
"watching TCE to trade VLCC stock is bad." The key is the AVERAGE TCE level and the
DURATION at that level — prove it with data. Also: how big is the TCE peak vs the
stock-price peak in past cycles? Do both a real backtest and a simulation. (FRO + DHT.)

**What was built**:
- `tce_analysis.py` — real backtest: weekly BDTI (proxy, 2020-2024) + FRO/DHT adjusted
  closes. Correlation of stock LEVEL vs rate across spot/4/13/26/52-wk averaging windows;
  lead/lag; real amplitude episodes; long-cycle TCE-peak vs stock-peak table.
- `tce_simulation.py` — synthetic average x duration model (deterministic, seed=42):
  same-peak/different-duration, peak control, and signal-quality (spot vs sustained).
- `generate_tce_charts.py` — 5 charts.
- `35_TCE_vs_StockPrice_EN.md` + `36_TCE_vs_StockPrice_CN.md`.

**Key findings (data)**:
- **Core proof**: stock-vs-rate R² rises with the averaging window — FRO 0.12 (spot) -> 0.37
  (52-wk avg); DHT 0.20 -> 0.50. The stock prices the sustained average, not spot. Lead/lag
  is contemporaneous (best lag = 0) so the spot tape gives no timing edge. (Honest nuance:
  4-wk *change* R² is higher for spot ~0.21 -> spot wiggles jiggle the stock intra-quarter,
  but not its level.)
- **Amplitude compression (answers the user's direct question)**: TCE peaks 5-10.6x baseline
  while stock peaks only ~1-3x (2008 TCE x10 / FRO x3.0 / DHT x0.9; 2015 x5 / x1.1 / x1.2;
  2020 x10.6 / x1.2 / x1.2; 2026 Hormuz x8 / x1.9 / x1.6).
- **Duration beats peak (real)**: 2020 COVID spike (+45% rate, weeks) -> FRO +11%; 2022-24
  sustained (lower peak, ~18 mo) -> FRO +307%.
- **Simulation**: same $200k peak -> 2-wk spike x1.0 vs 2-yr sustained x1.82; tripling the
  peak ($120k->$350k) at fixed 52-wk duration moves stock only x1.66->x1.83 (+10%);
  sustained-avg signal fwd-26w return median +64% (80% win) vs spot +10% (63% win).

**Verdict**: spot TCE is the noise, the trailing 26-52-wk average + its duration is the
signal. Dovetails with Modeling Stash (momentum + rate-confirmation); 2026 Hormuz (stock
dipped while spot hit $400k ATH) is the canonical "don't trade the tape" case.

**Limitations**: BDTI proxy understates pure-VLCC TD3C amplitude; free BDTI only 2020-24;
long-cycle TCE values are sourced approximations (web-verified, flagged); simulation is
illustrative not predictive; ~4 clean cycles only. Two-Step Research Protocol (draft +
strict peer review) included in the report.

**Files Updated**: tce_analysis.py, tce_simulation.py, generate_tce_charts.py,
35_TCE_vs_StockPrice_EN.md, 36_TCE_vs_StockPrice_CN.md, index.md, charts/tce_*.png,
Prompt_Log_EN.md, Prompt_Log_CN.md
"""

CN = """

---

## Prompt 33: TCE/WS 与 VLCC 股价 — "均值 x 持续时间"论点
**日期**: 2026年6月26日

用户：讨论 TCE/WS 与 VLCC 股价的关系。有人说"盯着 TCE 来交易 VLCC 股票是错的"。关键在于
平均 TCE 水平及其持续时间——用数据证明。另外：过去周期中 TCE 峰值相对股价峰值有多大？
做真实回测 + 模拟。（FRO + DHT。）

**构建内容**：
- `tce_analysis.py` —— 真实回测：周度 BDTI（代理，2020-2024）+ FRO/DHT 复权收盘价。
  股价水平对运价在 即期/4/13/26/52 周平均窗口下的相关性；领先滞后；真实振幅事件；
  长周期 TCE峰值 vs 股价峰值表。
- `tce_simulation.py` —— 合成的均值 x 持续时间模型（确定性，种子=42）：相同峰值/不同
  持续时间、峰值对照、信号质量（即期 vs 持续）。
- `generate_tce_charts.py` —— 5 张图。
- `35_TCE_vs_StockPrice_EN.md` + `36_TCE_vs_StockPrice_CN.md`。

**关键发现（数据）**：
- **核心证据**：股价对运价的 R² 随平均窗口拉长而上升——FRO 0.12（即期）-> 0.37（52周均值）；
  DHT 0.20 -> 0.50。股价为持续均值定价，而非即期。领先滞后为同期（最佳滞后=0），即期盘口
  无择时优势。（诚实说明：4 周变化率 R² 即期更高约 0.21 -> 即期波动让股价季度内抖动，但不
  影响其水平。）
- **振幅压缩（回答用户直接问题）**：TCE 峰值为基线 5-10.6 倍，而股价峰值仅约 1-3 倍
  （2008 TCE x10 / FRO x3.0 / DHT x0.9；2015 x5 / x1.1 / x1.2；2020 x10.6 / x1.2 / x1.2；
  2026 霍尔木兹 x8 / x1.9 / x1.6）。
- **持续时间胜过峰值（真实）**：2020 新冠飙升（运价 +45%，数周）-> FRO +11%；2022-24 持续
  （峰值更低，约 18 个月）-> FRO +307%。
- **模拟**：相同 $20万 峰值 -> 2周飙升 x1.0 vs 2年持续 x1.82；固定 52 周持续时间下峰值翻三倍
  （$12万->$35万）股价仅 x1.66->x1.83（+10%）；持续均值信号前瞻 26 周收益中位数 +64%
  （胜率 80%）vs 即期 +10%（胜率 63%）。

**结论**：即期 TCE 是噪音，滚动 26-52 周均值 + 持续时间才是信号。与 Modeling Stash
（动量 + 运价确认）吻合；2026 霍尔木兹（股价下跌而即期创 $40万 历史新高）是"不要交易盘口"
的典型案例。

**局限**：BDTI 代理低估纯 VLCC TD3C 振幅；免费 BDTI 仅 2020-24；长周期 TCE 值为引用近似值
（经网络核实，已标注）；模拟仅示意非预测；仅约 4 个干净周期。报告含两步研究协议
（草稿 + 严格同行评审）。

**更新文件**: tce_analysis.py, tce_simulation.py, generate_tce_charts.py,
35_TCE_vs_StockPrice_EN.md, 36_TCE_vs_StockPrice_CN.md, index.md, charts/tce_*.png,
Prompt_Log_EN.md, Prompt_Log_CN.md
"""

for fn, txt in [("Prompt_Log_EN.md", EN), ("Prompt_Log_CN.md", CN)]:
    p = Path(fn)
    p.write_text(p.read_text(encoding="utf-8") + txt, encoding="utf-8")
    print("Appended", fn)

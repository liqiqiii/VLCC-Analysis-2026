"""
Generate the bilingual VLCC Cycle-Position report (Jun-2026):
  37_VLCC_Cycle_Position_Jun2026_EN.md  /  38_..._CN.md
Applies the Average x Duration model (reports 35/36) to current FRO/DHT prices.
Targets computed from the repo earnings-sensitivity model for consistency.
Written via Python (RULES Rule 13).
"""
import json
from pathlib import Path

d = json.load(open("dht_fro_april_data.json"))
RT = d["rates"]

def eps(stk, tce):
    s = stk.lower()
    base = RT["70000"][f"{s}_eps"]
    step = RT["70000"][f"{s}_eps"] - RT["65000"][f"{s}_eps"]
    return base + (tce - 70000) / 5000 * step

# ── current snapshot (fetched 2026-06-26) ───────────────────────────────────
ASOF = "June 26, 2026"
PX = {"FRO": 34.94, "DHT": 17.34}
OFF_HI = {"FRO": -14.6, "DHT": -8.2}      # % off 52-wk high
VS_AVG = {"FRO": +34.1, "DHT": +25.5}     # % vs 52-wk avg
HI52 = {"FRO": 40.93, "DHT": 18.89}
LO52 = {"FRO": 16.20, "DHT": 10.22}

# sustained-average PE matrix
PEROWS = [50000, 70000, 90000, 100000, 120000]
def pe(stk, tce):
    return PX[stk] / eps(stk, tce)

# target scenarios (sustained TCE, applied PE)
SCN = [("Conservative", 70000, 7, "rates normalize to ~$70k as spike fully unwinds"),
       ("Base", 95000, 6, "structural ~$90-100k sustained into 2027"),
       ("Bull", 120000, 6.5, "tight supply holds rates ~$120k+ through 2027")]
def target(stk, tce, p):
    return p * eps(stk, tce)

def tgt_row(stk):
    out = []
    for lab, t, p, _ in SCN:
        tg = target(stk, t, p)
        up = (tg / PX[stk] - 1) * 100
        out.append((lab, eps(stk, t), tg, up))
    return out

ft, dt = tgt_row("FRO"), tgt_row("DHT")

def pematrix_rows():
    lines = []
    for t in PEROWS:
        lines.append(f"| ${t:,} | {eps('DHT',t):.2f} | {pe('DHT',t):.1f}x | "
                     f"{eps('FRO',t):.2f} | {pe('FRO',t):.1f}x |")
    return "\n".join(lines)

# ── English report ──────────────────────────────────────────────────────────
EN = f"""---
layout: default
title: "VLCC Cycle Position (Jun 2026) — Are DHT/FRO Cheap or Expensive?"
---

# VLCC Cycle Position — Are DHT / FRO Cheap or Expensive? (June 2026)

**Applying the "Average × Duration" model to current prices**

*As of {ASOF} · Companion to [TCE vs Stock Price (35)](35_TCE_vs_StockPrice_EN)*

> ⚠️ **Disclaimer:** Analytical research, **not investment advice**. Cyclical valuations
> are highly sensitive to the assumed *sustained* rate; do your own due diligence.

---

## TL;DR — Verdict

**Neither DHT nor FRO is expensive. Both are CHEAP-to-FAIR — and the market is pricing them
almost exactly on the *sustained average* TCE (~\\$100k), not the spike.** That is the
[Average × Duration thesis](35_TCE_vs_StockPrice_EN) confirmed in real time: the stocks
ignored the \\$420k Hormuz top *and* are ignoring its collapse, holding at a level
consistent with ~\\$90–100k sustained.

| | DHT | FRO |
|:---|:---|:---|
| Price ({ASOF}) | **\\${PX['DHT']:.2f}** | **\\${PX['FRO']:.2f}** |
| Off 52-wk high | {OFF_HI['DHT']:.1f}% | {OFF_HI['FRO']:.1f}% |
| vs 52-wk avg | +{VS_AVG['DHT']:.0f}% | +{VS_AVG['FRO']:.0f}% |
| PE @ \\$100k sustained | **{pe('DHT',100000):.1f}x** | **{pe('FRO',100000):.1f}x** |
| PE @ \\$70k sustained | {pe('DHT',70000):.1f}x | {pe('FRO',70000):.1f}x |
| Verdict | **Fair-to-cheap, lower beta** | **Cheap-to-fair, higher beta** |

**They become "expensive" only if** the sustainable average is really ~\\$50–60k *and*
duration ends soon — which the post-2027 orderbook argues against.

---

## 1. Current TCE status & duration (the only input that matters)

| | Level | Note |
|:---|:---|:---|
| **Spot TD3C now (late Jun-26)** | **~\\$100k/day** | Down ~76% from the spike |
| Mar-2026 peak | **~\\$420–424k/day** | Hormuz / US–Iran war spike — **transient** |
| 2025 base | ~\\$50–70k/day | Structural ramp through H2-2025 |
| Structural elevation | since ~H2-2025 | Sustained **~9–12 months already** |
| Forward (orderbook) | supportive **through 2027** | ~50 VLCCs ordered Q1-26 but deliver **post-2027**; scrapping accelerating |

**Two layers (per the model):** a **durable structural elevation** (~\\$100k, months-long,
supply-backed into 2027) plus a **transient spike** (the \\$420k that already collapsed).
The model says: **capitalize the first, ignore the second.** The stocks are doing exactly
that.

> *Data note (Rule 4):* sources conflict on the 2025 average — some cite \\$40–70k, others
> \\$100–125k for H2-25. Reality = a structural ramp + the Mar-26 spike. Flagged, not hidden.

---

## 2. Sustained-average valuation matrix (repo earnings model)

What PE are you paying at each *sustained* (not spot) TCE? Prices {ASOF}.

| Sustained TCE | DHT EPS | DHT PE | FRO EPS | FRO PE |
|:---|:--:|:--:|:--:|:--:|
{pematrix_rows()}

**Read (cyclical PE rule — low PE = peak-earnings risk, high PE = trough):**
At ~\\$100k the stocks sit at **PE ~5–6x**; at \\$70k, **~8–9x**. That is **mid-cycle**,
not the PE 2–3x super-peak danger zone and not the PE 13–14x trough-pricing zone. With a
**duration runway into 2027**, PE 5–6x is **cheap-to-fair**.

The stocks at \\${PX['FRO']:.0f}/\\${PX['DHT']:.0f} imply roughly **\\$90–110k sustained** —
i.e. the current normalized spot, **not** the \\$420k spike (which would put FRO above
\\$80). Thesis confirmed: **price = sustained average.**

---

## 3. Target prices (12-month)

Computed from the repo sensitivity model: `target = PE × EPS(sustained TCE)`.

### FRO (\\${PX['FRO']:.2f})
| Scenario | Sustained TCE | PE | EPS | Target | Upside |
|:---|:--:|:--:|:--:|:--:|:--:|
{chr(10).join(f"| {SCN[i][0]} | ${SCN[i][1]:,} | {SCN[i][2]}x | {ft[i][1]:.2f} | **${ft[i][2]:.0f}** | {ft[i][3]:+.0f}% |" for i in range(3))}

### DHT (\\${PX['DHT']:.2f})
| Scenario | Sustained TCE | PE | EPS | Target | Upside |
|:---|:--:|:--:|:--:|:--:|:--:|
{chr(10).join(f"| {SCN[i][0]} | ${SCN[i][1]:,} | {SCN[i][2]}x | {dt[i][1]:.2f} | **${dt[i][2]:.0f}** | {dt[i][3]:+.0f}% |" for i in range(3))}

**Plus the dividend.** At ~\\$100k earnings these are 12–15%+ smoothed-yield names; on the
[Modeling Stash](modeling_stash) "≥8% smoothed yield = buy" rule, both still qualify. Much
of the total return here is **income**, not just price.

**24-month:** the base case holds *only while the structural average holds*. The genuine
risk window is **late-2027–2028**, when the newbuild wave delivers and the average can
roll toward \\$50–70k — that, not the spot tape, is when targets compress.

---

## 4. Sell-signal check (Modeling Stash algo)

| Tier | Rule | Status now |
|:---|:---|:---|
| Tier 1 | PE > 7x + EPS falling 2Q | ❌ Not triggered — PE ~5–6x on sustained, EPS structurally rising |
| Tier 2 | Stock −20% **and** rates −15% from 90d high | 🛡️ Rates *are* down (spike unwind) but stock isn't −20%, and **a spike-unwind ≠ a cycle turn** |

This is the **2026-Hormuz "DO NOT SELL"** case playing out live: a geopolitical rate drop
with the **structural average intact** → hold / accumulate, not sell.

---

## 5. Cycle position (CRule 1)

```
Current cycle position: Mid-to-late, STRUCTURAL up-cycle, post-spike normalization
Evidence: spot ~$100k (vs $420k Mar peak, vs ~$50-70k 2025); elevated ~9-12 months;
          supply relief not until late-2027/2028
Stock vs rate: stock prices the sustained ~$100k average, NOT the spike (didn't chase
          the $420k top, isn't crashing with the unwind) -> textbook average x duration
Predicted next 6-12m: rates range ~$80-130k structural; stocks range-to-higher on
          sustained earnings + heavy dividends
Time to peak/turn: duration risk begins late-2027-2028 (newbuild wave)
Key risk: the AVERAGE rolling over (not the spot spike unwinding)
```

---

## 6. Risk matrix

| Risk | Prob | Impact | Note |
|:---|:--:|:--:|:---|
| Sustained average rolls to \\$50–70k early | Med | High | The real sell trigger; watch the trailing avg, not spot |
| Newbuild wave arrives faster than expected | Low-Med | High | Mostly post-2027 per orderbook |
| Hormuz fully reopens → backlog clears | High | Low-Med | Spot eases further; structural floor remains |
| Demand shock (China/recession) | Low-Med | High | Cuts ton-mile + rates together |
| Balance-sheet / dilution (FRO) | Low | Med | Higher gearing than DHT |

---

## 7. Per-name verdict

- **DHT \\${PX['DHT']:.2f}** — **Fair-to-cheap**, pure-play, lower beta, **{OFF_HI['DHT']:.1f}%** off
  high. PE {pe('DHT',100000):.1f}x@\\$100k / {pe('DHT',70000):.1f}x@\\$70k. The "own the
  average" name; cheapest risk-adjusted exposure, big income.
- **FRO \\${PX['FRO']:.2f}** — **Cheap-to-fair**, higher spot beta, **{OFF_HI['FRO']:.1f}%** off
  high (gave back more of the spike, as expected). PE {pe('FRO',100000):.1f}x@\\$100k /
  {pe('FRO',70000):.1f}x@\\$70k. More upside if the average holds, more downside if it
  normalizes — the leveraged expression of the same thesis.

**Bottom line:** on any reasonable *sustained* average ≥ \\$70k, **neither is expensive**;
both are **cheap-to-fair with income**, and the decisive variable is **duration** — how
long ~\\$100k holds — exactly what reports 35/36 argue you should watch instead of the tape.

{{EXTRA_EN}}

---

*Part of the [VLCC-Analysis-2026](https://github.com/liqiqiii/VLCC-Analysis-2026) project.
Prices via Yahoo Finance ({ASOF}); earnings via repo sensitivity model. Not investment advice.*
"""

# ── Chinese report ──────────────────────────────────────────────────────────
CN = f"""---
layout: default
title: "VLCC 周期定位（2026年6月）— DHT/FRO 便宜还是贵？"
---

# VLCC 周期定位 — DHT / FRO 便宜还是贵？（2026年6月）

**将"均值 × 持续时间"模型应用于当前价格**

*截至 {ASOF} · [TCE 与股价（35）](35_TCE_vs_StockPrice_EN) 的姊妹篇*

> ⚠️ **免责声明：** 分析研究，**非投资建议**。周期股估值对假设的*持续*运价极度敏感；
> 请自行尽职调查。

---

## 摘要 — 结论

**DHT 与 FRO 都不贵。两者均为便宜至合理——且市场几乎正好按*持续平均* TCE（约 \\$10万）
为其定价，而非按飙升。** 这正是[均值 × 持续时间论点](35_TCE_vs_StockPrice_EN)的实时验证：
股价无视了 \\$42万 的霍尔木兹顶部，*也*无视其崩塌，停在与约 \\$9–10万 持续水平一致的位置。

| | DHT | FRO |
|:---|:---|:---|
| 价格（{ASOF}） | **\\${PX['DHT']:.2f}** | **\\${PX['FRO']:.2f}** |
| 距52周高点 | {OFF_HI['DHT']:.1f}% | {OFF_HI['FRO']:.1f}% |
| 相对52周均值 | +{VS_AVG['DHT']:.0f}% | +{VS_AVG['FRO']:.0f}% |
| PE @ \\$10万持续 | **{pe('DHT',100000):.1f}x** | **{pe('FRO',100000):.1f}x** |
| PE @ \\$7万持续 | {pe('DHT',70000):.1f}x | {pe('FRO',70000):.1f}x |
| 结论 | **合理偏便宜，低 beta** | **便宜偏合理，高 beta** |

**只有当**可持续平均确实仅约 \\$5–6万*且*持续时间很快结束时，它们才"贵"——而 2027 年后的
订单簿不支持这一点。

---

## 1. 当前 TCE 状态与持续时间（唯一重要的输入）

| | 水平 | 说明 |
|:---|:---|:---|
| **当前即期 TD3C（6月下旬）** | **约 \\$10万/天** | 较峰值下跌约 76% |
| 2026年3月峰值 | **约 \\$42–42.4万/天** | 霍尔木兹/美伊战争飙升——**短暂** |
| 2025 基线 | 约 \\$5–7万/天 | 下半年结构性爬升 |
| 结构性抬升 | 自约 2025下半年 | 已持续 **约 9–12 个月** |
| 前瞻（订单簿） | **2027 年前**支撑 | Q1-26 约 50 艘 VLCC 订单，但 **2027 后**才交付；拆解加速 |

**两层结构（按模型）：** 一个**持久的结构性抬升**（约 \\$10万，已数月，供给支撑至 2027）
加上一个**短暂飙升**（已崩塌的 \\$42万）。模型说：**资本化第一层，无视第二层。** 股价正是
如此。

> *数据说明（规则4）：* 各来源对 2025 均值存在分歧——部分引用 \\$4–7万，部分引用下半年
> \\$10–12.5万。实际 = 结构性爬升 + 3月飙升。已标注，未隐藏。

---

## 2. 持续平均估值矩阵（仓库盈利模型）

在每个*持续*（非即期）TCE 下你支付多少 PE？价格为 {ASOF}。

| 持续 TCE | DHT EPS | DHT PE | FRO EPS | FRO PE |
|:---|:--:|:--:|:--:|:--:|
{pematrix_rows()}

**解读（周期 PE 规则——低 PE = 峰值盈利风险，高 PE = 谷底）：**
约 \\$10万 时股价处于 **PE 约 5–6x**；\\$7万 时 **约 8–9x**。这是**周期中段**，既非 PE 2–3x
的超级峰值危险区，也非 PE 13–14x 的谷底定价区。在**持续至 2027 的跑道**下，PE 5–6x 属
**便宜偏合理**。

\\${PX['FRO']:.0f}/\\${PX['DHT']:.0f} 的股价隐含约 **\\$9–11万 持续**——即当前归一化即期，
**而非** \\$42万 飙升（那会让 FRO 超过 \\$80）。论点验证：**价格 = 持续均值。**

---

## 3. 目标价（12个月）

由仓库敏感性模型计算：`目标价 = PE × EPS(持续 TCE)`。

### FRO（\\${PX['FRO']:.2f}）
| 情景 | 持续 TCE | PE | EPS | 目标价 | 空间 |
|:---|:--:|:--:|:--:|:--:|:--:|
{chr(10).join(f"| {['保守','基准','乐观'][i]} | ${SCN[i][1]:,} | {SCN[i][2]}x | {ft[i][1]:.2f} | **${ft[i][2]:.0f}** | {ft[i][3]:+.0f}% |" for i in range(3))}

### DHT（\\${PX['DHT']:.2f}）
| 情景 | 持续 TCE | PE | EPS | 目标价 | 空间 |
|:---|:--:|:--:|:--:|:--:|:--:|
{chr(10).join(f"| {['保守','基准','乐观'][i]} | ${SCN[i][1]:,} | {SCN[i][2]}x | {dt[i][1]:.2f} | **${dt[i][2]:.0f}** | {dt[i][3]:+.0f}% |" for i in range(3))}

**外加股息。** 在约 \\$10万 盈利下，这是 12–15%+ 平滑股息率的标的；按
[Modeling Stash](modeling_stash) 的"平滑股息率 ≥ 8% = 买入"规则，两者仍然符合。此处总回报
很大一部分是**收入**，而不仅是价格。

**24个月：** 基准情景*仅在结构性均值维持时*成立。真正的风险窗口是 **2027下半年–2028**，
届时新船交付浪潮可能令均值回落至 \\$5–7万——那才是目标价压缩之时，而非即期盘口。

---

## 4. 卖出信号检查（Modeling Stash 算法）

| 层级 | 规则 | 当前状态 |
|:---|:---|:---|
| 第一层 | PE > 7x + EPS 连续2季下降 | ❌ 未触发——持续口径 PE 约 5–6x，EPS 结构性上升 |
| 第二层 | 股价较90日高点 −20% **且** 运价 −15% | 🛡️ 运价*确实*下跌（飙升回吐）但股价未 −20%，且**飙升回吐 ≠ 周期反转** |

这是 **2026 霍尔木兹"不要卖出"**案例的实时上演：地缘运价下跌但**结构性均值完好** → 持有/
加仓，而非卖出。

---

## 5. 周期定位（CRule 1）

```
当前周期定位：中段偏后、结构性上行周期、飙升后归一化
证据：即期约 $10万（vs 3月峰值 $42万，vs 2025 约 $5-7万）；已抬升约 9-12 个月；
      供给缓解要到 2027下半年/2028
股价 vs 运价：股价按持续约 $10万 均值定价，而非飙升（未追 $42万 顶部，也未随回吐崩塌）
      -> 典型的均值 × 持续时间
未来 6-12 月预测：运价结构性区间约 $8-13万；股价凭持续盈利 + 高股息维持至走高
到峰值/反转时间：持续时间风险始于 2027下半年-2028（新船浪潮）
关键风险：均值回落（而非即期飙升回吐）
```

---

## 6. 风险矩阵

| 风险 | 概率 | 影响 | 说明 |
|:---|:--:|:--:|:---|
| 持续均值提前回落至 \\$5–7万 | 中 | 高 | 真正的卖出触发；盯滚动均值，而非即期 |
| 新船浪潮早于预期 | 低-中 | 高 | 按订单簿多在 2027 后 |
| 霍尔木兹完全重开 → 积压清理 | 高 | 低-中 | 即期进一步走弱；结构性底仍在 |
| 需求冲击（中国/衰退） | 低-中 | 高 | 同时削减吨海里 + 运价 |
| 资产负债表/稀释（FRO） | 低 | 中 | 杠杆高于 DHT |

---

## 7. 个股结论

- **DHT \\${PX['DHT']:.2f}** —— **合理偏便宜**，纯标的，低 beta，距高点 **{OFF_HI['DHT']:.1f}%**。
  PE {pe('DHT',100000):.1f}x@\\$10万 / {pe('DHT',70000):.1f}x@\\$7万。"持有均值"的标的；
  风险调整后最便宜的敞口，高收入。
- **FRO \\${PX['FRO']:.2f}** —— **便宜偏合理**，更高即期 beta，距高点 **{OFF_HI['FRO']:.1f}%**
  （如预期回吐了更多飙升）。PE {pe('FRO',100000):.1f}x@\\$10万 / {pe('FRO',70000):.1f}x@\\$7万。
  均值维持则上行更大，归一化则下行更大——同一论点的杠杆表达。

**底线：** 在任何合理的*持续*均值 ≥ \\$7万 下，**两者都不贵**；均为**便宜偏合理且有收入**，
决定性变量是**持续时间**——约 \\$10万 能维持多久——这正是报告 35/36 主张你应当关注的、
而非盘口。

{{EXTRA_CN}}

---

*隶属于 [VLCC-Analysis-2026](https://github.com/liqiqiii/VLCC-Analysis-2026) 项目。
价格来自 Yahoo Finance（{ASOF}）；盈利来自仓库敏感性模型。非投资建议。*
"""

# Fact-check section (shared with 35/36 §9), tailored heading number
EXTRA_EN = """---

## 8. Fact-Check & Open-Questions Resolution

Verifications behind reports 35/36 (carried here for completeness):

| Item | Earlier claim | **Fact-checked** | Source |
|:---|:---|:---|:---|
| 2008 TD3C peak | ~$300-350k | **~$229-230k/day** ($300k+ = outlier fixtures) | Clarksons/Baltic |
| 2026 Hormuz peak | ~$400k | **~$420-424k/day** | Lloyd's List "VLCC index tops $420K" |
| 2020 COVID peak | $264k | **$264,072/day** confirmed | industry press |
| 2025 average | (open) | **conflicting: $40-70k vs $100-125k H2** | flagged, not resolved |

- **BDTI vs TD3C (resolved):** BDTI is a Baltic basket (VLCC TD1/TD2/TD3C + Suezmax +
  Aframax) that *includes* TD3C, strongly correlated but **dampened** — so it **understates**
  pure-VLCC amplitude. The amplitude compression in 35/36 is therefore **conservative**.
- **Open unknowns:** paywalled full Baltic TD3C $/day weekly history (2005-2026); company
  realised-TCE disclosures to tie rate -> EPS precisely.
"""

EXTRA_CN = """---

## 8. 事实核查与遗留问题解答

支撑报告 35/36 的核查（此处一并列出）：

| 项目 | 早先说法 | **核查后** | 来源 |
|:---|:---|:---|:---|
| 2008 TD3C 峰值 | 约 $30-35万 | **约 $22.9-23万/天**（$30万+ 为异常成交） | Clarksons/Baltic |
| 2026 霍尔木兹峰值 | 约 $40万 | **约 $42-42.4万/天** | Lloyd's List "VLCC 指数突破 $42万" |
| 2020 新冠峰值 | $26.4万 | **$264,072/天** 已确认 | 行业媒体 |
| 2025 均值 | （开放） | **分歧：$4-7万 vs 下半年 $10-12.5万** | 已标注，未解决 |

- **BDTI vs TD3C（已解决）：** BDTI 是 Baltic 一篮子指数（VLCC TD1/TD2/TD3C + Suezmax +
  Aframax），*包含* TD3C，高度相关但被**削弱**——因此**低估**了纯 VLCC 振幅。故 35/36 的
  振幅压缩结论是**保守的**。
- **开放未知：** 付费墙下的完整 Baltic TD3C 美元/天周度历史（2005-2026）；公司实现 TCE
  披露以精确串联运价 -> EPS。
"""

EN = EN.replace("{EXTRA_EN}", EXTRA_EN)
CN = CN.replace("{EXTRA_CN}", EXTRA_CN)

Path("37_VLCC_Cycle_Position_Jun2026_EN.md").write_text(EN, encoding="utf-8")
Path("38_VLCC_Cycle_Position_Jun2026_CN.md").write_text(CN, encoding="utf-8")
print("Wrote 37_EN", len(EN), "/ 38_CN", len(CN))
print("FRO targets:", [(s[0], round(t[2],1), f"{t[3]:+.0f}%") for s, t in zip(SCN, ft)])
print("DHT targets:", [(s[0], round(t[2],1), f"{t[3]:+.0f}%") for s, t in zip(SCN, dt)])

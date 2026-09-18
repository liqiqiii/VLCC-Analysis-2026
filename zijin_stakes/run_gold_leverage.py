# -*- coding: utf-8 -*-
"""
Operating leverage on the gold price for the three live Zijin situations.

This is the repo's Rule 6 (operating-leverage analysis) applied to:
    赤峰黄金 Chifeng   600988.SS / 6693.HK
    招金矿业 Zhaojin   1818.HK
    Allied Gold        AAUC.TO

WHY THIS MATTERS: a gold miner's earnings are levered to (gold price - AISC),
not to the gold price. A high-cost producer has MORE torque in both directions.
This is the same elasticity arithmetic used in the gold_miners report:

    margin/oz      = gold - AISC
    elasticity     = gold / (gold - AISC)      <- % change in margin per % change in gold

So the question "which of these has the most potential" is largely answered by
where each sits on the cost curve -- and the answer is uncomfortable, because
the highest-potential name is also the most fragile.

*** DATA HONESTY ***
Only Allied Gold DISCLOSES AISC. Chifeng and Zhaojin do NOT publish AISC.
Chifeng's figure here is a BROKER ESTIMATE converted by me; Zhaojin's is
UNKNOWN and is modelled as a RANGE, not a point. Every such case is labelled.
Nothing here should be read as a company-disclosed number unless marked DISCLOSED.
"""

import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                          "Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
import numpy as np
import pandas as pd
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")
os.makedirs(DATA, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

GRAMS_PER_OZ = 31.1035

# ------------------------------------------------------------------ inputs
# src: DISCLOSED | BROKER | DERIVED | UNKNOWN  -- carried through to the output
PEERS = {
    "Agnico Eagle":  dict(aisc=1339, src="DISCLOSED"),
    "Newmont":       dict(aisc=1609, src="DISCLOSED"),
    "Barrick":       dict(aisc=1637, src="DISCLOSED"),
}

COMPANIES = {
    "赤峰黄金 Chifeng": dict(
        ticker="600988.SS", ccy="CNY", fx=7.10,
        prod_oz=14.51e3 * 1000 / GRAMS_PER_OZ,       # 14.51 t FY2025 CONFIRMED
        prod_src="DISCLOSED & CONFIRMED (14.51 t FY2025, -4.3% vs 15.16 t in "
                 "2024, per China Gold Association on the 2025 annual report). "
                 "The '16.7 t' figure circulating in one source is WRONG.",
        aisc=1179, aisc_lo=1179, aisc_hi=2190,
        aisc_src="DISCLOSED BUT STALE: US$1,179.1/oz for FY2023 (H-share "
                 "prospectus; vs a US$1,348.5/oz global average that year) -- "
                 "i.e. a GENUINE cost advantage in 2023. *** FY2026 AISC is NOT "
                 "DISCLOSED and is certainly far higher: H1-2026 unit cost of "
                 "sales rose +20.18% to CNY383.44/g on resource tax, royalties "
                 "and the gold-linked levy. Broker range CNY400-500/g approx "
                 "US$1,750-2,190/oz. The band below spans 1,179 -> 2,190. ***",
        shares=1.86e9, shares_src="DERIVED from mcap ~CNY82.6bn / CNY44.26"),
    "招金矿业 Zhaojin": dict(
        ticker="1818.HK", ccy="CNY", fx=7.10,
        prod_oz=19.79e3 * 1000 / GRAMS_PER_OZ,       # mined gold FY2025
        prod_src="DISCLOSED (mined gold 19.79 t FY2025, +7.93%; total 27.23 t). "
                 "*** H1-2026 WARNING: mined gold FELL 21.87% to 7,997 kg and "
                 "total gold fell 12.33%, on tightened domestic mine-safety "
                 "supervision. FY2026 will not repeat FY2025. ***",
        aisc=1700, aisc_lo=1400, aisc_hi=2000,
        aisc_src="UNKNOWN - Zhaojin does NOT disclose AISC. WIDE ASSUMED RANGE "
                 "for sensitivity only. DO NOT QUOTE AS FACT.",
        shares=3.542e9, shares_src="DISCLOSED (share capital RMB3,542,393k)"),
    "Allied Gold": dict(
        ticker="AAUC.TO", ccy="USD", fx=1.0,
        prod_oz=379081,
        prod_src="DISCLOSED (379,081 oz FY2025, beat >375koz guidance). FY2026 "
                 "guidance 485-575 koz incl. Kurmuk -- but first gold only "
                 "~mid/late Sep 2026, so treat as BOTTOM-HALF.",
        aisc=2264, aisc_lo=1700, aisc_hi=2264,
        aisc_src="DISCLOSED: Q1-2026 consolidated AISC US$2,264/oz (worse than "
                 "the Q4-2025 ~US$1,980 previously used). Kurmuk targets "
                 "<US$1,200/oz. The low end of the band (1,700) is MY "
                 "ARITHMETIC for a post-Kurmuk blend, NOT company guidance.",
        shares=139e6, shares_src="DERIVED - LOW CONFIDENCE"),
}

print("=" * 88)
print("OPERATING LEVERAGE TO THE GOLD PRICE — Chifeng / Zhaojin / Allied Gold")
print("=" * 88)

gold = yf.download("GC=F", start="2024-01-01", progress=False,
                   auto_adjust=True)["Close"]
gold = gold.iloc[:, 0] if hasattr(gold, "columns") else gold
SPOT = float(gold.iloc[-1])
print(f"\n  Gold spot (GC=F, {gold.index[-1].date()}): US${SPOT:,.0f}/oz")

# ============================================================ 1) cost curve
print("\n" + "-" * 88)
print("1) WHERE THEY SIT ON THE COST CURVE — and the elasticity that follows")
print("-" * 88)
print(f"  {'name':<22}{'AISC $/oz':>11}{'source':>12}{'margin $/oz':>13}"
      f"{'margin %':>10}{'elasticity':>12}")
rows = []
for n, d in {**{k: dict(v, prod_oz=np.nan, shares=np.nan, ccy="USD", fx=1.0,
                        aisc_lo=v["aisc"], aisc_hi=v["aisc"],
                        prod_src="-", aisc_src=v["src"], shares_src="-")
                for k, v in PEERS.items()},
             **COMPANIES}.items():
    m = SPOT - d["aisc"]
    elas = SPOT / m if m > 0 else np.nan
    tag = "DISCLOSED" if "DISCLOSED" in d["aisc_src"] else (
        "BROKER" if "BROKER" in d["aisc_src"] else "ASSUMED")
    print(f"  {n:<22}{d['aisc']:>11,.0f}{tag:>12}{m:>13,.0f}"
          f"{m/SPOT*100:>9.0f}%{elas:>11.2f}x")
    rows.append(dict(name=n, aisc=d["aisc"], aisc_source=tag,
                     margin_per_oz=round(m), margin_pct=round(m/SPOT*100, 1),
                     elasticity=round(elas, 2)))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "cost_curve.csv"), index=False)
print("\n  elasticity = gold / (gold - AISC): the % change in cash margin for a")
print("  1% change in the gold price. HIGHER COST = HIGHER TORQUE, both ways.")
print("  >> Allied Gold is the highest-cost and therefore the highest-torque of")
print("     the three. That is the bull case AND the bear case, simultaneously.")

# ============================================================ 2) sensitivity
print("\n" + "-" * 88)
print("2) GROSS CASH MARGIN vs GOLD PRICE (production held at FY2025 actuals)")
print("-" * 88)
SCEN = [3000, 3500, 4000, round(SPOT / 100) * 100, 5000, 5500]
SCEN = sorted(set(SCEN))
hdr = "  " + f"{'gold US$/oz':<14}" + "".join(f"{n[:16]:>18}" for n in COMPANIES)
print(hdr)
sens = []
for g in SCEN:
    line = f"  {g:<14,}"
    rec = dict(gold=g)
    for n, d in COMPANIES.items():
        margin_usd = (g - d["aisc"]) * d["prod_oz"] / 1e6
        rec[n] = round(margin_usd, 0)
        mark = " *" if abs(g - SPOT) < 60 else "  "
        line += f"{margin_usd:>16,.0f}{mark}"
    print(line)
    sens.append(rec)
print("\n  (US$m of gross cash margin = (gold - AISC) x FY2025 oz. * = near spot.)")
print("  NOT net profit: excludes tax, D&A, interest, by-products, hedging.")
pd.DataFrame(sens).to_csv(os.path.join(DATA, "gold_sensitivity.csv"), index=False)

# ============================================================ 3) breakevens
print("\n" + "-" * 88)
print("3) THE DOWNSIDE — how far can gold fall before each one stops earning?")
print("-" * 88)
print(f"  {'name':<22}{'AISC':>9}{'cushion vs spot':>18}{'gold -20%':>12}"
      f"{'gold -35%':>12}")
for n, d in COMPANIES.items():
    cush = (SPOT - d["aisc"]) / SPOT * 100
    g20, g35 = SPOT * .80, SPOT * .65
    s20 = "OK" if g20 > d["aisc"] else "UNDERWATER"
    s35 = "OK" if g35 > d["aisc"] else "UNDERWATER"
    print(f"  {n:<22}{d['aisc']:>9,.0f}{cush:>17.0f}%"
          f"{s20:>12}{s35:>12}")
print(f"\n  gold -20% = US${SPOT*.8:,.0f}   gold -35% = US${SPOT*.65:,.0f}")
print("  >> At AISC ~US$1,980 Allied still clears a 35% gold drawdown on paper,")
print("     but it was LOSS-MAKING in FY2024 and FY2025 at the NET level -- AISC")
print("     is not net profit. Cost-curve position understates its fragility.")

# ============================================================ 4) chart
fig, axes = plt.subplots(1, 3, figsize=(17, 5.6))

ax = axes[0]
allc = {**{k: v["aisc"] for k, v in PEERS.items()},
        **{k: v["aisc"] for k, v in COMPANIES.items()}}
order = sorted(allc, key=allc.get)
cols = ["#c0392b" if k in COMPANIES else "#95a5a6" for k in order]
ax.bar(range(len(order)), [allc[k] for k in order], color=cols)
ax.axhline(SPOT, color="#f1c40f", lw=2, ls="--", label=f"gold US${SPOT:,.0f}")
for i, k in enumerate(order):
    ax.text(i, allc[k] + 40, f"{allc[k]:,}", ha="center", fontsize=8)
ax.set_xticks(range(len(order)))
ax.set_xticklabels(order, rotation=30, ha="right", fontsize=8)
ax.set_ylabel("AISC US$/oz")
ax.set_title("A. Cost curve (red = the three)\ngrey peers DISCLOSED; Chifeng=broker, Zhaojin=ASSUMED",
             fontsize=9.5, fontweight="bold")
ax.legend(fontsize=8); ax.grid(axis="y", alpha=.25)

ax = axes[1]
grid = np.linspace(2500, 6000, 120)
for n, d, c in [(k, v, c) for (k, v), c in
                zip(COMPANIES.items(), ["#c0392b", "#2980b9", "#27ae60"])]:
    ax.plot(grid, (grid - d["aisc"]) * d["prod_oz"] / 1e6, color=c, lw=2, label=n)
    ax.fill_between(grid, (grid - d["aisc_hi"]) * d["prod_oz"] / 1e6,
                    (grid - d["aisc_lo"]) * d["prod_oz"] / 1e6, color=c, alpha=.15)
ax.axvline(SPOT, color="#f1c40f", lw=2, ls="--")
ax.text(SPOT, ax.get_ylim()[1], f" spot ${SPOT:,.0f}", fontsize=8,
        va="top", color="#b7950b", fontweight="bold")
ax.axhline(0, color="k", lw=.9)
ax.set_xlabel("gold US$/oz"); ax.set_ylabel("gross cash margin US$m")
ax.set_title("B. Margin vs gold (band = AISC uncertainty)\nFY2025 production held constant",
             fontsize=9.5, fontweight="bold")
ax.legend(fontsize=8); ax.grid(alpha=.25)

ax = axes[2]
names = list(COMPANIES)
elas = [SPOT / (SPOT - COMPANIES[n]["aisc"]) for n in names]
ax.bar(names, elas, color=["#c0392b", "#2980b9", "#27ae60"])
for i, v in enumerate(elas):
    ax.text(i, v + .02, f"{v:.2f}x", ha="center", fontsize=9, fontweight="bold")
ax.set_ylabel("margin elasticity to gold (x)")
ax.set_title("C. Torque: % margin change per 1% gold move\nhigher = more upside AND more downside",
             fontsize=9.5, fontweight="bold")
ax.tick_params(axis="x", labelsize=8)
ax.grid(axis="y", alpha=.25)

fig.suptitle("Operating leverage to gold — the three live Zijin situations\n"
             "AISC: Allied DISCLOSED · Chifeng BROKER ESTIMATE · Zhaojin ASSUMED "
             "RANGE (not disclosed). Treat accordingly.",
             fontsize=11.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .90])
p = os.path.join(CHARTS, "gold_leverage.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")

# ============================================================ 5) provenance
print("\n" + "-" * 88)
print("5) DATA PROVENANCE — read before quoting anything above")
print("-" * 88)
prov = []
for n, d in COMPANIES.items():
    print(f"\n  {n} ({d['ticker']})")
    for lbl, key in [("production", "prod_src"), ("AISC", "aisc_src"),
                     ("share count", "shares_src")]:
        print(f"    {lbl:<12}: {d[key]}")
        prov.append(dict(company=n, field=lbl, provenance=d[key]))
pd.DataFrame(prov).to_csv(os.path.join(DATA, "provenance.csv"), index=False)
print("\nDone.")

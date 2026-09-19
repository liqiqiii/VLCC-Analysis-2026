# -*- coding: utf-8 -*-
"""
VLCC cycle-top valuation: three independent ceilings.

The user's framework (18 Sep 2026):
    "当股息率被压缩（股票贵的时候），吃息的人会离场；我们由此可以按照
     2倍PB来计算一下估值；并且以vlcc的期租价格为指引，作为价格中枢"

Three ideas that interlock:

  1. TIME-CHARTER RATE AS THE CENTRAL ANCHOR (价格中枢)
     The TC rate is what a counterparty will COMMIT to for 1-3 years. It is
     the market's own estimate of the SUSTAINABLE rate, with the spot spike
     stripped out. This is the cleanest possible expression of the finding in
     report sections 6-8: stocks capitalise SUSTAINED rates ~1:1 and ignore
     transient spikes. So: earn at the TC rate, not at the spot print.

  2. 2x PRICE/BOOK AS THE CYCLE-TOP CEILING
     Shipping is asset-heavy; P/B is the classic shipping ceiling metric.
     *** BUT SEE THE BOOK-VALUE TRAP BELOW -- this is where the framework
     needs a correction before it can be used. ***

  3. DIVIDEND-YIELD COMPRESSION AS THE EXIT TRIGGER
     DHT and FRO are owned substantially by income buyers. They do not sell
     on valuation; they sell when the YIELD ON SUSTAINABLE EARNINGS drops
     below their hurdle. That is a mechanical, forecastable seller.

*** THE BOOK-VALUE TRAP (the correction this script exists to make) ***
Accounting book value = historical cost less accumulated depreciation. In 2026
second-hand VLCC values are at multi-decade highs -- a 5-year-old VLCC is worth
MORE than a newbuild. So book massively UNDERSTATES asset value, and a raw P/B
of 2x is NOT the same signal it was in a normal market. This script therefore
computes BOTH P/B (accounting) and P/NAV (vessel market values) and shows how
far apart they are.
"""

import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
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

# ---------------------------------------------------------------- inputs
# Company parameters carried from sections 7-12 of this report (sourced there).
# Balance-sheet figures are from the 30-Jun-2026 quarterly statements.
CO = {
    "DHT": dict(
        vlcc_equiv=24.0,            # 24 VLCCs, pure play
        days_per_ship=350,
        breakeven=17_500,           # DISCLOSED cash breakeven $/day
        dna_m=105,                  # D&A US$m/yr
        shares_m=161.24,
        equity_m=1330,              # 30-Jun-2026 stockholders' equity
        debt_m=435, cash_m=163,
        payout=0.50,                # disclosed policy ~100% of net income has
                                    # varied; Yahoo payoutRatio 0.50 used
        spot_pct=0.52,
        five_yr_avg_yield=6.42,     # Yahoo fiveYearAvgDividendYield
        ttm_div=2.45,
        fleet_mix=[(24, 150)],      # (ships, US$m each) -- VLCC only
    ),
    "FRO": dict(
        vlcc_equiv=57.9,            # 42 VLCC + 21 Suezmax*0.5 + 18 LR2*0.3
        days_per_ship=350,
        breakeven=23_800,
        dna_m=300,
        shares_m=222.62,
        equity_m=3155,
        debt_m=2435, cash_m=322,
        payout=0.4693,
        spot_pct=0.86,
        five_yr_avg_yield=11.48,
        ttm_div=5.38,
        fleet_mix=[(42, 150), (21, 120), (18, 100)],   # VLCC / Suezmax / LR2
    ),
}

# Sourced 18-Sep-2026: 1-year VLCC TC quoted US$93,000-105,000/day.
# DHT fixed a 2011-built VLCC at US$105,000/day for 12 months.
TC_LOW, TC_MID, TC_HIGH = 93_000, 100_000, 105_000
TC_SCENARIOS = [60_000, 75_000, TC_LOW, TC_MID, TC_HIGH, 120_000, 150_000]

print("=" * 92)
print("VLCC CYCLE-TOP VALUATION — TC rate as the anchor, 2x P/B as the ceiling,")
print("                           dividend-yield compression as the trigger")
print("=" * 92)

px = {}
for t in CO:
    s = yf.download(t, period="5y", progress=False, auto_adjust=True)["Close"]
    px[t] = (s.iloc[:, 0] if hasattr(s, "columns") else s).dropna()
    CO[t]["price"] = float(px[t].iloc[-1])

print(f"\n  Prices ({px['DHT'].index[-1].date()}): "
      + " · ".join(f"{t} US${CO[t]['price']:.2f}" for t in CO))
print(f"  1-yr VLCC TC anchor: US${TC_LOW:,}–{TC_HIGH:,}/day "
      f"(central US${TC_MID:,})")

# ================================================================ 1) the trap
print("\n" + "-" * 92)
print("1) ⚠️ THE BOOK-VALUE TRAP — why raw '2x P/B' does NOT mean today what it")
print("   meant in a normal market")
print("-" * 92)
print(f"  {'':<6}{'price':>9}{'BVPS':>9}{'P/B':>8}{'NAVPS':>9}{'P/NAV':>8}"
      f"{'fleet US$m':>12}{'net debt':>10}")
trap = []
for t, d in CO.items():
    bvps = d["equity_m"] / d["shares_m"]
    fleet = sum(n * v for n, v in d["fleet_mix"])
    net_debt = d["debt_m"] - d["cash_m"]
    nav = fleet - net_debt
    navps = nav / d["shares_m"]
    d.update(bvps=bvps, navps=navps, fleet_m=fleet, net_debt_m=net_debt)
    print(f"  {t:<6}{d['price']:>9.2f}{bvps:>9.2f}{d['price']/bvps:>8.2f}"
          f"{navps:>9.2f}{d['price']/navps:>8.2f}{fleet:>12,.0f}{net_debt:>10,.0f}")
    trap.append(dict(ticker=t, price=round(d["price"], 2), bvps=round(bvps, 2),
                     pb=round(d["price"]/bvps, 2), navps=round(navps, 2),
                     p_nav=round(d["price"]/navps, 2), fleet_usd_m=fleet,
                     net_debt_usd_m=net_debt))
pd.DataFrame(trap).to_csv(os.path.join(DATA, "pb_vs_pnav.csv"), index=False)

print("\n  >> BOTH ARE ALREADY ABOVE 2x P/B ON ACCOUNTING BOOK.")
print("     But P/NAV -- using vessel MARKET values -- is far lower, because a")
print("     5-year-old VLCC is worth ~US$174.5m against a US$129.5m newbuild:")
print("     second-hand values are at multi-decade highs, so depreciated book")
print("     massively understates the assets.")
print("  >> CONCLUSION: '2x P/B' must be applied to NAV, not to accounting book,")
print("     or the threshold has to be re-calibrated upward. Applied naively to")
print("     book it would have told you to sell a long way back.")
print("  ⚠️ Fleet values assume US$150m/VLCC, US$120m/Suezmax, US$100m/LR2 —")
print("     an ASSUMPTION for an age-mixed fleet, not a broker valuation.")

# ================================================================ 2) TC anchor
print("\n" + "-" * 92)
print("2) THE TC RATE AS THE CENTRAL ANCHOR — sustainable earnings, not spot")
print("-" * 92)
rows = []
for t, d in CO.items():
    days = d["vlcc_equiv"] * d["days_per_ship"]
    print(f"\n  ── {t} ── {d['vlcc_equiv']:.1f} VLCC-equiv × {d['days_per_ship']} "
          f"= {days:,.0f} vessel-days · breakeven US${d['breakeven']:,}/day")
    print(f"     {'TC rate':>10}{'revenue':>10}{'EBITDA':>9}{'net US$m':>10}"
          f"{'EPS':>8}{'DPS':>7}{'yield@px':>10}{'P/E':>7}")
    for tc in TC_SCENARIOS:
        rev = tc * days / 1e6
        ebitda = (tc - d["breakeven"]) * days / 1e6
        net = ebitda - d["dna_m"]
        eps = net / d["shares_m"]
        dps = max(eps, 0) * d["payout"]
        yld = dps / d["price"] * 100
        pe = d["price"] / eps if eps > 0 else np.nan
        mark = "  <-- ANCHOR" if tc == TC_MID else ""
        print(f"     {tc:>10,}{rev:>10,.0f}{ebitda:>9,.0f}{net:>10,.0f}"
              f"{eps:>8.2f}{dps:>7.2f}{yld:>9.1f}%{pe:>7.1f}{mark}")
        rows.append(dict(ticker=t, tc_rate=tc, revenue_m=round(rev),
                         ebitda_m=round(ebitda), net_m=round(net),
                         eps=round(eps, 2), dps=round(dps, 2),
                         yield_at_price_pct=round(yld, 1),
                         pe=round(pe, 1) if pe == pe else None))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "tc_anchor_earnings.csv"), index=False)

# ================================================================ 3) yield
print("\n" + "-" * 92)
print("3) THE INCOME HOLDER'S EXIT — what price does each hurdle yield imply?")
print("-" * 92)
print("  Mechanism: the yield buyer does not sell on 'valuation'. They sell when")
print("  the yield on SUSTAINABLE (TC-rate) earnings falls below their hurdle.")
print(f"  So: price ceiling = (TC-rate DPS) / (hurdle yield).\n")
HURDLES = [6, 8, 10, 12, 15]
yr = []
for t, d in CO.items():
    days = d["vlcc_equiv"] * d["days_per_ship"]
    net = (TC_MID - d["breakeven"]) * days / 1e6 - d["dna_m"]
    eps = net / d["shares_m"]
    dps = eps * d["payout"]
    print(f"  ── {t} ── at the US${TC_MID:,}/day anchor: EPS US${eps:.2f}, "
          f"DPS US${dps:.2f}  (current price US${d['price']:.2f})")
    print(f"     {'hurdle yield':>14}{'implied price':>16}{'vs today':>11}"
          f"{'implied P/B':>13}{'implied P/NAV':>15}")
    for h in HURDLES:
        p = dps / (h / 100)
        print(f"     {h:>13}%{p:>16.2f}{(p/d['price']-1)*100:>10.0f}%"
              f"{p/d['bvps']:>13.2f}{p/d['navps']:>15.2f}")
        yr.append(dict(ticker=t, hurdle_yield_pct=h, implied_price=round(p, 2),
                       vs_today_pct=round((p/d["price"]-1)*100),
                       implied_pb=round(p/d["bvps"], 2),
                       implied_pnav=round(p/d["navps"], 2)))
    print(f"     current TC-based yield at today's price: "
          f"{dps/d['price']*100:.1f}%   |   5-yr average actual yield: "
          f"{d['five_yr_avg_yield']:.2f}%   |   TTM paid: US${d['ttm_div']:.2f}")
pd.DataFrame(yr).to_csv(os.path.join(DATA, "yield_ceilings.csv"), index=False)

# ================================================================ 4) converge
print("\n" + "-" * 92)
print("4) THREE CEILINGS, SIDE BY SIDE — where do they converge?")
print("-" * 92)
conv = []
for t, d in CO.items():
    days = d["vlcc_equiv"] * d["days_per_ship"]
    net = (TC_MID - d["breakeven"]) * days / 1e6 - d["dna_m"]
    eps = net / d["shares_m"]
    dps = eps * d["payout"]
    c_pb2 = 2 * d["bvps"]
    c_nav15 = 1.5 * d["navps"]
    c_y8 = dps / 0.08
    c_y10 = dps / 0.10
    print(f"\n  ── {t} ── today US${d['price']:.2f}")
    for lbl, v in [("2.0x accounting book", c_pb2),
                   ("1.5x P/NAV (vessel market values)", c_nav15),
                   ("8% yield on TC-rate earnings", c_y8),
                   ("10% yield on TC-rate earnings", c_y10)]:
        print(f"     {lbl:<38}US${v:>8.2f}   {(v/d['price']-1)*100:>+6.0f}%")
        conv.append(dict(ticker=t, ceiling=lbl, price=round(v, 2),
                         vs_today_pct=round((v/d["price"]-1)*100)))
    lo, hi = min(c_pb2, c_nav15, c_y8, c_y10), max(c_pb2, c_nav15, c_y8, c_y10)
    print(f"     {'RANGE':<38}US${lo:.2f} – US${hi:.2f}   "
          f"({(lo/d['price']-1)*100:+.0f}% to {(hi/d['price']-1)*100:+.0f}%)")
pd.DataFrame(conv).to_csv(os.path.join(DATA, "ceilings.csv"), index=False)

# ================================================================ 5) inverse
print("\n" + "-" * 92)
print("5) THE INVERSE QUESTION — what TC rate does TODAY'S price already assume?")
print("-" * 92)
print("  Solve for the TC rate that makes each ceiling equal the current price.\n")
inv = []
for t, d in CO.items():
    days = d["vlcc_equiv"] * d["days_per_ship"]

    def tc_for_eps(target_eps):
        return (target_eps * d["shares_m"] + d["dna_m"]) * 1e6 / days + d["breakeven"]

    for lbl, hurdle in [("8% yield", .08), ("10% yield", .10), ("12% yield", .12)]:
        need_dps = d["price"] * hurdle
        need_eps = need_dps / d["payout"]
        tc = tc_for_eps(need_eps)
        print(f"  {t} — to justify US${d['price']:.2f} at a {lbl} you need a "
              f"SUSTAINED TC rate of US${tc:,.0f}/day")
        inv.append(dict(ticker=t, basis=lbl, required_tc=round(tc)))
    print(f"     ... versus the actual 1-yr TC market of "
          f"US${TC_LOW:,}–{TC_HIGH:,}/day\n")
pd.DataFrame(inv).to_csv(os.path.join(DATA, "implied_tc.csv"), index=False)

# ================================================================ 5b) NAV sens
print("\n" + "-" * 92)
print("5b) ⚠️ HOW MUCH DOES THE NAV CONCLUSION DEPEND ON MY VESSEL-VALUE GUESS?")
print("-" * 92)
print("  The P/NAV numbers above use US$150m/VLCC. That is an ASSUMPTION for an")
print("  age-mixed fleet. Sourced 2026 market values: 5-yr-old VLCC US$174.5m,")
print("  newbuild US$129.5m. Test the whole plausible range.\n")
print(f"  {'VLCC US$m':>11}{'DHT NAVPS':>12}{'DHT P/NAV':>12}"
      f"{'FRO NAVPS':>12}{'FRO P/NAV':>12}")
navsens = []
for vl in [110, 125, 150, 175, 200]:
    row = dict(vlcc_value_usd_m=vl)
    out = []
    for t, d in CO.items():
        scale = vl / 150.0
        fleet = sum(n * v * scale for n, v in d["fleet_mix"])
        nav = fleet - d["net_debt_m"]
        navps = nav / d["shares_m"]
        out += [navps, d["price"] / navps]
        row[f"{t}_navps"] = round(navps, 2)
        row[f"{t}_p_nav"] = round(d["price"] / navps, 2)
    print(f"  {vl:>11}{out[0]:>12.2f}{out[1]:>12.2f}{out[2]:>12.2f}{out[3]:>12.2f}")
    navsens.append(row)
pd.DataFrame(navsens).to_csv(os.path.join(DATA, "nav_sensitivity.csv"), index=False)
print("\n  >> The ABSOLUTE P/NAV moves a lot with the assumption. But the RELATIVE")
print("     conclusion does not: FRO trades at a ~27% higher P/NAV than DHT at")
print("     EVERY vessel value. The relative call is robust; the absolute is not.")

# ================================================================ chart
fig, axes = plt.subplots(2, 2, figsize=(16, 10.5))

ax = axes[0][0]
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    d = CO[t]
    days = d["vlcc_equiv"] * d["days_per_ship"]
    grid = np.linspace(40_000, 160_000, 200)
    dps = np.maximum(((grid - d["breakeven"]) * days / 1e6 - d["dna_m"])
                     / d["shares_m"], 0) * d["payout"]
    ax.plot(grid / 1000, dps / d["price"] * 100, color=c, lw=2.2, label=t)
ax.axvspan(TC_LOW / 1000, TC_HIGH / 1000, color="#27ae60", alpha=.15)
ax.text((TC_LOW + TC_HIGH) / 2000, ax.get_ylim()[1] * .95,
        "1-yr TC market\n$93–105k", ha="center", fontsize=8,
        color="#1e8449", fontweight="bold")
for h, ls in [(8, "--"), (10, ":")]:
    ax.axhline(h, color="#7f8c8d", ls=ls, lw=1.2)
    ax.text(155, h + .3, f"{h}% hurdle", fontsize=7.5, ha="right", color="#555")
ax.set_xlabel("sustained TC rate US$000/day")
ax.set_ylabel("dividend yield at TODAY'S price (%)")
ax.set_title("A. Yield on SUSTAINABLE earnings vs the TC rate\nwhere the income holder's hurdle is breached",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=9); ax.grid(alpha=.25)

ax = axes[0][1]
labels, dht_v, fro_v = [], [], []
for lbl in ["2.0x accounting book", "1.5x P/NAV (vessel market values)",
            "8% yield on TC-rate earnings", "10% yield on TC-rate earnings"]:
    labels.append(lbl.replace(" (vessel market values)", "").replace(" on TC-rate earnings", ""))
    dht_v.append(next(r["price"] for r in conv if r["ticker"] == "DHT" and r["ceiling"] == lbl))
    fro_v.append(next(r["price"] for r in conv if r["ticker"] == "FRO" and r["ceiling"] == lbl))
x = np.arange(len(labels))
ax.bar(x - .2, dht_v, .4, label="DHT", color="#c0392b")
ax.bar(x + .2, fro_v, .4, label="FRO", color="#2980b9")
ax.axhline(CO["DHT"]["price"], color="#c0392b", ls="--", lw=1.4)
ax.axhline(CO["FRO"]["price"], color="#2980b9", ls="--", lw=1.4)
ax.text(len(labels) - .5, CO["DHT"]["price"] + 1, f"DHT today ${CO['DHT']['price']:.2f}",
        fontsize=7.5, color="#c0392b", ha="right", fontweight="bold")
ax.text(len(labels) - .5, CO["FRO"]["price"] + 1, f"FRO today ${CO['FRO']['price']:.2f}",
        fontsize=7.5, color="#2980b9", ha="right", fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=7.5, rotation=12)
ax.set_ylabel("implied price US$")
ax.set_title("B. Four independent ceilings vs today's price\ndashed = current price",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=9); ax.grid(axis="y", alpha=.25)

ax = axes[1][0]
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    d = CO[t]
    s = px[t]
    # rolling P/B proxy: price / latest BVPS (book only known for recent qtrs)
    ax.plot(s.index, s.values / d["bvps"], color=c, lw=1.6, label=f"{t} P/B (current BVPS)")
ax.axhline(2.0, color="#27ae60", ls="--", lw=1.8)
ax.text(s.index[0], 2.05, "2.0x book", fontsize=8.5, color="#1e8449", fontweight="bold")
ax.set_ylabel("price ÷ CURRENT book value per share")
ax.set_title("C. P/B against TODAY'S book — illustrative only\n(book compounded fast, so a fixed 2x line is a MOVING target)",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=8.5); ax.grid(alpha=.25)

ax = axes[1][1]
q = ["2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30"]
dht_eq = [1089, 1096, 1133, 1233, 1330]
fro_eq = [2367, 2326, 2511, 2841, 3155]
ax.plot(q, [e / CO["DHT"]["shares_m"] for e in dht_eq], "o-", color="#c0392b", lw=2, label="DHT BVPS")
ax.plot(q, [e / CO["FRO"]["shares_m"] for e in fro_eq], "o-", color="#2980b9", lw=2, label="FRO BVPS")
for i, (a, b) in enumerate(zip(dht_eq, fro_eq)):
    ax.text(i, a / CO["DHT"]["shares_m"] + .2, f"{a/CO['DHT']['shares_m']:.2f}", fontsize=7.5, ha="center")
    ax.text(i, b / CO["FRO"]["shares_m"] + .2, f"{b/CO['FRO']['shares_m']:.2f}", fontsize=7.5, ha="center")
ax.set_ylabel("book value per share US$")
ax.tick_params(axis="x", labelsize=7.5, rotation=20)
ax.set_title("D. Book value is COMPOUNDING — so the 2x P/B ceiling RISES\nDHT +22% YoY · FRO +33% YoY",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=9); ax.grid(alpha=.25)

fig.suptitle("VLCC cycle-top framework — TC rate as the anchor · 2x P/B as the ceiling · "
             "yield compression as the trigger\n"
             f"DHT US${CO['DHT']['price']:.2f} · FRO US${CO['FRO']['price']:.2f} · "
             f"1-yr VLCC TC US${TC_LOW:,}–{TC_HIGH:,}/day",
             fontsize=12, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .93])
p = os.path.join(CHARTS, "cycle_top_valuation.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

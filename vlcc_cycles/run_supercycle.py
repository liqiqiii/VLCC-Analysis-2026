# -*- coding: utf-8 -*-
"""
The 2005-08 super-cycle: P/B and P/NAV, from the original SEC 20-F filings.

The user, 20 Sep 2026: "跟05-08年的超级大周期比呢？"

Sections 14 and 15 could not answer this because the balance-sheet source
started in 2011. This file goes to the primary documents instead:

    DHT 20-F for FY2008  https://www.sec.gov/Archives/edgar/data/1331284/
                         000095015709000131/form20f.htm
    FRO 20-F for FY2008  https://www.sec.gov/Archives/edgar/data/913290/
                         000091957409009523/d990591_20-f.htm

Both contain a five-year "Selected Financial Data" table, so FY2004-FY2008
balance-sheet figures come straight from the filings.

*** TWO TRAPS THAT HAD TO BE HANDLED ***

1. REVERSE SPLITS. DHT did 1-for-12 on 17-Jul-2012; FRO did 1-for-5 on
   03-Feb-2016. Yahoo back-adjusts prices for splits, so its 2007 "close" is
   NOT what anyone paid. Every price below is converted back to the ACTUAL
   traded price by multiplying by the split factor, so that it matches the
   book value per share computed on the share count of the day.

2. THESE ARE NOT THE SAME COMPANIES. In 2005-08:
     - DHT owned NINE vessels (3 VLCC, 2 Suezmax, 4 Aframax) on long-term
       time charters to OSG. It was a high-payout, high-leverage charter
       vehicle, not a spot VLCC play. Today it is 24 VLCCs, ~52% spot.
     - FRO owned 28 VLCCs + 15 Suezmaxes + 8 Suezmax OBOs, AND chartered IN
       a further 12 VLCCs and 14 Suezmaxes it did not own, AND had 18
       newbuildings on order. Chartered-in tonnage earns money but is not an
       asset, so it inflates earnings relative to NAV.
   The multiples are therefore comparable as MULTIPLES, but the businesses
   underneath them are not. This is stated, not buried.
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

SPLIT = {"DHT": 12.0, "FRO": 5.0}      # divide Yahoo's adjusted price by this

# ---- straight from the FY2008 20-F five-year tables (US$ thousands) --------
SUPER = {
    "DHT": {
        "2006-12-31": dict(assets=349_040, cur_liab=9_625, lt_liab=236_000,
                           cash=17_680, shares=30_007_000, vessels_net=322_577),
        "2007-12-31": dict(assets=422_208, cur_liab=96_633, lt_liab=253_700,
                           cash=10_365, shares=30_024_407, vessels_net=398_005),
        "2008-12-31": dict(assets=532_496, cur_liab=40_673, lt_liab=344_000,
                           cash=59_020, shares=36_055_422, vessels_net=462_387),
    },
    "FRO": {
        # equity is REPORTED directly in FRO's table, so it is used as given
        "2006-12-31": dict(assets=4_589_937, equity=668_560, shares=74_825_169),
        "2007-12-31": dict(assets=3_762_091, equity=445_969, shares=74_825_169),
        "2008-12-31": dict(assets=4_027_728, equity=702_217, shares=77_858_502),
    },
}

# Owned fleet. DHT: "three VLCCs, two Suezmax and four Aframax" (FY2008 20-F).
# FRO at 31-Dec-2008: "28 VLCCs, 15 Suezmax tankers, eight Suezmax OBOs"
# PLUS 12 VLCCs and 14 Suezmaxes CHARTERED IN (excluded - not assets)
# and 18 newbuildings on order (excluded - not yet delivered).
FLEET_SUPER = {
    "DHT": {"2007-12-31": dict(vlcc=3, suez=2, afra=4),
            "2008-12-31": dict(vlcc=3, suez=2, afra=4)},
    "FRO": {"2007-12-31": dict(vlcc=28, suez=23),      # ⚠️ 2007 assumed = 2008
            "2008-12-31": dict(vlcc=28, suez=23)},
}

# 5-year-old second-hand values, US$m (broker/press; see report).
VALS = {
    "2007-12-31": dict(vlcc=(150, 165), suez=(95, 110), afra=(65, 78)),
    "2008-12-31": dict(vlcc=(80, 95), suez=(55, 68), afra=(40, 50)),
    "2026-09-18": dict(vlcc=(170, 179), suez=(115, 125), afra=(95, 105)),
}
AGE_SUPER = {"DHT": 8, "FRO": 7}       # estimated average fleet age, years
AGE_DECAY = 0.055

print("=" * 96)
print("THE 2005-08 SUPER-CYCLE — P/B and P/NAV from the original 20-F filings")
print("=" * 96)

PX = {}
for t in ["DHT", "FRO"]:
    s = yf.download(t, start="2005-01-01", progress=False, auto_adjust=False)["Close"]
    PX[t] = (s.iloc[:, 0] if hasattr(s, "columns") else s).dropna()

print("\n" + "-" * 96)
print("1) ⚠️ THE SPLIT TRAP — Yahoo's 2007 price is NOT what anyone paid")
print("-" * 96)
print(f"  {'':<6}{'date':<13}{'Yahoo close':>13}{'reverse split':>15}{'ACTUAL price':>14}")
for t in ["DHT", "FRO"]:
    for d in ["2007-12-31", "2008-06-30", "2008-12-31"]:
        adj = float(PX[t].loc[:d].iloc[-1])
        print(f"  {t:<6}{d:<13}{adj:>13.2f}{f'1-for-{SPLIT[t]:.0f}':>15}"
              f"{adj/SPLIT[t]:>14.2f}")
print("\n  DHT 1-for-12 on 17-Jul-2012 · FRO 1-for-5 on 03-Feb-2016.")
print("  Using the unconverted figure would overstate historical P/B by 12x / 5x.")

# ================================================================ compute
print("\n" + "-" * 96)
print("2) THE SUPER-CYCLE MULTIPLES")
print("-" * 96)
rows = []
for t in ["DHT", "FRO"]:
    print(f"\n  ── {t} ──")
    print(f"  {'date':<13}{'price':>9}{'equity$m':>10}{'shares m':>10}{'BVPS':>8}"
          f"{'P/B':>7}{'ships':>7}{'fleet$m':>9}{'netdebt':>9}{'NAVPS':>8}{'P/NAV':>8}")
    for d, f in SUPER[t].items():
        if d not in FLEET_SUPER[t]:
            continue
        shares = f["shares"] / 1e6
        eq = (f.get("equity") or
              f["assets"] - f["cur_liab"] - f["lt_liab"]) / 1e3     # US$m
        bvps = eq / shares
        price = float(PX[t].loc[:d].iloc[-1]) / SPLIT[t]
        pb = price / bvps

        fl = FLEET_SUPER[t][d]
        v = VALS[d]
        hair = max(0.25, 1 - AGE_DECAY * max(0, AGE_SUPER[t] - 5))
        lo = sum(fl.get(k, 0) * v[k][0] for k in ("vlcc", "suez", "afra")) * hair
        hi = sum(fl.get(k, 0) * v[k][1] for k in ("vlcc", "suez", "afra")) * hair
        # net debt: DHT from the components; FRO from assets - equity as a proxy
        if "cur_liab" in f:
            nd = (f["cur_liab"] + f["lt_liab"] - f["cash"]) / 1e3
        else:
            nd = (f["assets"] - f["equity"]) / 1e3        # total liabilities proxy
        navps_lo, navps_hi = (lo - nd) / shares, (hi - nd) / shares
        navps = (navps_lo + navps_hi) / 2
        pnav = price / navps if navps > 0 else np.nan
        print(f"  {d:<13}{price:>9.2f}{eq:>10,.0f}{shares:>10.1f}{bvps:>8.2f}"
              f"{pb:>7.2f}{sum(fl.values()):>7}{(lo+hi)/2:>9,.0f}{nd:>9,.0f}"
              f"{navps:>8.2f}{pnav:>8.2f}")
        rows.append(dict(ticker=t, date=d, price=round(price, 2),
                         equity_usd_m=round(eq), shares_m=round(shares, 1),
                         bvps=round(bvps, 2), pb=round(pb, 2),
                         ships=sum(fl.values()), fleet_usd_m=round((lo + hi) / 2),
                         net_debt_usd_m=round(nd), navps=round(navps, 2),
                         pnav=round(pnav, 2) if pnav == pnav else None))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA, "supercycle_0508.csv"), index=False)

# ================================================================ vs today
print("\n" + "=" * 96)
print("3) ⭐ THE SUPER-CYCLE vs TODAY")
print("=" * 96)
TODAY = {"DHT": dict(price=23.27, bvps=8.26, pb=2.82, pnav=1.45),
         "FRO": dict(price=51.42, bvps=14.15, pb=3.63, pnav=1.35)}
try:
    prev = pd.read_csv(os.path.join(DATA, "corrected_pb_pnav.csv"))
except Exception:
    prev = None

for t in ["DHT", "FRO"]:
    d07 = df[(df["ticker"] == t) & (df["date"] == "2007-12-31")]
    d08 = df[(df["ticker"] == t) & (df["date"] == "2008-12-31")]
    n = TODAY[t]
    print(f"\n  ── {t} ──")
    print(f"  {'':<26}{'P/B':>9}{'P/NAV':>9}")
    if len(d07):
        r = d07.iloc[0]
        print(f"  {'Dec-2007 (super-cycle)':<26}{r['pb']:>9.2f}"
              f"{(r['pnav'] if r['pnav'] == r['pnav'] else float('nan')):>9.2f}")
    if len(d08):
        r = d08.iloc[0]
        print(f"  {'Dec-2008 (post-crash)':<26}{r['pb']:>9.2f}{r['pnav']:>9.2f}")
    if prev is not None:
        for _, r in prev[prev["ticker"] == t].iterrows():
            if r["date"] != "2026-09-18":
                print(f"  {r['date'][:8]+' ':<26}{r['pb']:>9.2f}{r['pnav']:>9.2f}")
    print(f"  {'TODAY':<26}{n['pb']:>9.2f}{n['pnav']:>9.2f}")
    if len(d07):
        r = d07.iloc[0]
        print(f"\n     >> today's P/B is {n['pb']/r['pb']:.2f}x the Dec-2007 level "
              f"({n['pb']:.2f} vs {r['pb']:.2f})")

print("\n  🔴 THE HEADLINE: at the 2007 super-cycle peak both companies traded at")
print("     FAR HIGHER price/book than today — because they ran very high")
print("     leverage and paid out nearly everything, leaving almost no book")
print("     equity. Today's balance sheets are far stronger, so the SAME share")
print("     price buys a much larger book.")

# ================================================================ why
print("\n" + "-" * 96)
print("4) WHY — leverage then vs now")
print("-" * 96)
print(f"  {'':<6}{'date':<13}{'assets$m':>10}{'equity$m':>10}{'equity/assets':>15}")
for t in ["DHT", "FRO"]:
    for d, f in SUPER[t].items():
        eq = (f.get("equity") or f["assets"] - f["cur_liab"] - f["lt_liab"]) / 1e3
        print(f"  {t:<6}{d:<13}{f['assets']/1e3:>10,.0f}{eq:>10,.0f}"
              f"{eq/(f['assets']/1e3)*100:>14.0f}%")
print(f"  {'DHT':<6}{'2026-06-30':<13}{1808:>10,.0f}{1330:>10,.0f}{1330/1808*100:>14.0f}%")
print(f"  {'FRO':<6}{'2026-06-30':<13}{5813:>10,.0f}{3155:>10,.0f}{3155/5813*100:>14.0f}%")
print("\n  DHT equity/assets went from 17% (2007) to 74% (2026).")
print("  FRO went from 12% (2007) to 54%. THAT is why P/B looks lower today")
print("  in the super-cycle comparison: the denominator got much bigger.")

# ================================================================ 4b) the lesson
print("\n" + "-" * 96)
print("4b) 🔴 THE REAL LESSON OF 2008 — what leverage did to NAV")
print("-" * 96)
f07 = df[(df["ticker"] == "FRO") & (df["date"] == "2007-12-31")].iloc[0]
f08 = df[(df["ticker"] == "FRO") & (df["date"] == "2008-12-31")].iloc[0]
print(f"  FRO NAV per share:  Dec-2007 US${f07['navps']:.2f}  ->  "
      f"Dec-2008 US${f08['navps']:.2f}   = {(f08['navps']/f07['navps']-1)*100:.0f}%")
print(f"  (fleet value US${f07['fleet_usd_m']:,.0f}m -> US${f08['fleet_usd_m']:,.0f}m,")
print(f"   while net debt barely moved: US${f07['net_debt_usd_m']:,.0f}m -> "
      f"US${f08['net_debt_usd_m']:,.0f}m)")
print("\n  >> The 'P/NAV 20.24x' printed above for Dec-2008 is NOT a valuation.")
print("     It is NAV collapsing towards zero. With 88% of assets financed by")
print("     debt, a ~45% fall in ship values erased ~96% of net asset value.")
print("     THAT is what a cycle top does to a levered owner.")

print("\n  Same stress test on TODAY's balance sheets:")
print(f"  {'':<6}{'fleet US$m':>12}{'net debt':>10}{'NAVPS now':>11}"
      f"{'NAVPS if -45%':>15}{'change':>9}")
for t, fleet, nd, sh in [("DHT", 2806, 226, 161.24), ("FRO", 10368, 1847, 222.62)]:
    now = (fleet - nd) / sh
    crash = (fleet * 0.55 - nd) / sh
    print(f"  {t:<6}{fleet:>12,}{nd:>10,}{now:>11.2f}{crash:>15.2f}"
          f"{(crash/now-1)*100:>8.0f}%")
print("\n  >> DHT and FRO are now financed at ~8% and ~18% net-debt-to-fleet.")
print("     The SAME 45% vessel-value crash that erased 96% of FRO's NAV in")
print("     2008 would today cost roughly 50-55%. Still severe — but the")
print("     wipe-out risk of the super-cycle capital structure is gone.")

# ================================================================ chart
fig, axes = plt.subplots(1, 2, figsize=(15.5, 6))
for i, t in enumerate(["DHT", "FRO"]):
    ax = axes[i]
    labs, pbs, pnavs = [], [], []
    for d in ["2007-12-31", "2008-12-31"]:
        r = df[(df["ticker"] == t) & (df["date"] == d)]
        if len(r):
            labs.append(d[:7]); pbs.append(r.iloc[0]["pb"]); pnavs.append(r.iloc[0]["pnav"])
    if prev is not None:
        for _, r in prev[prev["ticker"] == t].iterrows():
            if r["date"] != "2026-09-18":
                labs.append(r["date"][:7]); pbs.append(r["pb"]); pnavs.append(r["pnav"])
    labs.append("TODAY"); pbs.append(TODAY[t]["pb"]); pnavs.append(TODAY[t]["pnav"])
    x = np.arange(len(labs))
    ax.bar(x - .2, pbs, .4, color="#7f8c8d", label="P/B")
    ax.bar(x + .2, pnavs, .4, color="#c0392b", label="P/NAV")
    for xi, v in zip(x - .2, pbs):
        ax.text(xi, v + .08, f"{v:.2f}", ha="center", fontsize=8, fontweight="bold")
    for xi, v in zip(x + .2, pnavs):
        if v == v:
            ax.text(xi, v + .08, f"{v:.2f}", ha="center", fontsize=8, fontweight="bold")
    ax.axhline(1.0, color="#27ae60", ls="--", lw=1.5)
    ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=8.5, rotation=15)
    ax.set_ylabel("multiple (x)")
    ax.set_title(f"{'AB'[i]}. {t} — including the 2005-08 super-cycle\n"
                 "Dec-2007 was FAR more expensive on book than today",
                 fontsize=10.5, fontweight="bold")
    ax.legend(fontsize=9); ax.grid(axis="y", alpha=.25)
fig.suptitle("The 2005-08 super-cycle vs today — multiples from the original 20-F filings\n"
             "prices converted back through the DHT 1-for-12 and FRO 1-for-5 reverse splits",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .90])
p = os.path.join(CHARTS, "supercycle_0508.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

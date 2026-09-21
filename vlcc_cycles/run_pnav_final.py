# -*- coding: utf-8 -*-
"""
FINAL, FILING-SOURCED P/NAV — replacing every estimated input.

This supersedes run_pnav_corrected.py. Research into the 20-F filings turned up
something far better than broker-range estimates:

  *** DHT PUBLISHES A PER-VESSEL THIRD-PARTY BROKER VALUATION TABLE IN EVERY
      20-F, ALONGSIDE CARRYING VALUE. ***

Those aggregates reconcile exactly to the prose DHT states in the same filing
(e.g. FY2020: carrying 1,476.4 - market 1,414.0 = the 62.4m shortfall DHT
discloses). So DHT's NAV is now COMPANY-REPORTED, not modelled.

TWO CORRECTIONS THIS FORCES:

1. THE US$174.5m "5-YEAR-OLD VLCC" I HAD BEEN USING IS MIS-LABELLED.
   It traces to Signal Ocean via Seatrade (7 May 2026), where 174.5 is an
   illustrative RESALE at a 35% premium to newbuild. In that SAME source the
   5-year-old is US$138m. The latest read (Allied, 2 Sep 2026) is ~US$151m for
   a 5-year-old and ~US$178m for a resale. Using the resale price as the
   5-year-old inflated NAV and therefore UNDERSTATED today's P/NAV.

2. DHT'S END-2015 FLEET WAS 18 VESSELS (15 VLCC + 1 Suezmax + 2 Aframax),
   NOT 14 VLCCs, and the share count was 92.910m, not the 112m the aggregator
   reported. Both of my earlier 2015 figures were wrong.

FRO REMAINS THE WEAK LINK: Frontline does NOT disclose an aggregate fleet
market value in any year examined. Its NAV therefore stays modelled, and is
labelled as such throughout.
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

SPLIT = {"DHT": 12.0, "FRO": 5.0}

# ============ DHT: EVERYTHING BELOW IS FROM THE 20-F FILINGS ================
# fleet_mv = aggregate charter-free fair market value, third-party brokers,
#            as disclosed by DHT and verified against its own prose totals.
DHT = {
    "2015-12-31": dict(ships=18, net_debt=495.7, shares=92.910, fleet_mv=1050.0,
                       note="15 VLCC + 1 Suezmax + 2 Aframax"),
    "2020-12-31": dict(ships=27, net_debt=381.4, shares=170.798, fleet_mv=1414.0,
                       note="27 VLCC"),
    "2023-12-31": dict(ships=24, net_debt=354.0, shares=161.000, fleet_mv=1965.5,
                       note="24 VLCC"),
    "2025-12-31": dict(ships=22, net_debt=349.7, shares=160.799, fleet_mv=1961.0,
                       note="22 VLCC + 2 newbuildings under construction"),
}
# Today: DHT has NOT yet disclosed a 2026 fleet value. Scale the Dec-2025
# aggregate by the move in second-hand VLCC values and add the extra hull.
# Dec-2025 implied 5-yr ~US$120m (DHT's own 7-yr was 110, 10-yr 91);
# Sep-2026 5-yr ~US$151m (Allied) => +26%.
DHT_TODAY = dict(ships=23, net_debt=273.1, shares=161.236,
                 fleet_mv=1961.0 * 1.26 * (23 / 22),
                 note="ESTIMATE: Dec-2025 aggregate scaled +26% for the move in "
                      "5-yr-old VLCC values and pro-rated 22->23 hulls")

# ============ FRO: MODELLED (no disclosure) ================================
FRO_FLEET = {"2020-12-31": dict(vlcc=22, suez=24, lr2=16),
             "2023-12-31": dict(vlcc=33, suez=25, lr2=18),
             "2026-09-18": dict(vlcc=42, suez=21, lr2=18)}
FRO_BS = {"2020-12-31": dict(net_debt=2073.9, shares=197.692),
          "2023-12-31": dict(net_debt=3150.7, shares=222.623),
          "2026-09-18": dict(net_debt=2113.4, shares=222.623)}
# CORRECTED 5-year-old values (not resale prices)
VALS = {"2020-12-31": dict(vlcc=65, suez=45, lr2=40),      # DSF Oct-2020
        "2023-12-31": dict(vlcc=98, suez=78, lr2=72.5),    # DSF Nov-2023
        "2026-09-18": dict(vlcc=151, suez=100, lr2=85)}    # Allied 2-Sep-2026
FRO_AGE = {"2020-12-31": 5, "2023-12-31": 6, "2026-09-18": 7}
AGE_DECAY = 0.055

print("=" * 98)
print("FINAL P/NAV — DHT from its own 20-F broker valuations; FRO modelled")
print("=" * 98)

PX, EQ = {}, {}
for t in ["DHT", "FRO"]:
    s = yf.download(t, start="2005-01-01", progress=False, auto_adjust=False)["Close"]
    PX[t] = (s.iloc[:, 0] if hasattr(s, "columns") else s).dropna()
    EQ[t] = pd.read_csv(os.path.join(DATA, f"bs_history_{t}.csv"),
                        index_col=0, parse_dates=True)

print("\n" + "-" * 98)
print("1) 🔴 THE VESSEL-VALUE CORRECTION")
print("-" * 98)
print("  What I had been using for 'today':  US$170-179m  <- this is a RESALE price")
print("  Signal Ocean 7-May-2026 : 5-yr-old US$138m · newbuild US$129m · resale US$174.5m")
print("  Allied      2-Sep-2026 : 5-yr-old ~US$151m · newbuild ~US$130m · resale ~US$178m")
print("  >> Using the RESALE price as the 5-year-old inflated NAV and therefore")
print("     UNDERSTATED today's P/NAV. Corrected to US$151m.")

# ================================================================ DHT
print("\n" + "-" * 98)
print("2) DHT — NAV from the company's own disclosed broker valuations")
print("-" * 98)
print(f"  {'date':<13}{'ships':>6}{'fleet MV':>10}{'net debt':>10}{'shares':>9}"
      f"{'NAVPS':>8}{'price':>8}{'P/NAV':>8}{'BVPS':>8}{'P/B':>7}  source")
rows = []
for d, f in list(DHT.items()) + [("2026-09-18", DHT_TODAY)]:
    ts = pd.Timestamp(d)
    price = float(PX["DHT"].loc[:d].iloc[-1])
    b = EQ["DHT"][EQ["DHT"].index <= ts].tail(1)
    eq = (b.iloc[0]["total-assets"] - b.iloc[0]["total-liabilities"]) if len(b) else np.nan
    bvps = eq / f["shares"]
    navps = (f["fleet_mv"] - f["net_debt"]) / f["shares"]
    src = "20-F" if d in DHT else "EST"
    print(f"  {d:<13}{f['ships']:>6}{f['fleet_mv']:>10,.0f}{f['net_debt']:>10,.1f}"
          f"{f['shares']:>9.1f}{navps:>8.2f}{price:>8.2f}{price/navps:>8.2f}"
          f"{bvps:>8.2f}{price/bvps:>7.2f}  {src}")
    rows.append(dict(ticker="DHT", date=d, ships=f["ships"],
                     fleet_mv=round(f["fleet_mv"], 1), net_debt=f["net_debt"],
                     shares=f["shares"], navps=round(navps, 2),
                     price=round(price, 2), pnav=round(price / navps, 2),
                     bvps=round(bvps, 2), pb=round(price / bvps, 2), source=src))

# ================================================================ FRO
print("\n" + "-" * 98)
print("3) FRO — MODELLED (Frontline discloses no aggregate fleet value)")
print("-" * 98)
print(f"  {'date':<13}{'ships':>6}{'fleet MV':>10}{'net debt':>10}{'shares':>9}"
      f"{'NAVPS':>8}{'price':>8}{'P/NAV':>8}{'BVPS':>8}{'P/B':>7}")
for d, fl in FRO_FLEET.items():
    ts = pd.Timestamp(d)
    bs = FRO_BS[d]
    price = float(PX["FRO"].loc[:d].iloc[-1])
    b = EQ["FRO"][EQ["FRO"].index <= ts].tail(1)
    eq = (b.iloc[0]["total-assets"] - b.iloc[0]["total-liabilities"]) if len(b) else np.nan
    bvps = eq / bs["shares"]
    hair = max(0.25, 1 - AGE_DECAY * max(0, FRO_AGE[d] - 5))
    mv = sum(fl[k] * VALS[d][k] for k in fl) * hair
    navps = (mv - bs["net_debt"]) / bs["shares"]
    print(f"  {d:<13}{sum(fl.values()):>6}{mv:>10,.0f}{bs['net_debt']:>10,.1f}"
          f"{bs['shares']:>9.1f}{navps:>8.2f}{price:>8.2f}{price/navps:>8.2f}"
          f"{bvps:>8.2f}{price/bvps:>7.2f}")
    rows.append(dict(ticker="FRO", date=d, ships=sum(fl.values()),
                     fleet_mv=round(mv), net_debt=bs["net_debt"],
                     shares=bs["shares"], navps=round(navps, 2),
                     price=round(price, 2), pnav=round(price / navps, 2),
                     bvps=round(bvps, 2), pb=round(price / bvps, 2),
                     source="MODELLED"))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA, "pnav_final.csv"), index=False)

# ================================================================ verdict
print("\n" + "=" * 98)
print("4) ⭐ FINAL ANSWER — how does today compare, on filing-sourced NAV?")
print("=" * 98)
for t in ["DHT", "FRO"]:
    d = df[df["ticker"] == t]
    now = d.iloc[-1]
    prior = d.iloc[:-1]
    print(f"\n  ── {t} ──")
    print(f"  {'date':<13}{'P/B':>8}{'P/NAV':>8}   source")
    for _, r in d.iterrows():
        tag = "  <-- TODAY" if r["date"] == "2026-09-18" else ""
        print(f"  {r['date']:<13}{r['pb']:>8.2f}{r['pnav']:>8.2f}   {r['source']}{tag}")
    print(f"     today P/NAV {now['pnav']:.2f}x vs prior {prior['pnav'].min():.2f}"
          f"-{prior['pnav'].max():.2f}x  -> {now['pnav']/prior['pnav'].max():.2f}x the peak")

print("\n  Plus the 2007 super-cycle from §16 (20-F sourced):")
print("     DHT Dec-2007  P/B 5.11x     FRO Dec-2007  P/B 8.05x")

# ================================================================ chart
fig, axes = plt.subplots(1, 2, figsize=(15.5, 6))
for i, t in enumerate(["DHT", "FRO"]):
    ax = axes[i]
    d = df[df["ticker"] == t]
    x = np.arange(len(d))
    ax.bar(x - .2, d["pb"], .4, color="#7f8c8d", label="P/B")
    ax.bar(x + .2, d["pnav"], .4, color="#c0392b", label="P/NAV")
    for xi, v in zip(x - .2, d["pb"]):
        ax.text(xi, v + .03, f"{v:.2f}", ha="center", fontsize=8.5, fontweight="bold")
    for xi, v in zip(x + .2, d["pnav"]):
        ax.text(xi, v + .03, f"{v:.2f}", ha="center", fontsize=8.5, fontweight="bold")
    ax.axhline(1.0, color="#27ae60", ls="--", lw=1.6)
    ax.set_xticks(x)
    ax.set_xticklabels([r["date"][:7] for _, r in d.iterrows()], fontsize=8.5, rotation=12)
    ax.set_ylabel("multiple (x)")
    sub = "NAV from DHT's own 20-F broker valuations" if t == "DHT" \
        else "NAV MODELLED — Frontline discloses none"
    ax.set_title(f"{'AB'[i]}. {t}\n{sub}", fontsize=10.5, fontweight="bold")
    ax.legend(fontsize=9); ax.grid(axis="y", alpha=.25)
fig.suptitle("Final P/NAV — corrected for the resale-vs-5-year-old mislabel and "
             "rebuilt on filing-sourced fleet values",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .90])
p = os.path.join(CHARTS, "pnav_final.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

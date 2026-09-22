# -*- coding: utf-8 -*-
"""
SECTION 28 v2 — CONSOLIDATED DASHBOARD, rebuilt after the GPT-6-Astra review.

The review returned five required withdrawals. The most damaging was one I had
missed entirely: DHT's "current" fleet was priced off a DECEMBER-2025 roster
that includes three vessels the company has since SOLD, and omits two
newbuildings it has since TAKEN DELIVERY of.

From DHT's own FY2025 20-F, verbatim:
  "in December 2025 and January 2026, we agreed to sell our three 2007-built
   VLCCs, the DHT China, DHT Europe and DHT Bauhinia. In January 2026, we took
   delivery of a newbuild vessel, the DHT Antelope, and in March 2026 we took
   delivery of the DHT Addax. We expect two additional newbuilds to be
   delivered in 2026."
  "...sell the DHT China and DHT Europe for a combined price of $101.6 million"
  "...sell the DHT Bauhinia, built in 2007, for a price of $51.5 million"

Also corrected: the Xclusiv report DOES carry Suezmax and Aframax benchmarks.
The earlier draft used assumed values instead. Full table, Sep-2026 vs Sep-2025:

             Resale   5 Year  10 Year  15 Year
  VLCC        193.0    172.0    152.0    135.0
  Suezmax     136.0    116.0     95.0     72.0
  Aframax      95.0     85.0     72.5     55.0
"""

import io
import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
MARK = "18-21 Sep 2026 (Xclusiv)"
NOW = 2026.72

CURVE = {  # age -> value, from the Xclusiv table. >15yr is EXTRAPOLATED.
    "VLCC":    ([0, 5, 10, 15, 20], [193.0, 172.0, 152.0, 135.0, 85.0]),
    "Suezmax": ([0, 5, 10, 15, 20], [136.0, 116.0, 95.0, 72.0, 45.0]),
    "LR2":     ([0, 5, 10, 15, 20], [95.0, 85.0, 72.5, 55.0, 35.0]),
}


def val(typ, age):
    a, v = CURVE[typ]
    return float(np.interp(max(age, 0), a, v))


print("=" * 100)
print("SECTION 28 v2 — DASHBOARD REBUILT AFTER REVIEW")
print("=" * 100)

# ══════════════════ 1) DHT roster, corrected ═════════════════════════════════
v = pd.read_csv(os.path.join(DATA, "s27_dht_vessels.csv"))
SOLD = ["DHT China", "DHT Europe", "DHT Bauhinia"]
sold_mask = v["name"].isin(SOLD)
print("\n" + "-" * 100)
print("1) 🔴 DHT ROSTER — the earlier draft priced vessels DHT no longer owns")
print("-" * 100)
print(f"  {'vessel':<18}{'built':>7}{'my value':>11}{'ACTUAL sale price':>20}{'error':>10}")
ACTUAL = {"DHT China": 50.8, "DHT Europe": 50.8, "DHT Bauhinia": 51.5}
err = 0
for _, r in v[sold_mask].iterrows():
    a = ACTUAL[r["name"]]
    err += r["now_val"] - a
    print(f"  {r['name']:<18}{int(r['built']):>7}{r['now_val']:>11.1f}{a:>20.1f}"
          f"{r['now_val']-a:>+10.1f}")
print(f"  {'':<18}{'':>7}{v[sold_mask]['now_val'].sum():>11.1f}"
      f"{sum(ACTUAL.values()):>20.1f}{err:>+10.1f}")
print(f"\n  >> The three 2007-built VLCCs were AGREED SOLD in Dec-2025/Jan-2026")
print(f"     for US$153.1m in total. The draft carried them at "
      f"US${v[sold_mask]['now_val'].sum():.1f}m and, worse,")
print(f"     counted them as still owned. DHT Europe was delivered to its new")
print(f"     owner on 30 January 2026.")

keep = v[~sold_mask].copy()
NEWBUILDS = [("DHT Antelope", 2026.0), ("DHT Addax", 2026.2)]
nb_rows = [dict(name=n, built=b, typ="VLCC", dec25_fmv=np.nan,
                age=NOW - b, now_val=val("VLCC", NOW - b)) for n, b in NEWBUILDS]
dht = pd.concat([keep, pd.DataFrame(nb_rows)], ignore_index=True)
print(f"\n  Corrected roster: {len(v)} parsed - {int(sold_mask.sum())} sold "
      f"+ {len(NEWBUILDS)} delivered newbuilds = {len(dht)} vessels")
print(f"  {'':<18}{'fleet value':>14}{'avg age':>10}")
print(f"  {'draft':<18}{v['now_val'].sum():>14,.0f}{v['age'].mean():>10.1f}")
print(f"  {'corrected':<18}{dht['now_val'].sum():>14,.0f}{dht['age'].mean():>10.1f}")
print(f"\n  ⚠️ STILL UNRESOLVED: the parser captured 21 of 22 vessels at Dec-2025,")
print(f"     and DHT says TWO MORE newbuilds were expected during 2026. The")
print(f"     roster below is therefore a LOWER BOUND on vessel count.")
dht_fleet = dht["now_val"].sum()

# ══════════════════ 2) FRO, on the actual broker marks ═══════════════════════
print("\n" + "-" * 100)
print("2) FRO — now on the Xclusiv Suezmax/Aframax marks, not assumptions")
print("-" * 100)
FRO_AGE = 6.6
SEGS = [("VLCC", 40), ("Suezmax", 19), ("LR2", 18)]
print(f"  {'segment':<10}{'ships':>7}{'draft $m/ship':>15}{'CORRECTED':>12}"
      f"{'total $m':>12}")
fro_fleet = 0
DRAFT = {"VLCC": 165.6, "Suezmax": 120.0, "LR2": 80.0}
for s, n in SEGS:
    x = val(s, FRO_AGE)
    fro_fleet += n * x
    print(f"  {s:<10}{n:>7}{DRAFT[s]:>15.1f}{x:>12.1f}{n*x:>12,.0f}")
print(f"  {'TOTAL':<10}{77:>7}{'':>15}{'':>12}{fro_fleet:>12,.0f}")
print(f"  draft total was $10,344m -> corrected {fro_fleet/10344-1:+.1%}")
print("  >> The draft's $120m Suezmax was ABOVE the actual 5-year mark of $116m.")

# ══════════════════ 3) corrected dashboard ═══════════════════════════════════
CO = {
    "DHT": dict(shares=161.236, bvps=8.26, net_debt=273.1, fleet=dht_fleet,
                vlcc_eq=24.0, days=350, be=17_500, dna=105,
                q2_eps=1.22, q2_dps=1.22, ttm_eps=2.94, ttm_dps=2.27,
                hist_mean=1.04, hist_max=1.45),
    "FRO": dict(shares=222.623, bvps=14.15, net_debt=2113.4, fleet=fro_fleet,
                vlcc_eq=57.9, days=350, be=23_800, dna=300,
                q2_eps=2.61, q2_dps=2.61, ttm_eps=6.67, ttm_dps=5.99,
                hist_mean=0.99, hist_max=1.45),
}
for t in CO:
    s = yf.download(t, period="5d", progress=False, auto_adjust=False)["Close"]
    CO[t]["price"] = float((s.iloc[:, 0] if hasattr(s, "columns") else s).dropna().iloc[-1])


def eps(d, r):
    return ((r - d["be"]) * d["vlcc_eq"] * d["days"] / 1e6 - d["dna"]) / d["shares"]


print("\n" + "=" * 100)
print("3) CORRECTED DASHBOARD")
print("=" * 100)
print(f"  {'':<32}{'DHT':>15}{'FRO':>15}")
rows = {}
for t, d in CO.items():
    nav = (d["fleet"] - d["net_debt"]) / d["shares"]
    rows[t] = dict(price=d["price"], navps=nav, pnav=d["price"] / nav,
                   pb=d["price"] / d["bvps"],
                   pe_q2=d["price"] / (d["q2_eps"] * 4),
                   pe_ttm=d["price"] / d["ttm_eps"],
                   y_q2=d["q2_dps"] * 4 / d["price"] * 100,
                   y_ttm=d["ttm_dps"] / d["price"] * 100,
                   prem=d["price"] - nav, fleet=d["fleet"])
for lbl, k, f in [("price", "price", "${:.2f}"), ("fleet value US$m", "fleet", "{:,.0f}"),
                  ("NAV/share", "navps", "${:.2f}"), ("P/NAV", "pnav", "{:.2f}x"),
                  ("P/B", "pb", "{:.2f}x"),
                  ("P/E on Q2 annualised", "pe_q2", "{:.2f}x"),
                  ("P/E trailing 12m", "pe_ttm", "{:.2f}x"),
                  ("yield, Q2 annualised", "y_q2", "{:.1f}%"),
                  ("yield, trailing 12m", "y_ttm", "{:.1f}%"),
                  ("premium over NAV/share", "prem", "${:.2f}")]:
    print(f"  {lbl:<32}" + "".join(f.format(rows[t][k]).rjust(15) for t in ("DHT", "FRO")))

print("\n  PREMIUM / DIVIDEND at FOUR dividend bases — NOT a payback forecast")
print(f"  {'basis':<30}{'DHT':>12}{'FRO':>12}")
for lbl, fn in [("Q2 annualised (peak qtr)", lambda d: d["q2_dps"] * 4),
                ("trailing 12m actual", lambda d: d["ttm_dps"]),
                ("model @ 1-yr TC $105k", lambda d: max(eps(d, 105_000), 0)),
                ("model @ 1-yr TC $93k", lambda d: max(eps(d, 93_000), 0)),
                ("model @ FY2025 $47.2k", lambda d: max(eps(d, 47_200), 0))]:
    cells = ""
    for t, d in CO.items():
        dv = fn(d)
        cells += (f"{rows[t]['prem']/dv:>11.2f}y" if dv > .01 else f"{'never':>12}")
    print(f"  {lbl:<30}{cells}")

print("\n  P/NAV SENSITIVITY — two-sided, because the direction of bias is NOT known")
print(f"  {'scenario':<40}{'DHT':>10}{'FRO':>10}")
for lbl, dmul, fmul in [("as computed", 1.0, 1.0),
                        ("fleet values -10%", .9, .9),
                        ("fleet values -20%", .8, .8),
                        ("fleet values +10%", 1.1, 1.1)]:
    c = ""
    for t, m in (("DHT", dmul), ("FRO", fmul)):
        d = CO[t]
        nv = (d["fleet"] * m - d["net_debt"]) / d["shares"]
        c += f"{d['price']/nv:>10.2f}"
    print(f"  {lbl:<40}{c}")

pd.DataFrame(rows).T.to_csv(os.path.join(DATA, "s28_dashboard.csv"))
dht.to_csv(os.path.join(DATA, "s28_dht_roster.csv"), index=False)
print(f"\n  >> vessel marks dated {MARK}")
print("\nDone.")

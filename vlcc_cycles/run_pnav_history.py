# -*- coding: utf-8 -*-
"""
P/NAV HISTORY for DHT and FRO.

  NAV per share = (fleet charter-free market value - net debt) / shares
  P/NAV         = year-end share price / NAV per share

DHT: fleet market value is FILING-SOURCED -- summed from the per-vessel broker
     valuation tables in each 20-F (see run_dht_fleet_fmv.py). Balance-sheet
     items come from SEC XBRL company facts.

FRO: Frontline discloses NO fleet market value in any year examined (§23.9).
     Its NAV is therefore MODELLED: DHT's disclosed average value per vessel is
     applied to FRO's VLCC-equivalent fleet. This is an approximation and is
     labelled as such everywhere. It is the same approach §17 used.
"""

import io
import json
import os
import sys
import time
import urllib.request

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
DATA, CHARTS = os.path.join(HERE, "data"), os.path.join(HERE, "charts")
UA = {"User-Agent": "VLCC-Research research@example.com"}


def facts(cik):
    u = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    return json.loads(urllib.request.urlopen(
        urllib.request.Request(u, headers=UA), timeout=90).read())


def series(f, tags, unit="USD"):
    out = {}
    for ns in ("us-gaap", "ifrs-full"):
        for t in tags:
            node = f.get("facts", {}).get(ns, {}).get(t)
            if not node:
                continue
            for u, arr in node.get("units", {}).items():
                if unit not in u:
                    continue
                for e in arr:
                    if e.get("form", "").startswith("20-F") and "end" in e \
                            and e["end"].endswith("-12-31"):
                        out.setdefault(int(e["end"][:4]), {}).setdefault(t, e["val"])
    return {y: list(v.values())[0] for y, v in out.items()}


print("=" * 100)
print("P/NAV HISTORY — DHT (filing-sourced fleet values) and FRO (modelled)")
print("=" * 100)

fl = pd.read_csv(os.path.join(DATA, "s26_dht_fleet_fmv.csv"))
FLEET = dict(zip(fl["asof"], fl["fleet_fmv_m"]))
NSHIP = dict(zip(fl["asof"], fl["n_vessels"]))
AVG = dict(zip(fl["asof"], fl["avg_per_vessel_m"]))

DEBT_TAGS = ["LongtermBorrowings", "LongTermDebtNoncurrent", "LongTermDebt",
             "Borrowings", "LongTermDebtAndCapitalLeaseObligations"]
CUR_TAGS = ["CurrentPortionOfLongtermBorrowings",
            "CurrentBorrowingsAndCurrentPortionOfNoncurrentBorrowings",
            "LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent"]
LEASE_TAGS = ["NoncurrentLeaseLiabilities", "CapitalLeaseObligationsNoncurrent"]
LEASE_CUR = ["CurrentLeaseLiabilities", "CapitalLeaseObligationsCurrent"]
CASH_TAGS = ["CashAndCashEquivalents", "CashAndCashEquivalentsAtCarryingValue"]
SHARE_TAGS = ["NumberOfSharesOutstanding", "CommonStockSharesOutstanding",
              "NumberOfSharesIssuedAndFullyPaid", "IssuedCapitalOrdinaryShares",
              "CommonStockSharesIssued", "AdjustedWeightedAverageShares"]

bal = {}
for nm, cik in [("DHT", 1331284), ("FRO", 913290)]:
    f = facts(cik)
    bal[nm] = dict(debt=series(f, DEBT_TAGS), cash=series(f, CASH_TAGS),
                   cur=series(f, CUR_TAGS), lease=series(f, LEASE_TAGS),
                   lcur=series(f, LEASE_CUR),
                   eq=series(f, ["Equity", "StockholdersEquity",
                                 "EquityAttributableToOwnersOfParent"]),
                   sh=series(f, SHARE_TAGS, unit="shares"))
    print(f"  {nm}: debt yrs {sorted(bal[nm]['debt'])[:3]}..{sorted(bal[nm]['debt'])[-3:]} "
          f"| shares yrs {sorted(bal[nm]['sh'])[:3]}..{sorted(bal[nm]['sh'])[-3:]}")
    time.sleep(0.4)


def net_debt(nm, y):
    b = bal[nm]
    return (b["debt"].get(y, 0) + b["cur"].get(y, 0)
            + b["lease"].get(y, 0) + b["lcur"].get(y, 0)
            - b["cash"].get(y, 0)) / 1e6

px = {}
for t in ("DHT", "FRO"):
    d = yf.download(t, period="max", progress=False, auto_adjust=False)["Close"]
    px[t] = (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna()

# ── DHT: everything filing-sourced except price ──────────────────────────────
print("\n" + "-" * 100)
print("DHT — fleet value from its own 20-F per-vessel broker tables")
print("-" * 100)
print(f"  {'year':<6}{'ships':>6}{'fleet FMV':>12}{'net debt':>11}{'NAV $m':>10}"
      f"{'shares m':>10}{'NAVPS':>8}{'price':>8}{'P/NAV':>8}")
rows = []
for y in sorted(FLEET):
    b = bal["DHT"]
    if y not in b["debt"] or y not in b["sh"]:
        continue
    nd = net_debt("DHT", y)
    nav = FLEET[y] - nd
    sh = b["sh"][y] / 1e6
    navps = nav / sh
    p = float(px["DHT"][:f"{y}-12-31"].iloc[-1])
    rows.append(dict(ticker="DHT", year=y, ships=NSHIP[y], fleet_fmv=FLEET[y],
                     net_debt=round(nd, 1), nav=round(nav, 1), shares=round(sh, 2),
                     navps=round(navps, 2), price=round(p, 2),
                     pnav=round(p / navps, 3), basis="filed"))
    print(f"  {y:<6}{NSHIP[y]:>6}{FLEET[y]:>12,.0f}{nd:>11,.0f}{nav:>10,.0f}"
          f"{sh:>10.1f}{navps:>8.2f}{p:>8.2f}{p/navps:>8.2f}")

# ── FRO: modelled ────────────────────────────────────────────────────────────
FRO_EQ = {2017: 52.0, 2018: 53.0, 2019: 56.0, 2020: 62.0, 2021: 62.0,
          2022: 63.0, 2023: 76.0, 2024: 81.0, 2025: 81.0}    # VLCC-equivalents
print("\n" + "-" * 100)
print("FRO — ⚠️ MODELLED. Frontline discloses no fleet market value (§23.9).")
print("  DHT's disclosed average value per vessel is applied to FRO's fleet.")
print("-" * 100)
print(f"  {'year':<6}{'VLCC-eq':>9}{'$m/ship':>9}{'fleet FMV':>12}{'net debt':>11}"
      f"{'NAVPS':>8}{'price':>8}{'P/NAV':>8}")
for y in sorted(FRO_EQ):
    if y not in AVG:
        continue
    b = bal["FRO"]
    if y not in b["debt"] or y not in b["sh"]:
        continue
    fmv = FRO_EQ[y] * AVG[y]
    nd = net_debt("FRO", y)
    sh = b["sh"][y] / 1e6
    navps = (fmv - nd) / sh
    p = float(px["FRO"][:f"{y}-12-31"].iloc[-1])
    if navps <= 0:
        continue
    rows.append(dict(ticker="FRO", year=y, ships=FRO_EQ[y], fleet_fmv=round(fmv),
                     net_debt=round(nd, 1), nav=round(fmv - nd, 1),
                     shares=round(sh, 2), navps=round(navps, 2), price=round(p, 2),
                     pnav=round(p / navps, 3), basis="modelled"))
    print(f"  {y:<6}{FRO_EQ[y]:>9.0f}{AVG[y]:>9.1f}{fmv:>12,.0f}{nd:>11,.0f}"
          f"{navps:>8.2f}{p:>8.2f}{p/navps:>8.2f}")

df = pd.DataFrame(rows)
# ── sanity filter: drop rows whose share count is implausible ────────────────
BAD = (df["shares"] < 50) | (df["shares"] > 400)
if BAD.any():
    print(f"\n  ⚠️ DROPPED {int(BAD.sum())} row(s) with an implausible share count "
          f"(XBRL tag collision):")
    for _, r in df[BAD].iterrows():
        print(f"     {r['ticker']} {int(r['year'])}: {r['shares']:,.1f}m shares — excluded")
    df = df[~BAD].copy()
df.to_csv(os.path.join(DATA, "s26_pnav_history.csv"), index=False)

print("\n  CROSS-CHECK — DHT against the filing-sourced values already in §17:")
S17 = {2020: 0.87, 2023: 0.98, 2025: 1.22}
for y, v in S17.items():
    r = df[(df["ticker"] == "DHT") & (df["year"] == y)]
    if len(r):
        got = float(r["pnav"].iloc[0])
        print(f"     {y}: §17 {v:.2f}x · this series {got:.2f}x · "
              f"diff {(got/v-1)*100:+.0f}%")

# ── summary ──────────────────────────────────────────────────────────────────
TODAY = {"DHT": 1.62, "FRO": 1.69}
print("\n" + "=" * 100)
print("⭐ HISTORICAL AVERAGE vs TODAY")
print("=" * 100)
print(f"  {'':<6}{'n':>4}{'mean':>8}{'median':>9}{'min':>8}{'max':>8}"
      f"{'TODAY':>9}{'vs mean':>10}{'vs max':>9}")
summ = []
for t in ("DHT", "FRO"):
    s = df[df["ticker"] == t]["pnav"]
    if not len(s):
        continue
    td = TODAY[t]
    print(f"  {t:<6}{len(s):>4}{s.mean():>8.2f}{s.median():>9.2f}{s.min():>8.2f}"
          f"{s.max():>8.2f}{td:>9.2f}{(td/s.mean()-1)*100:>9.0f}%"
          f"{(td/s.max()-1)*100:>8.0f}%")
    summ.append(dict(ticker=t, n=len(s), mean=round(s.mean(), 2),
                     median=round(s.median(), 2), min=round(s.min(), 2),
                     max=round(s.max(), 2), today=td,
                     vs_mean_pct=round((td / s.mean() - 1) * 100),
                     vs_max_pct=round((td / s.max() - 1) * 100)))
pd.DataFrame(summ).to_csv(os.path.join(DATA, "s26_pnav_summary.csv"), index=False)

# ── chart ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(1, 2, figsize=(15, 5.6))
for i, t in enumerate(("DHT", "FRO")):
    a = ax[i]
    s = df[df["ticker"] == t]
    if not len(s):
        continue
    c = "#c0392b" if t == "DHT" else "#2980b9"
    a.plot(s["year"], s["pnav"], "o-", color=c, lw=2.2, ms=7, label="year-end P/NAV")
    a.axhline(s["pnav"].mean(), color=c, ls="--", lw=1.6,
              label=f"mean {s['pnav'].mean():.2f}x")
    a.axhline(1.0, color="k", ls=":", lw=1.4)
    a.scatter([2026.7], [TODAY[t]], s=170, marker="*", color="#f59e0b",
              zorder=5, edgecolor="k", linewidth=.7,
              label=f"today {TODAY[t]:.2f}x")
    a.text(2026.7, TODAY[t] * 1.06, f"{TODAY[t]:.2f}x", ha="center",
           fontsize=10, fontweight="bold", color="#b45309")
    for _, r in s.iterrows():
        a.text(r["year"], r["pnav"] - .09, f"{r['pnav']:.2f}", ha="center",
               fontsize=7.5, color=c)
    a.set_ylabel("price / NAV per share")
    a.set_ylim(0, max(TODAY[t], s["pnav"].max()) * 1.28)
    basis = "filing-sourced fleet values" if t == "DHT" else "MODELLED fleet values (see caveat)"
    a.set_title(f"{'AB'[i]}. {t} — P/NAV history\n{basis}",
                fontsize=11.5, fontweight="bold")
    a.legend(fontsize=9); a.grid(alpha=.25)
fig.suptitle("P/NAV trajectory vs today — DHT and Frontline",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .92])
p = os.path.join(CHARTS, "s26_pnav_history.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

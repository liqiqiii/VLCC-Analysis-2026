# -*- coding: utf-8 -*-
"""
CORRECTED P/B and P/NAV at every cycle top.

*** WHY THIS FILE EXISTS: A CORRECTION ***

run_historical_pb.py sourced its P/B series from macrotrends. That source
divides a DIVIDEND-ADJUSTED price by an UNADJUSTED book value per share. For
ordinary stocks the distortion is small. For tanker companies, which pay out
most of their earnings, it is severe and systematic: it makes every historical
period look CHEAPER than it was.

Measured distortion (raw price / actual reported BVPS vs what was published):

    DHT 2015-12-31   published 0.42x   ACTUAL 1.23x
    DHT 2020-12-31   published 0.52x   ACTUAL 0.80x
    DHT 2023-12-31   published 1.16x   ACTUAL 1.54x
    FRO 2023-12-31   published 1.51x   ACTUAL 1.96x

The direction of the error always flattered the "today is unprecedented" story,
so it had to be fixed before any conclusion could stand.

THIS FILE REBUILDS BOTH MEASURES FROM PRIMARY-STYLE INPUTS:
    price  = RAW (unadjusted) closing price from Yahoo on the date
    BVPS   = (total assets - total liabilities) / shares outstanding, from the
             balance sheet for that quarter
    NAV    = (vessels x second-hand value of a similar-age ship) - net debt

Balance-sheet history covers 2011-2026, so the 2008 super-cycle CANNOT be
computed on this basis and is reported as a GAP rather than with bad data.
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

# 5-year-old second-hand values, US$m (broker/press ranges -- see report).
VLCC_5YR = {"2015-12-31": (70, 80), "2020-12-31": (68, 72),
            "2023-12-31": (98, 113), "2026-09-18": (170, 179)}
SUEZ_5YR = {"2020-12-31": (45, 50), "2023-12-31": (72, 80), "2026-09-18": (115, 125)}
LR2_5YR = {"2020-12-31": (38, 43), "2023-12-31": (60, 68), "2026-09-18": (95, 105)}

FLEET = {
    "DHT": {"2015-12-31": dict(vlcc=14), "2020-12-31": dict(vlcc=27),
            "2023-12-31": dict(vlcc=24), "2026-09-18": dict(vlcc=24)},
    # FRO 2023 CORRECTED: 33 VLCC / 25 Suezmax / 18 LR2 = 76 owned vessels per
    # the 2023 ESG report -- 11 of the Euronav VLCCs had already been delivered
    # in Q4-2023 (13 more followed in 2024). An earlier draft used 22 VLCCs and
    # materially overstated FRO's 2023 P/NAV.
    # FRO 2020 is flagged INDICATIVE: the source could not confirm it from the
    # 20-F and gave ~22/24/16.
    "FRO": {"2020-12-31": dict(vlcc=22, suez=24, lr2=16),
            "2023-12-31": dict(vlcc=33, suez=25, lr2=18),
            "2026-09-18": dict(vlcc=42, suez=21, lr2=18)},
}
AVG_AGE = {"DHT": {"2015-12-31": 7, "2020-12-31": 8, "2023-12-31": 10,
                   "2026-09-18": 11},
           "FRO": {"2020-12-31": 5, "2023-12-31": 6, "2026-09-18": 7}}
AGE_DECAY = 0.055

print("=" * 98)
print("CORRECTED: P/B and P/NAV at every cycle top, from RAW prices and")
print("           REPORTED book value — replacing the contaminated series")
print("=" * 98)

PX, BS = {}, {}
for t in ["DHT", "FRO"]:
    s = yf.download(t, start="2011-01-01", progress=False, auto_adjust=False)["Close"]
    PX[t] = (s.iloc[:, 0] if hasattr(s, "columns") else s).dropna()
    BS[t] = pd.read_csv(os.path.join(DATA, f"bs_history_{t}.csv"),
                        index_col=0, parse_dates=True)

print("\n" + "-" * 98)
print("1) THE CORRECTION, QUANTIFIED — published vs actual")
print("-" * 98)
PUBLISHED = {("DHT", "2015-12-31"): 0.42, ("DHT", "2020-12-31"): 0.52,
             ("DHT", "2023-12-31"): 1.16, ("FRO", "2020-12-31"): 0.49,
             ("FRO", "2023-12-31"): 1.51}
print(f"  {'':<6}{'date':<13}{'published P/B':>15}{'ACTUAL P/B':>13}{'error':>10}")
corr = []
for (t, d), pub in PUBLISHED.items():
    b = BS[t][BS[t].index <= pd.Timestamp(d)].tail(1).iloc[0]
    bvps = (b["total-assets"] - b["total-liabilities"]) / b["shares-outstanding"]
    raw = float(PX[t].loc[:d].iloc[-1])
    act = raw / bvps
    print(f"  {t:<6}{d:<13}{pub:>15.2f}{act:>13.2f}{(pub/act-1)*100:>9.0f}%")
    corr.append(dict(ticker=t, date=d, published_pb=pub, actual_pb=round(act, 2),
                     understated_by_pct=round((pub / act - 1) * 100)))
pd.DataFrame(corr).to_csv(os.path.join(DATA, "pb_correction.csv"), index=False)
print("\n  Every published figure was TOO LOW. The error is systematic because")
print("  dividend-adjusted prices shrink the numerator while book value —")
print("  which dividends genuinely reduce — was left unadjusted.")

# ================================================================ rebuild
print("\n" + "-" * 98)
print("2) CORRECTED P/B AND P/NAV AT EACH CYCLE TOP")
print("-" * 98)
rows = []
for t in ["DHT", "FRO"]:
    print(f"\n  ── {t} ──")
    print(f"  {'date':<13}{'price':>8}{'BVPS':>8}{'P/B':>7}"
          f"{'ships':>7}{'age':>5}{'fleet':>9}{'netdebt':>9}{'NAVPS':>8}{'P/NAV':>8}")
    for d, fl in FLEET[t].items():
        ts = pd.Timestamp(d)
        b = BS[t][BS[t].index <= ts].tail(1).iloc[0]
        sh = b["shares-outstanding"]
        eq = b["total-assets"] - b["total-liabilities"]
        bvps = eq / sh
        nd = b["long-term-debt"] - b["cash-on-hand"]
        price = float(PX[t].loc[:d].iloc[-1]) if ts <= PX[t].index[-1] \
            else float(PX[t].iloc[-1])
        age = AVG_AGE[t][d]
        hair = max(0.25, 1 - AGE_DECAY * max(0, age - 5))
        vals = []
        for i in (0, 1):
            v = VLCC_5YR[d][i] * fl.get("vlcc", 0)
            if fl.get("suez"):
                v += SUEZ_5YR[d][i] * fl["suez"]
            if fl.get("lr2"):
                v += LR2_5YR[d][i] * fl["lr2"]
            vals.append(v * hair)
        fleet_mid = np.mean(vals)
        navps_lo, navps_hi = (vals[0] - nd) / sh, (vals[1] - nd) / sh
        navps = (navps_lo + navps_hi) / 2
        pb, pnav = price / bvps, price / navps
        print(f"  {d:<13}{price:>8.2f}{bvps:>8.2f}{pb:>7.2f}"
              f"{sum(fl.values()):>7}{age:>5}{fleet_mid:>9,.0f}{nd:>9,.0f}"
              f"{navps:>8.2f}{pnav:>8.2f}")
        rows.append(dict(ticker=t, date=d, price=round(price, 2),
                         bvps=round(bvps, 2), pb=round(pb, 2),
                         ships=sum(fl.values()), avg_age=age,
                         fleet_usd_m=round(fleet_mid), net_debt=round(nd),
                         navps=round(navps, 2),
                         pnav_lo=round(price / navps_hi, 2),
                         pnav_hi=round(price / navps_lo, 2),
                         pnav=round(pnav, 2)))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA, "corrected_pb_pnav.csv"), index=False)

# ================================================================ verdict
print("\n" + "=" * 98)
print("3) ⭐ THE VERDICT — and it is NOT what the contaminated series said")
print("=" * 98)
for t in ["DHT", "FRO"]:
    d = df[df["ticker"] == t]
    now, prior = d.iloc[-1], d.iloc[:-1]
    print(f"\n  ── {t} ──")
    print(f"  {'cycle top':<13}{'P/B':>8}{'P/NAV':>8}   {'P/NAV range':>16}")
    for _, r in d.iterrows():
        tag = "  <-- TODAY" if r["date"] == "2026-09-18" else ""
        print(f"  {r['date']:<13}{r['pb']:>8.2f}{r['pnav']:>8.2f}   "
              f"{f'{r[chr(112)+chr(110)+chr(97)+chr(118)+chr(95)+chr(108)+chr(111)]:.2f}-{r[chr(112)+chr(110)+chr(97)+chr(118)+chr(95)+chr(104)+chr(105)]:.2f}':>16}{tag}")
    print(f"\n     P/B   today {now['pb']:.2f}x vs prior tops "
          f"{prior['pb'].min():.2f}-{prior['pb'].max():.2f}x  "
          f"-> {now['pb']/prior['pb'].max():.2f}x the prior peak")
    print(f"     P/NAV today {now['pnav']:.2f}x vs prior tops "
          f"{prior['pnav'].min():.2f}-{prior['pnav'].max():.2f}x  "
          f"-> {now['pnav']/prior['pnav'].max():.2f}x the prior peak")

# ================================================================ sensitivity
print("\n" + "-" * 98)
print("4) SENSITIVITY — the fleet-age haircut is the weakest input")
print("-" * 98)
print(f"  {'':<6}{'date':<13}" + "".join(f"{f'age {a}y':>9}" for a in [5, 8, 11, 14]))
sens = []
for t in ["DHT", "FRO"]:
    for d, fl in FLEET[t].items():
        ts = pd.Timestamp(d)
        b = BS[t][BS[t].index <= ts].tail(1).iloc[0]
        sh, nd = b["shares-outstanding"], b["long-term-debt"] - b["cash-on-hand"]
        price = float(PX[t].loc[:d].iloc[-1]) if ts <= PX[t].index[-1] \
            else float(PX[t].iloc[-1])
        line, rec = f"  {t:<6}{d:<13}", dict(ticker=t, date=d)
        for a in [5, 8, 11, 14]:
            h = max(0.25, 1 - AGE_DECAY * max(0, a - 5))
            v = np.mean(VLCC_5YR[d]) * fl.get("vlcc", 0)
            if fl.get("suez"):
                v += np.mean(SUEZ_5YR[d]) * fl["suez"]
            if fl.get("lr2"):
                v += np.mean(LR2_5YR[d]) * fl["lr2"]
            pn = price / ((v * h - nd) / sh)
            line += f"{pn:>9.2f}"
            rec[f"age{a}"] = round(pn, 2)
        print(line)
        sens.append(rec)
pd.DataFrame(sens).to_csv(os.path.join(DATA, "pnav_age_sensitivity.csv"), index=False)

# ================================================================ chart
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

ax = axes[0]
x = np.arange(len(PUBLISHED))
labs = [f"{t}\n{d[:7]}" for (t, d) in PUBLISHED]
ax.bar(x - .2, [v for v in PUBLISHED.values()], .4, color="#95a5a6",
       label="published (contaminated)")
ax.bar(x + .2, [c["actual_pb"] for c in corr], .4, color="#c0392b",
       label="ACTUAL (raw price / reported book)")
for xi, v in zip(x - .2, PUBLISHED.values()):
    ax.text(xi, v + .03, f"{v:.2f}", ha="center", fontsize=8)
for xi, v in zip(x + .2, [c["actual_pb"] for c in corr]):
    ax.text(xi, v + .03, f"{v:.2f}", ha="center", fontsize=8, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=8)
ax.set_ylabel("P/B (x)")
ax.set_title("A. THE CORRECTION\ndividend-adjusted prices understated every past P/B",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=8); ax.grid(axis="y", alpha=.25)

for i, t in enumerate(["DHT", "FRO"]):
    ax = axes[i + 1]
    d = df[df["ticker"] == t]
    x = np.arange(len(d))
    ax.bar(x - .2, d["pb"], .4, color="#7f8c8d", label="P/B (depreciated cost)")
    ax.bar(x + .2, d["pnav"], .4, color="#c0392b", label="P/NAV (market value)")
    for xi, v in zip(x - .2, d["pb"]):
        ax.text(xi, v + .03, f"{v:.2f}", ha="center", fontsize=8.5, fontweight="bold")
    for xi, v in zip(x + .2, d["pnav"]):
        ax.text(xi, v + .03, f"{v:.2f}", ha="center", fontsize=8.5, fontweight="bold")
    ax.axhline(1.0, color="#27ae60", ls="--", lw=1.6)
    ax.set_xticks(x); ax.set_xticklabels([r["date"][:7] for _, r in d.iterrows()],
                                         fontsize=9)
    ax.set_ylabel("multiple (x)")
    ax.set_title(f"{'BC'[i]}. {t} — P/B vs P/NAV at each cycle top\n"
                 "green = 1.0x NAV", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8.5); ax.grid(axis="y", alpha=.25)

fig.suptitle("Valuing the fleet at SECOND-HAND replacement cost — corrected for the "
             "dividend-adjustment error",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .92])
p = os.path.join(CHARTS, "pnav_corrected.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

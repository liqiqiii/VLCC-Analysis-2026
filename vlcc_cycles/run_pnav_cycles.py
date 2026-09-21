# -*- coding: utf-8 -*-
"""
Price-to-NAV at every VLCC cycle top, using SECOND-HAND VESSEL VALUES.

The user, 20 Sep 2026:
    "那帮我按照船队重置成本进行估值；就按照每个周期顶峰的卖相似年份二手船价格。"

This closes the gap flagged at the end of section 14: the P/B series says today
is the most expensive moment in twenty years, but P/B uses DEPRECIATED
HISTORICAL COST. Valuing the fleet at the SECOND-HAND MARKET PRICE OF A
SIMILAR-AGE SHIP at each cycle top is the correct like-for-like test, because
it re-prices the denominator in every period instead of only the current one.

    NAV        = (vessels x second-hand value of a similar-age ship) - net debt
    NAV/share  = NAV / shares outstanding
    P/NAV      = share price / NAV per share

WHY THIS IS THE DECISIVE TEST
P/B compares price to what the ships COST. P/NAV compares price to what the
ships are WORTH. In a market where a 5-year-old VLCC (US$174.5m) is worth more
than a newbuilding (US$129.5m), those two questions have very different answers.

*** HONESTY NOTES ***
1. Vessel values are BROKER/PRESS RANGES, not a paid Clarksons feed. Every one
   is carried as a LOW/HIGH band and the output shows P/NAV at BOTH ends.
2. FRO's 2015 data is NOT comparable: the Frontline / Frontline 2012 merger
   and share consolidation completed in late 2015. The balance sheet shows
   1,158m shares and US$0.70 BVPS in Jun-2015 versus 120m shares and US$12.05
   in Dec-2015. That entity is not continuous and is excluded.
3. Fleet counts are point-in-time and vessels are NOT all the benchmark age.
   A fleet of 15-year-old ships is worth far less than the 5-year-old
   benchmark. This is the single biggest weakness and is handled explicitly
   with an age-haircut sensitivity.
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

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")

# ---------------------------------------------------------------- inputs
# 5-YEAR-OLD VLCC SECOND-HAND VALUE, US$m. Broker/press ranges - see honesty
# note 1. Sources named in the report.
VLCC_5YR = {
    "2007-12-31": (155, 165),   # 2008 super-cycle; NB was ~165-170
    "2015-12-31": (70, 80),     # post-oil-collapse spike year
    "2020-12-31": (68, 72),     # COVID storage pulse; values did NOT follow rates
    "2023-12-31": (98, 113),    # post-Ukraine re-rating
    "2026-09-18": (170, 179),   # today; central 174.5
}
# Suezmax and LR2 5-yr-old values, needed for FRO's mixed fleet (US$m).
SUEZ_5YR = {"2020-12-31": (45, 50), "2023-12-31": (72, 80), "2026-09-18": (115, 125)}
LR2_5YR = {"2020-12-31": (38, 43), "2023-12-31": (60, 68), "2026-09-18": (95, 105)}

# Fleet counts at each date (OWNED vessels). Sourced in the report.
FLEET = {
    "DHT": {
        "2015-12-31": dict(vlcc=14),
        "2020-12-31": dict(vlcc=27),
        "2023-12-31": dict(vlcc=24),
        "2026-09-18": dict(vlcc=24),
    },
    "FRO": {
        # 2015 EXCLUDED - merger/consolidation discontinuity (honesty note 2)
        "2020-12-31": dict(vlcc=21, suez=27, lr2=20),
        "2023-12-31": dict(vlcc=22, suez=25, lr2=18),
        "2026-09-18": dict(vlcc=42, suez=21, lr2=18),
    },
}

# Average fleet age at each date -> haircut vs the 5-year-old benchmark.
# A VLCC loses roughly 5-6% of value per year of age beyond the benchmark.
# These ages are ESTIMATES and are stress-tested below.
AVG_AGE = {
    "DHT": {"2015-12-31": 7, "2020-12-31": 8, "2023-12-31": 10, "2026-09-18": 11},
    "FRO": {"2020-12-31": 5, "2023-12-31": 6, "2026-09-18": 7},
}
AGE_DECAY = 0.055      # value lost per year of age beyond 5


def load(t):
    pb = pd.read_csv(os.path.join(DATA, f"pb_history_{t}.csv"), parse_dates=["date"])
    bs = pd.read_csv(os.path.join(DATA, f"bs_history_{t}.csv"), index_col=0,
                     parse_dates=True)
    return pb, bs


print("=" * 96)
print("PRICE-to-NAV AT EVERY CYCLE TOP — fleet valued at SECOND-HAND MARKET PRICES")
print("=" * 96)
print("\n  NAV = (vessels x second-hand value of a similar-age ship) - net debt")
print("  P/NAV = share price / (NAV / shares)")

DATA_OK = {}
for t in ["DHT", "FRO"]:
    try:
        DATA_OK[t] = load(t)
        print(f"  loaded {t}")
    except Exception as exc:
        print(f"  {t}: LOAD FAILED — {exc}  (run run_historical_pb.py first)")

rows = []
for t, (pb, bs) in DATA_OK.items():
    print("\n" + "-" * 96)
    print(f"  ── {t} ──")
    print(f"  {'date':<13}{'ships':>7}{'age':>5}{'fleet US$m':>13}{'net debt':>10}"
          f"{'NAVPS':>9}{'price':>8}{'P/NAV':>8}{'P/B':>7}")
    for dt, fl in FLEET[t].items():
        ts = pd.Timestamp(dt)
        # price and book from the P/B series (the last row is the live point)
        r = pb[pb["date"] == ts]
        if len(r) == 0:
            r = pb[pb["date"] <= ts].tail(1)
        if len(r) == 0:
            print(f"  {dt:<13} no price row")
            continue
        price = float(r["price"].iloc[0])
        pbv = float(r["pb"].iloc[0])

        # balance sheet: nearest quarter on or before
        b = bs[bs.index <= ts].tail(1)
        if len(b) == 0:
            print(f"  {dt:<13} no balance-sheet row")
            continue
        b = b.iloc[0]
        shares = float(b["shares-outstanding"])
        net_debt = float(b["long-term-debt"]) - float(b["cash-on-hand"])

        age = AVG_AGE[t][dt]
        hair = max(0.25, 1 - AGE_DECAY * max(0, age - 5))

        out = {}
        for side, idx in [("lo", 0), ("hi", 1)]:
            v = VLCC_5YR[dt][idx] * fl.get("vlcc", 0)
            if fl.get("suez"):
                v += SUEZ_5YR.get(dt, (0, 0))[idx] * fl["suez"]
            if fl.get("lr2"):
                v += LR2_5YR.get(dt, (0, 0))[idx] * fl["lr2"]
            v *= hair
            nav = v - net_debt
            out[side] = dict(fleet=v, nav=nav, navps=nav / shares,
                             pnav=price / (nav / shares) if nav > 0 else np.nan)

        mid_navps = (out["lo"]["navps"] + out["hi"]["navps"]) / 2
        mid_pnav = price / mid_navps if mid_navps > 0 else np.nan
        nships = sum(fl.values())
        print(f"  {dt:<13}{nships:>7}{age:>5}"
              f"{(out['lo']['fleet']+out['hi']['fleet'])/2:>13,.0f}{net_debt:>10,.0f}"
              f"{mid_navps:>9.2f}{price:>8.2f}{mid_pnav:>8.2f}{pbv:>7.2f}")
        rows.append(dict(ticker=t, date=dt, ships=nships, avg_age=age,
                         age_haircut=round(hair, 3),
                         fleet_lo=round(out["lo"]["fleet"]),
                         fleet_hi=round(out["hi"]["fleet"]),
                         net_debt=round(net_debt), shares=round(shares),
                         navps_lo=round(out["lo"]["navps"], 2),
                         navps_hi=round(out["hi"]["navps"], 2),
                         navps_mid=round(mid_navps, 2), price=round(price, 2),
                         pnav_lo=round(out["hi"]["pnav"], 2),   # hi value -> lo P/NAV
                         pnav_hi=round(out["lo"]["pnav"], 2),
                         pnav_mid=round(mid_pnav, 2), pb=round(pbv, 2)))

df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA, "pnav_cycle_tops.csv"), index=False)

# ================================================================ the answer
print("\n" + "=" * 96)
print("THE ANSWER — P/B said one thing. What does P/NAV say?")
print("=" * 96)
for t in DATA_OK:
    d = df[df["ticker"] == t]
    if len(d) == 0:
        continue
    print(f"\n  ── {t} ──")
    print(f"  {'cycle top':<13}{'P/B':>7}{'P/NAV (low-high)':>22}{'P/NAV mid':>11}")
    for _, r in d.iterrows():
        print(f"  {r['date']:<13}{r['pb']:>7.2f}"
              f"{f'{r[chr(112)+chr(110)+chr(97)+chr(118)+chr(95)+chr(108)+chr(111)]:.2f} – {r[chr(112)+chr(110)+chr(97)+chr(118)+chr(95)+chr(104)+chr(105)]:.2f}':>22}"
              f"{r['pnav_mid']:>11.2f}")
    now = d.iloc[-1]
    prior = d.iloc[:-1]
    if len(prior):
        print(f"\n     today P/NAV {now['pnav_mid']:.2f}x vs prior cycle tops "
              f"{prior['pnav_mid'].min():.2f}–{prior['pnav_mid'].max():.2f}x")
        print(f"     today P/B   {now['pb']:.2f}x vs prior cycle tops "
              f"{prior['pb'].min():.2f}–{prior['pb'].max():.2f}x")

# ================================================================ sensitivity
print("\n" + "-" * 96)
print("SENSITIVITY — the age haircut is the weakest input. Stress it.")
print("-" * 96)
print(f"  {'':<6}{'date':<13}" + "".join(f"{f'age {a}y':>10}" for a in [5, 8, 11, 14]))
sens = []
for t, (pb, bs) in DATA_OK.items():
    for dt, fl in FLEET[t].items():
        ts = pd.Timestamp(dt)
        r = pb[pb["date"] == ts]
        if len(r) == 0:
            r = pb[pb["date"] <= ts].tail(1)
        price = float(r["price"].iloc[0])
        b = bs[bs.index <= ts].tail(1).iloc[0]
        shares = float(b["shares-outstanding"])
        nd = float(b["long-term-debt"]) - float(b["cash-on-hand"])
        line = f"  {t:<6}{dt:<13}"
        rec = dict(ticker=t, date=dt)
        for a in [5, 8, 11, 14]:
            h = max(0.25, 1 - AGE_DECAY * max(0, a - 5))
            v = np.mean(VLCC_5YR[dt]) * fl.get("vlcc", 0)
            if fl.get("suez"):
                v += np.mean(SUEZ_5YR.get(dt, (0, 0))) * fl["suez"]
            if fl.get("lr2"):
                v += np.mean(LR2_5YR.get(dt, (0, 0))) * fl["lr2"]
            nav = v * h - nd
            pn = price / (nav / shares) if nav > 0 else np.nan
            line += f"{pn:>10.2f}" if pn == pn else f"{'n/m':>10}"
            rec[f"age{a}"] = round(pn, 2) if pn == pn else None
        print(line)
        sens.append(rec)
pd.DataFrame(sens).to_csv(os.path.join(DATA, "pnav_age_sensitivity.csv"), index=False)
print("\n  >> Older assumed age -> smaller NAV -> HIGHER P/NAV. If today's fleets")
print("     are older than assumed, today looks even more expensive, not less.")

# ================================================================ chart
fig, axes = plt.subplots(1, 2, figsize=(16, 6.2))

ax = axes[0]
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    d = df[df["ticker"] == t]
    if len(d) == 0:
        continue
    x = np.arange(len(d))
    ax.plot(x, d["pnav_mid"], "o-", color=c, lw=2.4, ms=8, label=f"{t} P/NAV")
    ax.fill_between(x, d["pnav_lo"], d["pnav_hi"], color=c, alpha=.18)
    for xi, (_, r) in zip(x, d.iterrows()):
        ax.text(xi, r["pnav_mid"] + .06, f"{r['pnav_mid']:.2f}", ha="center",
                fontsize=8.5, fontweight="bold", color=c)
lbl = list(FLEET["DHT"].keys())
ax.set_xticks(np.arange(len(lbl)))
ax.set_xticklabels([l[:7] for l in lbl], fontsize=9)
ax.axhline(1.0, color="#27ae60", ls="--", lw=1.8)
ax.text(0, 1.03, "1.0x NAV = fleet worth what the market pays", fontsize=8,
        color="#1e8449", fontweight="bold")
ax.set_ylabel("price / NAV (x)")
ax.set_title("A. P/NAV at each cycle top\nfleet valued at similar-age SECOND-HAND prices; band = value range",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(alpha=.25)

ax = axes[1]
d = df[df["ticker"] == "DHT"]
x = np.arange(len(d))
ax.bar(x - .2, d["pb"], .4, color="#7f8c8d", label="P/B (depreciated cost)")
ax.bar(x + .2, d["pnav_mid"], .4, color="#c0392b", label="P/NAV (market value)")
for xi, v in zip(x - .2, d["pb"]):
    ax.text(xi, v + .04, f"{v:.2f}", ha="center", fontsize=8.5, fontweight="bold")
for xi, v in zip(x + .2, d["pnav_mid"]):
    ax.text(xi, v + .04, f"{v:.2f}", ha="center", fontsize=8.5, fontweight="bold")
ax.axhline(1.0, color="#27ae60", ls="--", lw=1.6)
ax.set_xticks(x)
ax.set_xticklabels([r["date"][:7] for _, r in d.iterrows()], fontsize=9)
ax.set_ylabel("multiple (x)")
ax.set_title("B. DHT — the two measures disagree, and the gap IS the story\n"
             "P/B rises because book is stale; P/NAV re-prices the denominator",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=.25)

fig.suptitle("Valuing the fleet at REPLACEMENT / SECOND-HAND cost, cycle top by cycle top",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .92])
p = os.path.join(CHARTS, "pnav_cycle_tops.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

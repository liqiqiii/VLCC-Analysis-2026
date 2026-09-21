# -*- coding: utf-8 -*-
"""
"If BWET explains only 10% of DHT's daily variance, why do their PATHS look
almost perfectly correlated?"

There are TWO answers, and only one of them is an illusion.

 (1) THE ILLUSION. Correlation of PRICE LEVELS between two trending series is
     near 1 almost regardless of any real relationship. This is the classic
     spurious-regression problem (Granger & Newbold 1974). Demonstrated below
     with a simulation of INDEPENDENT random walks: they routinely show level
     correlations above 0.9 while having, by construction, zero relationship.

 (2) THE REAL PART. A low DAILY R^2 does NOT imply a low LONG-HORIZON R^2.
     The common component accumulates linearly with horizon while independent
     noise accumulates only with the square root of horizon, so the signal
     ratio rises. This is genuine, not an artefact -- and it is why the
     economic link is stronger than the daily number suggests.

Measured separately for BWET~DHT and BWET~FRO.
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


def s(t):
    d = yf.download(t, period="max", progress=False, auto_adjust=False)["Adj Close"]
    return (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna().rename(t)


tr = pd.concat([s(t) for t in ["BWET", "DHT", "FRO"]], axis=1).dropna()
ret = tr.pct_change().dropna()
print("=" * 98)
print("WHY DO THE PATHS LOOK CORRELATED IF DAILY R^2 IS ONLY 0.10?")
print("=" * 98)

# ══════════════════════════ 1) levels vs returns ══════════════════════════════
print("\n" + "-" * 98)
print("1) THE ANSWER IN ONE TABLE — levels and returns are different questions")
print("-" * 98)
print(f"  {'':<6}{'corr of LEVELS':>17}{'corr of LOG levels':>21}"
      f"{'corr of RETURNS':>18}{'R^2 of returns':>17}")
rows = []
for t in ["DHT", "FRO"]:
    cl = tr["BWET"].corr(tr[t])
    clg = np.log(tr["BWET"]).corr(np.log(tr[t]))
    cr = ret["BWET"].corr(ret[t])
    print(f"  {t:<6}{cl:>17.3f}{clg:>21.3f}{cr:>18.3f}{cr**2:>17.3f}")
    rows.append(dict(ticker=t, corr_levels=round(cl, 3), corr_log_levels=round(clg, 3),
                     corr_returns=round(cr, 3), r2_returns=round(cr ** 2, 3)))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "s22_levels_vs_returns.csv"), index=False)
print("\n  >> The eye reads the LEFT column. The economics live in the RIGHT one.")
print("     A chart of two rising lines shows you the left column.")

# ══════════════════════════ 2) the illusion, proved ═══════════════════════════
print("\n" + "-" * 98)
print("2) PROOF THAT THE LEFT COLUMN IS MOSTLY AN ILLUSION")
print("-" * 98)
print("  Simulate pairs of INDEPENDENT random walks with drift, matched to the")
print("  actual samples' length, drift and volatility. By construction their")
print("  true relationship is ZERO. What level correlation do they show?\n")
rng = np.random.default_rng(42)
n = len(ret)
sim = []
for t in ["DHT", "FRO"]:
    mu_b, sd_b = ret["BWET"].mean(), ret["BWET"].std()
    mu_e, sd_e = ret[t].mean(), ret[t].std()
    lv, rv = [], []
    for _ in range(2000):
        a = np.cumprod(1 + rng.normal(mu_b, sd_b, n))
        b = np.cumprod(1 + rng.normal(mu_e, sd_e, n))
        lv.append(np.corrcoef(a, b)[0, 1])
        rv.append(np.corrcoef(np.diff(a) / a[:-1], np.diff(b) / b[:-1])[0, 1])
    lv, rv = np.array(lv), np.array(rv)
    print(f"  vs {t}: INDEPENDENT series, true relationship = 0")
    print(f"     corr of LEVELS  : mean {lv.mean():+.3f}   "
          f"|corr|>0.8 in {(np.abs(lv) > .8).mean()*100:.0f}% of trials")
    print(f"     corr of RETURNS : mean {rv.mean():+.3f}   "
          f"|corr|>0.8 in {(np.abs(rv) > .8).mean()*100:.0f}% of trials")
    print(f"     ACTUAL levels corr was {tr['BWET'].corr(tr[t]):+.3f}\n")
    sim.append(dict(ticker=t, sim_level_corr_mean=round(lv.mean(), 3),
                    sim_level_gt08_pct=round((np.abs(lv) > .8).mean() * 100),
                    sim_return_corr_mean=round(rv.mean(), 3),
                    actual_level_corr=round(tr["BWET"].corr(tr[t]), 3)))
pd.DataFrame(sim).to_csv(os.path.join(DATA, "s22_spurious_sim.csv"), index=False)
print("  >> Two unrelated series that both drift upward will LOOK correlated.")
print("     That is why level correlation cannot be used as evidence, and why")
print("     every correlation in this report is computed on RETURNS.")

# ══════════════════════════ 3) the REAL horizon effect ════════════════════════
print("-" * 98)
print("3) ⭐ BUT PART OF IT IS REAL — the horizon effect")
print("-" * 98)
print("  A shared component grows with horizon h; independent noise grows with")
print("  sqrt(h). So the explained share should RISE with horizon. Measured on")
print("  non-overlapping windows (overlapping windows would inflate this):\n")
print(f"  {'horizon':<14}{'n':>6}{'BWET~DHT r':>13}{'R^2':>8}"
      f"{'BWET~FRO r':>14}{'R^2':>8}")
hz = []
for lbl, h in [("1 day", 1), ("1 week (5d)", 5), ("1 month (21d)", 21),
               ("1 quarter (63d)", 63), ("6 months (126d)", 126)]:
    lg = np.log1p(ret)
    agg = lg.groupby(np.arange(len(lg)) // h).sum()
    agg = agg.iloc[:-1] if len(lg) % h else agg      # drop partial final window
    if len(agg) < 8:
        continue
    c1 = agg["BWET"].corr(agg["DHT"])
    c2 = agg["BWET"].corr(agg["FRO"])
    print(f"  {lbl:<14}{len(agg):>6}{c1:>13.3f}{c1**2:>8.3f}{c2:>14.3f}{c2**2:>8.3f}")
    hz.append(dict(horizon=lbl, n=len(agg), r_dht=round(c1, 3),
                   r2_dht=round(c1 ** 2, 3), r_fro=round(c2, 3),
                   r2_fro=round(c2 ** 2, 3)))
pd.DataFrame(hz).to_csv(os.path.join(DATA, "s22_horizon.csv"), index=False)
print("\n  ⚠️ The long-horizon cells have very few observations, so treat them as")
print("     indicative only. But the DIRECTION is the economically meaningful")
print("     point: daily noise partly cancels, the freight link partly persists.")

# ══════════════════════════ 4) what the eye is doing ══════════════════════════
print("\n" + "-" * 98)
print("4) AND THE PATHS DO NOT ACTUALLY MATCH — the chart says so if you read it")
print("-" * 98)
W = tr.iloc[-1] / tr.iloc[0]
print(f"  {'':<6}{'total growth':>15}{'US$100 became':>17}")
for t in ["BWET", "DHT", "FRO"]:
    print(f"  {t:<6}{float(W[t]):>14.1f}x{100*float(W[t]):>17,.0f}")
print(f"\n  >> BWET grew {float(W['BWET'])/float(W['DHT']):.1f}x more than DHT and "
      f"{float(W['BWET'])/float(W['FRO']):.1f}x more than FRO.")
print("     On a log/symlog axis that enormous gap is visually compressed into")
print("     'three lines that go up together'. The similarity is the AXIS, not")
print("     the data.")
print("\nDone.")

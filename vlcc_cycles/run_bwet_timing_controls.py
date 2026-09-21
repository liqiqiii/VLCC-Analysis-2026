# -*- coding: utf-8 -*-
"""
The daily test found a SIGNIFICANT next-day effect. Before believing it, rule
out the three ways this is normally an artefact:

  1. It is just the EQUITY'S OWN lag-1 autocorrelation, with BWET proxying it.
  2. It is STALE PRICING / non-synchronous closes in a thinly traded ETF --
     BWET's close may embed information the equity close has not yet absorbed,
     which looks like prediction but is not tradeable.
  3. It only exists in the 2026 crisis and is one-regime noise.

Plus the practical killer: TRANSACTION COSTS on a signal that trades often.
"""

import io
import os
import sys
from math import erfc

import numpy as np
import pandas as pd
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def col(df, c):
    return (df[c].iloc[:, 0] if hasattr(df[c], "columns") else df[c]).dropna()


raw = {t: yf.download(t, period="max", progress=False, auto_adjust=False)
       for t in ["BWET", "DHT", "FRO"]}
tr = pd.concat([col(raw[t], "Adj Close").rename(t) for t in raw], axis=1).dropna()
vol = pd.concat([col(raw[t], "Volume").rename(t) for t in raw], axis=1).dropna()
ret = tr.pct_change().dropna()
print("=" * 98)
print("IS THE NEXT-DAY EFFECT REAL, OR AN ARTEFACT?")
print("=" * 98)

# ---------- 0. liquidity: is BWET thin enough to have stale prices? ----------
print("\n0) LIQUIDITY — stale pricing is the classic source of a fake lead")
dollar = (vol * tr.reindex(vol.index)).dropna()
print(f"  {'':<6}{'median shares/day':>20}{'median US$/day':>18}")
for t in ["BWET", "DHT", "FRO"]:
    print(f"  {t:<6}{vol[t].median():>20,.0f}{dollar[t].median():>18,.0f}")
print("  >> If BWET is thin relative to the equities, its close can lag or lead")
print("     mechanically. Judge the tests below with that in mind.")

# ---------- 1. does BWET survive controlling for the equity's OWN lag? -------
print("\n" + "-" * 98)
print("1) ⭐ THE DECISIVE TEST — does BWET add anything BEYOND the equity's own")
print("   lagged return? If not, 'BWET predicts' is just equity momentum.")
print("-" * 98)
print(f"  {'':<6}{'model':<34}{'coef on BWET(t-1)':>19}{'t':>8}{'p':>9}{'R^2':>8}")
rows = []
for t in ["DHT", "FRO"]:
    y = ret[t].iloc[1:]
    xb = ret["BWET"].shift(1).iloc[1:]
    xe = ret[t].shift(1).iloc[1:]
    df = pd.concat([y, xb, xe], axis=1).dropna()
    df.columns = ["y", "b1", "e1"]
    n = len(df)

    def ols(X, yv):
        X = np.column_stack([np.ones(len(X))] + [X[:, i] for i in range(X.shape[1])])
        beta, *_ = np.linalg.lstsq(X, yv, rcond=None)
        resid = yv - X @ beta
        s2 = resid @ resid / (len(yv) - X.shape[1])
        cov = s2 * np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(cov))
        r2 = 1 - resid.var() / yv.var()
        return beta, se, r2

    # univariate: BWET lag only
    b1, se1, r21 = ols(df[["b1"]].values, df["y"].values)
    t1 = b1[1] / se1[1]
    p1 = erfc(abs(t1) / np.sqrt(2))
    print(f"  {t:<6}{'BWET(t-1) only':<34}{b1[1]:>19.4f}{t1:>8.2f}{p1:>9.4f}{r21:>8.4f}")
    # bivariate: add the equity's own lag
    b2, se2, r22 = ols(df[["b1", "e1"]].values, df["y"].values)
    t2 = b2[1] / se2[1]
    p2 = erfc(abs(t2) / np.sqrt(2))
    te = b2[2] / se2[2]
    pe = erfc(abs(te) / np.sqrt(2))
    print(f"  {t:<6}{'+ own lagged return':<34}{b2[1]:>19.4f}{t2:>8.2f}{p2:>9.4f}{r22:>8.4f}")
    print(f"  {'':<6}{'   (own lag coef)':<34}{b2[2]:>19.4f}{te:>8.2f}{pe:>9.4f}")
    verdict = "SURVIVES" if p2 < 0.05 else "DIES once own-lag is controlled"
    print(f"  {'':<6}=> BWET(t-1) {verdict}\n")
    rows.append(dict(ticker=t, coef_uni=round(b1[1], 4), t_uni=round(t1, 2),
                     p_uni=round(p1, 4), coef_bi=round(b2[1], 4), t_bi=round(t2, 2),
                     p_bi=round(p2, 4), own_lag_coef=round(b2[2], 4),
                     own_lag_p=round(pe, 4), verdict=verdict, n=n))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "s22_timing_controls.csv"), index=False)

# ---------- 2. skip-a-day: kills stale-price overlap -------------------------
print("-" * 98)
print("2) SKIP-A-DAY — use BWET at t-2. A genuine lead should survive; a")
print("   stale-price overlap artefact should largely disappear.")
print("-" * 98)
print(f"  {'':<6}{'lag':<8}{'after up':>12}{'after down':>13}{'diff':>10}{'t':>8}{'p':>9}")
for t in ["DHT", "FRO"]:
    for L in [1, 2, 3]:
        up = ret["BWET"].shift(L) > 0
        a, b = ret[t][up].dropna(), ret[t][~up].dropna()
        diff = a.mean() - b.mean()
        se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        ts = diff / se
        p = erfc(abs(ts) / np.sqrt(2))
        print(f"  {t:<6}{f't-{L}':<8}{a.mean()*100:>11.3f}%{b.mean()*100:>12.3f}%"
              f"{diff*100:>9.3f}%{ts:>8.2f}{p:>9.3f}")
    print()

# ---------- 3. subperiod stability -------------------------------------------
print("-" * 98)
print("3) SUBPERIOD — does it exist outside the 2026 crisis?")
print("-" * 98)
SEG = [("2023-05-04", "2024-12-31", "pre-crisis"),
       ("2025-01-01", "2025-12-31", "2025"),
       ("2026-01-01", "2026-12-31", "2026 crisis")]
print(f"  {'':<6}{'period':<14}{'n':>5}{'diff (next-day)':>18}{'t':>8}{'p':>9}")
for t in ["DHT", "FRO"]:
    for a_, b_, lbl in SEG:
        seg = ret.loc[a_:b_]
        up = seg["BWET"].shift(1) > 0
        x, y = seg[t][up].dropna(), seg[t][~up].dropna()
        if len(x) < 30 or len(y) < 30:
            continue
        diff = x.mean() - y.mean()
        se = np.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y))
        ts = diff / se
        p = erfc(abs(ts) / np.sqrt(2))
        print(f"  {t:<6}{lbl:<14}{len(seg):>5}{diff*100:>17.3f}%{ts:>8.2f}{p:>9.3f}"
              f"  {'sig' if p < 0.05 else '-'}")
    print()

# ---------- 4. transaction costs ---------------------------------------------
print("-" * 98)
print("4) TRANSACTION COSTS — the rule trades a lot. What survives?")
print("-" * 98)
print(f"  {'':<6}{'round-trips/yr':>16}{'0 bps':>10}{'10 bps':>10}{'25 bps':>10}"
      f"{'50 bps':>10}{'B&H':>10}")
for t in ["DHT", "FRO"]:
    r = ret[t]
    sig = (ret["BWET"].shift(1) > 0).reindex(r.index).fillna(False)
    trades = sig.astype(int).diff().abs().fillna(0)
    tpy = trades.sum() / (len(r) / 252)
    bh = (1 + r).prod() ** (252 / len(r)) - 1
    cells = ""
    for bps in [0, 10, 25, 50]:
        net = r.where(sig, 0.0) - trades * bps / 10_000
        ann = (1 + net).prod() ** (252 / len(net)) - 1
        cells += f"{ann*100:>9.1f}%"
    print(f"  {t:<6}{tpy:>16.0f}{cells}{bh*100:>9.1f}%")
print("\n  >> Compare each cost column with the buy-and-hold column on the right.")
print("\nDone.")

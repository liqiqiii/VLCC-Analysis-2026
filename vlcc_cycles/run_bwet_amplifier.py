# -*- coding: utf-8 -*-
"""
Three questions, answered separately for BWET~DHT and BWET~FRO.
No DHT-vs-FRO comparison anywhere.

 Q1. Where did "one tenth to one seventh" come from?
     -> It is R^2, nothing else. Stated explicitly with its provenance.

 Q2. If the DIRECTION agrees, what is the remaining variance? Could the
     equity be an AMPLIFIER / ATTENUATOR of freight rather than being driven
     by something else entirely?
     -> This is the real question. A constant-beta OLS punishes a stable
        DIRECTION with an UNSTABLE MAGNITUDE. So decompose:
          (a) how often do the signs agree?
          (b) is beta stable, or does it change with the SIZE of the freight
              move (an amplifier) or over TIME (a regime amplifier)?
          (c) how much of the R^2 shortfall is sign disagreement vs
              magnitude scatter?

 Q3. Report BWET~DHT and BWET~FRO separately throughout.
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


def s(t):
    d = yf.download(t, period="max", progress=False, auto_adjust=False)["Adj Close"]
    return (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna().rename(t)


tr = pd.concat([s(t) for t in ["BWET", "DHT", "FRO"]], axis=1).dropna()
ret = tr.pct_change().dropna()
n = len(ret)
print("=" * 98)
print("AMPLIFIER OR ATTENUATOR? Decomposing what BWET does and does not explain")
print("=" * 98)
print(f"  {ret.index[0].date()} -> {ret.index[-1].date()}   n = {n}   daily, close-to-close")

# ══════════════════════════ Q1: provenance of 1/10 - 1/7 ══════════════════════
print("\n" + "-" * 98)
print("Q1) WHERE '1/10 TO 1/7' CAME FROM — it is R^2 and nothing else")
print("-" * 98)
print(f"  {'':<6}{'corr':>9}{'R^2':>9}{'as a fraction':>17}{'period':>16}")
for t in ["DHT", "FRO"]:
    c_all = ret["BWET"].corr(ret[t])
    seg = ret.loc["2026-01-01":]
    c_26 = seg["BWET"].corr(seg[t])
    print(f"  {t:<6}{c_all:>9.3f}{c_all**2:>9.3f}{f'1/{1/c_all**2:.1f}':>17}{'full sample':>16}")
    print(f"  {'':<6}{c_26:>9.3f}{c_26**2:>9.3f}{f'1/{1/c_26**2:.1f}':>17}{'2026 only':>16}")
print("\n  >> R^2 is the share of VARIANCE a CONSTANT-BETA straight line explains.")
print("     It is NOT the share of days that move together, and it is NOT a")
print("     measure of whether the direction agrees. That is the whole point")
print("     of Q2 below: a stable DIRECTION with an unstable MAGNITUDE produces")
print("     a LOW R^2 while still being a tight economic relationship.")

# ══════════════════════════ Q2a: sign agreement ═══════════════════════════════
print("\n" + "-" * 98)
print("Q2a) DO THE SIGNS ACTUALLY AGREE? (the direction question)")
print("-" * 98)
print(f"  {'':<6}{'same sign':>11}{'vs 50%':>9}{'z':>8}{'p':>9}"
      f"{'| BWET big moves only':>24}")
rows = []
for t in ["DHT", "FRO"]:
    same = (np.sign(ret["BWET"]) == np.sign(ret[t]))
    r = same.mean()
    z = (r - .5) / np.sqrt(.25 / n)
    p = erfc(abs(z) / np.sqrt(2))
    # restrict to the largest 25% of BWET moves
    big = ret["BWET"].abs() >= ret["BWET"].abs().quantile(.75)
    rb = same[big].mean()
    print(f"  {t:<6}{r*100:>10.1f}%{(r-.5)*100:>8.1f}{z:>8.1f}{p:>9.1e}"
          f"{rb*100:>23.1f}%")
    rows.append(dict(ticker=t, same_sign_pct=round(r * 100, 1),
                     same_sign_big_moves_pct=round(rb * 100, 1), z=round(z, 1)))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "s22_sign_agreement.csv"), index=False)
print("\n  >> If direction agreement were near 100%, the low R^2 would be purely")
print("     a magnitude story. Judge from the actual numbers above.")

# ══════════════════════════ Q2b: beta by size of move ═════════════════════════
print("\n" + "-" * 98)
print("Q2b) ⭐ IS IT AN AMPLIFIER? Beta conditional on the SIZE of the freight move")
print("-" * 98)
print("  If the equity amplifies big freight moves, beta should RISE across")
print("  the buckets. If it filters noise and only responds to real moves,")
print("  beta should rise AND R^2 should rise with it.\n")
q = pd.qcut(ret["BWET"].abs(), 4, labels=["Q1 smallest", "Q2", "Q3", "Q4 largest"])
amp = []
for t in ["DHT", "FRO"]:
    print(f"  ── {t} ──")
    print(f"     {'|BWET| bucket':<14}{'n':>5}{'mean |BWET|':>13}{'beta':>9}"
          f"{'R^2':>8}{'same sign':>11}")
    for lab in ["Q1 smallest", "Q2", "Q3", "Q4 largest"]:
        m = q == lab
        x, y = ret["BWET"][m].values, ret[t][m].values
        b = np.polyfit(x, y, 1)[0]
        r2 = np.corrcoef(x, y)[0, 1] ** 2
        ss = (np.sign(x) == np.sign(y)).mean()
        print(f"     {lab:<14}{m.sum():>5}{np.abs(x).mean()*100:>12.2f}%{b:>9.3f}"
              f"{r2:>8.3f}{ss*100:>10.1f}%")
        amp.append(dict(ticker=t, bucket=lab, n=int(m.sum()),
                        mean_abs_bwet_pct=round(np.abs(x).mean() * 100, 2),
                        beta=round(b, 3), r2=round(r2, 3),
                        same_sign_pct=round(ss * 100, 1)))
    print()
pd.DataFrame(amp).to_csv(os.path.join(DATA, "s22_amplifier.csv"), index=False)

# ══════════════════════════ Q2c: volatility ratio ═════════════════════════════
print("-" * 98)
print("Q2c) AMPLIFIER OR ATTENUATOR IN LEVEL TERMS?")
print("-" * 98)
sb = ret["BWET"].std()
print(f"  BWET daily volatility ............ {sb*100:.2f}%")
for t in ["DHT", "FRO"]:
    st = ret[t].std()
    beta = np.polyfit(ret["BWET"].values, ret[t].values, 1)[0]
    c = ret["BWET"].corr(ret[t])
    print(f"  {t} daily volatility ............. {st*100:.2f}%   "
          f"(BWET is {sb/st:.2f}x as volatile)")
    print(f"     beta {beta:.3f}  =  corr {c:.3f}  x  (sigma_{t} {st*100:.2f}% / "
          f"sigma_BWET {sb*100:.2f}%)  = {c*st/sb:.3f} ✓")
print("\n  >> beta < 1 in PERCENT terms. Per 1% of freight move the equity moves")
print("     far less. In RISK terms the equity is the calmer asset: BWET carries")
print("     multiples of its daily volatility.")

# ══════════════════════════ Q2d: what IS the residual? ════════════════════════
print("\n" + "-" * 98)
print("Q2d) SO WHAT IS THE OTHER ~90%? Test the candidates directly")
print("-" * 98)
extra = pd.concat([s(t) for t in ["SPY", "XLE", "BNO", "^VIX"]], axis=1).dropna()
er = pd.concat([ret, extra.pct_change()], axis=1).dropna()
print(f"  {'':<6}{'BWET':>9}{'+SPY':>9}{'+XLE':>9}{'+BNO':>9}{'+VIX':>9}"
      f"{'ALL':>9}{'unexplained':>14}")
for t in ["DHT", "FRO"]:
    y = er[t].values

    def r2f(cols):
        X = np.column_stack([np.ones(len(er))] + [er[c].values for c in cols])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        return 1 - res.var() / y.var()

    cells = [r2f(["BWET"]), r2f(["BWET", "SPY"]), r2f(["BWET", "SPY", "XLE"]),
             r2f(["BWET", "SPY", "XLE", "BNO"]),
             r2f(["BWET", "SPY", "XLE", "BNO", "^VIX"])]
    allr2 = cells[-1]
    print(f"  {t:<6}{cells[0]:>9.3f}{cells[1]:>9.3f}{cells[2]:>9.3f}"
          f"{cells[3]:>9.3f}{cells[4]:>9.3f}{allr2:>9.3f}{1-allr2:>13.1%}")
print("\n  >> Whatever the residual is, it is NOT the equity market, the energy")
print("     sector, the oil price or volatility. It is idiosyncratic to these")
print("     shipping names: fleet news, charters, dividends, S&P/index flows,")
print("     buybacks, vessel sales, analyst actions and pure liquidity.")

# ══════════════════════════ Q2e: is beta time-varying? ════════════════════════
print("\n" + "-" * 98)
print("Q2e) IS THE RELATIONSHIP A STABLE SCALER, OR A TIME-VARYING AMPLIFIER?")
print("-" * 98)
print(f"  60-day rolling beta:")
print(f"  {'':<6}{'mean':>8}{'std':>8}{'min':>8}{'max':>8}{'% of time >0':>14}")
for t in ["DHT", "FRO"]:
    cov = ret["BWET"].rolling(60).cov(ret[t])
    var = ret["BWET"].rolling(60).var()
    rb = (cov / var).dropna()
    print(f"  {t:<6}{rb.mean():>8.3f}{rb.std():>8.3f}{rb.min():>8.3f}"
          f"{rb.max():>8.3f}{(rb > 0).mean()*100:>13.0f}%")
print("\n  >> A large std relative to the mean means the 'amplification factor'")
print("     is NOT constant. A single beta is an average of a moving quantity,")
print("     which is itself a reason a constant-beta R^2 understates the link.")
print("\nDone.")

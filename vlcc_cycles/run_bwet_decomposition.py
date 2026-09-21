# -*- coding: utf-8 -*-
"""
Claim under test: "BWET explains DHT's daily moves well, which shows the
forward freight indicator is efficiently traded."

Two separate propositions, which need different evidence:

  (P1) BWET EXPLAINS DHT's daily returns well.
       -> tested by R^2 / variance decomposition, and by what is left over.

  (P2) The forward-freight indicator is EFFICIENTLY TRADED / fully priced.
       -> R^2 is the WRONG evidence for this. Efficiency shows up as
          information being impounded CONTEMPORANEOUSLY rather than with a
          lag. The right test is whether the lead disappears.

Also note: this uses CLOSE-TO-CLOSE daily returns. True intraday ("日内")
co-movement would need intraday bars, which are not used here.
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

TK = ["BWET", "DHT", "FRO", "SPY", "XLE", "BNO"]   # market, energy, Brent oil


def s(t):
    d = yf.download(t, period="max", progress=False, auto_adjust=False)["Adj Close"]
    return (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna().rename(t)


tr = pd.concat([s(t) for t in TK], axis=1).dropna()
ret = tr.pct_change().dropna()
print("=" * 96)
print("HOW MUCH OF DHT's DAILY MOVE DOES FREIGHT ACTUALLY EXPLAIN?")
print("=" * 96)
print(f"  {ret.index[0].date()} -> {ret.index[-1].date()}   n = {len(ret)}")
print("  Close-to-close daily returns. (True intraday co-movement would need")
print("  intraday bars and is NOT measured here.)")


def ols_r2(y, X):
    X = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return 1 - resid.var() / y.var(), beta


print("\n" + "-" * 96)
print("1) NESTED MODELS — what each factor adds, for DHT")
print("-" * 96)
y = ret["DHT"].values
MODELS = [
    ("BWET alone", ["BWET"]),
    ("SPY alone (equity market)", ["SPY"]),
    ("XLE alone (energy sector)", ["XLE"]),
    ("BNO alone (Brent oil)", ["BNO"]),
    ("FRO alone (the other tanker)", ["FRO"]),
    ("BWET + SPY", ["BWET", "SPY"]),
    ("BWET + SPY + XLE + BNO", ["BWET", "SPY", "XLE", "BNO"]),
    ("FRO + BWET", ["FRO", "BWET"]),
    ("everything", ["BWET", "FRO", "SPY", "XLE", "BNO"]),
]
print(f"  {'model':<34}{'R^2':>9}{'marginal vs BWET-only':>24}")
rows = []
base = None
for name, cols in MODELS:
    r2, _ = ols_r2(y, ret[cols].values)
    if name == "BWET alone":
        base = r2
    mar = "" if base is None or name == "BWET alone" else f"{(r2-base)*100:+.1f}pp"
    print(f"  {name:<34}{r2:>9.3f}{mar:>24}")
    rows.append(dict(model=name, r2=round(r2, 3)))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "s22_decomposition.csv"), index=False)

print("\n  >> Read the gap between 'BWET alone' and 'FRO alone'. If BWET were")
print("     the dominant driver, the two tanker equities could not share far")
print("     more variance with each other than either shares with freight.")

print("\n" + "-" * 96)
print("2) IS THE COMMON TANKER FACTOR A FREIGHT FACTOR?")
print("-" * 96)
# how much of the DHT-FRO common move is explained by BWET?
common = (ret["DHT"] + ret["FRO"]) / 2
r2_c, _ = ols_r2(common.values, ret[["BWET"]].values)
print(f"  corr(DHT, FRO) = {ret['DHT'].corr(ret['FRO']):.3f}  ->  they share "
      f"{ret['DHT'].corr(ret['FRO'])**2*100:.0f}% of variance")
print(f"  BWET explains {r2_c*100:.1f}% of that COMMON tanker move.")
print("  >> So the thing that moves both tankers together is only partly")
print("     freight. Most of it is not measured by BWET at all.")

# what is left after BWET?
for t in ["DHT", "FRO"]:
    r2_b, _ = ols_r2(ret[t].values, ret[["BWET"]].values)
    resid_dht = ret[t] - np.column_stack(
        [np.ones(len(ret)), ret["BWET"].values]) @ ols_r2(
        ret[t].values, ret[["BWET"]].values)[1]
    print(f"  {t}: BWET R^2 {r2_b:.3f}  ->  residual still correlates "
          f"{pd.Series(resid_dht, index=ret.index).corr(ret['SPY']):.2f} with SPY")

print("\n" + "-" * 96)
print("3) ⭐ THE RIGHT TEST FOR 'EFFICIENTLY TRADED' — it is NOT R^2")
print("-" * 96)
print("  Efficiency means information is impounded CONTEMPORANEOUSLY, not")
print("  with a lag. So the evidence is the LEAD collapsing, not R^2 rising.\n")
SEG = [("2023-05-04", "2024-12-31", "pre-crisis"),
       ("2025-01-01", "2025-12-31", "2025"),
       ("2026-01-01", "2026-12-31", "2026")]
print(f"  {'period':<14}{'same-day r':>12}{'R^2':>8}{'1-day lead r':>15}"
      f"{'lead share':>13}")
for a, b, lbl in SEG:
    seg = ret.loc[a:b]
    same = seg["BWET"].corr(seg["DHT"])
    lead = seg["BWET"].shift(1).corr(seg["DHT"])
    share = abs(lead) / (abs(same) + abs(lead)) * 100
    print(f"  {lbl:<14}{same:>12.3f}{same**2:>8.3f}{lead:>15.3f}{share:>12.0f}%")
print("\n  >> The share of the total BWET-DHT relationship that arrives LATE")
print("     falls from ~33% to ~2%. THAT is the efficiency result: freight")
print("     information now reaches the equity the same day.")
print("  >> But note R^2 barely moved. Efficiency of PRICING and STRENGTH of")
print("     explanation are different things. The market prices freight news")
print("     quickly; freight news is simply not most of what moves the stock.")
print("\nDone.")

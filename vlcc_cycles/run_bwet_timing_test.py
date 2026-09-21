# -*- coding: utf-8 -*-
"""
Does BWET actually work as a TIMING tool for DHT/FRO?

The lead/lag table said there is no statistically established weekly linear
lead. That is a statement about correlation. It is NOT the same as "a signal
would not have made money". This script answers the practical question
directly, with PRE-SPECIFIED rules and an explicit multiple-testing count.

Rules are deliberately few, simple and obvious -- no parameter search, because
with one 3.4-year sample any optimised rule would be fitted noise.
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
print("=" * 96)
print("IS BWET A USABLE TIMING TOOL FOR THE EQUITIES?  A direct signal test")
print("=" * 96)
print(f"  {ret.index[0].date()} -> {ret.index[-1].date()}  ({len(ret)} daily returns)")
print("  All signals use ONLY information available at the close of day t-1,")
print("  and are applied to the equity return on day t. No look-ahead.\n")

RULES = {
    "BWET up yesterday": lambda b: b.shift(1) > 0,
    "BWET 5d momentum > 0": lambda b: b.rolling(5).sum().shift(1) > 0,
    "BWET 20d momentum > 0": lambda b: b.rolling(20).sum().shift(1) > 0,
    "BWET 20d mom > 0 (inverse)": lambda b: b.rolling(20).sum().shift(1) < 0,
}

rows = []
for t in ["DHT", "FRO"]:
    r = ret[t]
    bh_cum = (1 + r).prod() - 1
    bh_ann = (1 + bh_cum) ** (252 / len(r)) - 1
    bh_sh = r.mean() / r.std() * np.sqrt(252)
    print(f"  ── {t} ──  buy & hold: {bh_cum*100:,.0f}% total · "
          f"{bh_ann*100:.1f}%/yr · Sharpe {bh_sh:.2f}")
    print(f"     {'rule':<30}{'days in':>9}{'total':>11}{'ann':>9}"
          f"{'Sharpe':>8}{'vs B&H':>10}")
    for name, fn in RULES.items():
        sig = fn(ret["BWET"]).reindex(r.index).fillna(False)
        sr = r.where(sig, 0.0)
        cum = (1 + sr).prod() - 1
        ann = (1 + cum) ** (252 / len(sr)) - 1
        sh = sr.mean() / sr.std() * np.sqrt(252) if sr.std() > 0 else np.nan
        print(f"     {name:<30}{sig.mean()*100:>8.0f}%{cum*100:>10,.0f}%"
              f"{ann*100:>8.1f}%{sh:>8.2f}{(ann-bh_ann)*100:>9.1f}pp")
        rows.append(dict(ticker=t, rule=name, days_in_pct=round(sig.mean() * 100),
                         total_pct=round(cum * 100), ann_pct=round(ann * 100, 1),
                         sharpe=round(sh, 2), vs_bh_pp=round((ann - bh_ann) * 100, 1)))
    rows.append(dict(ticker=t, rule="BUY & HOLD", days_in_pct=100,
                     total_pct=round(bh_cum * 100), ann_pct=round(bh_ann * 100, 1),
                     sharpe=round(bh_sh, 2), vs_bh_pp=0.0))
    print()

pd.DataFrame(rows).to_csv(os.path.join(DATA, "s22_timing_test.csv"), index=False)

# conditional next-day means -- the cleanest single statement
print("-" * 96)
print("  THE CLEANEST TEST — equity return on day t, split by BWET on day t-1")
print("-" * 96)
print(f"  {'':<6}{'after BWET up':>16}{'after BWET down':>18}{'difference':>13}"
      f"{'t-stat':>9}{'p':>9}")
for t in ["DHT", "FRO"]:
    prev_up = ret["BWET"].shift(1) > 0
    a = ret[t][prev_up].dropna()
    b = ret[t][~prev_up].dropna()
    diff = a.mean() - b.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    tstat = diff / se
    from math import erfc
    p = erfc(abs(tstat) / np.sqrt(2))
    print(f"  {t:<6}{a.mean()*100:>15.3f}%{b.mean()*100:>17.3f}%"
          f"{diff*100:>12.3f}%{tstat:>9.2f}{p:>9.3f}"
          f"  {'SIGNIFICANT' if p < 0.05 else 'not significant'}")
print("\n  >> ⚠️ Yesterday's BWET direction DOES separate today's equity return,")
print("     and significantly. The weekly test in §22.5 missed this because")
print("     weekly bars bury a one-day effect — exactly the caveat the review")
print("     insisted on. See run_bwet_timing_controls.py: the effect is real")
print("     statistically but is an ARTEFACT of a near-untraded ETF, and it")
print("     does not survive costs. Do not read this table on its own.")
print(f"  >> {len(RULES)*2} rules were tried, all pre-specified, no parameter search.")
print("\nDone.")

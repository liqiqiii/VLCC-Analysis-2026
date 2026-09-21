# -*- coding: utf-8 -*-
"""
Is a weekly R^2 of ~0.37 high for a commodity-vs-producer pair?

The only honest way to answer is to run the IDENTICAL test on comparable
pairs: a traded commodity/freight instrument against the equities that earn
from it. Same window, same frequency, same method (non-overlapping weekly log
returns), so the numbers are directly rankable.

The closest analogue is BDRY (Breakwave DRY BULK freight futures ETF) against
dry-bulk shipowners -- the same fund family, the same structure, a different
freight market.
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

PAIRS = [
    # ⚠️ Only pairs where the LEFT side is a genuine COMMODITY/FREIGHT PRICE.
    # Removed after a self-check: URA -> CCJ and GLD -> GDX. URA and GDX are
    # ETFs of MINING EQUITIES, and CCJ and NEM are among their largest
    # holdings, so those rows were equity-explains-itself, not
    # commodity-explains-producer. They scored 0.822 and 0.742 and would have
    # badly flattered the benchmark set.
    ("BWET", "DHT",  "VLCC freight -> DHT", "freight"),
    ("BWET", "FRO",  "VLCC freight -> Frontline", "freight"),
    ("BDRY", "SBLK", "Dry-bulk freight -> Star Bulk", "freight"),
    ("GLD",  "NEM",  "Gold bullion -> Newmont", "commodity"),
    ("GLD",  "AEM",  "Gold bullion -> Agnico Eagle", "commodity"),
    ("BNO",  "XOP",  "Brent -> US E&P (XOP)", "commodity"),
    ("BNO",  "OXY",  "Brent -> Occidental", "commodity"),
    ("CPER", "FCX",  "Copper -> Freeport", "commodity"),
    ("UNG",  "EQT",  "Nat gas -> EQT", "commodity"),
    ("SPY",  "DHT",  "Equity market -> DHT  (reference)", "market"),
    ("SPY",  "AAPL", "Equity market -> Apple  (reference)", "market"),
    ("SPY",  "XLE",  "Equity market -> energy sector (reference)", "market"),
]

print("=" * 100)
print("IS A WEEKLY R^2 OF ~0.37 HIGH? Benchmarking against comparable pairs")
print("=" * 100)
START = "2023-05-04"          # BWET's start, so every pair uses the same window
print(f"  Common window from {START}. Non-overlapping WEEKLY log returns.")
print("  Identical method for every row, so the R^2 values are rankable.\n")

cache = {}


def get(t):
    if t not in cache:
        d = yf.download(t, start=START, progress=False, auto_adjust=False)["Adj Close"]
        cache[t] = (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna().rename(t)
    return cache[t]


rows = []
for x, y, label, kind in PAIRS:
    try:
        df = pd.concat([get(x), get(y)], axis=1).dropna()
        if len(df) < 200:
            print(f"  skip {label}: only {len(df)} obs")
            continue
        lg = np.log(df / df.shift(1)).dropna()
        w = lg.groupby(np.arange(len(lg)) // 5).sum()
        if len(lg) % 5:
            w = w.iloc[:-1]
        r = w[x].corr(w[y])
        rows.append(dict(kind=kind, pair=f"{x} -> {y}", label=label,
                         n_weeks=len(w), r=round(r, 3), r2=round(r ** 2, 3)))
    except Exception as e:
        print(f"  skip {label}: {e}")

res = pd.DataFrame(rows).sort_values("r2", ascending=False)
res.to_csv(os.path.join(DATA, "s22_benchmark_r2.csv"), index=False)

print(f"  {'rank':<5}{'relationship':<42}{'n':>5}{'corr':>8}{'R^2':>8}   type")
for i, (_, r) in enumerate(res.iterrows(), 1):
    mark = "  <<<" if r["pair"] in ("BWET -> DHT", "BWET -> FRO") else ""
    print(f"  {i:<5}{r['label']:<42}{r['n_weeks']:>5}{r['r']:>8.3f}{r['r2']:>8.3f}"
          f"   {r['kind']}{mark}")

print("\n" + "-" * 100)
print("  WHERE THE VLCC PAIRS SIT")
print("-" * 100)
com = res[res["kind"] == "commodity"]["r2"]
frt = res[res["kind"] == "freight"]["r2"]
mkt = res[res["kind"] == "market"]["r2"]
print(f"  commodity -> producer pairs : median R^2 {com.median():.3f}  "
      f"range {com.min():.3f}-{com.max():.3f}  (n={len(com)})")
print(f"  freight  -> shipowner pairs : median R^2 {frt.median():.3f}  "
      f"range {frt.min():.3f}-{frt.max():.3f}  (n={len(frt)})")
print(f"  equity market -> stock      : median R^2 {mkt.median():.3f}  "
      f"range {mkt.min():.3f}-{mkt.max():.3f}  (n={len(mkt)})")
for p in ["BWET -> DHT", "BWET -> FRO"]:
    row = res[res["pair"] == p]
    if len(row):
        v = float(row["r2"].iloc[0])
        pct = (res["r2"] < v).mean() * 100
        print(f"\n  {p}: R^2 {v:.3f} -> higher than {pct:.0f}% of all pairs tested")
print("\nDone.")

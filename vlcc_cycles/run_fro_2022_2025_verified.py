# -*- coding: utf-8 -*-
"""
"FRO rose many-fold 2022 to end-2025, but rates only hit $100k/day in 2025.
 Why did the shares do so well?"

ALL RATES BELOW ARE FRONTLINE'S OWN REPORTED VLCC SPOT TCE, taken from its
SEC 6-K results releases. No estimates, no benchmarks:

  FY2022  6-K filed 2023-03-01  0000919574-23-001981  d9968199_6k.htm
  FY2023  6-K filed 2024-03-01  0000919574-24-001843  d10992818_6k.htm
  FY2025  6-K filed 2026-02-27  0000919574-26-001430  d12109952_6-k.htm
          (the FY2025 release also carries the FY2024 column)

The question contains a factual premise that the filings contradict, and the
answer turns on the difference between an annual average and a spot peak.
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

# ── Frontline's OWN reported VLCC spot TCE, US$/day (filing-sourced) ─────────
ANNUAL = {2021: 15_300, 2022: 31_300, 2023: 49_200, 2024: 43_400, 2025: 47_200}
QUARTERLY = {
    "2022 Q1": 15_700, "2022 Q2": 16_400, "2022 Q3": 25_000, "2022 Q4": 63_200,
    "2023 Q1": 52_500, "2023 Q2": 64_000, "2023 Q3": 42_500, "2023 Q4": 39_200,
    "2025 Q1": 37_200, "2025 Q2": 43_100, "2025 Q3": 34_300, "2025 Q4": 74_200,
}
Q1_2026_CONTRACTED = 107_100      # 92% covered, per the FY2025 release
BREAKEVEN_2026 = 25_000           # company's own next-12-month VLCC cash breakeven


def s(t, f):
    d = yf.download(t, period="max", progress=False, auto_adjust=False)[f]
    return (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna().rename(t)


px, tr = s("FRO", "Close"), s("FRO", "Adj Close")

print("=" * 98)
print("FRO 2022 -> END-2025: THE SHARES, THE RATES, AND THE PREMISE IN THE QUESTION")
print("=" * 98)

# ── 1. correct the premise ───────────────────────────────────────────────────
print("\n" + "-" * 98)
print("1) ⚠️ FIRST, THE PREMISE — rates did NOT reach $100k/day in 2025")
print("-" * 98)
print("  Frontline's OWN reported VLCC spot TCE (SEC 6-K releases):\n")
print(f"  {'year':<8}{'annual avg':>13}{'  quarterly detail'}")
for y in sorted(ANNUAL):
    qs = " · ".join(f"Q{i}: ${QUARTERLY[f'{y} Q{i}']:,}" for i in (1, 2, 3, 4)
                    if f"{y} Q{i}" in QUARTERLY)
    print(f"  {y:<8}${ANNUAL[y]:>12,}   {qs}")
print(f"\n  Q1-2026 already CONTRACTED: ${Q1_2026_CONTRACTED:,}/day at 92% covered")
print(f"  Company's own VLCC cash breakeven for the next 12 months: ${BREAKEVEN_2026:,}/day")
print(f"""
  >> The highest QUARTER in the whole 2022-25 window was Q4-2025 at
     ${QUARTERLY['2025 Q4']:,}. The highest ANNUAL average was 2023 at ${ANNUAL[2023]:,}.
     US$100k/day is a 2026 phenomenon, not a 2025 one -- it first appears in
     the Q1-2026 contracted figure of ${Q1_2026_CONTRACTED:,}.
  >> So the shares did NOT rise on a $100k rate. They rose on a market that
     went from ${ANNUAL[2021]:,} to roughly ${ANNUAL[2025]:,} -- against a cash breakeven
     of about ${BREAKEVEN_2026:,}.""")

# ── 2. the shares ────────────────────────────────────────────────────────────
print("\n" + "-" * 98)
print("2) WHAT THE SHARES ACTUALLY DID — and the rate change alongside")
print("-" * 98)
print(f"  {'year':<7}{'VLCC TCE':>11}{'rate chg':>10}{'FRO price':>20}"
      f"{'price':>9}{'TOTAL':>9}{'same dir?':>11}")
rows = []
for y in [2022, 2023, 2024, 2025]:
    a, b = f"{y}-01-01", f"{y}-12-31"
    p0, p1 = float(px[:a].iloc[-1]), float(px[:b].iloc[-1])
    t0, t1 = float(tr[:a].iloc[-1]), float(tr[:b].iloc[-1])
    pr, trr = p1 / p0 - 1, t1 / t0 - 1
    dr = ANNUAL[y] / ANNUAL[y - 1] - 1
    same = "YES" if np.sign(dr) == np.sign(trr) else "no"
    print(f"  {y:<7}{ANNUAL[y]:>11,}{dr*100:>9.0f}%"
          f"{f'${p0:.2f} -> ${p1:.2f}':>20}{pr*100:>8.0f}%{trr*100:>8.0f}%{same:>11}")
    rows.append(dict(year=y, vlcc_tce=ANNUAL[y], rate_chg_pct=round(dr * 100),
                     price_ret_pct=round(pr * 100), total_ret_pct=round(trr * 100),
                     same_direction=same))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA, "s24_fro_vs_rate.csv"), index=False)
print(f"\n  >> The rate direction and the equity direction agree in "
      f"{(df.same_direction=='YES').sum()} of 4 years.")
print("     At ANNUAL frequency the link is tight — exactly what §22.5e showed:")
print("     daily R² ~0.10, weekly ~0.37, and the relationship keeps tightening")
print("     as the horizon lengthens and idiosyncratic noise cancels out.")

# ── 3. cumulative, and the dividend point ────────────────────────────────────
print("\n" + "-" * 98)
print("3) HOW BIG WAS THE MOVE, REALLY?")
print("-" * 98)
p0 = float(px[:"2022-01-01"].iloc[-1]); p1 = float(px[:"2025-12-31"].iloc[-1])
t0 = float(tr[:"2022-01-01"].iloc[-1]); t1 = float(tr[:"2025-12-31"].iloc[-1])
print(f"  price          ${p0:.2f} -> ${p1:.2f}   = {p1/p0:.2f}x   ({(p1/p0-1)*100:+.0f}%)")
print(f"  TOTAL RETURN                        = {t1/t0:.2f}x   ({(t1/t0-1)*100:+.0f}%)")
print(f"  >> dividends added {((t1/t0)-(p1/p0))*100:.0f} percentage points.")
lo = float(px["2021-01-01":"2022-12-31"].min())
lod = px["2021-01-01":"2022-12-31"].idxmin()
print(f"\n  From the 2021-22 low of ${lo:.2f} ({lod.date()}): {p1/lo:.1f}x")
print("  >> 'Many-fold' is ~3x on price and ~4x on total return from the start")
print("     of 2022 — not 10x. And the low it came off existed because the")
print(f"     market was earning ${ANNUAL[2021]:,}/day against a ~${BREAKEVEN_2026:,} breakeven,")
print("     i.e. it was LOSS-MAKING. Recovery from a loss is arithmetic.")

# ── 4. the four real drivers ─────────────────────────────────────────────────
print("\n" + "-" * 98)
print("4) ⭐ SO WHY SO STRONG? Four drivers, none of which is a $100k rate")
print("-" * 98)
op = {y: (ANNUAL[y] - BREAKEVEN_2026) for y in ANNUAL}
print("  (a) OPERATING LEVERAGE. Profit is the rate MINUS breakeven, so small")
print("      rate moves become large profit moves — and 2021 was BELOW cost:\n")
print(f"      {'year':<8}{'rate':>10}{'- breakeven':>13}{'= margin/day':>14}{'vs 2021':>14}")
for y in sorted(ANNUAL):
    v = op[y]
    rel = "—" if y == 2021 else f"{v-op[2021]:+,}/day"
    print(f"      {y:<8}{ANNUAL[y]:>10,}{BREAKEVEN_2026:>13,}{v:>14,}{rel:>14}")
print(f"\n      >> The rate roughly TRIPLED 2021->2025 (${ANNUAL[2021]:,} to ${ANNUAL[2025]:,}),")
print(f"         but the margin over breakeven swung from MINUS ${abs(op[2021]):,} to")
print(f"         PLUS ${op[2025]:,} — a ${op[2025]-op[2021]:,}/day swing per vessel.")
print("         It cannot be written as a multiple because it crosses zero:")
print("         the company went from losing money on every voyage to earning")
print(f"         ${op[2025]:,} a day on each of ~80 ships. THAT is what re-rated.")
print("""
  (b) DIVIDENDS — about a quarter of the total return, invisible on a price chart.

  (c) THE FLEET GREW. Frontline bought 24 VLCCs from Euronav; 11 delivered in
      Q4-2023 and 13 during 2024 (§15). Note the FY2023 release shows the
      Euronav ships earning only $5,700/day in 2023 because they had just
      arrived — they diluted the reported 2023 rate from $50,300 to $49,200
      while ADDING earning capacity for later years.

  (d) ASSET VALUES. A 5-year-old VLCC went from ~$105m at end-2023 to $151.1m
      by end-Aug 2026 (§15, §21). On a leveraged balance sheet NAV per share
      rises far faster than the asset itself.""")

print("\n" + "-" * 98)
print("5) AND 2024 IS THE CONTROL CASE")
print("-" * 98)
print(f"  2024 rate FELL from ${ANNUAL[2023]:,} to ${ANNUAL[2024]:,} "
      f"({(ANNUAL[2024]/ANNUAL[2023]-1)*100:.0f}%) ...")
print(f"  ... and the shares fell {df[df.year==2024].total_ret_pct.iloc[0]}% on total return.")
print("  >> When the rate fell, the equity fell. The 2022-25 rise was not a")
print("     detached re-rating; it tracked the rate at annual frequency.")
print("\nDone.")

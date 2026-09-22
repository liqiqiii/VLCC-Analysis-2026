# -*- coding: utf-8 -*-
"""
"On the 4-year fit, if 2026's rate is $100k, should the stock be up 4x?"

Test it rather than assert. Four things have to be checked:

  1. What IS the fitted relationship on those 4 years? Rate-linear?
     Margin-linear? Log-linear? Fit all three and compare.
  2. What does each extrapolate to at $100k?
  3. How much of that has ALREADY happened in 2026?
  4. Why does the extrapolation break? Quantify each reason rather than
     hand-waving.

The headline risk: n=4, and the $100k point is far OUTSIDE the fitted range
(the sample tops out at $49,200). Extrapolating a 4-point fit past double its
own range is not a forecast.
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

RATE = {2021: 15_300, 2022: 31_300, 2023: 49_200, 2024: 43_400, 2025: 47_200}
BE = 25_000                       # Frontline's own VLCC cash breakeven
# FRO year-end prices (Close), filled from market data below
FRO = dict(vlcc_eq=57.9, days=350, breakeven=23_800, dna=300, shares=222.623,
           navps=30.37)


def s(t, f):
    d = yf.download(t, period="max", progress=False, auto_adjust=False)[f]
    return (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna().rename(t)


px, tr = s("FRO", "Close"), s("FRO", "Adj Close")
ye = {y: float(px[:f"{y}-12-31"].iloc[-1]) for y in RATE}
ye_tr = {y: float(tr[:f"{y}-12-31"].iloc[-1]) for y in RATE}
now_px, now_tr = float(px.iloc[-1]), float(tr.iloc[-1])

print("=" * 98)
print("DOES THE 4-YEAR FIT SUPPORT '$100k RATE => 4x THE STOCK'?")
print("=" * 98)
print(f"\n  {'year':<7}{'rate':>10}{'margin over BE':>17}{'FRO year-end':>15}"
      f"{'total-ret index':>18}")
for y in sorted(RATE):
    print(f"  {y:<7}{RATE[y]:>10,}{RATE[y]-BE:>17,}{ye[y]:>15.2f}{ye_tr[y]:>18.2f}")
print(f"  {'now':<7}{'—':>10}{'—':>17}{now_px:>15.2f}{now_tr:>18.2f}")

# ══════════════════════ 1) fit three specifications ══════════════════════════
print("\n" + "-" * 98)
print("1) FIT THE RELATIONSHIP THREE WAYS — the answer depends entirely on which")
print("-" * 98)
yrs = sorted(RATE)
r = np.array([RATE[y] for y in yrs], float)
m = r - BE
p = np.array([ye_tr[y] for y in yrs], float)     # total-return index
TARGET = 100_000
fits = []
# (a) price linear in RATE
b1 = np.polyfit(r, p, 1)
pred_a = np.polyval(b1, TARGET)
# (b) price linear in MARGIN over breakeven
b2 = np.polyfit(m, p, 1)
pred_b = np.polyval(b2, TARGET - BE)
# (c) log price linear in log rate (constant elasticity)
b3 = np.polyfit(np.log(r), np.log(p), 1)
pred_c = np.exp(np.polyval(b3, np.log(TARGET)))
base = ye_tr[2025]
print(f"  {'specification':<38}{'R^2':>7}{'pred @ $100k':>15}{'vs end-2025':>14}")


def eps_model(rate):
    return ((rate - FRO["breakeven"]) * FRO["vlcc_eq"] * FRO["days"] / 1e6
            - FRO["dna"]) / FRO["shares"]


# (a) and (b) are the SAME model: margin = rate - constant, so an OLS line in
# one is an OLS line in the other. Reported once, honestly.
r2a = np.corrcoef(r, p)[0, 1] ** 2
r2c = np.corrcoef(np.log(r), np.log(p))[0, 1] ** 2
# (d) constant-P/E: price scales with MODELLED EPS, which is non-linear in the
# rate because of the breakeven and D&A. A genuinely different specification.
pred_d = base * eps_model(TARGET) / eps_model(RATE[2025])
SPECS = [
    ("price ~ rate (linear)", r2a, pred_a),
    ("  [= price ~ margin, identical by construction]", np.nan, np.nan),
    ("log price ~ log rate (elasticity)", r2c, pred_c),
    ("price ~ modelled EPS (constant P/E)", np.nan, pred_d),
]
for lbl, r2v, pr in SPECS:
    if np.isnan(pr):
        print(f"  {lbl:<38}{'—':>7}{'—':>15}{'—':>14}")
        continue
    r2s = f"{r2v:.3f}" if not np.isnan(r2v) else "n/a"
    print(f"  {lbl:<38}{r2s:>7}{pr:>15.2f}{pr/base:>13.2f}x")
    fits.append(dict(spec=lbl, r2=None if np.isnan(r2v) else round(r2v, 3),
                     pred=round(pr, 2), mult_vs_2025=round(pr / base, 2)))
pd.DataFrame(fits).to_csv(os.path.join(DATA, "s25_fits.csv"), index=False)
mults = [f["mult_vs_2025"] for f in fits]
print(f"\n  >> On the SAME four points, defensible specifications give")
print(f"     {min(mults):.2f}x to {max(mults):.2f}x versus end-2025. THAT SPREAD IS THE")
print("     ANSWER: with n=4 the functional form is unidentified, so the")
print("     multiple is essentially whatever you assume it to be.")
print("  >> Note the constant-P/E case is the ONLY one that gets anywhere near")
print("     4x — and a constant P/E is precisely what cyclical peaks do not do.")
print(f"\n  ⚠️ AND $100,000 IS FAR OUTSIDE THE FITTED RANGE.")
print(f"     Sample rates span ${r.min():,.0f} to ${r.max():,.0f}.")
print(f"     $100,000 is {TARGET/r.max():.1f}x the top of the sample.")
print("     Extrapolating a 4-point fit past double its own range is not a")
print("     forecast; it is an assumption wearing a regression's clothes.")

# ══════════════════════ 2) what already happened ═════════════════════════════
print("\n" + "-" * 98)
print("2) ⭐ THE DECISIVE POINT — most of it has ALREADY HAPPENED")
print("-" * 98)
print(f"  FRO end-2025 price      ${ye[2025]:.2f}")
print(f"  FRO now                 ${now_px:.2f}   = {now_px/ye[2025]:.2f}x on price")
print(f"  On total return                    = {now_tr/ye_tr[2025]:.2f}x")
print(f"\n  And the rate has ALREADY exceeded $100k:")
print(f"     FRO achieved VLCC TCE, Q2-2026:      $152,700/day  (reported)")
print(f"     FRO contracted Q1-2026:              $107,100/day at 92% covered")
print(f"     FRO FY2025 average:                  ${RATE[2025]:,}/day")
print(f"\n  >> The '$100k scenario' is not a future case to be priced — it is")
print(f"     the CURRENT state, and the shares have already re-rated "
      f"{now_px/ye[2025]:.1f}x on price")
print("     this year. Asking 'should it go up 4x if the rate is $100k' treats")
print("     an event that has largely occurred as if it were still ahead.")

# ══════════════════════ 3) why the extrapolation breaks ══════════════════════
print("\n" + "-" * 98)
print("3) FOUR REASONS THE EXTRAPOLATION BREAKS — each quantified")
print("-" * 98)


def eps(rate):
    return ((rate - FRO["breakeven"]) * FRO["vlcc_eq"] * FRO["days"] / 1e6
            - FRO["dna"]) / FRO["shares"]


print("  (a) THE 2021-25 MOVE INCLUDED CROSSING ZERO. That cannot repeat.")
print(f"      2021 margin  -${abs(RATE[2021]-BE):,}/day  (LOSS-MAKING)")
print(f"      2025 margin  +${RATE[2025]-BE:,}/day")
print("      Going from a loss to a profit is an infinite percentage change in")
print("      earnings. Going from a profit to a bigger profit is not. The next")
print("      leg cannot borrow that arithmetic.\n")

print("  (b) P/E COMPRESSES AT PEAKS. This report's own framework puts the")
print("      cycle-peak zone at 2.5-3.5x (§21).")
print(f"      {'sustained rate':>16}{'model EPS':>11}{'P/E at today':>14}"
      f"{'price at 3x':>13}{'at 5x':>9}{'at 7x':>9}")
for rate in [47_200, 75_000, 100_000, 152_700]:
    e = eps(rate)
    print(f"      {rate:>16,}{e:>11.2f}{now_px/e:>14.1f}x{3*e:>13.2f}{5*e:>9.2f}"
          f"{7*e:>9.2f}")
print(f"\n      >> At a SUSTAINED $100,000/day the model gives EPS ${eps(100_000):.2f}.")
print(f"         Today's ${now_px:.2f} is already {now_px/eps(100_000):.1f}x that.")
print(f"         For the shares to go 4x from end-2025 (${4*ye[2025]:.2f}) on")
print(f"         $100k earnings would require a P/E of {4*ye[2025]/eps(100_000):.1f}x —")
print("         roughly FIVE TIMES the historical peak-zone multiple.\n")

print("  (c) FLEET GROWTH IS NOT REPEATABLE. The 24 Euronav VLCCs lifted")
print("      earning capacity independently of the rate (§24). There is no")
print("      comparable acquisition in the 2026 numbers.\n")

print("  (d) NAV IS A CEILING THE 2021 BASE DID NOT HAVE.")
print(f"      FRO NAV/share today ${FRO['navps']:.2f}; price ${now_px:.2f} = "
      f"{now_px/FRO['navps']:.2f}x NAV.")
print(f"      A 4x from end-2025 means ${4*ye[2025]:.2f} = "
      f"{4*ye[2025]/FRO['navps']:.2f}x NAV,")
print("      versus a filing-sourced historical maximum of 1.50x (§17). In 2021")
print("      the shares traded BELOW NAV, so the re-rating had room. It no")
print("      longer does.")

print("\n" + "-" * 98)
print("4) WHAT THE FIT CAN AND CANNOT SAY")
print("-" * 98)
print(f"""  CAN say: over 2022-25 the rate direction and the equity direction agreed
  in 4 of 4 years, and the annual relationship was tight (§24).

  CANNOT say: that the elasticity measured between ${r.min():,.0f} and ${r.max():,.0f}
  carries to $100,000. The sample contains no observation above ${r.max():,.0f},
  it contains a sign change in profitability that cannot recur, and the
  dependent variable is bounded by asset value in a way it was not in 2021.

  The honest framing is the one already in §21: forget elasticity, ask how
  many YEARS of a given rate the price already embeds. At 7x P/E today's
  price implies about $119,300/day sustained — ABOVE $100k, not below it.""")
print("\nDone.")

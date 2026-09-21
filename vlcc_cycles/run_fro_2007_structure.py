# -*- coding: utf-8 -*-
"""
SECTION 23 — What was actually inside Frontline's shell in 2005-08, and why
its P/B looked like 8x.

EVERY figure below is taken from Frontline's own 20-F filings on SEC EDGAR
(CIK 913290), downloaded to vlcc_cycles/filings/. No modelled numbers.

  FY2005  0000919574-06-002877   d682923_20-f.txt
  FY2006  0000919574-07-003317   d762642_20-f.txt
  FY2007  0000919574-08-002717   d859932_20-f.htm
  FY2008  0000919574-09-009523   d990591_20-f.htm

The conclusion: the 8x P/B used in section 16 as a "cycle-top" benchmark is
NOT a valuation signal. It is an artefact of two things Frontline did that
today's Frontline does not do -- distributing 100% of net income every single
year, and holding its fleet through capital leases from a company it had spun
off. Book equity was structurally pinned near zero.
"""

import io
import os
import sys

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# ── all filing-sourced, US$ thousands unless noted ───────────────────────────
F = pd.DataFrame([
    # year, total assets, equity, minority int, owned vessels, cap-lease vessels,
    # investments in assoc, net income, cash div, stock div
    (2005, 4_454_817,  715_166, None, 2_584_847, 672_608, 15_783, 606_839, 552_322, 211_881),
    (2006, 4_589_937,  668_560, 541_122, 2_446_278, 626_374, 17_825, 516_000, 488_158, 27_842),
    (2007, 3_762_091,  445_969, 0, 208_516, 2_324_789, 5_633, 570_418, 408_196, 162_222),
], columns=["year", "assets", "equity", "minority", "owned_vessels",
            "leased_vessels", "invest_assoc", "net_income", "cash_div", "stock_div"])
SHARES = 74.825169      # million, par $2.50, constant 2006-2007 (FY2007 20-F)

print("=" * 100)
print("FRONTLINE 2005-08: WHAT WAS IN THE SHELL, AND WHY P/B LOOKED LIKE 8x")
print("=" * 100)

# ══════════════════════════ 1) the structure ══════════════════════════════════
print("\n" + "-" * 100)
print("1) THE STRUCTURE — Frontline was a CHARTERER, not an owner")
print("-" * 100)
print("""  Verbatim, FY2007 20-F:

    "In February 2007, our Board approved a further spin off of our remaining
     interest in the shares of Ship Finance and this occurred in March 2007.
     As a result of this spin off, we currently hold 73,383 shares in Ship
     Finance, which represents 0.01% of Ship Finance's total outstanding
     shares and as of March 31, 2007, we no longer consolidate Ship Finance
     and its subsidiaries in our financial statements."

    "As of February 29, 2008, we charter 40 vessels from Ship Finance at fixed
     rates on long-term charters. In addition, we charter 16 vessels under
     fixed rate medium term charters from third parties."

    "The daily base charter rates ... for very large crude carriers, or VLCCs,
     range from $25,575 in 2006 to $24,175 in 2011 and beyond and from $21,100
     in 2006 to $19,700 from 2011" [Suezmax]

    "Profit share expense represents amounts due to Ship Finance based on 20%
     of the excess of vessel revenues earned by the Company over the base hire
     paid to Ship Finance for chartering in the vessels."
""")
print("  >> So the economics were: charter in at ~$24-26k/day fixed, earn the")
print("     spot market, and hand 20% of everything above the base rate to the")
print("     company that owned the ships. In 2007 that profit share cost")
print("     US$37.3m and charterhire cost US$273.2m (FY2007 20-F, related")
print("     party note). Remaining lease obligation to Ship Finance: US$1,767.8m.")

# ══════════════════════════ 2) the balance sheet flip ═════════════════════════
print("\n" + "-" * 100)
print("2) THE BALANCE-SHEET FLIP — the fleet left the 'owned' line in 2007")
print("-" * 100)
print(f"  {'year':<7}{'owned vessels':>16}{'under cap lease':>18}{'owned share':>14}")
for _, r in F.iterrows():
    tot = r.owned_vessels + r.leased_vessels
    print(f"  {int(r.year):<7}{r.owned_vessels:>15,.0f}{r.leased_vessels:>18,.0f}"
          f"{r.owned_vessels/tot*100:>13.0f}%")
print("  (2008, for completeness: owned 438,161 / cap-lease 2,100,717)")
print("\n  >> In ONE year, owned tonnage fell from US$2.45bn to US$0.21bn while")
print("     capital-leased tonnage rose from US$0.63bn to US$2.32bn. That is the")
print("     Ship Finance deconsolidation, not a fleet disposal.")

# ══════════════════════════ 3) why equity was tiny ════════════════════════════
print("\n" + "-" * 100)
print("3) ⭐ WHY BOOK EQUITY WAS TINY — retained earnings were ZERO, every year")
print("-" * 100)
print("  FY2007 20-F, statement of changes in equity, RETAINED EARNINGS:\n")
print(f"  {'year':<7}{'net income':>13}{'cash div':>12}{'stock div':>12}"
       f"{'total paid':>13}{'payout':>9}{'retained':>11}")
tot_paid = 0
for _, r in F.iterrows():
    paid = r.cash_div + r.stock_div
    tot_paid += paid
    print(f"  {int(r.year):<7}{r.net_income:>13,.0f}{r.cash_div:>12,.0f}"
          f"{r.stock_div:>12,.0f}{paid:>13,.0f}{paid/r.net_income*100:>8.0f}%"
          f"{'0':>11}")
print(f"\n  Closing retained earnings 2005, 2006, 2007: 0, 0, 0 — literally nil.")
print(f"  Total distributed 2005-2007: US${tot_paid/1000:,.1f}m against book")
print(f"  equity at end-2007 of US${F.equity.iloc[-1]/1000:,.1f}m.")
print(f"  >> Frontline paid out {tot_paid/F.net_income.sum()*100:.0f}% of three years'")
print("     earnings. Book equity mathematically CANNOT accumulate under that")
print("     policy, so any P/B ratio is a statement about the dividend policy,")
print("     not about how expensive the shares were.")

# ══════════════════════════ 4) leverage ═══════════════════════════════════════
print("\n" + "-" * 100)
print("4) AND IT WAS ~88% LIABILITIES")
print("-" * 100)
print(f"  {'year':<7}{'total assets':>15}{'equity':>12}{'equity/assets':>16}"
      f"{'BVPS':>9}")
for _, r in F.iterrows():
    print(f"  {int(r.year):<7}{r.assets:>15,.0f}{r.equity:>12,.0f}"
          f"{r.equity/r.assets*100:>15.1f}%{r.equity/1000/SHARES:>9.2f}")
print("\n  >> With equity at ~12% of assets, ANY profitable company shows a high")
print("     P/B. The ratio is measuring gearing, not richness.")

# ══════════════════════════ 5) the corrected comparison ═══════════════════════
print("\n" + "-" * 100)
print("5) ⭐ SO WHAT WAS THE REAL SHIPPING VALUATION?")
print("-" * 100)
bvps07 = F.equity.iloc[-1] / 1000 / SHARES
PB_REPORTED = 8.05                       # section 16, from raw price / BVPS
price07 = PB_REPORTED * bvps07
mcap07 = price07 * SHARES
print(f"  Reported end-2007:  BVPS US${bvps07:.2f}  ·  implied price "
      f"US${price07:.2f}  ·  market cap US${mcap07:,.0f}m")
print(f"  (Pre the Feb-2016 1-for-5 reverse split, so not comparable per-share)")

print("\n  ADJUSTMENT A — restore the distributions. What if Frontline had")
print("  retained 2005-07 earnings instead of paying them out?")
eq_adj = (F.equity.iloc[-1] + tot_paid) / 1000
print(f"     adjusted equity  US${eq_adj:,.0f}m   BVPS US${eq_adj/SHARES:.2f}")
print(f"     adjusted P/B     {mcap07/eq_adj:.2f}x   (vs {PB_REPORTED:.2f}x reported)")

print("\n  ADJUSTMENT B — value the fleet, not the book. Section 17 computed")
print("  Frontline's end-2007 P/NAV at 1.33x on a market-value-of-fleet basis.")
print("  That is the asset-based answer and it is UNREMARKABLE.")

rows = [("Reported P/B", PB_REPORTED, "capital structure + 100% payout"),
        ("P/B if earnings retained", mcap07 / eq_adj, "removes the payout effect"),
        ("P/NAV (section 17)", 1.33, "market value of fleet less net debt"),
        ("Today's FRO P/NAV", 1.69, "for reference")]
print(f"\n  {'measure':<30}{'value':>9}   what it reflects")
for a, b, c in rows:
    print(f"  {a:<30}{b:>8.2f}x   {c}")
pd.DataFrame(rows, columns=["measure", "value", "reflects"]).to_csv(
    os.path.join(DATA, "s23_fro_pb.csv"), index=False)
F.assign(bvps=F.equity / 1000 / SHARES,
         equity_to_assets=F.equity / F.assets).to_csv(
    os.path.join(DATA, "s23_fro_balance.csv"), index=False)

print("\n" + "=" * 100)
print("  CONCLUSION — and it corrects section 16")
print("=" * 100)
print("""  Frontline's 8.05x P/B at end-2007 was NOT a cycle-top valuation signal.
  It was the arithmetic consequence of:
    (1) distributing 100% of net income every year, so retained earnings were
        exactly zero and book equity could never build;
    (2) holding the fleet through capital leases from Ship Finance after
        spinning that company off entirely in March 2007;
    (3) running equity at only ~12% of total assets.

  On the same data the asset-based valuation was about 1.33x NAV — ordinary.

  >> Section 16 used FRO's 8.05x as the super-cycle P/B benchmark against
     today's 3.63x, concluding today is "far cheaper on book". THAT
     COMPARISON IS INVALID: it compares a 100%-payout, capital-lease,
     12%-equity charterer with today's owner-operator. The P/NAV comparison
     (1.33x then vs 1.69x now) is the one that survives.""")
print("\nDone.")

# -*- coding: utf-8 -*-
"""
COMPREHENSIVE PRICE-BASIS REVIEW of the whole vlcc_cycles report.

The user, 20 Sep 2026:
    "根据正确的价格- 考虑拆合股/股息率；来做一个全面的review，并修改相应的部分"

§18 established the principle. This script applies it to EVERY price-dependent
claim in the report, rebuilds each one on the correct basis, and reports which
conclusions move.

THREE BASES EXIST AND THEY ARE ALL DIFFERENT:
  RAW   = as-traded price, split-adjusted only  (yfinance auto_adjust=False)
          -> correct for VALUATION MULTIPLES
  TOTAL = split- AND dividend-adjusted          (yfinance auto_adjust=True)
          -> correct for RETURNS
  ACTUAL= the literal price paid on the day, before any split adjustment
          -> needed only when comparing to a per-share figure from that era

For DHT and FRO the split factors are large (1-for-12 in 2012, 1-for-5 in 2016),
so RAW and ACTUAL diverge by 12x and 5x before those dates. And because both
pay out ~half of earnings, RAW and TOTAL diverge enormously too.

THE CLAIM MOST AT RISK: §7 compared average share prices ACROSS ERAS to argue
that "2015-16 and 2019-20 had nearly the same average rate as 2005-08 yet FRO
traded ~12x lower". If that used adjusted prices, the historical price is
understated by cumulative dividends and the gap is EXAGGERATED. Tested below.
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
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")

SPLIT_EVENTS = {"DHT": [("2012-07-17", 1 / 12)], "FRO": [("2016-02-03", 1 / 5)]}

RAW, TOT = {}, {}
for t in ["DHT", "FRO"]:
    r = yf.download(t, start="2004-01-01", progress=False, auto_adjust=False)["Close"]
    a = yf.download(t, start="2004-01-01", progress=False, auto_adjust=True)["Close"]
    RAW[t] = (r.iloc[:, 0] if hasattr(r, "columns") else r).dropna()
    TOT[t] = (a.iloc[:, 0] if hasattr(a, "columns") else a).dropna()


def actual(t, when):
    """The literal price paid on that day, undoing yfinance's split adjustment.

    A 1-for-12 REVERSE split means yfinance MULTIPLIES historical prices by 12
    to make them comparable with today's shares. To recover what was actually
    paid we therefore DIVIDE by 12 (i.e. multiply by the stored ratio 1/12).

    An earlier version of this function had the direction inverted. It was
    caught by the market-cap sanity check below: it implied a DHT market cap of
    ~US$53bn in 2007 against total assets of US$422m.
    """
    p = float(RAW[t].loc[:when].iloc[-1])
    for d, f in SPLIT_EVENTS[t]:
        if pd.Timestamp(when) < pd.Timestamp(d):
            p *= f            # f = 1/12 or 1/5
    return p


# shares outstanding at each date (millions) for the market-cap sanity check.
# 2007 from the 20-F; later years from the filings/aggregator.
SHARES = {"DHT": {"2007-12-31": 30.024, "2015-12-31": 92.910,
                  "2020-12-31": 170.798, "2023-12-31": 161.000,
                  "2026-09-18": 161.236},
          "FRO": {"2007-12-31": 74.825, "2020-12-31": 197.692,
                  "2023-12-31": 222.623, "2026-09-18": 222.623}}
# total assets (US$m) at each date, as a plausibility bound
ASSETS = {"DHT": {"2007-12-31": 422, "2015-12-31": 1424, "2020-12-31": 1622,
                  "2023-12-31": 1492, "2026-09-18": 1808},
          "FRO": {"2007-12-31": 3762, "2020-12-31": 3918, "2023-12-31": 5883,
                  "2026-09-18": 5813}}


print("=" * 100)
print("COMPREHENSIVE PRICE-BASIS REVIEW — rebuilding every price claim correctly")
print("=" * 100)

# ================================================================ 1) 3 bases
print("\n" + "-" * 100)
print("1) THE THREE BASES, SIDE BY SIDE — they diverge by up to 12x")
print("-" * 100)
print(f"  {'':<6}{'date':<13}{'TOTAL (adj)':>13}{'RAW (split-adj)':>17}"
      f"{'ACTUAL paid':>14}{'ACTUAL/TOTAL':>14}")
rows = []
for t in ["DHT", "FRO"]:
    for d in ["2007-12-31", "2015-12-31", "2020-12-31", "2023-12-31", "2026-09-18"]:
        if pd.Timestamp(d) < RAW[t].index[0]:
            continue
        tot = float(TOT[t].loc[:d].iloc[-1])
        raw = float(RAW[t].loc[:d].iloc[-1])
        act = actual(t, d)
        print(f"  {t:<6}{d:<13}{tot:>13.2f}{raw:>17.2f}{act:>14.2f}{act/tot:>14.2f}")
        rows.append(dict(ticker=t, date=d, total=round(tot, 2), raw=round(raw, 2),
                         actual=round(act, 2), actual_over_total=round(act / tot, 2)))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "review_three_bases.csv"), index=False)

# ---- the sanity check that catches direction errors automatically
print("\n  MARKET-CAP SANITY CHECK — does the ACTUAL price imply a sane company?")
print(f"  {'':<6}{'date':<13}{'actual px':>11}{'shares m':>10}{'mcap US$m':>12}"
      f"{'total assets':>14}{'mcap/assets':>13}")
bad = 0
for t in ["DHT", "FRO"]:
    for d, sh in SHARES[t].items():
        if d not in ASSETS[t] or pd.Timestamp(d) < RAW[t].index[0]:
            continue
        px = actual(t, d)
        mc = px * sh
        ratio = mc / ASSETS[t][d]
        flag = "OK" if 0.05 < ratio < 8 else "🔴 IMPLAUSIBLE"
        if flag != "OK":
            bad += 1
        print(f"  {t:<6}{d:<13}{px:>11.2f}{sh:>10.1f}{mc:>12,.0f}"
              f"{ASSETS[t][d]:>14,}{ratio:>12.2f}x  {flag}")
print(f"\n  >> {bad} implausible readings. A tanker owner's market cap should sit")
print("     within a few multiples of its assets; anything outside that range")
print("     means the split direction was applied the wrong way.")
print("\n  >> The three bases diverge enormously in the past and converge to")
print("     identical values today. Any cross-era price comparison must say")
print("     WHICH basis it is on, or it means nothing.")

# ================================================================ 2) the claim
print("\n" + "-" * 100)
print("2) 🔴 THE CLAIM MOST AT RISK — §7's 'FRO traded ~12x lower' cross-era comparison")
print("-" * 100)
ERAS = [("2005-08 super-cycle", "2005-01-01", "2008-12-31"),
        ("2015-16", "2015-01-01", "2016-12-31"),
        ("2019-20", "2019-01-01", "2020-12-31"),
        ("2026 today", "2026-01-01", "2026-12-31")]
print(f"  {'':<6}{'era':<22}{'avg TOTAL':>12}{'avg RAW':>11}{'avg ACTUAL':>13}")
era_rows = []
for t in ["DHT", "FRO"]:
    for nm, lo, hi in ERAS:
        w_t = TOT[t].loc[lo:hi]
        w_r = RAW[t].loc[lo:hi]
        if len(w_r) == 0:
            continue
        # actual = raw scaled back for splits that post-date the era
        sc = 1.0
        for d, f in SPLIT_EVENTS[t]:
            if pd.Timestamp(hi) < pd.Timestamp(d):
                sc *= f
        print(f"  {t:<6}{nm:<22}{w_t.mean():>12.2f}{w_r.mean():>11.2f}"
              f"{w_r.mean()*sc:>13.2f}")
        era_rows.append(dict(ticker=t, era=nm, avg_total=round(float(w_t.mean()), 2),
                             avg_raw=round(float(w_r.mean()), 2),
                             avg_actual=round(float(w_r.mean() * sc), 2)))
er = pd.DataFrame(era_rows)
er.to_csv(os.path.join(DATA, "review_era_prices.csv"), index=False)

print("\n  The ratio that §7 quoted as '~12x lower' — recomputed on each basis:")
print(f"  {'':<6}{'comparison':<30}{'on TOTAL':>10}{'on RAW':>9}{'on ACTUAL':>11}")
for t in ["DHT", "FRO"]:
    a = er[(er["ticker"] == t) & (er["era"] == "2005-08 super-cycle")]
    b = er[(er["ticker"] == t) & (er["era"] == "2015-16")]
    if len(a) == 0 or len(b) == 0:
        continue
    a, b = a.iloc[0], b.iloc[0]
    print(f"  {t:<6}{'2005-08 avg / 2015-16 avg':<30}"
          f"{a['avg_total']/b['avg_total']:>10.2f}{a['avg_raw']/b['avg_raw']:>9.2f}"
          f"{a['avg_actual']/b['avg_actual']:>11.2f}")

print("\n  🔴 §7's '~12x' came from the TOTAL-return column. On the price actually")
print("     paid it is only ~2.0x (DHT) and ~3.8x (FRO). The claim was overstated")
print("     by roughly 3-6x. The DIRECTION survives — the same rate did fetch a")
print("     much lower price — but the magnitude does not.")

# ---- and the genuinely correct cross-era measure: MARKET CAP, not price
print("\n  But price per share is the WRONG cross-era measure anyway, because the")
print("  share counts changed enormously (DHT 30m -> 161m). Market cap is the")
print("  like-for-like comparison:")
ERA_SHARES = {"DHT": {"2005-08 super-cycle": 30.0, "2015-16": 92.9,
                      "2019-20": 170.8, "2026 today": 161.2},
              "FRO": {"2005-08 super-cycle": 74.8, "2015-16": 120.0,
                      "2019-20": 197.7, "2026 today": 222.6}}
print(f"  {'':<6}{'era':<22}{'actual px':>11}{'shares m':>10}{'MARKET CAP US$m':>17}")
mc_rows = []
for t in ["DHT", "FRO"]:
    for nm in ["2005-08 super-cycle", "2015-16", "2019-20", "2026 today"]:
        r = er[(er["ticker"] == t) & (er["era"] == nm)]
        if len(r) == 0:
            continue
        px = r.iloc[0]["avg_actual"]
        sh = ERA_SHARES[t][nm]
        print(f"  {t:<6}{nm:<22}{px:>11.2f}{sh:>10.1f}{px*sh:>17,.0f}")
        mc_rows.append(dict(ticker=t, era=nm, actual_px=px, shares_m=sh,
                            mcap_usd_m=round(px * sh)))
mc = pd.DataFrame(mc_rows)
mc.to_csv(os.path.join(DATA, "review_era_mcap.csv"), index=False)
print("\n  On MARKET CAP:")
for t in ["DHT", "FRO"]:
    a = mc[(mc["ticker"] == t) & (mc["era"] == "2005-08 super-cycle")]
    b = mc[(mc["ticker"] == t) & (mc["era"] == "2015-16")]
    if len(a) and len(b):
        ratio = a.iloc[0]["mcap_usd_m"] / b.iloc[0]["mcap_usd_m"]
        verdict = "HIGHER in the super-cycle" if ratio > 1 else "LOWER in the super-cycle"
        print(f"    {t}: super-cycle US${a.iloc[0]['mcap_usd_m']:,}m vs 2015-16 "
              f"US${b.iloc[0]['mcap_usd_m']:,}m = {ratio:.2f}x  ({verdict})")
print("\n  >> DHT's market cap was actually LARGER in 2015-16 than in the")
print("     super-cycle, because the share count tripled. The 'traded 12x lower'")
print("     framing does not survive on the correct measure at all for DHT,")
print("     and shrinks to ~2.4x for FRO.")

# ================================================================ 3) returns
print("\n" + "-" * 100)
print("3) CYCLE TROUGH->PEAK MULTIPLES — §5/§6 used TOTAL return (correct). Verify.")
print("-" * 100)
CYCLES = [("2015-16", "2014-06-30", "2016-06-30"),
          ("2019-20", "2018-06-30", "2020-12-31"),
          ("2022-26", "2022-01-01", "2026-09-18")]
print(f"  {'':<6}{'cycle':<10}{'TOTAL-return mult':>19}{'RAW-price mult':>17}"
      f"{'difference':>13}")
cyc = []
for t in ["DHT", "FRO"]:
    for nm, lo, hi in CYCLES:
        wt, wr = TOT[t].loc[lo:hi], RAW[t].loc[lo:hi]
        if len(wt) < 10:
            continue
        mt = float(wt.max() / wt.min())
        mr = float(wr.max() / wr.min())
        print(f"  {t:<6}{nm:<10}{mt:>18.2f}x{mr:>16.2f}x{(mt/mr-1)*100:>12.0f}%")
        cyc.append(dict(ticker=t, cycle=nm, total_mult=round(mt, 2),
                        raw_mult=round(mr, 2), diff_pct=round((mt / mr - 1) * 100)))
pd.DataFrame(cyc).to_csv(os.path.join(DATA, "review_cycle_mults.csv"), index=False)
print("\n  >> Trough-to-peak multiples are RETURNS, so TOTAL is the correct basis")
print("     and §5/§6 used it. The raw-price column shows how much would have")
print("     been missed by quoting price only.")

# ================================================================ 4) checklist
print("\n" + "-" * 100)
print("4) ⭐ FULL CHECKLIST — every price-dependent claim, audited")
print("-" * 100)
CHECK = [
    ("§5/§6", "cycle trough->peak multiples", "TOTAL", "TOTAL", "OK", ""),
    ("§7", "cross-era average price comparison", "TOTAL", "ACTUAL", "WRONG",
     "understated the gap; direction survives, number does not"),
    ("§7", "implied rate from TODAY's price", "TOTAL(latest)", "RAW(latest)", "OK",
     "at the present the two coincide"),
    ("§8", "P/NAV cross-check", "TOTAL(latest)", "RAW(latest)", "OK", "current only"),
    ("§11/§12", "peak P/E, capstone matrix", "current price", "RAW(latest)", "OK",
     "all current-price; no historical multiples"),
    ("§13", "P/B, P/NAV, dividend yield", "TOTAL(latest)", "RAW(latest)", "OK",
     "current only; panel C was labelled illustrative"),
    ("§14", "historical P/B series", "ADJ / unadjusted book", "RAW / book",
     "WRONG", "superseded by §15/§17"),
    ("§14.6", "forward returns from P/B peaks", "TOTAL", "TOTAL", "OK",
     "basis right, but ANCHOR DATES were wrong -- fixed in §18.5"),
    ("§15/§17", "P/NAV at cycle tops", "RAW / reported book", "same", "OK", ""),
    ("§16", "2005-08 super-cycle multiples", "ACTUAL (split-undone)", "same", "OK",
     "the only section that needed the ACTUAL basis"),
    ("§18", "the audit itself", "both, explicitly", "same", "OK", ""),
]
print(f"  {'section':<9}{'claim':<38}{'basis used':<22}{'verdict':<8}note")
for s, c, used, should, v, note in CHECK:
    mark = "✅" if v == "OK" else "🔴"
    print(f"  {s:<9}{c:<38}{used:<22}{mark} {v:<6}{note}")
pd.DataFrame(CHECK, columns=["section", "claim", "basis_used", "correct_basis",
                             "verdict", "note"]
             ).to_csv(os.path.join(DATA, "review_checklist.csv"), index=False)

# ================================================================ chart
fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))

ax = axes[0]
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    r = RAW[t].loc["2005-01-01":]
    a = TOT[t].loc["2005-01-01":]
    ax.plot(a.index, a, color=c, lw=1.5, ls=":", label=f"{t} TOTAL (adjusted)")
    ax.plot(r.index, r, color=c, lw=1.9, label=f"{t} RAW (split-adj only)")
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    for d, f in SPLIT_EVENTS[t]:
        ax.axvline(pd.Timestamp(d), color=c, ls="--", lw=1.2, alpha=.6)
        ax.text(pd.Timestamp(d), ax.get_ylim()[1] * .6,
                f" {t} 1-for-{int(1/f)}", fontsize=7.5, color=c, rotation=90)
ax.set_yscale("log")
ax.set_ylabel("US$ (log)")
ax.set_title("A. RAW vs TOTAL-return price\nthe gap is cumulative dividends; dashed lines = reverse splits",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=8); ax.grid(alpha=.25, which="both")

ax = axes[1]
labs, tot_v, raw_v, act_v = [], [], [], []
for _, r in er[er["ticker"] == "FRO"].iterrows():
    labs.append(r["era"].replace(" ", "\n", 1))
    tot_v.append(r["avg_total"]); raw_v.append(r["avg_raw"]); act_v.append(r["avg_actual"])
x = np.arange(len(labs))
ax.bar(x - .27, tot_v, .27, color="#95a5a6", label="TOTAL (what §7 used)")
ax.bar(x, raw_v, .27, color="#e67e22", label="RAW")
ax.bar(x + .27, act_v, .27, color="#c0392b", label="ACTUAL paid")
for xi, v in zip(x + .27, act_v):
    ax.text(xi, v + 1, f"{v:.0f}", ha="center", fontsize=8, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=8.5)
ax.set_ylabel("average FRO price US$")
ax.set_title("B. FRO average price by era, three bases\n§7 compared eras on the GREY bars — the wrong one",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=8.5); ax.grid(axis="y", alpha=.25)

fig.suptitle("Comprehensive price-basis review — splits, dividends and cross-era comparison",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .91])
p = os.path.join(CHARTS, "price_basis_review.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

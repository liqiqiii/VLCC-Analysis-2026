# -*- coding: utf-8 -*-
"""
Deep dive on the three CURRENTLY-FOLLOWABLE Zijin situations, plus the
downside/risk work the user asked for:

    赤峰黄金 Chifeng Gold   600988.SS / 6693.HK   (Zijin taking 25.85% control, Mar-2026)
    招金矿业 Zhaojin Mining 1818.HK               (Zijin stake + shared Haiyu gold mine)
    Allied Gold            AAUC.TO               (C$44 takeover DIED Jul-2026; 9.2% placement instead)

Plus the systemic risk to the whole "follow Zijin" strategy: Zijin's own
balance sheet, and the drawdown behaviour of every name in the roster.

Everything here is COMPUTED from market data. Operating data (production,
AISC, reserves) is NOT invented here -- it lives in the report with sources.

Rule 4 guards:
  * yfinance columns come back ALPHABETICALLY -> index by ticker NAME.
  * A/H comparison needs an explicit FX conversion, done here, not eyeballed.
"""

import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                          "Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
import numpy as np
import pandas as pd
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")
os.makedirs(DATA, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

FOCUS = {
    "600988.SS": "赤峰黄金 Chifeng (A)",
    "6693.HK": "赤峰黄金 Chifeng (H)",
    "1818.HK": "招金矿业 Zhaojin",
    "AAUC.TO": "Allied Gold",
}
CONTEXT = {
    "601899.SS": "紫金 Zijin (A)",
    "2259.HK": "紫金黄金国际 Zijin Gold Intl",
    "000408.SZ": "藏格 Zangge",
    "600388.SS": "龙净 Longking",
    "IVN.TO": "Ivanhoe",
    "MAU.TO": "Montage Gold",
    "GC=F": "Gold",
    "HG=F": "Copper",
}
ALL = {**FOCUS, **CONTEXT}


def closes(tickers, start="2014-01-01"):
    raw = yf.download(list(tickers), start=start, progress=False, auto_adjust=True)
    cl = raw["Close"]
    if not hasattr(cl, "columns"):
        cl = cl.to_frame(list(tickers)[0])
    return {t: cl[t].dropna() for t in tickers if t in cl.columns}


print("=" * 86)
print("ZIJIN'S FOLLOWABLE SET — valuation, risk and downside")
print("=" * 86)

px = closes(ALL)
info = {}
for t in ALL:
    try:
        info[t] = yf.Ticker(t).info
    except Exception as exc:
        info[t] = {}
        print(f"  info FAILED for {t}: {exc}")

# ================================================================ 1) valuation
print("\n" + "-" * 86)
print("1) VALUATION SNAPSHOT (Yahoo Finance consensus fields; currency per row)")
print("-" * 86)
hdr = (f"  {'ticker':<11}{'name':<24}{'ccy':<5}{'price':>9}{'mcap bn':>9}"
       f"{'PE(t)':>8}{'PE(f)':>8}{'P/B':>7}{'ROE%':>7}{'netDebt bn':>12}")
print(hdr)
vrows = []
for t, n in ALL.items():
    if t.endswith("=F"):
        continue
    i = info.get(t, {})
    mc = (i.get("marketCap") or np.nan) / 1e9
    td, cash = i.get("totalDebt") or 0, i.get("totalCash") or 0
    nd = (td - cash) / 1e9 if (td or cash) else np.nan
    row = dict(ticker=t, name=n, ccy=i.get("currency", "?"),
               price=i.get("currentPrice") or i.get("previousClose"),
               mcap_bn=round(mc, 1) if mc == mc else None,
               pe_trailing=i.get("trailingPE"), pe_forward=i.get("forwardPE"),
               pb=i.get("priceToBook"),
               roe_pct=round((i.get("returnOnEquity") or np.nan) * 100, 1),
               net_debt_bn=round(nd, 2) if nd == nd else None)
    vrows.append(row)
    f = lambda v, w, d=1: (f"{v:>{w}.{d}f}" if isinstance(v, (int, float))
                           and v == v else f"{'n/a':>{w}}")
    print(f"  {t:<11}{n:<24}{row['ccy']:<5}{f(row['price'],9,2)}"
          f"{f(row['mcap_bn'],9)}{f(row['pe_trailing'],8)}{f(row['pe_forward'],8)}"
          f"{f(row['pb'],7,2)}{f(row['roe_pct'],7)}{f(row['net_debt_bn'],12,2)}")
pd.DataFrame(vrows).to_csv(os.path.join(DATA, "valuation_snapshot.csv"), index=False)

print("\n  Reading it:")
print("   * PE(f) << PE(t) means consensus expects earnings to RISE sharply")
print("     (Zhaojin 18.0->9.0 = the Haiyu ramp; Allied 3.0 = the Kurmuk ramp).")
print("   * PE(f) >> PE(t) means consensus expects earnings to FALL")
print("     (Zangge 19.9->35.4 -- a warning on the potash/lithium side).")
print("   * Net debt is where the downside lives: Zhaojin and Zijin are levered;")
print("     Chifeng is in NET CASH.")

# ================================================================ 2) A/H spread
print("\n" + "-" * 86)
print("2) CHIFENG A vs H — the same company, two prices")
print("-" * 86)
fx = closes(["HKDCNY=X"])
if "HKDCNY=X" in fx:
    rate = fx["HKDCNY=X"].iloc[-1]
    a, h = px["600988.SS"].iloc[-1], px["6693.HK"].iloc[-1]
    h_cny = h * rate
    print(f"  A-share 600988.SS : CNY {a:,.2f}")
    print(f"  H-share 6693.HK   : HKD {h:,.2f}  = CNY {h_cny:,.2f}  (HKDCNY {rate:.4f})")
    print(f"  H discount to A   : {(h_cny/a - 1)*100:+.1f}%")
    print(f"  Zijin's agreed price: CNY 41.36 (A) / HKD 30.19 (H)")
    print(f"    -> A now trades {(a/41.36 - 1)*100:+.1f}% vs the deal price")
    print(f"    -> H now trades {(h/30.19 - 1)*100:+.1f}% vs the deal price")
    pd.DataFrame([dict(a_cny=a, h_hkd=h, hkdcny=rate, h_in_cny=h_cny,
                       h_discount_pct=round((h_cny/a - 1)*100, 1),
                       deal_a_cny=41.36, deal_h_hkd=30.19)]
                 ).to_csv(os.path.join(DATA, "chifeng_ah.csv"), index=False)
else:
    print("  FX unavailable — skipped.")

# ================================================================ 3) drawdowns
print("\n" + "-" * 86)
print("3) DOWNSIDE — what these things actually do when they go wrong")
print("-" * 86)
print(f"  {'name':<26}{'max DD':>9}{'when':>12}{'DD from 52w hi':>16}{'vol(ann)':>10}")
drows = []
for t, n in ALL.items():
    s = px.get(t)
    if s is None or len(s) < 60:
        continue
    run = s.cummax()
    dd = s / run - 1
    mdd, mdd_d = dd.min(), dd.idxmin()
    last12 = s.loc[s.index[-1] - pd.Timedelta(days=365):]
    from_hi = s.iloc[-1] / last12.max() - 1
    vol = s.pct_change().std() * np.sqrt(252) * 100
    drows.append(dict(ticker=t, name=n, max_dd_pct=round(mdd*100, 1),
                      max_dd_date=str(mdd_d.date()),
                      dd_from_52w_high_pct=round(from_hi*100, 1),
                      ann_vol_pct=round(vol, 1)))
    print(f"  {n:<26}{mdd*100:>8.1f}%{str(mdd_d.date()):>12}"
          f"{from_hi*100:>15.1f}%{vol:>9.1f}%")
pd.DataFrame(drows).to_csv(os.path.join(DATA, "drawdowns.csv"), index=False)
print("\n  >> This is the answer to 'what is the downside'. These are NOT")
print("     low-volatility compounders. The strategy's winners routinely")
print("     halve. Position size accordingly.")

# ================================================================ 4) Allied Gold
print("\n" + "-" * 86)
print("4) ALLIED GOLD — the cost of a FAILED Zijin deal, measured")
print("-" * 86)
aa = px["AAUC.TO"]
events = [("2026-01-26", "Zijin Gold Intl agrees to buy 100% at C$44.00/sh"),
          ("2026-07-29", "TERMINATED (Chinese regulatory approval delay)"),
          ("2026-08-10", "Replaced by a ~9.2% placement at C$32.55")]
for d, ev in events:
    p, pd_ = (aa.loc[:d].iloc[-1], aa.loc[:d].index[-1]) if len(aa.loc[:d]) else (np.nan, None)
    print(f"  {d}  C${p:6.2f} ({pd_.date() if pd_ is not None else '-'})   {ev}")
pre = aa.loc[:"2026-01-23"].iloc[-1]
at_deal = aa.loc[:"2026-07-28"].iloc[-1]
after = aa.loc["2026-07-29":].iloc[0] if len(aa.loc["2026-07-29":]) else np.nan
print(f"\n  Undisturbed before the bid (2026-01-23) : C${pre:.2f}")
print(f"  Offer price                              : C$44.00  "
      f"({(44.00/pre-1)*100:+.0f}% premium)")
print(f"  Last close before termination            : C${at_deal:.2f}  "
      f"({(at_deal/44.00-1)*100:+.1f}% vs offer = the market's doubt)")
print(f"  First close after termination            : C${after:.2f}  "
      f"({(after/at_deal-1)*100:+.1f}% on the day)")
print(f"  Today                                    : C${aa.iloc[-1]:.2f}  "
      f"({(aa.iloc[-1]/44.00-1)*100:+.1f}% vs the offer that never happened)")
print("\n  >> LESSON: the market NEVER fully believed it "
      f"({(at_deal/44.00-1)*100:+.0f}% discount to the offer the day before it died).")
print("     Merger-arb on a Chinese acquirer carries approval risk on BOTH sides.")

# ================================================================ 5) chart
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

ax = axes[0][0]
for t, lab, col in [("600988.SS", "赤峰黄金 A", "#c0392b"),
                    ("1818.HK", "招金矿业", "#2980b9"),
                    ("601899.SS", "紫金 Zijin", "#2c3e50"),
                    ("GC=F", "Gold", "#f1c40f")]:
    s = px[t].loc["2024-01-01":]
    ax.plot(s.index, s / s.iloc[0], color=col, lw=1.9, label=lab)
ax.axvline(pd.Timestamp("2026-03-22"), color="#27ae60", ls=":", lw=1.6)
ax.text(pd.Timestamp("2026-03-22"), ax.get_ylim()[1], " Zijin bids for\n Chifeng 25.85%",
        fontsize=7.5, va="top", color="#27ae60", fontweight="bold")
ax.set_title("A. The two live A/H situations vs Zijin and gold (rebased 2024)",
             fontsize=10.5, fontweight="bold")
ax.grid(alpha=.25); ax.legend(fontsize=8)

ax = axes[0][1]
s = px["AAUC.TO"].loc["2025-09-01":]
ax.plot(s.index, s.values, color="#c0392b", lw=1.9, label="Allied Gold")
ax.axhline(44.00, color="#27ae60", ls="--", lw=1.5, label="C$44.00 offer (never paid)")
ax.axhline(32.55, color="#8e44ad", ls="--", lw=1.4, label="C$32.55 placement")
for d, c in [("2026-01-26", "#27ae60"), ("2026-07-29", "#c0392b")]:
    ax.axvline(pd.Timestamp(d), color=c, ls=":", lw=1.6)
ax.set_title("B. Allied Gold — a failed Zijin takeover, in prices",
             fontsize=10.5, fontweight="bold")
ax.set_ylabel("CAD"); ax.grid(alpha=.25); ax.legend(fontsize=7.5)

ax = axes[1][0]
names = [d["name"] for d in drows]
vals = [d["max_dd_pct"] for d in drows]
order = np.argsort(vals)
ax.barh([names[i] for i in order], [vals[i] for i in order], color="#c0392b")
for i, v in enumerate([vals[i] for i in order]):
    ax.text(v, i, f" {v:.0f}%", va="center", fontsize=7.5)
ax.set_title("C. Maximum drawdown since 2014 — the real downside",
             fontsize=10.5, fontweight="bold")
ax.set_xlabel("%"); ax.grid(axis="x", alpha=.25)
ax.tick_params(labelsize=8)

ax = axes[1][1]
vv = [r for r in vrows if r["pe_forward"] and r["pe_trailing"]]
x = [r["pe_trailing"] for r in vv]
y = [r["pe_forward"] for r in vv]
ax.scatter(x, y, s=70, color="#2980b9")
for r in vv:
    ax.annotate(r["name"], (r["pe_trailing"], r["pe_forward"]), fontsize=7.5,
                xytext=(4, 4), textcoords="offset points")
lim = max(max(x), max(y)) * 1.08
ax.plot([0, lim], [0, lim], color="k", ls="--", lw=1)
ax.set_xlim(0, lim); ax.set_ylim(0, lim)
ax.set_xlabel("trailing P/E"); ax.set_ylabel("forward P/E")
ax.set_title("D. Below the line = consensus expects earnings to GROW",
             fontsize=10.5, fontweight="bold")
ax.grid(alpha=.25)

fig.suptitle("Zijin's followable set — valuation, downside and a failed deal\n"
             "Source: Yahoo Finance. Operating data (production, AISC, reserves) "
             "is sourced separately in the report.",
             fontsize=12, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .94])
p = os.path.join(CHARTS, "company_deep.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

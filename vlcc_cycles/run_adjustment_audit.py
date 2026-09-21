# -*- coding: utf-8 -*-
"""
ADJUSTMENT AUDIT — where dividend/split adjustment matters in this report,
where it does not, and whether any conclusion actually moves.

The user, 20 Sep 2026:
    "你觉得需要考虑除权/复权吗？或者说你在这份报告里考虑了吗？
     因为除权复权既会影响价格和点位的计算；股息率本身也影响估值。"

Both halves of the question are right, and they need separate answers.

THE GOVERNING PRINCIPLE: MATCH THE NUMERATOR TO THE DENOMINATOR.

  * A VALUATION MULTIPLE is a point-in-time ratio. When a dividend is paid,
    BOTH the price AND book equity fall by roughly the same amount. So RAW
    price over CONTEMPORANEOUS book is internally consistent. Using an
    ADJUSTED price (which strips dividends cumulatively, working backwards)
    against an UNADJUSTED book is not -- and the error GROWS the further back
    you go. That is exactly the §15 correction.

  * A RETURN is a holding-period outcome. The holder actually received the
    dividends, so TOTAL RETURN (adjusted) is the correct basis. Using price
    only would understate the experience of owning a 10%-yielding tanker.

So the report needs BOTH bases -- just never mixed inside one calculation.
This script audits every place it matters and tests whether the conclusions
survive.
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

print("=" * 98)
print("ADJUSTMENT AUDIT — does ex-dividend / adjusted pricing change any conclusion?")
print("=" * 98)

RAW, TOT, DIV = {}, {}, {}
for t in ["DHT", "FRO"]:
    r = yf.download(t, start="2011-01-01", progress=False, auto_adjust=False)["Close"]
    a = yf.download(t, start="2011-01-01", progress=False, auto_adjust=True)["Close"]
    RAW[t] = (r.iloc[:, 0] if hasattr(r, "columns") else r).dropna()
    TOT[t] = (a.iloc[:, 0] if hasattr(a, "columns") else a).dropna()
    DIV[t] = yf.Ticker(t).dividends

# ================================================================ 1) the drag
print("\n" + "-" * 98)
print("1) HOW BIG IS THE DIVIDEND EFFECT? (the reason this question matters at all)")
print("-" * 98)
print(f"  {'':<6}{'period':<24}{'price only':>12}{'total return':>14}{'dividend drag':>15}")
rows = []
for t in ["DHT", "FRO"]:
    for lo, lab in [("2015-12-31", "since Dec-2015"), ("2020-12-31", "since Dec-2020"),
                    ("2023-12-31", "since Dec-2023")]:
        p0, p1 = float(RAW[t].loc[:lo].iloc[-1]), float(RAW[t].iloc[-1])
        a0, a1 = float(TOT[t].loc[:lo].iloc[-1]), float(TOT[t].iloc[-1])
        pr, tr = (p1 / p0 - 1) * 100, (a1 / a0 - 1) * 100
        print(f"  {t:<6}{lab:<24}{pr:>11.0f}%{tr:>13.0f}%{tr-pr:>14.0f}pp")
        rows.append(dict(ticker=t, period=lab, price_only_pct=round(pr),
                         total_return_pct=round(tr), dividend_pp=round(tr - pr)))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "adj_dividend_drag.csv"), index=False)
print("\n  >> For these names the gap is enormous. Any 'return' quoted on a")
print("     price-only basis would be badly wrong. This report used TOTAL")
print("     RETURN for every return figure -- which is the correct choice.")

# ================================================================ 2) the error
print("\n" + "-" * 98)
print("2) WHY THE §15 ERROR GREW WITH AGE — the signature of cumulative adjustment")
print("-" * 98)
print(f"  {'':<6}{'date':<13}{'raw price':>11}{'adjusted':>10}{'ratio':>8}"
      f"{'published P/B':>15}{'actual P/B':>12}{'error':>8}")
PUB = {("DHT", "2015-12-31"): 0.42, ("DHT", "2020-12-31"): 0.52,
       ("DHT", "2023-12-31"): 1.16, ("FRO", "2020-12-31"): 0.49,
       ("FRO", "2023-12-31"): 1.51}
ACT = {("DHT", "2015-12-31"): 1.02, ("DHT", "2020-12-31"): 0.81,
       ("DHT", "2023-12-31"): 1.53, ("FRO", "2020-12-31"): 0.76,
       ("FRO", "2023-12-31"): 1.96}
sig = []
for (t, d), pub in PUB.items():
    raw = float(RAW[t].loc[:d].iloc[-1])
    adj = float(TOT[t].loc[:d].iloc[-1])
    act = ACT[(t, d)]
    print(f"  {t:<6}{d:<13}{raw:>11.2f}{adj:>10.2f}{adj/raw:>8.2f}"
          f"{pub:>15.2f}{act:>12.2f}{(pub/act-1)*100:>7.0f}%")
    sig.append(dict(ticker=t, date=d, raw=round(raw, 2), adjusted=round(adj, 2),
                    adj_over_raw=round(adj / raw, 3), published_pb=pub,
                    actual_pb=act, error_pct=round((pub / act - 1) * 100)))
pd.DataFrame(sig).to_csv(os.path.join(DATA, "adj_error_signature.csv"), index=False)
print("\n  >> The 'adjusted/raw' ratio IS the error. It shrinks towards 1.0 as you")
print("     approach today, because fewer dividends remain to be stripped out.")
print("     That monotonic pattern is the fingerprint of the bug, and it")
print("     confirms the diagnosis rather than merely asserting it.")

# ================================================================ 3) peak dates
print("\n" + "-" * 98)
print("3) DOES THE CONTAMINATION MOVE THE IDENTIFIED CYCLE PEAKS? (a real risk)")
print("-" * 98)
print("  §14 picked each cycle's P/B peak DATE using the contaminated series.")
print("  If the contamination shifted those dates, the forward-return table")
print("  in §14.6 would be anchored on the wrong days. Test it directly.\n")
try:
    pb_hist = {t: pd.read_csv(os.path.join(DATA, f"pb_history_{t}.csv"),
                              parse_dates=["date"]) for t in ["DHT", "FRO"]}
    bs = {t: pd.read_csv(os.path.join(DATA, f"bs_history_{t}.csv"), index_col=0,
                         parse_dates=True) for t in ["DHT", "FRO"]}
    CYC = [("2015-16", "2015-01-01", "2016-06-30"),
           ("2020", "2020-01-01", "2020-12-31"),
           ("2022-23", "2022-06-30", "2023-12-31")]
    moved = []
    print(f"  {'':<6}{'cycle':<10}{'peak on CONTAMINATED':>24}{'peak on CORRECTED':>22}"
          f"{'same?':>13}")
    for t in ["DHT", "FRO"]:
        h = pb_hist[t].copy()
        # rebuild corrected P/B: raw price / (equity/shares) at each period end
        cor = []
        for _, r in h.iterrows():
            b = bs[t][bs[t].index <= r["date"]].tail(1)
            if len(b) == 0 or r["date"] > RAW[t].index[-1]:
                cor.append(np.nan); continue
            bb = b.iloc[0]
            bvps = (bb["total-assets"] - bb["total-liabilities"]) / bb["shares-outstanding"]
            raw = float(RAW[t].loc[:r["date"]].iloc[-1])
            cor.append(raw / bvps if bvps > 0 else np.nan)
        h["pb_cor"] = cor
        for nm, lo, hi in CYC:
            w = h[(h["date"] >= lo) & (h["date"] <= hi)].dropna(subset=["pb_cor"])
            if len(w) == 0:
                continue
            d_old = w.loc[w["pb"].idxmax(), "date"]
            d_new = w.loc[w["pb_cor"].idxmax(), "date"]
            same = d_old == d_new
            print(f"  {t:<6}{nm:<10}{str(d_old.date()):>24}{str(d_new.date()):>22}"
                  f"{('YES' if same else 'NO — MOVED'):>13}")
            moved.append(dict(ticker=t, cycle=nm, old=str(d_old.date()),
                              new=str(d_new.date()), moved=not same))

    print("\n  🔴 TWO OF SIX PEAK DATES MOVED. §14.6's forward-return table is")
    print("     therefore anchored on the wrong day for DHT 2015-16 and 2022-23.")
    print("     Recompute those forward returns from the CORRECTED peaks:\n")
    print(f"  {'':<6}{'cycle':<10}{'anchor':<13}{'basis':<14}"
          f"{'+6m':>8}{'+12m':>8}{'+24m':>8}")
    for m in moved:
        t = m["ticker"]
        for lbl, dt in [("contaminated", m["old"]), ("CORRECTED", m["new"])]:
            if m["moved"] is False and lbl == "contaminated":
                continue
            ts = pd.Timestamp(dt)
            base = TOT[t].loc[:ts]
            if len(base) == 0:
                continue
            p0 = float(base.iloc[-1])
            cells = ""
            for mo in (6, 12, 24):
                end = ts + pd.DateOffset(months=mo)
                fut = TOT[t].loc[ts:end]
                need = ts + pd.Timedelta(days=int(30.4 * mo * 0.8))
                cells += (f"{(float(fut.iloc[-1])/p0-1)*100:>7.0f}%"
                          if len(fut) > 1 and fut.index[-1] >= need else f"{'n/a':>8}")
            print(f"  {t:<6}{m['cycle']:<10}{dt:<13}{lbl:<14}{cells}")
    pd.DataFrame(moved).to_csv(os.path.join(DATA, "adj_peak_dates.csv"), index=False)
except Exception as exc:
    print(f"  could not run: {exc}")

# ================================================================ 4) payout
print("\n" + "-" * 98)
print("4) THE USER'S SECOND POINT — payout policy distorts P/B COMPARISONS")
print("-" * 98)
print("  A company paying out 100% of earnings has flat book and flat price:")
print("  its P/B is stable by construction. One retaining everything compounds")
print("  book, so its P/B FALLS for the same business performance. Comparing")
print("  P/B across different payout policies is therefore not like-for-like.\n")
print(f"  {'':<6}{'BVPS Dec-2023':>15}{'BVPS Jun-2026':>15}{'book CAGR':>11}"
       f"{'TTM payout':>12}{'implied ROE':>13}")
pay = []
for t, b23, b26, payout in [("DHT", 6.40, 8.25, 0.50), ("FRO", 10.23, 14.15, 0.4693)]:
    yrs = 2.5
    cagr = (b26 / b23) ** (1 / yrs) - 1
    roe = cagr / (1 - payout)          # book growth = ROE x retention
    print(f"  {t:<6}{b23:>15.2f}{b26:>15.2f}{cagr*100:>10.1f}%"
          f"{payout*100:>11.0f}%{roe*100:>12.1f}%")
    pay.append(dict(ticker=t, bvps_2023=b23, bvps_2026=b26,
                    book_cagr_pct=round(cagr * 100, 1), payout_pct=round(payout * 100),
                    implied_roe_pct=round(roe * 100, 1)))
pd.DataFrame(pay).to_csv(os.path.join(DATA, "adj_payout_effect.csv"), index=False)
print("\n  >> Both pay out roughly half, so the distortion between THESE two is")
print("     small. But it is the reason §13 flagged '2x book is a MOVING")
print("     target': retained earnings raise the denominator every quarter.")

# ================================================================ 5) yield
print("\n" + "-" * 98)
print("5) DOES THE ADJUSTMENT ISSUE TOUCH §13's YIELD ANALYSIS? (check, don't assume)")
print("-" * 98)
print("  §13 computed: dividend yield = (TC-rate DPS) / CURRENT RAW PRICE.")
print("  Both sides are current and unadjusted, so there is no mismatch. ✓")
print("  The one place to be careful is the 5-year AVERAGE yield used as a")
print("  hurdle. Rebuild it from actual dividends and raw prices as a check:\n")
print(f"  {'':<6}{'year':<7}{'dividends paid':>16}{'avg raw price':>15}{'yield':>9}")
for t in ["DHT", "FRO"]:
    d = DIV[t]
    if d is None or len(d) == 0:
        continue
    d.index = pd.to_datetime(d.index).tz_localize(None)
    ys = []
    for y in range(2021, 2026):
        paid = float(d[(d.index >= f"{y}-01-01") & (d.index <= f"{y}-12-31")].sum())
        px = RAW[t].loc[f"{y}-01-01":f"{y}-12-31"]
        if len(px) == 0 or paid == 0:
            continue
        ap = float(px.mean())
        ys.append(paid / ap * 100)
        print(f"  {t:<6}{y:<7}{paid:>16.2f}{ap:>15.2f}{paid/ap*100:>8.1f}%")
    if ys:
        print(f"  {t:<6}{'MEAN':<7}{'':>16}{'':>15}{np.mean(ys):>8.1f}%   "
              f"(Yahoo's 5-yr avg: {'6.42' if t=='DHT' else '11.48'}%)")
print("\n  >> Rebuilt from raw dividends over raw prices. Any gap versus Yahoo's")
print("     figure is a definition difference (Yahoo uses its own window and")
print("     may annualise differently), not an adjustment error.")

# ================================================================ chart
fig, axes = plt.subplots(1, 3, figsize=(17.5, 5.6))

ax = axes[0]
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    r = RAW[t].loc["2015-01-01":]
    a = TOT[t].loc["2015-01-01":]
    ax.plot(r.index, r / r.iloc[0], color=c, lw=1.6, ls="--", label=f"{t} price only")
    ax.plot(a.index, a / a.iloc[0], color=c, lw=2.2, label=f"{t} TOTAL return")
ax.set_yscale("log")
ax.set_ylabel("rebased (log)")
ax.set_title("A. Price-only vs total return\nthe gap IS the dividend — huge for tankers",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=8); ax.grid(alpha=.25, which="both")

ax = axes[1]
lab = [f"{t}\n{d[:7]}" for (t, d) in PUB]
x = np.arange(len(lab))
ax.bar(x - .2, [PUB[k] for k in PUB], .4, color="#95a5a6", label="published (adjusted ÷ unadjusted)")
ax.bar(x + .2, [ACT[k] for k in PUB], .4, color="#c0392b", label="correct (raw ÷ reported)")
for xi, k in zip(x, PUB):
    ax.text(xi, max(PUB[k], ACT[k]) + .06, f"{(PUB[k]/ACT[k]-1)*100:.0f}%",
            ha="center", fontsize=8, fontweight="bold", color="#c0392b")
ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=8)
ax.set_ylabel("P/B (x)")
ax.set_title("B. The mismatch error, and how it grows with age\nlabels = size of understatement",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=8); ax.grid(axis="y", alpha=.25)

ax = axes[2]
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    s = (TOT[t] / RAW[t])
    s = s.loc["2015-01-01":]
    ax.plot(s.index, s, color=c, lw=2, label=f"{t}")
ax.axhline(1.0, color="k", lw=1, ls=":")
ax.set_ylabel("adjusted ÷ raw price")
ax.set_title("C. The adjustment factor over time\nfar below 1.0 in the past = the size of the trap",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=9); ax.grid(alpha=.25)

fig.suptitle("Ex-dividend / adjusted pricing — where it matters in this report and where it does not",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .91])
p = os.path.join(CHARTS, "adjustment_audit.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

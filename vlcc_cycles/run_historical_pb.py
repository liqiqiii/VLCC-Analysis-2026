# -*- coding: utf-8 -*-
"""
REAL historical P/B across VLCC cycle tops — DHT and FRO.

This replaces the placeholder panel in run_cycle_top.py, which divided the whole
price history by TODAY'S book value. That was illustrative only and, as the user
correctly pointed out, not good enough: book value moves, so dividing by a single
current figure distorts every historical point.

Here the book value per share is the ACTUAL REPORTED figure for each period, so
the P/B series is the real one.

SOURCE: macrotrends.net price-book pages, which publish, per period:
    date · stock price · book value per share · price-to-book ratio
Coverage is annual for the older years and quarterly from ~2012. FRO's series
starts 2009; DHT's is checked at runtime.

WHY THIS MATTERS (CRule 2): cyclical stocks trade at HIGH P/E on trough earnings
and LOW P/E on peak earnings. P/B behaves differently -- it is an ASSET multiple,
so it tends to PEAK at cycle tops, when the market pays a premium to steel.
The question the user is asking is: what premium, historically?

⚠️ Rule 4: this is a single secondary source. Cross-checked against the
independently-known 30-Jun-2026 figures (DHT BVPS US$8.25, FRO US$14.17) before
anything is published.
"""

import io
import json
import os
import re
import sys
import urllib.request

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
os.makedirs(DATA, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
URLS = {
    "DHT": "https://www.macrotrends.net/stocks/charts/DHT/dht-holdings/price-book",
    "FRO": "https://www.macrotrends.net/stocks/charts/FRO/frontline/price-book",
}
ROW = re.compile(
    r"<tr[^>]*>\s*<td[^>]*>(\d{4}-\d{2}-\d{2})</td>\s*"
    r"<td[^>]*>\$?([\d.,-]+)</td>\s*<td[^>]*>\$?([\d.,-]+)</td>\s*"
    r"<td[^>]*>([\d.,-]+)</td>")


def fetch_pb(ticker):
    req = urllib.request.Request(URLS[ticker], headers=UA)
    with urllib.request.urlopen(req, timeout=30) as f:
        html = f.read().decode("utf-8", "ignore")
    rows = ROW.findall(html)
    recs = []
    for d, px, bv, pb in rows:
        try:
            recs.append(dict(date=pd.Timestamp(d), price=float(px.replace(",", "")),
                             bvps=float(bv.replace(",", "")),
                             pb=float(pb.replace(",", ""))))
        except ValueError:
            continue
    df = pd.DataFrame(recs).sort_values("date").reset_index(drop=True)
    return df[df["bvps"] > 0]


print("=" * 94)
print("REAL HISTORICAL PRICE/BOOK ACROSS VLCC CYCLE TOPS — DHT vs FRO")
print("=" * 94)

PB = {}
for t in URLS:
    try:
        PB[t] = fetch_pb(t)
        d = PB[t]
        print(f"\n  {t}: {len(d)} periods  {d['date'].iloc[0].date()} -> "
              f"{d['date'].iloc[-1].date()}")
        print(f"      latest: price ${d['price'].iloc[-1]:.2f} · "
              f"BVPS ${d['bvps'].iloc[-1]:.2f} · P/B {d['pb'].iloc[-1]:.2f}x")
    except Exception as exc:
        print(f"  {t}: FETCH FAILED — {exc}")

# ---- append TODAY's live P/B: current price / LAST REPORTED book value.
# The scraped rows are PERIOD-END prices, so the last row is 30-Jun-2026, not
# today. Without this step every "today" comparison would be stale.
print("\n" + "-" * 94)
print("0a) TODAY vs the last reported period — the series is PERIOD-END, not live")
print("-" * 94)
LIVE = {}
for t_ in list(PB):
    s = yf.download(t_, period="5d", progress=False, auto_adjust=True)["Close"]
    s = (s.iloc[:, 0] if hasattr(s, "columns") else s).dropna()
    live_px = float(s.iloc[-1])
    last = PB[t_].iloc[-1]
    live_pb = live_px / float(last["bvps"])
    LIVE[t_] = dict(price=live_px, bvps=float(last["bvps"]), pb=live_pb,
                    asof=s.index[-1])
    print(f"  {t_}: period-end {last['date'].date()} price ${last['price']:.2f} "
          f"-> P/B {last['pb']:.2f}x")
    print(f"       LIVE {s.index[-1].date()} price ${live_px:.2f} on the same "
          f"BVPS ${last['bvps']:.2f} -> P/B {live_pb:.2f}x")
    PB[t_] = pd.concat([PB[t_], pd.DataFrame([dict(
        date=pd.Timestamp(s.index[-1].date()), price=live_px,
        bvps=float(last["bvps"]), pb=live_pb)])], ignore_index=True)

# ---- Rule 4 cross-check against the independently known Jun-2026 figures
print("\n" + "-" * 94)
print("0) RULE 4 CROSS-CHECK — does the scraped source agree with the filings?")
print("-" * 94)
KNOWN = {"DHT": 8.25, "FRO": 14.17}     # 30-Jun-2026 BVPS from quarterly filings
for t, known in KNOWN.items():
    if t not in PB:
        continue
    d = PB[t]
    row = d[d["date"] == pd.Timestamp("2026-06-30")]
    if len(row):
        got = float(row["bvps"].iloc[0])
        err = (got / known - 1) * 100
        flag = "OK" if abs(err) < 3 else "MISMATCH"
        print(f"  {t} 30-Jun-2026 BVPS: source ${got:.2f} vs filing ${known:.2f}"
              f"  ({err:+.1f}%)  {flag}")
    else:
        print(f"  {t}: no 2026-06-30 row to check")

# ================================================================ cycle tops
# Windows chosen from the rate cycles documented in sections 4-6 of this report.
CYCLES = [
    ("2008 super-cycle", "2007-01-01", "2009-06-30",
     "Demand-driven peak; peak earnings AND peak multiples"),
    ("2015-16 spike", "2015-01-01", "2016-06-30",
     "Oil-price-collapse-driven tonne-mile surge"),
    ("2020 floating storage", "2020-01-01", "2020-12-31",
     "COVID contango; violent but short"),
    ("2022-23 post-Ukraine", "2022-06-30", "2023-12-31",
     "Re-routing; the start of the current cycle"),
    ("2026 current", "2026-01-01", "2026-12-31",
     "Supply-driven + Hormuz war premium"),
]

print("\n" + "-" * 94)
print("1) PEAK P/B IN EACH CYCLE — the actual historical record")
print("-" * 94)
print(f"  {'cycle':<24}{'DHT peak P/B':>14}{'when':>12}"
      f"{'FRO peak P/B':>14}{'when':>12}")
rows = []
for name, lo, hi, note in CYCLES:
    out = {"cycle": name, "note": note}
    line = f"  {name:<24}"
    for t in ["DHT", "FRO"]:
        if t not in PB:
            line += f"{'n/d':>14}{'':>12}"
            continue
        w = PB[t][(PB[t]["date"] >= lo) & (PB[t]["date"] <= hi)]
        if len(w) == 0:
            line += f"{'n/d':>14}{'':>12}"
            out[f"{t}_peak_pb"] = None
            continue
        i = w["pb"].idxmax()
        line += f"{w.loc[i,'pb']:>13.2f}x{str(w.loc[i,'date'].date()):>12}"
        out[f"{t}_peak_pb"] = round(float(w.loc[i, "pb"]), 2)
        out[f"{t}_peak_date"] = str(w.loc[i, "date"].date())
        out[f"{t}_peak_price"] = round(float(w.loc[i, "price"]), 2)
        out[f"{t}_peak_bvps"] = round(float(w.loc[i, "bvps"]), 2)
    print(line)
    rows.append(out)
pd.DataFrame(rows).to_csv(os.path.join(DATA, "cycle_peak_pb.csv"), index=False)

# ================================================================ distribution
print("\n" + "-" * 94)
print("2) WHERE DOES TODAY SIT IN THE FULL HISTORICAL DISTRIBUTION?")
print("-" * 94)
print("  (FRO's 2014 reading of ~24x is excluded: BVPS had collapsed to US$0.36")
print("   after its near-bankruptcy restructuring, so the ratio is meaningless.)\n")
print(f"  {'':<6}{'periods':>9}{'min':>8}{'median':>9}{'mean':>8}"
      f"{'75th':>8}{'90th':>8}{'max':>8}{'TODAY':>9}{'pctile':>9}")
dist = []
for t in ["DHT", "FRO"]:
    if t not in PB:
        continue
    s_all = PB[t]["pb"].dropna()
    # FRO's 2014 reading of ~24x is a post-restructuring artefact: BVPS had
    # collapsed to US$0.36, so the ratio is meaningless. Excluded from stats.
    s = s_all[s_all < 10]
    now = float(s_all.iloc[-1])
    pct = (s < now).mean() * 100
    print(f"  {t:<6}{len(s):>9}{s.min():>8.2f}{s.median():>9.2f}{s.mean():>8.2f}"
          f"{s.quantile(.75):>8.2f}{s.quantile(.90):>8.2f}{s.max():>8.2f}"
          f"{now:>9.2f}{pct:>8.0f}%")
    dist.append(dict(ticker=t, n=len(s), excluded=len(s_all) - len(s),
                     min=round(s.min(), 2),
                     median=round(s.median(), 2), mean=round(s.mean(), 2),
                     p75=round(s.quantile(.75), 2), p90=round(s.quantile(.90), 2),
                     max=round(s.max(), 2), today=round(now, 2),
                     percentile=round(pct)))
pd.DataFrame(dist).to_csv(os.path.join(DATA, "pb_distribution.csv"), index=False)

# ================================================================ the 2x test
print("\n" + "-" * 94)
print("3) ⭐ THE USER'S 2x TEST — how often has P/B EVER been above 2.0x?")
print("-" * 94)
for t in ["DHT", "FRO"]:
    if t not in PB:
        continue
    d = PB[t]
    above = d[d["pb"] >= 2.0]
    print(f"\n  {t}: {len(above)} of {len(d)} periods ({len(above)/len(d)*100:.0f}%) "
          f"at or above 2.0x book")
    if len(above):
        print(f"     every occurrence:")
        for _, r in above.iterrows():
            print(f"       {r['date'].date()}  price ${r['price']:>7.2f}  "
                  f"BVPS ${r['bvps']:>6.2f}  P/B {r['pb']:.2f}x")
    else:
        print("     NEVER — 2.0x has not been reached in the available history")

# ================================================================ what happened
print("\n" + "-" * 94)
print("4) WHAT HAPPENED AFTER THE P/B PEAK? (the question that matters)")
print("-" * 94)
fwd = []
for t in ["DHT", "FRO"]:
    if t not in PB:
        continue
    px = yf.download(t, start="2005-01-01", progress=False,
                     auto_adjust=True)["Close"]
    px = (px.iloc[:, 0] if hasattr(px, "columns") else px).dropna()
    print(f"\n  ── {t} ── forward TOTAL RETURN from each cycle's P/B peak")
    print(f"     {'peak date':<12}{'P/B':>7}{'+6m':>9}{'+12m':>9}{'+24m':>9}")
    for name, lo, hi, _ in CYCLES:
        w = PB[t][(PB[t]["date"] >= lo) & (PB[t]["date"] <= hi)]
        if len(w) == 0:
            continue
        i = w["pb"].idxmax()
        dt, pb = w.loc[i, "date"], w.loc[i, "pb"]
        base = px.loc[:dt]
        if len(base) == 0:
            continue
        p0 = float(base.iloc[-1])
        cells = []
        rec = dict(ticker=t, cycle=name, peak_date=str(dt.date()), peak_pb=round(pb, 2))
        for m, lbl in [(6, "+6m"), (12, "+12m"), (24, "+24m")]:
            end = dt + pd.DateOffset(months=m)
            fut = px.loc[dt:end]
            need = dt + pd.Timedelta(days=int(30.4 * m * 0.8))
            if len(fut) > 1 and fut.index[-1] >= need:
                r = (float(fut.iloc[-1]) / p0 - 1) * 100
                cells.append(f"{r:>8.0f}%")
                rec[lbl] = round(r)
            else:
                cells.append(f"{'n/a':>9}")
                rec[lbl] = None
        print(f"     {str(dt.date()):<12}{pb:>6.2f}x" + "".join(cells))
        fwd.append(rec)
pd.DataFrame(fwd).to_csv(os.path.join(DATA, "pb_peak_forward_returns.csv"), index=False)

# ================================================================ chart
fig = plt.figure(figsize=(16.5, 11))
gs = fig.add_gridspec(2, 2, height_ratios=[1.25, 1])

ax = fig.add_subplot(gs[0, :])
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    if t not in PB:
        continue
    d = PB[t]
    ax.plot(d["date"], d["pb"], "o-", color=c, lw=1.9, ms=3.4, label=f"{t} actual P/B")
for name, lo, hi, _ in CYCLES:
    ax.axvspan(pd.Timestamp(lo), pd.Timestamp(hi), color="#f39c12", alpha=.11)
    ax.text(pd.Timestamp(lo) + (pd.Timestamp(hi) - pd.Timestamp(lo)) / 2,
            ax.get_ylim()[1] * .97, name.replace(" ", "\n", 1), ha="center",
            va="top", fontsize=7.4, color="#a0670a", fontweight="bold")
ax.axhline(2.0, color="#27ae60", ls="--", lw=2)
ax.text(pd.Timestamp("2009-06-01"), 2.06, "the user's 2.0x line",
        fontsize=9, color="#1e8449", fontweight="bold")
ax.axhline(1.0, color="#7f8c8d", ls=":", lw=1.3)
ax.text(pd.Timestamp("2009-06-01"), 1.04, "1.0x book", fontsize=8, color="#555")
ax.set_ylim(0, 4.3)
ax.set_ylabel("price / book value per share (x)")
ax.set_title("A. ACTUAL historical P/B using each period's REPORTED book value — "
             "not today's\nSource: macrotrends.net period data; cross-checked "
             "against the Jun-2026 filings",
             fontsize=11.5, fontweight="bold")
ax.legend(fontsize=9.5, loc="upper left")
ax.grid(alpha=.25)

ax = fig.add_subplot(gs[1, 0])
names = [r["cycle"] for r in rows]
x = np.arange(len(names))
dh = [r.get("DHT_peak_pb") or 0 for r in rows]
fr = [r.get("FRO_peak_pb") or 0 for r in rows]
ax.bar(x - .2, dh, .4, color="#c0392b", label="DHT")
ax.bar(x + .2, fr, .4, color="#2980b9", label="FRO")
for xi, v in zip(x - .2, dh):
    if v:
        ax.text(xi, v + .04, f"{v:.2f}", ha="center", fontsize=8, fontweight="bold")
for xi, v in zip(x + .2, fr):
    if v:
        ax.text(xi, v + .04, f"{v:.2f}", ha="center", fontsize=8, fontweight="bold")
ax.axhline(2.0, color="#27ae60", ls="--", lw=1.8)
ax.set_xticks(x)
ax.set_xticklabels([n.replace(" ", "\n", 1) for n in names], fontsize=7.6)
ax.set_ylabel("peak P/B in the cycle (x)")
ax.set_title("B. Peak P/B reached in each cycle\ngreen = the 2.0x line",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=.25)

ax = fig.add_subplot(gs[1, 1])
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    if t not in PB:
        continue
    s = PB[t]["pb"].dropna()
    s = s[s < 10]
    ax.hist(s, bins=22, alpha=.5, color=c, label=f"{t} (n={len(s)})")
    ax.axvline(float(s.iloc[-1]), color=c, ls="-", lw=2.4)
    ax.text(float(s.iloc[-1]), ax.get_ylim()[1] * (.92 if t == "DHT" else .80),
            f" {t} today {float(s.iloc[-1]):.2f}x", color=c, fontsize=8.5,
            fontweight="bold")
ax.axvline(2.0, color="#27ae60", ls="--", lw=2)
ax.set_xlabel("P/B (x)")
ax.set_ylabel("number of periods")
ax.set_title("C. The full distribution — where today sits\nvertical lines = today",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=.25)

fig.suptitle("VLCC cycle tops: what P/B did the market ACTUALLY pay?\n"
             "DHT and FRO, real reported book value per period",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .94])
p = os.path.join(CHARTS, "historical_pb.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")

for t in PB:
    PB[t].to_csv(os.path.join(DATA, f"pb_history_{t}.csv"), index=False)
print("  history CSVs written.")
print("\nDone.")

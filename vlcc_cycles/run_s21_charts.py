# -*- coding: utf-8 -*-
"""Aggregate summary charts for section 21 (user request: final-step visuals)."""
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

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA, CHARTS = os.path.join(HERE, "data"), os.path.join(HERE, "charts")

bt = pd.read_csv(os.path.join(DATA, "s21_backtest.csv"), keep_default_na=False)
bt["diff_pct"] = pd.to_numeric(bt["diff_pct"])
grid = pd.read_csv(os.path.join(DATA, "s21_valuation_grid.csv"))
val = pd.read_csv(os.path.join(DATA, "s21_validation.csv"))
tr = pd.read_csv(os.path.join(DATA, "s21_total_return.csv"))
NAVPS = {"DHT": 14.33, "FRO": 30.37}

PX = {"DHT": 23.27, "FRO": 51.42}
TC_LO, TC_HI = 93_000, 105_000
ACHIEVED = {"DHT": 126_700, "FRO": 152_700}

fig = plt.figure(figsize=(19, 10.5))
gs = fig.add_gridspec(2, 3, hspace=.42, wspace=.28)

# ── A. the freight ladder ─────────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 0])
lad = [("TD3C\nassessment", 1_035_000, "#7f1d1d"),
       ("TD3C TCE\n11 Sep", 862_150, "#b91c1c"),
       ("reported\nfixtures", 566_500, "#ea580c"),
       ("TD34\noutside Hormuz", 465_764, "#f59e0b"),
       ("FRO achieved\nVLCC TCE", 152_700, "#16a34a"),
       ("1-yr time\ncharter", 99_000, "#2563eb"),
       ("mid-cycle\nbenchmark", 30_000, "#64748b")]
names = [l[0] for l in lad]
vals = [l[1] for l in lad]
cols = [l[2] for l in lad]
b = ax.barh(range(len(lad))[::-1], vals, color=cols)
for i, v in enumerate(vals):
    ax.text(v * 1.05, len(lad) - 1 - i, f"{v/1000:,.0f}k/d", va="center",
            fontsize=8.5, fontweight="bold")
ax.set_yticks(range(len(lad))[::-1])
ax.set_yticklabels(names, fontsize=8.5)
ax.set_xscale("log")
ax.set_xlim(2e4, 3e6)
ax.set_xlabel("US$/day (log scale)")
ax.set_title("A. The freight ladder\nthe headline is NOT what anyone earns",
             fontsize=11, fontweight="bold")
ax.grid(axis="x", alpha=.25)

# ── B. conditional earnings error ─────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 1])
eb = bt[bt["matures"] == "n/a"].copy()
eb["lbl"] = eb["source"].str.replace(" Update", "").str.replace("Cycle ", "") + \
    "\n" + eb["metric"].str[:3]
y = np.arange(len(eb))
cols3 = ["#dc2626" if s == "in-sample" else "#f59e0b" for s in eb["status"]]
ax.barh(y[::-1], eb["diff_pct"], color=cols3)
for i, v in enumerate(eb["diff_pct"]):
    ax.text(v - 1.2, len(eb) - 1 - i, f"{v:+.0f}%", va="center", ha="right",
            fontsize=9, fontweight="bold", color="white")
ax.axvline(0, color="k", lw=1.2)
ax.set_yticks(y[::-1])
ax.set_yticklabels(eb["lbl"], fontsize=8)
ax.set_xlabel("actual vs published curve (%)")
ax.set_xlim(-24, 4)
ax.set_title("B. Every published earnings curve OVERSTATED profit\n"
             "at the rate that actually occurred", fontsize=11, fontweight="bold")
ax.grid(axis="x", alpha=.25)

# ── C. engine validation ──────────────────────────────────────────────────────
ax = fig.add_subplot(gs[0, 2])
x = np.arange(len(val))
ax.bar(x - .2, val["model_ni_q"], .4, label="model", color="#64748b")
ax.bar(x + .2, val["actual_ni_q"], .4, label="ACTUAL reported", color="#16a34a")
for i, r in val.iterrows():
    ax.text(i, max(r["model_ni_q"], r["actual_ni_q"]) * 1.04,
            f"{r['error_pct']:+.1f}%", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([f"{r.ticker}\n@ ${r.input_tce/1000:.0f}k/day"
                    for r in val.itertuples()], fontsize=9)
ax.set_ylabel("Q2-2026 net income, US$m")
ax.set_title("C. Engine reconciliation vs reported Q2-2026\nclose fit, but from OFFSETTING errors — not validation",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5)
ax.grid(axis="y", alpha=.25)

# ── D/E. yield and PE curves ──────────────────────────────────────────────────
for j, (metric, ylab, ttl) in enumerate([
        ("yield_pct", "dividend yield at today's price (%)",
         "D. Yield vs freight rate\nhypothetical 100% payout of modelled recurring EPS"),
        ("pe", "P/E at today's price",
         "E. P/E vs freight rate\nlow P/E = peak earnings, not cheapness")]):
    ax = fig.add_subplot(gs[1, j])
    for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
        d = grid[grid["ticker"] == t].dropna(subset=[metric])
        ax.plot(d["tce"] / 1000, d[metric], "o-", color=c, lw=2.2, ms=6, label=t)
    ax.axvspan(TC_LO / 1000, TC_HI / 1000, color="#2563eb", alpha=.12)
    if metric == "yield_pct":
        ax.set_ylim(0, 42)
        ax.axhline(8, color="#dc2626", ls="--", lw=1.8)
        ax.text(31, 9.0, "8% hurdle", fontsize=8.5, color="#dc2626",
                fontweight="bold")
        ax.text((TC_LO + TC_HI) / 2000, 35.5, "1-yr TC\nmarket", ha="center",
                fontsize=8.5, color="#1d4ed8", fontweight="bold", clip_on=True)
    else:
        ax.set_ylim(0, 32)
        ax.axhspan(2.5, 3.5, color="#dc2626", alpha=.13)
        ax.text(168, 4.2, "peak zone", fontsize=8.5, color="#dc2626",
                fontweight="bold")
        ax.text((TC_LO + TC_HI) / 2000, 27.0, "1-yr TC\nmarket", ha="center",
                fontsize=8.5, color="#1d4ed8", fontweight="bold", clip_on=True)
    for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
        ax.axvline(ACHIEVED[t] / 1000, color=c, ls=":", lw=1.6, alpha=.8)
    ax.set_xlabel("sustained TCE, US$ thousand/day")
    ax.set_ylabel(ylab)
    ax.set_title(ttl, fontsize=11, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(alpha=.25)

# ── F. the decision: premium over NAV vs dividends ────────────────────────────
ax = fig.add_subplot(gs[1, 2])
names2 = list(tr["ticker"])
x = np.arange(len(names2))
prem = [PX[t] - NAVPS[t] for t in names2]
ax.bar(x, NAVPS.values() if False else [NAVPS[t] for t in names2], .55,
       label="NAV per share", color="#2980b9")
ax.bar(x, prem, .55, bottom=[NAVPS[t] for t in names2],
       label="premium over NAV", color="#dc2626")
for i, t in enumerate(names2):
    dps = float(tr[tr["ticker"] == t]["dividend"].iloc[0])
    yrs = prem[i] / dps
    ax.text(i, PX[t] + 1.2, f"{yrs:.1f} yrs of\ndividends\nto earn back",
            ha="center", fontsize=9, fontweight="bold", color="#7f1d1d")
    ax.text(i, NAVPS[t] / 2, f"${NAVPS[t]:.2f}", ha="center", color="white",
            fontsize=10, fontweight="bold")
    ax.text(i, NAVPS[t] + prem[i] / 2, f"+${prem[i]:.2f}", ha="center",
            color="white", fontsize=10, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([f"{t}\nUS${PX[t]:.2f}" for t in names2], fontsize=10)
ax.set_ylabel("US$ per share")
ax.set_ylim(0, max(PX.values()) * 1.32)
ax.set_title("F. The actual decision\ncan the rate hold long enough to earn the premium?",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5, loc="upper left")
ax.grid(axis="y", alpha=.25)

fig.suptitle("Section 21 — back-test of prior forecasts and the cycle position, "
             "on numbers only  ·  DHT US\\$23.27 · FRO US\\$51.42",
             fontsize=13.5, fontweight="bold")
p = os.path.join(CHARTS, "s21_summary.png")
fig.savefig(p, dpi=140, bbox_inches="tight")
plt.close(fig)
print(f"  chart -> {p}")
print("Done.")

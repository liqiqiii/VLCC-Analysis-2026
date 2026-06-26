"""
Generate charts for the TCE vs VLCC stock "average x duration" report.
Reads tce_results.json, tce_data.json, sim_results.json, sim_paths.json.
Saves PNGs to charts/.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path("charts")
OUT.mkdir(exist_ok=True)

res = json.load(open("tce_results.json"))
sim = json.load(open("sim_results.json"))
paths = json.load(open("sim_paths.json"))
data = pd.DataFrame(json.load(open("tce_data.json")))
data["index"] = pd.to_datetime(data["Date"])

BLUE, ORANGE, GREEN, RED, GREY = "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#7f7f7f"


# 1. Headline: R^2 of stock LEVEL vs rate, by averaging window ────────────────
def chart_r2_windows():
    w = res["correlation"]["windows_weeks"]
    labels = ["spot" if x == 1 else f"{x}w avg" for x in w]
    fro = res["correlation"]["stocks"]["FRO"]["r2_level"]
    dht = res["correlation"]["stocks"]["DHT"]["r2_level"]
    x = np.arange(len(w))
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.bar(x - 0.2, fro, 0.4, label="FRO", color=BLUE)
    ax.bar(x + 0.2, dht, 0.4, label="DHT", color=ORANGE)
    for i, (a, b) in enumerate(zip(fro, dht)):
        ax.text(i - 0.2, a + 0.005, f"{a:.2f}", ha="center", fontsize=8)
        ax.text(i + 0.2, b + 0.005, f"{b:.2f}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("R\u00b2 (stock price level vs rate)")
    ax.set_title("Stock tracks the SUSTAINED AVERAGE rate, not spot\n"
                 "R\u00b2 rises as the averaging window lengthens (BDTI weekly, 2020\u20132024)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "tce_r2_windows.png", dpi=130)
    plt.close(fig)


# 2. Visual decoupling: spot vs 52w-avg rate vs FRO price ─────────────────────
def chart_overlay():
    d = data.copy()
    d["avg52"] = d["BDTI"].rolling(52, min_periods=52).mean()
    fig, ax1 = plt.subplots(figsize=(10, 5.2))
    ax1.plot(d["index"], d["BDTI"], color=GREY, lw=1, alpha=0.7, label="BDTI spot")
    ax1.plot(d["index"], d["avg52"], color=GREEN, lw=2.2, label="BDTI 52w avg")
    ax1.set_ylabel("BDTI (index)")
    ax2 = ax1.twinx()
    ax2.plot(d["index"], d["FRO"], color=BLUE, lw=2, label="FRO price")
    ax2.set_ylabel("FRO price (USD, adj)")
    ax1.set_title("Spot rate spikes vs the slow 52w average vs the stock\n"
                  "The stock follows the green line, not the grey spikes")
    l1, lab1 = ax1.get_legend_handles_labels()
    l2, lab2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, lab1 + lab2, loc="upper left", fontsize=9)
    ax1.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "tce_overlay.png", dpi=130)
    plt.close(fig)


# 3. Amplitude compression: TCE peak mult vs stock peak mult ──────────────────
def chart_amplitude():
    rows = res["long_cycle"]["rows"]
    cycles = [r["cycle"].replace(" ", "\n", 1) for r in rows]
    tce = [r["tce_peak_mult"] for r in rows]
    fro = [r.get("FRO_peak_mult") or 0 for r in rows]
    dht = [r.get("DHT_peak_mult") or 0 for r in rows]
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.bar(x - 0.27, tce, 0.27, label="TCE peak \u00d7", color=RED)
    ax.bar(x, fro, 0.27, label="FRO peak \u00d7", color=BLUE)
    ax.bar(x + 0.27, dht, 0.27, label="DHT peak \u00d7", color=ORANGE)
    for i in range(len(rows)):
        ax.text(i - 0.27, tce[i] + 0.1, f"{tce[i]:.1f}\u00d7", ha="center", fontsize=8)
        if fro[i]:
            ax.text(i, fro[i] + 0.1, f"{fro[i]:.1f}\u00d7", ha="center", fontsize=8)
        if dht[i]:
            ax.text(i + 0.27, dht[i] + 0.1, f"{dht[i]:.1f}\u00d7", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(cycles, fontsize=8)
    ax.set_ylabel("Peak / baseline multiple")
    ax.set_title("TCE peaks are 5\u201310\u00d7; stock peaks only ~1\u20133\u00d7\n"
                 "Amplitude compression: the market discounts transient rate spikes")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "tce_amplitude.png", dpi=130)
    plt.close(fig)


# 4. Simulation EXP1: same peak, different duration ───────────────────────────
def chart_sim_duration():
    sc = paths["exp1"]["scenarios"]
    names = [("spike_2w", "2-week spike"), ("plateau_6m", "6-month plateau"),
             ("sustained_2y", "2-year sustained")]
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    for ax, (key, title) in zip(axes, names):
        s = sc[key]
        tce = np.array(s["tce_path"])
        stk = np.array(s["stock_path"])
        ax.plot(tce, color=GREY, lw=1.3, label="TCE ($/day)")
        ax.set_ylabel("TCE $/day", color=GREY)
        ax.tick_params(axis="y", labelcolor=GREY)
        axr = ax.twinx()
        axr.plot(stk, color=BLUE, lw=2.2, label="Stock")
        axr.set_ylabel("Stock", color=BLUE)
        axr.tick_params(axis="y", labelcolor=BLUE)
        ax.set_title(f"{title}: same $200k peak \u2192 stock re-rate "
                     f"\u00d7{s['stock_rerate_x']}", fontsize=10)
        ax.grid(alpha=0.2)
    axes[-1].set_xlabel("week")
    fig.suptitle("Same TCE peak, different DURATION \u2192 very different stock outcome",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(OUT / "tce_sim_duration.png", dpi=130)
    plt.close(fig)


# 5. Simulation EXP3: forward return after spot vs sustained signal ───────────
def chart_sim_signal():
    s = sim["exp3_signal_quality"]
    cats = ["mean_fwd_return", "median_fwd_return", "win_rate"]
    labels = ["mean fwd\n26w return", "median fwd\n26w return", "win rate"]
    spot = [s["spot_signal"][c] for c in cats]
    sust = [s["sustained_signal"][c] for c in cats]
    x = np.arange(len(cats))
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.bar(x - 0.2, spot, 0.4, label=f"Spot spike signal (n={s['spot_signal']['n']})", color=GREY)
    ax.bar(x + 0.2, sust, 0.4, label=f"Sustained-avg signal (n={s['sustained_signal']['n']})", color=GREEN)
    for i in range(len(cats)):
        ax.text(i - 0.2, spot[i] + 0.01, f"{spot[i]:.2f}", ha="center", fontsize=8)
        ax.text(i + 0.2, sust[i] + 0.01, f"{sust[i]:.2f}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Buying the stock on a SUSTAINED-average signal beats spot-chasing\n"
                 "(simulation: forward 26-week stock return after each signal type)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "tce_sim_signal.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    chart_r2_windows()
    chart_overlay()
    chart_amplitude()
    chart_sim_duration()
    chart_sim_signal()
    print("Charts written to", OUT.resolve())
    for p in sorted(OUT.glob("tce_*.png")):
        print(" ", p.name)

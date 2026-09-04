"""
Gold-miner price charts (companion to run_gold_compare.py):
  (1) six miners' dividend-adjusted (total-return) price vs the gold price, rebased
  (2) Zijin's price vs gold AND copper, rebased

Data hygiene (Rule 4): yfinance auto_adjust=True gives dividend/split-adjusted
(复权) prices; columns come back ALPHABETICAL, so index BY TICKER NAME. Gold=GC=F,
copper=HG=F; if a futures symbol fails we fall back to an ETF proxy (GLD, CPER).
All series rebased to 100 at the common start for comparability.

Outputs (./charts/): miners_vs_gold.png, zijin_gold_copper.png
Run: python run_price_charts.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf

HERE = os.path.dirname(__file__)
CH = os.path.join(HERE, "charts"); os.makedirs(CH, exist_ok=True)
DATA = os.path.join(HERE, "data"); os.makedirs(DATA, exist_ok=True)

START = "2021-01-01"

MINERS = {  # ticker -> label (dividend-adjusted / 复权). The SIX: top-3 each market.
    "NEM": "Newmont", "AEM": "Agnico", "KGC": "Kinross",
    "601899.SS": "Zijin", "600547.SS": "Shandong Gold", "1818.HK": "Zhaojin",
}


def dl(ticker, start=START):
    s = yf.download(ticker, start=start, interval="1d",
                    auto_adjust=True, progress=False)["Close"]
    if hasattr(s, "columns"):
        s = s.iloc[:, 0]
    s = s.dropna()
    # resample to a common weekly grid (Friday) so cross-exchange dates align
    return s.resample("W-FRI").last()


def gold_series(start=START):
    for t in ("GC=F", "GLD"):
        s = dl(t, start)
        if len(s) > 50:
            return s, ("Gold (spot)" if t == "GC=F" else "Gold (GLD proxy)")
    return None, None


def copper_series(start=START):
    for t in ("HG=F", "CPER"):
        s = dl(t, start)
        if len(s) > 50:
            return s, ("Copper (spot)" if t == "HG=F" else "Copper (CPER proxy)")
    return None, None


def rebase(s, ref_index):
    s = s.reindex(ref_index).ffill()
    valid = s.dropna()
    if valid.empty:
        return s
    return s / valid.iloc[0] * 100


def chart_miners_vs_gold():
    gold, glabel = gold_series()
    if gold is None:
        print("gold fetch failed"); return
    # common weekly index from gold
    idx = gold.index
    fig, ax = plt.subplots(figsize=(13, 6.5))
    # gold as a thick gold band in the background
    g = rebase(gold, idx)
    ax.plot(idx, g, color="#e0a80d", lw=3.2, label=glabel + " (rebased 100)", zorder=5)
    colors = {"Newmont": "#2b6cb0", "Agnico": "#2e7d4f", "Kinross": "#6b46c1",
              "Zhaojin": "#8a8d91", "Zijin": "#b0413e", "Shandong Gold": "#d15fa8"}
    frame = {"gold": g}
    for t, lab in MINERS.items():
        s = dl(t)
        if len(s) < 50:
            print(f"  {lab} ({t}) sparse"); continue
        r = rebase(s, idx)
        frame[lab] = r
        ax.plot(idx, r, color=colors.get(lab, "grey"), lw=1.4, label=lab, alpha=0.9)
    ax.axhline(100, color="black", lw=0.6, ls=":")
    ax.set_title("Gold miners (dividend-adjusted) vs the gold price — rebased to 100 (%s -> now)" % START[:4])
    ax.set_ylabel("Rebased total-return index (100 = start)")
    ax.legend(ncol=2, fontsize=8, loc="upper left"); ax.grid(alpha=0.2)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "miners_vs_gold.png"), dpi=115, bbox_inches="tight")
    plt.close(fig)
    pd.DataFrame(frame).to_csv(os.path.join(DATA, "miners_vs_gold.csv"))
    # print final rebased values (torque check)
    print("Rebased levels now (100=start):")
    for k, v in frame.items():
        print(f"  {k:16s} {v.dropna().iloc[-1]:6.0f}")


def chart_zijin_gold_copper():
    gold, glabel = gold_series()
    copper, clabel = copper_series()
    z = dl("601899.SS")
    if gold is None or copper is None or len(z) < 50:
        print("zijin/gold/copper fetch issue"); return
    idx = z.index
    zr = rebase(z, idx); gr = rebase(gold, idx); cr = rebase(copper, idx)
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.plot(idx, zr, color="#b0413e", lw=2.4, label="Zijin (601899.SS, div-adj)", zorder=5)
    ax.plot(idx, gr, color="#e0a80d", lw=2.0, label=glabel)
    ax.plot(idx, cr, color="#c47f17", lw=2.0, ls="--", label=clabel)
    ax.axhline(100, color="black", lw=0.6, ls=":")
    ax.set_title("Zijin Mining vs Gold AND Copper — rebased to 100 (Zijin is a copper-gold play, ~33%% gold rev)")
    ax.set_ylabel("Rebased index (100 = start)")
    ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.2)
    # correlation box
    df = pd.DataFrame({"zijin": zr, "gold": gr, "copper": cr}).dropna()
    ret = df.pct_change().dropna()
    cg = ret["zijin"].corr(ret["gold"]); cc = ret["zijin"].corr(ret["copper"])
    ax.text(0.99, 0.03, f"weekly-return corr:  Zijin~Gold {cg:.2f}   Zijin~Copper {cc:.2f}",
            transform=ax.transAxes, ha="right", fontsize=9,
            bbox=dict(boxstyle="round", fc="#f5f5f5", ec="grey"))
    fig.tight_layout(); fig.savefig(os.path.join(CH, "zijin_gold_copper.png"), dpi=115, bbox_inches="tight")
    plt.close(fig)
    df.to_csv(os.path.join(DATA, "zijin_gold_copper.csv"))
    print(f"\nZijin corr to gold {cg:.2f}, to copper {cc:.2f}")
    print(f"Rebased now: Zijin {zr.dropna().iloc[-1]:.0f}, Gold {gr.dropna().iloc[-1]:.0f}, Copper {cr.dropna().iloc[-1]:.0f}")


def main():
    chart_miners_vs_gold()
    chart_zijin_gold_copper()
    print(f"\nCharts -> {CH}")


if __name__ == "__main__":
    main()

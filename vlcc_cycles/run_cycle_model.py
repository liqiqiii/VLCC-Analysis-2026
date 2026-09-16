"""
VLCC big-cycle study — Module 2: rate-vs-stock relationship across cycles.
For each major cycle, find the STOCK trough then its SUBSEQUENT peak (so the
multiple is a real trough->peak move), and compare the stock multiple to the
sourced VLCC TD3C freight-rate multiple over the same window.

Data hygiene (Rule 4): FRO/DHT prices are yfinance split/dividend-adjusted (exact,
indexed by name). VLCC TD3C rate anchors are APPROXIMATE annual-average / cycle
figures compiled from public sources (Baltic/Clarksons via trade press) — used
only to illustrate the rate-multiple vs stock-multiple relationship; flagged.

Outputs (./data/, ./charts/):
  cycle_multiples.csv   -- per-cycle stock trough->peak vs rate trough->peak
  fro_dht_history.png   -- FRO & DHT split-adjusted price, log scale, cycles shaded
Run: python run_cycle_model.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "data"); os.makedirs(OUT, exist_ok=True)
CH = os.path.join(HERE, "charts"); os.makedirs(CH, exist_ok=True)

# Cycle windows (UP-LEG only, ending before the crash). Rate anchors are SUSTAINED
# annual-average $/day (trough->peak); rate_spike = transient peak for context. APPROX/sourced.
CYCLES = {
    "2005-08": dict(win=("2005-10-01", "2008-09-30"),
                    rate_lo=50000, rate_hi=95000, rate_spike=196000,
                    note="China demand supercycle; sustained ~$50k->$95k, Jul-2008 spike ~$196k"),
    "2015": dict(win=("2014-06-01", "2015-12-31"),
                 rate_lo=28000, rate_hi=65000, rate_spike=100000,
                 note="China SPR buying + cheap oil; sustained ~$28k->$65k, spike ~$100k"),
    "2019-20": dict(win=("2018-07-01", "2020-05-31"),
                    rate_lo=18000, rate_hi=45000, rate_spike=300000,
                    note="Sustained ~$18k->$45k; TRANSIENT spikes: COSCO Oct-19 ~$300k, COVID 2020 ~$200k"),
    "2022-26": dict(win=("2021-06-01", "2026-09-30"),
                    rate_lo=20000, rate_hi=95000, rate_spike=585000,
                    note="Supply-driven + Russia rerouting + Hormuz; sustained ~$20k->$85-95k, 2026 spike ~$585k"),
}


def load(t):
    s = yf.download(t, start="2001-01-01", interval="1mo",
                    auto_adjust=True, progress=False)["Close"].dropna()
    return s.iloc[:, 0] if hasattr(s, "columns") else s


def trough_then_peak(s, win):
    """Rising-leg multiple: find the PEAK in the window, then the TROUGH BEFORE it."""
    w = s[(s.index >= win[0]) & (s.index <= win[1])]
    if len(w) < 4:
        return None
    pk_idx = w.idxmax()
    pk = w.loc[pk_idx]
    before = w[w.index <= pk_idx]          # trough must come BEFORE the peak
    tr_idx = before.idxmin()
    tr = before.loc[tr_idx]
    return dict(trough=round(float(tr), 2), trough_date=str(tr_idx.date()),
                peak=round(float(pk), 2), peak_date=str(pk_idx.date()),
                mult=round(float(pk / tr), 1),
                months=(pk_idx.year - tr_idx.year) * 12 + (pk_idx.month - tr_idx.month))


def main():
    fro, dht = load("FRO"), load("DHT")
    rows = []
    for name, c in CYCLES.items():
        rate_mult = c["rate_hi"] / c["rate_lo"]
        spike_mult = c["rate_spike"] / c["rate_lo"]
        for t, s in [("FRO", fro), ("DHT", dht)]:
            r = trough_then_peak(s, c["win"])
            if not r:
                continue
            rows.append(dict(cycle=name, ticker=t, **r,
                             rate_lo=c["rate_lo"], rate_hi_sustained=c["rate_hi"],
                             rate_spike=c["rate_spike"],
                             rate_mult_sustained=round(rate_mult, 1),
                             rate_mult_spike=round(spike_mult, 1),
                             stock_vs_sustained_beta=round(r["mult"] / rate_mult, 2),
                             stock_vs_spike_beta=round(r["mult"] / spike_mult, 2),
                             note=c["note"]))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "cycle_multiples.csv"), index=False)
    print("CYCLE MULTIPLES — stock trough->peak vs rate trough->peak:")
    print(df[["cycle", "ticker", "trough", "trough_date", "peak", "peak_date",
              "mult", "months", "rate_mult_sustained", "rate_mult_spike",
              "stock_vs_sustained_beta"]].to_string(index=False))

    # chart: FRO/DHT split-adjusted, log scale, cycle windows shaded
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.semilogy(fro.index, fro.values, color="#b0413e", lw=1.4, label="FRO (Frontline, split-adj)")
    ax.semilogy(dht.index, dht.values, color="#2b6cb0", lw=1.4, label="DHT (split-adj)")
    for name, c in CYCLES.items():
        a = pd.Timestamp(c["win"][0]); b = pd.Timestamp(c["win"][1])
        ax.axvspan(a, b, color="gold", alpha=0.08)
        ax.text(a, ax.get_ylim()[1] * 0.7, name, fontsize=8, color="#7a5c00")
    ax.set_title("FRO & DHT across four VLCC cycles (log scale) — cyclical, not buy-and-hold")
    ax.set_ylabel("Split/dividend-adjusted price (log)")
    ax.legend(loc="upper left"); ax.grid(alpha=0.2, which="both")
    fig.tight_layout(); fig.savefig(os.path.join(CH, "fro_dht_history.png"), dpi=115, bbox_inches="tight")
    plt.close(fig)

    print("\nKey reads:")
    for name in CYCLES:
        sub = df[df["cycle"] == name]
        if len(sub):
            print(f"  {name}: sustained rate {sub.iloc[0]['rate_mult_sustained']}x "
                  f"(spike {sub.iloc[0]['rate_mult_spike']}x) -> stock {list(sub['mult'])} "
                  f"| beta-vs-sustained {list(sub['stock_vs_sustained_beta'])}")
    print(f"\nCharts -> {CH}\nCSVs -> {OUT}")


if __name__ == "__main__":
    main()

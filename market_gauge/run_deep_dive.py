"""
Market Gauge — DEEP DIVE (companion to run_market_gauge.py)

Adds, per the user's request:
  (a) TRUE breadth from S&P 500 constituents: % above 60-day and 200-day MA,
      as a time series (not a proxy) — current + 3-yr trend.
  (b) CAPE forward-return backtest: what starting valuation has meant for
      subsequent real total returns (1/3/10-yr), and specifically when starting
      near today's ~99th-percentile CAPE.
  Plus: valuation PEAK/BOTTOM history (1929/2000/2021 ...), what drove them and
  what happened after; and CHARTS (PNGs into ./charts/).

Data hygiene (Rule 4): constituents from GitHub 'datasets/s-and-p-500-companies';
prices via yfinance (indexed by name); CAPE + real-total-return from Yale
ie_data.xls. Everything reproducible.

Run: python run_deep_dive.py
"""
import os
import ssl
import urllib.request
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "data")
CH = os.path.join(HERE, "charts")
os.makedirs(OUT, exist_ok=True)
os.makedirs(CH, exist_ok=True)


def get_constituents():
    path = os.path.join(HERE, "sp500_syms.txt")
    if os.path.exists(path):
        return open(path).read().split()
    for u in ["https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"]:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        df = pd.read_csv(io.BytesIO(urllib.request.urlopen(req, timeout=30).read()))
        col = [c for c in df.columns if c.lower() in ("symbol", "ticker")][0]
        syms = [str(s).replace(".", "-") for s in df[col]]
        open(path, "w").write("\n".join(syms))
        return syms


# ---------- (a) TRUE breadth from constituents ----------
def breadth_from_constituents():
    syms = get_constituents()
    px = yf.download(syms, start="2022-06-01", interval="1d",
                     auto_adjust=True, progress=False)["Close"]
    px = px.dropna(axis=1, how="all")
    ma60 = px.rolling(60).mean()
    ma200 = px.rolling(200).mean()
    above60 = (px > ma60).sum(axis=1) / px.notna().sum(axis=1) * 100
    above200 = (px > ma200).sum(axis=1) / px.notna().sum(axis=1) * 100
    bt = pd.DataFrame({"pct_above_60dma": above60.round(1),
                       "pct_above_200dma": above200.round(1)}).dropna()
    bt.to_csv(os.path.join(OUT, "breadth_constituents.csv"))
    cur = bt.iloc[-1]
    print(f"BREADTH from {px.shape[1]} constituents, latest {bt.index[-1].date()}: "
          f">60dma {cur['pct_above_60dma']:.0f}% | >200dma {cur['pct_above_200dma']:.0f}%")

    # chart
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(bt.index, bt["pct_above_60dma"], label="% above 60-day MA", lw=1.3, color="#e07b39")
    ax.plot(bt.index, bt["pct_above_200dma"], label="% above 200-day MA", lw=1.6, color="#2b6cb0")
    for lvl in (20, 50, 80):
        ax.axhline(lvl, color="grey", lw=0.5, ls=":")
    ax.set_title("S&P 500 market breadth — % of constituents above moving averages")
    ax.set_ylabel("% of index members"); ax.set_ylim(0, 100)
    ax.legend(loc="lower left"); ax.grid(alpha=0.2)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "breadth_constituents.png"), dpi=110)
    plt.close(fig)
    return cur, bt


# ---------- Shiller loader ----------
def load_shiller():
    path = os.path.join(HERE, "ie_data.xls")
    if not os.path.exists(path):
        ctx = ssl.create_default_context(); ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request("http://www.econ.yale.edu/~shiller/data/ie_data.xls",
                                     headers={"User-Agent": "Mozilla/5.0"})
        open(path, "wb").write(urllib.request.urlopen(req, timeout=30, context=ctx).read())
    df = pd.read_excel(path, sheet_name="Data", skiprows=7)
    # Column layout (Shiller): 0 Date, ... 12 CAPE(P/E10). Find real total return price col.
    df = df.rename(columns={df.columns[0]: "DateFrac"})
    df["CAPE"] = pd.to_numeric(df.iloc[:, 12], errors="coerce")
    # Real Total Return Price is column 9 ('Price.1' in Shiller's sheet: the
    # dividends-reinvested real index, ~109 in 1871 -> ~2.96M by 2023).
    df["RTR"] = pd.to_numeric(df.iloc[:, 9], errors="coerce")
    # build a proper year-month index from the fractional date (e.g., 2026.07)
    d = df["DateFrac"].astype(str).str.replace(".1$", ".10", regex=True)
    yr = d.str.split(".").str[0].astype(float)
    mo = d.str.split(".").str[1].fillna("01").str.pad(2, "right", "0").astype(float)
    df["ym"] = yr + (mo - 1) / 12
    return df.dropna(subset=["CAPE"]).reset_index(drop=True)


# ---------- (b) CAPE -> forward real total return ----------
def cape_forward_returns():
    df = load_shiller()
    df = df.dropna(subset=["RTR"]).reset_index(drop=True)
    rtr = df["RTR"].values
    cape = df["CAPE"].values
    n = len(df)
    for horizon, key in [(12, "fwd_1y"), (36, "fwd_3y"), (120, "fwd_10y")]:
        fwd = np.full(n, np.nan)
        for i in range(n - horizon):
            fwd[i] = (rtr[i + horizon] / rtr[i]) ** (12 / horizon) - 1
        df[key] = fwd * 100
    # bucket by CAPE decile
    df["cape_decile"] = pd.qcut(df["CAPE"], 10, labels=False) + 1
    tab = df.groupby("cape_decile").agg(
        cape_lo=("CAPE", "min"), cape_hi=("CAPE", "max"),
        fwd_1y=("fwd_1y", "mean"), fwd_3y=("fwd_3y", "mean"),
        fwd_10y=("fwd_10y", "mean")).round(1)
    tab.to_csv(os.path.join(OUT, "cape_forward_returns.csv"))
    print("\nCAPE decile -> forward REAL total return (annualized %, 1881-now):")
    print(tab.to_string())

    # what happens starting from today's CAPE bucket (top decile)
    cur_cape = 41.3
    hi = df[df["CAPE"] >= 34]  # roughly the >=95th pct / dot-com-like zone
    print(f"\nStarting CAPE >= 34 (n={len(hi.dropna(subset=['fwd_10y']))}): "
          f"avg fwd-10y real {hi['fwd_10y'].mean():.1f}%/yr, "
          f"worst {hi['fwd_10y'].min():.1f}%, best {hi['fwd_10y'].max():.1f}%")

    # scatter chart: starting CAPE vs forward 10y real return
    fig, ax = plt.subplots(figsize=(9, 6))
    s = df.dropna(subset=["fwd_10y"])
    sc = ax.scatter(s["CAPE"], s["fwd_10y"], s=6, alpha=0.35, c=s["ym"], cmap="viridis")
    ax.axvline(cur_cape, color="red", lw=1.5, ls="--", label=f"today CAPE {cur_cape}")
    ax.axhline(0, color="grey", lw=0.6)
    ax.set_xlabel("Starting Shiller CAPE"); ax.set_ylabel("Subsequent 10-yr real total return (%/yr)")
    ax.set_title("Starting valuation vs forward 10-yr return (S&P, 1881-now)")
    cb = fig.colorbar(sc); cb.set_label("year")
    ax.legend(); ax.grid(alpha=0.2)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "cape_forward_scatter.png"), dpi=110)
    plt.close(fig)

    # CAPE history line chart with peaks annotated
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["ym"], df["CAPE"], lw=0.8, color="#2b6cb0")
    ax.axhline(df["CAPE"].median(), color="green", lw=0.8, ls=":", label=f"median {df['CAPE'].median():.0f}")
    ax.axhline(cur_cape, color="red", lw=1.0, ls="--", label=f"today {cur_cape}")
    for yr, lab in [(1929.7, "1929"), (2000.0, "2000"), (2021.9, "2021")]:
        row = df.iloc[(df["ym"] - yr).abs().argmin()]
        ax.annotate(lab, (row["ym"], row["CAPE"]), fontsize=8,
                    xytext=(row["ym"] - 6, row["CAPE"] + 2))
    ax.set_title("Shiller CAPE, 1881-2026 (with today marked)")
    ax.set_ylabel("CAPE (P/E10)"); ax.legend(); ax.grid(alpha=0.2)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "cape_history.png"), dpi=110)
    plt.close(fig)
    return tab, df


# ---------- valuation peak/bottom history ----------
def peaks_and_troughs(df):
    # Known major CAPE extremes; compute the subsequent drawdown from Shiller RTR
    rtr = df.set_index("ym")["RTR"]
    events = [
        ("1929-09 peak", 1929.7, "Roaring-20s mania, leverage/margin", 32.6),
        ("1966 peak", 1966.0, "Nifty-Fifty era start; pre-stagflation", 24.1),
        ("2000-03 peak", 2000.2, "Dot-com internet bubble", 44.2),
        ("2007-10 peak", 2007.8, "Housing/credit peak", 27.5),
        ("2021-12 peak", 2021.9, "Post-COVID stimulus/mega-cap", 38.6),
        ("1982-07 trough", 1982.5, "Volcker recession, 14% inflation broke", 6.6),
        ("2009-03 trough", 2009.2, "GFC bottom", 13.3),
    ]
    rows = []
    for name, yr, why, cape in events:
        try:
            i = int(np.abs(np.asarray(rtr.index, dtype=float) - yr).argmin())
            start = rtr.iloc[i]
            fwd5 = rtr.iloc[i:i + 60]
            trough = fwd5.min()
            dd = (trough / start - 1) * 100
            j = min(i + 120, len(rtr) - 1)
            yrs = (rtr.index[j] - rtr.index[i])
            fwd10 = (rtr.iloc[j] / start) ** (1 / yrs) - 1 if yrs > 0 else np.nan
            partial = "" if (i + 120) < len(rtr) else " (partial: data ends 2023)"
            rows.append({"event": name, "approx_CAPE": cape, "driver": why,
                         "next_5y_real_drawdown_pct": f"{round(dd, 0):.0f}{partial}",
                         "next_10y_real_cagr_pct": round(fwd10 * 100, 1)})
        except Exception as e:
            rows.append({"event": name, "approx_CAPE": cape, "driver": why,
                         "next_5y_real_drawdown_pct": "n/a", "next_10y_real_cagr_pct": "n/a"})
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(OUT, "valuation_peaks.csv"), index=False)
    print("\nVALUATION PEAKS/TROUGHS -> what happened after:")
    print(t.to_string(index=False))
    return t


def main():
    breadth_from_constituents()
    tab, df = cape_forward_returns()
    peaks_and_troughs(df)
    print(f"\nCharts -> {CH}")
    print(f"CSVs   -> {OUT}")


if __name__ == "__main__":
    main()

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
    # ~11 years so the 200-day MA is valid from ~2015 (a full-decade view)
    px = yf.download(syms, start="2014-06-01", interval="1d",
                     auto_adjust=True, progress=False)["Close"]
    px = px.dropna(axis=1, how="all")
    ma60 = px.rolling(60).mean()
    ma200 = px.rolling(200).mean()
    above60 = (px > ma60).sum(axis=1) / px.notna().sum(axis=1) * 100
    above200 = (px > ma200).sum(axis=1) / px.notna().sum(axis=1) * 100
    bt = pd.DataFrame({"pct_above_60dma": above60.round(1),
                       "pct_above_200dma": above200.round(1)}).dropna()
    bt = bt[bt.index >= "2015-01-01"]
    bt.to_csv(os.path.join(OUT, "breadth_constituents.csv"))
    cur = bt.iloc[-1]
    print(f"BREADTH from {px.shape[1]} constituents, latest {bt.index[-1].date()}: "
          f">60dma {cur['pct_above_60dma']:.0f}% | >200dma {cur['pct_above_200dma']:.0f}%")

    # 2-panel chart: full decade (left) + last 12 months zoom (right)
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [2.4, 1]})
    for ax, sub, ttl in [(axL, bt, "Last ~10 years (2015-2026)"),
                         (axR, bt[bt.index >= bt.index[-1] - pd.Timedelta(days=365)], "Last 12 months")]:
        ax.plot(sub.index, sub["pct_above_60dma"], label="% > 60-day MA", lw=1.2, color="#e07b39")
        ax.plot(sub.index, sub["pct_above_200dma"], label="% > 200-day MA", lw=1.6, color="#2b6cb0")
        for lvl in (20, 50, 80):
            ax.axhline(lvl, color="grey", lw=0.5, ls=":")
        ax.set_ylim(0, 100); ax.grid(alpha=0.2); ax.set_title(ttl)
    axL.set_ylabel("% of index members"); axL.legend(loc="lower left")
    fig.suptitle("S&P 500 breadth — % of constituents above moving averages", y=1.02, fontsize=12)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "breadth_constituents.png"), dpi=110, bbox_inches="tight")
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


# ---------- recent CAPE reconstruction (Shiller mirror ends Sep-2023) ----------
def recent_cape_series(last_shiller_cape=30.8, target_today=41.3):
    """Extend CAPE from 2023-10 to now using real price (CPI cancels in CAPE):
    CAPE_t = CAPE_sep23 * (P_t/P_sep23) / (E10_t/E10_sep23), with the slow E10
    denominator grown at a constant rate CALIBRATED so the endpoint = today's
    reported CAPE (41.3). Transparent 2-anchor interpolation, not a new source."""
    g = yf.download("^GSPC", start="2023-06-01", interval="1mo",
                    auto_adjust=False, progress=False)["Close"].dropna()
    g = g.iloc[:, 0] if hasattr(g, "columns") else g
    p0 = float(g[g.index <= "2023-09-30"].iloc[-1])
    post = g[g.index > "2023-09-30"]
    n = len(post)
    m = (last_shiller_cape * (float(post.iloc[-1]) / p0) / target_today) ** (1 / n) - 1
    rows = []
    for k, (dt, px) in enumerate(post.items(), start=1):
        ym = dt.year + (dt.month - 1) / 12
        cape = last_shiller_cape * (float(px) / p0) / ((1 + m) ** k)
        rows.append({"ym": ym, "CAPE": cape})
    return pd.DataFrame(rows)


# ---------- (b) CAPE -> forward real total return ----------
def cape_forward_returns():
    df = load_shiller()
    df = df.dropna(subset=["RTR"]).reset_index(drop=True)
    rtr = df["RTR"].values
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

    cur_cape = 41.3
    hi = df[df["CAPE"] >= 34]
    print(f"\nStarting CAPE >= 34 (n={len(hi.dropna(subset=['fwd_10y']))}): "
          f"avg fwd-10y real {hi['fwd_10y'].mean():.1f}%/yr, "
          f"worst {hi['fwd_10y'].min():.1f}%, best {hi['fwd_10y'].max():.1f}%")

    # build a full CAPE series (history + reconstructed recent) for the charts
    recent = recent_cape_series()
    full = pd.concat([df[["ym", "CAPE"]], recent], ignore_index=True)

    # ===== CHART 1: scatter — full history (fwd-10y) + last-10yr (fwd-1y) =====
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 6))
    s = df.dropna(subset=["fwd_10y"])
    sc = axL.scatter(s["CAPE"], s["fwd_10y"], s=6, alpha=0.35, c=s["ym"], cmap="viridis")
    axL.axvline(cur_cape, color="red", lw=1.5, ls="--", label=f"today CAPE {cur_cape}")
    axL.axhline(0, color="grey", lw=0.6)
    axL.set_xlabel("Starting Shiller CAPE"); axL.set_ylabel("Subsequent 10-yr real return (%/yr)")
    axL.set_title("FULL HISTORY (1881-now): CAPE vs forward 10-yr return")
    axL.legend(); axL.grid(alpha=0.2)
    fig.colorbar(sc, ax=axL, label="year")
    # right: last-10-years starts (2013-2022) CAPE vs forward 1-yr real return
    rec = df[(df["ym"] >= 2013) & (df["ym"] <= 2022.8)].dropna(subset=["fwd_1y"])
    sc2 = axR.scatter(rec["CAPE"], rec["fwd_1y"], s=18, alpha=0.7, c=rec["ym"], cmap="plasma")
    axR.axhline(0, color="grey", lw=0.6)
    axR.set_xlabel("Starting Shiller CAPE"); axR.set_ylabel("Subsequent 1-yr real return (%)")
    axR.set_title("LAST ~10 YEARS (2013-2022 starts): CAPE vs forward 1-yr")
    axR.grid(alpha=0.2)
    fig.colorbar(sc2, ax=axR, label="year")
    fig.suptitle("Higher starting CAPE -> lower forward return: full history (10-yr) AND the recent decade (1-yr; note the 2021 peak preceding 2022)",
                 y=1.02, fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "cape_forward_scatter.png"), dpi=110, bbox_inches="tight")
    plt.close(fig)

    # ===== CHART 2: CAPE history — full 1881-2026 + last-10-year zoom =====
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [2.2, 1]})
    axL.plot(df["ym"], df["CAPE"], lw=0.8, color="#2b6cb0")
    axL.plot(recent["ym"], recent["CAPE"], lw=1.2, color="#c0392b")  # reconstructed tail
    axL.axhline(df["CAPE"].median(), color="green", lw=0.8, ls=":", label=f"median {df['CAPE'].median():.0f}")
    axL.axhline(cur_cape, color="red", lw=1.0, ls="--", label=f"today {cur_cape}")
    for yr, lab in [(1929.7, "1929"), (2000.0, "2000"), (2021.9, "2021")]:
        row = df.iloc[(df["ym"] - yr).abs().argmin()]
        axL.annotate(lab, (row["ym"], row["CAPE"]), fontsize=8, xytext=(row["ym"] - 6, row["CAPE"] + 2))
    axL.set_title("FULL HISTORY 1881-2026"); axL.set_ylabel("CAPE (P/E10)")
    axL.legend(loc="upper left"); axL.grid(alpha=0.2)
    # right: last 10 years
    f10 = full[full["ym"] >= 2016]
    med10 = f10["CAPE"].median()
    axR.plot(f10["ym"], f10["CAPE"], lw=1.4, color="#2b6cb0")
    axR.axhline(med10, color="green", lw=0.9, ls=":", label=f"10-yr median {med10:.0f}")
    axR.axhline(cur_cape, color="red", lw=1.0, ls="--", label=f"today {cur_cape}")
    axR.set_title("LAST ~10 YEARS (2016-2026)"); axR.grid(alpha=0.2); axR.legend(loc="upper left")
    fig.suptitle("Shiller CAPE — today 41.3 is high vs both the century and the decade (2023-26 reconstructed, red)",
                 y=1.02, fontsize=11)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "cape_history.png"), dpi=110, bbox_inches="tight")
    plt.close(fig)

    print(f"\nRecent-decade CAPE median (2016-2026): {med10:.1f}; today {cur_cape}")
    return tab, df


# ---------- (c) Equity Risk Premium: Excess CAPE Yield (rate-aware) ----------
def erp_excess_cape_yield():
    """Excess CAPE Yield (ECY) = CAPE real earnings yield (1/CAPE) - 10Y REAL yield.
    Uses Shiller's own ECY column for history (through Sep-2023), then extends to
    now anchored to that last value by the CHANGE in CAPE-yield and nominal 10Y:
      ECY_t = ECY_sep23 + (100/CAPE_t - 100/CAPE_sep23) - (TNX_t - TNX_sep23)
    (a constant inflation expectation cancels in the rate DIFFERENCE)."""
    raw = pd.read_excel(os.path.join(HERE, "ie_data.xls"), sheet_name="Data", skiprows=7)
    d = raw.iloc[:, 0].astype(str)
    yr = pd.to_numeric(d.str.split(".").str[0], errors="coerce")
    mo = pd.to_numeric(d.str.split(".").str[1].fillna("01").str.pad(2, "right", "0"), errors="coerce")
    ym = yr + (mo - 1) / 12
    ecy = pd.to_numeric(raw.iloc[:, 16], errors="coerce") * 100  # -> %
    hist = pd.DataFrame({"ym": ym, "ECY": ecy}).dropna()
    ecy_sep23 = float(hist["ECY"].iloc[-1])                       # ~1.87%
    cape_sep23 = 30.8

    recent = recent_cape_series()                                # ym, CAPE (2023-10..now)
    tnx = yf.download("^TNX", start="2023-06-01", interval="1mo",
                      auto_adjust=False, progress=False)["Close"].dropna()
    tnx = tnx.iloc[:, 0] if hasattr(tnx, "columns") else tnx
    tnx_sep23 = float(tnx[tnx.index <= "2023-09-30"].iloc[-1])
    tnx_recent = tnx[tnx.index > "2023-09-30"].reset_index(drop=True)
    rec = recent.reset_index(drop=True).copy()
    n = min(len(rec), len(tnx_recent))
    rec = rec.iloc[:n]
    rec["ECY"] = ecy_sep23 + (100 / rec["CAPE"] - 100 / cape_sep23) \
        - (tnx_recent.iloc[:n].values - tnx_sep23)
    full = pd.concat([hist[["ym", "ECY"]], rec[["ym", "ECY"]]], ignore_index=True)
    full.to_csv(os.path.join(OUT, "excess_cape_yield.csv"), index=False)
    cur = float(rec["ECY"].iloc[-1])
    print(f"\nExcess CAPE Yield now ~{cur:.1f}% (vs Sep-2023 {ecy_sep23:.1f}%; 2000 low {hist['ECY'].min():.1f}%)")

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5), gridspec_kw={"width_ratios": [2.2, 1]})
    for ax, sub, ttl in [(axL, full[full["ym"] >= 1920], "1920-2026"),
                         (axR, full[full["ym"] >= 2016], "LAST ~10 YEARS (2016-2026)")]:
        ax.plot(sub["ym"], sub["ECY"], lw=1.0, color="#6b46c1")
        ax.axhline(0, color="red", lw=0.8, ls="-", alpha=0.6)
        ax.axhline(sub["ECY"].median(), color="green", lw=0.8, ls=":", label=f"median {sub['ECY'].median():.1f}%")
        ax.axhline(cur, color="black", lw=1.0, ls="--", label=f"today ~{cur:.1f}%")
        ax.set_ylabel("Excess CAPE Yield (%)"); ax.grid(alpha=0.2); ax.set_title(ttl); ax.legend(loc="upper right")
    axL.annotate("2000 (negative!)", (2000, -1.8), fontsize=8, color="crimson")
    fig.suptitle("Equity Risk Premium (Excess CAPE Yield = real earnings yield - real 10Y): thin ~1% now, but NOT the negative 2000 extreme",
                 y=1.02, fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "erp_excess_cape_yield.png"), dpi=110, bbox_inches="tight")
    plt.close(fig)
    return cur


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
    erp_excess_cape_yield()
    peaks_and_troughs(df)
    print(f"\nCharts -> {CH}")
    print(f"CSVs   -> {OUT}")


if __name__ == "__main__":
    main()

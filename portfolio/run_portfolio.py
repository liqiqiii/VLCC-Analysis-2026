"""
Portfolio strategy study — the user's 30% gold / 30% index / 40% alpha barbell,
plus the "dividend/blue-chip" (SCHD) core tilt and the "ballast" (XLP vs low-vol
vs Treasuries) question.

CRITICAL DATA HYGIENE (Rule 4): yfinance returns Close columns sorted
ALPHABETICALLY, not in the order passed. We therefore always index by explicit
ticker name and rename ^SP500TR -> SPX. (An earlier positional rename silently
scrambled labels and produced wrong numbers — do not repeat.)

Outputs (./data/):
  core_stats_2005.csv       -- gold vs SPX since 2005 (GLD inception)
  ballast_comparison.csv    -- XLP/USMV/SPLV/SHY/BIL/SCHD/GLD vs SPX (2011+)
  correlation_matrix.csv    -- full corr matrix (2011+)
  portfolios.csv            -- candidate portfolio blends
  alpha_sensitivity.csv     -- whole-portfolio CAGR vs alpha-sleeve return

Run: python run_portfolio.py
"""
import os
import numpy as np
import pandas as pd
import yfinance as yf

OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)


def load(tickers, start):
    px = yf.download(tickers, start=start, interval="1mo",
                     auto_adjust=True, progress=False)["Close"]
    px = px.rename(columns={"^SP500TR": "SPX"})   # by NAME, never positional
    return px.dropna()


def stats(x):
    n = len(x)
    cagr = (1 + x).prod() ** (12 / n) - 1
    vol = x.std() * np.sqrt(12)
    cum = (1 + x).cumprod()
    dd = (cum / cum.cummax() - 1).min()
    return round(cagr * 100, 1), round(vol * 100, 1), round(dd * 100, 1), \
        (round(cagr / vol, 2) if vol else np.nan)


def main():
    # --- 1) core: gold vs SPX since 2005 (long window, includes 2008) ---
    core = load(["GLD", "^SP500TR"], "2005-01-01")
    rc = core.pct_change().dropna()
    rows = []
    for c in ["GLD", "SPX"]:
        a = stats(rc[c])
        rows.append({"asset": c, "CAGR_pct": a[0], "Vol_pct": a[1],
                     "MaxDD_pct": a[2], "Sharpe": a[3]})
    rows.append({"asset": "corr_GLD_SPX", "CAGR_pct": round(rc["GLD"].corr(rc["SPX"]), 2),
                 "Vol_pct": "", "MaxDD_pct": "", "Sharpe": ""})
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "core_stats_2005.csv"), index=False)
    print(f"CORE 2005+ ({rc.index[0].date()}->{rc.index[-1].date()}, {len(rc)}mo)")
    print(pd.DataFrame(rows).to_string(index=False))

    # --- 2) ballast comparison + full universe since 2011 (SCHD/USMV inception) ---
    uni = load(["XLP", "USMV", "SPLV", "SHY", "BIL", "SCHD", "GLD", "^SP500TR"], "2011-11-01")
    r = uni.pct_change().dropna()
    dn = r[r["SPX"] < 0]
    brows = []
    for c in ["BIL", "SHY", "GLD", "XLP", "SPLV", "USMV", "SCHD", "SPX"]:
        a = stats(r[c])
        brows.append({"asset": c, "CAGR_pct": a[0], "Vol_pct": a[1], "MaxDD_pct": a[2],
                      "Sharpe": a[3], "corr_SPX": round(r[c].corr(r["SPX"]), 2),
                      "down_capture_pct": round(dn[c].mean() * 100, 2)})
    bdf = pd.DataFrame(brows)
    bdf.to_csv(os.path.join(OUT, "ballast_comparison.csv"), index=False)
    print(f"\nBALLAST/UNIVERSE 2011+ ({r.index[0].date()}->{r.index[-1].date()}, {len(r)}mo)"
          f"  [avg down-SPX month = {dn['SPX'].mean()*100:.2f}%]")
    print(bdf.to_string(index=False))

    r.corr().round(2).to_csv(os.path.join(OUT, "correlation_matrix.csv"))

    # --- 3) candidate portfolios (40% held as cash proxy to isolate the beta core) ---
    cash = 0.02 / 12
    blends = {
        "A: 30GLD/30SPX/40cash":            0.30 * r.GLD + 0.30 * r.SPX + 0.40 * cash,
        "B: 30GLD/15SPX/15SCHD/40cash":     0.30 * r.GLD + 0.15 * r.SPX + 0.15 * r.SCHD + 0.40 * cash,
        "C: 30GLD/10SPX/10SCHD/10XLP/40c":  0.30 * r.GLD + 0.10 * r.SPX + 0.10 * r.SCHD + 0.10 * r.XLP + 0.40 * cash,
        "D: 25GLD/20SPX/10SCHD/5XLP/40c":   0.25 * r.GLD + 0.20 * r.SPX + 0.10 * r.SCHD + 0.05 * r.XLP + 0.40 * cash,
        "E: 60/40 (SPX/SHY)":               0.60 * r.SPX + 0.40 * r.SHY,
        "F: 100 SPX":                       r.SPX,
    }
    prows = []
    for k, p in blends.items():
        a = stats(p)
        prows.append({"portfolio": k, "CAGR_pct": a[0], "Vol_pct": a[1],
                      "MaxDD_pct": a[2], "Sharpe": a[3]})
    pdf = pd.DataFrame(prows)
    pdf.to_csv(os.path.join(OUT, "portfolios.csv"), index=False)
    print("\nCANDIDATE PORTFOLIOS (40% = cash proxy where noted; the real 40% is ALPHA)")
    print(pdf.to_string(index=False))

    # --- 4) alpha sensitivity: whole-portfolio CAGR vs alpha-sleeve return ---
    g, s = 0.08, 0.10   # forward haircut assumptions for gold, equity core
    arows = []
    for al in [-0.20, -0.10, 0.0, 0.10, 0.15, 0.20, 0.30]:
        arows.append({"alpha_sleeve_ret_pct": int(al * 100),
                      "portfolio_CAGR_pct": round((0.30 * g + 0.30 * s + 0.40 * al) * 100, 1)})
    adf = pd.DataFrame(arows)
    adf.to_csv(os.path.join(OUT, "alpha_sensitivity.csv"), index=False)
    print("\nALPHA SENSITIVITY (assumes gold 8%, equity core 10%; hurdle = 10% = just index it)")
    print(adf.to_string(index=False))

    print(f"\nWrote CSVs to {OUT}")


if __name__ == "__main__":
    main()

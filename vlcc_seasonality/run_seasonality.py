"""
VLCC seasonality study — is Q4 stock strength a CALENDAR effect (Q4 = peak TCE
season) or a RELATIVE-STRENGTH effect (how strong THIS year's Q4 rate is)?

Method
------
1. Pull DHT & FRO monthly TOTAL-return series (dividend-adjusted) from yfinance.
2. Quarterly seasonality: average/median return and win-rate by calendar quarter.
3. Monthly seasonality: average return and win-rate by calendar month (to locate
   exactly where the "winter bump" sits).
4. Cross-year test: correlate each year's Q4 stock return with that year's
   approximate Q4-average VLCC TD3C (MEG->China) TCE level.

Data quality note (Rule 4)
--------------------------
Stock data is exact (yfinance total return). The Q4 TCE levels are APPROXIMATE
annual Q4-average TD3C TCE ($k/day) compiled from public reports (Clarksons /
Baltic Exchange / company IR / trade press). They are used only to illustrate
the cross-year LEVEL relationship; the qualitative ranking (2019>2014>2022>2015
>...>2020>2021) is well established even if exact figures vary by source.

Run: python run_seasonality.py   (writes CSVs into ./data/)
"""
import os
import numpy as np
import pandas as pd
import yfinance as yf

OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)
TKS = ["DHT", "FRO"]

# Approximate Q4-average VLCC TD3C TCE, $k/day (public reports; estimates).
Q4_TCE = {2013: 45, 2014: 75, 2015: 55, 2016: 38, 2017: 26, 2018: 38,
          2019: 120, 2020: 18, 2021: 12, 2022: 65, 2023: 42, 2024: 40, 2025: 38}


def load_monthly():
    px = yf.download(TKS, start="2010-01-01", interval="1mo",
                     auto_adjust=True, progress=False)["Close"].dropna(how="all")
    return px


def quarterly_table(px, t):
    m = px[t].dropna().resample("ME").last()
    q = m.resample("QE").last().pct_change() * 100
    df = pd.DataFrame({"ret": q})
    df["year"] = df.index.year
    df["q"] = df.index.quarter
    piv = df.pivot_table(index="year", columns="q", values="ret")
    piv.columns = [f"Q{c}" for c in piv.columns]
    return piv.round(1)


def monthly_seasonality(px, t):
    m = px[t].dropna().resample("ME").last().pct_change() * 100
    df = pd.DataFrame({"r": m})
    df["mon"] = df.index.month
    out = pd.DataFrame({
        "avg_ret_pct": df.groupby("mon")["r"].mean().round(1),
        "median_ret_pct": df.groupby("mon")["r"].median().round(1),
        "pct_positive": (df.assign(p=df.r > 0).groupby("mon")["p"].mean() * 100).round(0),
    })
    return out


def q4_returns(px, t):
    m = px[t].dropna().resample("ME").last()
    q = m.resample("QE").last().pct_change() * 100
    return {ix.year: round(v, 1) for ix, v in q[q.index.quarter == 4].items()}


def corr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = ~np.isnan(a) & ~np.isnan(b)
    return round(float(np.corrcoef(a[m], b[m])[0, 1]), 2)


def main():
    px = load_monthly()

    # 1) quarterly tables + seasonality summary
    seas_rows = []
    for t in TKS:
        piv = quarterly_table(px, t)
        piv.to_csv(os.path.join(OUT, f"quarterly_returns_{t}.csv"))
        for qc in ["Q1", "Q2", "Q3", "Q4"]:
            col = piv[qc].dropna()
            seas_rows.append({
                "ticker": t, "quarter": qc,
                "avg_pct": round(col.mean(), 1),
                "median_pct": round(col.median(), 1),
                "pct_positive": round((col > 0).mean() * 100, 0),
                "n": int(col.count()),
            })
    seas = pd.DataFrame(seas_rows)
    seas.to_csv(os.path.join(OUT, "quarterly_seasonality.csv"), index=False)

    # 2) monthly seasonality
    for t in TKS:
        monthly_seasonality(px, t).to_csv(os.path.join(OUT, f"monthly_seasonality_{t}.csv"))

    # 3) cross-year Q4 TCE vs Q4 stock-return correlation
    dht, fro = q4_returns(px, "DHT"), q4_returns(px, "FRO")
    rows = []
    for y in sorted(Q4_TCE):
        rows.append({"year": y, "q4_tce_k_per_day": Q4_TCE[y],
                     "DHT_Q4_ret_pct": dht.get(y, np.nan),
                     "FRO_Q4_ret_pct": fro.get(y, np.nan)})
    q4 = pd.DataFrame(rows)
    q4.to_csv(os.path.join(OUT, "q4_tce_vs_stock.csv"), index=False)

    c_dht = corr(q4["q4_tce_k_per_day"], q4["DHT_Q4_ret_pct"])
    c_fro = corr(q4["q4_tce_k_per_day"], q4["FRO_Q4_ret_pct"])

    print("=== Quarterly seasonality ===")
    print(seas.to_string(index=False))
    print("\n=== Q4 TCE level vs Q4 stock return ===")
    print(q4.to_string(index=False))
    print(f"\ncorr(Q4 TCE level, DHT Q4 ret) = {c_dht}")
    print(f"corr(Q4 TCE level, FRO Q4 ret) = {c_fro}")

    pd.DataFrame([
        {"pair": "Q4_TCE_vs_DHT_Q4", "pearson_r": c_dht},
        {"pair": "Q4_TCE_vs_FRO_Q4", "pearson_r": c_fro},
    ]).to_csv(os.path.join(OUT, "q4_correlation.csv"), index=False)
    print(f"\nWrote CSVs to {OUT}")


if __name__ == "__main__":
    main()

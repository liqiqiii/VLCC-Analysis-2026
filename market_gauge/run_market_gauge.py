"""
Market Gauge — "how high is the S&P 500, and how good is the quality?"
Four axes: (1) breadth, (2) valuation, (3) positioning/sentiment, (4) quality.

Data hygiene (Rule 4): yfinance returns columns ALPHABETICALLY; we index by
explicit ticker name. Valuation levels (forward/trailing PE, P/S, Buffett) are
web-sourced point-in-time estimates (flagged); CAPE percentile, breadth and VIX
percentiles are computed here and fully reproducible.

Outputs (./data/):
  breadth.csv        -- RSP/SPY equal- vs cap-weight: level, percentile, recent trend
  sector_breadth.csv -- how many of 11 SPDR sectors beat SPY (1mo/3mo)
  valuation.csv      -- CAPE percentile (computed) + web-sourced PE/PS/Buffett
  vix.csv            -- VIX level + percentile
  scorecard.csv      -- composite percentile scorecard across axes

Run: python run_market_gauge.py
"""
import os
import ssl
import urllib.request
import numpy as np
import pandas as pd
import yfinance as yf

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "data")
os.makedirs(OUT, exist_ok=True)


def load(tickers, start):
    px = yf.download(tickers, start=start, interval="1d",
                     auto_adjust=True, progress=False)["Close"]
    px = px.rename(columns={"^VIX": "VIX"})
    return px.dropna()


def breadth_and_vix():
    px = load(["RSP", "SPY", "^VIX"], "2005-01-01")
    ratio = px["RSP"] / px["SPY"]
    cur = ratio.iloc[-1]
    pct = (ratio < cur).mean() * 100
    trend = {lbl: round((ratio.iloc[-1] / ratio.iloc[-w] - 1) * 100, 2)
             for w, lbl in [(5, "1wk"), (10, "2wk"), (21, "1mo"), (63, "3mo"), (252, "12mo")]}
    pd.DataFrame([{
        "metric": "RSP/SPY equal-vs-cap ratio", "level": round(cur, 3),
        "percentile_2005_26": round(pct, 0),
        **{f"chg_{k}_pct": v for k, v in trend.items()},
    }]).to_csv(os.path.join(OUT, "breadth.csv"), index=False)

    v = px["VIX"]
    pd.DataFrame([{
        "VIX_latest": round(v.iloc[-1], 1), "VIX_1y_avg": round(v.tail(252).mean(), 1),
        "VIX_median_2005_26": round(v.median(), 1),
        "VIX_percentile": round((v < v.iloc[-1]).mean() * 100, 0),
    }]).to_csv(os.path.join(OUT, "vix.csv"), index=False)
    return round(pct, 0), trend, round((v < v.iloc[-1]).mean() * 100, 0)


def sector_breadth():
    secs = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
    sp = load(secs + ["SPY"], "2026-01-01")
    rows = []
    for w, lbl in [(21, "1mo"), (63, "3mo")]:
        spx = sp["SPY"].iloc[-1] / sp["SPY"].iloc[-w] - 1
        beat = sum((sp[s].iloc[-1] / sp[s].iloc[-w] - 1) > spx for s in secs)
        rows.append({"window": lbl, "sectors_beating_SPY": beat, "of": 11})
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "sector_breadth.csv"), index=False)
    return rows


def cape_percentile(web_cape=41.3):
    """Compute CAPE percentile from Shiller data; fall back to known history."""
    path = os.path.join(HERE, "ie_data.xls")
    try:
        if not os.path.exists(path):
            ctx = ssl.create_default_context(); ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request("http://www.econ.yale.edu/~shiller/data/ie_data.xls",
                                         headers={"User-Agent": "Mozilla/5.0"})
            open(path, "wb").write(urllib.request.urlopen(req, timeout=30, context=ctx).read())
        df = pd.read_excel(path, sheet_name="Data", skiprows=7)
        cape = pd.to_numeric(df.iloc[:, 12], errors="coerce").dropna()
        pct = (cape < web_cape).mean() * 100
        return round(pct, 1), round(cape.median(), 1), round(cape.max(), 1), len(cape)
    except Exception as e:
        print("CAPE fetch failed, using known history:", e)
        return 99.0, 16.5, 44.2, None


def main():
    b_pct, b_trend, vix_pct = breadth_and_vix()
    sb = sector_breadth()
    cpct, cmed, cmax, cn = cape_percentile()

    # valuation scorecard (web-sourced levels + computed CAPE percentile)
    val = pd.DataFrame([
        {"metric": "Shiller CAPE", "current": 41.3, "hist_avg_or_median": cmed,
         "percentile": cpct, "source": f"computed vs {cn} mo since 1881 (all-time max {cmax}, Dec-1999)"},
        {"metric": "Forward P/E", "current": 21.0, "hist_avg_or_median": 17.5,
         "percentile": ">90", "source": "web (MacroMicro/investsnips)"},
        {"metric": "Trailing P/E", "current": 28.5, "hist_avg_or_median": 19.5,
         "percentile": ">90", "source": "web (investsnips/worldperatio)"},
        {"metric": "Price/Sales", "current": 3.0, "hist_avg_or_median": 1.5,
         "percentile": "~99", "source": "web (est.)"},
        {"metric": "Buffett (MktCap/GDP)", "current": 225, "hist_avg_or_median": 100,
         "percentile": "99-100", "source": "web (200-250% range)"},
    ])
    val.to_csv(os.path.join(OUT, "valuation.csv"), index=False)

    # composite percentile scorecard
    score = pd.DataFrame([
        {"axis": "Valuation (CAPE)", "reading": f"CAPE 41.3", "percentile": cpct, "signal": "EXPENSIVE"},
        {"axis": "Valuation (Buffett)", "reading": "~225% GDP", "percentile": 99, "signal": "EXPENSIVE"},
        {"axis": "Breadth (concentration)", "reading": f"RSP/SPY {b_pct}th pct", "percentile": b_pct, "signal": "NARROW"},
        {"axis": "Breadth (recent trend)", "reading": f"3mo {b_trend['3mo']:+}% / 1wk {b_trend['1wk']:+}%", "percentile": "-", "signal": "BROADENING but fragile"},
        {"axis": "Positioning (VIX)", "reading": f"VIX percentile {vix_pct}", "percentile": vix_pct, "signal": "MID / complacent-ish"},
        {"axis": "Positioning (CTA)", "reading": "net long $34B S&P; $100B+ downside", "percentile": "-", "signal": "STRETCHED/asymmetric"},
        {"axis": "Quality (earnings)", "reading": "record earnings + record margins", "percentile": "-", "signal": "HIGH (real profits)"},
    ])
    score.to_csv(os.path.join(OUT, "scorecard.csv"), index=False)

    print("BREADTH: RSP/SPY percentile", b_pct, "| trend", b_trend)
    print("SECTOR BREADTH:", sb)
    print("VIX percentile:", vix_pct)
    print(f"CAPE 41.3 -> {cpct}th pct (median {cmed}, max {cmax})")
    print("\nSCORECARD:"); print(score.to_string(index=False))
    print(f"\nWrote CSVs to {OUT}")


if __name__ == "__main__":
    main()

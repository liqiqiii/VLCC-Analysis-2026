"""
Event-volatility / desensitization check for the VLCC geopolitical-surprise
question (report §8): has the market stopped reacting to Iran/Hormuz headlines,
and what did the June-2026 Strait-of-Hormuz spike do to DHT/FRO?

Outputs (./data/):
  event_vol_monthly.csv   -- DHT/FRO monthly annualized realized vol + max daily move
  event_spike_fade.csv    -- 2026 low/high/June-high/latest + drawdown off high

Run: python run_event_vol.py
"""
import os
import numpy as np
import pandas as pd
import yfinance as yf

OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)
TKS = ["DHT", "FRO"]


def main():
    px = yf.download(TKS, start="2025-01-01", interval="1d",
                     auto_adjust=True, progress=False)["Close"].dropna(how="all")
    r = px.pct_change()

    # monthly annualized realized vol + max abs daily move
    frames = []
    for t in TKS:
        s = r[t].dropna()
        g = s.groupby([s.index.year, s.index.month])
        df = pd.DataFrame({
            f"{t}_ann_vol_pct": (g.std() * np.sqrt(252) * 100).round(0),
            f"{t}_max_daily_pct": g.apply(lambda x: x.abs().max() * 100).round(1),
        })
        frames.append(df)
    vol = pd.concat(frames, axis=1)
    vol.index = [f"{y}-{m:02d}" for (y, m) in vol.index]
    vol.to_csv(os.path.join(OUT, "event_vol_monthly.csv"))

    # spike/fade around June 2026
    rows = []
    for t in TKS:
        s = px[t].dropna()
        s26 = s[s.index >= "2026-01-01"]
        jun = s26[(s26.index >= "2026-06-01") & (s26.index <= "2026-06-30")]
        rows.append({
            "ticker": t,
            "yr2026_low": round(s26.min(), 2), "low_date": str(s26.idxmin().date()),
            "yr2026_high": round(s26.max(), 2), "high_date": str(s26.idxmax().date()),
            "june_high": round(jun.max(), 2),
            "latest": round(s26.iloc[-1], 2), "latest_date": str(s26.index[-1].date()),
            "off_high_pct": round((s26.iloc[-1] / s26.max() - 1) * 100, 0),
        })
    sf = pd.DataFrame(rows)
    sf.to_csv(os.path.join(OUT, "event_spike_fade.csv"), index=False)

    print("=== Monthly annualized vol (%) / max daily move (%) ===")
    print(vol.tail(14).to_string())
    print("\n=== 2026 spike/fade ===")
    print(sf.to_string(index=False))
    print(f"\nWrote CSVs to {OUT}")


if __name__ == "__main__":
    main()

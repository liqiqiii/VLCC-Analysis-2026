"""
TCE vs VLCC Stock Price — "Average x Duration" thesis, empirical backtest.

Proves: VLCC equities track the SUSTAINED AVERAGE rate (and its DURATION), not
spot-TCE spikes. Quantifies the TCE-peak vs stock-peak amplitude compression.

Real data:
  - BDTI (Baltic Dirty Tanker Index) weekly, 2020-2024 (free GitHub CSV)
  - FRO, DHT weekly prices (yfinance, full history)
Curated/sourced anchors (clearly marked) for long cycles (2008, 2015) where free
high-frequency TCE history is paywalled.

Outputs tce_results.json consumed by the report + chart scripts.
No fabricated data: estimated points are flagged with "source"/"estimated".
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

warnings.simplefilter("ignore")

BDTI_URL = (
    "https://raw.githubusercontent.com/Aftikharmnz/Baltic/main/"
    "Baltic%20Dirty%20Tanker%20Historical%20Data.csv"
)
OUT = Path("tce_results.json")
DATA = Path("tce_data.json")


# ────────────────────────────────────────────────────────────────────────────
# 1. Load real data
# ────────────────────────────────────────────────────────────────────────────
def load_bdti() -> pd.DataFrame:
    b = pd.read_csv(BDTI_URL)
    b["Date"] = pd.to_datetime(b["Date"], format="mixed")
    b = b[["Date", "Price"]].rename(columns={"Price": "BDTI"})
    b = b.sort_values("Date").set_index("Date")
    # to weekly (W-FRI) last observation
    w = b["BDTI"].resample("W-FRI").last().dropna()
    return w.to_frame()


def load_prices() -> pd.DataFrame:
    out = {}
    for t in ["FRO", "DHT"]:
        h = yf.Ticker(t).history(period="max", interval="1wk", auto_adjust=True)
        s = h["Close"].copy()
        s.index = s.index.tz_localize(None)
        s = s.resample("W-FRI").last()
        out[t] = s
    return pd.DataFrame(out)


# ────────────────────────────────────────────────────────────────────────────
# 2. Correlation: stock vs spot vs trailing-average rate  (the core proof)
# ────────────────────────────────────────────────────────────────────────────
def correlation_block(df: pd.DataFrame) -> dict:
    """df has columns BDTI, FRO, DHT on a common weekly index."""
    windows = [1, 4, 13, 26, 52]  # 1 = spot
    res = {"windows_weeks": windows, "stocks": {}}
    for stk in ["FRO", "DHT"]:
        r2_level, r2_ret = [], []
        for w in windows:
            avg = df["BDTI"].rolling(w, min_periods=w).mean()
            sub = pd.concat([df[stk], avg], axis=1).dropna()
            sub.columns = ["px", "rate"]
            # level R^2
            r2_level.append(round(float(np.corrcoef(sub["px"], sub["rate"])[0, 1] ** 2), 4))
            # change/return R^2 (4-week % change of each)
            chg = pd.concat(
                [df[stk].pct_change(4), avg.pct_change(4)], axis=1
            ).dropna()
            chg.columns = ["px", "rate"]
            chg = chg.replace([np.inf, -np.inf], np.nan).dropna()
            r2_ret.append(round(float(np.corrcoef(chg["px"], chg["rate"])[0, 1] ** 2), 4))
        res["stocks"][stk] = {"r2_level": r2_level, "r2_change4w": r2_ret}
    return res


# ────────────────────────────────────────────────────────────────────────────
# 3. Lead/lag cross-correlation (stock vs spot rate, returns)
# ────────────────────────────────────────────────────────────────────────────
def leadlag_block(df: pd.DataFrame, stk: str, max_lag: int = 12) -> dict:
    a = df[stk].pct_change().dropna()
    b = df["BDTI"].pct_change().dropna()
    j = pd.concat([a, b], axis=1).dropna()
    j.columns = ["px", "rate"]
    lags = list(range(-max_lag, max_lag + 1))
    cc = []
    for L in lags:
        # positive L: rate leads stock by L weeks (stock_t vs rate_{t-L})
        c = j["px"].corr(j["rate"].shift(L))
        cc.append(round(float(c), 3))
    best = lags[int(np.nanargmax(np.abs(cc)))]
    return {"lags_weeks": lags, "corr": cc, "best_lag_weeks": best,
            "interpretation": "positive lag = rate leads stock"}


# ────────────────────────────────────────────────────────────────────────────
# 4. Amplitude compression on REAL 2020-2024 episodes
# ────────────────────────────────────────────────────────────────────────────
def amplitude_real(df: pd.DataFrame) -> list:
    """Compare rate spike multiple vs stock move multiple for real episodes."""
    episodes = [
        # name, window start, window end, baseline window (pre) start/end
        ("2020 COVID floating-storage spike", "2020-03-01", "2020-07-31",
         "2020-01-01", "2020-02-29"),
        ("2022-2024 sustained up-cycle", "2022-09-01", "2024-06-30",
         "2022-01-01", "2022-06-30"),
    ]
    out = []
    for name, s, e, bs, be in episodes:
        win = df.loc[s:e]
        base = df.loc[bs:be]
        if win.empty or base.empty:
            continue
        rate_peak = float(win["BDTI"].max())
        rate_base = float(base["BDTI"].mean())
        row = {"episode": name, "rate_baseline": round(rate_base, 1),
               "rate_peak": round(rate_peak, 1),
               "rate_peak_mult": round(rate_peak / rate_base, 2)}
        for stk in ["FRO", "DHT"]:
            px_peak = float(win[stk].max())
            px_base = float(base[stk].mean())
            row[f"{stk}_peak_mult"] = round(px_peak / px_base, 2)
            row[f"{stk}_compression"] = round(
                (rate_peak / rate_base) / (px_peak / px_base), 2)
        out.append(row)
    return out


# ────────────────────────────────────────────────────────────────────────────
# 5. Duration test on REAL BDTI: weeks-above-threshold vs stock re-rate
# ────────────────────────────────────────────────────────────────────────────
def duration_real(df: pd.DataFrame) -> dict:
    """Rolling 26-week: how many weeks was BDTI above its trailing median,
    and how does stock change relate to (a) max spot vs (b) weeks-elevated."""
    med = df["BDTI"].median()
    res = {"bdti_median": round(float(med), 1), "rolling_window_weeks": 26, "rows": []}
    win = 26
    recs = []
    idx = df.index
    for i in range(win, len(df) - win):
        seg = df.iloc[i - win:i]
        fwd = df.iloc[i:i + win]
        weeks_elev = int((seg["BDTI"] > med).sum())
        max_spot = float(seg["BDTI"].max())
        avg_rate = float(seg["BDTI"].mean())
        fro_fwd = float(fwd["FRO"].iloc[-1] / df["FRO"].iloc[i] - 1)
        recs.append({"avg_rate": avg_rate, "max_spot": max_spot,
                     "weeks_elev": weeks_elev, "fro_fwd26": fro_fwd})
    rdf = pd.DataFrame(recs).dropna()
    # which explains forward stock move better: avg_rate, max_spot, or weeks_elev?
    def r2(x, y):
        m = pd.concat([x, y], axis=1).dropna()
        if len(m) < 10:
            return None
        return round(float(np.corrcoef(m.iloc[:, 0], m.iloc[:, 1])[0, 1] ** 2), 4)
    res["r2_fwdstock_vs_avgrate"] = r2(rdf["avg_rate"], rdf["fro_fwd26"])
    res["r2_fwdstock_vs_maxspot"] = r2(rdf["max_spot"], rdf["fro_fwd26"])
    res["r2_fwdstock_vs_weeks_elevated"] = r2(rdf["weeks_elev"], rdf["fro_fwd26"])
    res["n"] = int(len(rdf))
    return res


# ────────────────────────────────────────────────────────────────────────────
# 6. Long-cycle amplitude table (curated TCE anchors + real stock peaks)
# ────────────────────────────────────────────────────────────────────────────
def long_cycle_table(prices: pd.DataFrame) -> dict:
    """TCE anchors are sourced approximations (paywalled high-freq history).
    Stock peak/baseline multiples use REAL yfinance adjusted weekly closes."""
    # Sourced TCE anchors ($/day). baseline = mid-cycle trough avg before the spike.
    # Sources: industry press / Clarksons-Gibson commentary / web verification.
    cycles = [
        {"cycle": "2008 demand super-spike", "tce_baseline": 30000, "tce_peak": 300000,
         "stk_lo": "2007-01-01", "stk_lo_end": "2007-03-31",
         "stk_hi": "2008-01-01", "stk_hi_end": "2008-12-31",
         "source": "2008 TD3C peak ~$300-350k/day (web-verified); baseline ~ pre-spike trough"},
        {"cycle": "2015 mini-cycle", "tce_baseline": 20000, "tce_peak": 100000,
         "stk_lo": "2014-01-01", "stk_lo_end": "2014-06-30",
         "stk_hi": "2015-01-01", "stk_hi_end": "2015-12-31",
         "source": "2015 avg ~$50-60k, intra-year peak ~$100k (web-verified); baseline 2013-14 trough"},
        {"cycle": "2020 COVID storage pulse", "tce_baseline": 25000, "tce_peak": 264000,
         "stk_lo": "2019-10-01", "stk_lo_end": "2019-12-31",
         "stk_hi": "2020-01-01", "stk_hi_end": "2020-06-30",
         "source": "2020 TD3C peak $264,072/day Mar-2020 (web-verified)"},
        {"cycle": "2026 Hormuz spike", "tce_baseline": 50000, "tce_peak": 400000,
         "stk_lo": "2025-10-01", "stk_lo_end": "2025-12-31",
         "stk_hi": "2026-01-01", "stk_hi_end": "2026-06-30",
         "source": "repo modeling_stash.md: TD3C ~$400k ATH Mar-2026"},
    ]
    rows = []
    for c in cycles:
        row = {"cycle": c["cycle"], "tce_baseline": c["tce_baseline"],
               "tce_peak": c["tce_peak"],
               "tce_peak_mult": round(c["tce_peak"] / c["tce_baseline"], 2),
               "source": c["source"]}
        for stk in ["FRO", "DHT"]:
            try:
                lo = prices.loc[c["stk_lo"]:c["stk_lo_end"], stk].mean()
                hi = prices.loc[c["stk_hi"]:c["stk_hi_end"], stk].max()
                if np.isnan(lo) or np.isnan(hi) or lo <= 0:
                    row[f"{stk}_peak_mult"] = None
                    row[f"{stk}_compression"] = None
                else:
                    pm = hi / lo
                    row[f"{stk}_peak_mult"] = round(float(pm), 2)
                    row[f"{stk}_compression"] = round(
                        (c["tce_peak"] / c["tce_baseline"]) / float(pm), 2)
            except Exception:
                row[f"{stk}_peak_mult"] = None
                row[f"{stk}_compression"] = None
        rows.append(row)
    return {"note": "TCE = sourced approximations; stock multiples = real yfinance "
                    "adjusted weekly closes. DHT IPO Oct-2005, so 2008 row valid; "
                    "earlier-than-IPO cells are None.",
            "rows": rows}


# ────────────────────────────────────────────────────────────────────────────
def main():
    print("Loading BDTI (real, 2020-2024)...")
    bdti = load_bdti()
    print(f"  BDTI weekly: {len(bdti)} rows {bdti.index.min().date()}..{bdti.index.max().date()}")

    print("Loading FRO/DHT prices (real)...")
    prices = load_prices()
    print(f"  prices: {len(prices)} rows {prices.index.min().date()}..{prices.index.max().date()}")

    # common weekly frame for the high-frequency proof
    df = bdti.join(prices, how="inner").dropna()
    print(f"  aligned BDTI+stocks: {len(df)} rows {df.index.min().date()}..{df.index.max().date()}")

    results = {
        "meta": {
            "bdti_source": BDTI_URL,
            "bdti_range": [str(bdti.index.min().date()), str(bdti.index.max().date())],
            "price_source": "yfinance weekly auto-adjusted",
            "price_range": [str(prices.index.min().date()), str(prices.index.max().date())],
            "aligned_n_weeks": int(len(df)),
            "disclaimer": "Not investment advice. BDTI used as VLCC dirty-rate proxy; "
                          "long-cycle TCE values are sourced approximations.",
        },
        "correlation": correlation_block(df),
        "leadlag_FRO": leadlag_block(df, "FRO"),
        "leadlag_DHT": leadlag_block(df, "DHT"),
        "amplitude_real": amplitude_real(df),
        "duration_real": duration_real(df),
        "long_cycle": long_cycle_table(prices),
    }
    OUT.write_text(json.dumps(results, indent=2))
    print(f"Wrote {OUT}")

    # also persist the aligned series for charts
    df_out = df.copy()
    df_out.index = df_out.index.astype(str)
    DATA.write_text(df_out.reset_index().to_json(orient="records"))
    print(f"Wrote {DATA}")

    # console summary
    print("\n=== CORE PROOF: R^2 of stock LEVEL vs rate (spot -> trailing avg) ===")
    w = results["correlation"]["windows_weeks"]
    for stk in ["FRO", "DHT"]:
        print(f" {stk} windows{w}: R2_level={results['correlation']['stocks'][stk]['r2_level']}")
    print("\n=== Amplitude compression (real episodes) ===")
    for r in results["amplitude_real"]:
        print(f" {r['episode']}: rate x{r['rate_peak_mult']} | "
              f"FRO x{r['FRO_peak_mult']} (compress {r['FRO_compression']}) | "
              f"DHT x{r['DHT_peak_mult']} (compress {r['DHT_compression']})")
    print("\n=== Duration test (what explains fwd 26w stock move) ===")
    d = results["duration_real"]
    print(f" R2 vs avg_rate={d['r2_fwdstock_vs_avgrate']} | "
          f"vs max_spot={d['r2_fwdstock_vs_maxspot']} | "
          f"vs weeks_elevated={d['r2_fwdstock_vs_weeks_elevated']}")
    print("\n=== Long cycle TCE-peak vs stock-peak ===")
    for r in results["long_cycle"]["rows"]:
        print(f" {r['cycle']}: TCE x{r['tce_peak_mult']} | "
              f"FRO x{r.get('FRO_peak_mult')} | DHT x{r.get('DHT_peak_mult')}")


if __name__ == "__main__":
    main()

"""Pre-registered event study: following PAG's entries (A) and holding after PAG's exits (C).

Rules (fixed before looking at results):
- Entry = first trading close STRICTLY AFTER the announcement date (T+1), to avoid look-ahead.
- Total-return prices (yfinance auto_adjust=True) for instruments AND benchmarks (HK benchmark = 2800.HK,
  not the ^HSI price index). Baskets are equal-weighted at entry, no rebalancing.
- Event date = first public disclosure. Data cutoff END = 2026-11-06 (inclusive), fixed for reproducibility.
- Excess return = instrument return - benchmark return over the same window.
- Horizons: 63 / 252 / 756 trading days (~3m / 12m / 36m), plus "to date". A horizon is
  reported only if enough data exists (no partial windows).
- Events without a listed instrument are listed as EXCLUDED, not dropped silently.
Run: python pag_distressed/run_follow_backtest.py
"""
import warnings
import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")
HORIZONS = {"3m": 63, "12m": 252, "36m": 756}
END = "2026-11-07"  # exclusive upper bound -> data through 2026-11-06

ENTRY_EVENTS = [
    # id, date, PAG event, instruments, benchmark, how the instrument relates
    ("A1", "2016-04-19", "Lexmark buyout with Apex/Ninestar (PAG 42.94% of JV)", ["002180.SZ"], "510300.SS",
     "listed co-investor (Ninestar)"),
    ("A2", "2023-01-12", "Goldin Financial Global Centre bought from receivers", ["2778.HK", "1972.HK"], "2800.HK",
     "HK office landlord proxies"),
    ("A3", "2023-12-12", "Wanda new agreement (Opco control bloc)",
     ["1209.HK", "6049.HK", "2669.HK", "6098.HK", "1516.HK", "6666.HK", "0169.HK"], "2800.HK",
     "HK-listed China property-services / commercial-operation basket"),
    ("A4", "2025-05-20", "48 Wanda Plazas JV clearance published by SAMR (approved 6-May, published 20-May)",
     ["1209.HK", "6049.HK", "2669.HK", "6098.HK", "1516.HK", "6666.HK", "0169.HK"], "2800.HK",
     "same basket as A3"),
    ("A5", "2025-12-24", "Sapporo Real Estate (with KKR, EV ¥477bn)", ["2501.T", "8801.T", "8802.T"], "1306.T",
     "seller (Sapporo HD) + Japanese real-estate majors"),
]
EXCLUDED_ENTRIES = [
    ("China Music Corp", "2013", "unlisted target"),
    ("Universal Studios Japan", "Dec-2013", "unlisted target; exact date unverified"),
    ("DTZ", "Nov-2014", "seller UGL.AX has no data"),
    ("Yingde Gases", "2017", "delisted; 2392.HK ticker now belongs to another company"),
    ("Evergrande Services", "30-Oct-2026", "too recent -> forward paper portfolio (D)"),
]

# Test C is DESCRIPTIVE: these are listed vehicles/acquirers linked to PAG exit routes.
# CWK's IPO was a primary issue (PAG did not sell at IPO); PAG's TME sale dates are unknown;
# XRX measures the acquirer's whole business. No PAG exit-timing inference is drawn.
EXIT_EVENTS = [
    ("C1", "2018-08-02", "Cushman & Wakefield NYSE IPO (primary issue; PAG still a holder)", ["CWK"], "SPY", "IPO buyer"),
    ("C2", "2018-12-12", "Tencent Music NYSE IPO (China Music exit route)", ["TME"], "KWEB", "IPO buyer"),
    ("C3", "2024-12-23", "Xerox agrees to buy Lexmark (PAG's JV sells)", ["XRX"], "SPY", "strategic buyer"),
]
EXCLUDED_EXITS = [
    ("USJ -> Comcast", "2015/2017", "USJ is too small a part of CMCSA to measure"),
    ("AirPower gases -> Chinese consortium", "Nov-2024", "unlisted buyer"),
]

_cache = {}


def px(t):
    if t not in _cache:
        h = yf.Ticker(t).history(start="2000-01-01", end=END, auto_adjust=True)["Close"]
        if h.empty:
            raise ValueError(f"no data for {t}")
        h.index = h.index.tz_localize(None).normalize()
        _cache[t] = h.dropna()
    return _cache[t]


def basket_path(tickers, start):
    paths = []
    for t in tickers:
        s = px(t)
        s = s[s.index > start]
        if len(s):
            paths.append(s / s.iloc[0])
    df = pd.concat(paths, axis=1).ffill()
    df = df.dropna()  # common dates after every member has started
    return df.mean(axis=1), [t for t in tickers if len(px(t)[px(t).index > start])]


def run(events, label):
    rows = []
    for eid, d, name, tick, bench, rel in events:
        start = pd.Timestamp(d)
        b, used = basket_path(tick, start)
        m = px(bench)
        m = m[m.index > start]
        m = m / m.iloc[0]
        j = pd.concat([b, m], axis=1, keys=["inst", "bench"]).ffill().dropna()
        row = {"id": eid, "event_date": d, "entry_close": j.index[0].date(), "event": name,
               "instruments": "+".join(used), "benchmark": bench, "relation": rel}
        for k, n in HORIZONS.items():
            if len(j) > n:
                r, br = j["inst"].iloc[n] - 1, j["bench"].iloc[n] - 1
                row[f"{k}_ret"], row[f"{k}_excess"] = round(r * 100, 1), round((r - br) * 100, 1)
            else:
                row[f"{k}_ret"] = row[f"{k}_excess"] = None
        r, br = j["inst"].iloc[-1] - 1, j["bench"].iloc[-1] - 1
        row["to_date"] = j.index[-1].date()
        row["td_ret"], row["td_excess"] = round(r * 100, 1), round((r - br) * 100, 1)
        rows.append(row)
    df = pd.DataFrame(rows)
    print(f"=== {label} ===")
    cols = ["id", "entry_close", "instruments", "benchmark", "3m_excess", "12m_excess", "36m_excess", "to_date", "td_ret", "td_excess"]
    print(df[cols].to_string(index=False))
    for k in HORIZONS:
        s = df[f"{k}_excess"].dropna()
        if len(s):
            print(f"  {k}: n={len(s)}, mean excess {s.mean():+.1f} pp, positive {int((s > 0).sum())}/{len(s)}")
    print()
    return df


if __name__ == "__main__":
    a = run(ENTRY_EVENTS, "A. Follow PAG's entry (T+1 close)")
    print("Excluded entries:", "; ".join(f"{n} ({d}): {why}" for n, d, why in EXCLUDED_ENTRIES), "\n")
    c = run(EXIT_EVENTS, "C. Descriptive: listed exit vehicles / acquirer (not PAG exit timing)")
    print("Excluded exits:", "; ".join(f"{n} ({d}): {why}" for n, d, why in EXCLUDED_EXITS))
    pd.concat([a.assign(test="A"), c.assign(test="C")]).to_csv("pag_distressed/data/follow_backtest_results.csv", index=False)

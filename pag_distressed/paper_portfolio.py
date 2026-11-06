"""Out-of-sample paper portfolio (test D), pre-registered on 6-Nov-2026.

Hypothesis: PAG's control bid for Evergrande Property Services (announced 30-Oct-2026)
signals a turn for HK-listed China property-services stocks, so a basket bought now
should beat the Tracker Fund over 3 / 12 / 24 / 36 months.

Fixed rules (do NOT change after inception; any change must be a new, separately dated test):
- Inception = official HK close on 2026-11-06 (captured after the close settled; manifest in
  data/paper_portfolio_start.csv, whose SHA-256 is printed in report #51 and fixed by git history).
- Equal weight HK$100,000 per name, no rebalancing, dividends reinvested (Yahoo total-return prices).
- Basket: 6666.HK, 1209.HK, 6049.HK, 2669.HK, 6098.HK, 1516.HK. Benchmark: 2800.HK.
- Valuation date for a review = the first common HK trading close ON OR AFTER the review date:
  2027-02-06 (+3m), 2027-11-06 (+12m), 2028-11-06 (+24m), 2029-11-06 (+36m).
- Success = basket beats 2800.HK at +12m AND +36m. Failures are reported as prominently as successes.
- The PAG offer for 6666 (HK$0.8359) is not executable until the deal completes.

Usage:
  python pag_distressed/paper_portfolio.py init                  # once; refuses to overwrite
  python pag_distressed/paper_portfolio.py mark [YYYY-MM-DD]     # valuation on/after that date (default: latest)
"""
import csv
import os
import sys
import warnings
from datetime import date

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")
INCEPTION = "2026-11-06"
BASKET = ["6666.HK", "1209.HK", "6049.HK", "2669.HK", "6098.HK", "1516.HK"]
BENCH = "2800.HK"
NOTIONAL = 100_000
TOL = 0.005  # max allowed gap between stored and re-fetched raw inception close
D = os.path.join(os.path.dirname(__file__), "data")
START = os.path.join(D, "paper_portfolio_start.csv")
LOG = os.path.join(D, "paper_portfolio_log.csv")


def fetch(t):
    h = yf.Ticker(t).history(start=INCEPTION, auto_adjust=False)[["Close", "Adj Close"]].dropna()
    h.index = pd.to_datetime(h.index).tz_localize(None).normalize()
    if h.empty or h.index[0] != pd.Timestamp(INCEPTION):
        raise SystemExit(f"{t}: no close on inception date {INCEPTION}")
    return h


def init():
    if os.path.exists(START):
        raise SystemExit("paper_portfolio_start.csv exists; inception is fixed and will not be overwritten")
    with open(START, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ticker", "role", "inception_date", "inception_close_raw", "notional_hkd"])
        for t in BASKET + [BENCH]:
            raw = fetch(t)["Close"].iloc[0]
            w.writerow([t, "benchmark" if t == BENCH else "basket", INCEPTION, round(float(raw), 4),
                        NOTIONAL * (len(BASKET) if t == BENCH else 1)])
    print(f"Initialised {START}")


def manifest():
    with open(START, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    tick = [r["ticker"] for r in rows]
    if tick != BASKET + [BENCH] or any(r["inception_date"] != INCEPTION for r in rows):
        raise SystemExit("manifest does not match the pre-registered basket/date")
    return {r["ticker"]: float(r["inception_close_raw"]) for r in rows}


def mark(on_or_after=None):
    stored = manifest()
    data = {t: fetch(t) for t in BASKET + [BENCH]}  # one fetch per ticker
    for t, h in data.items():
        gap = abs(h["Close"].iloc[0] / stored[t] - 1)
        if gap > TOL:
            raise SystemExit(f"{t}: re-fetched inception close {h['Close'].iloc[0]} differs from manifest {stored[t]} by {gap:.2%}")
    adj = pd.concat({t: h["Adj Close"] for t, h in data.items()}, axis=1)
    common = adj.dropna()  # only dates on which every ticker has a close (no stale prices)
    if on_or_after:
        common = common[common.index >= pd.Timestamp(on_or_after)]
        if common.empty:
            raise SystemExit(f"no common close on or after {on_or_after} yet")
        row = common.iloc[0]
        asof = common.index[0].date()
    else:
        row = common.iloc[-1]
        asof = common.index[-1].date()
    rel = row / adj.iloc[0]
    basket_ret = sum(NOTIONAL * rel[t] for t in BASKET) / (NOTIONAL * len(BASKET)) - 1
    bench_ret = rel[BENCH] - 1
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["marked_on", "review_date_arg", "as_of", "basket_ret_pct", "bench_ret_pct", "excess_pp"] + BASKET)
        w.writerow([date.today().isoformat(), on_or_after or "latest", asof, round(basket_ret * 100, 2),
                    round(bench_ret * 100, 2), round((basket_ret - bench_ret) * 100, 2)]
                   + [round((rel[t] - 1) * 100, 2) for t in BASKET])
    print(f"as of {asof}: basket {basket_ret:+.2%} vs 2800.HK {bench_ret:+.2%} -> excess {(basket_ret-bench_ret)*100:+.2f} pp")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "mark"
    if cmd == "init":
        init()
    else:
        mark(sys.argv[2] if len(sys.argv) > 2 else None)

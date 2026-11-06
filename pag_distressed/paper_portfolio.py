"""Out-of-sample paper portfolio (test D), pre-registered on 6-Nov-2026.

Hypothesis: PAG's control bid for Evergrande Property Services (announced 30-Oct-2026)
signals a turn for HK-listed China property-services stocks, so a basket bought now
should beat the Tracker Fund over 3 / 12 / 24 / 36 months.

Fixed rules (do NOT change after inception; any change must be a new, separately dated test):
- Inception = official HK close on 2026-11-06, recorded in data/paper_portfolio_start.csv (LF line
  endings, stored byte-for-byte via .gitattributes; SHA-256 printed in report #51).
- Returns are ANCHORED TO THE MANIFEST PRICE: value_t = manifest_close x shares, with
  shares = HK$100,000 / manifest_close; dividends reinvested via Yahoo's total-return factor
  (Adj Close ratio); share splits/consolidations after inception are applied via Yahoo's split
  history so the manifest price stays the denominator.
- Basket: 6666.HK, 1209.HK, 6049.HK, 2669.HK, 6098.HK, 1516.HK (HK$100k each, no rebalancing).
  Benchmark: 2800.HK (HK$600k).
- Valuation date = the first 2800.HK trading close ON OR AFTER the review date:
  2027-02-06 (+3m), 2027-11-06 (+12m), 2028-11-06 (+24m), 2029-11-06 (+36m).
  Only COMPLETED sessions are used (an HK date counts only after 18:00 HKT that day).
- Suspension / delisting: a constituent without a close on the valuation date is carried at its
  last close (flagged "stale" in the log). If it is taken private / acquired for cash, it is valued
  at the cash consideration from the completion date onward and earns 0% thereafter. The terminal
  record is frozen in TERMINAL while Yahoo history still exists (use `terminal-shares` to compute
  shares held per inception share = post-inception split product x dividend-reinvestment factor up
  to completion), so later valuations do NOT need a live price history for that ticker.
  This rule is fixed; only the deal data is added later, with its source.
- Success = basket beats 2800.HK at +12m AND +36m. Failures are reported as prominently as successes.
- Log semantics: only the four scheduled review dates produce "review" rows (dates normalised to ISO);
  the FIRST "review" row for a scheduled date is canonical; any later row for the same date is
  "revision" and must be explained in the report. All other runs are "interim" (informational).
- The first `mark` run after 18:00 HKT on 6-Nov-2026 also serves as the inception check: it aborts if
  any Yahoo inception close differs from the manifest by more than 0.5%.

Usage:
  python pag_distressed/paper_portfolio.py init                     # once; refuses to overwrite
  python pag_distressed/paper_portfolio.py mark [YYYY-MM-DD]        # scheduled review (or interim at a date / latest)
  python pag_distressed/paper_portfolio.py terminal-shares TICKER COMPLETION_DATE   # helper for TERMINAL
"""
import csv
import os
import sys
import warnings
from datetime import date, datetime, timedelta, timezone

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")
INCEPTION = "2026-11-06"
BASKET = ["6666.HK", "1209.HK", "6049.HK", "2669.HK", "6098.HK", "1516.HK"]
BENCH = "2800.HK"
REVIEWS = ["2027-02-06", "2027-11-06", "2028-11-06", "2029-11-06"]
NOTIONAL = 100_000
TOL = 0.005
HKT = timezone(timedelta(hours=8))
# Frozen cash-takeover records:
# {ticker: (completion_date, cash_per_share_hkd, shares_per_inception_share, source)}
TERMINAL = {}
D = os.path.join(os.path.dirname(__file__), "data")
START = os.path.join(D, "paper_portfolio_start.csv")
LOG = os.path.join(D, "paper_portfolio_log.csv")


def last_completed_hk_date():
    now = datetime.now(HKT)
    d = now.date() if now.hour >= 18 else now.date() - timedelta(days=1)
    return pd.Timestamp(d)


def fetch(t):
    tk = yf.Ticker(t)
    h = tk.history(start=INCEPTION, auto_adjust=False)[["Close", "Adj Close"]].dropna()
    h.index = pd.to_datetime(h.index).tz_localize(None).normalize()
    h = h[h.index <= last_completed_hk_date()]
    if h.empty or h.index[0] != pd.Timestamp(INCEPTION):
        raise SystemExit(f"{t}: no close on inception date {INCEPTION}")
    sp = tk.splits
    sp.index = pd.to_datetime(sp.index).tz_localize(None).normalize()
    split_factor = float(sp[sp.index > pd.Timestamp(INCEPTION)].prod()) if len(sp) else 1.0
    return h, split_factor


def init():
    if os.path.exists(START):
        raise SystemExit("paper_portfolio_start.csv exists; inception is fixed and will not be overwritten")
    with open(START, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ticker", "role", "inception_date", "inception_close_raw", "notional_hkd"])
        for t in BASKET + [BENCH]:
            raw = fetch(t)[0]["Close"].iloc[0]
            w.writerow([t, "benchmark" if t == BENCH else "basket", INCEPTION, round(float(raw), 4),
                        NOTIONAL * (len(BASKET) if t == BENCH else 1)])
    print(f"Initialised {START}")


def manifest():
    with open(START, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if [r["ticker"] for r in rows] != BASKET + [BENCH] or any(r["inception_date"] != INCEPTION for r in rows):
        raise SystemExit("manifest does not match the pre-registered basket/date")
    return {r["ticker"]: (float(r["inception_close_raw"]), float(r["notional_hkd"])) for r in rows}


def terminal_shares(t, completion_date):
    """Shares held per inception share at completion = split product x dividend-reinvestment factor."""
    comp = pd.Timestamp(completion_date)
    tk = yf.Ticker(t)
    h, _ = fetch(t)
    h = h[h.index < comp]
    sp = tk.splits
    sp.index = pd.to_datetime(sp.index).tz_localize(None).normalize()
    split_prod = float(sp[(sp.index > pd.Timestamp(INCEPTION)) & (sp.index < comp)].prod()) if len(sp) else 1.0
    div_factor = (h["Adj Close"].iloc[-1] / h["Adj Close"].iloc[0]) / (h["Close"].iloc[-1] / h["Close"].iloc[0])
    shares = split_prod * div_factor
    print(f"{t}: shares per inception share at {comp.date()} = {split_prod:g} (splits) x {div_factor:.6f} "
          f"(dividends) = {shares:.6f}. Add to TERMINAL with the cash price and its source.")
    return shares


def mark(review_arg=None):
    man = manifest()
    bench_h, bench_split = fetch(BENCH)
    bench_dates = bench_h.index
    review_date = pd.Timestamp(review_arg).date().isoformat() if review_arg else None
    if review_date:
        cand = bench_dates[bench_dates >= pd.Timestamp(review_date)]
        if cand.empty:
            raise SystemExit(f"no completed 2800.HK close on or after {review_date} yet")
        asof = cand[0]
    else:
        asof = bench_dates[-1]

    rets, stale = {}, []
    for t in BASKET + [BENCH]:
        m_px, _ = man[t]
        if t in TERMINAL and asof >= pd.Timestamp(TERMINAL[t][0]):
            _, cash, shares, _src = TERMINAL[t]
            rets[t] = shares * cash / m_px - 1  # frozen record; no live history needed
            continue
        h, split = (bench_h, bench_split) if t == BENCH else fetch(t)
        y0 = h["Close"].iloc[0] * split  # Yahoo's split-adjusted history scaled back to inception shares
        if abs(y0 / m_px - 1) > TOL:
            raise SystemExit(f"{t}: Yahoo inception close {y0:.4f} (split-adjusted back) vs manifest {m_px} > {TOL:.1%}")
        upto = h[h.index <= asof]
        if upto.index[-1] != asof:
            stale.append(t)
        tr_factor = upto["Adj Close"].iloc[-1] / h["Adj Close"].iloc[0]
        # anchor to the manifest price instead of Yahoo's (possibly revised) inception close
        rets[t] = tr_factor * (y0 / m_px) - 1

    basket_ret = sum(NOTIONAL * (1 + rets[t]) for t in BASKET) / (NOTIONAL * len(BASKET)) - 1
    bench_ret = rets[BENCH]
    kind = "interim"
    if review_date in REVIEWS:
        kind = "review"
        if os.path.exists(LOG):
            with open(LOG, encoding="utf-8") as f:
                if any(r["record_type"] in ("review", "revision") and r["review_date_arg"] == review_date
                       for r in csv.DictReader(f)):
                    kind = "revision"
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        if new:
            w.writerow(["marked_on", "record_type", "review_date_arg", "as_of", "basket_ret_pct", "bench_ret_pct",
                        "excess_pp", "stale"] + BASKET)
        w.writerow([date.today().isoformat(), kind, review_date or "", asof.date(), round(basket_ret * 100, 2),
                    round(bench_ret * 100, 2), round((basket_ret - bench_ret) * 100, 2), "+".join(stale)]
                   + [round(rets[t] * 100, 2) for t in BASKET])
    print(f"[{kind}] as of {asof.date()}: basket {basket_ret:+.2%} vs 2800.HK {bench_ret:+.2%} -> "
          f"excess {(basket_ret-bench_ret)*100:+.2f} pp" + (f"; stale: {stale}" if stale else ""))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "mark"
    if cmd == "init":
        init()
    elif cmd == "terminal-shares":
        terminal_shares(sys.argv[2], sys.argv[3])
    else:
        mark(sys.argv[2] if len(sys.argv) > 2 else None)

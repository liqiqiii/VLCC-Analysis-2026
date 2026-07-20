"""
Tail-hedge / convexity backtest — 50 years of REAL S&P 500 total return.
================================================================================
Validates the Taleb/Spitznagel tail-hedging (convexity) thesis discussed in the
report against 1974-09 .. 2024-09 monthly data.

Data source : Robert J. Shiller, "Real Total Return Price" (dividends reinvested,
              CPI-adjusted), monthly. http://www.econ.yale.edu/~shiller/data.htm
Window      : 1974-09 .. 2024-09 (600 months = 50.0 years).

Reproducibility:
  * If tail_hedge/data/shiller_real_tr_monthly_1974_2024.csv exists, it is used.
  * Else the script looks for shiller2.xls / shiller.xls (cwd or ~), else downloads
    ie_data.xls from Shiller's site, parses column 9 (Real Total Return Price),
    and writes the derived monthly CSV.

Outputs (written to tail_hedge/data/):
  shiller_real_tr_monthly_1974_2024.csv  — derived input series (Date, RealTRP, ret)
  results_baseline_barbell.csv           — Buy&Hold + cash-barbell (AQR alternative)
  results_monthly_put_hedge.csv          — rolling 1-month OTM put, BS-priced (grid)
  results_leaps_put_hedge.csv            — rolling 12-month (LEAPS) put (grid)
  results_equal_drawdown.csv             — hedge vs barbell tuned to equal maxDD
  results_tail_shape.csv                 — skew/kurtosis/worst-month (left-tail clip)
  results_crash_episodes.csv             — convex payoff in the 5 major crashes

CAVEAT: Shiller monthly prices are month-AVERAGES, which smooth fast intra-month
crashes (1987, 2020) -> measured drawdowns understated -> hedge value here is
CONSERVATIVE (biased against the hedge). Results are gross of tax/transaction cost.
"""
import os
import math
import urllib.request
import pandas as pd
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
CSV_IN = os.path.join(DATA, "shiller_real_tr_monthly_1974_2024.csv")


# ------------------------------------------------------------------ helpers
def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_put(k_otm, sigma_ann, T):
    """Black-Scholes put price as a fraction of spot. Strike=(1-k)*S, r=q=0."""
    if sigma_ann <= 1e-9:
        return max(0.0, (1 - k_otm) - 1.0)
    K = 1.0 - k_otm
    sq = math.sqrt(T)
    d1 = (math.log(1.0 / K) + 0.5 * sigma_ann ** 2 * T) / (sigma_ann * sq)
    d2 = d1 - sigma_ann * sq
    return K * norm_cdf(-d2) - norm_cdf(-d1)


def _skew(x):
    x = np.asarray(x); m, s = x.mean(), x.std()
    return float(np.mean(((x - m) / s) ** 3))


def _kurt(x):
    x = np.asarray(x); m, s = x.mean(), x.std()
    return float(np.mean(((x - m) / s) ** 4) - 3)


def metrics(mr):
    mr = np.asarray(mr, float)
    c = np.cumprod(1 + mr)
    n = len(mr)
    cagr = c[-1] ** (12 / n) - 1
    arith = np.mean(mr) * 12
    vol = np.std(mr, ddof=1) * math.sqrt(12)
    dd = (c / np.maximum.accumulate(c) - 1).min()
    w12 = pd.Series(mr).rolling(12).apply(lambda x: np.prod(1 + x) - 1, raw=True)
    worst12 = float(np.nanmin(w12.values))
    return dict(CAGR=cagr, arith=arith, vol=vol, maxDD=dd, worst12m=worst12,
                Sharpe=arith / vol if vol > 0 else float("nan"),
                terminal=c[-1], skew=_skew(mr), kurt=_kurt(mr))


def r4(m):
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()}


# ------------------------------------------------------------------ load data
def load_series():
    if os.path.exists(CSV_IN):
        df = pd.read_csv(CSV_IN)
        return df
    # find or fetch the Shiller workbook
    xls = None
    for cand in ["shiller2.xls", "shiller.xls",
                 os.path.expanduser("~/shiller2.xls"),
                 os.path.expanduser("~/shiller.xls")]:
        if os.path.exists(cand):
            xls = cand
            break
    if xls is None:
        xls = os.path.join(HERE, "ie_data.xls")
        url = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(xls, "wb").write(urllib.request.urlopen(req, timeout=30).read())
    full = pd.read_excel(xls, "Data", header=7)
    s = full.iloc[:, [0, 9]].copy()
    s.columns = ["Date", "RealTRP"]
    s = s.dropna()
    s = s[s["Date"].astype(str).str.match(r"^\d{4}\.\d")]
    s["RealTRP"] = pd.to_numeric(s["RealTRP"], errors="coerce")
    s = s.dropna().reset_index(drop=True)
    s["ret"] = s["RealTRP"].pct_change()
    return s


s = load_series()
s["ret"] = s["RealTRP"].pct_change()
s["rvol"] = s["ret"].rolling(12).std() * math.sqrt(12)

# window: 600 months ending 2024.09
end_idx = s.index[np.isclose(s["Date"], 2024.09)][0]
win = s.iloc[end_idx - 599: end_idx + 1].reset_index(drop=True)
# persist the derived input series actually used
win[["Date", "RealTRP", "ret"]].to_csv(CSV_IN, index=False)

r = win["ret"].values
rvol = win["rvol"].values
N = len(r)
print(f"Window {win['Date'].iloc[0]}..{win['Date'].iloc[-1]}  {N} months ({N/12:.1f}y)")

bh = metrics(r)

# ------------------------------------------------------------------ A/B baseline + barbell
rowsAB = [{"strategy": "Buy&Hold 100% equity", **r4(bh)}]
for wc in (0.05, 0.10, 0.20):
    rowsAB.append({"strategy": f"Barbell {int((1-wc)*100)}/{int(wc*100)} equity/cash",
                   **r4(metrics((1 - wc) * r))})
pd.DataFrame(rowsAB).to_csv(os.path.join(DATA, "results_baseline_barbell.csv"), index=False)

# ------------------------------------------------------------------ C monthly put hedge grid
def hedge_monthly(k, vrp, h=1.0):
    net = np.empty(N); prem = np.empty(N); pay = np.empty(N)
    for t in range(N):
        iv = (rvol[t] if not math.isnan(rvol[t]) else 0.15) * (1 + vrp)
        p = bs_put(k, iv, 1 / 12)
        po = max(0.0, -(r[t] + k))
        net[t] = r[t] + h * (po - p); prem[t] = p; pay[t] = po
    return net, prem.mean() * 12, pay.mean() * 12

rowsC = []
for k in (0.05, 0.10):
    for vrp in (0.0, 0.25, 0.50):
        net, ap, apo = hedge_monthly(k, vrp)
        rowsC.append({"strategy": f"1m put k={int(k*100)}%OTM VRP={int(vrp*100)}%",
                      "ann_premium": round(ap, 4), "ann_payoff": round(apo, 4),
                      "net_drag": round(ap - apo, 4), **r4(metrics(net))})
pd.DataFrame(rowsC).to_csv(os.path.join(DATA, "results_monthly_put_hedge.csv"), index=False)

# ------------------------------------------------------------------ C2 LEAPS (annual) put grid
def ann_metrics(a):
    a = np.asarray(a); c = np.cumprod(1 + a); n = len(a)
    return dict(CAGR=round(c[-1] ** (1 / n) - 1, 4), vol=round(np.std(a, ddof=1), 4),
                maxDD=round((c / np.maximum.accumulate(c) - 1).min(), 4),
                terminal=round(c[-1], 2))

yrs = N // 12
rowsL = []
# baseline annual (non-overlapping)
eq = np.array([np.prod(1 + r[y * 12:(y + 1) * 12]) - 1 for y in range(yrs)])
bh_ann = ann_metrics(eq)
rowsL.append({"strategy": "Buy&Hold (annual)", "ann_premium": 0.0, "ann_payoff": 0.0, **bh_ann})
for k in (0.10, 0.20):
    for vrp in (0.0, 0.25, 0.50):
        hd = np.empty(yrs); pr = []; pyo = []
        for y in range(yrs):
            r12 = np.prod(1 + r[y * 12:(y + 1) * 12]) - 1
            iv = (rvol[y * 12] if not math.isnan(rvol[y * 12]) else 0.15) * (1 + vrp)
            p = bs_put(k, iv, 1.0); po = max(0.0, -(r12 + k))
            hd[y] = r12 + po - p; pr.append(p); pyo.append(po)
        rowsL.append({"strategy": f"LEAPS 1y put k={int(k*100)}%OTM VRP={int(vrp*100)}%",
                      "ann_premium": round(np.mean(pr), 4), "ann_payoff": round(np.mean(pyo), 4),
                      **ann_metrics(hd)})
pd.DataFrame(rowsL).to_csv(os.path.join(DATA, "results_leaps_put_hedge.csv"), index=False)

# ------------------------------------------------------------------ D equal-drawdown fair test
target = -0.40
def best_to_target(fn, grid):
    best = None
    for g in grid:
        m = metrics(fn(g))
        if best is None or abs(m["maxDD"] - target) < abs(best[1] - target):
            best = (g, m["maxDD"], m)
    return best
wb, ddb, mb = best_to_target(lambda w: (1 - w) * r, np.linspace(0, 0.5, 51))
hh, ddh, mh = best_to_target(lambda h: hedge_monthly(0.05, 0.25, h)[0], np.linspace(0, 3, 61))
pd.DataFrame([
    {"defense": f"Cash barbell (cash={wb*100:.0f}%)", "maxDD": round(mb["maxDD"], 4),
     "CAGR": round(mb["CAGR"], 4), "Sharpe": round(mb["Sharpe"], 3)},
    {"defense": f"Put hedge (h={hh:.2f}, k5,VRP25)", "maxDD": round(mh["maxDD"], 4),
     "CAGR": round(mh["CAGR"], 4), "Sharpe": round(mh["Sharpe"], 3)},
]).to_csv(os.path.join(DATA, "results_equal_drawdown.csv"), index=False)

# ------------------------------------------------------------------ E tail-shape
rowsT = [{"strategy": "Buy&Hold", **r4(bh)}]
for tag, (k, vrp) in {"cheap VRP0": (0.05, 0.0), "realistic VRP25": (0.05, 0.25),
                      "expensive VRP50": (0.05, 0.50)}.items():
    rowsT.append({"strategy": f"1m put k5 {tag}", **r4(metrics(hedge_monthly(k, vrp)[0]))})
worst_bh = sorted(r)[:6]
worst_hd = sorted(hedge_monthly(0.05, 0.25)[0])[:6]
tdf = pd.DataFrame(rowsT)
tdf["worst6_months_bh"] = [";".join(f"{x*100:.1f}%" for x in worst_bh)] + [""] * (len(tdf) - 1)
tdf["worst6_months_hedged_realistic"] = [";".join(f"{x*100:.1f}%" for x in worst_hd)] + [""] * (len(tdf) - 1)
tdf.to_csv(os.path.join(DATA, "results_tail_shape.csv"), index=False)

# ------------------------------------------------------------------ F crash episodes
episodes = {"1973-74 bear": (1973.01, 1974.12), "1987 crash": (1987.08, 1987.12),
            "2000-02 dotcom": (2000.03, 2002.10), "2008 GFC": (2007.10, 2009.03),
            "2020 COVID": (2020.01, 2020.06)}
k, vrp = 0.10, 0.25
rowsF = []
for name, (d0, d1) in episodes.items():
    i0 = s.index[np.isclose(s["Date"], d0)][0]; i1 = s.index[np.isclose(s["Date"], d1)][0]
    bhc = hdc = 1.0
    for t in range(i0, i1 + 1):
        rr = s["ret"].iloc[t]
        iv = (s["rvol"].iloc[t] if not math.isnan(s["rvol"].iloc[t]) else 0.15) * (1 + vrp)
        p = bs_put(k, iv, 1 / 12); po = max(0.0, -(rr + k))
        bhc *= (1 + rr); hdc *= (1 + rr + po - p)
    rowsF.append({"episode": name, "buy_hold": round(bhc - 1, 4),
                  "hedged_1m_k10_vrp25": round(hdc - 1, 4),
                  "protection_pp": round((hdc - bhc) * 100, 1)})
pd.DataFrame(rowsF).to_csv(os.path.join(DATA, "results_crash_episodes.csv"), index=False)

print("Wrote CSVs to", DATA)
for f in sorted(os.listdir(DATA)):
    print("  ", f)
print(f"\nHeadline: Buy&Hold CAGR {bh['CAGR']*100:.2f}%  maxDD {bh['maxDD']*100:.1f}%  "
      f"skew {bh['skew']:.2f} | best LEAPS(k10,VRP0) vs realistic — see CSVs.")

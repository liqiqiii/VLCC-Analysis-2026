"""
Robustness follow-up to run_backtest_vlcc.py:
  (1) Break-even VRP over SUB-WINDOWS (2005+, 2013+, 2019+) — is DHT's ~67% CAGR
      break-even VRP a stable property, or an artifact of the 2008-2012 crash?
  (2) LIVE option-chain VRP calibration — what VRP does a VLCC holder actually pay
      TODAY, and how does it compare to the break-even?
Writes: data/results_vlcc_breakeven_windows.csv, data/results_vlcc_paid_vrp.csv
"""
import os, math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RV_WIN = 63; TENOR = 252; K = 0.30

def norm_cdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_put_frac(k, sig, T):
    if T <= 1e-9 or sig <= 1e-9: return max(0.0, (1 - k) - 1.0)
    Kk = 1 - k; sq = math.sqrt(T)
    d1 = (math.log(1 / Kk) + 0.5 * sig * sig * T) / (sig * sq); d2 = d1 - sig * sq
    return Kk * norm_cdf(-d2) - norm_cdf(-d1)

def load(fn):
    df = pd.read_csv(os.path.join(DATA, fn))
    dts = pd.to_datetime(df['Date']).values
    s = df['AdjClose'].astype(float).values
    r = np.zeros(len(s)); r[1:] = s[1:] / s[:-1] - 1
    rv = pd.Series(r).rolling(RV_WIN).std().values * math.sqrt(252)
    rv = np.where(np.isnan(rv), np.nanmean(rv[~np.isnan(rv)]), rv)
    return dts, s, r, rv

def metrics_cagr(nav):
    return nav[-1] ** (252 / len(nav)) - 1

def hedged_nav(s, r, rv, vrp):
    n = len(s); T0 = TENOR / 252.0; dt = 1 / 252.0
    eq = 1.0; nav = np.empty(n); nav[0] = 1.0; Kabs = None; T = 0.0; q = 0.0
    def establish(i):
        nonlocal Kabs, T, q, eq
        Kabs = s[i] * (1 - K); T = T0
        q = eq / s[i]
        eq -= q * (bs_put_frac(K, rv[i] * (1 + vrp), T) * s[i])
    establish(0)
    for i in range(1, n):
        eq *= (1 + r[i]); T -= dt
        if T <= 1e-6:
            eq += q * max(0.0, Kabs - s[i]); establish(i)
        pp = 0.0
        if T > 1e-6:
            sig = rv[i] * (1 + vrp)
            if sig > 1e-9:
                sq = math.sqrt(T); d1 = (math.log(s[i]/Kabs)+0.5*sig*sig*T)/(sig*sq); d2 = d1-sig*sq
                pp = Kabs*norm_cdf(-d2) - s[i]*norm_cdf(-d1)
            else: pp = max(0.0, Kabs - s[i])
        nav[i] = eq + q * pp
    return nav

def period_pnl(s, rv, vrp, step=21):
    n = len(s); T0 = TENOR / 252.0; prem = []; pay = []
    for i in range(0, n - TENOR, step):
        prem.append(bs_put_frac(K, rv[i] * (1 + vrp), T0))
        pay.append(max(0.0, (1 - K) - s[i + TENOR] / s[i]))
    return np.array(prem), np.array(pay)

def breakeven(s, r, rv):
    cu = metrics_cagr(np.cumprod(np.r_[1.0, 1 + r[1:]]))
    grid = np.arange(0.0, 3.01, 0.05)
    exp_v = []; cagr_v = []
    for vrp in grid:
        prem, pay = period_pnl(s, rv, vrp)
        exp_v.append((pay - prem).mean())
        cagr_v.append(metrics_cagr(hedged_nav(s, r, rv, vrp)))
    exp_v = np.array(exp_v); cagr_v = np.array(cagr_v)
    def cross(y, tgt):
        d = y - tgt; idx = np.where(np.diff(np.sign(d)))[0]
        if len(idx) == 0: return round(grid[-1], 2) if d[-1] > 0 else 0.0
        i0 = idx[0]; x0, x1, y0, y1 = grid[i0], grid[i0+1], d[i0], d[i0+1]
        return round(x0 - y0 * (x1 - x0) / (y1 - y0), 3)
    return cu, cross(exp_v, 0.0), cross(cagr_v, cu)

# ---- (1) sub-window break-even ----
windows = {"2005+": "2005-01-01", "2013+": "2013-01-01", "2019+": "2019-01-01"}
rows = []
for a, fn in [("DHT", "dht_daily_2005_2024.csv"), ("FRO", "fro_daily_2005_2024.csv")]:
    dts, s, r, rv = load(fn)
    for w, start in windows.items():
        i0 = int((dts >= np.datetime64(start)).argmax())
        ss, rr, rvv = s[i0:], r[i0:], rv[i0:]
        rr = rr.copy(); rr[0] = 0.0
        cu, be_exp, be_cagr = breakeven(ss, rr, rvv)
        yrs = round(len(ss) / 252, 1)
        rows.append({"asset": a, "window": w, "years": yrs,
                     "CAGR_unhedged": round(cu, 4),
                     "breakeven_VRP_expectancy": be_exp, "breakeven_VRP_CAGR": be_cagr})
        print(f"{a} {w:<6} {yrs:>4}y  unhedgedCAGR {cu*100:+6.1f}%  BE_exp {be_exp}  BE_CAGR {be_cagr}")
pd.DataFrame(rows).to_csv(os.path.join(DATA, "results_vlcc_breakeven_windows.csv"), index=False)

# ---- (2) live option-chain paid VRP ----
import datetime as dt
try:
    import yfinance as yf
    today = dt.date(2026, 7, 20)
    prows = []
    for tk, exp in [("DHT", "2027-07-16"), ("FRO", "2028-01-21"), ("FRO", "2027-02-19")]:
        t = yf.Ticker(tk)
        h = t.history(period="1y")["Close"]; spot = float(h.iloc[-1])
        rr = h.pct_change().dropna(); rvol = float(rr.tail(63).std() * math.sqrt(252))
        puts = t.option_chain(exp).puts.copy()
        puts["dist"] = (puts["strike"] - spot * (1 - K)).abs()
        row = puts.sort_values("dist").iloc[0]
        T = (dt.date.fromisoformat(exp) - today).days / 365
        iv = float(row["impliedVolatility"])
        prows.append({"ticker": tk, "expiry": exp, "T_years": round(T, 2), "spot": round(spot, 2),
                      "strike_30pctOTM": float(row["strike"]), "put_IV": round(iv, 3),
                      "realized_vol_63d": round(rvol, 3), "paid_VRP": round(iv / rvol - 1, 3),
                      "open_interest": int(row["openInterest"]) if row["openInterest"] == row["openInterest"] else 0})
        print(f"{tk} {exp} T{T:.2f}y spot {spot:.2f} IV {iv*100:.0f}% realized {rvol*100:.0f}% paidVRP {iv/rvol-1:.2f} OI {prows[-1]['open_interest']}")
    pd.DataFrame(prows).to_csv(os.path.join(DATA, "results_vlcc_paid_vrp.csv"), index=False)
except Exception as e:
    print("live option pull failed:", e)
print("\nWrote results_vlcc_breakeven_windows.csv, results_vlcc_paid_vrp.csv")

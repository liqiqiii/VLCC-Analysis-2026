"""
VLCC convexity / tail-hedge backtest on DHT & FRO — reliability across scenarios,
and a WIN-RATE-vs-VRP framework for deciding how much you can overpay for insurance.
================================================================================
Motivation: a large LONG VLCC holder (DHT/FRO) wants to know whether deep-OTM put
tail-hedging is worth it, HOW RELIABLE it is across scenarios (fast crash vs slow
cyclical grind, strike depth, tenor), and — crucially — how the answer depends on
the vol-risk-premium (VRP = how overpriced the puts are). VLCC stocks are ~3x the
S&P's volatility with ~ -97% drawdowns, so the calculus is very different.

Data   : DHT (2005-10..2024-12), FRO (2005-01..2024-12) daily ADJUSTED close
         (splits + dividends), yfinance -> data/{dht,fro}_daily_2005_2024.csv.
         S&P from data/sp500_daily_close_1974_2024.csv (price only) for comparison.
Hedge  : PASSIVE rolled put (held to expiry, rolled) — the design that dominated the
         S&P study (report Section 7.5). Priced by Black-Scholes, IV = trailing 63d
         realized vol * (1 + VRP). Notional = full position; premium financed from NAV.
Outputs (data/):
  results_vlcc_profile.csv        — vol / drawdown profile (DHT/FRO vs S&P)
  results_vlcc_hedge_grid.csv     — strike x tenor x VRP: CAGR / maxDD (reliability grid)
  results_vlcc_winrate_vrp.csv    — per-VRP win-rate, expectancy, avg win/loss, CAGR delta
  results_vlcc_breakeven_vrp.csv  — expectancy break-even VRP and CAGR break-even VRP
  results_vlcc_reliability.csv    — annual underlying return vs hedge P&L (convexity picture)

Caveats: options modeled on the adjusted (total-return) series (real puts are on price;
minor distortion). FRO pre-2013 includes the 2011-12 restructuring (credit-event-like).
Gross of tax / transaction cost / bid-ask / option illiquidity (VLCC options are thin).
"""
import os, math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RV_WIN = 63

def norm_cdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def bs_put_frac(k_otm, sig, T):
    """BS put price as FRACTION of spot (strike = (1-k)*S, r=q=0)."""
    if T <= 1e-9 or sig <= 1e-9:
        return max(0.0, (1 - k_otm) - 1.0)
    K = 1 - k_otm; sq = math.sqrt(T)
    d1 = (math.log(1 / K) + 0.5 * sig * sig * T) / (sig * sq); d2 = d1 - sig * sq
    return K * norm_cdf(-d2) - norm_cdf(-d1)

def load(path, col):
    df = pd.read_csv(path)
    s = df[col].astype(float).values
    r = np.zeros(len(s)); r[1:] = s[1:] / s[:-1] - 1
    rv = pd.Series(r).rolling(RV_WIN).std().values * math.sqrt(252)
    rv = np.where(np.isnan(rv), np.nanmean(rv[~np.isnan(rv)]) if np.any(~np.isnan(rv)) else 0.5, rv)
    return s, r, rv

assets = {
    'DHT': load(os.path.join(DATA, "dht_daily_2005_2024.csv"), "AdjClose"),
    'FRO': load(os.path.join(DATA, "fro_daily_2005_2024.csv"), "AdjClose"),
    'SP500': load(os.path.join(DATA, "sp500_daily_close_1974_2024.csv"), "SP500"),
}
dt = 1 / 252.0

def metrics(nav):
    r = nav[1:] / nav[:-1] - 1
    cagr = nav[-1] ** (252 / len(nav)) - 1
    vol = np.std(r, ddof=1) * math.sqrt(252)
    dd = (nav / np.maximum.accumulate(nav) - 1).min()
    return cagr, vol, dd

def profile(s, r):
    c = np.cumprod(1 + r[1:])
    dd = (c / np.maximum.accumulate(c) - 1).min()
    vol = np.std(r[1:], ddof=1) * math.sqrt(252)
    return vol, dd, r.min(), r.max()

# ---------- 1) profile ----------
prow = []
for a, (s, r, rv) in assets.items():
    vol, dd, wd, bd = profile(s, r)
    prow.append({"asset": a, "years": round(len(s)/252, 1), "ann_vol": round(vol, 3),
                 "maxDD": round(dd, 3), "worst_day": round(wd, 3), "best_day": round(bd, 3)})
pd.DataFrame(prow).to_csv(os.path.join(DATA, "results_vlcc_profile.csv"), index=False)
print("PROFILE:"); [print(" ", p) for p in prow]

# ---------- passive rolled-put hedged NAV ----------
def hedged_nav(s, r, rv, k, tenor_days, vrp):
    n = len(s); T0 = tenor_days / 252.0
    equity = 1.0; nav = np.empty(n); nav[0] = 1.0
    K = None; T = 0.0; q = 0.0
    def establish(i):
        nonlocal K, T, q, equity
        K = s[i] * (1 - k); T = T0
        prem_frac = bs_put_frac(k, rv[i] * (1 + vrp), T)
        q = equity / s[i]                      # units hedged (full notional)
        equity -= q * (prem_frac * s[i])       # premium in $ = q * prem_pts, prem_pts=prem_frac*S
    establish(0)
    for i in range(1, n):
        equity *= (1 + r[i])
        T -= dt
        if T <= 1e-6:
            equity += q * max(0.0, K - s[i]); establish(i)
        put_pts = 0.0
        if T > 1e-6:
            sig = rv[i] * (1 + vrp); Kf = K / s[i]
            # BS put in points via frac of current spot with shifted moneyness
            if sig > 1e-9:
                sq = math.sqrt(T); d1 = (math.log(s[i]/K) + 0.5*sig*sig*T)/(sig*sq); d2 = d1 - sig*sq
                put_pts = K*norm_cdf(-d2) - s[i]*norm_cdf(-d1)
            else:
                put_pts = max(0.0, K - s[i])
        nav[i] = equity + q * put_pts
    return nav

# ---------- 2) hedge grid (reliability across strike x tenor x VRP) ----------
grows = []
for a in ['DHT', 'FRO']:
    s, r, rv = assets[a]
    cagr_u, vol_u, dd_u = metrics(np.cumprod(np.r_[1.0, 1 + r[1:]]))
    grows.append({"asset": a, "hedge": "UNHEDGED", "CAGR": round(cagr_u, 4), "maxDD": round(dd_u, 4)})
    for k in (0.10, 0.20, 0.30):
        for tenor in (63, 252):
            for vrp in (0.0, 0.5, 1.0):
                cg, vv, dd = metrics(hedged_nav(s, r, rv, k, tenor, vrp))
                grows.append({"asset": a, "hedge": f"k{int(k*100)}% {tenor}d VRP{int(vrp*100)}%",
                              "CAGR": round(cg, 4), "maxDD": round(dd, 4)})
pd.DataFrame(grows).to_csv(os.path.join(DATA, "results_vlcc_hedge_grid.csv"), index=False)

# ---------- period stats for win-rate (rolling monthly-start 1y puts) ----------
def period_pnl(s, rv, k, tenor_days, vrp, step=21):
    n = len(s); T0 = tenor_days / 252.0; prem = []; pay = []
    for i in range(0, n - tenor_days, step):
        p = bs_put_frac(k, rv[i] * (1 + vrp), T0)            # premium (frac of spot at start)
        payoff = max(0.0, (1 - k) - s[i + tenor_days] / s[i])  # intrinsic frac of start spot
        prem.append(p); pay.append(payoff)
    return np.array(prem), np.array(pay)

# ---------- 3) win-rate vs VRP + 4) break-even VRP ----------
def cagr_unhedged(s, r):
    return metrics(np.cumprod(np.r_[1.0, 1 + r[1:]]))[0]

canon = {'DHT': 0.30, 'FRO': 0.30, 'SP500': 0.20}   # canonical strike per asset (deep-OTM, vol-scaled)
TENOR = 252
wrows = []; brows = []
for a, k in canon.items():
    s, r, rv = assets[a]
    cu = cagr_unhedged(s, r)
    # premium(vrp) uses same payoff; recompute premium per vrp
    _, payoff = period_pnl(s, rv, k, TENOR, 0.0)
    mean_pay = payoff.mean()
    # win-rate table at selected VRPs
    for vrp in (0.0, 0.25, 0.5, 1.0, 2.0):
        prem, pay = period_pnl(s, rv, k, TENOR, vrp)
        pnl = pay - prem
        wins = pnl > 0
        wr = wins.mean()
        aw = pnl[pnl > 0].mean() if wins.any() else 0.0
        al = pnl[~wins].mean() if (~wins).any() else 0.0
        ch, _, _ = metrics(hedged_nav(s, r, rv, k, TENOR, vrp))
        wrows.append({"asset": a, "strike": f"{int(k*100)}%OTM", "tenor": f"{TENOR}d", "VRP": vrp,
                      "win_rate": round(wr, 3), "expectancy": round(pnl.mean(), 4),
                      "avg_win": round(aw, 4), "avg_loss": round(al, 4),
                      "payoff_ratio": round(abs(aw/al), 2) if al != 0 else np.nan,
                      "CAGR_hedged": round(ch, 4), "CAGR_unhedged": round(cu, 4),
                      "CAGR_delta": round(ch - cu, 4)})
    # break-even VRPs (scan)
    grid = np.arange(0.0, 3.01, 0.05)
    exp_v = []; cagr_v = []
    for vrp in grid:
        prem, pay = period_pnl(s, rv, k, TENOR, vrp)
        exp_v.append((pay - prem).mean())
        cagr_v.append(metrics(hedged_nav(s, r, rv, k, TENOR, vrp))[0])
    exp_v = np.array(exp_v); cagr_v = np.array(cagr_v)
    def cross(grid, y, target):
        d = y - target
        idx = np.where(np.diff(np.sign(d)))[0]
        if len(idx) == 0:
            return (grid[-1] if d[-1] > 0 else 0.0)  # never crosses in range
        i0 = idx[0]
        x0, x1, y0, y1 = grid[i0], grid[i0+1], d[i0], d[i0+1]
        return round(x0 - y0 * (x1 - x0) / (y1 - y0), 3)
    be_exp = cross(grid, exp_v, 0.0)          # VRP where expectancy = 0
    be_cagr = cross(grid, cagr_v, cu)         # VRP where CAGR_hedged = CAGR_unhedged
    brows.append({"asset": a, "strike": f"{int(k*100)}%OTM", "tenor": f"{TENOR}d",
                  "mean_payoff_frac": round(mean_pay, 4),
                  "breakeven_VRP_expectancy": be_exp, "breakeven_VRP_CAGR": be_cagr,
                  "CAGR_unhedged": round(cu, 4)})
pd.DataFrame(wrows).to_csv(os.path.join(DATA, "results_vlcc_winrate_vrp.csv"), index=False)
pd.DataFrame(brows).to_csv(os.path.join(DATA, "results_vlcc_breakeven_vrp.csv"), index=False)
print("\nBREAK-EVEN VRP:"); [print(" ", b) for b in brows]

# ---------- 5) reliability: annual underlying return vs hedge P&L ----------
def year_index(path, dcol="Date"):
    return pd.to_datetime(pd.read_csv(path)[dcol]).dt.year.values
yr = {'DHT': year_index(os.path.join(DATA, "dht_daily_2005_2024.csv")),
      'FRO': year_index(os.path.join(DATA, "fro_daily_2005_2024.csv"))}
rel = []
for a in ['DHT', 'FRO']:
    s, r, rv = assets[a]; years = yr[a]; k = 0.30; vrp = 0.5; T0 = 1.0
    for y in sorted(set(years)):
        idx = np.where(years == y)[0]
        if len(idx) < 60: continue
        i0, i1 = idx[0], idx[-1]
        under = s[i1] / s[i0] - 1
        prem = bs_put_frac(k, rv[i0] * (1 + vrp), T0)
        payoff = max(0.0, (1 - k) - s[i1] / s[i0])
        rel.append({"asset": a, "year": int(y), "underlying_ret": round(under, 3),
                    "hedge_pnl_frac": round(payoff - prem, 4)})
pd.DataFrame(rel).to_csv(os.path.join(DATA, "results_vlcc_reliability.csv"), index=False)
print("\nWin-rate table + break-even + reliability written to data/. Sample win-rate rows:")
for w in wrows:
    if w['VRP'] in (0.0, 0.5, 1.0):
        print(f"  {w['asset']:<6} {w['strike']} VRP{int(w['VRP']*100):>3}%  win {w['win_rate']*100:4.0f}%  "
              f"exp {w['expectancy']*100:+5.1f}%  CAGRd {w['CAGR_delta']*100:+5.2f}pp")

"""
DAILY path-dependent tail-hedge backtest — tests the MONETIZE-THE-CRASH ladder,
now with a LAGGED-REDEPLOY CONTROL GROUP that cleanly isolates the dip-timing alpha.
================================================================================
Follow-up to run_backtest.py (monthly, could NOT test the redeploy alpha because
month-average data has no intra-month V-bottoms). Uses DAILY S&P 500 to capture
1987 / 2000-02 / 2008 / 2020 intra-month crashes and implements the user's rule:

  * Hold a standing 1-year deep-OTM put as portfolio insurance (rolled at expiry).
  * MONETIZE LADDER: put value +100% (doubles) -> sell HALF; +200% (triples) -> sell
    the REST; then re-establish a fresh put ("wait for the next round").
  * REDEPLOY: monetization proceeds buy equity ("buy the dip").

Strategies (daily NAV):
  A) Buy & Hold                      — equity only (+ dividend drip)
  B) Hedge PASSIVE                   — hold put to expiry, roll; no ladder, no redeploy
  C) Ladder -> CASH (hoard)          — monetize, proceeds sit in cash forever
  E) Ladder -> EQUITY, LAGGED buy    — monetize, redeploy N trading days LATER (control)
  D) Ladder -> EQUITY, IMMEDIATE     — monetize, redeploy same day ("buy the dip")

Clean decomposition of the redeploy edge:
  (E - C) = value of eventually REINVESTING vs hoarding cash  (removes dip-timing)
  (D - E) = pure DIP-TIMING alpha: buying the exact dip vs N days later
  (D - C) = (E - C) + (D - E)

Data   : ^GSPC daily close 1974-2024 (yfinance), PRICE return + constant ~1.9%/yr
         dividend drip. NOMINAL (not inflation-adjusted). The RELATIVE ranking is
         the point. Put marked daily by Black-Scholes (1y, 20% OTM, IV = 63d
         realized vol * 1.25). Gross of tax / transaction cost / bid-ask.
"""
import os, math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CSV = os.path.join(DATA, "sp500_daily_close_1974_2024.csv")

DIV_YIELD = 0.019
VRP = 0.25
K_OTM = 0.20
TENOR = 1.0
H = 1.0
RV_WIN = 63
LAG_MAIN = 20      # trading days for the main lagged control (E) ~ 1 month

def norm_cdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def bs_put_pts(S, K, T, sig):
    if T <= 1e-6 or sig <= 1e-6:
        return max(0.0, K - S)
    sq = math.sqrt(T)
    d1 = (math.log(S / K) + 0.5 * sig * sig * T) / (sig * sq)
    d2 = d1 - sig * sq
    return K * norm_cdf(-d2) - S * norm_cdf(-d1)

df = pd.read_csv(CSV, parse_dates=["Date"])
S = df["SP500"].values
dates = df["Date"].values
n = len(S)
ret = np.zeros(n); ret[1:] = S[1:] / S[:-1] - 1
rv = pd.Series(ret).rolling(RV_WIN).std().values * math.sqrt(252)
rv = np.where(np.isnan(rv), 0.15, rv)
div_daily = DIV_YIELD / 252.0
dt = 1.0 / 252.0


def run(mode, lag=0):
    """mode in {'bh','passive','ladder_cash','ladder_equity'}.
       For 'ladder_equity', lag>0 defers the redeploy by `lag` trading days (control E)."""
    equity = 1.0
    cash = 0.0
    pending = []          # [[deploy_index, amount], ...] for lagged redeploy
    pending_total = 0.0
    K = None; T = 0.0; q = 0.0; basis_pts = 0.0; sold_half = False
    nav = np.empty(n); nav[0] = 1.0

    def establish(i):
        nonlocal K, T, q, basis_pts, sold_half, equity
        K = S[i] * (1 - K_OTM); T = TENOR
        pts = bs_put_pts(S[i], K, T, rv[i] * (1 + VRP))
        q = (H * equity) / S[i]
        equity -= q * pts
        basis_pts = pts; sold_half = False

    def redeploy(i, proceeds):
        nonlocal equity, pending_total
        if mode == 'ladder_cash':
            # handled by caller (cash += proceeds); not used here
            return
        if lag <= 0:
            equity += proceeds
        else:
            pending.append([i + lag, proceeds]); 
            # track pending_total below

    if mode != 'bh':
        establish(0)

    for i in range(1, n):
        # 1) mature any pending (lagged) redeployments due today -> buy equity at today's price
        if pending:
            still = []
            for dd, amt in pending:
                if dd <= i:
                    equity += amt
                else:
                    still.append([dd, amt])
            pending = still
        pending_total = sum(a for _, a in pending)

        # 2) equity grows with price return + dividend drip
        equity *= (1 + ret[i] + div_daily)

        if mode == 'bh':
            nav[i] = equity + cash + pending_total
            continue

        T -= dt
        iv = rv[i] * (1 + VRP)
        val_pts = bs_put_pts(S[i], K, T, iv)

        # 3) ladder monetization
        if mode in ('ladder_cash', 'ladder_equity') and q > 0 and basis_pts > 1e-9:
            gain = val_pts / basis_pts
            if (not sold_half) and gain >= 2.0:
                proceeds = 0.5 * q * val_pts; q *= 0.5; sold_half = True
                if mode == 'ladder_cash': cash += proceeds
                else:
                    if lag <= 0: equity += proceeds
                    else: pending.append([i + lag, proceeds])
            elif sold_half and gain >= 3.0:
                proceeds = q * val_pts; q = 0.0
                if mode == 'ladder_cash': cash += proceeds
                else:
                    if lag <= 0: equity += proceeds
                    else: pending.append([i + lag, proceeds])

        # 4) expiry -> settle intrinsic (immediate roll into equity), re-establish
        if T <= 1e-6:
            proceeds = q * max(0.0, K - S[i])
            if mode == 'ladder_cash': cash += proceeds
            else: equity += proceeds
            establish(i)
        elif q == 0.0 and mode in ('ladder_cash', 'ladder_equity'):
            establish(i)

        pending_total = sum(a for _, a in pending)
        hedge_val = q * bs_put_pts(S[i], K, T, iv)
        nav[i] = equity + cash + hedge_val + pending_total
    return nav


def metrics(nav):
    r = nav[1:] / nav[:-1] - 1
    yrs = len(nav) / 252
    cagr = nav[-1] ** (1 / yrs) - 1
    vol = np.std(r, ddof=1) * math.sqrt(252)
    dd = (nav / np.maximum.accumulate(nav) - 1).min()
    sharpe = (np.mean(r) * 252) / vol
    m, sd = r.mean(), r.std()
    skew = np.mean(((r - m) / sd) ** 3); kurt = np.mean(((r - m) / sd) ** 4) - 3
    return dict(CAGR=cagr, vol=vol, maxDD=dd, Sharpe=sharpe, terminal=nav[-1], skew=skew, kurt=kurt)


navs = {
    'bh': run('bh'),
    'passive': run('passive'),
    'ladder_cash': run('ladder_cash'),
    'ladder_lag': run('ladder_equity', lag=LAG_MAIN),   # E (control)
    'ladder_equity': run('ladder_equity', lag=0),        # D (immediate dip-buy)
}
labels = {'bh': 'A. Buy & Hold', 'passive': 'B. Hedge passive (hold to expiry)',
          'ladder_cash': 'C. Ladder -> CASH (hoard)',
          'ladder_lag': f'E. Ladder -> EQUITY, +{LAG_MAIN}d lagged (control)',
          'ladder_equity': 'D. Ladder -> EQUITY, immediate (buy the dip)'}
rows = []
for k in ['bh', 'passive', 'ladder_cash', 'ladder_lag', 'ladder_equity']:
    m = metrics(navs[k])
    rows.append({"strategy": labels[k], "CAGR": round(m['CAGR'], 4), "vol": round(m['vol'], 4),
                 "maxDD": round(m['maxDD'], 4), "Sharpe": round(m['Sharpe'], 3),
                 "terminal": round(m['terminal'], 2), "skew": round(m['skew'], 2), "kurt": round(m['kurt'], 1)})
    print(f"{labels[k]:<48} CAGR {m['CAGR']*100:6.2f}%  vol {m['vol']*100:4.1f}%  "
          f"maxDD {m['maxDD']*100:7.1f}%  Sharpe {m['Sharpe']:.2f}  x{m['terminal']:.1f}")
pd.DataFrame(rows).to_csv(os.path.join(DATA, "results_daily_ladder.csv"), index=False)

# ---- clean decomposition ----
cB, cC, cE, cD = (metrics(navs[k])['CAGR'] for k in ['passive', 'ladder_cash', 'ladder_lag', 'ladder_equity'])
cA = metrics(navs['bh'])['CAGR']
print("\nClean decomposition of the redeploy edge (CAGR):")
print(f"  reinvest vs hoard cash (E - C):  {(cE-cC)*100:+.2f} pp/yr")
print(f"  pure dip-timing (D - E):         {(cD-cE)*100:+.2f} pp/yr   <-- the control-isolated alpha")
print(f"  total redeploy (D - C):          {(cD-cC)*100:+.2f} pp/yr   (= E-C plus D-E)")
print(f"  full hedge vs Buy&Hold (D - A):  {(cD-cA)*100:+.2f} pp/yr")

# ---- lag sensitivity ----
print("\nDip-timing alpha vs redeploy lag (D=lag0 minus lagged):")
lrows = [{"lag_days": 0, "CAGR": round(cD, 4), "dip_timing_vs_this": 0.0, "note": "D immediate (buy the dip)"}]
for L in (5, 20, 60, 120):
    cL = metrics(run('ladder_equity', lag=L))['CAGR']
    lrows.append({"lag_days": L, "CAGR": round(cL, 4),
                  "dip_timing_vs_this": round(cD - cL, 4), "note": f"buy {L} trading days after the dip"})
    print(f"  lag {L:>3}d: CAGR {cL*100:6.2f}%   dip-timing (D - E_lag) {(cD-cL)*100:+.2f} pp/yr")
lrows.append({"lag_days": "cash", "CAGR": round(cC, 4), "dip_timing_vs_this": round(cD - cC, 4), "note": "C hoard cash forever"})
pd.DataFrame(lrows).to_csv(os.path.join(DATA, "results_daily_redeploy_lag.csv"), index=False)

# ---- crash episodes (now include E) ----
episodes = {"1987 crash": ("1987-08-01", "1987-12-31"), "2000-02 dotcom": ("2000-03-01", "2002-10-31"),
            "2008 GFC": ("2007-10-01", "2009-03-31"), "2020 COVID": ("2020-02-01", "2020-06-30"),
            "2022 bear": ("2022-01-01", "2022-12-31")}
d = pd.Series(dates); erows = []
for name, (a, b) in episodes.items():
    ia = int((d >= np.datetime64(a)).idxmax()); ib = int((d <= np.datetime64(b))[::-1].idxmax())
    seg = {k: navs[k][ib] / navs[k][ia] - 1 for k in ['bh', 'passive', 'ladder_lag', 'ladder_equity']}
    def wdd(nav): w = nav[ia:ib + 1]; return (w / np.maximum.accumulate(w) - 1).min()
    erows.append({"episode": name, "buy_hold": round(seg['bh'], 4), "hedge_passive": round(seg['passive'], 4),
                  "ladder_lagged_E": round(seg['ladder_lag'], 4), "ladder_immediate_D": round(seg['ladder_equity'], 4),
                  "bh_trough_DD": round(wdd(navs['bh']), 4), "full_trough_DD": round(wdd(navs['ladder_equity']), 4)})
    print(f"{name:<16} B&H {seg['bh']*100:6.1f}%  E(lag) {seg['ladder_lag']*100:6.1f}%  D(imm) {seg['ladder_equity']*100:6.1f}%")
pd.DataFrame(erows).to_csv(os.path.join(DATA, "results_daily_crash_episodes.csv"), index=False)
print("\nWrote results_daily_ladder.csv, results_daily_redeploy_lag.csv, results_daily_crash_episodes.csv")

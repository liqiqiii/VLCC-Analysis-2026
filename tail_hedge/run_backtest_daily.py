"""
DAILY path-dependent tail-hedge backtest — tests the MONETIZE-THE-CRASH ladder.
================================================================================
Follow-up to run_backtest.py (which used monthly month-average data and therefore
could NOT test the 'monetize + buy the dip' redeploy alpha, because monthly data
has no intra-month V-bottoms). This uses DAILY S&P 500 to capture 1987, 2000-02,
2008, 2020 intra-month crashes and implements the user's exact rule:

  * Hold a standing 1-year deep-OTM put as portfolio insurance (rolled at expiry).
  * MONETIZE LADDER: when the put value gains +100% (doubles) sell HALF; when it
    gains +200% (triples) sell the REST; then re-establish a fresh put ("wait for
    the next round").
  * REDEPLOY: monetization proceeds buy equity ("buy the dip") -> convexity harvest.

Strategies compared (daily NAV):
  A) Buy & Hold (equity only, + dividend drip)
  B) Hedge PASSIVE          — hold put to expiry, roll; no ladder, no redeploy
  C) Hedge + LADDER -> CASH — monetize on +100%/+200%, proceeds to cash (no dip-buy)
  D) Hedge + LADDER -> EQUITY — monetize AND redeploy into equity (the full strategy)

Isolation:  (D - C) = the 'buy-the-dip' redeploy alpha
            (C - B) = the 'monetization timing' alpha

Data   : ^GSPC daily close 1974-2024 (Yahoo/yfinance), PRICE return + constant
         dividend drip (~1.9%/yr) to approximate total return. NOMINAL (not
         inflation-adjusted). The RELATIVE comparison (D vs C vs B vs A) is the
         point; absolute level is nominal-total-return-approx.
Pricing: put marked-to-market daily by Black-Scholes, IV = trailing 63d realized
         vol (annualized) * (1 + VRP). r=0.
Caveat : gross of tax, transaction cost, bid-ask; European-style annual put with a
         daily-monetization overlay approximates a real American-LEAPS ladder.
"""
import os, math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CSV = os.path.join(DATA, "sp500_daily_close_1974_2024.csv")

DIV_YIELD = 0.019      # annual dividend drip added to equity sleeve
VRP = 0.25             # vol-risk-premium markup on realized vol for IV
K_OTM = 0.20           # 1-year put strike = 20% below spot at each roll
TENOR = 1.0            # years
H = 1.0                # hedge notional = H * equity value at each roll
RV_WIN = 63            # trailing days for realized vol

def norm_cdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def bs_put_pts(S, K, T, sig):
    """BS put price in index points. r=q=0."""
    if T <= 1e-6 or sig <= 1e-6:
        return max(0.0, K - S)
    sq = math.sqrt(T)
    d1 = (math.log(S / K) + 0.5 * sig * sig * T) / (sig * sq)
    d2 = d1 - sig * sq
    return K * norm_cdf(-d2) - S * norm_cdf(-d1)

# ---------- data ----------
df = pd.read_csv(CSV, parse_dates=["Date"])
S = df["SP500"].values
dates = df["Date"].values
n = len(S)
ret = np.zeros(n)
ret[1:] = S[1:] / S[:-1] - 1
# trailing realized vol (annualized), computed on daily returns
rv = pd.Series(ret).rolling(RV_WIN).std().values * math.sqrt(252)
rv = np.where(np.isnan(rv), 0.15, rv)
div_daily = DIV_YIELD / 252.0
dt = 1.0 / 252.0

def run(mode):
    """mode in {'bh','passive','ladder_cash','ladder_equity'}"""
    equity = 1.0            # dollars in equity sleeve
    cash = 0.0
    # hedge cycle state
    K = None; T = 0.0; q = 0.0; basis_pts = 0.0; sold_half = False
    nav = np.empty(n); nav[0] = 1.0
    prem_paid = 0.0

    def establish(i):
        nonlocal K, T, q, basis_pts, sold_half, equity, prem_paid
        K = S[i] * (1 - K_OTM); T = TENOR
        pts = bs_put_pts(S[i], K, T, rv[i] * (1 + VRP))
        notional = H * equity
        q = notional / S[i]                 # index units hedged
        prem = q * pts                       # dollars
        equity -= prem                       # premium financed from equity
        prem_paid += prem
        basis_pts = pts; sold_half = False

    if mode != 'bh':
        establish(0)

    for i in range(1, n):
        # equity grows with price return + dividend drip
        equity *= (1 + ret[i] + div_daily)
        if mode == 'bh':
            nav[i] = equity + cash
            continue
        T -= dt
        iv = rv[i] * (1 + VRP)
        val_pts = bs_put_pts(S[i], K, T, iv)
        # --- monetization / expiry ---
        if mode in ('ladder_cash', 'ladder_equity') and q > 0 and basis_pts > 1e-9:
            gain = val_pts / basis_pts
            if (not sold_half) and gain >= 2.0:
                proceeds = 0.5 * q * val_pts
                q *= 0.5; sold_half = True
                if mode == 'ladder_equity': equity += proceeds
                else: cash += proceeds
            elif sold_half and gain >= 3.0:
                proceeds = q * val_pts; q = 0.0
                if mode == 'ladder_equity': equity += proceeds
                else: cash += proceeds
        if T <= 1e-6:
            # settle remaining at intrinsic, redeploy, re-establish
            proceeds = q * max(0.0, K - S[i])
            if mode == 'ladder_cash': cash += proceeds
            else: equity += proceeds        # passive & ladder_equity roll into equity
            establish(i)
        elif q == 0.0 and mode in ('ladder_cash', 'ladder_equity'):
            # fully monetized -> wait for next round: re-establish fresh put
            establish(i)
        # mark hedge value into NAV
        hedge_val = q * bs_put_pts(S[i], K, T, iv)
        nav[i] = equity + cash + hedge_val
    return nav, prem_paid

def metrics(nav):
    r = nav[1:] / nav[:-1] - 1
    yrs = len(nav) / 252
    cagr = nav[-1] ** (1 / yrs) - 1
    vol = np.std(r, ddof=1) * math.sqrt(252)
    dd = (nav / np.maximum.accumulate(nav) - 1).min()
    sharpe = (np.mean(r) * 252) / vol
    # skew/kurt of daily
    m, sd = r.mean(), r.std()
    skew = np.mean(((r - m) / sd) ** 3); kurt = np.mean(((r - m) / sd) ** 4) - 3
    return dict(CAGR=cagr, vol=vol, maxDD=dd, Sharpe=sharpe, terminal=nav[-1],
                skew=skew, kurt=kurt)

labels = {'bh': 'A. Buy & Hold', 'passive': 'B. Hedge passive (hold to expiry)',
          'ladder_cash': 'C. Ladder monetize -> CASH', 'ladder_equity': 'D. Ladder monetize -> EQUITY (full)'}
navs = {}; rows = []
for mode in ['bh', 'passive', 'ladder_cash', 'ladder_equity']:
    nav, prem = run(mode)
    navs[mode] = nav
    m = metrics(nav)
    rows.append({"strategy": labels[mode],
                 "CAGR": round(m['CAGR'], 4), "vol": round(m['vol'], 4),
                 "maxDD": round(m['maxDD'], 4), "Sharpe": round(m['Sharpe'], 3),
                 "terminal": round(m['terminal'], 2),
                 "skew": round(m['skew'], 2), "kurt": round(m['kurt'], 1)})
    print(f"{labels[mode]:<40} CAGR {m['CAGR']*100:6.2f}%  vol {m['vol']*100:4.1f}%  "
          f"maxDD {m['maxDD']*100:7.1f}%  Sharpe {m['Sharpe']:.2f}  x{m['terminal']:.1f}  "
          f"skew {m['skew']:+.2f} kurt {m['kurt']:4.1f}")
pd.DataFrame(rows).to_csv(os.path.join(DATA, "results_daily_ladder.csv"), index=False)

# alpha isolation
mB, mC, mD = metrics(navs['passive']), metrics(navs['ladder_cash']), metrics(navs['ladder_equity'])
print("\nAlpha isolation (CAGR):")
print(f"  monetization-timing (C - B): {(mC['CAGR']-mB['CAGR'])*100:+.2f} pp/yr")
print(f"  buy-the-dip redeploy (D - C): {(mD['CAGR']-mC['CAGR'])*100:+.2f} pp/yr")
print(f"  full hedge vs Buy&Hold (D - A): {(mD['CAGR']-metrics(navs['bh'])['CAGR'])*100:+.2f} pp/yr")

# crash-episode NAV comparison (daily captures intra-month bottoms)
episodes = {"1987 crash": ("1987-08-01", "1987-12-31"),
            "2000-02 dotcom": ("2000-03-01", "2002-10-31"),
            "2008 GFC": ("2007-10-01", "2009-03-31"),
            "2020 COVID": ("2020-02-01", "2020-06-30"),
            "2022 bear": ("2022-01-01", "2022-12-31")}
d = pd.Series(dates)
erows = []
for name, (a, b) in episodes.items():
    ia = int((d >= np.datetime64(a)).idxmax())
    ib = int((d <= np.datetime64(b))[::-1].idxmax())
    seg = {}
    for mode in ['bh', 'passive', 'ladder_equity']:
        seg[mode] = navs[mode][ib] / navs[mode][ia] - 1
    # trough drawdown within window for bh vs full
    def wdd(nav): 
        w = nav[ia:ib+1]; return (w / np.maximum.accumulate(w) - 1).min()
    erows.append({"episode": name,
                  "buy_hold": round(seg['bh'], 4),
                  "hedge_passive": round(seg['passive'], 4),
                  "hedge_ladder_equity": round(seg['ladder_equity'], 4),
                  "bh_trough_DD": round(wdd(navs['bh']), 4),
                  "full_trough_DD": round(wdd(navs['ladder_equity']), 4)})
    print(f"{name:<16} B&H {seg['bh']*100:7.1f}%  passive {seg['passive']*100:7.1f}%  "
          f"full {seg['ladder_equity']*100:7.1f}%   (troughDD bh {wdd(navs['bh'])*100:.0f}% vs full {wdd(navs['ladder_equity'])*100:.0f}%)")
pd.DataFrame(erows).to_csv(os.path.join(DATA, "results_daily_crash_episodes.csv"), index=False)
print("\nWrote results_daily_ladder.csv, results_daily_crash_episodes.csv")

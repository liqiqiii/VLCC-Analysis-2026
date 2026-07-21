"""
DAILY path-dependent tail-hedge backtest — monetize-ladder, lagged-redeploy control,
AND a Universa-style disciplined-hedge variant (F) that tries to remove the 2020
failure mode.
================================================================================
Strategies (daily NAV; ^GSPC 1974-2024, price + ~1.9%/yr dividend drip; puts marked
daily by Black-Scholes, 1y 20% OTM, IV = 63d realized vol * 1.25; gross of costs):

  A) Buy & Hold
  B) Hedge PASSIVE            — hold put to expiry, roll; no ladder
  C) Ladder -> CASH (hoard)   — monetize on +100%/+200%, proceeds hoarded in cash
  E) Ladder -> EQUITY, +Nd    — monetize, redeploy N trading days LATER (dip-timing control)
  D) Ladder -> EQUITY, now    — monetize, redeploy same day ("buy the dip")
  F) UNIVERSA-STYLE           — (i) DEPTH-SCALED gradual monetization (not fixed +100/+200),
                                (ii) ALWAYS keep a residual CORE hedge on (never fully de-hedge),
                                (iii) no forced mid-crash re-establishment at peak IV.
                                Proceeds redeploy into equity; roll only at expiry.

Why F: strategies D/E did -17.2% in the fast 2020 V-crash because the +100/+200 ladder
(a) sold ALL protection partway down and (b) re-bought a full put at peak IV (~80%).
F keeps a CORE on and scales selling to drawdown depth, so it never fully de-hedges and
never re-buys at the vol peak. Question: does F remove the 2020 failure mode?
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
LAG_MAIN = 20
CORE_DEFAULT = 0.30     # F: minimum fraction of hedge notional always kept on
GAIN_CAP = 3.0          # F: put gain-multiple at which the sold fraction reaches (1-core)

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


def run(mode, lag=0, core=CORE_DEFAULT):
    equity = 1.0; cash = 0.0
    pending = []
    K = None; T = 0.0; q = 0.0; q0 = 0.0; basis_pts = 0.0; sold_half = False; sold_frac = 0.0
    nav = np.empty(n); nav[0] = 1.0

    def establish(i):
        nonlocal K, T, q, q0, basis_pts, sold_half, sold_frac, equity
        K = S[i] * (1 - K_OTM); T = TENOR
        pts = bs_put_pts(S[i], K, T, rv[i] * (1 + VRP))
        q = (H * equity) / S[i]; q0 = q
        equity -= q * pts
        basis_pts = pts; sold_half = False; sold_frac = 0.0

    if mode != 'bh':
        establish(0)

    for i in range(1, n):
        if pending:
            still = []
            for dd, amt in pending:
                if dd <= i: equity += amt
                else: still.append([dd, amt])
            pending = still
        pending_total = sum(a for _, a in pending)
        equity *= (1 + ret[i] + div_daily)
        if mode == 'bh':
            nav[i] = equity + cash + pending_total
            continue

        T -= dt
        iv = rv[i] * (1 + VRP)
        val_pts = bs_put_pts(S[i], K, T, iv)

        if q > 0 and basis_pts > 1e-9:
            gain = val_pts / basis_pts
            if mode in ('ladder_cash', 'ladder_equity'):
                # fixed +100%/+200% ladder (sell half, then rest)
                if (not sold_half) and gain >= 2.0:
                    proceeds = 0.5 * q * val_pts; q *= 0.5; sold_half = True
                    if mode == 'ladder_cash': cash += proceeds
                    elif lag <= 0: equity += proceeds
                    else: pending.append([i + lag, proceeds])
                elif sold_half and gain >= 3.0:
                    proceeds = q * val_pts; q = 0.0
                    if mode == 'ladder_cash': cash += proceeds
                    elif lag <= 0: equity += proceeds
                    else: pending.append([i + lag, proceeds])
            elif mode == 'universa':
                # depth-scaled gradual monetization, capped so a CORE is always kept
                target_sold = min(1.0 - core, max(0.0, (gain - 1.0) * (1.0 - core) / (GAIN_CAP - 1.0)))
                if target_sold > sold_frac + 1e-9:
                    dsell = (target_sold - sold_frac) * q0
                    proceeds = dsell * val_pts
                    q -= dsell; sold_frac = target_sold
                    equity += proceeds

        if T <= 1e-6:
            equity += q * max(0.0, K - S[i])   # settle remaining at expiry, roll
            establish(i)
        elif q <= 1e-12 and mode in ('ladder_cash', 'ladder_equity'):
            establish(i)                        # ladder fully monetized -> re-establish (peak-IV re-buy)

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
    'bh': run('bh'), 'passive': run('passive'), 'ladder_cash': run('ladder_cash'),
    'ladder_lag': run('ladder_equity', lag=LAG_MAIN), 'ladder_equity': run('ladder_equity', lag=0),
    'universa': run('universa', core=CORE_DEFAULT),
}
labels = {'bh': 'A. Buy & Hold', 'passive': 'B. Hedge passive (hold to expiry)',
          'ladder_cash': 'C. Ladder -> CASH (hoard)',
          'ladder_lag': f'E. Ladder -> EQUITY, +{LAG_MAIN}d lagged (control)',
          'ladder_equity': 'D. Ladder -> EQUITY, immediate (buy the dip)',
          'universa': f'F. Universa-style (core {int(CORE_DEFAULT*100)}%, depth-scaled)'}
rows = []
for k in ['bh', 'passive', 'ladder_cash', 'ladder_lag', 'ladder_equity', 'universa']:
    m = metrics(navs[k])
    rows.append({"strategy": labels[k], "CAGR": round(m['CAGR'], 4), "vol": round(m['vol'], 4),
                 "maxDD": round(m['maxDD'], 4), "Sharpe": round(m['Sharpe'], 3),
                 "terminal": round(m['terminal'], 2), "skew": round(m['skew'], 2), "kurt": round(m['kurt'], 1)})
    print(f"{labels[k]:<48} CAGR {m['CAGR']*100:6.2f}%  vol {m['vol']*100:4.1f}%  "
          f"maxDD {m['maxDD']*100:7.1f}%  Sharpe {m['Sharpe']:.2f}  x{m['terminal']:.1f}")
pd.DataFrame(rows).to_csv(os.path.join(DATA, "results_daily_ladder.csv"), index=False)

# decomposition (unchanged)
cA, cB, cC, cE, cD, cF = (metrics(navs[k])['CAGR'] for k in
                          ['bh', 'passive', 'ladder_cash', 'ladder_lag', 'ladder_equity', 'universa'])
print("\nRedeploy decomposition (CAGR):")
print(f"  reinvest vs hoard (E - C): {(cE-cC)*100:+.2f} pp   pure dip-timing (D - E): {(cD-cE)*100:+.2f} pp")
print(f"  Universa F vs Buy&Hold (F - A): {(cF-cA)*100:+.2f} pp   F vs immediate-ladder D (F - D): {(cF-cD)*100:+.2f} pp")

# lag sensitivity (unchanged)
lrows = [{"lag_days": 0, "CAGR": round(cD, 4), "dip_timing_vs_this": 0.0, "note": "D immediate"}]
for L in (5, 20, 60, 120):
    cL = metrics(run('ladder_equity', lag=L))['CAGR']
    lrows.append({"lag_days": L, "CAGR": round(cL, 4), "dip_timing_vs_this": round(cD - cL, 4), "note": f"buy {L}d after dip"})
lrows.append({"lag_days": "cash", "CAGR": round(cC, 4), "dip_timing_vs_this": round(cD - cC, 4), "note": "C hoard cash"})
pd.DataFrame(lrows).to_csv(os.path.join(DATA, "results_daily_redeploy_lag.csv"), index=False)

# CORE sensitivity for F (full-sample + 2020 window)
d = pd.Series(dates)
i20a = int((d >= np.datetime64("2020-02-01")).idxmax()); i20b = int((d <= np.datetime64("2020-06-30"))[::-1].idxmax())
crows = []
print("\nUniversa CORE sensitivity (full-sample + 2020 Feb-Jun window):")
for core in (0.0, 0.25, 0.30, 0.50):
    nv = run('universa', core=core); m = metrics(nv)
    ret2020 = nv[i20b] / nv[i20a] - 1
    crows.append({"core": core, "CAGR": round(m['CAGR'], 4), "maxDD": round(m['maxDD'], 4),
                  "Sharpe": round(m['Sharpe'], 3), "ret_2020_febjun": round(ret2020, 4)})
    print(f"  core {int(core*100):>3}%: CAGR {m['CAGR']*100:6.2f}%  maxDD {m['maxDD']*100:7.1f}%  2020 {ret2020*100:+6.1f}%")
pd.DataFrame(crows).to_csv(os.path.join(DATA, "results_daily_universa_core.csv"), index=False)

# crash episodes (add F)
episodes = {"1987 crash": ("1987-08-01", "1987-12-31"), "2000-02 dotcom": ("2000-03-01", "2002-10-31"),
            "2008 GFC": ("2007-10-01", "2009-03-31"), "2020 COVID": ("2020-02-01", "2020-06-30"),
            "2022 bear": ("2022-01-01", "2022-12-31")}
erows = []
print("\nCrash episodes (window return):")
for name, (a, b) in episodes.items():
    ia = int((d >= np.datetime64(a)).idxmax()); ib = int((d <= np.datetime64(b))[::-1].idxmax())
    seg = {k: navs[k][ib] / navs[k][ia] - 1 for k in ['bh', 'ladder_equity', 'universa']}
    def wdd(nav): w = nav[ia:ib + 1]; return (w / np.maximum.accumulate(w) - 1).min()
    erows.append({"episode": name, "buy_hold": round(seg['bh'], 4),
                  "ladder_immediate_D": round(seg['ladder_equity'], 4),
                  "universa_F": round(seg['universa'], 4),
                  "bh_trough_DD": round(wdd(navs['bh']), 4),
                  "D_trough_DD": round(wdd(navs['ladder_equity']), 4),
                  "F_trough_DD": round(wdd(navs['universa']), 4)})
    print(f"{name:<16} B&H {seg['bh']*100:6.1f}%  D(ladder) {seg['ladder_equity']*100:6.1f}%  F(universa) {seg['universa']*100:6.1f}%")
pd.DataFrame(erows).to_csv(os.path.join(DATA, "results_daily_crash_episodes.csv"), index=False)
print("\nWrote results_daily_ladder / _redeploy_lag / _universa_core / _crash_episodes .csv")

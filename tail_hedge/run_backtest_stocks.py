"""
Individual-name convexity backtest — JPMorgan (JPM) & American Express (AXP),
the quality financials a holder might own INSTEAD of the diluted XLF sector ETF.
================================================================================
Same PASSIVE rolled-put framework as run_backtest_sectors.py. Question: do quality
compounders (high drift) have different hedge economics (break-even VRP) than XLF?

Data   : JPM, AXP daily ADJUSTED close (1998-01 .. 2024-12), yfinance.
Outputs (data/): results_stock_profile.csv, results_stock_breakeven_windows.csv,
  results_stock_winrate_vrp.csv, results_stock_hedge_grid.csv, results_stock_paid_vrp.csv,
  and appends JPM/AXP to results_breakeven_spectrum_full.csv (with XLF/XLK/SP/DHT/FRO).
Caveats: options on adjusted (total-return) series; windowed break-evens are
crash-regime-dependent; gross of tax/cost. Single-name idiosyncratic risk is real.
"""
import os, math, datetime as dt
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, "data")
RV_WIN = 63; TENOR = 252

def norm_cdf(x): return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def bs_put_frac(k, sig, T):
    if T <= 1e-9 or sig <= 1e-9: return max(0.0, (1 - k) - 1.0)
    K = 1 - k; sq = math.sqrt(T)
    d1 = (math.log(1 / K) + 0.5 * sig * sig * T) / (sig * sq); d2 = d1 - sig * sq
    return K * norm_cdf(-d2) - norm_cdf(-d1)

def fetch_save(tk, fn):
    path = os.path.join(DATA, fn)
    if not os.path.exists(path):
        import yfinance as yf
        c = yf.download(tk, start="1998-01-01", end="2024-12-31", interval="1d",
                        progress=False, auto_adjust=True)["Close"].dropna().iloc[:, 0]
        pd.DataFrame({"Date": c.index.strftime("%Y-%m-%d"), "AdjClose": c.values}).to_csv(path, index=False)
    return path

def load(path, col="AdjClose"):
    df = pd.read_csv(path); dts = pd.to_datetime(df["Date"]).values
    s = df[col].astype(float).values
    r = np.zeros(len(s)); r[1:] = s[1:] / s[:-1] - 1
    rv = pd.Series(r).rolling(RV_WIN).std().values * math.sqrt(252)
    rv = np.where(np.isnan(rv), np.nanmean(rv[~np.isnan(rv)]), rv)
    return dts, s, r, rv

def cagr(nav): return nav[-1] ** (252 / len(nav)) - 1
def maxdd(nav): return (nav / np.maximum.accumulate(nav) - 1).min()

def hedged_nav(s, r, rv, k, vrp, tenor_days=TENOR):
    n = len(s); T0 = tenor_days / 252.0; dt_ = 1 / 252.0
    eq = 1.0; nav = np.empty(n); nav[0] = 1.0; Kabs = None; T = 0.0; q = 0.0
    def est(i):
        nonlocal Kabs, T, q, eq
        Kabs = s[i] * (1 - k); T = T0; q = eq / s[i]
        eq -= q * (bs_put_frac(k, rv[i] * (1 + vrp), T) * s[i])
    est(0)
    for i in range(1, n):
        eq *= (1 + r[i]); T -= dt_
        if T <= 1e-6:
            eq += q * max(0.0, Kabs - s[i]); est(i)
        pp = 0.0
        if T > 1e-6:
            sig = rv[i] * (1 + vrp)
            if sig > 1e-9:
                sq = math.sqrt(T); d1 = (math.log(s[i]/Kabs)+0.5*sig*sig*T)/(sig*sq); d2 = d1-sig*sq
                pp = Kabs*norm_cdf(-d2) - s[i]*norm_cdf(-d1)
            else: pp = max(0.0, Kabs - s[i])
        nav[i] = eq + q * pp
    return nav

def period_pnl(s, rv, k, vrp, step=21):
    n = len(s); T0 = TENOR / 252.0; prem = []; pay = []
    for i in range(0, n - TENOR, step):
        prem.append(bs_put_frac(k, rv[i] * (1 + vrp), T0))
        pay.append(max(0.0, (1 - k) - s[i + TENOR] / s[i]))
    return np.array(prem), np.array(pay)

def breakeven(s, r, rv, k):
    cu = cagr(np.cumprod(np.r_[1.0, 1 + r[1:]])); grid = np.arange(0.0, 3.01, 0.05); ev = []; cg = []
    for vrp in grid:
        pr, pa = period_pnl(s, rv, k, vrp); ev.append((pa - pr).mean())
        cg.append(cagr(hedged_nav(s, r, rv, k, vrp)))
    ev = np.array(ev); cg = np.array(cg)
    def cross(y, tgt):
        d = y - tgt; idx = np.where(np.diff(np.sign(d)))[0]
        if len(idx) == 0: return round(grid[-1], 2) if d[-1] > 0 else 0.0
        i0 = idx[0]; return round(grid[i0] - d[i0] * (grid[i0+1]-grid[i0]) / (d[i0+1]-d[i0]), 3)
    return cu, cross(ev, 0.0), cross(cg, cu)

names = {"JPM": load(fetch_save("JPM", "jpm_daily_1998_2024.csv")),
         "AXP": load(fetch_save("AXP", "axp_daily_1998_2024.csv"))}
K0 = 0.20

# profile
prow = []
for a, (dts, s, r, rv) in names.items():
    prow.append({"asset": a, "years": round(len(s)/252, 1),
                 "ann_vol": round(np.std(r[1:], ddof=1)*math.sqrt(252), 3),
                 "maxDD": round(maxdd(np.cumprod(np.r_[1.0, 1+r[1:]])), 3),
                 "CAGR": round(cagr(np.cumprod(np.r_[1.0, 1+r[1:]])), 4)})
pd.DataFrame(prow).to_csv(os.path.join(DATA, "results_stock_profile.csv"), index=False); print("PROFILE:", prow)

# break-even windows
wins = {"full": None, "2010+": "2010-01-01", "2015+": "2015-01-01"}; brows = []
for a, (dts, s, r, rv) in names.items():
    for w, start in wins.items():
        i0 = 0 if start is None else int((dts >= np.datetime64(start)).argmax())
        ss, rr, rvv = s[i0:], r[i0:].copy(), rv[i0:]; rr[0] = 0.0
        cu, be, bc = breakeven(ss, rr, rvv, K0)
        brows.append({"asset": a, "window": w, "years": round(len(ss)/252, 1),
                      "CAGR_unhedged": round(cu, 4), "breakeven_VRP_expectancy": be, "breakeven_VRP_CAGR": bc})
        print(f"{a} {w:<6} unhedgedCAGR {cu*100:+6.1f}%  BE_CAGR {bc}")
pd.DataFrame(brows).to_csv(os.path.join(DATA, "results_stock_breakeven_windows.csv"), index=False)

# win-rate vs VRP
wr = []
for a, (dts, s, r, rv) in names.items():
    cu = cagr(np.cumprod(np.r_[1.0, 1+r[1:]]))
    for vrp in (0.0, 0.25, 0.5, 1.0):
        pr, pa = period_pnl(s, rv, K0, vrp); pnl = pa - pr; wmask = pnl > 0
        aw = pnl[wmask].mean() if wmask.any() else 0.0; al = pnl[~wmask].mean() if (~wmask).any() else 0.0
        ch = cagr(hedged_nav(s, r, rv, K0, vrp))
        wr.append({"asset": a, "VRP": vrp, "win_rate": round(wmask.mean(), 3), "expectancy": round(pnl.mean(), 4),
                   "payoff_ratio": round(abs(aw/al), 2) if al != 0 else np.nan,
                   "CAGR_hedged": round(ch, 4), "CAGR_unhedged": round(cu, 4), "CAGR_delta": round(ch-cu, 4)})
pd.DataFrame(wr).to_csv(os.path.join(DATA, "results_stock_winrate_vrp.csv"), index=False)

# hedge grid
gr = []
for a, (dts, s, r, rv) in names.items():
    gr.append({"asset": a, "hedge": "UNHEDGED", "CAGR": round(cagr(np.cumprod(np.r_[1.0, 1+r[1:]])), 4),
               "maxDD": round(maxdd(np.cumprod(np.r_[1.0, 1+r[1:]])), 4)})
    for k in (0.20, 0.30):
        for ten in (252,):
            for vrp in (0.0, 0.5):
                nav = hedged_nav(s, r, rv, k, vrp, tenor_days=ten)
                gr.append({"asset": a, "hedge": f"k{int(k*100)}% {ten}d VRP{int(vrp*100)}%",
                           "CAGR": round(cagr(nav), 4), "maxDD": round(maxdd(nav), 4)})
pd.DataFrame(gr).to_csv(os.path.join(DATA, "results_stock_hedge_grid.csv"), index=False)

# live paid VRP (JPM/AXP options liquid)
try:
    import yfinance as yf
    today = dt.date(2026, 7, 20); prows = []
    for tk in ("JPM", "AXP"):
        t = yf.Ticker(tk); exps = t.options
        target = min(exps, key=lambda e: abs((dt.date.fromisoformat(e) - today).days - 365))
        h = t.history(period="1y")["Close"]; spot = float(h.iloc[-1])
        rvol = float(h.pct_change().dropna().tail(63).std()*math.sqrt(252))
        puts = t.option_chain(target).puts; puts = puts[(puts["openInterest"] > 0) & (puts["impliedVolatility"] > 0.05)]
        row = None
        for otm in (0.20, 0.10):
            sub = puts.copy(); sub["d"] = (sub["strike"] - spot*(1-otm)).abs(); sub = sub.sort_values("d")
            if len(sub): row = sub.iloc[0]; used = otm; break
        T = (dt.date.fromisoformat(target) - today).days/365
        if row is None:
            prows.append({"ticker": tk, "expiry": target, "spot": round(spot, 2), "note": "no liquid deep-OTM put"})
            print(f"{tk}: no liquid deep-OTM put")
        else:
            iv = float(row["impliedVolatility"])
            prows.append({"ticker": tk, "expiry": target, "T_years": round(T, 2), "spot": round(spot, 2),
                          "strike": float(row["strike"]), "otm": used, "put_IV": round(iv, 3),
                          "realized_vol_63d": round(rvol, 3), "paid_VRP": round(iv/rvol-1, 3),
                          "open_interest": int(row["openInterest"])})
            print(f"{tk} {target} spot {spot:.1f} ~{int(used*100)}%OTM strike {row['strike']:.0f} IV {iv*100:.0f}% realized {rvol*100:.0f}% paidVRP {iv/rvol-1:.2f} OI {int(row['openInterest'])}")
    pd.DataFrame(prows).to_csv(os.path.join(DATA, "results_stock_paid_vrp.csv"), index=False)
except Exception as e:
    print("live pull failed:", e)

# combined full spectrum
spec = []
try:
    sp = pd.read_csv(os.path.join(DATA, "results_breakeven_spectrum.csv"))
    for _, x in sp.iterrows():
        if x["asset"] in ("SP500", "XLF", "XLK", "DHT", "FRO") and not (x["asset"] == "SP500" and pd.isna(x["maxDD"])):
            spec.append({"asset": x["asset"], "CAGR_unhedged": x["CAGR_unhedged"], "breakeven_VRP_CAGR": x["breakeven_VRP_CAGR"]})
except Exception: pass
for a in ("JPM", "AXP"):
    full = next(b for b in brows if b["asset"] == a and b["window"] == "full")
    spec.append({"asset": a, "CAGR_unhedged": full["CAGR_unhedged"], "breakeven_VRP_CAGR": full["breakeven_VRP_CAGR"]})
pd.DataFrame(spec).to_csv(os.path.join(DATA, "results_breakeven_spectrum_full.csv"), index=False)
print("\nFULL SPECTRUM:"); [print(" ", s) for s in spec]

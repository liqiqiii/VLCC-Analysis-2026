# -*- coding: utf-8 -*-
"""
ZIM March-2022 peak — volume anatomy and tests of every claim that Reports #41/#42
left "unverified" or "untested".  v2: REBUILT after a GPT-6-Astra adversarial review.

What changed vs v1, and why (review findings in brackets):
 [1] Total return is now a GROSS wealth index built from prices + dividends,
     W_t = W_{t-1} * (P_t + D_t) / P_{t-1}  (dividend reinvested at the ex-date close).
     Yahoo's Adj Close uses P_t / (P_{t-1} - D) and overstates ex-date returns
     (ZIM 22-Mar-2022: +8.83% Yahoo vs +7.13% gross).
 [2] OBV is reported both price-signed and gross-return-signed.
 [4] Peer peaks use ONE convention at a time (price-only, then gross TR) and three
     search windows.
 [5] Event windows are symmetric (10 returns each side); benchmarks are SPY and a
     same-segment peer basket (self excluded); inference is clustered by calendar
     month; yield dependence is tested by OLS with firm + year fixed effects;
     events with an earnings release inside the window are excluded where dates exist.
 [6] Tops are tested on price-only and gross-TR series separately, with complete
     +/-252-session horizons, active payer = dividend in the prior 126 sessions only,
     and a placebo null that shifts each issuer's own ex-date calendar.
 [7][8] Back-test: next-session reference price (executable), state-matched nulls
     (near-high for near-high signals; depth-matched for the momentum rule),
     incremental-volume tests (same price pattern with vs without the volume
     condition), month-block bootstrap CIs, and hold-out splits.
 [9] BWET is quarantined (unvalidated price path); no exit recommendation is made.

Data: Yahoo Finance via yfinance (auto_adjust=False; Close is split-adjusted only).
FINRA consolidated short interest (API). SCFI weekly: two GitHub copies of the
Shanghai Shipping Exchange print. Earnings dates: yfinance (partial coverage).
"""
import io
import os
import sys
import json

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA, CHARTS = os.path.join(HERE, "data"), os.path.join(HERE, "charts")
CACHE = os.path.join(os.environ.get("TEMP", HERE), "zim_peak_cache")
os.makedirs(CACHE, exist_ok=True)
START, END = "2004-01-01", "2026-10-14"
RNG = np.random.default_rng(20261013)
ZIM_SHARES = 2.04e9 / 17.0  # $2.04bn / $17 per share (ZIM PR 9-Mar-2022) = 120.0M

CONT_US = ["ZIM", "MATX", "DAC", "GSL"]
CONT_EX = ["HLAG.DE", "MAERSK-B.CO", "2603.TW", "2609.TW", "1919.HK"]
CONTAINER = CONT_US + CONT_EX
TANKER = ["FRO", "DHT", "INSW", "TNK", "NAT"]
UNIVERSE = CONTAINER + TANKER
US_DIV = CONT_US + TANKER
OUT = {}


def load(t):
    f = os.path.join(CACHE, f"{t}.csv")
    if os.path.exists(f):
        df = pd.read_csv(f, index_col=0, parse_dates=True)
    else:
        df = yf.Ticker(t).history(start=START, end=END, auto_adjust=False, actions=True)
        df.index = pd.to_datetime(df.index).tz_localize(None).normalize()
        df.to_csv(f)
    df = df[df["Close"].notna() & (df["Close"] > 0)].copy()
    df = df[~df.index.duplicated()]
    df["Dividends"] = df["Dividends"].fillna(0) if "Dividends" in df else 0.0
    c, d = df["Close"], df["Dividends"]
    g = ((c + d) / c.shift(1)).fillna(1.0)
    df["tr"] = g.cumprod() * c.iloc[0]          # gross total-return wealth index
    df["tr_ret"] = g - 1.0
    df["px_ret"] = c.pct_change()
    fac = df["tr"] / c
    for col in ["Open", "High", "Low"]:
        df["t" + col] = df[col] * fac
    v = df["Volume"].astype(float)
    df["rvol20"] = v / v.shift(1).rolling(20).mean()
    df["obv_tr"] = (np.sign(df["tr_ret"]).fillna(0) * v).cumsum()
    df["obv_px"] = (np.sign(df["px_ret"]).fillna(0) * v).cumsum()
    rng = (df["High"] - df["Low"]).replace(0, np.nan)
    df["clv"] = (((c - df["Low"]) - (df["High"] - c)) / rng).fillna(0)  # scale-invariant
    df["adl"] = (df["clv"] * v).cumsum()
    down = df["tr_ret"] <= -0.002
    df["dist25"] = (down & (v > v.shift(1))).rolling(25).sum()
    df["down25"] = down.rolling(25).sum()
    df["hi252"] = df["tHigh"].shift(1).rolling(252, min_periods=120).max()
    df["cmax252"] = df["tr"].rolling(252, min_periods=120).max()
    df["sma50"] = df["tr"].rolling(50).mean()
    return df


def earnings_dates(t):
    f = os.path.join(DATA, "earnings_dates_yfinance.csv")
    allx = pd.read_csv(f, parse_dates=["date"]) if os.path.exists(f) else pd.DataFrame(columns=["ticker", "date"])
    if t not in set(allx["ticker"]):
        try:
            e = yf.Ticker(t).get_earnings_dates(limit=100)
            dates = pd.to_datetime(e.index).tz_localize(None).normalize() if e is not None else []
        except Exception:
            dates = []
        allx = pd.concat([allx, pd.DataFrame({"ticker": t, "date": list(dates)})])
        allx.to_csv(f, index=False)
    return pd.to_datetime(allx.loc[allx.ticker == t, "date"]).sort_values().values


def updown(sl, col="tr_ret"):
    s = sl.dropna(subset=[col])
    return round(s.loc[s[col] > 0, "Volume"].sum() / s.loc[s[col] < 0, "Volume"].sum(), 2)


def cluster_ols(y, X, groups):
    """OLS with one-way cluster-robust (CR1) standard errors."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    b = XtX_inv @ X.T @ y
    u = y - X @ b
    meat = np.zeros((k, k))
    g = pd.Series(groups).astype(str).values
    G = 0
    for gv in np.unique(g):
        m = g == gv
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
        G += 1
    V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
    return b, np.sqrt(np.diag(V)), G


def cluster_mean(x, groups):
    x = np.asarray(x, float)
    b, se, G = cluster_ols(x, np.ones((len(x), 1)), groups)
    return round(float(b[0]), 4), round(float(b[0] / se[0]), 2), len(x), G


ALL_MONTHS = pd.period_range("2004-01", "2026-10", freq="M").astype(str)
MONTH_POS = {m: k for k, m in enumerate(ALL_MONTHS)}


def block_weights(L, reps):
    """Circular moving-block bootstrap over contiguous calendar months, synchronized across firms.
    Returns a (reps x M) matrix of month multiplicities."""
    M = len(ALL_MONTHS)
    nb = int(np.ceil(M / L))
    W = np.zeros((reps, M))
    starts = RNG.integers(0, M, size=(reps, nb))
    for r in range(reps):
        idx = ((starts[r][:, None] + np.arange(L)[None, :]) % M).ravel()[:M]
        np.add.at(W[r], idx, 1.0)
    return W


WB = {L: block_weights(L, 2000) for L in (3, 6, 12)}


def block_ci_mean(x, months, L):
    x = np.asarray(x, float)
    pos = np.array([MONTH_POS[m] for m in months])
    S = np.bincount(pos, weights=x, minlength=len(ALL_MONTHS))
    N = np.bincount(pos, minlength=len(ALL_MONTHS)).astype(float)
    W = WB[L]
    with np.errstate(invalid="ignore", divide="ignore"):
        m = (W @ S) / (W @ N)
    m = m[~np.isnan(m)]
    return [round(float(np.percentile(m, 2.5)), 4), round(float(np.percentile(m, 97.5)), 4)]


print("=" * 100)
print("ZIM PEAK — VOLUME ANATOMY AND CLAIM TESTS (v2)")
print("=" * 100)
D = {t: load(t) for t in UNIVERSE + ["SPY", "BWET"]}
z, spy = D["ZIM"], D["SPY"]
z[["Open", "High", "Low", "Close", "Adj Close", "Volume", "Dividends", "tr"]].to_csv(
    os.path.join(DATA, "zim_daily_yahoo.csv"), float_format="%.4f")

# ======================================================================= A
print("\nA. ZIM VOLUME ANATOMY")
win = z.loc["2022-02-22":"2022-04-14"].copy()
win["turnover_pct"] = win["Volume"] / ZIM_SHARES * 100
cols = ["Open", "High", "Low", "Close", "px_ret", "tr_ret", "Volume", "rvol20", "dist25", "turnover_pct", "Dividends"]
win[cols].to_csv(os.path.join(DATA, "zim_peak_window.csv"), float_format="%.4f")
print(win[cols].round(3).to_string())

A = {}
p_close_dt = z.loc["2021":"2023", "Close"].idxmax()
p_high_dt = z.loc["2021":"2023", "High"].idxmax()
tr_dt = z.loc["2021":"2023", "tr"].idxmax()
A["price_close_peak"] = [str(p_close_dt.date()), round(z.loc[p_close_dt, "Close"], 2)]
A["price_intraday_peak"] = [str(p_high_dt.date()), round(z.loc[p_high_dt, "High"], 2)]
A["gross_tr_peak_date"] = str(tr_dt.date())
A["gross_tr_peak_vs_3_16"] = round(z.loc[tr_dt, "tr"] / z.loc[p_close_dt, "tr"] - 1, 4)
A["ex_day_return_gross_vs_yahoo"] = [round(float(z.loc["2022-03-22", "tr_ret"]), 4),
                                     round(float(z.loc["2022-03-22", "Adj Close"] / z.loc["2022-03-21", "Adj Close"] - 1), 4),
                                     round(float(z.loc["2022-03-22", "px_ret"]), 4)]
path = z.loc["2021":"2024", "tr"]
dd = path / path.cummax() - 1
A["gross_tr_max_drawdown"] = [str(path.loc[:dd.idxmin()].idxmax().date()), str(dd.idxmin().date()), round(float(dd.min()), 4)]
A["price_only_drawdown_from_close_peak"] = round(z.loc[p_close_dt:"2024-12-31", "Close"].min() / z.loc[p_close_dt, "Close"] - 1, 4)
A["intraday_low_after_peak"] = [str(z.loc["2022-03-17":"2024-12-31", "Low"].idxmin().date()), round(float(z.loc["2022-03-17":"2024-12-31", "Low"].min()), 2)]
hist = z.loc["2021-02-01":"2023-12-31"]
A["volume_rank_of_734"] = {}
for d in ["2022-03-09", "2022-03-14", "2022-03-16", "2022-03-17", "2022-03-21", "2022-03-22", "2022-03-28", "2022-03-31"]:
    d = pd.Timestamp(d)
    rk = int((hist["Volume"] > hist.loc[d, "Volume"]).sum() + 1)
    A["volume_rank_of_734"][str(d.date())] = [rk, round(rk / len(hist) * 100, 1), round(float(z.loc[d, "rvol20"]), 2),
                                             round(float(z.loc[d, "px_ret"]), 4)]
top10 = hist.nlargest(10, "Volume")
A["top10_volume_days"] = [[str(i.date()), int(r.Volume), round(float(r.rvol20), 2), round(float(r.px_ret), 4)] for i, r in top10.iterrows()]
# daily RVOL path in the rally (to show WHEN volume expanded, not just leg averages)
pre = z.loc[:p_close_dt].iloc[-61:]
leg_low_dt = pre["Close"].idxmin()
leg = z.loc[leg_low_dt:p_close_dt]
A["rally_leg"] = {"low": [str(leg_low_dt.date()), round(float(z.loc[leg_low_dt, "Close"]), 2)],
                  "gain_price": round(float(z.loc[p_close_dt, "Close"] / z.loc[leg_low_dt, "Close"] - 1), 4),
                  "sessions": len(leg) - 1,
                  "rvol_ge_1_5_from_low_through_3_16": [str(x.date()) for x in leg.index[leg["rvol20"] >= 1.5]],
                  "rvol_ge_1_5_3_9_through_3_22": [str(x.date()) for x in z.loc["2022-03-09":"2022-03-22"].index[z.loc["2022-03-09":"2022-03-22", "rvol20"] >= 1.5]],
                  "rvol_ge_1_4_3_9_through_3_22": int((z.loc["2022-03-09":"2022-03-22", "rvol20"] >= 1.4).sum())}
ip = z.index.get_loc(p_close_dt)
A["updown_volume_ratio"] = {
    "tr_signed": {"50_before": updown(z.iloc[ip - 50:ip + 1]), "25_before": updown(z.iloc[ip - 25:ip + 1]),
                  "25_after": updown(z.iloc[ip + 1:ip + 26]), "50_after": updown(z.iloc[ip + 1:ip + 51])},
    "price_signed": {"50_before": updown(z.iloc[ip - 50:ip + 1], "px_ret"), "25_before": updown(z.iloc[ip - 25:ip + 1], "px_ret"),
                     "25_after": updown(z.iloc[ip + 1:ip + 26], "px_ret"), "50_after": updown(z.iloc[ip + 1:ip + 51], "px_ret")}}
for ind in ["obv_px", "obv_tr", "adl"]:
    s = z[ind]
    A[ind] = {"new_high_on_price_peak_3_16": bool(s.loc[p_close_dt] >= s.loc[:p_close_dt].max()),
              "max_date_2021_23": str(s.loc["2021":"2023"].idxmax().date()),
              "change_3_16_to_3_31_M": round(float(s.loc["2022-03-31"] - s.loc[p_close_dt]) / 1e6, 1),
              "change_3_16_to_4_29_M": round(float(s.loc["2022-04-29"] - s.loc[p_close_dt]) / 1e6, 1)}
seg = z.loc[leg_low_dt:"2022-06-30"]
tp = (seg["tHigh"] + seg["tLow"] + seg["tr"]) / 3
avwap = (tp * seg["Volume"]).cumsum() / seg["Volume"].cumsum()
below = seg.loc[p_close_dt:].index[seg.loc[p_close_dt:, "tr"] < avwap.loc[p_close_dt:]]
A["first_close_below_rally_avwap_gross_tr"] = str(below[0].date()) if len(below) else None
A["dist25_at_price_peak"] = int(z.loc[p_close_dt, "dist25"])
A["dist25_max_feb_apr"] = [str(z.loc["2022-02-01":"2022-04-30", "dist25"].idxmax().date()), int(z.loc["2022-02-01":"2022-04-30", "dist25"].max())]
A["turnover_3_14_to_3_21_pct_of_shares_out"] = round(float(z.loc["2022-03-14":"2022-03-21", "Volume"].sum() / ZIM_SHARES * 100), 1)
A["spy_gross_tr_3_16_to_3_31"] = round(float(spy.loc["2022-03-31", "tr"] / spy.loc["2022-03-16", "tr"] - 1), 4)
A["zim_gross_tr_3_16_to_3_31"] = round(float(z.loc["2022-03-31", "tr"] / z.loc["2022-03-16", "tr"] - 1), 4)
A["zim_price_3_16_to_3_31"] = round(float(z.loc["2022-03-31", "Close"] / z.loc["2022-03-16", "Close"] - 1), 4)
rel = (z["tr"] / spy["tr"].reindex(z.index)).loc["2021":"2023"]
A["zim_over_spy_gross_tr_peak"] = str(rel.idxmax().date())
A["mar9_mar10_reaction"] = [round(float(z.loc["2022-03-09", "px_ret"]), 4), round(float(z.loc["2022-03-09", "rvol20"]), 2),
                            round(float(z.loc["2022-03-10", "px_ret"]), 4), round(float(z.loc["2022-03-10", "rvol20"]), 2)]
A["exdate_drop_ratio"] = {"open": round(float((z.loc["2022-03-21", "Close"] - z.loc["2022-03-22", "Open"]) / 17.0), 3),
                          "close": round(float((z.loc["2022-03-21", "Close"] - z.loc["2022-03-22", "Close"]) / 17.0), 3)}
si = pd.read_csv(os.path.join(DATA, "finra_short_interest_zim.csv"))
si["settlementDate"] = pd.to_datetime(si["settlementDate"])
si = si.sort_values("settlementDate")
si = si[(si.settlementDate >= "2021-10-01") & (si.settlementDate <= "2023-01-31")]
A["finra_short_interest"] = [[str(r.settlementDate.date()), int(r.currentShortPositionQuantity),
                              round(r.currentShortPositionQuantity / ZIM_SHARES * 100, 2), float(r.daysToCoverQuantity),
                              int(r.averageDailyVolumeQuantity)] for r in si.itertuples()]
OUT["A"] = A
print(json.dumps(A, indent=1, default=str))

# ======================================================================= B
print("\nB. SCFI vs EQUITY PEAKS")
sa = pd.read_csv(os.path.join(DATA, "scfi_weekly_sourceA_jordanbell2357.csv"), parse_dates=["Week"]).set_index("Week")["SCFI"]
sb = pd.read_csv(os.path.join(DATA, "scfi_weekly_sourceB_bensontryit.csv"), parse_dates=["Week"]).set_index("Week")["SCFI"]
cm = sa.index.intersection(sb.index)
diff = (sa[cm] - sb[cm]).abs()
B = {"scfi_overlap_weeks": len(cm), "scfi_weeks_differing": [str(x.date()) for x in diff.index[diff > 0.01]]}
scfi = sb.sort_index()
cyc = scfi.loc["2020":"2023"]
sp_dt = cyc.idxmax()
post = scfi.loc[sp_dt:]
B["scfi_peak"] = [str(sp_dt.date()), float(cyc.max())]
B["scfi_first_print_5pct_below_peak"] = str(post[post <= cyc.max() * 0.95].index[0].date())
B["scfi_first_print_10pct_below_peak"] = str(post[post <= cyc.max() * 0.90].index[0].date())
yoy = scfi.pct_change(52)
B["scfi_yoy_peak"] = [str(yoy.loc["2020":"2022"].idxmax().date()), round(float(yoy.loc["2020":"2022"].max()), 3)]
seq = scfi.loc[sp_dt:"2022-03-18"].diff().dropna()
B["scfi_weekly_declines_peak_to_3_18"] = [int((seq < 0).sum()), len(seq)]
B["scfi_levels"] = {d: float(scfi.loc[:d].iloc[-1]) for d in ["2022-03-18", "2022-03-25", "2022-06-30", "2022-12-30", "2023-03-31"]}
rows = []
for start in ["2021-01-01", "2021-06-01", "2021-10-01"]:
    for t in CONTAINER:
        d = D[t].loc[start:"2022-12-31"]
        for conv, col in [("price", "Close"), ("gross_tr", "tr")]:
            pk = d[col].idxmax()
            rows.append({"window_start": start, "ticker": t, "convention": conv, "peak": str(pk.date()),
                         "lag_weeks_vs_scfi_peak": round((pk - sp_dt).days / 7, 1),
                         "rvol20_on_peak": round(float(D[t].loc[pk, "rvol20"]), 2)})
peaks = pd.DataFrame(rows)
peaks.to_csv(os.path.join(DATA, "container_peaks_vs_scfi.csv"), index=False)
B["peaks_window_2021_06_01"] = peaks[peaks.window_start == "2021-06-01"].pivot(index="ticker", columns="convention", values="lag_weeks_vs_scfi_peak").to_dict()
B["peak_dates_window_2021_06_01"] = peaks[peaks.window_start == "2021-06-01"].pivot(index="ticker", columns="convention", values="peak").to_dict()
B["window_sensitivity_changes"] = []
for (t, conv), g in peaks.groupby(["ticker", "convention"]):
    if g["peak"].nunique() > 1:
        B["window_sensitivity_changes"].append([t, conv, dict(zip(g.window_start, g.peak))])
for conv in ["price", "gross_tr"]:
    s = peaks[(peaks.window_start == "2021-06-01") & (peaks.convention == conv)]["lag_weeks_vs_scfi_peak"]
    B[f"lag_weeks_{conv}"] = {"min": float(s.min()), "median": float(s.median()), "max": float(s.max()),
                              "n_after_scfi_peak": int((s > 0).sum()), "n": len(s)}
OUT["B"] = B
print(json.dumps(B, indent=1, default=str))

# ======================================================================= C
print("\nC. EX-DIVIDEND EVENT STUDY (gross TR, symmetric 10-return windows)")
trs = pd.DataFrame({t: D[t]["tr"] for t in US_DIV}).sort_index()
rets = trs.pct_change(fill_method=None)
spy_tr = spy["tr"]
ev = []
for t in US_DIV:
    d = D[t]
    peers_seg = [o for o in (TANKER if t in TANKER else CONT_US) if o != t]
    seg_idx = (1 + rets[peers_seg].mean(axis=1, skipna=True).fillna(0)).cumprod().reindex(d.index).ffill()
    sp = spy_tr.reindex(d.index).ffill()
    ed = earnings_dates(t)
    cov_start = pd.Timestamp(ed.min()) if len(ed) else None
    W = d["tr"]
    for i in np.where(d["Dividends"].values > 0)[0]:
        if i < 31 or i + 20 >= len(d):
            continue
        dv, pc = d["Dividends"].iloc[i], d["Close"].iloc[i - 1]
        w0, w1 = d.index[i - 11], d.index[i + 9]
        if cov_start is None or d.index[i - 11] < cov_start:
            clean = np.nan
        else:
            clean = float(not ((ed >= np.datetime64(w0)) & (ed <= np.datetime64(w1))).any())
        r = lambda s, a, b: s.iloc[b] / s.iloc[a] - 1
        base_v = d["Volume"].iloc[i - 31:i - 11].mean()
        ev.append({"ticker": t, "segment": "tanker" if t in TANKER else "container", "exdate": d.index[i],
                   "div": dv, "yield": dv / pc,
                   "pre_spy": r(W, i - 11, i - 1) - r(sp, i - 11, i - 1),
                   "post_spy": r(W, i - 1, i + 9) - r(sp, i - 1, i + 9),
                   "pre_seg": r(W, i - 11, i - 1) - r(seg_idx, i - 11, i - 1),
                   "post_seg": r(W, i - 1, i + 9) - r(seg_idx, i - 1, i + 9),
                   "post20_seg": r(W, i - 1, i + 19) - r(seg_idx, i - 1, i + 19),
                   "exday_gross": d["tr_ret"].iloc[i],
                   "drop_ratio_open": (pc - d["Open"].iloc[i]) / dv,
                   "rvol_cum_day": d["Volume"].iloc[i - 1] / base_v if base_v > 0 else np.nan,
                   "rvol_ex_day": d["Volume"].iloc[i] / base_v if base_v > 0 else np.nan,
                   "earnings_clean": clean})
ev = pd.DataFrame(ev)
ev["month"] = ev["exdate"].dt.to_period("M").astype(str)
ev["year"] = ev["exdate"].dt.year
ev["bucket"] = pd.cut(ev["yield"], [0, 0.02, 0.05, 10.0], labels=["<2%", "2-5%", ">=5%"], right=False)
ev.to_csv(os.path.join(DATA, "exdiv_event_study.csv"), index=False, float_format="%.5f")


def ev_summary(g):
    out = {"n": len(g)}
    for c in ["pre_spy", "post_spy", "pre_seg", "post_seg", "post20_seg"]:
        x = g[c].replace([np.inf, -np.inf], np.nan)
        m = x.notna()
        if m.sum() <= 5:
            out[c] = None
            continue
        out[c] = {"mean": round(float(x[m].mean()), 4), "n": int(m.sum()),
                  "ci95_block3": block_ci_mean(x[m], g.loc[m, "month"].values, 3),
                  "ci95_block6": block_ci_mean(x[m], g.loc[m, "month"].values, 6)}
    out["drop_ratio_open_median"] = round(float(g["drop_ratio_open"].median()), 3)
    out["rvol_cum_day_median"] = round(float(g["rvol_cum_day"].median()), 2)
    out["rvol_ex_day_median"] = round(float(g["rvol_ex_day"].median()), 2)
    return out


C = {"all": ev_summary(ev)}
for b, g in ev.groupby("bucket", observed=True):
    C["yield " + str(b)] = ev_summary(g)
C["tanker_yield_ge2pct"] = ev_summary(ev[(ev.segment == "tanker") & (ev["yield"] >= 0.02)])
C["container_us_yield_ge2pct"] = ev_summary(ev[(ev.segment == "container") & (ev["yield"] >= 0.02)])
cov = ev[ev.earnings_clean.notna()]
cl = ev[ev.earnings_clean == 1.0]
C["covered_all"] = ev_summary(cov)
C["earnings_clean_all"] = ev_summary(cl)
C["covered_yield_ge2pct"] = ev_summary(cov[cov["yield"] >= 0.02])
C["earnings_clean_yield_ge2pct"] = ev_summary(cl[cl["yield"] >= 0.02])
C["earnings_coverage"] = {"all": len(ev), "covered": len(cov), "clean": len(cl),
                          "covered_definition": "event window start (t-11) on/after the issuer's first yfinance earnings date"}
# yield dependence: pre_seg ~ yield + firm FE + year FE; month-clustered t AND moving-block bootstrap of the slope
for dep in ["pre_seg", "post_seg"]:
    g = ev.dropna(subset=[dep]).copy().reset_index(drop=True)
    y_ = g["yield"].clip(upper=0.30).values
    Xf = pd.get_dummies(g["ticker"], drop_first=True, dtype=float)
    Xy = pd.get_dummies(g["year"], prefix="y", drop_first=True, dtype=float)
    X = np.column_stack([np.ones(len(g)), y_, Xf.values, Xy.values])
    b, se, G = cluster_ols(g[dep].values, X, g["month"].values)
    pos = np.array([MONTH_POS[m] for m in g["month"]])
    slopes = []
    for r in range(1000):
        wm = WB[6][r][pos]
        sw = np.sqrt(wm)
        keep = wm > 0
        bb = np.linalg.lstsq(X[keep] * sw[keep, None], g[dep].values[keep] * sw[keep], rcond=None)[0]
        slopes.append(bb[1])
    C[f"yield_slope_{dep}_firm_year_FE"] = {"slope": round(float(b[1]), 3), "t_month_cluster": round(float(b[1] / se[1]), 2),
                                           "ci95_block6": [round(float(np.percentile(slopes, 2.5)), 3), round(float(np.percentile(slopes, 97.5)), 3)],
                                           "n": len(g)}
C["zim_events"] = ev[ev.ticker == "ZIM"][["exdate", "yield", "pre_seg", "post_seg", "post20_seg", "rvol_cum_day", "rvol_ex_day"]].assign(
    exdate=lambda x: x.exdate.dt.date.astype(str)).round(4).values.tolist()
OUT["C"] = C
print(json.dumps(C, indent=1, default=str))

# ======================================================================= D
print("\nD. MAJOR TOPS (complete +/-252 horizons) AND EX-DATE PROXIMITY")


def major_tops(s, half=252, fall=0.40):
    a = s.values
    out = []
    for i in range(half, len(a) - half):
        w = a[i - half:i + half + 1]
        if a[i] < w.max() or a[i] <= 0:
            continue
        if a[i:i + half + 1].min() <= a[i] * (1 - fall):
            if out and i - out[-1] <= 21:
                continue
            out.append(i)
    return out


tops = []
for t in UNIVERSE:
    d = D[t]
    div_ix = np.where(d["Dividends"].values > 0)[0]
    for conv, col in [("gross_tr", "tr"), ("price", "Close")]:
        for i in major_tops(d[col]):
            prv = div_ix[div_ix <= i]
            nxt = div_ix[div_ix > i]
            j = i + int(np.argmin(d[col].values[i:i + 253]))
            tops.append({"ticker": t, "convention": conv, "i": i, "date": str(d.index[i].date()),
                         "trough": str(d.index[j].date()), "depth": round(float(d[col].iloc[j] / d[col].iloc[i] - 1), 3),
                         "active_payer": bool(len(prv) and i - prv[-1] <= 126),
                         "since_last_ex": int(i - prv[-1]) if len(prv) else None,
                         "to_next_ex": int(nxt[0] - i) if len(nxt) else None,
                         "rvol20": round(float(d["rvol20"].iloc[i]), 2)})
tops = pd.DataFrame(tops)
tops.to_csv(os.path.join(DATA, "major_tops.csv"), index=False)


DIVIX = {t: np.where(D[t]["Dividends"].values > 0)[0] for t in UNIVERSE}


def prox_counts(tp, shift_map=None):
    before = after = 0
    for r in tp.itertuples():
        dix = DIVIX[r.ticker]
        if shift_map is not None:
            dix = dix + shift_map[r.ticker]
        before += int(((dix - r.i >= 1) & (dix - r.i <= 5)).any())
        after += int(((r.i - dix >= 0) & (r.i - dix <= 5)).any())
    return before, after


Dd = {"n_tops": tops.groupby("convention").size().to_dict()}
for conv in ["gross_tr", "price"]:
    tp = tops[(tops.convention == conv) & tops.active_payer]
    ob, oa = prox_counts(tp)
    shifts = np.r_[np.arange(-40, -5), np.arange(6, 41)]
    sims = []
    for _ in range(3000):
        sm = {t: int(RNG.choice(shifts)) for t in UNIVERSE}
        sims.append(prox_counts(tp, sm))
    sims = np.array(sims)
    # DESCRIPTIVE contrast only (not a calibrated null): the same tops vs each issuer's ex-date
    # calendar displaced by 6-40 sessions. Eligibility and the dividend effects in the TR series are NOT re-simulated.
    Dd[conv] = {"active_payer_tops": len(tp),
                "peak_1_to_5_sessions_BEFORE_ex": ob, "displaced_calendar_mean_before": round(float(sims[:, 0].mean()), 2),
                "displaced_draws_ge_obs_before_of_3000": int((sims[:, 0] >= ob).sum()),
                "peak_0_to_5_sessions_AFTER_ex": oa, "displaced_calendar_mean_after": round(float(sims[:, 1].mean()), 2),
                "displaced_draws_ge_obs_after_of_3000": int((sims[:, 1] >= oa).sum()),
                "tops": tp[["ticker", "date", "since_last_ex", "to_next_ex"]].values.tolist()}
Dd["rvol20_at_tops_gross_tr"] = {"median": float(tops[tops.convention == "gross_tr"].rvol20.median()),
                                 "share_ge_1_3": round(float((tops[tops.convention == "gross_tr"].rvol20 >= 1.3).mean()), 2),
                                 "share_ge_2": round(float((tops[tops.convention == "gross_tr"].rvol20 >= 2).mean()), 2)}
OUT["D"] = Dd
print(json.dumps({k: v for k, v in Dd.items()}, indent=1, default=str)[:6000])

# ======================================================================= E
print("\nE. FLAG BACK-TEST (next-session reference, state-matched nulls, month-block bootstrap)")


def signals(d):
    s = pd.DataFrame(index=d.index)
    a, rv = d["tr"], d["rvol20"]
    near = a >= 0.9 * d["cmax252"]
    recent_near = a.rolling(20).max() >= 0.9 * d["cmax252"]
    rev = (d["tHigh"] >= d["hi252"]) & (d["Close"] < d["Open"]) & (d["clv"] <= 0)
    s["F5_rev_vol"] = rev & (rv >= 1.3)
    s["F5_rev_novol"] = rev & (rv < 1.3)
    s["DIST_cluster"] = (d["dist25"] >= 6) & near & ~((d["dist25"].shift(1) >= 6) & near.shift(1, fill_value=False))
    s["DOWN_cluster_novol"] = (d["down25"] >= 9) & near & ~((d["down25"].shift(1) >= 9) & near.shift(1, fill_value=False))
    hi63 = a >= a.rolling(63).max()
    obv_low = d["obv_px"] < d["obv_px"].shift(1).rolling(63).max()
    s["NEWHI63_obv_div"] = hi63 & near & obv_low
    s["NEWHI63_obv_conf"] = hi63 & near & ~obv_low
    cross50 = (a < d["sma50"]) & (a.shift(1) >= d["sma50"].shift(1)) & recent_near
    s["BREAK50_vol"] = cross50 & (rv >= 1.5)
    s["BREAK50_novol"] = cross50 & (rv < 1.5)
    gap = (d["tOpen"] <= a.shift(1) * 0.95) & recent_near
    s["GAPDOWN_vol"] = gap & (rv >= 1.5)
    s["GAPDOWN_novol"] = gap & (rv < 1.5)
    s["DROP8"] = (d["tr_ret"] <= -0.08) & recent_near
    m90 = a.rolling(90).max()
    s["MOM20"] = (a <= 0.8 * m90) & (a.shift(1) > 0.8 * m90.shift(1))
    return s.fillna(False)


SIG = ["F5_rev_vol", "F5_rev_novol", "DIST_cluster", "DOWN_cluster_novol", "NEWHI63_obv_div", "NEWHI63_obv_conf",
       "BREAK50_vol", "BREAK50_novol", "GAPDOWN_vol", "GAPDOWN_novol", "DROP8", "MOM20"]
PAIRS = [("F5_rev_vol", "F5_rev_novol"), ("DIST_cluster", "DOWN_cluster_novol"), ("NEWHI63_obv_div", "NEWHI63_obv_conf"),
         ("BREAK50_vol", "BREAK50_novol"), ("GAPDOWN_vol", "GAPDOWN_novol")]
NULL_OF = {s: "NULL_near" for s in SIG}
NULL_OF["MOM20"] = "NULL_depth"


def outcome(a, i):
    ref = a[i + 1]
    fw = a[i + 2:i + 128]
    jm = int(np.argmin(fw))
    return (fw[jm] <= 0.75 * ref) and (fw[:jm + 1].max() < 1.10 * ref), a[i + 64] / ref - 1


obs = []
for t in UNIVERSE:
    d = D[t]
    if len(d) < 600:
        continue
    s = signals(d)
    a = d["tr"].values
    n = len(a)
    near = (d["tr"] >= 0.9 * d["cmax252"]).values
    m90 = d["tr"].rolling(90).max().values
    months = d.index.to_period("M").astype(str)
    years = d.index.year
    for i in range(252, n - 129):
        h, r63 = outcome(a, i)
        if near[i]:
            obs.append((t, "NULL_near", months[i], years[i], h, r63))
        if 0.75 <= a[i] / m90[i] <= 0.85:
            obs.append((t, "NULL_depth", months[i], years[i], h, r63))
    for sg in SIG:
        last = -999
        for i in np.where(s[sg].values)[0]:
            if i - last < 20 or i < 252 or i >= n - 129:
                continue
            last = i
            h, r63 = outcome(a, i)
            obs.append((t, sg, months[i], years[i], h, r63))
obs = pd.DataFrame(obs, columns=["ticker", "group", "month", "year", "hit", "r63"])
obs[~obs.group.isin(["NULL_near", "NULL_depth"])].to_csv(os.path.join(DATA, "flag_triggers.csv"), index=False, float_format="%.4f")


def boot_diff(df, g1, g2, L):
    """Difference in hit rates; trigger and comparison resampled JOINTLY with the same
    synchronized moving blocks of L contiguous calendar months."""
    sub = df[df.group.isin([g1, g2])]
    M = len(ALL_MONTHS)
    H = np.zeros((M, 2))
    N = np.zeros((M, 2))
    for (m, g), x in sub.groupby(["month", "group"]):
        col = 0 if g == g1 else 1
        H[MONTH_POS[m], col] = x.hit.sum()
        N[MONTH_POS[m], col] = len(x)
    w = WB[L]
    with np.errstate(invalid="ignore", divide="ignore"):
        dlt = (w @ H[:, 0]) / (w @ N[:, 0]) - (w @ H[:, 1]) / (w @ N[:, 1])
    dlt = dlt[~np.isnan(dlt)]
    point = H[:, 0].sum() / N[:, 0].sum() - H[:, 1].sum() / N[:, 1].sum()
    return round(float(point), 3), [round(float(np.percentile(dlt, 2.5)), 3), round(float(np.percentile(dlt, 97.5)), 3)], int(N[:, 0].sum())


def evaluate(df, label):
    rows = []
    for sg in SIG:
        g = df[df.group == sg]
        if len(g) < 5:
            continue
        nul = NULL_OF[sg]
        pt, ci6, n = boot_diff(df, sg, nul, 6)
        _, ci12, _ = boot_diff(df, sg, nul, 12)
        rows.append({"sample": label, "signal": sg, "n": n, "hit": round(float(g.hit.mean()), 3),
                     "comparison": nul, "comparison_hit": round(float(df[df.group == nul].hit.mean()), 3),
                     "diff": pt, "ci95_block6m": ci6, "ci95_block12m": ci12, "median_r63": round(float(g.r63.median()), 3)})
    for v1, v0 in PAIRS:
        if (df.group == v1).sum() >= 5 and (df.group == v0).sum() >= 5:
            pt, ci6, n = boot_diff(df, v1, v0, 6)
            _, ci12, _ = boot_diff(df, v1, v0, 12)
            rows.append({"sample": label, "signal": f"{v1} minus {v0}", "n": n, "comparison": v0,
                         "diff": pt, "ci95_block6m": ci6, "ci95_block12m": ci12})
    return rows


res = []
res += evaluate(obs, "all")
res += evaluate(obs[obs.ticker != "ZIM"], "ex_ZIM")
res += evaluate(obs[obs.ticker.isin(TANKER)], "tankers")
res += evaluate(obs[obs.year <= 2015], "2004-2015")
res += evaluate(obs[obs.year >= 2016], "2016-2026")
res = pd.DataFrame(res)
res.to_csv(os.path.join(DATA, "flag_backtest.csv"), index=False)
E = {"results": res.to_dict("records")}
zs = signals(z).loc["2021-12-01":"2022-07-31"]
E["zim_signal_dates_dec21_jul22"] = {sg: [str(x.date()) for x in zs.index[zs[sg]]] for sg in SIG if zs[sg].any()}
OUT["E"] = E
pd.set_option("display.width", 250)
print(res.to_string())

# ======================================================================= F
print("\nF. CURRENT OBSERVATIONS (not a validated system)")
F = {}
for t in ["FRO", "DHT", "INSW"]:
    d = D[t]
    s = signals(d)
    l20 = s.iloc[-20:]
    divs = d.loc[d["Dividends"] > 0, "Dividends"].iloc[-4:]
    yl = [[str(i.date()), round(float(v), 3), round(float(v / d["Close"].iloc[d.index.get_loc(i) - 1]), 4)] for i, v in divs.items()]
    ed = earnings_dates(t)
    nxt = [str(pd.Timestamp(x).date()) for x in ed if pd.Timestamp(x) > d.index[-1]]
    F[t] = {"last_date": str(d.index[-1].date()), "close": round(float(d["Close"].iloc[-1]), 2),
            "gross_tr_vs_52w_closing_high": round(float(d["tr"].iloc[-1] / d["tr"].iloc[-252:].max() - 1), 4),
            "52w_closing_high_date": str(d["tr"].iloc[-252:].idxmax().date()),
            "rvol20": round(float(d["rvol20"].iloc[-1]), 2), "dist25": int(d["dist25"].iloc[-1]),
            "above_sma50": bool(d["tr"].iloc[-1] > d["sma50"].iloc[-1]),
            "updown_vol_25_price_signed": updown(d.iloc[-25:], "px_ret"),
            "signals_last_20": {sg: [str(x.date()) for x in l20.index[l20[sg]]] for sg in SIG if l20[sg].any()},
            "last_4_dividends_date_amt_yield": yl, "next_earnings_yf": nxt[:1]}
b = D["BWET"]
F["BWET_quarantined"] = {"note": "unvalidated price path; not used for conclusions",
                         "quarter_end_closes": {str(k.date()): round(float(v), 2) for k, v in b["Close"].resample("QE").last().tail(6).items()}}
OUT["F"] = F
print(json.dumps(F, indent=1, default=str))
with open(os.path.join(DATA, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(OUT, fh, indent=1, default=str)

# ======================================================================= charts
fig, ax = plt.subplots(3, 1, figsize=(12, 11), sharex=True, gridspec_kw={"height_ratios": [3, 1.4, 1.4]})
w = z.loc["2022-01-03":"2022-06-30"]
ax[0].plot(w.index, w["Close"], color="#111827", label="ZIM close (price only)")
ax[0].plot(w.index, w["tr"] * (w["Close"].iloc[0] / w["tr"].iloc[0]), color="#2980b9", ls="--", label="ZIM gross total return (rebased to 3-Jan close)")
a2 = ax[0].twinx()
sc = scfi.loc["2022-01-01":"2022-06-30"]
a2.plot(sc.index, sc.values, color="#c0392b", marker="o", ms=3, label="SCFI (weekly)")
a2.set_ylabel("SCFI")
lo_, hi_ = w["Close"].min() * 0.8, max(w["Close"].max(), (w["tr"] * (w["Close"].iloc[0] / w["tr"].iloc[0])).max()) * 1.05
ax[0].set_ylim(lo_, hi_)
for dt, lab in [("2022-03-09", "results + $17 div"), ("2022-03-16", "price close high"), ("2022-03-22", "ex-div / TR high"), ("2022-03-28", "Shanghai lockdown")]:
    ax[0].axvline(pd.Timestamp(dt), color="grey", lw=0.7, ls=":")
    ax[0].text(pd.Timestamp(dt), lo_ * 1.02, " " + lab, rotation=90, fontsize=7, va="bottom")
ax[0].legend(loc="upper left", fontsize=8)
a2.legend(loc="upper right", fontsize=8)
ax[0].set_title("ZIM 2022: price, gross total return, SCFI")
ax[1].bar(w.index, w["Volume"] / 1e6, color=np.where(w["px_ret"] >= 0, "#27ae60", "#c0392b"), width=1.0)
ax[1].plot(w.index, w["Volume"].shift(1).rolling(20).mean() / 1e6, color="black", lw=1, label="20d avg volume")
ax[1].set_ylabel("Volume (M)")
ax[1].legend(fontsize=8)
ax[2].plot(w.index, (w["obv_px"] - w["obv_px"].iloc[0]) / 1e6, color="#8e44ad", label="OBV (price-signed)")
ax[2].plot(w.index, (w["obv_tr"] - w["obv_tr"].iloc[0]) / 1e6, color="#8e44ad", ls="--", label="OBV (gross-return-signed)")
ax[2].plot(w.index, (w["adl"] - w["adl"].iloc[0]) / 1e6, color="#16a085", label="A/D line")
ax[2].set_ylabel("M shares")
ax[2].legend(fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "zim_2022_price_volume_scfi.png"), dpi=130)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.5))
pk = peaks[peaks.window_start == "2021-06-01"].pivot(index="ticker", columns="convention", values="peak").apply(pd.to_datetime)
pk = pk.sort_values("price")
y = np.arange(len(pk))
ax.scatter(pk["price"], y, color="#111827", label="price-only peak", zorder=3)
ax.scatter(pk["gross_tr"], y, color="#2980b9", marker="x", label="gross-TR peak", zorder=3)
ax.set_yticks(y)
ax.set_yticklabels(pk.index)
ax.axvline(sp_dt, color="#c0392b", ls="--", label=f"SCFI peak {sp_dt.date()}")
ax.axvline(pd.Timestamp(B["scfi_yoy_peak"][0]), color="#e67e22", ls=":", label="SCFI YoY-growth peak")
ax.legend(fontsize=8)
ax.set_title("Container equities (window from 2021-06-01): peak dates vs SCFI")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "container_peaks_vs_scfi.png"), dpi=130)
plt.close()

fig, ax = plt.subplots(figsize=(10, 4.5))
bk = ev.groupby("bucket", observed=True)[["pre_seg", "post_seg"]].mean() * 100
bk.columns = ["10 sessions before ex-date", "ex-date + 9 sessions"]
bk.plot(kind="bar", ax=ax, color=["#2980b9", "#c0392b"])
ax.axhline(0, color="black", lw=0.7)
ax.set_ylabel("Mean gross return minus segment basket, %")
ax.set_title(f"Ex-dividend event study: {len(ev)} events, 9 US-listed shipping names, by dividend yield")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "exdiv_event_study.png"), dpi=130)
plt.close()
print("\nDone.")

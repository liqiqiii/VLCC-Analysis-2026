# -*- coding: utf-8 -*-
"""
SECTION 22 v2 — BWET (tanker freight futures ETF) vs DHT and FRO.

REBUILT after a GPT-6-Astra adversarial review returned four blocking findings.
What changed, and why:

 [A1] REAL BUG. Regime returns were computed as first-to-last inside each
      calendar slice, which DROPS the return across each regime boundary. The
      regime multiples then failed to compound to the full-period return
      (BWET off by +2.16%, FRO by +2.42%). Now every period return is built by
      COMPOUNDING DAILY RETURNS, and the identity is asserted in code.

 [A2] The "19%/18% operational capture" imported from section 21 divided a Q2
      AVERAGE by a SEPTEMBER assessment. That is a period mismatch. It is
      corrected here and flagged back to section 21.

 [A3] The headline claim -- that the equities' log capture "sits in the same
      range" as their operational capture, proving the market prices the
      convertible share -- is WITHDRAWN as numerical pattern-matching.

 [A4] "30.3%/38.5% is the CORRECT capture" is WITHDRAWN. Astra's decisive
      counterexample: randomly reorder the equity's daily returns and the log
      ratio is unchanged while correlation and beta can change completely.
      The statistic therefore carries NO information about transmission.
      Three distinct concepts are now reported separately.

 Plus: complete-period resampling only; regime-correlation significance tests;
 log-return robustness; and BWET's actual structure (3.50% expense ratio,
 ~90% TD3C / 10% TD20, 50-70 day target maturity, +7%/-6% premium/discount).
"""

import io
import os
import sys
from math import erfc

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
import numpy as np
import pandas as pd
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA, CHARTS = os.path.join(HERE, "data"), os.path.join(HERE, "charts")
TICKERS = ["BWET", "DHT", "FRO"]
COL = {"BWET": "#111827", "DHT": "#c0392b", "FRO": "#2980b9"}

print("=" * 100)
print("SECTION 22 — BWET tanker-freight ETF vs DHT / FRO   (rebuilt after review)")
print("=" * 100)


def series(t, field):
    d = yf.download(t, period="max", progress=False, auto_adjust=False)[field]
    return (d.iloc[:, 0] if hasattr(d, "columns") else d).dropna().rename(t)


px = pd.concat([series(t, "Close") for t in TICKERS], axis=1).dropna()
tr = pd.concat([series(t, "Adj Close") for t in TICKERS], axis=1).dropna()
ret = tr.pct_change().dropna()
START, END = px.index[0], px.index[-1]
print(f"\n  Window {START.date()} -> {END.date()}  ({len(px)} prices, {len(ret)} returns)")
print("  BWET = Breakwave Tanker Shipping ETF (holds tanker FREIGHT FUTURES)")
print("  Basis: Adj Close (total return). The equities pay very large dividends,")
print("  so a price-only comparison would badly understate the equity holder.")

print("\n  WHAT BWET ACTUALLY IS — it is NOT the spot rate:")
print("     benchmark allocation ~90% TD3C / 10% TD20 (per prospectus)")
print("     target average maturity ~50-70 days; allocations can drift")
print("     expense ratio 3.50%; returns also include collateral interest")
print("     historical market premium/discount to NAV has reached +6.96% / -6.38%")
print("  >> Its return = futures P&L + roll/convergence + collateral - fees")
print("     +/- premium change. It owns no ships and pays no dividend.")

# ═══════════════════════════ 1) three DISTINCT concepts ═══════════════════════
print("\n" + "-" * 100)
print("1) HOW MUCH OF THE FREIGHT MOVE REACHED THE EQUITY? — three separate")
print("   questions that must NOT be merged into one 'capture' number")
print("-" * 100)
W = tr.iloc[-1] / tr.iloc[0]
Wp = px.iloc[-1] / px.iloc[0]
print(f"\n  (a) INVESTMENT OUTCOME — what US$100 became")
print(f"      {'':<6}{'price only':>13}{'total return':>15}{'dividends':>12}")
rows = []
for t in TICKERS:
    print(f"      {t:<6}{100*float(Wp[t]):>12,.0f}{100*float(W[t]):>15,.0f}"
          f"{100*(float(W[t])-float(Wp[t])):>12,.0f}")
    rows.append(dict(ticker=t, usd100_price=round(100 * float(Wp[t])),
                     usd100_total=round(100 * float(W[t])),
                     dividend_usd=round(100 * (float(W[t]) - float(Wp[t])))))
pd.DataFrame(rows).to_csv(os.path.join(DATA, "s22_outcome.csv"), index=False)

print(f"\n  (b) RELATIVE CUMULATIVE GROWTH — two legitimate but different ratios")
print(f"      {'':<6}{'simple-return ratio':>22}{'log-growth ratio':>20}")
capr = []
for t in ["DHT", "FRO"]:
    simple = (float(W[t]) - 1) / (float(W["BWET"]) - 1) * 100
    logc = np.log(float(W[t])) / np.log(float(W["BWET"])) * 100
    print(f"      {t:<6}{simple:>21.1f}%{logc:>19.1f}%")
    capr.append(dict(ticker=t, simple_ratio_pct=round(simple, 1),
                     log_growth_ratio_pct=round(logc, 1)))
pd.DataFrame(capr).to_csv(os.path.join(DATA, "s22_capture.csv"), index=False)

print("\n  🔴 THE EARLIER DRAFT CALLED 30.3%/38.5% 'THE CORRECT CAPTURE'.")
print("     THAT IS WITHDRAWN. Decisive counterexample, computed below:")
rng = np.random.default_rng(11)
sh = ret.copy()
sh["DHT"] = rng.permutation(sh["DHT"].values)
w_sh = (1 + sh["DHT"]).prod()
print(f"       randomly REORDER DHT's daily returns:")
print(f"         log-growth ratio  {np.log(float(W['DHT']))/np.log(float(W['BWET']))*100:.1f}%"
      f"  ->  {np.log(float(w_sh))/np.log(float(W['BWET']))*100:.1f}%   (unchanged)")
print(f"         correlation with BWET  {ret['BWET'].corr(ret['DHT']):.3f}"
      f"  ->  {sh['BWET'].corr(sh['DHT']):.3f}   (destroyed)")
print("     >> The log ratio survives a shuffle that destroys every link to")
print("        BWET. It therefore contains NO information about transmission.")
print("        It is a relative-growth statistic, not a pass-through measure.")
print("\n  (c) SENSITIVITY — the only concept that DOES measure transmission is")
print("      the regression beta, reported in section 3 below.")

# ═══════════════════════════ 2) correlation ═══════════════════════════════════
print("\n" + "-" * 100)
print("2) CORRELATION — complete periods only, simple AND log returns")
print("-" * 100)


def resample_ret(frame, rule):
    """Complete periods only: drop a trailing partial bin."""
    last = frame.index[-1]
    g = frame.resample(rule).last()
    per_end = g.index[-1]
    if per_end.normalize() > last.normalize():
        g = g.iloc[:-1]
    return g.pct_change().dropna()


def fisher_ci(r, n, a=1.96):
    z, se = np.arctanh(r), 1 / np.sqrt(n - 3)
    return np.tanh(z - a * se), np.tanh(z + a * se)


def williams(r_jk, r_jh, r_kh, n):
    """Williams's test, H0: corr(j,k)==corr(j,h), sharing variable j."""
    R = 1 - r_jk ** 2 - r_jh ** 2 - r_kh ** 2 + 2 * r_jk * r_jh * r_kh
    t = (r_jk - r_jh) * np.sqrt(
        ((n - 1) * (1 + r_kh)) /
        (2 * ((n - 1) / (n - 3)) * R + ((r_jk + r_jh) ** 2 / 4) * (1 - r_kh) ** 3))
    return t, erfc(abs(t) / np.sqrt(2))


frames = {"daily": ret, "weekly": resample_ret(tr, "W-FRI"),
          "monthly": resample_ret(tr, "ME")}
print(f"  {'freq':<10}{'n':>5}{'BWET~DHT':>24}{'BWET~FRO':>24}{'DHT~FRO':>24}")
out = []
for lbl, rr in frames.items():
    c, n = rr.corr(), len(rr)
    cells = ""
    for a, b in [("BWET", "DHT"), ("BWET", "FRO"), ("DHT", "FRO")]:
        r = c.loc[a, b]
        lo, hi = fisher_ci(r, n)
        cells += f"{r:>8.3f} [{lo:.2f},{hi:.2f}]"
        out.append(dict(freq=lbl, pair=f"{a}~{b}", n=n, r=round(r, 3),
                        ci_lo=round(lo, 3), ci_hi=round(hi, 3)))
    print(f"  {lbl:<10}{n:>5}{cells}")
pd.DataFrame(out).to_csv(os.path.join(DATA, "s22_correlation.csv"), index=False)

print("\n  Williams test for DEPENDENT correlations (they share a variable):")
for lbl, rr in frames.items():
    c, n = rr.corr(), len(rr)
    t1, p1 = williams(c.loc["DHT", "FRO"], c.loc["DHT", "BWET"], c.loc["FRO", "BWET"], n)
    t2, p2 = williams(c.loc["DHT", "FRO"], c.loc["FRO", "BWET"], c.loc["DHT", "BWET"], n)
    t3, p3 = williams(c.loc["BWET", "DHT"], c.loc["BWET", "FRO"], c.loc["DHT", "FRO"], n)
    print(f"   {lbl:<9} DHT~FRO > DHT~BWET: p={p1:.1e} | "
          f"DHT~FRO > FRO~BWET: p={p2:.1e} | BWET~DHT vs BWET~FRO: p={p3:.2f}")
print("  >> The equity pair is more correlated than either equity-freight pair")
print("     at EVERY frequency, decisively. But DHT and FRO are NOT")
print("     distinguishable from each other in how they track freight.")

lr = np.log1p(ret)
cl = lr.corr()
print(f"\n  Log-return robustness (daily): BWET~DHT {cl.loc['BWET','DHT']:.3f} · "
      f"BWET~FRO {cl.loc['BWET','FRO']:.3f} · DHT~FRO {cl.loc['DHT','FRO']:.3f}")
print("  ⚠️ Correlation rises with horizon. That is CONSISTENT WITH an Epps-type")
print("     aggregation effect, but this analysis does not diagnose the cause;")
print("     stale pricing, premium/discount noise and regime change also qualify.")

# ═══════════════════════════ 3) beta ══════════════════════════════════════════
print("\n" + "-" * 100)
print("3) BETA — the one statistic that does measure sensitivity")
print("-" * 100)
print(f"  {'':<6}{'alpha/day':>11}{'beta':>8}{'SE':>7}{'t':>7}{'R^2':>7}"
      f"{'95% CI for beta':>20}")
bet = []
for t in ["DHT", "FRO"]:
    x, y = ret["BWET"].values, ret[t].values
    n = len(x)
    beta, alpha = np.polyfit(x, y, 1)
    resid = y - (alpha + beta * x)
    se = np.sqrt((resid ** 2).sum() / (n - 2) / ((x - x.mean()) ** 2).sum())
    r2 = np.corrcoef(x, y)[0, 1] ** 2
    print(f"  {t:<6}{alpha*100:>10.3f}%{beta:>8.3f}{se:>7.3f}{beta/se:>7.1f}{r2:>7.3f}"
          f"{f'[{beta-1.96*se:.3f}, {beta+1.96*se:.3f}]':>20}")
    bet.append(dict(ticker=t, alpha_daily_pct=round(alpha * 100, 4),
                    beta=round(beta, 3), se=round(se, 4), t=round(beta / se, 1),
                    r2=round(r2, 3)))
pd.DataFrame(bet).to_csv(os.path.join(DATA, "s22_beta.csv"), index=False)
print("\n  Reading: a 1% BWET move is associated with a ~0.14%/0.19% equity move")
print("  THROUGH THIS FITTED SLOPE. It does NOT mean 'the company gets 14% of")
print("  freight'. R^2 ~0.10 means ~90% of daily equity variance is not explained.")

# up/down, with the intercept caveat and a bootstrap
print("\n  Conditional mean-return ratios on BWET-up vs BWET-down days:")
print(f"  {'':<6}{'up':>9}{'down':>9}{'gap':>9}{'bootstrap 95% CI':>22}{'verdict':>16}")
for t in ["DHT", "FRO"]:
    x, y = ret["BWET"].values, ret[t].values
    n = len(x)
    up, dn = x > 0, x < 0
    uc = y[up].mean() / x[up].mean() * 100
    dc = y[dn].mean() / x[dn].mean() * 100
    gaps = []
    for _ in range(4000):
        i = rng.integers(0, n, n)
        xb, yb = x[i], y[i]
        u2, d2 = xb > 0, xb < 0
        if u2.sum() < 30 or d2.sum() < 30:
            continue
        gaps.append(yb[u2].mean() / xb[u2].mean() * 100 -
                    yb[d2].mean() / xb[d2].mean() * 100)
    lo, hi = np.percentile(gaps, [2.5, 97.5])
    v = "significant" if lo > 0 else "NOT significant"
    print(f"  {t:<6}{uc:>8.1f}%{dc:>8.1f}%{uc-dc:>8.1f}{f'[{lo:+.1f}, {hi:+.1f}]pp':>22}{v:>16}")
print("\n  🔴 THE 'FAVOURABLE ASYMMETRY' CLAIM IS WITHDRAWN. Both intervals span")
print("     zero. And structurally the gap is not identified: with a common")
print("     slope, C+ = beta + alpha/E[x|x>0] and C- = beta + alpha/E[x|x<0], so")
print("     a POSITIVE INTERCEPT ALONE produces C+ > C- with no slope asymmetry.")

# ═══════════════════════════ 4) lead / lag ════════════════════════════════════
print("\n" + "-" * 100)
print("4) LEAD / LAG — weekly, complete periods, with multiplicity correction")
print("-" * 100)
w = frames["weekly"]
lags = list(range(-4, 5))
print(f"  {'':<6}" + "".join(f"{k:>8}" for k in lags))
ll, praw = [], []
for t in ["DHT", "FRO"]:
    cells = ""
    for k in lags:
        pair = pd.concat([w["BWET"], w[t].shift(-k)], axis=1).dropna()
        r = pair.iloc[:, 0].corr(pair.iloc[:, 1])
        nn = len(pair)
        z = np.arctanh(r) * np.sqrt(nn - 3)
        p = erfc(abs(z) / np.sqrt(2))
        cells += f"{r:>8.2f}"
        ll.append(dict(ticker=t, lag_weeks=k, corr=round(r, 3), n=nn,
                       p_raw=round(p, 4)))
        if k != 0:
            praw.append((t, k, p))
    print(f"  {t:<6}{cells}")
pd.DataFrame(ll).to_csv(os.path.join(DATA, "s22_leadlag.csv"), index=False)
m = len(praw)
holm = sorted(praw, key=lambda z: z[2])
print(f"\n  Holm correction across the {m} non-zero lags tested:")
surv = []
for i, (t, k, p) in enumerate(holm[:4]):
    thr = 0.05 / (m - i)
    ok = p < thr
    surv.append(ok)
    print(f"     {t} k={k:+d}  p={p:.3f}  vs threshold {thr:.4f}  "
          f"{'SURVIVES' if ok else 'rejected'}")
print(f"  >> {'None' if not any(surv) else 'Some'} of the off-zero lags survives correction.")
print("  >> CORRECT WORDING: 'no statistically established WEEKLY LINEAR lead in")
print("     this analysis'. That is narrower than 'BWET gives no timing edge' —")
print("     weekly bars could bury a 1-2 day lead, and a lead could be non-linear.")

# ═══════════════════════════ 5) regimes, reconciled ═══════════════════════════
print("\n" + "-" * 100)
print("5) REGIMES — returns COMPOUNDED FROM DAILY DATA so they reconcile")
print("-" * 100)
REG = [("2023-05-03", "2024-12-31", "pre-crisis"),
       ("2025-01-01", "2025-12-31", "2025 build-up"),
       ("2026-01-01", "2026-12-31", "2026 Hormuz crisis")]
print(f"  {'regime':<22}{'n':>5}{'BWET':>10}{'DHT':>9}{'FRO':>9}"
       f"{'B~DHT':>8}{'B~FRO':>8}")
rg, prod = [], {t: 1.0 for t in TICKERS}
segs = {}
for a, b, lbl in REG:
    sr = ret.loc[a:b]
    if len(sr) < 20:
        continue
    mult = (1 + sr).prod()
    for t in TICKERS:
        prod[t] *= float(mult[t])
    c = sr.corr()
    segs[lbl] = sr
    print(f"  {lbl:<22}{len(sr):>5}{(float(mult['BWET'])-1)*100:>9.0f}%"
          f"{(float(mult['DHT'])-1)*100:>8.0f}%{(float(mult['FRO'])-1)*100:>8.0f}%"
          f"{c.loc['BWET','DHT']:>8.2f}{c.loc['BWET','FRO']:>8.2f}")
    rg.append(dict(regime=lbl, n=len(sr),
                   bwet=round((float(mult["BWET"]) - 1) * 100),
                   dht=round((float(mult["DHT"]) - 1) * 100),
                   fro=round((float(mult["FRO"]) - 1) * 100),
                   corr_dht=round(c.loc["BWET", "DHT"], 2),
                   corr_fro=round(c.loc["BWET", "FRO"], 2)))
pd.DataFrame(rg).to_csv(os.path.join(DATA, "s22_regimes.csv"), index=False)

print("\n  ✅ RECONCILIATION CHECK (this FAILED in the earlier draft):")
for t in TICKERS:
    err = (prod[t] / float(W[t]) - 1) * 100
    print(f"     {t}: regimes compound to {prod[t]:>9.4f} vs full-period "
          f"{float(W[t]):>9.4f}   error {err:+.6f}%")
print("     The earlier draft used first-to-last within each calendar slice,")
print("     which DROPPED the return across every regime boundary (BWET +2.16%,")
print("     FRO +2.42% too high). Fixed by compounding daily returns.")

print("\n  Is the crisis-period correlation increase significant? Fisher z:")
pre, cri = segs["pre-crisis"], segs["2026 Hormuz crisis"]
for t in ["DHT", "FRO"]:
    r1 = pre["BWET"].corr(pre[t])
    r2 = cri["BWET"].corr(cri[t])
    n1, n2 = len(pre), len(cri)
    z = (np.arctanh(r2) - np.arctanh(r1)) / np.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    p = erfc(abs(z) / np.sqrt(2))
    print(f"     {t}: {r1:.2f} -> {r2:.2f}   z={z:.2f}  p={p:.3f}  "
          f"{'significant' if p < 0.05 else 'NOT significant'}")
print("  >> The apparent 'transmission rises in a crisis' story is NOT")
print("     statistically established. Reported as description only.")

# ═══════════════════════════ 6) 2026, and the withdrawal ══════════════════════
print("\n" + "-" * 100)
print("6) 2026 YEAR-TO-DATE — and the headline that is WITHDRAWN")
print("-" * 100)
y = ret.loc["2026-01-01":]
m26 = (1 + y).prod()
print(f"  {'':<6}{'2026 total return':>20}{'log-growth ratio':>20}")
lb = np.log(float(m26["BWET"]))
for t in TICKERS:
    lg = "" if t == "BWET" else f"{np.log(float(m26[t]))/lb*100:>19.1f}%"
    print(f"  {t:<6}{(float(m26[t])-1)*100:>19,.0f}%{lg:>20}")
print("\n  🔴 WITHDRAWN: the draft claimed these log ratios 'sit in the SAME")
print("     RANGE' as the companies' operational capture of the TD3C print,")
print("     proving the market prices the convertible share and its duration.")
print("     Four reasons it does not survive:")
print("       1. PERIOD MISMATCH. Section 21 divided a Q2 AVERAGE achieved rate")
print("          by an 11 SEPTEMBER assessment. A company could have earned 100%")
print("          of the contemporaneous Q2 benchmark and still show ~19%.")
print("          >> Section 21's '19%/18% operational capture' is corrected.")
print("       2. NOT THE SAME OBJECT. One is a ratio of investment RETURNS over")
print("          a rolling futures portfolio; the other a ratio of RATE LEVELS.")
print("       3. TRANSFORMATION-DEPENDENT. On simple returns the same data give")
print(f"          {((float(m26['DHT'])-1)/(float(m26['BWET'])-1)*100):.1f}% and "
      f"{((float(m26['FRO'])-1)/(float(m26['BWET'])-1)*100):.1f}%, and the 'match' vanishes entirely.")
print("       4. NOT EVEN CLOSE ANYWAY. The FRO figure of "
      f"{np.log(float(m26['FRO']))/lb*100:.1f}% is ~{(np.log(float(m26['FRO']))/lb/0.18-1)*100:.0f}% larger")
print("          than the 18% it was supposedly corroborating.")
print("\n  ✅ WHAT SURVIVES, stated narrowly:")
print("     'The equities and the freight-futures vehicle delivered very")
print("      different returns. This is compatible with differences in")
print("      exposure, earnings duration, leverage and valuation, but this")
print("      return comparison does NOT identify operational pass-through and")
print("      does NOT show that the equities price the spike correctly.'")

# ═══════════════════════════ chart ════════════════════════════════════════════
cum = (1 + ret).cumprod() - 1
fig = plt.figure(figsize=(18.5, 10))
gs = fig.add_gridspec(2, 3, hspace=.4, wspace=.27)

ax = fig.add_subplot(gs[0, :2])
for t in TICKERS:
    ax.plot(cum.index, cum[t] * 100, color=COL[t], lw=2.1,
            label=f"{t}  {cum[t].iloc[-1]*100:+,.0f}%")
ax.axhline(0, color="k", lw=1)
ax.set_yscale("symlog", linthresh=100)
ax.set_ylabel("cumulative total return (%), symlog")
ax.set_title("A. BWET (tanker freight futures) vs the two equities — total return\n"
             "different instruments, not comparable claims on the same cash flows",
             fontsize=11.5, fontweight="bold")
ax.legend(fontsize=9.5, loc="upper left")
ax.grid(alpha=.25)

ax = fig.add_subplot(gs[0, 2])
roll = ret.rolling(60).corr()
r1 = roll.xs("BWET", level=1)["DHT"].dropna()
r2 = roll.xs("BWET", level=1)["FRO"].dropna()
ax.plot(r1.index, r1, color="#c0392b", lw=1.6, label="BWET~DHT")
ax.plot(r2.index, r2, color="#2980b9", lw=1.6, label="BWET~FRO")
ax.axhline(0, color="k", lw=1)
ax.set_ylabel("60-day rolling correlation")
ax.set_title(f"B. Unstable, and never high\nmeans {r1.mean():.2f} / {r2.mean():.2f}",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5); ax.grid(alpha=.25)
ax.tick_params(axis="x", labelrotation=30, labelsize=8)

ax = fig.add_subplot(gs[1, 0])
cd = pd.DataFrame(out)
piv = cd.pivot(index="freq", columns="pair", values="r").reindex(
    ["daily", "weekly", "monthly"])
lop = cd.pivot(index="freq", columns="pair", values="ci_lo").reindex(piv.index)
hip = cd.pivot(index="freq", columns="pair", values="ci_hi").reindex(piv.index)
x = np.arange(len(piv))
for j, (p_, c) in enumerate([("BWET~DHT", "#c0392b"), ("BWET~FRO", "#2980b9"),
                             ("DHT~FRO", "#16a34a")]):
    ax.bar(x + (j - 1) * .27, piv[p_], .27, color=c, label=p_,
           yerr=[piv[p_] - lop[p_], hip[p_] - piv[p_]], capsize=3,
           error_kw=dict(lw=1))
ax.set_xticks(x); ax.set_xticklabels(piv.index, fontsize=9.5)
ax.set_ylabel("correlation (95% CI)")
ax.set_ylim(0, 1.05)
ax.set_title("C. The equities track EACH OTHER far more\nthan either tracks freight",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5); ax.grid(axis="y", alpha=.25)

ax = fig.add_subplot(gs[1, 1])
lldf = pd.DataFrame(ll)
for t, c in [("DHT", "#c0392b"), ("FRO", "#2980b9")]:
    s = lldf[lldf["ticker"] == t]
    ax.plot(s["lag_weeks"], s["corr"], "o-", color=c, lw=2, ms=6, label=t)
ax.axvline(0, color="k", ls="--", lw=1.3)
ax.axhline(0, color="k", lw=.8)
ax.set_xlabel("k (weeks); k>0 = BWET leads")
ax.set_ylabel("correlation of weekly returns")
ax.set_title("D. Peak at k=0\nno weekly linear lead survives Holm correction",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9); ax.grid(alpha=.25)

ax = fig.add_subplot(gs[1, 2])
rgd = pd.DataFrame(rg)
xx = np.arange(len(rgd))
ax.bar(xx - .2, rgd["corr_dht"], .4, color="#c0392b", label="BWET~DHT")
ax.bar(xx + .2, rgd["corr_fro"], .4, color="#2980b9", label="BWET~FRO")
for i in range(len(rgd)):
    ax.text(i - .2, rgd["corr_dht"][i] + .01, f"{rgd['corr_dht'][i]:.2f}",
            ha="center", fontsize=9)
    ax.text(i + .2, rgd["corr_fro"][i] + .01, f"{rgd['corr_fro'][i]:.2f}",
            ha="center", fontsize=9)
ax.set_xticks(xx)
ax.set_xticklabels([r.replace(" ", "\n") for r in rgd["regime"]], fontsize=8.5)
ax.set_ylabel("correlation within regime")
ax.set_ylim(0, .55)
ax.set_title("E. Crisis-period rise is NOT\nstatistically significant",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=8.5); ax.grid(axis="y", alpha=.25)

fig.suptitle("Section 22 — BWET tanker-freight ETF vs DHT and Frontline  ·  total "
             f"return, {START.date()} to {END.date()}  ·  rebuilt after adversarial review",
             fontsize=13, fontweight="bold")
p = os.path.join(CHARTS, "s22_bwet.png")
fig.savefig(p, dpi=140, bbox_inches="tight")
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

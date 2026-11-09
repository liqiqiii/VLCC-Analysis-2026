"""Mitsui Fudosan (8801.T) distressed-turnaround case: reproducible numbers for reports #53/#54.

Inputs (mitsui_turnaround/data/, sources in sources.csv):
- mf8801_yearly_kabutan.csv : yearly OHLC, split-adjusted for the 2024 3:1 split (Kabutan)
- jrei_land_index_march.csv : JREI urban land price index, end-March, 2000=100 (Statistical Yearbook 20-13)
- miki_tokyo5_office_yearend.csv : Tokyo central-5-ward office vacancy and rent, year-end (Miki Shoji)
- mf_financials_fy1991_2008.csv : consolidated figures from Mitsui Fudosan annual reports 2000/2001/2002/2003/2008
- mf_later_ni_bps.csv : later net income / split-adjusted BPS (IRBANK, zaimdoc)
- japan_cpi_fred.csv : Japan CPI, annual average (OECD via FRED)
Outputs are author's arithmetic [E]. Prices are nominal and price-only (no dividends) unless stated.
Run: python mitsui_turnaround/run_mitsui.py
"""
import math
import os
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
D = os.path.join(os.path.dirname(__file__), "data")
SPLIT = 3.0  # 2024 3:1 split; Kabutan prices are adjusted, report EPS/BPS before 2024 are not

px = pd.read_csv(os.path.join(D, "mf8801_yearly_kabutan.csv")).set_index("year")
land = pd.read_csv(os.path.join(D, "jrei_land_index_march.csv")).set_index("year_end_march")
off = pd.read_csv(os.path.join(D, "miki_tokyo5_office_yearend.csv")).set_index("year")
fin = pd.read_csv(os.path.join(D, "mf_financials_fy1991_2008.csv")).set_index("fy_end_march")
later = pd.read_csv(os.path.join(D, "mf_later_ni_bps.csv")).set_index("fy_end_march")
cpi = pd.read_csv(os.path.join(D, "japan_cpi_fred.csv"))
cpi["year"] = pd.to_datetime(cpi["observation_date"]).dt.year
cpi = pd.to_numeric(cpi.set_index("year")["JPNCPIALLMINMEI"], errors="coerce").dropna()


def real(v, year, base=None):
    base = base or int(cpi.index.max())
    return v * cpi[base] / cpi[year]


def section(t):
    print(f"\n=== {t} ===")


def cycle_anatomy():
    section("A. Cycle anatomy (nominal; real = deflated to 2020 yen by Japan CPI (last complete FRED year))")
    lc = land["six_city_commercial"]
    print(f"6-city commercial land: 1985 {lc[1985]:.1f} -> peak {lc.max():.1f} (Mar-{lc.idxmax()}) = {lc.max()/lc[1985]:.2f}x; "
          f"-> trough {lc.loc[1992:2007].min():.1f} (Mar-{lc.loc[1992:2007].idxmin()}) = {lc.loc[1992:2007].min()/lc.max()-1:+.1%}")
    t2 = lc.loc[1992:2007].idxmin()
    print(f"  cycle 2: trough {lc[t2]:.1f} -> {lc.loc[2006:2010].max():.1f} (Mar-{lc.loc[2006:2010].idxmax()}) = "
          f"{lc.loc[2006:2010].max()/lc[t2]-1:+.1%}; -> {lc.loc[2009:2015].min():.1f} (Mar-{lc.loc[2009:2015].idxmin()}) = "
          f"{lc.loc[2009:2015].min()/lc.loc[2006:2010].max()-1:+.1%}")
    h, l = px["high"], px["low"]
    pk1, tr1 = h.loc[1985:1995].idxmax(), l.loc[1990:2004].idxmin()
    pk2, tr2 = h.loc[2004:2012].idxmax(), l.loc[2008:2012].idxmin()
    print(f"8801 stock: 1985 close {px.loc[1985,'close']} -> {pk1} high {h[pk1]} ({h[pk1]/px.loc[1985,'close']:.1f}x) -> "
          f"{tr1} low {l[tr1]} ({l[tr1]/h[pk1]-1:+.1%}, {tr1-pk1} yrs)")
    print(f"  real (2020 yen): {pk1} high {real(h[pk1],pk1):.0f} -> {tr1} low {real(l[tr1],tr1):.0f} ({real(l[tr1],tr1)/real(h[pk1],pk1)-1:+.1%})")
    print(f"  cycle 2: {tr1} low {l[tr1]} -> {pk2} high {h[pk2]} ({h[pk2]/l[tr1]:.2f}x, {pk2-tr1} yrs) -> "
          f"{tr2} low {l[tr2]} ({l[tr2]/h[pk2]-1:+.1%})")
    print(f"  {pk2} high vs {pk1} high: nominal {h[pk2]/h[pk1]-1:+.1%}, real {real(h[pk2],pk2)/real(h[pk1],pk1)-1:+.1%}")
    v, r = off["vacancy_pct"], off["avg_rent_yen_tsubo"]
    print(f"Tokyo 5-ward office: vacancy {v[1990]}% (1990) -> {v.loc[1990:1996].max()}% ({v.loc[1990:1996].idxmax()}) -> "
          f"{v.loc[2000:2005].max()}% ({v.loc[2000:2005].idxmax()}) -> {v.loc[2005:2008].min()}% ({v.loc[2005:2008].idxmin()}) -> "
          f"{v.loc[2009:2013].max()}% ({v.loc[2009:2013].idxmax()}) -> {v.loc[2014:2024].min()}% ({v.loc[2014:2024].idxmin()}) -> {v[2024]}% (2024)")
    print(f"  rent: {r[1991]:,} (1991 peak) -> {r.loc[1992:2006].min():,} ({r.loc[1992:2006].idxmin()}, "
          f"{r.loc[1992:2006].min()/r[1991]-1:+.1%}) -> {r.loc[2005:2009].max():,} ({r.loc[2005:2009].idxmax()}, "
          f"{r.loc[2005:2009].max()/r.loc[1992:2006].min()-1:+.1%}) -> {r.loc[2009:2014].min():,} ({r.loc[2009:2014].idxmin()}) -> "
          f"{r.loc[2015:2024].max():,} ({r.loc[2015:2024].idxmax()}) -> {r[2024]:,} (2024)")
    print("Stock vs land turning points: stock peak Dec-1989 (year high 1989) vs land peak Mar-1991 (index; JREI semiannual "
          "peak Sep-1990) -> stock led ~1 yr; stock trough 2003 vs land trough Mar-2005 -> ~2 yrs;")
    print("  stock peak 2007 vs land Mar-2008 -> ~1 yr; stock trough 2009 vs land 2012 -> ~3 yrs; vs rent trough 2004/2013 -> 1 yr / 4 yrs")


def correlations():
    section("B. Correlation and lead/lag (annual)")
    s = np.log(px["close"])  # Dec close of year Y
    lc = np.log(land["six_city_commercial"])  # end-March of year Y; align Dec Y with Mar Y+1 as lag 0
    ds, dl = s.diff(), lc.diff()

    def corr_lag(a, b, k, lo, hi):
        x = [a.get(y) for y in range(lo, hi + 1)]
        y = [b.get(y + 1 + k) for y in range(lo, hi + 1)]
        m = [(p, q) for p, q in zip(x, y) if p is not None and q is not None and not (math.isnan(p) or math.isnan(q))]
        if len(m) < 6:
            return float("nan"), len(m)
        p, q = zip(*m)
        return float(np.corrcoef(p, q)[0, 1]), len(m)

    def ci(r, n):  # naive Fisher-z 95% interval, assumes independent observations (they are not)
        if n < 5 or abs(r) >= 1:
            return float("nan"), float("nan")
        z, se = math.atanh(r), 1 / math.sqrt(n - 3)
        return math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)

    print("Lag k pairs the December close of year Y with end-March land of year Y+1+k: k=0 -> 3 months later, "
          "k=+1 -> 15 months, k=+2 -> 27 months")
    for label, lo, hi in [("full 1981-2014", 1981, 2014), ("cycle 1: 1985-2004", 1985, 2004), ("cycle 2: 2004-2014", 2004, 2014)]:
        lv = corr_lag(s, lc, 0, lo, hi)
        print(f"{label}: log-level R^2 (Dec close vs land 3 months later) = {lv[0]**2:.2f} (n={lv[1]})")
        row = []
        for k in (-2, -1, 0, 1, 2, 3):
            c, n = corr_lag(ds, dl, k, lo, hi)
            a, b = ci(c, n)
            row.append(f"k={k:+d}: {c:+.2f} (n={n}, 95% CI {a:+.2f}..{b:+.2f})")
        print("   yoy-change corr:\n     " + "\n     ".join(row))
    r = np.log(off["avg_rent_yen_tsubo"]); dr = r.diff()
    for label, lo, hi in [("rent 1991-2024", 1991, 2024), ("rent 2004-2013", 2004, 2013), ("rent 2013-2024", 2013, 2024)]:
        row = []
        for k in (-1, 0, 1, 2):
            x = [ds.get(y) for y in range(lo, hi + 1)]
            y = [dr.get(y + k) for y in range(lo, hi + 1)]
            m = [(p, q) for p, q in zip(x, y) if p is not None and q is not None and not (math.isnan(p) or math.isnan(q))]
            p, q = zip(*m)
            row.append(f"k={k:+d}: {np.corrcoef(p, q)[0,1]:+.2f} (n={len(m)})")
        print(f"{label}: stock yoy vs Dec rent yoy k yrs later: " + "; ".join(row))


def valuation_path():
    section("C. P/B and P/E path")
    # BPS: published 'net assets per share' FY2002-FY2008; FY1997-FY2001 = equity / shares issued (treasury negligible);
    # FY1991-FY1996 approximate (shares implied by NI/EPS; marked '~'). All divided by 3 for the 2024 split.
    bps = {}
    for y in fin.index:
        r = fin.loc[y]
        if not pd.isna(r["bps_published_raw"]):
            bps[y] = (r["bps_published_raw"] / SPLIT, "pub")
        elif not pd.isna(r["shares_issued_m"]):
            bps[y] = (r["equity_m"] / r["shares_issued_m"] / SPLIT, "eq/sh")
        else:
            bps[y] = (r["equity_m"] / (r["net_income_m"] / r["eps_raw"]) / SPLIT, "~approx")
    eps = fin["eps_raw"] / SPLIT
    print("RETROSPECTIVE annual table: uses the FY ending March of the same calendar year, i.e. for prices in Jan-May the")
    print("balance sheet was not yet published (look-ahead of up to ~2 months).")
    print(" year | low    high   | BPS (basis)     EPS   | P/B low-high | P/E low-high | equity ratio")
    for y in range(1991, 2009):
        lo, hi = px.loc[y, "low"], px.loc[y, "high"]
        b, basis = bps[y]
        pe = f"{lo/eps[y]:5.1f}-{hi/eps[y]:5.1f}" if eps[y] > 0 else "  loss      "
        eq = fin.loc[y, "equity_m"] / fin.loc[y, "total_assets_m"]
        print(f" {y} | {lo:6.1f} {hi:6.1f} | {b:5.1f} ({basis:7s}) {eps[y]:5.1f} | {lo/b:4.2f}-{hi/b:4.2f}    | {pe} | {eq:.1%}")
    for y in (2010, 2011, 2012, 2013, 2026):
        b = later.loc[y, "bps_adj"]
        print(f" {y} | {px.loc[y,'low']:6.1f} {px.loc[y,'high']:6.1f} | {b:5.1f} (IRBANK)        | "
              f"{px.loc[y,'low']/b:4.2f}-{px.loc[y,'high']/b:4.2f}")
    print("POINT-IN-TIME at turning points (latest BPS/EPS already published on that date):")
    pit = [("2003 low (11-Apr-2003)", px.loc[2003, "low"], 2002), ("2007 high (4-Jun-2007; FY2007 published May-2007)", px.loc[2007, "high"], 2007),
           ("2008 low (Oct-2008)", px.loc[2008, "low"], 2008), ("2009 low (Mar-2009)", px.loc[2009, "low"], 2008)]
    for label, p, fy in pit:
        b = fin.loc[fy, "bps_published_raw"] / SPLIT
        e = fin.loc[fy, "eps_raw"] / SPLIT
        print(f"  {label:50s} price {p:7.1f} | BPS FY{fy} {b:6.1f} -> P/B {p/b:4.2f} | EPS FY{fy} {e:5.1f} -> P/E {p/e:5.1f}")
    reserve02, reserve03 = 156405, 162289
    print(f"Land revaluation: Mar-2002 reserve ¥{reserve02/1e3:.1f}bn (+¥10.4bn retained earnings) = ¥166.8bn uplift; "
          f"Mar-2003 reserve ¥{reserve03/1e3:.1f}bn = {reserve03/fin.loc[2003,'equity_m']:.1%} of equity -> P/B before/after "
          "2002 is on different bases, and the revalued book is an accounting uplift, not proven recoverability")


def losses_and_balance_sheet():
    section("D. Loss recognition and balance sheet")
    loss = fin.loc[1997:2000, "net_income_m"].sum()
    print(f"FY1997-FY2000 consolidated net losses: ¥{loss/1e3:,.1f}bn over 4 years")
    print(f"Equity: Mar-1995 ¥{fin.loc[1995,'equity_m']/1e3:,.0f}bn -> Mar-2000 ¥{fin.loc[2000,'equity_m']/1e3:,.0f}bn "
          f"({fin.loc[2000,'equity_m']/fin.loc[1995,'equity_m']-1:+.0%}); equity ratio "
          f"{fin.loc[1995,'equity_m']/fin.loc[1995,'total_assets_m']:.1%} -> {fin.loc[2000,'equity_m']/fin.loc[2000,'total_assets_m']:.1%}")
    print(f"Total assets: Mar-1993 ¥{fin.loc[1993,'total_assets_m']/1e3:,.0f}bn (peak) -> Mar-2001 ¥{fin.loc[2001,'total_assets_m']/1e3:,.0f}bn "
          f"({fin.loc[2001,'total_assets_m']/fin.loc[1993,'total_assets_m']-1:+.0%})")
    print(f"Net income: FY2004 ¥{fin.loc[2004,'net_income_m']/1e3:.1f}bn -> FY2008 ¥{fin.loc[2008,'net_income_m']/1e3:.1f}bn "
          f"({fin.loc[2008,'net_income_m']/fin.loc[2004,'net_income_m']:.1f}x); EPS {fin.loc[2004,'eps_raw']} -> {fin.loc[2008,'eps_raw']} "
          f"({fin.loc[2008,'eps_raw']/fin.loc[2004,'eps_raw']:.1f}x)")
    oi04, oi08 = fin.loc[2004, "operating_income_bn"], fin.loc[2008, "operating_income_bn"]
    rv04, rv08 = fin.loc[2004, "revenue_m"] / 1e3, fin.loc[2008, "revenue_m"] / 1e3
    print(f"Bridge FY2004 -> FY2008: revenue ¥{rv04:,.0f}bn -> ¥{rv08:,.0f}bn ({rv08/rv04-1:+.0%}); operating income "
          f"¥{oi04}bn -> ¥{oi08}bn ({oi08/oi04-1:+.0%}); net income ¥{fin.loc[2004,'net_income_m']/1e3:.1f}bn -> "
          f"¥{fin.loc[2008,'net_income_m']/1e3:.1f}bn ({fin.loc[2008,'net_income_m']/fin.loc[2004,'net_income_m']:.1f}x)")
    ni04, ni08 = fin.loc[2004, "net_income_m"] / 1e3, fin.loc[2008, "net_income_m"] / 1e3
    print(f"  additive bridge (¥bn): net income +{ni08-ni04:.1f} = operating income +{oi08-oi04:.1f} "
          f"+ below-operating items {(ni08-oi08)-(ni04-oi04):+.1f} -> the 6x is mainly a low-base effect")
    print(f"FY2009 net income ¥83.6bn ({835.72/873.78-1:+.0%} vs FY2008) while the stock fell "
          f"{px.loc[2009,'low']/px.loc[2007,'high']-1:+.0%} (2007 high -> 2009 low): the 2008 crash was multiple compression")
    print(f"Dividend per share: FY1991 ¥{fin.loc[1991,'dps_raw']} -> FY1998-2000 ¥5.0 -> FY2008 ¥20.0 (pre-split)")
    print("FY2006 share count 823.4m -> 881.4m: mainly convertible-bond conversion (55.9m shares, non-cash) [AR2008 per review]")
    site_m2, land_bn, share, project_bn = 78393.6, 180.0, 0.40, 370.0  # M10 (area), M21 (price, share, cost)
    tsubo = site_m2 / 3.30579
    eq01 = fin.loc[2001, "equity_m"] / 1e3  # latest equity before the Sep-2001 decision
    print(f"Defense Agency site: ¥{land_bn:.0f}bn / {tsubo:,.0f} tsubo = ¥{land_bn*1e9/tsubo/1e4:,.0f} man/tsubo; "
          f"Mitsui 40% project share; IF costs split pro rata [E]: ¥{land_bn*share:.0f}bn land "
          f"({land_bn*share/eq01:.1%} of Mar-2001 equity), ¥{project_bn*share:.0f}bn of project cost ({project_bn*share/eq01:.1%})")


def buy_paths():
    section("E. Entry-point outcomes (price only, nominal; years to 2007 high and to the 6-Nov-2026 close)")
    end07, end26 = px.loc[2007, "high"], px.loc[2026, "close"]
    for label, y, col in [("1989 high", 1989, "high"), ("1990 low", 1990, "low"), ("1992 low", 1992, "low"),
                          ("1995 low", 1995, "low"), ("1998 low", 1998, "low"), ("2003 low", 2003, "low"),
                          ("2005 open", 2005, "open"), ("2007 high", 2007, "high"), ("2009 low", 2009, "low"),
                          ("2012 low", 2012, "low")]:
        p = px.loc[y, col]
        a = f"{end07/p:5.2f}x to 2007 high" if y < 2007 else " " * 20
        yrs = 2026.85 - (y + 0.5)
        cagr = (end26 / p) ** (1 / yrs) - 1
        print(f"  {label:10s} {p:7.1f}: {a} | {end26/p:5.2f}x to Nov-2026 ({cagr:+.1%}/yr price-only, ~{yrs:.0f} yrs)")


def peers():
    section("F. Peer check 2003-2009 (Yahoo daily closes, price only)")
    try:
        import yfinance as yf
        for t in ("8801.T", "8802.T", "^N225"):
            h = yf.Ticker(t).history(start="2003-01-01", end="2010-01-01", auto_adjust=False)["Close"]
            a = h.loc["2003"].min(); b = h.loc["2006":"2007"].max(); c = h.loc["2008":"2009"].min()
            print(f"  {t:7s} 2003 low {a:8.1f} -> 2006-07 high {b:8.1f} ({b/a:.2f}x) -> 2008-09 low {c:8.1f} ({c/b-1:+.0%})")
    except Exception as e:
        print("  yfinance unavailable:", e)


if __name__ == "__main__":
    cycle_anatomy()
    correlations()
    valuation_path()
    losses_and_balance_sheet()
    buy_paths()
    peers()

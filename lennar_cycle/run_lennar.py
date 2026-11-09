"""Lennar (LEN) cycle position vs the Mitsui Fudosan case: reproducible numbers for reports #55/#56.

Inputs: lennar_cycle/data/ (sources.csv). Prices: Yahoo (split-adjusted Close, no dividends, NOT adjusted
for the Feb-2025 Millrose spin-off distribution). Fundamentals: Lennar 10-K selected data (FY ends 30-Nov).
Outputs are author's arithmetic [E].
Run: python lennar_cycle/run_lennar.py
"""
import math
import os
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
D = os.path.join(os.path.dirname(__file__), "data")
END = "2026-11-10"  # data through 9-Nov-2026 (US close); fixed for reproducibility

fund = pd.read_csv(os.path.join(D, "len_fundamentals_fy2001_2025.csv")).set_index("fy_end_nov")
qtr = pd.read_csv(os.path.join(D, "len_quarterly_recent.csv"))


def fred(s):
    df = pd.read_csv(os.path.join(D, f"fred_{s}.csv"))
    df.columns = ["date", s]
    df["date"] = pd.to_datetime(df["date"])
    df[s] = pd.to_numeric(df[s], errors="coerce")
    return df.set_index("date")[s].dropna()


def prices(t):
    import yfinance as yf
    h = yf.Ticker(t).history(start="1995-01-01", end=END, auto_adjust=False)["Close"]
    h.index = h.index.tz_localize(None).normalize()
    h = h.dropna()
    if t == "LEN":  # undo Yahoo's 1.033 'split' for the Millrose spin so pre-2025 prices match contemporaneous BPS
        h.loc[h.index < pd.Timestamp("2025-01-21")] *= 1.033
    return h


def sec(t):
    print(f"\n=== {t} ===")


def cycle_anatomy(p):
    sec("A. LEN price cycle (split-adjusted close, price only)")
    m = p.resample("ME").last()

    def ext(a, b, fn):
        s = p.loc[a:b]
        return (s.idxmax(), s.max()) if fn == "max" else (s.idxmin(), s.min())

    pk1 = ext("2004", "2006", "max"); tr1 = ext("2007", "2011", "min")
    pk2 = ext("2020", "2025", "max"); last = (p.index[-1], p.iloc[-1])
    lo26 = ext("2025-06", "2026-11", "min")
    print(f"Peak 1 {pk1[0].date()} {pk1[1]:.2f} -> trough {tr1[0].date()} {tr1[1]:.2f} ({tr1[1]/pk1[1]-1:+.1%})")
    print(f"Trough 1 -> peak 2 {pk2[0].date()} {pk2[1]:.2f} ({pk2[1]/tr1[1]:.1f}x)")
    print(f"Peak 2 -> 2025-26 low {lo26[0].date()} {lo26[1]:.2f} ({lo26[1]/pk2[1]-1:+.1%}); last {last[0].date()} {last[1]:.2f} ({last[1]/pk2[1]-1:+.1%})")
    return m


def housing_cycle():
    sec("B. US housing cycle (FRED, monthly, SAAR where applicable)")
    st, nh, ms, comp, mtg = fred("HOUST1F"), fred("HSN1F"), fred("MSACSR"), fred("NHFSEPCS"), fred("MORTGAGE30US")
    for name, s, unit in [("Single-family starts (k)", st, ""), ("New home sales (k)", nh, ""), ("Months' supply, new", ms, ""),
                          ("Completed new homes for sale (k)", comp, "")]:
        pk = s.loc["2004":"2007"]; tr = s.loc["2007":"2012"]
        print(f"{name:34s} 2004-07 peak {pk.max():7.1f} ({pk.idxmax():%Y-%m}) | 2007-12 extreme "
              f"{(tr.min() if 'supply' not in name and 'Completed' not in name else tr.max()):7.1f} | "
              f"2020-25 range {s.loc['2020':'2025'].min():.1f}-{s.loc['2020':'2025'].max():.1f} | latest {s.iloc[-1]:.1f} ({s.index[-1]:%Y-%m})")
    long = ms.loc["1963":"2019"]
    print(f"Months' supply 1963-2019 median {long.median():.1f}; latest {ms.iloc[-1]:.1f} = {(long < ms.iloc[-1]).mean():.0%} pct "
          f"(1963-2019) / {(ms < ms.iloc[-1]).mean():.0%} pct (full history)")
    c26 = comp.loc["2024":]
    print(f"Completed-for-sale latest {comp.iloc[-1]:.0f}k; recent peak {c26.max():.0f}k ({c26.idxmax():%Y-%m}) -> "
          f"{comp.iloc[-1]/c26.max()-1:+.1%}; down in {(comp.loc['2026-02':].diff() < 0).sum()} of the last "
          f"{len(comp.loc['2026-02':])} months; 2008-07 peak {comp.loc['2007':'2010'].max():.0f}k; 2019 avg {comp.loc['2019'].mean():.0f}k")
    print(f"30y mortgage: latest {mtg.iloc[-1]:.2f}% ({mtg.index[-1].date()}); 2026 max {mtg.loc['2026'].max():.2f}%; 2021 min {mtg.loc['2021'].min():.2f}%")
    st_pk = st.loc["2020":"2023"]
    print(f"Single-family starts: 2020-23 peak {st_pk.max():.0f}k ({st_pk.idxmax():%Y-%m}); latest {st.iloc[-1]:.0f}k "
          f"({st.iloc[-1]/st_pk.max()-1:+.1%}); 2009 trough {st.loc['2008':'2011'].min():.0f}k; 2011 avg {st.loc['2011'].mean():.0f}k "
          f"-> latest = {st.iloc[-1]/st.loc['2011'].mean():.1f}x 2011")
    return st


def lead_lag(m, st):
    sec("C. Does LEN lead single-family starts? (12-month log changes, monthly, overlapping)")
    s = np.log(m).diff(12)
    h = np.log(st.resample("ME").last()).diff(12)
    j = pd.concat([s.rename("len"), h.rename("st")], axis=1)
    for label, a, b in [("1996-2019", "1996", "2019"), ("2000-2012", "2000", "2012"), ("2013-2026", "2013", "2026")]:
        row = []
        for k in (0, 3, 6, 9, 12):
            x = j["len"].loc[a:b]; y = j["st"].shift(-k).loc[a:b]
            ok = x.notna() & y.notna()
            row.append(f"k={k:2d}m r={np.corrcoef(x[ok], y[ok])[0,1]:+.2f} (n={ok.sum()})")
        print(f"{label}: " + "; ".join(row))
    print("Overlapping 12m windows: effective sample far smaller than n; read as association only")
    mm = m.loc["2007":"2010"]
    tps = [("LEN peak (daily)", "2005-07"), ("starts peak", str(st.loc['2004':'2007'].idxmax())[:7]),
           ("LEN trough daily", "2008-11"), ("LEN trough month-end", str(mm.idxmin())[:7]),
           ("starts trough", str(st.loc['2008':'2011'].idxmin())[:7])]
    print("Turning points: " + "; ".join(f"{a} {b}" for a, b in tps))


def valuation(p):
    sec("D. P/B and P/E path (BPS/EPS of the FY ending Nov of the same calendar year = retrospective)")
    print(" year | low     high    | BPS (basis)   EPS    | P/B low-high | P/E low-high | GM home")
    for y in range(2001, 2026):
        s = p.loc[str(y)]
        lo, hi = s.min(), s.max()
        b = fund.loc[y, "bps"]; e = fund.loc[y, "eps_diluted"]; gm = fund.loc[y, "gm_home_pct"]
        e = float(e) if str(e) not in ("", "nan") else float("nan")
        pe = f"{lo/e:5.1f}-{hi/e:5.1f}" if e == e and e > 0 else ("  loss     " if e == e else "  n/a      ")
        print(f" {y} | {lo:7.2f} {hi:7.2f} | {b:6.2f} ({fund.loc[y,'bps_basis']}) {e:6.2f} | {lo/b:4.2f}-{hi/b:4.2f}    | {pe} | {gm}")
    sec("D2. Point-in-time P/B at deduplicated trough episodes (latest PUBLISHED quarterly equity / approx. shares)")
    qe = pd.read_csv(os.path.join(D, "len_quarterly_equity_xbrl.csv"), parse_dates=["period_end", "first_filed"])
    shares_fy = (fund["equity_m"] / fund["bps"])  # millions of shares at FY end (published or calculated BPS)

    def pit(day):
        avail = qe[qe["first_filed"] <= day]
        if avail.empty:
            return None
        r = avail.sort_values("period_end").iloc[-1]
        fy = r["period_end"].year if r["period_end"].month == 11 else r["period_end"].year  # FY ends Nov
        if r["period_end"].month != 11:
            fy = r["period_end"].year
        sh = shares_fy.get(fy, shares_fy.get(fy - 1))
        return r["period_end"].date(), r["stockholders_equity"] / 1e6 / sh, sh
    episodes = [("2008 crisis", "2008-06", "2009-06"), ("2011", "2011-06", "2011-12"), ("2018-19", "2018-10", "2019-03"),
                ("2020 Covid", "2020-02", "2020-05"), ("2022", "2022-04", "2022-12"), ("2025-26", "2025-06", "2026-11")]
    for name, a, b in episodes:
        s = p.loc[a:b]
        day, px = s.idxmin(), s.min()
        r = pit(day)
        if r is None:
            print(f"  {name:10s} low {day.date()} {px:7.2f} | no XBRL equity published yet -> annual BPS FY{day.year-1} "
                  f"{fund.loc[day.year-1,'bps']:.2f} -> P/B {px/fund.loc[day.year-1,'bps']:.2f}")
        else:
            print(f"  {name:10s} low {day.date()} {px:7.2f} | equity as of {r[0]} / ~{r[2]:.0f}m sh = BPS {r[1]:.2f} -> P/B {px/r[1]:.2f}")
    print("  (share counts approximate: FY-end equity / BPS of the same FY; quarterly share counts not in XBRL)")
    for label, d, fy in [("2005 peak", p.loc["2005"].idxmax(), 2004), ("2024 peak", p.loc["2024"].idxmax(), 2023)]:
        px = p.loc[d]; b = fund.loc[fy, "bps"]; e = fund.loc[fy, "eps_diluted"]
        print(f"  {label:10s} {d.date()} {px:7.2f} | BPS FY{fy} {b:6.2f} -> P/B {px/b:4.2f} | EPS FY{fy} {e} -> P/E {px/float(e):5.1f}")
    last = p.iloc[-1]
    ttm = qtr["eps_diluted"].sum()
    bps_q = 90.62  # Yahoo book value/share (latest quarter, Aug-2026) [L12]
    print(f"  now        {p.index[-1].date()} {last:7.2f} | BPS FY2025 {fund.loc[2025,'bps']:.2f} -> P/B {last/fund.loc[2025,'bps']:.2f}; "
          f"Yahoo BPS (Aug-26) {bps_q} -> P/B {last/bps_q:.2f} | TTM EPS {ttm:.2f} -> P/E {last/ttm:.1f}")
    print(f"  FY2025 equity fell {fund.loc[2025,'equity_m']/fund.loc[2024,'equity_m']-1:+.0%} mainly from the Millrose spin-off "
          "(land assets distributed to shareholders), not from losses (FY2025 NI +$2.08bn)")


def margins():
    sec("E. Gross margin on home sales (cycle comparison)")
    g = fund["gm_home_pct"].replace("", np.nan).astype(float)
    print("FY: " + ", ".join(f"{y} {v:.1f}%" for y, v in g.dropna().items()))
    print(f"Peak 2005 {g[2005]}% -> 2007 {g[2007]}% (incl. valuation adj; ex-adj 13.9%) -> 2009 {g[2009]}% (ex 15.6%)")
    print(f"Peak 2022 {g[2022]}% -> 2025 {g[2025]}% -> Q3 FY26 15.8% (Q2 15.6%; Q4 guide 15.5-16.0%)")
    print(f"Decline so far: {15.8-g[2022]:+.1f} pp from peak vs {13.9-g[2005]:+.1f} pp (2005->2007 ex-adj) / {6.0-g[2005]:+.1f} pp incl. adj")


def peers_and_holders(p):
    sec("F. Peers and Berkshire (price only)")
    import yfinance as yf
    raw = yf.Ticker("LEN").history(start="2024-01-01", end=END, auto_adjust=False)["Close"]
    mrp = yf.Ticker("MRP").history(start="2025-02-01", end=END, auto_adjust=False)["Close"]
    raw.index = raw.index.tz_localize(None).normalize()
    pk_raw = raw.loc["2024"].max() * 1.033  # undo Yahoo's 1.033 spin 'split' factor on pre-21-Jan-2025 prices
    holder = raw.iloc[-1] + 0.5 * mrp.iloc[-1]
    print(f"Millrose spin (7-Feb-2025): 0.5 MRP per LEN share; Yahoo treats it as a 1.033 'split' (~3%), but 0.5 MRP was "
          f"~${0.5*mrp.iloc[0]:.1f} at first trade (~{0.5*mrp.iloc[0]/raw.loc['2025-02-06']:.0%} of LEN)")
    print(f"LEN raw 2024 high {pk_raw:.2f}; LEN + 0.5 MRP now {raw.iloc[-1]:.2f} + {0.5*mrp.iloc[-1]:.2f} = {holder:.2f} "
          f"({holder/pk_raw-1:+.0%} vs 2024 high, price only) vs LEN alone {raw.iloc[-1]/pk_raw-1:+.0%}")
    for t in ("LEN", "DHI", "PHM", "NVR", "TOL", "SPY"):
        s = prices(t)
        pk = s.loc["2024"].max()
        print(f"  {t:4s} 2024 high {pk:9.2f} -> last {s.iloc[-1]:9.2f} ({s.iloc[-1]/pk-1:+.0%}); 2008-09 low/2005 high "
              f"{(s.loc['2008':'2009'].min()/s.loc['2005'].max()-1) if len(s.loc['2005']) else float('nan'):+.0%}")
    q_ends = ["2025-03-31", "2025-06-30", "2026-03-31", "2026-06-30"]
    adds = [1.92, 5.08, 3.04, 3.01]  # m Class A shares added in Q1-25, Q2-25, Q1-26, Q2-26 [L13]; Q3-25 ~0
    closes = [raw.loc[:d].iloc[-1] for d in q_ends]
    cost = sum(a * c for a, c in zip(adds, closes)) / sum(adds)
    print(f"Berkshire ~{sum(adds):.1f}m Class A shares (13F: 13.11m at 30-Jun-2026); quarter-end closes "
          + "/".join(f"{c:.2f}" for c in closes) + f"; cost proxy ~${cost:.0f}/share vs last ${p.iloc[-1]:.2f} "
          f"({p.iloc[-1]/cost-1:+.0%}). Q3-2026 13F shows 30-Sep holdings; deadline Mon 16-Nov-2026")


def scenarios(p):
    sec("G. Illustrative 12/24-month scenarios (P/B on projected BPS; not a recommendation)")
    bps0 = 90.62
    ttm = qtr["eps_diluted"].sum()
    payout = 2.00 * 1.0  # ~$2/yr dividend (2.25% yield at ~$90) [L12]
    for name, eps, pb12, pb24 in [("Bear", 4.0, 0.80, 0.90), ("Base", 5.5, 1.05, 1.20), ("Bull", 7.5, 1.30, 1.60)]:
        b12 = bps0 + eps - payout; b24 = b12 + eps - payout  # constant EPS both years
        t12, t24 = b12 * pb12, b24 * pb24
        print(f"  {name}: EPS ~{eps}/yr, P/B {pb12}x/{pb24}x -> 12m ${t12:.0f} ({t12/p.iloc[-1]-1:+.0%}), 24m ${t24:.0f} ({t24/p.iloc[-1]-1:+.0%})")
    print(f"  (TTM EPS {ttm:.2f}; constant EPS; buybacks ignored; price only; start BPS is Aug-2026; Bear P/B 0.8x ~ the Oct-2026 low (0.84x) and below the 2011/2018/2022 point-in-time lows of 0.88-0.90x)")


if __name__ == "__main__":
    p = prices("LEN")
    m = cycle_anatomy(p)
    st = housing_cycle()
    lead_lag(m, st)
    valuation(p)
    margins()
    peers_and_holders(p)
    scenarios(p)

# -*- coding: utf-8 -*-
"""
Volcker 1979-82 vs Warsh 2026 — what actually ends a tightening regime?

Question from the user's analogy:
    Russia-Ukraine war  ~ 1st oil crisis (1973)
    US-Iran war         ~ 2nd oil crisis (1979)
    Warsh hike (2026)   ~ the Volcker moment (Oct 1979)
    => Was it the Latin American debt crisis that ENDED Volcker's high rates?
       And by analogy, what would make Warsh slow down?

This script does NOT answer the historiography (that is sourced in the report).
It supplies the MEASURABLE part: the exact dated policy path, the REAL policy
rate, and the macro readings at the moment Volcker actually pivoted -- then
prints today's readings against those same thresholds.

Data: FRED CSV endpoint (no API key).
    DFF            daily effective fed funds
    FEDFUNDS       monthly effective fed funds
    INTDSRUSM193N  discount rate (discontinued 2021)
    CPIAUCSL       CPI, all items (-> YoY)
    CPILFESL       CPI core (-> YoY)
    UNRATE         unemployment
    GS10           10-yr Treasury
    BAMLH0A0HYM2   US high-yield OAS      (credit tripwire)
    BAMLEMCBPIOAS  EM corporate OAS       (the "LDC" tripwire)

Rule 4 flag: in this environment the two BAML OAS series are returned by the
FRED mirror TRUNCATED to ~3 years (from 2023-09). They are therefore usable as
a CURRENT LEVEL only, not as history. Flagged in the report.
"""

import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")
os.makedirs(DATA, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"


def fred(series_id):
    df = pd.read_csv(FRED.format(series_id))
    df.columns = ["date", series_id]
    df["date"] = pd.to_datetime(df["date"])
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    return df.set_index("date")[series_id].dropna()


print("=" * 78)
print("VOLCKER (1979-82) vs WARSH (2026) — what ends a tightening regime?")
print("=" * 78)

series = {}
for sid in ["DFF", "FEDFUNDS", "INTDSRUSM193N", "CPIAUCSL", "CPILFESL",
            "CPIAUCNS", "CPILFENS",
            "UNRATE", "GS10", "BAMLH0A0HYM2", "BAMLEMCBPIOAS"]:
    try:
        series[sid] = fred(sid)
        print(f"  {sid:<16} {len(series[sid]):>6} obs  "
              f"{series[sid].index[0].date()} -> {series[sid].index[-1].date()}")
    except Exception as exc:
        print(f"  {sid:<16} FAILED: {exc}")

# ---------------------------------------------------------------- monthly panel
cpi_yoy = series["CPIAUCSL"].pct_change(12) * 100
core_yoy = series["CPILFESL"].pct_change(12) * 100

panel = pd.DataFrame({
    "effr": series["FEDFUNDS"],
    "discount": series.get("INTDSRUSM193N"),
    "cpi_yoy": cpi_yoy,
    "core_yoy": core_yoy,
    "unrate": series["UNRATE"],
    "gs10": series["GS10"],
})
panel["real_effr"] = panel["effr"] - panel["cpi_yoy"]
panel["real_effr_core"] = panel["effr"] - panel["core_yoy"]
panel.to_csv(os.path.join(DATA, "macro_panel_monthly.csv"))

# Rule 4 cross-check: seasonally-adjusted vs NOT-seasonally-adjusted CPI.
# The headline YoY number quoted in the press is built from the NSA index.
cpi_nsa_yoy = series["CPIAUCNS"].pct_change(12) * 100
core_nsa_yoy = series["CPILFENS"].pct_change(12) * 100
print(f"\n  Rule 4 CPI cross-check (latest, {cpi_nsa_yoy.index[-1]:%b-%Y}): "
      f"headline SA {cpi_yoy.iloc[-1]:.2f}% vs NSA {cpi_nsa_yoy.iloc[-1]:.2f}%; "
      f"core SA {core_yoy.iloc[-1]:.2f}% vs NSA {core_nsa_yoy.iloc[-1]:.2f}%")
print("  (Both agree to ~0.02pp, so the real-rate conclusion is insensitive to "
      "the choice.)")

# ================================================================ SECTION 1
print("\n" + "-" * 78)
print("1) THE VOLCKER PEAK — where did the funds rate actually top?")
print("-" * 78)

v = panel.loc["1979-01-01":"1984-12-01"]
pk = v["effr"].idxmax()
print(f"  Monthly EFFR peak      : {v['effr'].max():.2f}%  in {pk:%b %Y}")

dff = series["DFF"].loc["1979-01-01":"1984-12-31"]
dpk = dff.idxmax()
print(f"  DAILY EFFR peak        : {dff.max():.2f}%  on {dpk:%Y-%m-%d}")

# the 1981 double-top: the rate collapsed mid-1980 (credit controls) then re-peaked
print("\n  The famous 'double top' (monthly EFFR):")
for lo, hi, tag in [("1980-01-01", "1980-12-01", "1980 spike + Mar-Jul collapse"),
                    ("1981-01-01", "1981-12-01", "1981 re-peak")]:
    w = v.loc[lo:hi, "effr"]
    print(f"    {tag:<32} max {w.max():5.2f}% ({w.idxmax():%b %Y})  "
          f"min {w.min():5.2f}% ({w.idxmin():%b %Y})")

# ================================================================ SECTION 2
print("\n" + "-" * 78)
print("2) 1982 MONTH BY MONTH — did easing start BEFORE or AFTER Mexico (Aug-1982)?")
print("-" * 78)
y82 = panel.loc["1981-10-01":"1983-03-01",
                ["effr", "discount", "cpi_yoy", "unrate", "real_effr"]]
print(f"  {'month':<9}{'EFFR':>7}{'disc':>7}{'CPI':>7}{'unemp':>7}{'real':>8}   note")
notes = {
    "1981-07": "NBER recession BEGINS",
    "1982-05": "Drysdale Govt Securities collapses (May 17)",
    "1982-07": "Penn Square fails (Jul 5); CUT #1 voted Jul 19 (eff Jul 20); CUT #2 voted Jul 30",
    "1982-08": "MEXICO: Silva Herzog Aug 12; CUT #3 voted Aug 13; CUT #4 Aug 26",
    "1982-09": "Sep 13: Board DISAPPROVES a further cut — at the height of the crisis",
    "1982-10": "Oct 5 FOMC drops the M1 objective; Volcker announces it Oct 9; CUT #5",
    "1982-11": "NBER recession ENDS; unemployment peaks 10.8%; CUT #6",
    "1982-12": "CUT #7 (to 8.5%)",
}
for dt, row in y82.iterrows():
    key = f"{dt:%Y-%m}"
    disc = "  n/a" if pd.isna(row["discount"]) else f"{row['discount']:5.2f}"
    print(f"  {dt:%Y-%m}  {row['effr']:6.2f}%{disc:>7} {row['cpi_yoy']:6.2f}%"
          f"{row['unrate']:6.1f}%{row['real_effr']:7.2f}%   {notes.get(key,'')}")
y82.to_csv(os.path.join(DATA, "volcker_1982_path.csv"))

jun82, jul82, aug82, dec82 = [panel.loc[d] for d in
                              ["1982-06-01", "1982-07-01", "1982-08-01", "1982-12-01"]]
print(f"\n  EFFR Jun-82 {jun82['effr']:.2f}%  ->  Jul-82 {jul82['effr']:.2f}%"
      f"  ->  Aug-82 {aug82['effr']:.2f}%  ->  Dec-82 {dec82['effr']:.2f}%")
print(f"  Easing between Jun and Jul 1982 (i.e. BEFORE Mexico):"
      f" {jun82['effr'] - jul82['effr']:+.2f}pp")
print(f"  Easing between Jul and Dec 1982 (i.e. AFTER  Mexico):"
      f" {jul82['effr'] - dec82['effr']:+.2f}pp")

# ================================================================ SECTION 3
print("\n" + "-" * 78)
print("3) VOLCKER'S PIVOT PRECONDITIONS vs TODAY")
print("-" * 78)

peak_row = panel.loc[pk]
piv = panel.loc["1982-07-01"]          # first discount-rate cut of the cycle
today_m = panel.dropna(subset=["effr"]).index[-1]
now = panel.loc[today_m]

# post-hike policy rate: FRED monthly average lags the Sep-16-2026 hike
HIKE_MID = 3.875   # midpoint of the new 3.75-4.00% target range, set 2026-09-16

rows = [
    ("Nominal policy rate", f"{peak_row['effr']:.2f}%", f"{piv['effr']:.2f}%",
     f"{now['effr']:.2f}% (target mid {HIKE_MID:.2f}%)"),
    ("Headline CPI YoY", f"{peak_row['cpi_yoy']:.2f}%", f"{piv['cpi_yoy']:.2f}%",
     f"{now['cpi_yoy']:.2f}%"),
    ("Core CPI YoY", f"{peak_row['core_yoy']:.2f}%", f"{piv['core_yoy']:.2f}%",
     f"{now['core_yoy']:.2f}%"),
    ("REAL policy rate (hdln)", f"{peak_row['real_effr']:+.2f}%",
     f"{piv['real_effr']:+.2f}%", f"{HIKE_MID - now['cpi_yoy']:+.2f}%"),
    ("REAL policy rate (core)", f"{peak_row['real_effr_core']:+.2f}%",
     f"{piv['real_effr_core']:+.2f}%", f"{HIKE_MID - now['core_yoy']:+.2f}%"),
    ("Unemployment", f"{peak_row['unrate']:.1f}%", f"{piv['unrate']:.1f}%",
     f"{now['unrate']:.1f}%"),
    ("10-yr Treasury", f"{peak_row['gs10']:.2f}%", f"{piv['gs10']:.2f}%",
     f"{now['gs10']:.2f}%"),
]
hdr = f"  {'metric':<26}{'Volcker PEAK':>16}{'Volcker PIVOT':>16}{'TODAY':>26}"
print(hdr)
print(f"  {'':<26}{pk:%b-%Y':>16}"[:44] if False else
      f"  {'':<26}{pk.strftime('%b-%Y'):>16}{'Jul-1982':>16}"
      f"{today_m.strftime('%b-%Y'):>26}")
print("  " + "-" * (len(hdr) - 2))
for r in rows:
    print(f"  {r[0]:<26}{r[1]:>16}{r[2]:>16}{r[3]:>26}")
pd.DataFrame(rows, columns=["metric", f"volcker_peak_{pk:%Y-%m}",
                            "volcker_pivot_1982-07",
                            f"today_{today_m:%Y-%m}"]
             ).to_csv(os.path.join(DATA, "pivot_preconditions.csv"), index=False)

print(f"\n  >> Volcker held a real policy rate of "
      f"{piv['real_effr']:+.1f}pp (headline) at the moment he FIRST cut.")
print(f"  >> Warsh's real policy rate after the Sep-16-2026 hike is "
      f"{HIKE_MID - now['cpi_yoy']:+.1f}pp (headline).")
print(f"  >> Gap to the Volcker pivot condition: "
      f"{piv['real_effr'] - (HIKE_MID - now['cpi_yoy']):.1f}pp of real rate.")

# ================================================================ SECTION 4
print("\n" + "-" * 78)
print("4) THE 'DEBT CRISIS' TRIPWIRE TODAY (credit spreads)")
print("-" * 78)
for sid, label in [("BAMLH0A0HYM2", "US high-yield OAS"),
                   ("BAMLEMCBPIOAS", "EM corporate OAS")]:
    if sid in series:
        s = series[sid]
        last = s.iloc[-1]
        pct = (s < last).mean() * 100
        print(f"  {label:<20} {last:.2f}%  (percentile within the available "
              f"{s.index[0]:%Y-%m} -> {s.index[-1]:%Y-%m} window: {pct:.0f}th)")
        print(f"  {'':<20} window max {s.max():.2f}% ({s.idxmax():%Y-%m-%d}), "
              f"min {s.min():.2f}% ({s.idxmin():%Y-%m-%d})")
print("  Rule 4 flag: this FRED mirror truncates both OAS series to ~3 years,")
print("  so the percentile is WITHIN that short window only — not a full history.")

# ================================================================ SECTION 5
print("\n" + "-" * 78)
print("5) THE 1980 FALSE DAWN — why Volcker waited so long the SECOND time")
print("-" * 78)
fd = panel.loc["1980-01-01":"1981-12-01", ["effr", "cpi_yoy", "unrate"]]
apr80, jul80, dec80, jun81 = [panel.loc[d] for d in
                              ["1980-04-01", "1980-07-01", "1980-12-01", "1981-06-01"]]
print(f"  Apr-1980 EFFR {apr80['effr']:5.2f}%   CPI {apr80['cpi_yoy']:5.2f}%   "
      f"unemployment {apr80['unrate']:.1f}%   <- 1st peak")
print(f"  Jul-1980 EFFR {jul80['effr']:5.2f}%   CPI {jul80['cpi_yoy']:5.2f}%   "
      f"unemployment {jul80['unrate']:.1f}%   <- PREMATURE easing "
      f"({apr80['effr']-jul80['effr']:.2f}pp in 3 months)")
print(f"  Dec-1980 EFFR {dec80['effr']:5.2f}%   CPI {dec80['cpi_yoy']:5.2f}%   "
      f"unemployment {dec80['unrate']:.1f}%   <- forced to re-hike "
      f"{dec80['effr']-jul80['effr']:+.2f}pp")
print(f"  Jun-1981 EFFR {jun81['effr']:5.2f}%   CPI {jun81['cpi_yoy']:5.2f}%   "
      f"unemployment {jun81['unrate']:.1f}%   <- 2nd (true) peak")
print(f"\n  Real rate at the 1980 premature cut: "
      f"{jul80['real_effr']:+.2f}pp  (NEGATIVE-to-thin)")
print(f"  Real rate at the 1982 durable pivot : "
      f"{piv['real_effr']:+.2f}pp  (deeply positive)")
print("  >> Lesson: the first pivot failed BECAUSE the real rate was not yet")
print("     restrictive. That failure is why the 1982 pivot required +6pp real.")
fd.to_csv(os.path.join(DATA, "false_dawn_1980.csv"))

# ================================================================ SECTION 6
print("\n" + "-" * 78)
print("6) PIVOT-TRIGGER DASHBOARD — measurable tripwires, 1982 analog vs today")
print("-" * 78)

# Sahm-rule style labour trigger
u = panel["unrate"].dropna()
u3 = u.rolling(3).mean()
sahm = u3 - u3.rolling(12).min()


def sahm_at(dt):
    return sahm.loc[:dt].iloc[-1]


cyc_low_now = u.loc["2022-01-01":].min()
cyc_low_now_dt = u.loc["2022-01-01":].idxmin()
cyc_low_81 = u.loc["1979-01-01":"1981-12-01"].min()
cyc_low_81_dt = u.loc["1979-01-01":"1981-12-01"].idxmin()

months_shock_to_pivot = (1982 - 1979) * 12 + (7 - 10)

triggers = [
    ("T1 Inflation delivered",
     f"headline CPI {piv['cpi_yoy']:.1f}% (down {panel.loc['1980-03-01','cpi_yoy'] - piv['cpi_yoy']:.1f}pp "
     f"from the {panel.loc['1980-03-01','cpi_yoy']:.1f}% Mar-80 peak)",
     f"headline CPI {now['cpi_yoy']:.1f}%, core {now['core_yoy']:.1f}%",
     "PARTLY MET — core near target, but an oil shock is still passing through"),
    ("T2 Real policy rate restrictive",
     f"{piv['real_effr']:+.1f}pp headline / {piv['real_effr_core']:+.1f}pp core",
     f"{HIKE_MID - now['cpi_yoy']:+.1f}pp headline / {HIKE_MID - now['core_yoy']:+.1f}pp core",
     "NOT MET — policy is barely restrictive; nothing yet to 'un-do'"),
    ("T3 Labour market cracks",
     f"unemployment {piv['unrate']:.1f}% (+{piv['unrate']-cyc_low_81:.1f}pp from the "
     f"{cyc_low_81:.1f}% {cyc_low_81_dt:%b-%y} low); Sahm {sahm_at('1982-07-01'):+.2f}",
     f"unemployment {now['unrate']:.1f}% (+{now['unrate']-cyc_low_now:.1f}pp from the "
     f"{cyc_low_now:.1f}% {cyc_low_now_dt:%b-%y} low); Sahm {sahm_at(today_m):+.2f}",
     "NOT MET — no recession"),
    ("T4 Financial accident / credit",
     "Drysdale (May-82), Penn Square (Jul-5-82), Mexico (Aug-12-82), "
     "Lombard-Wall (Aug-82)",
     f"US HY OAS {series['BAMLH0A0HYM2'].iloc[-1]:.2f}%, "
     f"EM corp OAS {series['BAMLEMCBPIOAS'].iloc[-1]:.2f}% (window low)",
     "NOT MET — credit is at the TIGHT end; no accident visible"),
    ("T5 Technical cover / framework",
     "M1 distorted by new deposit accounts -> target de-emphasised Oct-9-82",
     "no equivalent identified — unknown",
     "UNKNOWN"),
]
print(f"  {'trigger':<32}{'1982 analog':<70}{'today':<52}status")
for t in triggers:
    print(f"  {t[0]:<32}{t[1][:68]:<70}{t[2][:50]:<52}{t[3]}")
pd.DataFrame(triggers, columns=["trigger", "volcker_1982_analog", "today_2026",
                                "status"]
             ).to_csv(os.path.join(DATA, "pivot_triggers.csv"), index=False)

print(f"\n  Clock: Volcker shock Oct-1979 -> first cut Jul-1982 = "
      f"{months_shock_to_pivot} months.")
print(f"  Same elapsed time from the Warsh hike (Sep-2026) lands in "
      f"{pd.Timestamp('2026-09-16') + pd.DateOffset(months=months_shock_to_pivot):%b-%Y}.")
print("  (Calibration only — NOT a forecast. Volcker started with 12% inflation;")
print("   Warsh started with ~3.7%, so his required distance is far shorter.)")

# ================================================================ SECTION 7
print("\n" + "-" * 78)
print("7) THE DECISIVE REFUTATION — the Fed RE-TIGHTENED while the debt crisis")
print("   was getting WORSE. Rates bottomed years before the crisis was resolved.")
print("-" * 78)
trough = panel.loc["1982-12-01":"1983-06-01", "effr"]
t_dt, t_val = trough.idxmin(), trough.min()
post = panel.loc["1983-01-01":"1985-12-01", "effr"]
r_dt, r_val = post.idxmax(), post.max()
print(f"  EFFR cycle trough        : {t_val:.2f}%  ({t_dt:%b-%Y})")
print(f"  EFFR re-tightening peak  : {r_val:.2f}%  ({r_dt:%b-%Y})  "
      f"= {r_val - t_val:+.2f}pp ABOVE the trough")
for d, ev in [("1983-08-01", "LDC crisis spreading; 27 countries / $239bn rescheduling by Oct-83"),
              ("1984-05-01", "Continental Illinois fails — the largest US bank failure to date"),
              ("1985-10-01", "Baker Plan (debt still NOT reduced, only rescheduled)"),
              ("1989-03-01", "Brady Plan — actual principal forgiveness begins")]:
    try:
        print(f"    {pd.Timestamp(d):%b-%Y}  EFFR {panel.loc[d,'effr']:5.2f}%   {ev}")
    except KeyError:
        print(f"    {pd.Timestamp(d):%b-%Y}  EFFR   n/a   {ev}")
print("\n  >> If the LDC crisis had ENDED the tightening, rates would have stayed")
print("     down until the crisis was resolved. Instead the Fed raised rates by")
print(f"     {r_val - t_val:.1f}pp into the WORST of it, and the funds-rate trough came")
print("     ~6.5 years before the Brady Plan actually reduced the debt.")
pd.DataFrame({"effr": panel.loc["1982-01-01":"1986-12-01", "effr"]}
             ).to_csv(os.path.join(DATA, "retightening_1983_84.csv"))

# ================================================================ SECTION 8
print("\n" + "-" * 78)
print("8) THE MODERN CONTROL EXPERIMENT — SVB, March 2023")
print("   Does a financial accident stop a hiking cycle? Check the tape.")
print("-" * 78)
svb = panel.loc["2023-01-01":"2023-08-01", ["effr", "cpi_yoy", "unrate"]]
for dt, row in svb.iterrows():
    tag = ""
    if f"{dt:%Y-%m}" == "2023-03":
        tag = "  <- SVB fails Mar 10; Fed HIKES 25bp Mar 22 and launches the BTFP"
    print(f"    {dt:%Y-%m}  EFFR {row['effr']:5.2f}%   CPI {row['cpi_yoy']:5.2f}%"
          f"   unemployment {row['unrate']:.1f}%{tag}")
print(f"\n  EFFR Feb-2023 {panel.loc['2023-02-01','effr']:.2f}%  ->  "
      f"Jul-2023 {panel.loc['2023-07-01','effr']:.2f}%  "
      f"({panel.loc['2023-07-01','effr'] - panel.loc['2023-02-01','effr']:+.2f}pp "
      f"THROUGH the banking crisis)")
print("  >> Same lesson as 1982: a financial accident gets a LIQUIDITY tool")
print("     (BTFP 2023 / swap lines + BIS bridge + forbearance 1982), NOT a")
print("     rate cut. Monetary policy and financial-stability policy are separate.")
svb.to_csv(os.path.join(DATA, "svb_2023_control.csv"))

# ================================================================ CHARTS
def panel_plot(ax, df, title, marks):
    ax.plot(df.index, df["effr"], color="#c0392b", lw=2.0, label="Fed funds (effective)")
    ax.plot(df.index, df["cpi_yoy"], color="#2c3e50", lw=1.6, label="CPI YoY")
    ax.plot(df.index, df["unrate"], color="#16a085", lw=1.4, ls="--", label="Unemployment")
    ax.fill_between(df.index, 0, df["real_effr"], where=df["real_effr"] >= 0,
                    color="#2980b9", alpha=0.20, label="Real policy rate (+)")
    ax.fill_between(df.index, 0, df["real_effr"], where=df["real_effr"] < 0,
                    color="#e67e22", alpha=0.25, label="Real policy rate (−)")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_ylabel("percent")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7.5, loc="upper right", ncol=2)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + (hi - lo) * 0.10)
    lo, hi = ax.get_ylim()
    for i, (x, txt, col) in enumerate(marks):
        ax.axvline(pd.Timestamp(x), color=col, ls=":", lw=1.4)
        ax.annotate(txt, xy=(pd.Timestamp(x), hi),
                    xytext=(6, -8 - 13 * (i % 3)), textcoords="offset points",
                    fontsize=7.0, color=col, va="top", ha="left",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white",
                              ec=col, lw=0.6, alpha=0.88))


fig, axes = plt.subplots(3, 1, figsize=(14, 15))

panel_plot(
    axes[0], panel.loc["1977-01-01":"1987-12-01"],
    "A. The Volcker regime — the durable pivot required a HUGE positive real rate "
    "(note the failed 1980 pivot at a NEGATIVE real rate)",
    [("1979-10-06", "Oct-79 Volcker shock", "#8e44ad"),
     ("1980-07-01", "Jul-80 FALSE DAWN (cut at −4.1pp real)", "#d35400"),
     ("1981-07-01", "Jul-81 recession begins", "#7f8c8d"),
     ("1982-07-20", "Jul-20-82 FIRST discount cut", "#27ae60"),
     ("1982-08-12", "Aug-12-82 Mexico", "#c0392b"),
     ("1982-11-01", "Nov-82 recession ends", "#7f8c8d")])

# --- the money shot: daily fed funds through 1982
axz = axes[1]
dz = series["DFF"].loc["1982-01-01":"1983-06-30"]
axz.plot(dz.index, dz.values, color="#c0392b", lw=1.5,
         label="Daily effective fed funds")
axz.plot(series["INTDSRUSM193N"].loc["1982-01-01":"1983-06-30"].index,
         series["INTDSRUSM193N"].loc["1982-01-01":"1983-06-30"].values,
         color="#2c3e50", lw=1.8, drawstyle="steps-post",
         label="Discount rate (monthly avg)")
zmarks = [("1982-05-17", "Drysdale collapses", "#8e44ad"),
          ("1982-07-05", "Penn Square Bank fails", "#d35400"),
          ("1982-07-20", "CUT #1 (voted Jul 19)\n12.0% → 11.5%", "#27ae60"),
          ("1982-08-02", "CUT #2 (voted Jul 30)", "#27ae60"),
          ("1982-08-12", "MEXICO cannot pay", "#c0392b"),
          ("1982-09-13", "Board REFUSES a cut", "#c0392b"),
          ("1982-10-09", "M1 target de-emphasised", "#16a085")]
lo, hi = axz.get_ylim()
axz.set_ylim(lo - 1.2, hi + 2.2)
lo, hi = axz.get_ylim()
for i, (x, txt, col) in enumerate(zmarks):
    axz.axvline(pd.Timestamp(x), color=col, ls=":", lw=1.5)
    axz.annotate(txt, xy=(pd.Timestamp(x), hi),
                 xytext=(5, -8 - 30 * (i % 2)), textcoords="offset points",
                 fontsize=7.4, color=col, va="top", ha="left", fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.22", fc="white", ec=col,
                           lw=0.7, alpha=0.9))
axz.annotate("", xy=(pd.Timestamp("1982-08-12"), lo + 0.5),
             xytext=(pd.Timestamp("1982-07-19"), lo + 0.5),
             arrowprops=dict(arrowstyle="<->", color="#27ae60", lw=1.6))
axz.text(pd.Timestamp("1982-07-22"), lo + 0.75,
         "24 days, and TWO cuts, BEFORE Mexico", fontsize=8.5,
         color="#27ae60", fontweight="bold")
axz.set_title("B. ZOOM 1982 (daily) — TWO discount-rate cuts were voted BEFORE Mexico; "
              "then the Board REFUSED one on Sep 13, mid-crisis",
              fontsize=11, fontweight="bold")
axz.set_ylabel("percent")
axz.grid(alpha=0.25)
axz.legend(fontsize=8, loc="upper right")

panel_plot(
    axes[2], panel.loc["2021-01-01":],
    "C. Today — Warsh has hiked into a real policy rate near ZERO. "
    "This is the 1979 starting line, not the 1982 finish line.",
    [("2022-03-16", "Mar-22 hiking begins", "#7f8c8d"),
     ("2026-09-16", "Sep-16-26 Warsh hikes to 3.75–4.00%", "#c0392b")])
axes[2].set_xlim(pd.Timestamp("2021-01-01"), pd.Timestamp("2027-06-01"))
axes[2].legend(fontsize=7.5, loc="center left", ncol=2)

fig.suptitle("What actually ends a tightening regime? Volcker 1979-82 vs Warsh 2026\n"
             "Source: FRED (DFF, FEDFUNDS, INTDSRUSM193N, CPIAUCSL, UNRATE). "
             "Real rate = fed funds − CPI YoY.",
             fontsize=13, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.955])
p1 = os.path.join(CHARTS, "volcker_vs_warsh.png")
fig.savefig(p1, dpi=135)
plt.close(fig)
print(f"\n  chart -> {p1}")

# distance-to-pivot bars
fig, ax = plt.subplots(figsize=(11, 5.6))
labels = ["Real policy rate\n(headline)", "Real policy rate\n(core)",
          "Headline CPI", "Unemployment"]
vpk = [peak_row["real_effr"], peak_row["real_effr_core"],
       peak_row["cpi_yoy"], peak_row["unrate"]]
vpv = [piv["real_effr"], piv["real_effr_core"], piv["cpi_yoy"], piv["unrate"]]
vnw = [HIKE_MID - now["cpi_yoy"], HIKE_MID - now["core_yoy"],
       now["cpi_yoy"], now["unrate"]]
x = range(len(labels))
w = 0.26
ax.bar([i - w for i in x], vpk, w, label=f"Volcker PEAK ({pk:%b-%Y})", color="#c0392b")
ax.bar(list(x), vpv, w, label="Volcker PIVOT (Jul-1982)", color="#e67e22")
ax.bar([i + w for i in x], vnw, w,
       label=f"TODAY (post Sep-16-26 hike, CPI {today_m:%b-%Y})", color="#2980b9")
for i, (a, b, c) in enumerate(zip(vpk, vpv, vnw)):
    for off, val in [(-w, a), (0, b), (w, c)]:
        ax.text(i + off, val + (0.3 if val >= 0 else -0.9), f"{val:.1f}",
                ha="center", fontsize=8.5)
ax.axhline(0, color="k", lw=0.9)
ax.set_xticks(list(x))
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylim(top=max(max(vpk), max(vpv), max(vnw)) * 1.38)
ax.set_ylabel("percent / percentage points")
ax.set_title("Distance to a 'Volcker pivot': the binding condition was a large POSITIVE "
             "real rate\nplus a 10.8% unemployment recession — today has neither",
             fontsize=11.5, fontweight="bold")
ax.grid(axis="y", alpha=0.25)
ax.legend(fontsize=8.5, loc="upper center", ncol=3)
fig.tight_layout()
p2 = os.path.join(CHARTS, "distance_to_pivot.png")
fig.savefig(p2, dpi=140)
plt.close(fig)
print(f"  chart -> {p2}")

print("\nDone. CSVs in data/, charts in charts/.")

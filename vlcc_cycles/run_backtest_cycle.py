# -*- coding: utf-8 -*-
"""
SECTION 21 — BACK-TEST + PURE-NUMBERS CYCLE POSITION.

Part 1 back-tests every dated forecast made in March / April / June 2026
against what actually happened.
Part 2 validates the section-20 earnings engine against REPORTED Q2-2026
results -- this is the hard evidence Astra's [B1] objection demanded.
Part 3 rebuilds valuation from observables only: realised TCE, second-hand
values, 1-year TC rates and the ACTUAL spot/charter split.
Part 4 scores the cycle position on numbers alone.

EVERY INPUT IS SOURCED. Nothing is modelled where a reported figure exists.
"""

import io
import os
import sys

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
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")

# ───────────────────────────── REPORTED ACTUALS (sourced) ─────────────────────
ACT = {
    "DHT": dict(
        q1_eps=1.02, q1_dps=0.41, q1_tce=78_800, q1_spot=106_000, q1_tc=61_300,
        q1_spot_unadj=91_700,
        q1_reported_ni=164.527, q1_vessel_gain=59.994, q1_deriv_gain=1.119,
        q1_ordinary_eps=0.64,
        q2_eps=1.22, q2_dps=1.22, q2_tce=126_700, q2_spot=162_600, q2_tc=90_800,
        q2_spot_adj=154_100, q2_reported_eps=1.23,
        q2_ni=198.3, q2_ebitda=231.0, q2_rev=255.0,
        q2_spot_opdays=48.4, q2_spot_ships=11, q2_ships=23,
        src="DHT 6-K 5 Aug 2026; Q1 release 5 May 2026"),
    "FRO": dict(
        q1_eps=2.51, q1_dps=1.55, q1_ni=559.0,
        q2_eps=2.96, q2_adj_eps=2.61, q2_dps=2.61, q2_special=0.80,
        q2_ni=659.2, q2_adj_ni=580.2, q2_rev=943.3,
        q2_vlcc_tce=152_700, q2_smax_tce=111_500, q2_lr2_tce=92_400,
        q3_booked_pct=86, q3_booked_rate=156_900,
        src="Frontline Q2-2026 results, 28 Aug 2026"),
}

# Company statics, unchanged from section 20 (filing-sourced)
CO = {
    "DHT": dict(vlcc_eq=24.0, days=350, breakeven=17_500, dna=105,
                shares=161.236, navps=14.33, bvps=8.26, net_debt=273.1,
                fleet_mv=2583.0, pnav_hi=1.36),
    "FRO": dict(vlcc_eq=57.9, days=350, breakeven=23_800, dna=300,
                shares=222.623, navps=30.37, bvps=14.15, net_debt=2113.4,
                fleet_mv=8875.0, pnav_hi=1.50),
}

# ───────────────────────────── MARKET OBSERVABLES (sourced) ───────────────────
# ⚠️ TD3C IS A PANEL ASSESSMENT, NOT A TRANSACTION PRICE.
# The Baltic told panellists (Circular 12/26, 4 Mar 2026) to assess the "best
# achievable market value" using judgement where direct fixtures are absent.
# Physical liquidity on the Hormuz-transit voyage has collapsed, so the printed
# benchmark and the business the market can actually see have diverged by ~2x.
# Every ratio below is therefore computed on the TRANSACTABLE figures, with the
# headline print shown only for context.
MKT = dict(
    td3c_assess=1_035_000,      # Baltic TD3C, 14 Sep 2026 -- ASSESSMENT
    td3c_tce_11sep=862_150,     # Baltic TD3C round-voyage TCE, 11 Sep
    td34_11sep=465_764,         # Baltic TD34 (loads OUTSIDE Hormuz), 11 Sep
    fixture_lo=530_000, fixture_hi=603_000,   # reported fixtures, w/c 8 Sep
    td3c_1sep=704_000,
    td2=702_000, td15=219_000, td22=208_000,   # Signal, 4 Sep 2026
    tc1yr_lo=93_000, tc1yr_hi=105_000,          # DHT Redwood 2011-built @105k
    vlcc_5yr=151.1, vlcc_nb=130.2,              # Signal, end-Aug 2026
    vlcc_20yr=71.1, vlcc_scrap=20.8,
    yoy_5=0.30, yoy_10=0.42, yoy_15=0.61, yoy_20=0.90,
    orders_2026_vlcc=217, orders_2026_crude=279,
    orderbook_pct_capacity=0.25,
    recycled_1h26=21,
    warrisk_now=0.0875, warrisk_pre=0.0025,
)

print("=" * 100)
print("SECTION 21 — BACK-TEST AND PURE-NUMBERS CYCLE POSITION")
print("=" * 100)

px = {}
for t in CO:
    s = yf.download(t, period="1mo", progress=False, auto_adjust=False)["Close"]
    px[t] = float((s.iloc[:, 0] if hasattr(s, "columns") else s).dropna().iloc[-1])
    CO[t]["price"] = px[t]
print(f"\n  Spot: DHT US${px['DHT']:.2f} · FRO US${px['FRO']:.2f}")


def eps_at(d, tc):
    return ((tc - d["breakeven"]) * d["vlcc_eq"] * d["days"] / 1e6 - d["dna"]) / d["shares"]


def ni_at(d, tc):
    return (tc - d["breakeven"]) * d["vlcc_eq"] * d["days"] / 1e6 - d["dna"]


# ══════════════════════════ PART 2 FIRST: RECONCILE THE ENGINE ════════════════
print("\n" + "=" * 100)
print("A) ENGINE RECONCILIATION vs REPORTED Q2-2026 — NOT a validation")
print("=" * 100)
print("  ⚠️ An earlier draft of this section claimed the engine was 'VALIDATED'")
print("     and that Astra's objection [B1] was 'answered'. BOTH CLAIMS ARE")
print("     WITHDRAWN. Frontline's own filing defines cash breakeven as covering")
print("     'operating expenses, including dry docks, REPAYMENTS OF LOANS, net")
print("     interest expense, bareboat hire, time charter hire and net G&A'.")
print("     Loan principal is not a P&L expense, so subtracting that breakeven")
print("     and then D&A cannot produce accounting earnings. The objection is")
print("     CONFIRMED by the filing, not answered.\n")

val = []
dht_model_q = ni_at(CO["DHT"], ACT["DHT"]["q2_tce"]) / 4
fro_model_q = ni_at(CO["FRO"], ACT["FRO"]["q2_vlcc_tce"]) / 4
for t, inp, mod, act in [("DHT", ACT["DHT"]["q2_tce"], dht_model_q, ACT["DHT"]["q2_ni"]),
                         ("FRO", ACT["FRO"]["q2_vlcc_tce"], fro_model_q, ACT["FRO"]["q2_adj_ni"])]:
    err = (mod / act - 1) * 100
    print(f"  {t} @ US${inp:,}/day:  model US${mod:.1f}m  vs  reported US${act:.1f}m"
          f"   ({err:+.1f}%)")
    val.append(dict(ticker=t, input_tce=inp, model_ni_q=round(mod, 1),
                    actual_ni_q=round(act, 1), error_pct=round(err, 1)))
pd.DataFrame(val).to_csv(os.path.join(DATA, "s21_validation.csv"), index=False)

print("\n  WHY THE CLOSE FIT PROVES NOTHING — the components do NOT reconcile.")
print("  The small bottom-line error is produced by TWO LARGER ERRORS CANCELLING:")
print(f"  {'':<6}{'model TCE revenue':>20}{'actual':>12}{'overstated by':>15}")
OFFSET = [("FRO", 773.616, 753.274, 195.577, 173.064),
          ("DHT", 266.070, 254.963, 63.000, 57.914)]
for t, mrev, arev, mded, aded in OFFSET:
    print(f"  {t:<6}{mrev:>20.1f}{arev:>12.1f}{mrev-arev:>+14.1f}m")
    print(f"        deductions to profit {mded:>11.1f}{aded:>12.1f}{mded-aded:>+14.1f}m")
print("  >> FRO: revenue overstated US$20.3m, deductions overstated US$22.5m,")
print("     leaving a deceptively small US$2.2m earnings error.")

print("\n  AND THE PARAMETERS ARE NOT SEPARATELY IDENTIFIED.")
print("     NI = A x TCE - (A x breakeven + D&A)")
print("  Only the COMBINED intercept (A x breakeven + D&A) is identified by")
print("  earnings. Offsetting changes leave every model output unchanged:")
for t, d, off in [("DHT", CO["DHT"], 8.4), ("FRO", CO["FRO"], 20.265)]:
    shift = d["vlcc_eq"] * d["days"] * 1_000 / 1e6
    print(f"     {t}: breakeven +US$1,000/day  and  D&A -US${shift:.1f}m "
          f"=> identical output")
print("  >> So a close fit cannot confirm that EITHER parameter is right.")
print("  >> STATUS: in-sample RECONCILIATION CHECK. Not an out-of-sample test,")
print("     not an accounting validation. One high-rate quarter only.")

# implied spot share from the two disclosed legs
s_dht = (ACT["DHT"]["q2_tce"] - ACT["DHT"]["q2_tc"]) / \
        (ACT["DHT"]["q2_spot"] - ACT["DHT"]["q2_tc"])
print(f"\n  DHT SPOT EXPOSURE — three measures, deliberately NOT conflated:")
print(f"     implied by the rounded TCE disclosures .... {s_dht*100:.0f}% of revenue days")
print(f"     DHT-reported spot share of operating days . {ACT['DHT']['q2_spot_opdays']:.1f}%")
print(f"     vessels on spot at quarter end ............ "
      f"{ACT['DHT']['q2_spot_ships']} of {ACT['DHT']['q2_ships']} "
      f"({ACT['DHT']['q2_spot_ships']/ACT['DHT']['q2_ships']*100:.1f}%)")
print("  >> All three say ROUGHLY HALF. None says 75-79%, which is what the")
print("     April model assumed. The earlier draft's claim of an EXACT 50.0%")
print("     solve is withdrawn: the inputs are rounded and the three bases differ.")

print(f"\n  ⚠️ FRO's '{CO['FRO']['vlcc_eq']} VLCC-equivalents' is a MODELLING CHOICE, not a")
print("     disclosure. It was built as 42 + 21x0.5 + 18x0.3 on an older")
print("     81-vessel configuration. Frontline's ACTUAL Q2 rate ratios were:")
r_s = ACT["FRO"]["q2_smax_tce"] / ACT["FRO"]["q2_vlcc_tce"]
r_l = ACT["FRO"]["q2_lr2_tce"] / ACT["FRO"]["q2_vlcc_tce"]
alt = 40 + 19 * r_s + 18 * r_l
print(f"     Suezmax/VLCC {r_s:.3f} (assumed 0.500) · LR2/VLCC {r_l:.3f} (assumed 0.300)")
print(f"     On the stated 40/19/18 fleet those imply {alt:.2f} equivalents, not "
      f"{CO['FRO']['vlcc_eq']}.")
e_now = eps_at(CO["FRO"], MKT["tc1yr_hi"])
d_alt = dict(CO["FRO"]); d_alt["vlcc_eq"] = alt
e_alt = eps_at(d_alt, MKT["tc1yr_hi"])
print(f"     Effect at US${MKT['tc1yr_hi']:,}/day: EPS ${e_now:.2f} -> ${e_alt:.2f} "
      f"({(e_alt/e_now-1)*100:+.0f}%)")
print("  >> Every FRO figure in sections 20 and 21 uses 57.9 and is therefore")
print("     CONSERVATIVE on earnings. The sensitivity is disclosed, not buried.")

# ══════════════════════════ PART 1: THE BACK-TEST ═════════════════════════════
print("\n" + "=" * 100)
print("B) BACK-TEST — every dated forecast vs what actually happened")
print("=" * 100)

# realised rates
dht_h1_tce = (ACT["DHT"]["q1_tce"] + ACT["DHT"]["q2_tce"]) / 2
dht_h1_eps = ACT["DHT"]["q1_eps"] + ACT["DHT"]["q2_eps"]
fro_h1_eps = ACT["FRO"]["q1_eps"] + ACT["FRO"]["q2_eps"]
print(f"\n  REALISED 1H-2026, on ORDINARY (recurring) earnings:")
print(f"    DHT ordinary EPS ${ACT['DHT']['q1_ordinary_eps']:.2f} + "
      f"${ACT['DHT']['q2_eps']:.2f} = ${ACT['DHT']['q1_ordinary_eps']+ACT['DHT']['q2_eps']:.2f} "
      f"(annualised ${(ACT['DHT']['q1_ordinary_eps']+ACT['DHT']['q2_eps'])*2:.2f})")
print(f"    DHT REPORTED EPS was ${ACT['DHT']['q1_eps']:.2f} + ${ACT['DHT']['q2_eps']:.2f}; "
      f"the difference is the Q1 vessel-sale gain")
print(f"    FRO adjusted EPS ${ACT['FRO']['q2_adj_eps']:.2f} in Q2 "
      f"(annualised ${ACT['FRO']['q2_adj_eps']*4:.2f}); reported was "
      f"${ACT['FRO']['q2_eps']:.2f}")

BT = [
    # ONLY genuine forward-looking targets. Four rows in the earlier draft were
    # REMOVED because they were not forecasts at all:
    #   - April "DHT price $18.57" / "FRO price $35.08" were the THEN-CURRENT
    #     market prices, so scoring them just measures that the shares rose.
    #   - March "DHT P/B 2.75" / "FRO P/B 3.65" were labelled "P/B (trailing)",
    #     i.e. contemporaneous observations, not predicted multiples.
    ("2026-03-02", "Deep Dive", "DHT target @ $100k, 7x PE", 23.70, px["DHT"], "12m"),
    ("2026-03-02", "Deep Dive", "FRO target @ $100k, 7x PE", 52.60, px["FRO"], "12m"),
    ("2026-04-08", "April Update", "DHT target @ $100k, 7x", 21.69, px["DHT"], "12m"),
    ("2026-04-08", "April Update", "FRO target @ $100k, 7x", 47.47, px["FRO"], "12m"),
    ("2026-04-08", "April Update", "DHT prob-weighted target", 29.05, px["DHT"], "12m"),
    ("2026-04-08", "April Update", "FRO prob-weighted target", 64.54, px["FRO"], "12m"),
    ("2026-06-26", "Cycle Jun26", "DHT base target ($95k, 6x)", 17.00, px["DHT"], "12m"),
    ("2026-06-26", "Cycle Jun26", "FRO base target ($95k, 6x)", 38.00, px["FRO"], "12m"),
    ("2026-06-26", "Cycle Jun26", "DHT bull target ($120k, 6.5x)", 25.00, px["DHT"], "12m"),
    ("2026-06-26", "Cycle Jun26", "FRO bull target ($120k, 6.5x)", 55.00, px["FRO"], "12m"),
]
print(f"\n  B1. PRICE TARGETS — ⚠️ ALL HORIZONS ARE STILL OPEN")
print("      Every target below was set on a 12-month horizon. The earliest")
print("      matures in March 2027. These are INTERIM MARKS, not completed")
print("      forecasts, and no skill can be claimed from them yet.")
print(f"\n  {'set on':<12}{'source':<15}{'target':<32}{'forecast':>10}{'now':>9}"
      f"{'gap':>8}{'matures':>10}")
rows = []
for dt, src, met, fc, ac, hz in BT:
    diff = (ac / fc - 1) * 100
    mat = {"2026-03-02": "2027-03", "2026-04-08": "2027-04",
           "2026-06-26": "2027-06"}[dt]
    print(f"  {dt:<12}{src:<15}{met:<32}{fc:>10.2f}{ac:>9.2f}{diff:>7.0f}%{mat:>10}")
    rows.append(dict(date=dt, source=src, metric=met, forecast=fc,
                     actual=round(ac, 2), diff_pct=round(diff), matures=mat,
                     status="OPEN"))
n_within = sum(1 for r in rows if abs(r["diff_pct"]) <= 10)
print(f"\n  >> {n_within} of {len(rows)} are currently within 10% of the mark.")
print("     Reported as a STATUS, not a score. No hit-rate is claimed.")

# ---- B2: conditional earnings error, on matched accounting bases -------------
print(f"\n  B2. CONDITIONAL EARNINGS ERROR — the only part that CAN be scored now")
print("      This tests one thing only: GIVEN the freight rate that actually")
print("      occurred, did the published earnings curve give the right profit?")
print("      It does NOT test the ability to forecast the rate itself.\n")
print("      Accounting fixes applied after external review:")
print(f"       · DHT Q1 reported profit US${ACT['DHT']['q1_reported_ni']:.1f}m included a")
print(f"         US${ACT['DHT']['q1_vessel_gain']:.1f}m VESSEL-SALE GAIN and a "
      f"US${ACT['DHT']['q1_deriv_gain']:.1f}m derivative gain.")
print(f"         Ordinary Q1 EPS is ~${ACT['DHT']['q1_ordinary_eps']:.2f}, not "
      f"${ACT['DHT']['q1_eps']:.2f}. Using the reported figure")
print("         would credit the freight model with a one-off asset disposal.")
print("       · DHT's Q1 US$106,000 is ADJUSTED spot TCE (IFRS 15) while Q2's")
print("         US$162,600 is UNADJUSTED. The earlier draft averaged the two")
print("         different bases. Both legs are now taken on the ADJUSTED basis.")

CURVES = {
    "April Update": dict(
        rate=[75_000, 90_000, 100_000, 120_000, 150_000, 200_000, 250_000],
        DHT=[2.18, 2.73, 3.10, 3.84, 4.94, 6.79, 8.63],
        FRO=[4.68, 5.94, 6.78, 8.46, 10.99, 15.20, 19.41]),
    "Cycle Jun26": dict(
        rate=[50_000, 70_000, 90_000, 100_000, 120_000],
        DHT=[1.25, 1.99, 2.73, 3.10, 3.84],
        FRO=[2.57, 4.26, 5.94, 6.78, 8.46]),
    "Deep Dive": dict(
        rate=[100_000, 150_000],
        DHT=[3.39, 5.43], FRO=[7.51, 12.15]),
}


def curve_eps(c, t, r):
    """Linear interpolation, with TRUE linear extrapolation outside the domain.

    The earlier draft used np.interp, which CLAMPS to the endpoint value and
    does not extrapolate -- so rows labelled 'extrapolated' were in fact the
    curve's last point. That produced three wrong verdicts.
    """
    x, y = np.asarray(c["rate"], float), np.asarray(c[t], float)
    inside = x[0] <= r <= x[-1]
    if inside:
        return float(np.interp(r, x, y)), True
    if r < x[0]:
        sl = (y[1] - y[0]) / (x[1] - x[0])
        return float(y[0] + sl * (r - x[0])), False
    sl = (y[-1] - y[-2]) / (x[-1] - x[-2])
    return float(y[-1] + sl * (r - x[-1])), False


dht_rate = (ACT["DHT"]["q1_spot"] + ACT["DHT"]["q2_spot_adj"]) / 2   # matched basis
dht_ord_eps = (ACT["DHT"]["q1_ordinary_eps"] + ACT["DHT"]["q2_eps"]) * 2
REAL = {
    "DHT": (dht_rate, dht_ord_eps, "1H-26 avg ADJUSTED spot TCE; ordinary EPS x2"),
    "FRO": (ACT["FRO"]["q2_vlcc_tce"], ACT["FRO"]["q2_adj_eps"] * 4,
            "Q2-26 VLCC spot TCE; adjusted EPS x4"),
}
print(f"\n  {'curve':<15}{'co':<5}{'realised rate':>14}{'curve EPS':>11}"
      f"{'actual EPS':>12}{'error':>8}  domain")
for src, c in CURVES.items():
    for t in ["DHT", "FRO"]:
        r, act_eps, _ = REAL[t]
        fc_eps, inside = curve_eps(c, t, r)
        diff = (act_eps / fc_eps - 1) * 100
        dom = "in-sample" if inside else "EXTRAPOLATED — weak"
        print(f"  {src:<15}{t:<5}{r:>14,.0f}{fc_eps:>11.2f}{act_eps:>12.2f}"
              f"{diff:>7.0f}%  {dom}")
        rows.append(dict(date=src, source=src, metric=f"{t} EPS | realised rate",
                         forecast=round(fc_eps, 2), actual=round(act_eps, 2),
                         diff_pct=round(diff), matures="n/a",
                         status="in-sample" if inside else "extrapolated"))
bt = pd.DataFrame(rows)
bt.to_csv(os.path.join(DATA, "s21_backtest.csv"), index=False)
print(f"\n  >> DHT: {REAL['DHT'][2]} = US${REAL['DHT'][0]:,.0f}/day, "
      f"EPS ${REAL['DHT'][1]:.2f}")
print(f"     FRO: {REAL['FRO'][2]} = US${REAL['FRO'][0]:,.0f}/day, "
      f"EPS ${REAL['FRO'][1]:.2f}")
print("  >> Note the two companies are annualised over DIFFERENT windows")
print("     (DHT two quarters, FRO one). They are not comparable with each other.")

errs = [r["diff_pct"] for r in rows if r["matures"] == "n/a"]
print(f"\n  ⚠️ DIRECTION OF THE ERROR — all {len(errs)} comparisons point the SAME way:")
print(f"     every published earnings curve OVERSTATED profit at the rate that")
print(f"     actually occurred, by {abs(max(errs)):.0f}-{abs(min(errs)):.0f}%.")
print("     The earlier draft of this section reported the OPPOSITE ('EXCEEDED')")
print("     because it (a) counted a one-off vessel-sale gain as freight earnings")
print("     and (b) used np.interp, which CLAMPS at the curve endpoint instead of")
print("     extrapolating. Both faults were found in external review and fixed.")
print("  >> Corrected reading: the rate forecasts were roughly right; the COST")
print("     and share-count assumptions behind the curves were too generous.")

# supply forecast back-test -- the one that went the WRONG way
print("\n  ⚠️ THE ONE THAT MOVED AGAINST THE THESIS — the orderbook:")
SUP = [("2026-05-28", "VLCC orderbook, % of fleet", "17-26%", "~25% of fleet by capacity"),
       ("2026-05-28", "VLCC orderbook, vessels", "~142", f"{MKT['orders_2026_vlcc']} VLCCs ORDERED IN 2026 ALONE"),
       ("2026-08-22", "orderbook % of fleet", "~35% (was 2% in 2023)", "confirmed, still climbing"),
       ("2026-05-28", "2026 VLCC scrapped", "2025: only 2", f"1H-2026: {MKT['recycled_1h26']} tankers total recycled")]
for d, m, f_, a in SUP:
    print(f"     {d}  {m:<32} forecast {f_:<24} actual {a}")
print("     >> Ordering ACCELERATED. This is the cycle's expiry being pulled forward.")

# ══════════════════════════ PART 3: PURE NUMBERS NOW ══════════════════════════
print("\n" + "=" * 100)
print("C) WHERE THE NUMBERS STAND TODAY — observables only")
print("=" * 100)
print(f"\n  FREIGHT — and the benchmark problem that changes how this must be read")
print(f"    TD3C ASSESSMENT, 14 Sep .................. US${MKT['td3c_assess']:,}/day")
print(f"    TD3C round-voyage TCE, 11 Sep ............ US${MKT['td3c_tce_11sep']:,}/day")
print(f"    reported PHYSICAL fixtures, w/c 8 Sep .... US${MKT['fixture_lo']:,}-{MKT['fixture_hi']:,}/day")
print(f"    TD34 (loads OUTSIDE Hormuz), 11 Sep ...... US${MKT['td34_11sep']:,}/day")
print(f"    TD2 MEG-Singapore, 4 Sep ................. US${MKT['td2']:,}/day")
print(f"    1-YEAR TIME CHARTER ...................... US${MKT['tc1yr_lo']:,}-{MKT['tc1yr_hi']:,}/day")
print(f"    DHT ACHIEVED spot leg, Q2 ................ US${ACT['DHT']['q2_spot']:,}/day")
print(f"    FRO ACHIEVED VLCC TCE, Q2 ................ US${ACT['FRO']['q2_vlcc_tce']:,}/day")
print(f"\n  ⚠️ The TD3C print is a PANEL ASSESSMENT of 'best achievable market value',")
print(f"     not an average of fixtures. Reported physical business is running at")
print(f"     roughly {MKT['fixture_lo']/MKT['td3c_assess']*100:.0f}-{MKT['fixture_hi']/MKT['td3c_assess']*100:.0f}% of the printed benchmark, because the Hormuz-")
print(f"     transit voyage has lost liquidity and cargo is moving by ship-to-ship")
print(f"     transfer outside the strait instead. DO NOT value a fleet off TD3C.")
hormuz = MKT["td3c_tce_11sep"] - MKT["td34_11sep"]
print(f"\n  THE CLEANEST OBSERVABLE RISK PRICE — same day, same destination:")
print(f"     TD3C (inside Hormuz)  US${MKT['td3c_tce_11sep']:,}/day")
print(f"     TD34 (outside Hormuz) US${MKT['td34_11sep']:,}/day")
print(f"     >> Hormuz transit premium = US${hormuz:,}/day "
      f"({hormuz/MKT['td34_11sep']*100:.0f}% of the non-transit rate)")
print(f"     This is the number that disappears if the strait normalises —")
print(f"     and it is observable daily, unlike any forecast.")

print(f"\n  WHAT THE COMPANIES ACTUALLY EARN vs THE BENCHMARK")
for t, ach in [("DHT", ACT["DHT"]["q2_spot"]), ("FRO", ACT["FRO"]["q2_vlcc_tce"])]:
    print(f"     {t} Q2 achieved US${ach:,}/day = "
          f"{ach/MKT['td3c_tce_11sep']*100:.0f}% of the TD3C TCE print")
print(f"     >> Neither company earns the headline. Valuation in section D below")
print(f"        therefore uses ACHIEVED TCE and the 1-year TC, never the benchmark.")

print(f"\n  ASSET VALUES (Signal Group, end-Aug 2026)")
print(f"    5-yr-old VLCC ........................... US${MKT['vlcc_5yr']}m")
print(f"    NEWBUILD ................................ US${MKT['vlcc_nb']}m")
print(f"    >> second-hand EXCEEDS newbuild by ...... {(MKT['vlcc_5yr']/MKT['vlcc_nb']-1)*100:.1f}%")
print(f"    20-yr-old VLCC .......................... US${MKT['vlcc_20yr']}m")
print(f"    scrap ................................... US${MKT['vlcc_scrap']}m")
print(f"    >> vintage tonnage at ................... {MKT['vlcc_20yr']/MKT['vlcc_scrap']:.1f}x scrap")
print(f"    YoY: +{MKT['yoy_5']:.0%} at 5yr, +{MKT['yoy_10']:.0%} at 10yr, "
      f"+{MKT['yoy_15']:.0%} at 15yr, +{MKT['yoy_20']:.0%} at 20yr")
print(f"    >> Appreciation RISES with age. That is a late-cycle signature:")
print(f"       buyers are paying for immediate earning capacity, not for life.")

print(f"\n  SUPPLY")
print(f"    VLCCs ordered in 2026 ................... {MKT['orders_2026_vlcc']}")
print(f"    crude tankers ordered in 2026 ........... {MKT['orders_2026_crude']}")
print(f"    orderbook, % of fleet by capacity ....... {MKT['orderbook_pct_capacity']:.0%}")
print(f"    tankers recycled 1H-2026 ................ {MKT['recycled_1h26']}")
print(f"    war-risk premium, % of hull ............. {MKT['warrisk_now']:.2%} "
      f"(pre-conflict {MKT['warrisk_pre']:.2%})")

# ══════════════════════════ PART 4: VALUATION ON ACTUALS ══════════════════════
print("\n" + "=" * 100)
print("D) VALUATION FROM OBSERVABLES — profit, PE, yield, P/B, P/NAV by rate")
print("=" * 100)
RATES = [30_000, 45_000, 60_000, 75_000, 93_000, 105_000, 126_700, 152_700, 200_000]
LBL = {30_000: "  <- mid-cycle benchmark", 93_000: "  <- 1yr TC low",
       105_000: "  <- 1yr TC high",
       126_700: "  <- DHT Q2 ACTUAL", 152_700: "  <- FRO Q2 ACTUAL"}
grid = []
for t, d in CO.items():
    print(f"\n  ── {t} ── price US${d['price']:.2f} · "
          f"P/B {d['price']/d['bvps']:.2f}x · P/NAV {d['price']/d['navps']:.2f}x")
    print(f"     {'TCE/day':>10}{'net income':>13}{'EPS':>8}{'P/E':>8}"
          f"{'DPS@100%':>10}{'yield':>8}")
    for r in RATES:
        ni, e = ni_at(d, r), eps_at(d, r)
        pe = d["price"] / e if e > 0 else np.nan
        y = max(e, 0) / d["price"] * 100
        print(f"     {r:>10,}{ni:>13,.0f}{e:>8.2f}"
              f"{(f'{pe:.1f}x' if e > 0 else '  n/m'):>8}{max(e,0):>10.2f}{y:>7.1f}%"
              + LBL.get(r, ""))
        grid.append(dict(ticker=t, tce=r, net_income_m=round(ni), eps=round(e, 2),
                         pe=round(pe, 1) if e > 0 else None,
                         dps_100pct=round(max(e, 0), 2), yield_pct=round(y, 1)))
pd.DataFrame(grid).to_csv(os.path.join(DATA, "s21_valuation_grid.csv"), index=False)
print("\n  Note: DPS shown at a 100% payout, which is what BOTH companies actually")
print("  did in Q2-2026 (DHT $1.22 on $1.22; FRO $2.61 on $2.61 adjusted).")

# what is priced in
print("\n  REVERSE TEST — what sustained TCE does today's price imply at a given PE?")
print(f"  {'':<6}" + "".join(f"{f'{p}x PE':>12}" for p in [3, 5, 7, 9]))
imp = []
for t, d in CO.items():
    cells = ""
    for pe in [3, 5, 7, 9]:
        need_eps = d["price"] / pe
        need_tce = (need_eps * d["shares"] + d["dna"]) / (d["vlcc_eq"] * d["days"] / 1e6) \
            + d["breakeven"]
        cells += f"{need_tce:>11,.0f} "
        imp.append(dict(ticker=t, pe=pe, implied_tce=round(need_tce)))
    print(f"  {t:<6}{cells}")
pd.DataFrame(imp).to_csv(os.path.join(DATA, "s21_implied_tce.csv"), index=False)
print(f"  >> Compare each cell with the 1-year TC market of "
      f"US${MKT['tc1yr_lo']:,}-{MKT['tc1yr_hi']:,}/day and with the Q2 actuals.")

# ══════════════════════════ PART 5: CYCLE POSITION SCORECARD ══════════════════
print("\n" + "=" * 100)
print("E) CYCLE-POSITION SCORECARD — numbers only, no narrative")
print("=" * 100)
# Mid-cycle benchmark: industry-standard normalised VLCC spot TCE is ~US$30k/day
# (range US$25-35k), per Signal Group TCE-benchmarking guidance and S&P Global.
# Published as a RANGE because it is a broker convention, not a measured series.
MIDCYCLE, MID_LO, MID_HI = 30_000, 25_000, 35_000

SCORE = [
    ("Achieved VLCC TCE vs mid-cycle", f"${ACT['FRO']['q2_vlcc_tce']:,}",
     f"{ACT['FRO']['q2_vlcc_tce']/MID_HI:.1f}-{ACT['FRO']['q2_vlcc_tce']/MID_LO:.1f}x", "LATE"),
    ("1-yr TC vs mid-cycle (~$30k)", f"${MKT['tc1yr_hi']:,}",
     f"{MKT['tc1yr_hi']/MID_HI:.1f}-{MKT['tc1yr_hi']/MID_LO:.1f}x", "MID"),
    ("Achieved TCE / 1-yr TC", f"{ACT['FRO']['q2_vlcc_tce']/MKT['tc1yr_hi']:.1f}x",
     "term mkt lags badly", "LATE"),
    ("Hormuz premium (TD3C-TD34)", f"${hormuz:,}/day",
     "zero if strait normalises", "EVENT-DRIVEN"),
    ("5-yr-old vs newbuild", f"{MKT['vlcc_5yr']/MKT['vlcc_nb']:.2f}x", ">1.0x only at peaks", "LATE"),
    ("20-yr-old vs scrap", f"{MKT['vlcc_20yr']/MKT['vlcc_scrap']:.1f}x", "normal ~1.2-1.5x", "LATE"),
    ("Value appreciation by age", f"+{MKT['yoy_20']:.0%} at 20yr vs +{MKT['yoy_5']:.0%} at 5yr", "inverted", "LATE"),
    ("VLCCs ordered in 2026", f"{MKT['orders_2026_vlcc']}", "vs ~2/yr scrapped 2025", "LATE"),
    ("Orderbook % of fleet", f"{MKT['orderbook_pct_capacity']:.0%}", "was 2% in 2023", "LATE"),
    ("P/NAV vs own record high", f"{px['DHT']/CO['DHT']['navps']:.2f}x / {px['FRO']/CO['FRO']['navps']:.2f}x",
     f"prior max {CO['DHT']['pnav_hi']:.2f}x / {CO['FRO']['pnav_hi']:.2f}x", "LATE"),
    ("P/E on Q2 annualised earnings", f"{px['DHT']/(ACT['DHT']['q2_eps']*4):.1f}x / "
     f"{px['FRO']/(ACT['FRO']['q2_adj_eps']*4):.1f}x", "peak zone 2.5-3.5x", "MID-LATE"),
    ("Deliveries 2027 / 2028", "~41-68 / ~125-127", "supply wall", "PRE-WALL"),
]
print(f"  {'indicator':<34}{'reading':<30}{'reference':<28}{'phase'}")
for a, b, c, p in SCORE:
    print(f"  {a:<34}{b:<30}{c:<28}{p}")
pd.DataFrame(SCORE, columns=["indicator", "reading", "reference", "phase"]
             ).to_csv(os.path.join(DATA, "s21_cycle_scorecard.csv"), index=False)
n_late = sum(1 for *_, p in SCORE if p == "LATE")
print(f"\n  ⚠️ DO NOT READ THIS AS '{n_late} OF {len(SCORE)} SAY LATE-CYCLE'.")
print("  These indicators are NOT independent. They are largely the same")
print("  freight shock measured repeatedly:")
print("     · achieved-TCE/mid-cycle and achieved-TCE/1-yr-TC share a numerator")
print("     · 5yr-vs-newbuild, 20yr-vs-scrap and age-appreciation all describe")
print("       one asset repricing")
print("     · 2026 orders and the orderbook percentage are the same fact twice")
print("  A tally of correlated measures is not a probability and cannot date a turn.")

print("\n  AND ONE OF THEM WAS OVER-INTERPRETED — the age-appreciation 'inversion':")
for age, now, yoy in [(5, MKT["vlcc_5yr"], MKT["yoy_5"]),
                      (20, MKT["vlcc_20yr"], MKT["yoy_20"])]:
    prior = now / (1 + yoy)
    print(f"     {age:>2}-yr-old: US${now:.1f}m now vs US${prior:.1f}m a year ago "
          f"= +US${now-prior:.1f}m  (+{yoy:.0%})")
print("  >> +90% and +30% are almost the SAME ABSOLUTE DOLLAR GAIN on different")
print("     bases. That is not independent proof of irrational vintage-asset")
print("     speculation, and the earlier draft overstated it. Downgraded.")
print("\n  The honest summary: freight, asset pricing, supply and equity multiples")
print("  are ALL elevated together, which is consistent with a late-cycle state.")
print("  Nothing here estimates WHEN it turns.")

# ══════════════════════════ F) RECONCILE §20 vs §21 ═══════════════════════════
print("\n" + "=" * 100)
print("F) RECONCILING SECTION 20 AND SECTION 21 — they disagree, and both are right")
print("=" * 100)
print("  Section 20 concluded: EXPENSIVE (targets below spot on a 1.0x-NAV exit).")
print("  Section 21's grid shows: CHEAP (P/E 6-7x and a 14-17% yield at the")
print("  1-year TC rate). These are not in conflict. They measure different things.\n")
print(f"  {'':<6}{'on ASSET value':>28}{'on CURRENT earnings':>28}")
for t, d in CO.items():
    e_tc = eps_at(d, MKT["tc1yr_hi"])
    p = d["price"]
    asset = f"P/NAV {p/d['navps']:.2f}x (record high)"
    earn = f"P/E {p/e_tc:.1f}x, yield {e_tc/p*100:.0f}%"
    print(f"  {t:<6}{asset:>28}{earn:>28}")
print("\n  >> The share price is HIGH against the steel and LOW against the cash.")
print("     Neither framing settles the question on its own. The only thing that")
print("     does is TOTAL RETURN: dividends received, plus whatever the equity is")
print("     worth afterwards. So compute it.\n")
print(f"  ONE-YEAR TOTAL RETURN at US${MKT['tc1yr_hi']:,}/day, exiting at TODAY'S NAV")
print("  (illustrative: it holds NAV flat, ignoring ageing, capex and debt change)")
print(f"  {'':<6}{'dividend':>10}{'exit NAV':>10}{'total':>9}{'price':>9}{'return':>9}")
tr = []
for t, d in CO.items():
    dps = max(eps_at(d, MKT["tc1yr_hi"]), 0)
    tot = dps + d["navps"]
    ret = (tot / d["price"] - 1) * 100
    print(f"  {t:<6}{dps:>10.2f}{d['navps']:>10.2f}{tot:>9.2f}{d['price']:>9.2f}"
          f"{ret:>8.1f}%")
    tr.append(dict(ticker=t, dividend=round(dps, 2), exit_nav=d["navps"],
                   total=round(tot, 2), price=d["price"], total_return_pct=round(ret, 1)))
pd.DataFrame(tr).to_csv(os.path.join(DATA, "s21_total_return.csv"), index=False)

print(f"\n  HOW LONG TO EARN BACK THE PREMIUM OVER NAV (undiscounted):")
print(f"  {'':<6}{'premium/share':>15}{'annual DPS':>12}{'years':>8}")
for t, d in CO.items():
    prem = d["price"] - d["navps"]
    dps = max(eps_at(d, MKT["tc1yr_hi"]), 0)
    print(f"  {t:<6}{prem:>15.2f}{dps:>12.2f}{prem/dps:>8.2f}")
print("  >> At the CURRENT 1-year TC rate, DHT needs ~2.3 years of dividends and")
print("     FRO ~3.5 years just to recover today's premium to asset value —")
print("     before any discounting, and before NAV erodes with ageing.")
print("  >> THAT is the decision. It is not 'cheap on P/E' versus 'dear on NAV'.")
print("     It is whether the rate holds long enough to earn back the premium.")

print(f"\n  ⚠️ PAYOUT — precise wording matters:")
print(f"     DHT paid ${ACT['DHT']['q2_dps']:.2f} against ORDINARY EPS "
      f"${ACT['DHT']['q2_eps']:.2f} (reported EPS was ${ACT['DHT']['q2_reported_eps']:.2f})")
print(f"     FRO paid ${ACT['FRO']['q2_dps']:.2f} = 100% of ADJUSTED EPS but only "
      f"{ACT['FRO']['q2_dps']/ACT['FRO']['q2_eps']*100:.1f}% of REPORTED EPS")
print(f"     FRO's extra ${ACT['FRO']['q2_special']:.2f} was announced SUBJECT TO completion")
print("     of vessel sales, so it is not an unconditional payment.")
print("  >> The yield grid is therefore a HYPOTHETICAL 100% payout of MODELLED")
print("     recurring EPS — not an assured forward yield.")

print("\nDone.")

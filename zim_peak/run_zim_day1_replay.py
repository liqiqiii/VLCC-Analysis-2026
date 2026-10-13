# -*- coding: utf-8 -*-
"""
Rule 12 / cyclical-rule replay for the ZIM March-2022 peak (Report #41 section 7).

Uses only primary figures from ZIM press releases (9-Mar-2022, 13-Mar-2024), the
gross-TR price series built by run_zim_peak_volume.py, SCFI weekly, and FRED CPI.

 CRule 1  two-cycle backtrack ZIM vs SCFI (2020-23 and 2023-25 Red Sea cycle):
          R^2 of monthly log levels, correlation of monthly log changes, lead/lag
 CRule 4  operating leverage: all-in cost per TEU, breakeven freight rate,
          profit multiplier table (FY2021 cost base, as known on 16-Mar-2022)
 CRule 7  FY(T+1) EPS sensitivity at five freight rates (as-of model) vs realized FY22/FY23
 CRule 2  PE path at the peak and after
 CRule 9  inflation adjustment of the peak (FRED CPIAUCSL)
 Module K/C valuation at the peak; realized 12-/24-month outcomes for the replay targets
"""
import io
import os
import sys
import json

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = {}

# ---------------- primary inputs (ZIM PR 9-Mar-2022 and PR 13-Mar-2024) ----------------
FY = {  # $M, K-TEU, $/TEU
    2020: dict(vol=2841, rate=1229, rev=3992, ebit=722, ni=524, eps=4.96),
    2021: dict(vol=3481, rate=2786, rev=10729, ebit=5816, ni=4649, eps=39.02, opex=3906, da=756, ga=268,
               ocf=5971, capex=1010, fcf=4877, adj_ebitda=6597, equity_owners=4592, net_cash=509, lease=2179 + 893),
    2022: dict(vol=3380, rate=3240, rev=12562, ebit=6136, adj_ebit=6145, ni=4629, eps=38.35, adj_ebitda=7541),
    2023: dict(vol=3281, rate=1203, rev=5162, ebit=-2511, adj_ebit=-422, ni=-2688, eps=-22.42, adj_ebitda=1049),
}
SHARES = 119_743_188 / 1e6  # 31-Dec-2021, PR footnote
P_PEAK = 88.62

# ---------------- CRule 4: operating leverage on the FY2021 cost base ----------------
f21 = FY[2021]
freight_rev = f21["vol"] * f21["rate"] / 1000.0  # $M
other_ratio = f21["rev"] / freight_rev - 1.0
cost_per_teu = (f21["rev"] - f21["ebit"]) / f21["vol"] * 1000.0  # all-in incl. D&A (IFRS16 charter hire sits in D&A + interest)
breakeven = cost_per_teu / (1 + other_ratio)
OUT["crule4"] = {"other_revenue_ratio_fy21": round(other_ratio, 3), "all_in_cost_per_teu_fy21": round(cost_per_teu),
                 "breakeven_freight_rate_fy21_cost_base": round(breakeven),
                 "q4_21_rate_vs_breakeven": round(3630 / breakeven, 2), "fy21_rate_vs_breakeven": round(f21["rate"] / breakeven, 2)}
for y in (2020, 2022, 2023):
    d = FY[y]
    e = d.get("adj_ebit", d["ebit"])
    c = (d["rev"] - e) / d["vol"] * 1000.0
    o = d["rev"] / (d["vol"] * d["rate"] / 1000.0) - 1
    OUT["crule4"][f"all_in_cost_per_teu_fy{y % 100}"] = round(c)
    OUT["crule4"][f"breakeven_fy{y % 100}"] = round(c / (1 + o))
lev = []
VOL, FIN, TAX = 3400, 157, 0.179  # FY21 net finance $157M, tax 17.9% (1,010/5,659)
for mult in (1.0, 1.5, 2.0, 2.5, 3.0):
    r = breakeven * mult
    ebit = VOL * (r * (1 + other_ratio) - cost_per_teu) / 1000.0
    ni = (ebit - FIN) * (1 - TAX) if ebit - FIN > 0 else ebit - FIN
    lev.append({"x_breakeven": mult, "rate": round(r), "ebit_$M": round(ebit), "net_income_$M": round(ni),
                "eps": round(ni / SHARES, 2), "ebit_margin": round(ebit / (VOL * r * (1 + other_ratio) / 1000.0), 3)})
OUT["crule4"]["table"] = lev

# ---------------- CRule 7: as-of sensitivity vs realized ----------------
sens = []
for r in (1200, 1800, 2400, 3000, 3630):
    ebit = VOL * (r * (1 + other_ratio) - cost_per_teu) / 1000.0
    ni = (ebit - FIN) * (1 - TAX) if ebit - FIN > 0 else ebit - FIN
    sens.append({"rate": r, "ebit_$M": round(ebit), "eps": round(ni / SHARES, 2), "pe_at_88.62": round(P_PEAK / (ni / SHARES), 1) if ni > 0 else None})
OUT["crule7_asof_sensitivity"] = sens
OUT["crule7_realized"] = {
    "FY22": {"rate": 3240, "model_ebit": round(3380 * (3240 * (1 + other_ratio) - cost_per_teu) / 1000), "actual_adj_ebit": 6145, "actual_eps": 38.35},
    "FY23": {"rate": 1203, "model_ebit": round(3281 * (1203 * (1 + other_ratio) - cost_per_teu) / 1000), "actual_adj_ebit": -422, "actual_eps": -22.42,
             "impairment_$M": 2060}}

# ---------------- price data ----------------
z = pd.read_csv(os.path.join(DATA, "zim_daily_yahoo.csv"), index_col=0, parse_dates=True)
px, tr = z["Close"], z["tr"]


def at(s, d):
    return float(s.loc[:d].iloc[-1])


# ---------------- Module K / C at the peak; CRule 2 PE path ----------------
mcap = P_PEAK * SHARES
ev = mcap - f21["net_cash"]  # ZIM net cash already nets lease liabilities
OUT["moduleK_C_at_peak"] = {
    "market_cap_$M": round(mcap), "ev_$M": round(ev),
    "pe_trailing_fy21": round(P_PEAK / 39.02, 2), "pe_on_realized_fy22": round(P_PEAK / 38.35, 2),
    "bv_per_share_dec21": round(f21["equity_owners"] / SHARES, 2), "pb": round(P_PEAK / (f21["equity_owners"] / SHARES), 2),
    "pb_pro_forma_after_17_div": round((P_PEAK - 17) / ((f21["equity_owners"] - 17 * SHARES) / SHARES), 2),
    "ev_ebitda_fy21": round(ev / f21["adj_ebitda"], 2), "ev_ebitda_fy22_guide_mid": round(ev / 7300, 2),
    "fcf_yield_fy21": round(f21["fcf"] / mcap, 3), "dividends_last_12m_incl_declared": 21.5,
    "dividend_yield_incl_declared": round(21.5 / P_PEAK, 3), "lease_liabilities_$M": f21["lease"],
}
pe_path = []
for d, eps, lab in [("2021-03-31", 4.96, "FY20 EPS"), ("2021-09-30", None, None), ("2022-03-16", 39.02, "FY21 EPS"),
                    ("2023-03-16", 38.35, "FY22 EPS"), ("2024-03-15", -22.42, "FY23 EPS")]:
    if eps is None:
        continue
    p = at(px, d)
    pe_path.append({"date": d, "price": round(p, 2), "trailing_eps": eps, "basis": lab, "pe": round(p / eps, 2) if eps > 0 else "n.m. (loss)"})
OUT["crule2_pe_path"] = pe_path

# ---------------- realized outcomes after the peak ----------------
divs = z.loc[z["Dividends"] > 0, "Dividends"]
out = {}
for months, d in [(12, "2023-03-16"), (24, "2024-03-15")]:
    rec = float(divs.loc["2022-03-17":d].sum())
    p = at(px, d)
    out[f"{months}m"] = {"date": d, "price": round(p, 2), "dividends_received": round(rec, 2),
                         "price_return": round(p / P_PEAK - 1, 3), "total_return_cash_divs": round((p + rec) / P_PEAK - 1, 3),
                         "gross_tr_return": round(at(tr, d) / at(tr, "2022-03-16") - 1, 3)}
OUT["realized_after_peak"] = out

# ---------------- CRule 9: inflation adjustment ----------------
cpi = pd.read_csv(os.path.join(DATA, "fred_cpiaucsl.csv"), parse_dates=["observation_date"]).set_index("observation_date")["CPIAUCSL"]
fac = float(cpi.iloc[-1] / cpi.loc["2022-03-01"])
OUT["crule9"] = {"cpi_mar22": float(cpi.loc["2022-03-01"]), "cpi_latest": [str(cpi.index[-1].date()), float(cpi.iloc[-1])],
                 "factor": round(fac, 4), "peak_close_real": round(P_PEAK * fac, 2), "intraday_peak_real": round(91.23 * fac, 2),
                 "mcap_real_$M": round(mcap * fac), "fy21_ni_real_$M": round(4649 * fac)}

# ---------------- CRule 1: two cycles ZIM vs SCFI ----------------
sc = pd.read_csv(os.path.join(DATA, "scfi_weekly_sourceB_bensontryit.csv"), parse_dates=["Week"]).set_index("Week")["SCFI"].sort_index()
scm = sc.resample("ME").last()
zm = pd.DataFrame({"px": px.resample("ME").last(), "tr": tr.resample("ME").last()})
cyc = {"cycle1_2021_02_to_2023_12": ("2021-02-28", "2023-12-31"), "cycle2_2023_10_to_2025_02": ("2023-10-31", "2025-02-28")}
rows = []
c1 = {}
for name, (a, b) in cyc.items():
    s = np.log(scm.loc[a:b])
    for conv in ("px", "tr"):
        y = np.log(zm[conv].loc[a:b])
        j = pd.concat([s, y], axis=1, keys=["scfi", "stk"]).dropna()
        r2 = float(np.corrcoef(j.scfi, j.stk)[0, 1] ** 2)
        dj = j.diff().dropna()
        ll = {}
        for k in range(-3, 4):
            # k>0: equity change at t vs SCFI change at t+k  (equity LEADS SCFI by k months)
            x = pd.concat([dj.stk, dj.scfi.shift(-k)], axis=1).dropna()
            ll[k] = round(float(np.corrcoef(x.iloc[:, 0], x.iloc[:, 1])[0, 1]), 3)
        best = max(ll, key=lambda k: ll[k])
        rows.append({"cycle": name, "convention": conv, "months": len(j), "r2_log_levels": round(r2, 3),
                     "corr_monthly_changes_k0": ll[0], "best_lag_k": best, "corr_at_best": ll[best], "lead_lag_profile": ll})
    seg = scm.loc[a:b]
    zp = zm["px"].loc[a:b]
    c1[name] = {"scfi_peak": [str(seg.idxmax().date()), float(seg.max())], "scfi_trough": [str(seg.idxmin().date()), float(seg.min())],
                "zim_monthly_close_peak": [str(zp.idxmax().date()), round(float(zp.max()), 2)],
                "zim_monthly_close_trough": [str(zp.idxmin().date()), round(float(zp.min()), 2)],
                "zim_peak_minus_scfi_peak_months": round((zp.idxmax() - seg.idxmax()).days / 30.44, 1)}
pd.DataFrame(rows).to_csv(os.path.join(DATA, "crule1_two_cycles.csv"), index=False)
OUT["crule1"] = {"stats": rows, "anatomy": c1}
# daily peaks for cycle 2 (more precise than month-end)
OUT["crule1"]["cycle2_daily"] = {"zim_price_peak": [str(px.loc["2023-10-01":"2025-03-31"].idxmax().date()), round(float(px.loc["2023-10-01":"2025-03-31"].max()), 2)],
                                 "zim_tr_peak": str(tr.loc["2023-10-01":"2025-03-31"].idxmax().date()),
                                 "scfi_weekly_peak": [str(sc.loc["2023-10-01":"2025-03-31"].idxmax().date()), float(sc.loc["2023-10-01":"2025-03-31"].max())]}

# ---------------- round-3 review additions ----------------
R3 = {}
# shares of other revenue: vs freight revenue and vs total revenue
R3["other_revenue_share"] = {}
for y in (2021, 2022, 2023):
    d = FY[y]
    fr = d["vol"] * d["rate"] / 1000.0
    R3["other_revenue_share"][y] = {"of_freight": round(d["rev"] / fr - 1, 4), "of_total": round(1 - fr / d["rev"], 4)}
# pretax breakeven on FY21 base (EBIT must cover net finance)
R3["pretax_breakeven_fy21"] = round((cost_per_teu + FIN / VOL * 1000.0) / (1 + other_ratio))
# alternative: residual (non-freight) revenue held constant PER TEU instead of proportional to freight rate
R3["ebit_breakeven_residual_const_per_teu"] = {}
for y in (2021, 2022, 2023):
    d = FY[y]
    e = d.get("adj_ebit", d["ebit"])
    fr = d["vol"] * d["rate"] / 1000.0
    resid_per_teu = (d["rev"] - fr) / d["vol"] * 1000.0
    c = (d["rev"] - e) / d["vol"] * 1000.0
    R3["ebit_breakeven_residual_const_per_teu"][y] = round(c - resid_per_teu)
# forecast-error bridge: actual minus FY21-base model (residual revenue and net operating cost)
R3["error_bridge"] = {}
for y in (2022, 2023):
    d = FY[y]
    e = d.get("adj_ebit", d["ebit"])
    fr = d["vol"] * d["rate"] / 1000.0
    model_resid = fr * other_ratio
    model_cost = d["vol"] * cost_per_teu / 1000.0
    act_resid = d["rev"] - fr
    act_cost = d["rev"] - e
    R3["error_bridge"][y] = {"extra_residual_revenue": round(act_resid - model_resid), "extra_net_operating_cost": round(-(act_cost - model_cost)),
                             "net_ebit_difference": round((act_resid - model_resid) - (act_cost - model_cost))}
# FY21 FCF per ZIM reconciliation, and cash after financing outflows
R3["fcf_bridge_fy21_$M"] = {"ocf": 5971, "capex_net_per_reconciliation": -1094, "fcf_reported": 4877,
                            "repayment_borrowings_and_leases_combined": -1191.3, "change_short_term_loans": -16.0, "interest_paid": -160.0,
                            "residual_after_displayed_principal_and_interest": round(4877 - 1191.3 - 16.0 - 160.0, 1),
                            "residual_yield": round((4877 - 1191.3 - 16.0 - 160.0) / mcap, 3)}
# PE on 9-Mar (same FY21 EPS)
R3["pe_on_2022_03_09"] = round(at(px, "2022-03-09") / 39.02, 2)
# calendar-2022 vs peak-to-year-end
R3["price_2022_calendar"] = round(at(px, "2022-12-30") / at(px, "2021-12-31") - 1, 3)
R3["price_peak_to_2022_end"] = round(at(px, "2022-12-30") / P_PEAK - 1, 3)
# SCFI as published by the 16-Mar cutoff
pub = sc.loc[:"2022-03-16"]
seqc = pub.loc["2022-01-07":].diff().dropna()
R3["scfi_at_cutoff"] = {"last_print": [str(pub.index[-1].date()), float(pub.iloc[-1])],
                        "vs_peak": round(float(pub.iloc[-1] / 5109.6 - 1), 4), "consecutive_declines": int((seqc < 0).sum())}
# peak lags in weeks (daily), price and gross TR
R3["peak_lag_weeks"] = {
    "cycle1_price": round((pd.Timestamp("2022-03-16") - pd.Timestamp("2022-01-07")).days / 7, 2),
    "cycle1_tr": round((pd.Timestamp("2022-03-22") - pd.Timestamp("2022-01-07")).days / 7, 2),
    "cycle2_price": round((pd.Timestamp("2024-11-20") - pd.Timestamp("2024-07-05")).days / 7, 2),
    "cycle2_tr": round((pd.Timestamp(OUT["crule1"]["cycle2_daily"]["zim_tr_peak"]) - pd.Timestamp("2024-07-05")).days / 7, 2)}
# CRule 9 for cycle 2 peak
fac2 = float(cpi.iloc[-1] / cpi.loc["2024-11-01"])
R3["crule9_cycle2"] = {"factor_nov24": round(fac2, 4), "peak_27.01_real": round(27.01 * fac2, 2)}
OUT["review_round3"] = R3

with open(os.path.join(DATA, "day1_replay.json"), "w", encoding="utf-8") as fh:
    json.dump(OUT, fh, indent=1, default=str)
print(json.dumps(OUT, indent=1, default=str))

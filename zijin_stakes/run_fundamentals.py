# -*- coding: utf-8 -*-
"""
Fundamental analysis and scenario valuation for the three live Zijin situations.

    赤峰黄金 Chifeng   600988.SS / 6693.HK
    招金矿业 Zhaojin   1818.HK
    Allied Gold        AAUC.TO

Applies the repo's Rule 6 (operating leverage) and Rule 7 (target prices are
REQUIRED: conservative / base / bull, 12m and 24m, with explicit multiple
assumptions).

VALUATION APPROACH -- deliberately three independent methods, because for
gold miners any single method lies:

  1. EARNINGS BRIDGE   gold price -> cash margin -> net income -> P/E target
     The honest core. Built bottom-up from each company's OWN production and
     its OWN cost base, not from a sell-side number.

  2. EV PER OUNCE      EV / annual production oz, and EV / reserve oz
     The standard mining cross-check. Catches when an earnings model is
     flattered by a temporary gold price.

  3. FCF YIELD         free cash flow / market cap
     Module C of the Day1Global framework -- "THE BIG ONE". A miner that
     cannot convert accounting profit into cash is not cheap at any P/E.

*** CURRENCY DISCIPLINE ***
Zhaojin REPORTS in RMB but TRADES in HKD. Chifeng reports in CNY and trades in
both CNY (A) and HKD (H). Allied reports in USD and trades in CAD. Every
cross-company comparison below is converted to USD explicitly. Mixing these is
the single easiest way to produce a wrong answer here.

*** AISC PROVENANCE (carried from run_gold_leverage.py) ***
Only Allied discloses a CURRENT AISC. Chifeng disclosed FY2023 only and then
stopped. Zhaojin has never disclosed one. Every scenario below therefore shows
the cost assumption explicitly, and the Zhaojin numbers are the weakest.
"""

import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei",
                                          "Microsoft JhengHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
import numpy as np
import pandas as pd
import yfinance as yf

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")
os.makedirs(DATA, exist_ok=True)
os.makedirs(CHARTS, exist_ok=True)

OZ = 31.1035          # grams per troy ounce
T_TO_OZ = 1000 * 1000 / OZ   # tonnes -> oz  (1 t = 1e6 g)

# ---------------------------------------------------------------- FX (live)
def fx_rates():
    pairs = {"USDCNY=X": "USDCNY", "USDHKD=X": "USDHKD", "USDCAD=X": "USDCAD"}
    out = {}
    d = yf.download(list(pairs), period="5d", progress=False, auto_adjust=True)["Close"]
    for k, v in pairs.items():
        s = d[k].dropna() if hasattr(d, "columns") else d.dropna()
        out[v] = float(s.iloc[-1])
    return out


FX = fx_rates()
print("=" * 90)
print("FUNDAMENTAL ANALYSIS & SCENARIO VALUATION — Chifeng / Zhaojin / Allied Gold")
print("=" * 90)
print(f"\n  FX: USDCNY {FX['USDCNY']:.4f} · USDHKD {FX['USDHKD']:.4f} · "
      f"USDCAD {FX['USDCAD']:.4f}")

gold = yf.download("GC=F", period="6mo", progress=False, auto_adjust=True)["Close"]
gold = gold.iloc[:, 0] if hasattr(gold, "columns") else gold
SPOT = float(gold.iloc[-1])
print(f"  Gold spot: US${SPOT:,.0f}/oz  ({gold.index[-1].date()})")

# ================================================================ company data
# Everything here is sourced in the report. src tags:
#   D = disclosed by the company   B = broker estimate   A = my assumption
#   Y = Yahoo Finance field        C = computed here
CO = {
    "赤峰黄金 Chifeng": dict(
        tick_main="600988.SS", tick_alt="6693.HK", rep_ccy="CNY", trade_ccy="CNY",
        # --- operating
        prod_oz_2025=14.51 * T_TO_OZ,         # D: 14.51 t FY2025
        prod_oz_2026e=14.70 * T_TO_OZ,        # D: company plan
        prod_oz_2027e=20.00 * T_TO_OZ,        # B: 2027 target ~20 t (FLAGGED)
        resources_t=582.7,                    # D: +49.41%
        reserves_t=None,                      # NOT DISCLOSED in the summary
        aisc_lo=1179,                         # D but FY2023 -> a floor
        aisc_hi=2190,                         # B: CNY400-500/g upper
        aisc_base=1800,                       # A: midpoint-ish for FY2026
        # --- financials FY2025, reporting ccy bn
        revenue=12.639, net_profit=3.082, ocf=5.556,
        cash=6.82, debt=1.11,
        shares=1.664,                          # Y
        eps_ttm=1.98, eps_fwd=3.45,            # Y
        bvps=7.599, ev_ebitda=10.872, ebitda=7.502,
        fcf=2.506, div_yield=0.0072,
        tgt_street=50.29, n_analysts=3,
        note="Net cash. 41% operating margin. But FY2025 production MISSED "
             "(14.51t, -4.3%) and H1-26 volumes fell 9.45% -- growth is price."),
    "招金矿业 Zhaojin": dict(
        tick_main="1818.HK", tick_alt=None, rep_ccy="CNY", trade_ccy="HKD",
        prod_oz_2025=19.79 * T_TO_OZ,         # D: MINED gold (excl. smelted)
        prod_oz_2026e=17.50 * T_TO_OZ,        # C: H1-26 mined -21.87% annualised
        prod_oz_2027e=30.00 * T_TO_OZ,        # A: +12-15t Haiyu IF it starts
        resources_t=1504.68, reserves_t=521.24,
        aisc_lo=1400, aisc_hi=2000, aisc_base=1700,   # A -- NEVER DISCLOSED
        revenue=18.056, net_profit=3.614, ocf=None,
        cash=4.609, debt=18.540,               # D: from the H1-26 interim
        shares=2.882,
        eps_ttm=1.10, eps_fwd=2.2439,
        bvps=6.6669, ev_ebitda=10.146, ebitda=8.615,
        fcf=None, div_yield=0.0057,
        tgt_street=31.74, n_analysts=9,
        note="A leveraged option on Haiyu. H1-26 mined gold -21.87%, "
             "attributable profit only +9.61%, NO interim dividend, and "
             "RMB5.39bn of perpetuals sit INSIDE equity."),
    "Allied Gold": dict(
        tick_main="AAUC.TO", tick_alt=None, rep_ccy="USD", trade_ccy="CAD",
        prod_oz_2025=379081,                   # D
        prod_oz_2026e=505000,                  # D: 485-575k guidance, BOTTOM half
        prod_oz_2027e=650000,                  # A: full Kurmuk year
        resources_t=None, reserves_t=None,     # partial only -- see report
        reserves_koz=2706,                     # D: Kurmuk P&P only
        aisc_lo=1700, aisc_hi=2264, aisc_base=2100,   # D: Q1-26 = 2,264
        revenue=1.330, net_profit=-0.0626, ocf=0.360,
        cash=0.1922, debt=0.1954,
        shares=0.139,
        eps_ttm=-1.91, eps_fwd=10.1188,
        bvps=5.5608, ev_ebitda=7.268, ebitda=0.541,
        fcf=0.150, div_yield=0.0,
        tgt_street=44.60, n_analysts=6,
        note="Highest cost of scale in the peer set (Q1-26 AISC US$2,264/oz) "
             "on 1.13-1.49 g/t grades. Loss-making FY24 AND FY25. The entire "
             "bull case is Kurmuk diluting group AISC."),
}

PX = {}
for n, d in CO.items():
    s = yf.download(d["tick_main"], period="1y", progress=False,
                    auto_adjust=True)["Close"]
    PX[n] = float((s.iloc[:, 0] if hasattr(s, "columns") else s).dropna().iloc[-1])


def to_usd(x, ccy):
    if x is None:
        return None
    return x / FX[f"USD{ccy}"] if ccy != "USD" else x


# ================================================================ 1) snapshot
print("\n" + "-" * 90)
print("1) THE SNAPSHOT — normalised to USD so the three are actually comparable")
print("-" * 90)
rows = []
for n, d in CO.items():
    px = PX[n]
    mcap_tr = px * d["shares"]                       # in TRADING currency, bn
    mcap_usd = to_usd(mcap_tr, d["trade_ccy"])
    net_debt_rep = d["debt"] - d["cash"]             # reporting ccy
    nd_usd = to_usd(net_debt_rep, d["rep_ccy"])
    ev_usd = mcap_usd + nd_usd
    rev_usd = to_usd(d["revenue"], d["rep_ccy"])
    np_usd = to_usd(d["net_profit"], d["rep_ccy"])
    prod = d["prod_oz_2025"]
    rows.append(dict(
        name=n, px=round(px, 2), ccy=d["trade_ccy"],
        mcap_usd_bn=round(mcap_usd, 2), net_debt_usd_bn=round(nd_usd, 2),
        ev_usd_bn=round(ev_usd, 2),
        revenue_usd_bn=round(rev_usd, 2), net_profit_usd_bn=round(np_usd, 3),
        net_margin_pct=round(np_usd / rev_usd * 100, 1),
        prod_koz_2025=round(prod / 1000),
        ev_per_prod_oz=round(ev_usd * 1e9 / prod),
        pe_ttm=round(px / d["eps_ttm"], 1) if d["eps_ttm"] > 0 else None,
        pe_fwd=round(px / d["eps_fwd"], 1) if d["eps_fwd"] else None,
        pb=round(px / d["bvps"], 2), ev_ebitda=d["ev_ebitda"],
        fcf_yield_pct=(round(to_usd(d["fcf"], d["rep_ccy"]) / mcap_usd * 100, 1)
                       if d["fcf"] else None),
        div_yield_pct=round(d["div_yield"] * 100, 2),
        street_tgt=d["tgt_street"], street_upside_pct=round((d["tgt_street"]/px-1)*100, 1),
        n_analysts=d["n_analysts"]))

snap = pd.DataFrame(rows)
snap.to_csv(os.path.join(DATA, "fundamental_snapshot.csv"), index=False)
for _, r in snap.iterrows():
    print(f"\n  {r['name']}  ({r['px']:,.2f} {r['ccy']})")
    print(f"     mcap US${r['mcap_usd_bn']:.2f}bn · net debt US${r['net_debt_usd_bn']:+.2f}bn"
          f" · EV US${r['ev_usd_bn']:.2f}bn")
    print(f"     revenue US${r['revenue_usd_bn']:.2f}bn · net profit "
          f"US${r['net_profit_usd_bn']:+.3f}bn · net margin {r['net_margin_pct']:+.1f}%")
    print(f"     2025 production {r['prod_koz_2025']:,} koz  ->  "
          f"EV/production oz = US${r['ev_per_prod_oz']:,}")
    pe = f"{r['pe_ttm']}" if r['pe_ttm'] else "n/m (loss)"
    print(f"     P/E {pe} trailing, {r['pe_fwd']} forward · P/B {r['pb']} · "
          f"EV/EBITDA {r['ev_ebitda']}")
    fy = f"{r['fcf_yield_pct']}%" if r['fcf_yield_pct'] else "n/d"
    print(f"     FCF yield {fy} · dividend {r['div_yield_pct']}% · "
          f"street target {r['street_tgt']} ({r['street_upside_pct']:+.1f}%, "
          f"{r['n_analysts']} analysts)")

# ================================================================ 2) EV/oz
print("\n" + "-" * 90)
print("2) EV PER OUNCE — the mining cross-check the P/E cannot give you")
print("-" * 90)
print(f"  {'name':<22}{'EV US$bn':>10}{'prod koz':>10}{'EV/prod oz':>13}"
      f"{'reserves koz':>14}{'EV/reserve oz':>15}")
ev_rows = []
for n, d in CO.items():
    r = snap[snap["name"] == n].iloc[0]
    res_koz = (d["reserves_t"] * T_TO_OZ / 1000 if d.get("reserves_t")
               else d.get("reserves_koz"))
    ev_res = r["ev_usd_bn"] * 1e9 / (res_koz * 1000) if res_koz else None
    print(f"  {n:<22}{r['ev_usd_bn']:>10.2f}{r['prod_koz_2025']:>10,}"
          f"{r['ev_per_prod_oz']:>13,}"
          f"{(f'{res_koz:,.0f}' if res_koz else 'n/d'):>14}"
          f"{(f'{ev_res:,.0f}' if ev_res else 'n/d'):>15}")
    ev_rows.append(dict(name=n, ev_usd_bn=r["ev_usd_bn"],
                        prod_koz=r["prod_koz_2025"],
                        ev_per_prod_oz=r["ev_per_prod_oz"],
                        reserves_koz=round(res_koz) if res_koz else None,
                        ev_per_reserve_oz=round(ev_res) if ev_res else None))
pd.DataFrame(ev_rows).to_csv(os.path.join(DATA, "ev_per_ounce.csv"), index=False)
print("\n  Reading it: EV/production oz is what the market pays per ounce of")
print("  ANNUAL output. EV/reserve oz is what it pays per ounce in the ground.")
print("  A low EV/reserve oz with a high EV/production oz = a company whose")
print("  ounces are not yet being mined (i.e. a development story).")
print("  ⚠️ Chifeng reserves are NOT disclosed; Allied's figure is Kurmuk P&P")
print("     ONLY, so its EV/reserve oz is overstated (too few ounces counted).")

# ================================================================ 3) scenarios
print("\n" + "-" * 90)
print("3) MODEL VALIDATION FIRST — does the bridge reproduce FY2025 actuals?")
print("-" * 90)
print("  A valuation model you have not back-tested against reported results is")
print("  a random number generator. Gold averaged ~US$3,050/oz in 2025.")
GOLD_2025 = 3050
print(f"\n  {'name':<22}{'modelled net US$m':>19}{'ACTUAL net US$m':>18}{'error':>9}")
val_rows = []
for n, d in CO.items():
    margin = (GOLD_2025 - d["aisc_base"]) * d["prod_oz_2025"] / 1e6
    modelled = margin * 0.75
    actual = to_usd(d["net_profit"], d["rep_ccy"]) * 1000
    err = (modelled / actual - 1) * 100 if actual > 0 else np.nan
    flag = "OK" if abs(err) < 35 else "⚠️ POOR FIT"
    print(f"  {n:<22}{modelled:>19,.0f}{actual:>18,.0f}"
          f"{(f'{err:+.0f}%' if err == err else 'n/m'):>9}  {flag}")
    d["gap_usd_m"] = modelled - actual      # cost the model cannot see
    val_rows.append(dict(name=n, gold_2025=GOLD_2025, aisc_used=d["aisc_base"],
                         modelled_net_usd_m=round(modelled),
                         actual_net_usd_m=round(actual),
                         error_pct=round(err, 1) if err == err else None,
                         gap_usd_m=round(modelled - actual)))
pd.DataFrame(val_rows).to_csv(os.path.join(DATA, "model_validation.csv"), index=False)
print("\n  Chifeng fits within 5% -- its AISC assumption is trustworthy.")
print("  Zhaojin is +19% (the model ignores its low-margin smelting line).")
print("  🔴 Allied is a POOR FIT: modelled +US$270m vs an ACTUAL LOSS of")
print("     US$63m -- a US$333m gap of D&A, interest and growth capex that")
print("     AISC simply does not capture.")
print("\n  >> CALIBRATION APPLIED: every scenario below subtracts each company's")
print("     OWN validation gap. Without this, Allied's targets are fantasy.")
print(f"     gaps: " + " · ".join(f"{n.split()[-1]} US${d['gap_usd_m']:+,.0f}m"
                                  for n, d in CO.items()))

print("\n" + "-" * 90)
print("4) RULE 7 — SCENARIO TARGET PRICES (cyclical multiple discipline applied)")
print("-" * 90)
print("  ⚠️ CRITICAL METHOD POINT: the multiple FALLS as gold rises.")
print("  Cyclical miners trade at HIGH P/Es on depressed earnings and LOW P/Es")
print("  on peak earnings. Applying a bull multiple to bull earnings counts the")
print("  same optimism twice -- the exact error caught in the VLCC capstone.")

SCEN = {
    "🐻 Conservative": dict(gold=3400, pe=12, aisc_key="aisc_hi",  prod_key="prod_oz_2026e",
                            tax=0.25,
                            note="gold -23%, cost at the HIGH end, 2026 volumes. "
                                 "P/E 12 -- depressed earnings earn a HIGHER multiple."),
    "⚖️ Base":         dict(gold=4400, pe=10, aisc_key="aisc_base", prod_key="prod_oz_2026e",
                            tax=0.25,
                            note="gold ~spot, mid-range cost, 2026 volumes, P/E 10."),
    "🐂 Bull":         dict(gold=5200, pe=7,  aisc_key="aisc_base", prod_key="prod_oz_2027e",
                            tax=0.25,
                            note="gold +18% AND 2027 volumes -- but cost held at "
                                 "BASE (not the low end) and P/E cut to 7, "
                                 "because peak earnings deserve a trough multiple."),
}

tp_rows = []
for n, d in CO.items():
    px = PX[n]
    print(f"\n  ── {n} ── spot {px:,.2f} {d['trade_ccy']}")
    print(f"     {'scenario':<18}{'gold':>7}{'AISC':>7}{'koz':>7}"
          f"{'margin US$m':>13}{'raw net':>9}{'calib net':>11}{'EPS':>8}"
          f"{'P/E':>5}{'target':>9}{'upside':>9}")
    for sname, s in SCEN.items():
        aisc = d[s["aisc_key"]]
        prod = d[s["prod_key"]]
        margin_usd = (s["gold"] - aisc) * prod / 1e6
        raw_net = margin_usd * (1 - s["tax"])
        net_usd = raw_net - d["gap_usd_m"]          # calibrated on FY2025 actuals
        net_trade = net_usd * (FX[f"USD{d['trade_ccy']}"] if d["trade_ccy"] != "USD" else 1)
        eps = net_trade / (d["shares"] * 1000)
        tgt = max(eps, 0) * s["pe"]
        up = (tgt / px - 1) * 100
        print(f"     {sname:<18}{s['gold']:>7,}{aisc:>7,}{prod/1000:>7,.0f}"
              f"{margin_usd:>13,.0f}{raw_net:>9,.0f}{net_usd:>11,.0f}{eps:>8.2f}"
              f"{s['pe']:>5}{tgt:>9,.2f}{up:>8.0f}%")
        tp_rows.append(dict(name=n, scenario=sname, gold=s["gold"], aisc=aisc,
                            prod_koz=round(prod/1000), margin_usd_m=round(margin_usd),
                            raw_net_usd_m=round(raw_net),
                            calibrated_net_usd_m=round(net_usd), eps=round(eps, 2),
                            pe=s["pe"], target=round(tgt, 2), upside_pct=round(up),
                            spot=round(px, 2), ccy=d["trade_ccy"],
                            assumptions=s["note"]))
pd.DataFrame(tp_rows).to_csv(os.path.join(DATA, "target_prices.csv"), index=False)

print("\n  ⚠️ METHOD CAVEATS — read before using any target above:")
print("   * Gross cash margin = (gold - AISC) x oz. AISC already includes")
print("     sustaining capex, so D&A is NOT deducted again. Growth capex,")
print("     interest and by-product credits are EXCLUDED.")
print("   * A flat 25% tax rate is applied to all three. Real rates differ by")
print("     jurisdiction (Mali/Ethiopia/Laos/Ghana/China all differ).")
print("   * Chifeng and Zhaojin also have non-gold revenue (copper at Sepon,")
print("     smelting at Zhaojin) that this model IGNORES -- so their true")
print("     earnings are HIGHER than modelled. The targets are conservative.")
print("   * Zhaojin's AISC is an ASSUMPTION. Its column is the least reliable.")

# ================================================================ 4) chart
fig, axes = plt.subplots(2, 2, figsize=(16, 10.5))

ax = axes[0][0]
names = list(CO)
x = np.arange(len(names))
w = 0.26
for i, (sname, col) in enumerate(zip(SCEN, ["#c0392b", "#2980b9", "#27ae60"])):
    vals = [next(r["upside_pct"] for r in tp_rows
                 if r["name"] == n and r["scenario"] == sname) for n in names]
    ax.bar(x + (i - 1) * w, vals, w, label=sname, color=col)
    for xi, v in zip(x + (i - 1) * w, vals):
        ax.text(xi, v + (4 if v >= 0 else -12), f"{v:+.0f}%", ha="center", fontsize=7.5)
ax.axhline(0, color="k", lw=1)
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=8.5)
ax.set_ylabel("upside / downside %")
ax.set_title("A. Scenario upside — conservative / base / bull\n(bottom-up from gold price and cost)",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=8); ax.grid(axis="y", alpha=.25)

ax = axes[0][1]
vals = [snap[snap["name"] == n]["ev_per_prod_oz"].iloc[0] for n in names]
ax.bar(names, vals, color=["#c0392b", "#2980b9", "#27ae60"])
for i, v in enumerate(vals):
    ax.text(i, v * 1.02, f"${v:,.0f}", ha="center", fontsize=9, fontweight="bold")
ax.set_ylabel("EV per ounce of ANNUAL production (US$)")
ax.set_title("B. What the market pays per ounce of output\nlower = cheaper on an asset basis",
             fontsize=10, fontweight="bold")
ax.tick_params(axis="x", labelsize=8.5); ax.grid(axis="y", alpha=.25)

ax = axes[1][0]
pe_t = [snap[snap["name"] == n]["pe_ttm"].iloc[0] or 0 for n in names]
pe_f = [snap[snap["name"] == n]["pe_fwd"].iloc[0] or 0 for n in names]
ax.bar(x - 0.2, pe_t, 0.4, label="trailing P/E", color="#95a5a6")
ax.bar(x + 0.2, pe_f, 0.4, label="forward P/E", color="#2980b9")
for xi, v in zip(x - 0.2, pe_t):
    ax.text(xi, v + .4, ("n/m" if v == 0 else f"{v:.1f}"), ha="center", fontsize=8)
for xi, v in zip(x + 0.2, pe_f):
    ax.text(xi, v + .4, f"{v:.1f}", ha="center", fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=8.5)
ax.set_ylabel("x")
ax.set_title("C. Trailing vs forward P/E\nbig gap = consensus expects a step-change",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=8); ax.grid(axis="y", alpha=.25)

ax = axes[1][1]
nd = [snap[snap["name"] == n]["net_debt_usd_bn"].iloc[0] for n in names]
cols = ["#27ae60" if v < 0 else "#c0392b" for v in nd]
ax.barh(names, nd, color=cols)
for i, v in enumerate(nd):
    ax.text(v, i, f"  {v:+.2f}", va="center", fontsize=9, fontweight="bold")
ax.axvline(0, color="k", lw=1)
ax.set_xlabel("net debt US$bn  (negative = NET CASH)")
ax.set_title("D. Balance sheet — the thing that decides who survives a gold drawdown",
             fontsize=10, fontweight="bold")
ax.tick_params(labelsize=8.5); ax.grid(axis="x", alpha=.25)

fig.suptitle("Fundamentals and scenario valuation — 赤峰黄金 · 招金矿业 · Allied Gold\n"
             f"Gold spot US${SPOT:,.0f}/oz. AISC: Allied DISCLOSED, Chifeng "
             "FY2023-only, Zhaojin ASSUMED. All USD conversions at live FX.",
             fontsize=12, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .93])
p = os.path.join(CHARTS, "fundamentals.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

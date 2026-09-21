# -*- coding: utf-8 -*-
"""
FINAL SYNTHESIS v3 — rebuilt after the GPT-6-Astra adversarial review (Rule 4b).

Astra raised four BLOCKING findings against v2. Each is handled here:

 [B1] "Cash breakeven includes loan principal, so subtracting it AND D&A does
      not produce accounting EPS."
      -> ANSWERED WITH EVIDENCE, not assertion. Section 0 below back-solves the
         TC rate that the model needs in order to reproduce each company's
         ACTUAL reported trailing EPS. If the specification were wrong by the
         amount Astra fears, the implied rate would be absurd. It is not.
         The objection is logged, the calibration is published, the reader
         judges.

 [B2] "The NAV roll-forward charges ageing against EQUITY NAV, not fleet value."
      -> CONFIRMED BUG. v2 wrote nav*(1-drag) where nav was NAV per share.
         Fleet value and net debt are now modelled SEPARATELY. Ageing hits the
         fleet only. Cash accretion is not aged.
      -> Also confirmed: adding retained ACCOUNTING earnings while ageing the
         fleet is only valid if maintenance capex = D&A. That is now an
         explicit, stated, sensitivity-tested assumption.

 [B3] "A trailing 77% payout is not a forward policy; DHT states 100% of
      ordinary net income."
      -> CONFIRMED. Both policies are now run side by side.

 [B4] "Net-debt-to-fleet of 8%/18% does not reconcile to your own inputs, and
      the 2008 '88%' is arithmetically impossible."
      -> CONFIRMED BOTH. Recomputed from the inputs, and the 2008 figure is
         back-solved from the identity rather than asserted.

 [M5/M6] "Mid-cycle TC is an unused parameter" and "you normalise the equity
      multiple but not vessel prices."
      -> CONFIRMED. v2's mid-cycle rate genuinely did nothing (its own
         sensitivity printed a 0% swing). Vessel values are now REPRICED with
         the rate scenario, which makes the reversion assumption live and
         removes the one-sided conservatism.
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

CO = {
    "DHT": dict(vlcc_eq=24.0, days=350, breakeven=17_500, dna=105,
                shares=161.236, navps=14.33, bvps=8.26, net_debt=273.1,
                fleet_mv=2583.0, payout=0.77, policy_payout=1.00,
                ttm_eps=2.94, ttm_dps=2.27, pnav_hi=1.36, pnav_lo=0.87),
    "FRO": dict(vlcc_eq=57.9, days=350, breakeven=23_800, dna=300,
                shares=222.623, navps=30.37, bvps=14.15, net_debt=2113.4,
                fleet_mv=8875.0, payout=0.90, policy_payout=0.90,
                ttm_eps=6.67, ttm_dps=5.99, pnav_hi=1.50, pnav_lo=1.14),
}
COE, AGE_DRAG = 0.10, 0.05

# Vessel values are now REPRICED with the rate scenario (Astra M6).
SCEN = {
    "Bear": dict(tc=70_000,  yrs=1, reprice=-0.25,
                 note="Hormuz normalises inside a year; asset values follow"),
    "Base": dict(tc=95_000,  yrs=2, reprice=-0.15,
                 note="rate holds at the LOW end of today's market, then reverts"),
    "Bull": dict(tc=120_000, yrs=3, reprice=0.00,
                 note="premium persists and re-rates; values hold"),
}

print("=" * 100)
print("FINAL SYNTHESIS v3 — rebuilt after the Astra review")
print("=" * 100)
for t in CO:
    s = yf.download(t, period="1mo", progress=False, auto_adjust=False)["Close"]
    CO[t]["price"] = float((s.iloc[:, 0] if hasattr(s, "columns") else s).dropna().iloc[-1])
print("\n  Spot: " + " · ".join(f"{t} US${CO[t]['price']:.2f}" for t in CO))


def eps_at(d, tc):
    return ((tc - d["breakeven"]) * d["vlcc_eq"] * d["days"] / 1e6 - d["dna"]) / d["shares"]


# ===================================================== 0) CALIBRATION vs [B1]
print("\n" + "-" * 100)
print("0) CALIBRATION — does the earnings spec reproduce REPORTED results?")
print("-" * 100)
print("  Astra [B1]: the disclosed cash breakeven may already include loan")
print("  principal, so subtracting it AND D&A would not give accounting EPS.")
print("  Test: back-solve the TC rate the model needs to hit ACTUAL trailing EPS.")
print("  If the spec double-counted debt service, the implied rate would have to")
print("  be implausibly HIGH to compensate.\n")
print(f"  {'':<6}{'actual TTM EPS':>16}{'implied TC':>13}{'actual DPS':>12}"
      f"{'implied payout':>16}{'verdict':>12}")
cal = []
for t, d in CO.items():
    implied_tc = (d["ttm_eps"] * d["shares"] + d["dna"]) / \
                 (d["vlcc_eq"] * d["days"] / 1e6) + d["breakeven"]
    ip = d["ttm_dps"] / d["ttm_eps"]
    ok = 60_000 <= implied_tc <= 130_000
    print(f"  {t:<6}{d['ttm_eps']:>16.2f}{implied_tc:>13,.0f}{d['ttm_dps']:>12.2f}"
          f"{ip*100:>15.0f}%{'PLAUSIBLE' if ok else 'IMPLAUSIBLE':>12}")
    cal.append(dict(ticker=t, ttm_eps=d["ttm_eps"], implied_tc=round(implied_tc),
                    ttm_dps=d["ttm_dps"], implied_payout=round(ip, 2)))
pd.DataFrame(cal).to_csv(os.path.join(DATA, "final_calibration.csv"), index=False)
print("\n  >> Both implied rates sit inside the range these fleets actually earned")
print("     over the trailing year. The spec is NOT obviously double-counting.")
print("     BUT Astra's objection is not disproved either: a compensating error")
print("     in the breakeven would be invisible to this test. Logged as a")
print("     KNOWN LIMITATION, not as a resolved issue.")

# ===================================================== 1) model-free facts
print("\n" + "-" * 100)
print("1) WHAT IS TRUE WITHOUT ANY MODEL — the part no assumption can move")
print("-" * 100)
print(f"  {'':<6}{'spot':>8}{'NAVPS':>9}{'P/NAV':>8}{'prior range':>16}"
      f"{'above prior high?':>20}")
mf = []
for t, d in CO.items():
    pn = d["price"] / d["navps"]
    above = pn > d["pnav_hi"]
    rng = f"{d['pnav_lo']:.2f}-{d['pnav_hi']:.2f}x"
    verdict = f"YES +{(pn/d['pnav_hi']-1)*100:.0f}%" if above else "no"
    print(f"  {t:<6}{d['price']:>8.2f}{d['navps']:>9.2f}{pn:>8.2f}"
          f"{rng:>16}{verdict:>20}")
    mf.append(dict(ticker=t, price=round(d["price"], 2), navps=d["navps"],
                   pnav=round(pn, 2), prior_low=d["pnav_lo"], prior_high=d["pnav_hi"],
                   above_prior_high=bool(above)))
pd.DataFrame(mf).to_csv(os.path.join(DATA, "final_modelfree.csv"), index=False)
print("\n  >> THIS is the durable finding. Both names trade ABOVE the highest")
print("     P/NAV either has recorded at any cycle top in the filing record,")
print("     INCLUDING the 2007-08 super-cycle. No forecast is involved.")

# corrected leverage -- Astra [B4]
print("\n  LEVERAGE, recomputed from these same inputs (Astra [B4]):")
print(f"  {'':<6}{'net debt':>11}{'fleet value':>13}{'net debt/fleet':>16}"
      f"{'previously stated':>19}")
for t, d in CO.items():
    lv = d["net_debt"] / d["fleet_mv"] * 100
    prev = "~8%" if t == "DHT" else "~18%"
    print(f"  {t:<6}{d['net_debt']:>11,.1f}{d['fleet_mv']:>13,.1f}{lv:>15.1f}%{prev:>19}")
nav0, nav1, fleet_fall = 36.18, 1.46, 0.43
implied_lev = 1 - fleet_fall / (1 - nav1 / nav0)
print(f"\n  The 2008 Frontline example: NAV/share {nav0} -> {nav1} is "
      f"{(1-nav1/nav0)*100:.1f}%.")
print(f"  With a {fleet_fall:.0%} fleet-value fall and unchanged debt, the identity")
print(f"      initial debt/fleet = 1 - (fleet fall) / (NAV fall)")
print(f"  implies {implied_lev*100:.1f}% — NOT the 88% previously published.")
print(f"  At 88%, a {fleet_fall:.0%} asset fall makes NAV NEGATIVE, not -96%.")
print("  >> The 88% figure is WITHDRAWN. The lesson survives; the number does not.")
print("\n  NOTE on the exit multiple: FRO's LOWEST observed P/NAV in the filing")
print(f"  record is {CO['FRO']['pnav_lo']:.2f}x (Dec-2020), never 1.00x. Using a 1.00x exit for")
print("  FRO is therefore BELOW anything it has ever traded at — a bearish thumb")
print("  on the scale, exactly as Astra warned. The joint grid in §3 is the fix:")
print("  the exit multiple is shown as a free variable, not buried as a constant.")

# ===================================================== 2) corrected valuation
print("\n" + "-" * 100)
print("2) CORRECTED MODEL — fleet and debt modelled SEPARATELY (fixes [B2])")
print("-" * 100)


def value(d, tc, yrs, reprice, payout, coe=COE, drag=AGE_DRAG, exit_pnav=1.00,
          capex_eq_dna=True):
    """
    Fleet value per share and net debt per share are tracked separately.
      fleet  <- ages at `drag`, then repriced once at exit by `reprice`
      cash   <- accretes retained earnings; NOT aged (v2's bug)
      NAV    <- fleet + cash - net debt
    Maintenance capex is assumed equal to D&A (stated assumption, tested).
    """
    eps = eps_at(d, tc)
    dps = max(eps, 0) * payout
    fleet = (d["navps"] * d["shares"] + d["net_debt"]) / d["shares"]
    nd, cash, pv_div = d["net_debt"] / d["shares"], 0.0, 0.0
    for y in range(1, yrs + 1):
        pv_div += dps / (1 + coe) ** y
        fleet *= (1 - drag)
        retained = eps - dps
        if not capex_eq_dna:
            retained += d["dna"] / d["shares"]
        cash += retained
    fleet *= (1 + reprice)
    nav_exit = fleet + cash - nd
    pv_exit = exit_pnav * nav_exit / (1 + coe) ** yrs
    return pv_div, pv_exit, pv_div + pv_exit, eps, dps, nav_exit


rows = []
for t, d in CO.items():
    for lbl, po in [("trailing", d["payout"]), ("policy", d["policy_payout"])]:
        if lbl == "policy" and abs(po - d["payout"]) < 1e-9:
            continue
        print(f"\n  ── {t} ── spot US${d['price']:.2f} · payout basis: {lbl} {po:.0%}")
        print(f"     {'scen':<6}{'TC':>9}{'yr':>4}{'repr':>7}{'EPS':>7}{'DPS':>7}"
              f"{'PVdiv':>8}{'PVexit':>8}{'NAVexit':>9}{'TARGET':>9}{'upside':>8}")
        for nm, s in SCEN.items():
            pvd, pvx, tot, eps, dps, navx = value(d, s["tc"], s["yrs"],
                                                  s["reprice"], po)
            up = (tot / d["price"] - 1) * 100
            print(f"     {nm:<6}{s['tc']:>9,}{s['yrs']:>4}{s['reprice']*100:>6.0f}%"
                  f"{eps:>7.2f}{dps:>7.2f}{pvd:>8.2f}{pvx:>8.2f}{navx:>9.2f}"
                  f"{tot:>9.2f}{up:>7.0f}%")
            rows.append(dict(ticker=t, payout_basis=lbl, payout=po, scenario=nm,
                             tc=s["tc"], years=s["yrs"], reprice=s["reprice"],
                             eps=round(eps, 2), dps=round(dps, 2),
                             pv_div=round(pvd, 2), pv_exit=round(pvx, 2),
                             nav_exit=round(navx, 2), target=round(tot, 2),
                             upside_pct=round(up), note=s["note"]))
tp = pd.DataFrame(rows)
tp.to_csv(os.path.join(DATA, "final_targets.csv"), index=False)

print("\n  v2 -> v3 effect of the corrections:")
print(f"  {'':<6}{'v2 base target':>16}{'v3 base target':>16}{'change':>10}")
for t, v2 in [("DHT", 16.47), ("FRO", 31.50)]:
    v3 = tp[(tp["ticker"] == t) & (tp["scenario"] == "Base") &
            (tp["payout_basis"] == "trailing")]["target"].iloc[0]
    print(f"  {t:<6}{v2:>16.2f}{v3:>16.2f}{(v3/v2-1)*100:>9.0f}%")

# ===================================================== 3) joint grid
print("\n" + "-" * 100)
print("3) THE JOINT GRID — Astra [M5]: duration and exit multiple TOGETHER")
print("-" * 100)
print("  v2 blamed the whole discount on rate duration. It is not identified:")
print("  the exit multiple does just as much work. Shown jointly, at US$95k.\n")
grid_rows = []
for t, d in CO.items():
    print(f"  ── {t} ── spot US${d['price']:.2f}   (cells = target; "
          f"shaded >= spot marked *)")
    mults = [0.80, 1.00, 1.20, 1.40, 1.60]
    print(f"     {'yrs':<5}" + "".join(f"{m:>11.2f}x" for m in mults))
    for y in [1, 2, 3, 5, 8]:
        cells = ""
        for m in mults:
            v = value(d, 95_000, y, SCEN["Base"]["reprice"], d["payout"],
                      exit_pnav=m)[2]
            cells += f"{v:>11.2f}{'*' if v >= d['price'] else ' '}"
            grid_rows.append(dict(ticker=t, years=y, exit_pnav=m,
                                  target=round(v, 2), clears_spot=v >= d["price"]))
        print(f"     {y:<5}" + cells)
    print()
pd.DataFrame(grid_rows).to_csv(os.path.join(DATA, "final_joint_grid.csv"), index=False)
print("  >> Wherever a '*' appears, today's price is justified. The '*' region is")
print("     reached by RAISING THE EXIT MULTIPLE just as easily as by extending")
print("     duration. That is precisely why v2's 'the market implies N years'")
print("     claim is WITHDRAWN — N is not identified from price alone.")

# ===================================================== 4) exits
print("\n" + "-" * 100)
print("4) EXIT TRIGGERS — re-anchored on OBSERVABLES, not on model output")
print("-" * 100)


def yld(t, rate, po=None):
    d = CO[t]
    return max(eps_at(d, rate), 0) * (po or d["payout"]) / d["price"] * 100


EXITS = [
    ("P/NAV falls back below 1.2x on a rising fleet value",
     "the premium is being given back", "the thesis is over — EXIT",
     "model-free; uses only broker values and the share price"),
    (f"P/NAV rises above 2.0x (DHT) / 2.2x (FRO)",
     "beyond EVERY observation in the filing record", "TRIM 25%",
     "today 1.62x / 1.69x — already above every prior cycle top"),
    ("1-yr TC below US$85,000 for 4 consecutive weeks",
     f"DHT yld {yld('DHT',85_000):.1f}% / FRO {yld('FRO',85_000):.1f}%",
     "TRIM 25%", "FRO loses its 8% cushion first"),
    ("1-yr TC below US$75,000",
     f"DHT {yld('DHT',75_000):.1f}% / FRO {yld('FRO',75_000):.1f}%",
     "TRIM to half", "both breach 8%; the income bid leaves"),
    ("1-yr TC below US$60,000",
     f"DHT {yld('DHT',60_000):.1f}% / FRO {yld('FRO',60_000):.1f}%",
     "EXIT", "at/below DHT's own historical average yield"),
    ("Hormuz transit normalises toward ~15+ mb/d",
     "the premium's CAUSE is removed", "TRIM 25% on the news",
     "do not wait for the rate; the equity leads it"),
    ("Second-hand 5-yr-old VLCC values fall two consecutive months",
     "NAV itself is falling — the denominator moves", "REDUCE",
     "a P/NAV premium on a FALLING NAV is the worst configuration"),
    ("FRO net-debt-to-fleet rises above 35% (today 23.8%)",
     "leverage re-amplifies asset moves", "REDUCE",
     "2008 showed ~55% leverage turned a -43% asset move into -96% NAV"),
    ("A dividend cut while the TC rate is UNCHANGED",
     "policy break, not a rate signal", "EXIT the name",
     "the payout IS the thesis for a yield-anchored holder"),
    ("2028 deliveries confirmed above ~125 VLCCs",
     "supply wall arrives early", "begin scaling out",
     "the cycle's known expiry date"),
]
print(f"  {'trigger':<52}{'reading':<38}{'action'}")
for a, b, c, why in EXITS:
    print(f"  {a:<52}{b:<38}{c}")
    print(f"       why: {why}")
pd.DataFrame(EXITS, columns=["trigger", "reading", "action", "rationale"]
             ).to_csv(os.path.join(DATA, "final_exits.csv"), index=False)

# ===================================================== chart
fig, axes = plt.subplots(1, 3, figsize=(18.5, 5.9))

ax = axes[0]
x = np.arange(2)
names = ["DHT", "FRO"]
cur = [CO[t]["price"] / CO[t]["navps"] for t in names]
hi = [CO[t]["pnav_hi"] for t in names]
lo = [CO[t]["pnav_lo"] for t in names]
ax.bar(x - .2, cur, .38, label="today", color="#c0392b")
ax.bar(x + .2, hi, .38, label="highest prior cycle top", color="#7f8c8d")
for i in range(2):
    ax.plot([x[i] + .2, x[i] + .2], [lo[i], hi[i]], color="#2c3e50", lw=2)
    ax.text(x[i] - .2, cur[i] + .04, f"{cur[i]:.2f}x", ha="center",
            fontweight="bold", fontsize=10)
    ax.text(x[i] + .2, hi[i] + .04, f"{hi[i]:.2f}x", ha="center", fontsize=9)
ax.axhline(1.0, color="k", ls=":", lw=1.5)
ax.text(1.45, 1.03, "NAV", fontsize=8.5)
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=11)
ax.set_ylabel("price / NAV per share")
ax.set_title("A. The one model-free fact\nboth above EVERY prior cycle top",
             fontsize=10.5, fontweight="bold")
ax.legend(fontsize=8.5); ax.grid(axis="y", alpha=.25)

for i, t in enumerate(names):
    ax = axes[i + 1]
    g = pd.DataFrame(grid_rows)
    g = g[g["ticker"] == t]
    piv = g.pivot(index="years", columns="exit_pnav", values="target")
    im = ax.imshow(piv.values, cmap="RdYlGn", aspect="auto",
                   vmin=CO[t]["price"] * .5, vmax=CO[t]["price"] * 1.5)
    ax.set_xticks(range(len(piv.columns)))
    ax.set_xticklabels([f"{c:.2f}x" for c in piv.columns], fontsize=9)
    ax.set_yticks(range(len(piv.index)))
    ax.set_yticklabels(piv.index, fontsize=9)
    ax.set_xlabel("exit P/NAV multiple"); ax.set_ylabel("years at US$95k/day")
    for r in range(piv.shape[0]):
        for c in range(piv.shape[1]):
            v = piv.values[r, c]
            ax.text(c, r, f"{v:.0f}", ha="center", va="center", fontsize=8.5,
                    fontweight="bold" if v >= CO[t]["price"] else "normal",
                    color="k")
    ax.set_title(f"{'BC'[i]}. {t} — duration is NOT identified\ngreen = today's "
                 f"${CO[t]['price']:.0f} justified", fontsize=10.5, fontweight="bold")

fig.suptitle("Final synthesis v3 — after the Astra review: the NAV premium is the "
             "finding; the implied-duration claim is withdrawn",
             fontsize=12.5, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, .90])
p = os.path.join(CHARTS, "final_synthesis.png")
fig.savefig(p, dpi=140)
plt.close(fig)
print(f"\n  chart -> {p}")
print("\nDone.")

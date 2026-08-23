"""
VLCC supply-demand balance model (2025-2030) — does the 2027/2028 newbuild wave
break the cycle? Turns the scary GROSS delivery numbers into NET fleet growth
after scrapping + shadow-fleet exit, and nets that against demand (tonne-mile +
SPR restocking).

Key inputs (mid-2026, sourced; see report §1 for citations & Rule-4 ranges):
- Total VLCC fleet ~900; compliant/"mainstream" ~700; shadow ~166-200.
- Gross deliveries: 2026 ~15, 2027 ~50-68 (user cited 68; Gibson ~41), 2028 ~125-127.
- Over-20yo now ~130 (~20% of fleet); doubles to ~300 by 2029-30 -> a huge, forced
  scrapping pool as IMO-2030/EEXI/CII bite.
- Tonne-mile demand growth: ~+2% 2026, ~0% 2027, ~flat 2028 (BIMCO); PLUS SPR
  restocking absorbing ~30-70 ships for years (this repo's report #13).

Outputs (./data/ and ./charts/):
  balance.csv        -- gross deliveries, scrap scenarios, net growth %, per year
  net_growth.png     -- gross vs net fleet growth under 3 scrap scenarios
  Run: python run_supply_model.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "data"); os.makedirs(OUT, exist_ok=True)
CH = os.path.join(HERE, "charts"); os.makedirs(CH, exist_ok=True)

FLEET_START = 900          # total VLCC fleet, start of 2026 (~870-917 across sources)
# Gross newbuild deliveries by year (user-cited 2027=68, 2028=125; ranges in report)
GROSS = {2026: 15, 2027: 68, 2028: 125, 2029: 90, 2030: 40}
# Ships crossing 20yo each year (the natural scrap-eligible pool); ~130 now -> ~300 by 2030
SCRAP_ELIGIBLE_ADDED = {2026: 30, 2027: 40, 2028: 45, 2029: 50, 2030: 45}

# Three scrapping-behaviour scenarios (ships actually recycled per year)
SCRAP = {
    "Low  (rates stay high, owners defer)":  {2026: 5,  2027: 15, 2028: 30, 2029: 45, 2030: 45},
    "Base (IMO-2030 forces gradual exit)":   {2026: 8,  2027: 30, 2028: 55, 2029: 70, 2030: 60},
    "High (regulatory cliff + soft rates)":  {2026: 12, 2027: 45, 2028: 80, 2029: 95, 2030: 80},
}


def build():
    rows = []
    fleets = {k: FLEET_START for k in SCRAP}
    for yr in range(2026, 2031):
        g = GROSS[yr]
        for name, sc in SCRAP.items():
            s = sc[yr]
            net = g - s
            f0 = fleets[name]
            gross_pct = g / f0 * 100
            net_pct = net / f0 * 100
            rows.append({"year": yr, "scenario": name, "gross_deliveries": g,
                         "scrapping": s, "net_add": net,
                         "gross_growth_pct": round(gross_pct, 1),
                         "net_growth_pct": round(net_pct, 1),
                         "fleet_end": f0 + net})
            fleets[name] = f0 + net
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "balance.csv"), index=False)
    return df


def chart(df):
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5.5))
    yrs = sorted(GROSS)
    # Left: gross vs net fleet growth % by scenario
    axL.bar([y - 0.25 for y in yrs], [GROSS[y] / FLEET_START * 100 for y in yrs],
            width=0.25, color="#b0413e", label="GROSS deliveries")
    colors = {"Low  (rates stay high, owners defer)": "#e08a2e",
              "Base (IMO-2030 forces gradual exit)": "#2b6cb0",
              "High (regulatory cliff + soft rates)": "#2e7d4f"}
    offs = {"Low  (rates stay high, owners defer)": 0.0,
            "Base (IMO-2030 forces gradual exit)": 0.0, "High (regulatory cliff + soft rates)": 0.0}
    for name in SCRAP:
        sub = df[df["scenario"] == name]
        axL.plot(sub["year"], sub["net_growth_pct"], marker="o", lw=2,
                 color=colors[name], label=f"NET — {name.split('(')[0].strip()}")
    axL.axhline(2.0, color="grey", ls=":", lw=1, label="~demand growth (tonne-mile, ~0-2%)")
    axL.set_title("VLCC fleet growth: GROSS deliveries vs NET after scrapping")
    axL.set_ylabel("% of fleet per year"); axL.set_xticks(yrs); axL.grid(alpha=0.2)
    axL.legend(fontsize=7, loc="upper right")

    # Right: absolute ships — gross deliveries vs scrap-eligible pool
    axR.bar([y - 0.2 for y in yrs], [GROSS[y] for y in yrs], width=0.4,
            color="#b0413e", label="Gross deliveries")
    axR.bar([y + 0.2 for y in yrs], [SCRAP_ELIGIBLE_ADDED[y] for y in yrs], width=0.4,
            color="#7b8a8b", label="Ships crossing 20yo (scrap-eligible)")
    axR.plot(yrs, [SCRAP["Base (IMO-2030 forces gradual exit)"][y] for y in yrs],
             marker="s", color="#2b6cb0", lw=2, label="Base-case scrapping")
    axR.set_title("Ships: deliveries vs the aging pool that can offset them")
    axR.set_ylabel("VLCCs per year"); axR.set_xticks(yrs); axR.grid(alpha=0.2)
    axR.legend(fontsize=8)
    fig.suptitle("The 2028 wave is real, but NET growth depends on scrapping — and a record aging pool is arriving to absorb it",
                 y=1.02, fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "net_growth.png"), dpi=110, bbox_inches="tight")
    plt.close(fig)


def main():
    df = build()
    print("VLCC supply-demand balance (fleet start 2026 = %d):" % FLEET_START)
    for name in SCRAP:
        print(f"\n-- {name} --")
        print(df[df["scenario"] == name][["year", "gross_deliveries", "scrapping",
              "net_add", "gross_growth_pct", "net_growth_pct"]].to_string(index=False))
    chart(df)
    # cumulative 2027-2028 net add
    print("\nCumulative NET adds 2027+2028 by scenario:")
    for name in SCRAP:
        sub = df[(df["scenario"] == name) & (df["year"].isin([2027, 2028]))]
        print(f"  {name.split('(')[0].strip():6}: gross {sub['gross_deliveries'].sum()}, "
              f"scrap {sub['scrapping'].sum()}, NET +{sub['net_add'].sum()} "
              f"({sub['net_add'].sum()/FLEET_START*100:.1f}% of fleet over 2 yrs)")
    print(f"\nCharts -> {CH}\nCSVs -> {OUT}")


if __name__ == "__main__":
    main()

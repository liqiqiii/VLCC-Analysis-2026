"""
Gold miners: US-listed Western majors vs China majors — comparison model.

Tests the user's thesis (US = higher cost but pure-play gold; China = low cost
but "non-lucrative" diversification) against 2025 data, and computes the
operating-leverage margin at different gold prices (gold ~$4,474/oz Sep-2026).

Data hygiene (Rule 4): production/AISC/mix are 2025 actuals or FY-guidance from
company filings + trade press (ranges flagged in the report §1). yfinance is used
only for live valuation cross-checks and is indexed BY TICKER NAME (columns come
back alphabetical).

Outputs (./data/, ./charts/):
  peers.csv            -- the master comparison table
  margin_by_price.csv  -- gold gross margin/oz and gold gross profit at price scenarios
  aisc_margin.png      -- AISC bars + margin at current gold price
Run: python run_gold_compare.py
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

GOLD_NOW = 4474  # $/oz, Sep 3 2026 (Kitco)

# 2025 actuals / FY-guidance. gold_moz = attributable gold; aisc = $/oz;
# gold_rev_pct = gold as % of revenue (100 = pure play); mcap_usd_b approx.
PEERS = [
    # US-listed Western majors
    dict(name="Newmont",       ticker="NEM",  market="US-listed", gold_moz=5.9,  aisc=1609,
         gold_rev_pct=88, mcap_usd_b=137, fwd_pe=12.9, div_yield=0.8, note="World #1 gold; >85% gold pure-play (post-Newcrest)"),
    dict(name="Agnico Eagle",  ticker="AEM",  market="US-listed", gold_moz=3.45, aisc=1339,
         gold_rev_pct=97, mcap_usd_b=105, fwd_pe=16.6, div_yield=0.9, note="Lowest AISC of the majors; Tier-1 (Canada/Finland/Aus)"),
    dict(name="Kinross",       ticker="KGC",  market="US-listed", gold_moz=2.0,  aisc=1480,
         gold_rev_pct=99, mcap_usd_b=38,  fwd_pe=10.3, div_yield=0.5, note="Near-pure gold; US(Nevada/Alaska)+W.Africa"),
    dict(name="Barrick",       ticker="GOLD", market="US-listed", gold_moz=3.26, aisc=1637,
         gold_rev_pct=80, mcap_usd_b=72,  fwd_pe=11.1, div_yield=1.9, note="Gold + growing copper ambition; jurisdiction issues"),
    # China majors
    dict(name="Zijin Mining",  ticker="2899.HK", market="China", gold_moz=2.9,  aisc=1480,
         gold_rev_pct=33, mcap_usd_b=120, fwd_pe=9.3,  div_yield=3.0, note="COPPER-gold major: ~50-55% copper rev (its profit engine), 45% overseas"),
    dict(name="Shandong Gold", ticker="1787.HK", market="China", gold_moz=1.5,  aisc=1250,
         gold_rev_pct=95, mcap_usd_b=24,  fwd_pe=11.0, div_yield=1.2, note="China's gold pure-play; deep Jiaodong mines"),
    dict(name="Zhaojin Mining",ticker="1818.HK", market="China", gold_moz=0.6,  aisc=1300,
         gold_rev_pct=90, mcap_usd_b=10,  fwd_pe=10.0, div_yield=0.5, note="Pure gold; Haiyu ramp -> AISC toward ~$1,100; Zijin-affiliated"),
]


def build_peers():
    df = pd.DataFrame(PEERS)
    df["margin_oz_now"] = GOLD_NOW - df["aisc"]
    df["gold_gross_profit_b"] = (df["margin_oz_now"] * df["gold_moz"] * 1e6 / 1e9).round(1)
    df["margin_pct_now"] = (df["margin_oz_now"] / GOLD_NOW * 100).round(0)
    # Gold-price elasticity of gold gross profit = P / (P - AISC).
    # Higher AISC -> higher torque to the gold price (more upside AND downside).
    df["gold_elasticity"] = (GOLD_NOW / (GOLD_NOW - df["aisc"])).round(2)
    # Effective equity torque also scaled by how much of the business IS gold.
    df["equity_gold_torque"] = (df["gold_elasticity"] * df["gold_rev_pct"] / 100).round(2)
    df.to_csv(os.path.join(OUT, "peers.csv"), index=False)
    return df


def margin_by_price(df):
    rows = []
    for price in [2500, 3000, 3500, 4000, GOLD_NOW, 5000]:
        for _, r in df.iterrows():
            m = price - r["aisc"]
            rows.append(dict(gold_price=price, name=r["name"], market=r["market"],
                             margin_oz=m, gold_gross_profit_b=round(m * r["gold_moz"] * 1e6 / 1e9, 1)))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(OUT, "margin_by_price.csv"), index=False)
    return out


def chart(df):
    df = df.sort_values("aisc")
    colors = ["#b0413e" if m == "China" else "#2b6cb0" for m in df["market"]]
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5.5))
    # Left: AISC bars with the gold-price line = margin visualized
    axL.bar(df["name"], df["aisc"], color=colors)
    axL.axhline(GOLD_NOW, color="gold", lw=2, ls="--", label=f"Gold ${GOLD_NOW}/oz (Sep-2026)")
    for x, (a, n) in enumerate(zip(df["aisc"], df["name"])):
        axL.text(x, a + 40, f"${a:,}", ha="center", fontsize=8)
    axL.set_ylabel("AISC ($/oz)"); axL.set_title("Cost curve — AISC vs the gold price (the gap = margin/oz)")
    axL.tick_params(axis="x", rotation=30); axL.legend(); axL.grid(alpha=0.2, axis="y")
    axL.set_ylim(0, GOLD_NOW + 400)
    # Right: gold gross profit at current price ($B) — pure-play vs diversified
    d2 = df.sort_values("gold_gross_profit_b", ascending=True)
    axR.barh(d2["name"], d2["gold_gross_profit_b"], color=["#b0413e" if m == "China" else "#2b6cb0" for m in d2["market"]])
    for y, v in enumerate(d2["gold_gross_profit_b"]):
        axR.text(v + 0.3, y, f"${v}B", va="center", fontsize=8)
    axR.set_xlabel("Gold gross profit at $%d/oz ($B)" % GOLD_NOW)
    axR.set_title("Gold-only gross profit (margin/oz × gold oz)")
    axR.grid(alpha=0.2, axis="x")
    import matplotlib.patches as mp
    axR.legend(handles=[mp.Patch(color="#2b6cb0", label="US-listed Western"),
                        mp.Patch(color="#b0413e", label="China")], loc="lower right")
    fig.suptitle("Gold miners: cost curve & gold-margin — China lower-cost than Newmont/Barrick, but Agnico (Western) is lowest of all",
                 y=1.02, fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(CH, "aisc_margin.png"), dpi=110, bbox_inches="tight")
    plt.close(fig)


def main():
    df = build_peers()
    print(f"Gold ${GOLD_NOW}/oz. Peer comparison:")
    print(df[["name", "market", "gold_moz", "aisc", "gold_rev_pct",
              "margin_oz_now", "gold_gross_profit_b", "fwd_pe", "div_yield"]].to_string(index=False))
    mbp = margin_by_price(df)
    chart(df)
    print("\nAISC ranking (low->high):")
    for _, r in df.sort_values("aisc").iterrows():
        print(f"  {r['name']:14s} ({r['market']:10s}) AISC ${r['aisc']:,} | gold {r['gold_rev_pct']}% of rev")
    print("\nGOLD-PRICE ELASTICITY = P/(P-AISC): higher AISC -> MORE torque to gold")
    for _, r in df.sort_values("gold_elasticity", ascending=False).iterrows():
        print(f"  {r['name']:14s} elasticity {r['gold_elasticity']:.2f}x | equity gold-torque {r['equity_gold_torque']:.2f}x (x gold%%)")
    # torque check: gold gross profit at $4,474 vs a $6,000 bull case
    print("\nBull-case torque — gold gross profit $4,474 -> $6,000/oz:")
    for _, r in df.sort_values("aisc").iterrows():
        p0 = (GOLD_NOW - r["aisc"]) * r["gold_moz"]
        p1 = (6000 - r["aisc"]) * r["gold_moz"]
        print(f"  {r['name']:14s} +{(p1/p0-1)*100:4.0f}% gold profit  (AISC ${r['aisc']:,})")
    print(f"\nCharts -> {CH}\nCSVs -> {OUT}")


if __name__ == "__main__":
    main()

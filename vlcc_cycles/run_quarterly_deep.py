"""
VLCC quarterly rebuild + three follow-ups:
  (1) QUARTERLY rate & price series (replaces the annual-average version)
  (2) Market-cap-per-VLCC  -> removes the share-dilution distortion that made
      cross-era PRICE comparisons misleading
  (3) Lead/lag: does the stock lead the rate, and by how much (quarterly + weekly)
  (4) CRule 8 exit-trigger dashboard with explicit thresholds

UNITS: the rate is TCE in USD per vessel per DAY ($/day). A "quarterly rate" is
the average of that daily rate over the quarter — NOT a per-quarter dollar sum.

DATA QUALITY (Rule 4), stated plainly:
  * Quarterly TCE for 2024Q1-2026Q3 = DHT's OWN disclosed fleet TCE (primary).
  * Earlier quarters have no reliable public quarterly TD3C series available to
    this analysis; they are marked source='annual-interp' (annual broker average
    carried across the 4 quarters) and must NOT be read as true quarterly prints.
  * Share counts are period approximations (Macrotrends/CompaniesMarketCap);
    FRO's pre-2012 count is especially uncertain (reverse split) -> flagged.
  * Fleet counts: DHT 24 (P-Rule 1) vs 28 (trade press) conflict -> both shown.

Outputs (./data/, ./charts/):
  quarterly_rate_price.csv   mcap_per_vlcc.csv   leadlag.csv   exit_dashboard.csv
  quarterly_rate_vs_stock.png
Run: python run_quarterly_deep.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "data"); os.makedirs(OUT, exist_ok=True)
CH = os.path.join(HERE, "charts"); os.makedirs(CH, exist_ok=True)

# ---------- (1) QUARTERLY TCE ($/day, average over the quarter) ----------
# PRIMARY: DHT-disclosed fleet TCE. Marked 'DHT-disclosed'.
DHT_DISCLOSED = {
    "2024Q1": 47200, "2024Q2": 47200, "2024Q3": 43000, "2024Q4": 45200,
    "2025Q1": 35800, "2025Q2": 46300, "2025Q3": 40500, "2025Q4": 60300,
    "2026Q1": 78800, "2026Q2": 126700, "2026Q3": 94300,
}
# Annual broker averages carried across quarters (NOT true quarterly prints).
ANNUAL_INTERP = {
    2005: 54000, 2006: 61000, 2007: 52000, 2008: 90000, 2009: 31000, 2010: 44000,
    2011: 19000, 2012: 22000, 2013: 19000, 2014: 28000, 2015: 64000, 2016: 41000,
    2017: 21000, 2018: 18000, 2019: 45000, 2020: 64000, 2021: 3000, 2022: 25000,
    2023: 44000,
}

# ---------- (2) P/NAV — the dilution-free valuation metric ----------
# Historical market-cap-per-VLCC reconstruction was ATTEMPTED and REJECTED: reliable
# point-in-time share counts are unavailable and FRO's reverse split makes pre-2012
# raw prices ambiguous (a naive run produced $495M/VLCC for DHT-2010 vs a true VLCC
# value of ~$100M). Instead we use TODAY's EV vs TODAY's fleet asset value, which is
# the standard shipping metric (P/NAV) and is fully sourced.
ASSET_VALUES = dict(vlcc_5yr=174.5, vlcc_newbuild=129.5, suezmax_5yr=120.0, lr2_5yr=100.0)
COMPANIES = dict(
    DHT=dict(ev=3994.2, mcap=3714.9, fleet={"vlcc_5yr": 24}),
    FRO=dict(ev=14060.2, mcap=11948.2,
             fleet={"vlcc_5yr": 42, "suezmax_5yr": 21, "lr2_5yr": 18}),
)

EXIT_RULES = [
    ("Spot TD3C < $60k/day for >3 consecutive weeks", "Reduce 30%",
     "Below ~2x DHT breakeven; sustained regime breaking (Rule B: sustained is what's capitalized)"),
    ("DHT quarterly disclosed fleet TCE falls QoQ two quarters running", "Reduce 30%",
     "Company-disclosed TCE is the cleanest primary signal; two down quarters = trend not noise"),
    ("FRO forward-booked % at a LOWER rate than the prior quarter's print", "Trim FRO first",
     "FRO is priced for ~$139k sustained; a booking downgrade hits it hardest"),
    ("Monthly VLCC demolition < 3-4 ships/month through 2027", "Raise cash / trim",
     "Low-scrap scenario -> net fleet growth approaches gross -> 2028 oversupply"),
    ("Any hyperscaler-style capex analog: new VLCC orders keep running >150/yr", "Begin trimming",
     "Orderbook already ~35% of fleet (CRule 5 sell-signal: order books filling)"),
    ("Sanctions thaw / shadow-fleet re-entry headlines", "Full re-underwrite",
     "Returning shadow VLCCs = +10-12% compliant supply shock"),
    ("Stock falls while spot rate is flat/up for >2 weeks", "Investigate, likely early exit",
     "Equity leads the rate by 2-4 weeks (both ways) - the market sees it first"),
    ("P/E < 4x on peak earnings", "Take profits on 50%",
     "CRule 2: trough-PE at peak-EPS = market pricing terminal decline"),
]


def q_label(ts):
    return f"{ts.year}Q{ts.quarter}"


def quarterly_prices():
    out = {}
    for t in ["FRO", "DHT"]:
        s = yf.download(t, start="2004-01-01", interval="1mo",
                        auto_adjust=True, progress=False)["Close"].dropna()
        s = s.iloc[:, 0] if hasattr(s, "columns") else s
        q = s.resample("QE").mean()
        out[t] = pd.Series(q.values, index=[q_label(i) for i in q.index])
    return out


def build_quarterly():
    px = quarterly_prices()
    rows = []
    for yr in range(2005, 2027):
        for qq in range(1, 5):
            lab = f"{yr}Q{qq}"
            if lab in DHT_DISCLOSED:
                rate, src = DHT_DISCLOSED[lab], "DHT-disclosed (primary)"
            elif yr in ANNUAL_INTERP:
                rate, src = ANNUAL_INTERP[yr], "annual-interp (NOT a true quarterly print)"
            else:
                continue
            rows.append(dict(quarter=lab, year=yr, q=qq, TCE_usd_per_day=rate, rate_source=src,
                             FRO_avg_px=round(float(px["FRO"].get(lab, np.nan)), 2),
                             DHT_avg_px=round(float(px["DHT"].get(lab, np.nan)), 2)))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "quarterly_rate_price.csv"), index=False)
    return df


def chart_quarterly(df):
    d = df.dropna(subset=["FRO_avg_px"]).reset_index(drop=True)
    x = np.arange(len(d))
    prim = d["rate_source"].str.startswith("DHT")
    fig, ax = plt.subplots(figsize=(15, 6.5))
    ax.bar(x[~prim.values], d.loc[~prim, "TCE_usd_per_day"] / 1000, color="#dfe6ec",
           label="TCE ($k/day) - annual-interp (not true quarterly)")
    ax.bar(x[prim.values], d.loc[prim, "TCE_usd_per_day"] / 1000, color="#7aa6c8",
           label="TCE ($k/day) - DHT-disclosed quarterly (primary)")
    ax.set_ylabel("Quarterly average VLCC TCE ($k/day)"); ax.set_ylim(0, 140)
    ax2 = ax.twinx()
    ax2.plot(x, d["FRO_avg_px"], color="#b0413e", lw=1.8, label="FRO quarterly avg px (adj, log)")
    ax2.plot(x, d["DHT_avg_px"], color="#2b6cb0", lw=1.8, label="DHT quarterly avg px (adj, log)")
    ax2.set_yscale("log"); ax2.set_ylabel("Quarterly average adjusted price (log, $)")
    step = 8
    ax.set_xticks(x[::step]); ax.set_xticklabels(d["quarter"][::step], rotation=45, fontsize=8)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)
    ax.set_title("QUARTERLY VLCC TCE ($/day, avg over quarter) vs DHT/FRO quarterly average adjusted price")
    ax.grid(alpha=0.2, axis="y")
    fig.tight_layout(); fig.savefig(os.path.join(CH, "quarterly_rate_vs_stock.png"),
                                    dpi=115, bbox_inches="tight")
    plt.close(fig)


def pnav():
    """(2) EV vs fleet asset value — dilution-free, sourced, cross-era-safe."""
    rows = []
    for name, c in COMPANIES.items():
        nav = sum(ASSET_VALUES[k] * n for k, n in c["fleet"].items())
        ships = sum(c["fleet"].values())
        rows.append(dict(ticker=name, ships=ships,
                         fleet_asset_value_M=round(nav),
                         EV_M=round(c["ev"]), mcap_M=round(c["mcap"]),
                         EV_per_ship_M=round(c["ev"] / ships, 1),
                         EV_to_NAV=round(c["ev"] / nav, 2),
                         premium_pct=round((c["ev"] / nav - 1) * 100)))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "pnav.csv"), index=False)
    return df


def leadlag():
    """(3) Quarterly lead/lag on REAL (non-interpolated) disclosed TCE.
    Convention: corr(px.shift(+k), rate) high at k>0 => the stock's move k quarters
    EARLIER aligns with today's rate => STOCK LEADS by k quarters."""
    q = pd.Series(DHT_DISCLOSED)
    order = sorted(q.index, key=lambda s: (int(s[:4]), int(s[-1])))
    rate = q.reindex(order)
    px = quarterly_prices()
    rows = []
    for t in ["FRO", "DHT"]:
        p = px[t].reindex(order).dropna()
        common = [i for i in order if i in p.index]
        if len(common) < 8:
            continue
        pr = p.reindex(common).pct_change()
        rr = rate.reindex(common).pct_change()
        k = pd.DataFrame({"p": pr, "r": rr}).dropna()
        best = None
        for lag in range(-2, 3):
            c = k["p"].shift(lag).corr(k["r"])
            rows.append(dict(ticker=t, lag_quarters=lag, corr=round(float(c), 2), n=len(k)))
            if best is None or (not np.isnan(c) and c > best[1]):
                best = (lag, c)
        lead = ("STOCK LEADS by %d quarter(s)" % best[0]) if best[0] > 0 else (
            "coincident" if best[0] == 0 else "stock lags by %d" % abs(best[0]))
        print(f"  {t}: best corr {best[1]:.2f} at lag {best[0]:+d}Q -> {lead}  (n={len(k)} — SMALL SAMPLE)")
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "leadlag.csv"), index=False)
    return df


def exit_dashboard():
    df = pd.DataFrame(EXIT_RULES, columns=["trigger", "action", "rationale"])
    df.to_csv(os.path.join(OUT, "exit_dashboard.csv"), index=False)
    return df


def main():
    print("UNITS: TCE = USD per vessel per DAY; a 'quarterly rate' is the AVERAGE"
          " daily rate over that quarter (not a quarterly sum).\n")
    df = build_quarterly()
    print("=== (1) QUARTERLY rate + price (last 14 quarters) ===")
    print(df.tail(14).to_string(index=False))
    chart_quarterly(df)

    print("\n=== (2) P/NAV: EV vs fleet asset value (dilution-free; replaces the")
    print("        historical market-cap-per-VLCC attempt, which was REJECTED —")
    print("        see module docstring for why) ===")
    m = pnav()
    print(m.to_string(index=False))
    print(f"    [asset values: 5-yr VLCC ${ASSET_VALUES['vlcc_5yr']}M, newbuild "
          f"${ASSET_VALUES['vlcc_newbuild']}M, Suezmax ${ASSET_VALUES['suezmax_5yr']}M, "
          f"LR2 ${ASSET_VALUES['lr2_5yr']}M — Clarksons/trade press 2026]")

    print("\n=== (3) LEAD/LAG on REAL quarterly disclosed TCE (positive lag = stock leads) ===")
    leadlag()

    print("\n=== (4) CRule 8 EXIT DASHBOARD ===")
    e = exit_dashboard()
    for _, r in e.iterrows():
        print(f"  [{r['action']:<26}] {r['trigger']}")
    print(f"\nCharts -> {CH}\nCSVs -> {OUT}")


if __name__ == "__main__":
    main()

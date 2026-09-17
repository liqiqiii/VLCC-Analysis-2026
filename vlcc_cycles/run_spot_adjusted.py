"""
CORRECTED earnings model — accounts for SPOT vs TIME-CHARTER coverage.

The prior model (run_rate_valuation.py) assumed 100% of vessel-days earn the spot
rate. That is WRONG and it materially biased the DHT-vs-FRO conclusion, because
the two companies have very different spot exposure:

  DHT : 23 VLCCs = 11 on TIME CHARTER + 12 SPOT  -> ~52% spot   (annual report, Mar-2026)
  FRO : Q3-2026 VLCC days 86% SPOT / 14% TC      -> ~86% spot   (Q3-2026 disclosure)

So DHT captures only about half of a spot spike; FRO captures ~86% of it.

Blended fleet TCE = spot_share x spot_rate + tc_share x tc_rate
EPS = [vessel_days x (blended_TCE - cash_breakeven) - D&A] / shares

Company-disclosed anchors (primary):
  DHT Q1-26: spot $91,700 | TC $61,300 | fleet blend $78,800
      Q2-26: spot $162,600 | TC $90,800 | fleet blend $126,700
      Q3-26: 48% of spot days fixed at $139,700; 74% of revenue days at $94,300
  FRO Q3-26: 86% of VLCC days booked at $156,900; breakeven $23,800 (next 12m)
      Aug-26 TC fixtures: newbuild 1yr $120,000/day; 2016-built 2yr avg $90,000
      (Y1 $110k, Y2 $70k); 3yr avg $75,000 (Y1 $110k, Y2 $70k, Y3 $45k)

Run: python run_spot_adjusted.py
"""
import os
import pandas as pd

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "data"); os.makedirs(OUT, exist_ok=True)

DHT = dict(name="DHT", days=8400, be=17500, da=105e6, sh=161.24e6, px=23.04,
           spot=0.52, tc_rate=90800)     # TC rate = DHT's own Q2-26 disclosed TC TCE
FRO = dict(name="FRO", days=20290, be=23800, da=300e6, sh=222.62e6, px=53.67,
           spot=0.86, tc_rate=100000)    # TC rate ~ Aug-26 fixture blend
# NOTE: FRO breakeven revised 26,000 -> 23,800 (company: next-12-month guidance)


def blended(c, spot_rate):
    return c["spot"] * spot_rate + (1 - c["spot"]) * c["tc_rate"]


def eps(c, spot_rate):
    b = blended(c, spot_rate)
    return (c["days"] * (b - c["be"]) - c["da"]) / c["sh"], b


def old_eps(c, spot_rate):
    """The WRONG model: 100% spot exposure."""
    return (c["days"] * (spot_rate - c["be"]) - c["da"]) / c["sh"]


def main():
    print("SPOT EXPOSURE (the correction):")
    print(f"  DHT: {DHT['spot']:.0%} spot (11 of 23 VLCCs on time charter) | TC rate ${DHT['tc_rate']:,}")
    print(f"  FRO: {FRO['spot']:.0%} spot (Q3-26 disclosure)               | TC rate ${FRO['tc_rate']:,}\n")

    rows = []
    print(f"{'SPOT $/day':>11} | {'DHT blend':>10} {'DHT EPS':>8} {'(old)':>8} | "
          f"{'FRO blend':>10} {'FRO EPS':>8} {'(old)':>8}")
    for r in [95000, 150000, 200000, 300000, 530000, 600000, 1035000]:
        de, db = eps(DHT, r); fe, fb = eps(FRO, r)
        do, fo = old_eps(DHT, r), old_eps(FRO, r)
        print(f"{r:>11,} | {db:>10,.0f} {de:>8.2f} {do:>8.2f} | {fb:>10,.0f} {fe:>8.2f} {fo:>8.2f}")
        rows.append(dict(spot_rate=r, DHT_blended_TCE=round(db), DHT_EPS=round(de, 2),
                         DHT_EPS_old_wrong=round(do, 2),
                         FRO_blended_TCE=round(fb), FRO_EPS=round(fe, 2),
                         FRO_EPS_old_wrong=round(fo, 2)))
    df = pd.DataFrame(rows)

    print("\nTARGET PRICE & UPSIDE (corrected, spot-adjusted):")
    print(f"{'SPOT $/day':>11} | {'DHT @3x':>9} {'up%':>7} {'DHT @6x':>9} {'up%':>7} | "
          f"{'FRO @3x':>9} {'up%':>7} {'FRO @6x':>9} {'up%':>7} | winner@3x")
    for _, r in df.iterrows():
        d3, d6 = r.DHT_EPS * 3, r.DHT_EPS * 6
        f3, f6 = r.FRO_EPS * 3, r.FRO_EPS * 6
        du3 = (d3 / DHT["px"] - 1) * 100; fu3 = (f3 / FRO["px"] - 1) * 100
        win = "DHT" if du3 > fu3 else "FRO"
        print(f"{int(r.spot_rate):>11,} | {d3:>9.0f} {du3:>6.0f}% {d6:>9.0f} "
              f"{(d6/DHT['px']-1)*100:>6.0f}% | {f3:>9.0f} {fu3:>6.0f}% {f6:>9.0f} "
              f"{(f6/FRO['px']-1)*100:>6.0f}% | {win}")
        df.loc[_, "DHT_up3x_pct"] = round(du3); df.loc[_, "FRO_up3x_pct"] = round(fu3)
        df.loc[_, "winner_at_3x"] = win
    df.to_csv(os.path.join(OUT, "spot_adjusted.csv"), index=False)

    print("\nVALIDATION vs company-disclosed blended fleet TCE:")
    print(f"  DHT Q1-26: model blend at spot $91,700 = ${blended(DHT,91700):,.0f} "
          f"vs DISCLOSED $78,800  (diff {blended(DHT,91700)/78800-1:+.0%})")
    print(f"  DHT Q2-26: model blend at spot $162,600 = ${blended(DHT,162600):,.0f} "
          f"vs DISCLOSED $126,700 (diff {blended(DHT,162600)/126700-1:+.0%})")
    print(f"  FRO Q3-26: model blend at spot $156,900-ish -> ${blended(FRO,156900):,.0f} "
          f"vs DISCLOSED booked $156,900")

    print("\nIMPLIED SPOT RATE from today's price (corrected):")
    for c in (DHT, FRO):
        for pe in [3, 6]:
            tgt = c["px"] / pe
            need_blend = ((tgt * c["sh"]) + c["da"]) / c["days"] + c["be"]
            need_spot = (need_blend - (1 - c["spot"]) * c["tc_rate"]) / c["spot"]
            print(f"  {c['name']} @PE {pe}x -> needs blended ${need_blend:,.0f} "
                  f"-> implies SPOT ${need_spot:,.0f}/day")
    print(f"\nCSV -> {OUT}")


if __name__ == "__main__":
    main()

"""
CAPSTONE: rate level x DURABILITY -> derived peak P/E -> value, for DHT & FRO.

THE KEY IDEA (answers "how is the peak P/E calculated?"):
  The peak multiple is NOT an assumption - it is DERIVED. A cyclical's value when
  a spike rate lasts N quarters and then reverts to a normal rate is:

     Value = normal_EPS x PE_normal            <- the ongoing business
           + (N/4) x (spike_EPS - normal_EPS)  <- the EXCESS, valued at ~1.0x
                                                  because windfall is CASH

  Then the P/E the market "should" show on peak-annualized earnings is simply:

     implied_peak_PE = Value / spike_EPS

  So a LONG-lasting spike -> high implied peak P/E (market capitalizes it);
  a SHORT spike -> very low implied peak P/E (it is just cash, worth 1x).
  This reproduces the empirical fact that FRO traded at 1.7-2.6x at the 2008 top:
  the market was implicitly assuming very few quarters of durability.

Spot exposure (the Section 10 correction) is applied throughout:
  DHT ~52% spot (11 of 23 VLCCs on time charter), FRO ~86% spot.

Run: python run_capstone_matrix.py
"""
import os
import pandas as pd

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "data"); os.makedirs(OUT, exist_ok=True)

DHT = dict(name="DHT", days=8400, be=17500, da=105e6, sh=161.24e6, px=23.04,
           spot=0.52, tc=90800)
FRO = dict(name="FRO", days=20290, be=23800, da=300e6, sh=222.62e6, px=53.67,
           spot=0.86, tc=100000)

NORMAL_SPOT = 80000     # post-crisis "normal" spot assumption (structural tightness)
PE_NORMAL = 7           # mid-cycle multiple DHT/FRO actually trade at in normal years

# 5 rate levels x 3 durabilities = 15 combinations
RATES = [
    ("P1 Pessimistic  - Hormuz normalises", 95000),
    ("P2 Below-normal - partial easing",   150000),
    ("N  Neutral      - war premium holds", 300000),
    ("O1 Optimistic   - today's PHYSICAL",  530000),
    ("O2 Extreme      - today's INDEX",    1035000),
]
DURATIONS = [
    ("D1 Transient (2Q)",  2,  "spike mean-reverts, like Aug-2026's -20%/day"),
    ("D2 One year (4Q)",   4,  "war premium persists ~12 months"),
    ("D3 Structural (12Q)", 12, "3 years - but collides with the 2028 supply wall"),
]

# Rough subjective probabilities (stated as judgement, NOT data - see report)
PROB = {
    ("P1", "D1"): 0.06, ("P1", "D2"): 0.05, ("P1", "D3"): 0.03,
    ("P2", "D1"): 0.08, ("P2", "D2"): 0.09, ("P2", "D3"): 0.04,
    ("N",  "D1"): 0.10, ("N",  "D2"): 0.14, ("N",  "D3"): 0.05,
    ("O1", "D1"): 0.11, ("O1", "D2"): 0.09, ("O1", "D3"): 0.03,
    ("O2", "D1"): 0.08, ("O2", "D2"): 0.04, ("O2", "D3"): 0.01,
}


def eps_at(c, spot):
    blended = c["spot"] * spot + (1 - c["spot"]) * c["tc"]
    return (c["days"] * (blended - c["be"]) - c["da"]) / c["sh"], blended


def main():
    norm_eps = {c["name"]: eps_at(c, NORMAL_SPOT)[0] for c in (DHT, FRO)}
    print(f"ASSUMPTIONS: normal spot ${NORMAL_SPOT:,}/day, normal P/E {PE_NORMAL}x")
    print(f"  normalized EPS -> DHT ${norm_eps['DHT']:.2f}, FRO ${norm_eps['FRO']:.2f}")
    print(f"  base (ongoing business) value -> DHT ${norm_eps['DHT']*PE_NORMAL:.2f}, "
          f"FRO ${norm_eps['FRO']*PE_NORMAL:.2f}\n")

    rows = []
    for rlab, spot in RATES:
        rcode = rlab.split()[0]
        for dlab, nq, dnote in DURATIONS:
            dcode = dlab.split()[0]
            for c in (DHT, FRO):
                se, blended = eps_at(c, spot)
                ne = norm_eps[c["name"]]
                base = ne * PE_NORMAL
                excess = (nq / 4.0) * (se - ne)          # windfall cash at 1.0x
                value = base + excess
                implied_pe = value / se if se > 0 else float("nan")
                rows.append(dict(
                    rate_scn=rcode, rate_label=rlab, spot=spot, dur=dcode, quarters=nq,
                    ticker=c["name"], blended_TCE=round(blended),
                    spike_EPS=round(se, 2), normal_EPS=round(ne, 2),
                    base_value=round(base, 2), windfall=round(excess, 2),
                    fair_value=round(value, 2),
                    implied_peak_PE=round(implied_pe, 2),
                    px=c["px"], upside_pct=round((value / c["px"] - 1) * 100),
                    prob=PROB[(rcode, dcode)]))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "capstone_matrix.csv"), index=False)

    for t in ["DHT", "FRO"]:
        d = df[df.ticker == t]
        print("=" * 108)
        print(f"{t}  (price ${d.px.iloc[0]})   — 15 combinations")
        print("=" * 108)
        print(f"{'rate scenario':<34}{'dur':<6}{'spikeEPS':>9}{'base':>8}{'windfall':>9}"
              f"{'FAIR':>8}{'impPE':>7}{'upside':>8}{'prob':>6}")
        for _, r in d.iterrows():
            star = " *" if r.prob >= 0.11 else "  "
            print(f"{r.rate_label:<34}{r.dur:<6}{r.spike_EPS:>9.2f}{r.base_value:>8.2f}"
                  f"{r.windfall:>9.2f}{r.fair_value:>8.2f}{r.implied_peak_PE:>7.2f}"
                  f"{r.upside_pct:>7.0f}%{r.prob:>6.0%}{star}")
        ev = (d.fair_value * d.prob).sum() / d.prob.sum()
        print(f"  --> probability-weighted fair value: ${ev:.2f}  "
              f"vs price ${d.px.iloc[0]}  ({(ev/d.px.iloc[0]-1)*100:+.0f}%)")
        print()

    print("MODAL (highest-probability) scenario: N + D2 = $300k spot sustained ~1 year (14%)")
    m = df[(df.rate_scn == "N") & (df.dur == "D2")]
    for _, r in m.iterrows():
        print(f"  {r.ticker}: fair ${r.fair_value:.2f} vs ${r.px} = {r.upside_pct:+.0f}%  "
              f"(implied peak P/E {r.implied_peak_PE:.2f}x)")
    print(f"\nCSV -> {OUT}")


if __name__ == "__main__":
    main()

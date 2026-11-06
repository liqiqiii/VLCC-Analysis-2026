"""Reproduce the computed numbers in reports #49/#50 (PAG track record and playbook).

Inputs are reported figures (see data/sources.csv rows S44+). Outputs are gross
deal-level arithmetic [E]: no fees, carry, FX hedging, leverage or holding-period
adjustments, so they are NOT fund returns.
Run: python pag_distressed/run_track_record.py
"""


def gross_multiples():
    print("=== A. Gross deal-level multiples (reported entry -> reported proceeds) ===")
    cases = [
        ("[Newbridge, pre-PAG] Korea First Bank (KRW bn)", 500, 1650, "S40"),
        ("[PAG] China Music Corp -> TME (US$m)", 137, 2600, "S48"),
        ("[not PAG] Goldman/ICBC, comparison (US$m)", 2582.2, 10100, "S22"),
    ]
    for name, cost, proceeds, src in cases:
        print(f"{name:40s} {proceeds/cost:5.1f}x  [{src}]")
    usj_cost_usd_m, usj_claimed_proceeds, usj_claimed_mult = 242, 1250, 9.42
    print(f"USJ consistency check only: Y25bn (~US${usj_cost_usd_m}m) -> unverified US${usj_claimed_proceeds}m = "
          f"{usj_claimed_proceeds/usj_cost_usd_m:.1f}x, inconsistent with the claimed {usj_claimed_mult}x [S44/S45]")
    print()


def yingde():
    print("=== B. Yingde / Baosteel Gases -> AirPower (entry cost only; exit equity not disclosed) ===")
    yingde_equity_hkd = 11.3e9          # HK$6/share, 100% equity value (AVCJ)
    hkd_per_usd = 7.77                  # approx. 2017
    baosteel_rmb = 4.166e9              # 51% Baosteel Gases, Aug-2018 auction
    rmb_per_usd = 6.85                  # approx. Aug-2018
    y_usd = yingde_equity_hkd / hkd_per_usd
    b_usd = baosteel_rmb / rmb_per_usd
    print(f"Yingde 100% equity at offer price ~US${y_usd/1e9:.2f}bn (PAG acquired ~98%); Baosteel 51% ~US${b_usd/1e9:.2f}bn; "
          f"aggregate transaction equity consideration ~US${(y_usd+b_usd)/1e9:.2f}bn "
          "(not PAG-funded capital; excludes debt, co-investors, later capex and bolt-ons)")
    print(f"Baosteel 51%: RMB 4.166bn vs RMB 1.956bn reserve price = {4.166/1.956:.2f}x the floor (competitive auction)")
    print("Exit: industrial-gas business sold at a reported US$6.8bn EV; PAG keeps ~25% + clean energy (>US$2bn reported).")
    print("Equity proceeds and net debt NOT disclosed -> the '8x' claim cannot be reproduced.")
    print()


def lexmark():
    print("=== C. Lexmark (minority with an exit right) ===")
    pag_in, pag_pct = 652e6, 0.4294
    ev_2016, ev_sale = 3.9e9, 1.5e9
    claim = 689e6
    print(f"PAG US${pag_in/1e6:.0f}m for {pag_pct:.2%} of the JV; 2016 deal EV ~US${ev_2016/1e9:.1f}bn")
    print(f"Xerox (closed 1-Jul-2025): US${ev_sale/1e9:.1f}bn incl. net debt and assumed liabilities = "
          f"{ev_sale/ev_2016-1:+.0%} vs the 2016 EV. Equity consideration US$70.6m is a different layer (no conflict)")
    print(f"PAG's stake had already fallen to 32.02% via earlier repurchases -> PAG's lifetime result is unknown")
    print(f"PAG's HKIAC claim US${claim/1e6:.0f}m = {claim/pag_in:.2f}x its original cheque (alleged, not adjudicated)")
    print()


def goldin():
    print("=== D. Goldin Financial Global Centre (bought from receivers, Jan-2023) ===")
    price, debt, failed, nla = 5.6e9, 6.8e9, 6.7e9, 886_703
    print(f"HK${price/1e9:.1f}bn = {price/debt-1:+.0%} vs the HK${debt/1e9:.1f}bn secured debt; "
          f"{price/failed-1:+.0%} vs the failed Sep-2022 sale; HK${price/nla:,.0f}/sq ft")
    print()


def fund_level():
    print("=== E. Fund-level net results: UNVERIFIED aggregator data (Seedtable; Asia I as of 30-Sep-2025, II/III 31-Dec-2025) ===")
    for f, v, irr, tvpi, dpi in [("PAG Asia I", 2012, "~17%", 1.80, 1.75),
                                 ("PAG Asia II", 2016, "~9%", 1.60, 0.99),
                                 ("PAG Asia III", 2019, "~9%", 1.40, 0.37)]:
        print(f"{f:12s} vintage {v}: net IRR {irr:>5s}, TVPI {tvpi:.2f}x, DPI {dpi:.2f}x")
    print("Printed inputs only; not benchmarked against vintage peers, so no 'above/below average' verdict.")
    print()


def sapporo():
    print("=== F. Sapporo Real Estate (PAG + KKR, Dec-2025) ===")
    ev_jpy = 477e9
    tranches = [(2026, 0.51), (2028, 0.29), (2029, 0.20)]
    print(f"EV Y{ev_jpy/1e9:.0f}bn; staged equity transfer " + ", ".join(f"{y}: {p:.0%}" for y, p in tranches)
          + f" (sums to {sum(p for _, p in tranches):.0%})")


if __name__ == "__main__":
    gross_multiples()
    yingde()
    lexmark()
    goldin()
    fund_level()
    sapporo()

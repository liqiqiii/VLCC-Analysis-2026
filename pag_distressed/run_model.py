"""Reproduce the numbers in reports #47/#48 (PAG distressed-asset playbook).

Every input is tagged with its source in data/sources.csv. Outputs are the
author's own arithmetic [E] unless stated. Revised after the gpt-6-astra review.
Run: python pag_distressed/run_model.py
"""

FX_DEAL = 0.85621    # RMB per HK$, PBOC rate 28-Oct-2026 used in the joint announcement (EN p.8)
FX_4NOV = 0.85009    # RMB per HK$, Yahoo HKDCNY=X close 4-Nov-2026
FX_NAV = 0.90322     # RMB per HK$, 31-Dec-2025 rate used only for the announcement's NAV comparison

SHARES = 10_810_811_000
NP_FY2025 = 986.573e6                         # RMB, attributable, FY2025
NP_H1_2026, NP_H1_2025 = 517.032e6, 472.272e6  # RMB, attributable, interim report
NP_TTM = NP_FY2025 - NP_H1_2025 + NP_H1_2026


def wanda_headline_proxies():
    print("=== A. Wanda: headline transaction-implied proxies (NOT like-for-like) ===")
    v2021 = 38.0 / 0.2117   # RMB bn; denominator includes management holders (The Paper)
    v2024 = 60.0 / 0.60     # RMB bn; new holdco Dalian Xindameng
    np2021, np2023e, div2023e = 5.3, 9.5, 8.5   # 2023 figures are Dec-2023 ESTIMATES
    print(f"2021 proxy RMB {v2021:,.1f}bn -> {v2021/np2021:.1f}x 2021 NPAT")
    print(f"2024 proxy RMB {v2024:,.1f}bn -> {v2024/np2023e:.1f}x 2023E NPAT; {div2023e/v2024:.1%} on 2023E dividends")
    print(f"Proxy change {v2024/v2021-1:+.0%}; NPAT change (2021 actual -> 2023E) {np2023e/np2021-1:+.0%}")
    print("PAG 2021 US$2.8bn = US$1.9bn equity + US$0.933bn syndicated loan (Reuters);"
          f" funding/stake ratio US$1.9bn/6.4285% = US${1.9/0.064285:.1f}bn -- NOT a valuation reconciliation")
    print()


def evergrande_services():
    print("=== B. Evergrande Property Services (6666.HK) ===")
    sale_ceg, sale_eg = 5_368_074_000, 147_155_000
    px_ceg, px_eg, offer = 0.7271, 0.8359, 0.8359
    side_hkd = 500e6 / FX_DEAL
    consideration = sale_ceg * px_ceg + sale_eg * px_eg
    all_in = consideration + side_hkd
    sale = sale_ceg + sale_eg
    print(f"Block: {sale/SHARES:.3%} for HK${consideration/1e9:.3f}bn; RMB500m side payment = HK${side_hkd/1e6:.1f}m at deal FX")
    print(f"CEG effective price {px_ceg + side_hkd/sale_ceg:.7f}; all-in HK${all_in/1e9:.4f}bn = HK${all_in/sale:.6f}/share")
    print(f"Check: at NAV-date FX the side payment would be HK${500e6/FX_NAV/1e6:.1f}m (wrong basis)")
    print(f"Offer values 100% at HK${SHARES*offer/1e9:.2f}bn")
    print(f"Attributable profit FY2025 RMB {NP_FY2025/1e6:.1f}m; TTM to Jun-2026 RMB {NP_TTM/1e6:.1f}m")
    for label, px, fx in [("offer 0.8359 @ deal FX", offer, FX_DEAL), ("4-Nov close 0.945 @ 4-Nov FX", 0.945, FX_4NOV)]:
        mcap_rmb = px * SHARES * fx
        print(f"  {label:30s} mcap RMB {mcap_rmb/1e9:.2f}bn | P/E FY2025 {mcap_rmb/NP_FY2025:.2f}x | P/E TTM {mcap_rmb/NP_TTM:.2f}x")
    cash_jun, fvpl_jun = 3.6917e9, 0.425e9
    print(f"Jun-2026: cash RMB {cash_jun/1e9:.2f}bn (Dec-2025 4.19bn); H1 OCF RMB 81.9m vs attributable profit RMB 517.0m "
          f"= {81.9/517.0:.0%} conversion (seasonal; not an annual measure)")
    mcap_offer = offer * SHARES * FX_DEAL
    print(f"Subordinate only: (offer mcap - all reported cash)/TTM profit = {(mcap_offer-cash_jun)/NP_TTM:.1f}x "
          "-- NOT a surplus-cash multiple (net current assets only RMB 645m)")
    print()
    print("EPS x multiple sensitivity (HK$ per share; TTM EPS at 4-Nov FX, no dividends, no special payout):")
    eps = NP_TTM / SHARES / FX_4NOV
    print(f"  TTM EPS HK${eps:.4f}")
    mults = (6, 7.5, 9, 11)
    print("  EPS chg | " + " | ".join(f"{m}x" for m in mults))
    for g in (-0.2, -0.1, 0.0, 0.1):
        row = [f"{eps*(1+g)*m:.2f} ({eps*(1+g)*m/0.945-1:+.0%})" for m in mults]
        print(f"  {g:+.0%}    | " + " | ".join(row))
    print()


def mall_stack_hypothetical():
    print("=== C. Hypothetical fixed-priority stack: 50 = 5 junior + 15 mezz + 30 senior (planned, anonymous source) ===")
    price, junior, claims = 50.0, 5.0, 45.0
    print(f"Assets/junior {price/junior:.0f}x; senior+mezz claims/junior {claims/junior:.0f}x; bank debt/value {30/price:.0%}")
    print("NOI yield on price is NOT disclosed; the reported 6-8% is an analyst's estimated annual RETURN, not a cap rate.")
    print("Junior value as multiple of 5bn if NOI and exit cap are as below (ignores capex, fees, tax, amortisation, holding period):")
    print("  hyp. NOI yield | exit 5.0% | exit 5.5% | exit 6.5% | exit 8.0%")
    for y in (0.05, 0.06, 0.07):
        noi = price * y
        print(f"  {y:.0%} (RMB {noi:.1f}bn) | " + " | ".join(f"{max(noi/c-claims,0)/junior:5.2f}x" for c in (0.05, 0.055, 0.065, 0.08)))
    print(f"At an unchanged cap rate, an NOI decline of {1-claims/price:.0%} erases the junior tranche.")
    print()


def bank_strategic_investors():
    print("=== D. Strategic investors (prospectus figures as cited by the review) ===")
    icbc_rmb_ps = 2582.2e6 * 8.0304 / 16_476_014_155
    boc_usd_ps = 3.048e9 / 20_942_736_236
    print(f"Goldman/ICBC: US$2,582.2m for 16,476,014,155 shares at RMB8.0304/US$ -> RMB {icbc_rmb_ps:.4f}/share (1.22x P/B)")
    print(f"RBS consortium/BOC: US$3.048bn for 20,942,736,236 shares -> US${boc_usd_ps:.5f}/share (1.17x 2004 book)")
    print(f"Goldman/ICBC gross sale proceeds / cost = {10.1/2.5822:.1f}x (not net profit, not fund MOIC)")
    print("KFB: Newbridge 51% for KRW500bn; ~48.6% sold for ~KRW1.65tn -> "
          f"{1650/500:.1f}x gross won proceeds/cost (net fund return unknown)")
    print()


def mitsui_fudosan_prices():
    print("=== E. Mitsui Fudosan 8801.T split-adjusted closes (Yahoo) ===")
    lo03, hi07, lo08, hi26 = 196.00, 1303.33, 356.67, 2147.50
    print(f"11-Apr-2003 {lo03} -> 4-Jun-2007 {hi07}: {hi07/lo03:.2f}x; -> 20-Nov-2008 {lo08}: {lo08/hi07-1:+.0%}; "
          f"-> 12-Feb-2026 {hi26}: {hi26/lo03:.1f}x (nominal, price only)")


if __name__ == "__main__":
    wanda_headline_proxies()
    evergrande_services()
    mall_stack_hypothetical()
    bank_strategic_investors()
    mitsui_fudosan_prices()

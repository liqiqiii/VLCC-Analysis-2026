"""Reproduce the October 12, 2026 DHT/FRO P/E fact-check without dependencies.

Source links, disclosure dates, and scenario limitations are in report_en.md
and report_cn.md. Inputs are a dated snapshot, not a live-data feed.
"""

from decimal import Decimal
import json


D = Decimal
PRICE = D("26.22")
SHARES = D("161235573")
REVENUE_DAYS = D("2055")
COVERED_FRACTION = D("0.78")
COVERED_TCE = D("225200")
POST_TCE_COSTS = D("60000000")
MILLION = D("1000000")


def q4_profit(unbooked_tce):
    return (
        REVENUE_DAYS
        * (COVERED_FRACTION * COVERED_TCE + (1 - COVERED_FRACTION) * unbooked_tce)
        - POST_TCE_COSTS
    )


def calculate():
    market_cap = PRICE * SHARES
    reported_ttm = sum(map(D, ("44.8", "66.1", "164.5", "198.3"))) * MILLION
    q3_before_sale_gain_proxy = REVENUE_DAYS * D("141300") - POST_TCE_COSTS
    q3_reported_proxy = q3_before_sale_gain_proxy + D("34.2") * MILLION
    q4_user_case = D("520") * MILLION
    fy2026_proxy = (D("164.5") + D("198.3")) * MILLION + q3_reported_proxy + q4_user_case
    uncovered_days = REVENUE_DAYS * (1 - COVERED_FRACTION)
    required_tce = (
        q4_user_case + POST_TCE_COSTS - REVENUE_DAYS * COVERED_FRACTION * COVERED_TCE
    ) / uncovered_days
    scenarios = []
    for rate in map(D, ("100000", "150000", "250000", "350000", "500000")):
        profit = q4_profit(rate)
        scenarios.append(
            {
                "unbooked_tce_usd_per_day": rate,
                "q4_profit_usd_m": profit / MILLION,
                "q4_eps_usd": profit / SHARES,
                "annualized_q4_pe": market_cap / (4 * profit),
            }
        )
    fro_high = D("72.36")
    fro_q2_eps = D("4.25")
    fro_ex_identified_gains_eps = D("163000000") / D("74837257")
    return {
        "as_of": "2026-10-12",
        "reference_price_usd": PRICE,
        "last_reported_shares": SHARES,
        "market_cap_usd_m": market_cap / MILLION,
        "q4_revenue_days_proxy": REVENUE_DAYS,
        "q4_post_tce_cost_assumption_usd_m": POST_TCE_COSTS / MILLION,
        "q2_post_tce_cost_reference_usd_m": sum(map(D, ("18.6", "27.8", "5.6", "4.8"))),
        "q4_covered_tce_revenue_proxy_usd_m": REVENUE_DAYS * COVERED_FRACTION * COVERED_TCE / MILLION,
        "q4_uncovered_days_proxy": uncovered_days,
        "q4_scenarios": scenarios,
        "q4_profit_sensitivity_per_100k_tce_usd_m": uncovered_days * D("100000") / MILLION,
        "unbooked_tce_for_520m_profit": required_tce,
        "reported_ttm_profit_usd_m": reported_ttm / MILLION,
        "reported_ttm_pe_approx": market_cap / reported_ttm,
        "q3_net_profit_before_sale_gain_proxy_usd_m": q3_before_sale_gain_proxy / MILLION,
        "q3_reported_profit_proxy_usd_m": q3_reported_proxy / MILLION,
        "fy2026_profit_with_520m_q4_usd_m": fy2026_proxy / MILLION,
        "fy2026_pe_with_520m_q4": market_cap / fy2026_proxy,
        "annualized_pe_with_520m_q4": market_cap / (4 * q4_user_case),
        "hypothetical_520m_q4_eps": q4_user_case / SHARES,
        "hypothetical_520m_quarter_earnings_yield_pct": 100 * q4_user_case / market_cap,
        "fro_filed_year_end_pe": {"2007": D("6.3"), "2008": D("3.2")},
        "fro_q2_2008_high_price": fro_high,
        "fro_high_over_annualized_q2_earnings_hindsight": fro_high / (4 * fro_q2_eps),
        "fro_high_over_annualized_q2_ex_identified_gains_hindsight": fro_high / (4 * fro_ex_identified_gains_eps),
        "fro_march_2009_low_over_fy2008_eps": D("15.78") / D("9.15"),
        "fro_march_2009_high_over_fy2008_eps": D("20.75") / D("9.15"),
        "fro_q2_identified_gains_share_pct": 100 * D("155.4") / D("318.4"),
    }


def decimal_string(value):
    if isinstance(value, Decimal):
        return format(value.quantize(D("0.0001")), "f")
    raise TypeError(f"Cannot serialize {type(value).__name__}")


if __name__ == "__main__":
    print(json.dumps(calculate(), default=decimal_string, indent=2))

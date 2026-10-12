"""Static/dynamic P/E labels and conditional term-charter earnings, using snapshots.

No live market data or confirmed company-profit floor is implied. All monetary
inputs and source limitations are documented in charter_anchor_en.md / _cn.md.
"""

import csv
from datetime import date
from decimal import Decimal as D
import json
from pathlib import Path

import run_analysis


HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
MILLION = D("1000000")


def calendar_hire_split(start, end, daily_hire):
    """Allocate an illustrative on-hire interval [start, end) by calendar year."""
    if end <= start or daily_hire < 0:
        raise ValueError("A positive charter interval and nonnegative hire are required")
    rows = []
    for year in range(start.year, end.year + 1):
        days = max(0, (min(end, date(year + 1, 1, 1)) - max(start, date(year, 1, 1))).days)
        if days:
            rows.append({"year": year, "days": days, "gross_hire_m": f"{days * daily_hire / MILLION:.2f}"})
    return rows


def ship_profit(daily_hire, paid_days, assumptions):
    if daily_hire < 0 or not 0 <= paid_days <= assumptions["calendar_days"]:
        raise ValueError("Daily hire must be nonnegative and paid days within the modeled year")
    gross = daily_hire * paid_days
    commissions = gross * D(assumptions["commission_fraction"])
    owner_costs = (
        D(assumptions["opex_per_calendar_day"]) * assumptions["calendar_days"]
        + D(assumptions["annual_depreciation"])
        + D(assumptions["annual_interest"])
        + D(assumptions["annual_allocated_ga"])
        + D(assumptions["annual_tax"])
    )
    return {
        "daily_hire": str(daily_hire),
        "paid_days": str(paid_days),
        "gross_hire_m": f"{gross / MILLION:.4f}",
        "commissions_m": f"{commissions / MILLION:.4f}",
        "other_accounting_costs_m": f"{owner_costs / MILLION:.4f}",
        "illustrative_profit_m": f"{(gross - commissions - owner_costs) / MILLION:.4f}",
    }


def calculate():
    inputs = json.loads((DATA / "charter_anchor_inputs.json").read_text())
    historical = json.loads((DATA / "fro_earnings_2006_2009.json").read_text())
    with (DATA / "fro_quarterly_pe_2007_2009.csv").open(newline="") as handle:
        previous = list(csv.DictReader(handle))
    if len(previous) != len(historical["quarters"]):
        raise ValueError("Historical price and earnings rows must align")
    pe_rows = []
    last_public_quarter_eps = D("1.80")
    for row, q in zip(previous, historical["quarters"]):
        if row["quarter"] != q["quarter"]:
            raise ValueError("Historical quarter mismatch")
        previous_year = str(int(q["quarter"][:4]) - 1)
        static_eps = (
            D("7.68") if q["quarter"] == "2008Q1"
            else D(historical["annual"][previous_year]["basic_eps"])
        )
        price = D(row["original_close"])
        ttm_eps = D(row["lag_ttm_eps_approx"])
        annualized_eps = last_public_quarter_eps * 4
        pe_rows.append(
            {
                "quarter": row["quarter"],
                "original_close": row["original_close"],
                "latest_annual_eps_approx": f"{static_eps:.2f}",
                "static_pe_approx": f"{price / static_eps:.2f}",
                "ttm_pe_reporting_lag_approx": row["reporting_lag_pe_approx"],
                "latest_quarter_eps_initial": f"{last_public_quarter_eps:.2f}",
                "annualized_latest_quarter_pe_approx": f"{price / annualized_eps:.2f}",
                "annualized_to_ttm_earnings_ratio": f"{annualized_eps / ttm_eps:.4f}",
            }
        )
        last_public_quarter_eps = D(q["basic_eps"])
    profit_rows = [
        ship_profit(rate, days, inputs["profit_example"])
        for rate in map(D, ("100000", "230000", "250000"))
        for days in (365, 350)
    ]
    cost = inputs["profit_example"]
    fixed_costs = (
        D(cost["opex_per_calendar_day"]) * cost["calendar_days"]
        + sum(D(cost[key]) for key in ("annual_depreciation", "annual_interest", "annual_allocated_ga", "annual_tax"))
    )
    required_hire = (D("80000000") + fixed_costs) / (D("365") * (1 - D(cost["commission_fraction"])))
    dht = run_analysis.calculate()
    summary = {
        "reference_price": "26.22",
        "dht_static_pe_at_reference": f"{D('26.22') / D('1.31'):.4f}",
        "dht_ttm_pe_at_reference": f"{dht['reported_ttm_pe_approx']:.4f}",
        "dht_latest_reported_quarter_annualized_pe": f"{D('26.22') / (4 * D('1.23')):.4f}",
        "dht_hypothetical_q4_annualized_pe": f"{dht['annualized_pe_with_520m_q4']:.4f}",
        "dht_fy2026_scenario_pe": f"{dht['fy2026_pe_with_520m_q4']:.4f}",
        "dht_actual_ntm_charter_supported_pe": None,
        "hypothetical_250k_calendar_split": calendar_hire_split(
            date(2026, 10, 1), date(2027, 10, 1), D("250000")
        ),
        "daily_hire_required_for_80m_at_365_paid_days": f"{required_hire:.2f}",
        "three_year_100k_gross_hire_m": "109.5000",
        "fearnleys_1year_assessment": "230000",
        "fearnleys_weekly_change": "45000",
        "fearnleys_prior_assessment_implied": "185000",
        "hypothetical_matched_250k_1year_100k_3year_later_average": "25000",
        "term_curve_warning": "The later-average illustration is undiscounted and requires identical vessel, date, terms and immediate start. The actual observations are not matched; do not infer this forward rate from them.",
    }
    return inputs, pe_rows, profit_rows, summary


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    _, pe, profit, summary = calculate()
    write_csv(DATA / "fro_static_dynamic_pe.csv", pe)
    write_csv(DATA / "single_ship_charter_scenarios.csv", profit)
    (DATA / "charter_anchor_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"summary": summary, "single_ship_scenarios": profit, "historical_pe": pe}, indent=2))

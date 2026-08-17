"""
Bellevue buy-vs-rent terminal-wealth model.

The model compares:
1. A buyer who puts $900K down on a $1.8M home and pays ownership cash costs.
2. A renter who invests the retained down payment, avoided purchase costs, and
   each year's ownership-minus-rent cash-flow difference.

Opportunity cost is NOT added separately to the terminal model because the
renter's invested portfolio already captures it.

Run:
    python housing/run_buy_vs_rent.py

Outputs:
    housing/data/rent_scenarios.csv
    housing/data/appreciation_sensitivity.csv
    housing/data/transaction_sensitivity.csv
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"


@dataclass(frozen=True)
class Assumptions:
    home_price: float = 1_800_000
    down_payment: float = 900_000
    mortgage_rate: float = 0.06
    mortgage_years: int = 30
    holding_years: int = 7
    after_tax_investment_return: float = 0.04
    purchase_cost_rate: float = 0.01
    sale_cost_rate: float = 0.07
    annual_property_tax: float = 15_400
    annual_insurance: float = 4_000
    annual_maintenance: float = 13_500
    standard_deduction: float = 32_200
    effective_marginal_tax_rate: float = 0.20
    mortgage_interest_debt_cap: float = 750_000

    @property
    def mortgage_principal(self) -> float:
        return self.home_price - self.down_payment


def mortgage_payment(assumptions: Assumptions) -> float:
    monthly_rate = assumptions.mortgage_rate / 12
    periods = assumptions.mortgage_years * 12
    principal = assumptions.mortgage_principal
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -periods)


def mortgage_year(
    opening_balance: float,
    monthly_payment: float,
    annual_rate: float,
) -> tuple[float, float, float]:
    balance = opening_balance
    interest = 0.0
    monthly_rate = annual_rate / 12

    for _ in range(12):
        monthly_interest = balance * monthly_rate
        principal_payment = monthly_payment - monthly_interest
        interest += monthly_interest
        balance -= principal_payment

    average_balance = (opening_balance + balance) / 2
    return balance, interest, average_balance


def tax_benefit(
    interest: float,
    average_balance: float,
    property_tax: float,
    standard_deduction: float,
    assumptions: Assumptions,
) -> float:
    deductible_share = min(
        1.0,
        assumptions.mortgage_interest_debt_cap / average_balance,
    )
    deductible_interest = interest * deductible_share
    incremental_itemized_deduction = max(
        0.0,
        deductible_interest + property_tax - standard_deduction,
    )
    return incremental_itemized_deduction * assumptions.effective_marginal_tax_rate


def terminal_comparison(
    monthly_rent: float,
    appreciation_rate: float,
    assumptions: Assumptions,
    rent_growth: float = 0.0,
    expense_growth: float = 0.0,
    standard_deduction_growth: float = 0.0,
) -> dict[str, float]:
    payment = mortgage_payment(assumptions)
    balance = assumptions.mortgage_principal
    renter_portfolio = (
        assumptions.down_payment
        + assumptions.home_price * assumptions.purchase_cost_rate
    )
    annual_rent = monthly_rent * 12
    property_tax = assumptions.annual_property_tax
    insurance = assumptions.annual_insurance
    maintenance = assumptions.annual_maintenance
    standard_deduction = assumptions.standard_deduction

    first_year_interest = 0.0
    first_year_principal = 0.0
    first_year_tax_benefit = 0.0

    for year in range(assumptions.holding_years):
        opening_balance = balance
        balance, interest, average_balance = mortgage_year(
            balance,
            payment,
            assumptions.mortgage_rate,
        )
        annual_tax_benefit = tax_benefit(
            interest,
            average_balance,
            property_tax,
            standard_deduction,
            assumptions,
        )
        owner_cash_cost = (
            payment * 12
            + property_tax
            + insurance
            + maintenance
            - annual_tax_benefit
        )
        renter_portfolio = (
            renter_portfolio
            * (1 + assumptions.after_tax_investment_return)
            + owner_cash_cost
            - annual_rent
        )

        if year == 0:
            first_year_interest = interest
            first_year_principal = opening_balance - balance
            first_year_tax_benefit = annual_tax_benefit

        annual_rent *= 1 + rent_growth
        property_tax *= 1 + expense_growth
        insurance *= 1 + expense_growth
        maintenance *= 1 + expense_growth
        standard_deduction *= 1 + standard_deduction_growth

    sale_price = assumptions.home_price * (
        1 + appreciation_rate
    ) ** assumptions.holding_years
    owner_terminal_wealth = (
        sale_price * (1 - assumptions.sale_cost_rate) - balance
    )
    terminal_gap = renter_portfolio - owner_terminal_wealth

    monthly_rate = assumptions.after_tax_investment_return / 12
    months = assumptions.holding_years * 12
    monthly_future_value_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    equivalent_monthly_premium = terminal_gap / monthly_future_value_factor

    return {
        "monthly_rent": monthly_rent,
        "appreciation_rate": appreciation_rate,
        "renter_terminal_wealth": renter_portfolio,
        "owner_terminal_wealth": owner_terminal_wealth,
        "terminal_gap_renter_minus_owner": terminal_gap,
        "equivalent_monthly_ownership_premium": equivalent_monthly_premium,
        "ending_mortgage_balance": balance,
        "first_year_interest": first_year_interest,
        "first_year_principal": first_year_principal,
        "first_year_tax_benefit": first_year_tax_benefit,
    }


def break_even_appreciation(
    monthly_rent: float,
    assumptions: Assumptions,
    rent_growth: float = 0.0,
    expense_growth: float = 0.0,
    standard_deduction_growth: float = 0.0,
) -> float:
    comparison = terminal_comparison(
        monthly_rent,
        0.0,
        assumptions,
        rent_growth,
        expense_growth,
        standard_deduction_growth,
    )
    required_terminal_price_factor = (
        comparison["renter_terminal_wealth"]
        + comparison["ending_mortgage_balance"]
    ) / (
        assumptions.home_price * (1 - assumptions.sale_cost_rate)
    )
    return (
        required_terminal_price_factor ** (1 / assumptions.holding_years) - 1
    )


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    assumptions = Assumptions()

    rent_rows = []
    for monthly_rent in (4_300, 5_200, 6_000, 8_000):
        at_three_percent = terminal_comparison(
            monthly_rent,
            0.03,
            assumptions,
        )
        rent_rows.append({
            "monthly_rent": monthly_rent,
            "annual_rent": monthly_rent * 12,
            "break_even_appreciation_pct": round(
                break_even_appreciation(monthly_rent, assumptions) * 100,
                3,
            ),
            "premium_at_3pct_appreciation_monthly": round(
                at_three_percent["equivalent_monthly_ownership_premium"],
                0,
            ),
            "terminal_gap_at_3pct": round(
                at_three_percent["terminal_gap_renter_minus_owner"],
                0,
            ),
        })
    write_csv(DATA_DIR / "rent_scenarios.csv", rent_rows)

    matched_home_break_even = break_even_appreciation(5_200, assumptions)
    appreciation_rows = []
    for appreciation in (
        0.00,
        0.02,
        0.03,
        0.04,
        matched_home_break_even,
        0.05,
    ):
        result = terminal_comparison(5_200, appreciation, assumptions)
        appreciation_rows.append({
            "appreciation_pct": round(appreciation * 100, 3),
            "owner_terminal_wealth": round(result["owner_terminal_wealth"], 0),
            "renter_terminal_wealth": round(result["renter_terminal_wealth"], 0),
            "terminal_gap_renter_minus_owner": round(
                result["terminal_gap_renter_minus_owner"],
                0,
            ),
            "equivalent_monthly_ownership_premium": round(
                result["equivalent_monthly_ownership_premium"],
                0,
            ),
        })
    write_csv(
        DATA_DIR / "appreciation_sensitivity.csv",
        appreciation_rows,
    )

    transaction_rows = []
    for sale_cost_rate in (0.06, 0.07, 0.08):
        scenario = replace(assumptions, sale_cost_rate=sale_cost_rate)
        transaction_rows.append({
            "sale_cost_pct": round(sale_cost_rate * 100, 1),
            "break_even_appreciation_pct": round(
                break_even_appreciation(5_200, scenario) * 100,
                3,
            ),
        })
    write_csv(
        DATA_DIR / "transaction_sensitivity.csv",
        transaction_rows,
    )

    inflation_case = break_even_appreciation(
        5_200,
        assumptions,
        rent_growth=0.03,
        expense_growth=0.03,
        standard_deduction_growth=0.025,
    )
    first_year = terminal_comparison(5_200, 0.03, assumptions)

    print("Bellevue buy-vs-rent model")
    print(f"Monthly mortgage payment: ${mortgage_payment(assumptions):,.2f}")
    print(f"First-year interest: ${first_year['first_year_interest']:,.2f}")
    print(f"First-year principal: ${first_year['first_year_principal']:,.2f}")
    print(f"First-year tax benefit: ${first_year['first_year_tax_benefit']:,.2f}")
    print()
    for row in rent_rows:
        print(
            f"Rent ${row['monthly_rent']:,.0f}: "
            f"break-even appreciation "
            f"{row['break_even_appreciation_pct']:.3f}%; "
            f"premium at 3% appreciation "
            f"${row['premium_at_3pct_appreciation_monthly']:,.0f}/month"
        )
    print(
        "Rent/expenses +3% and standard deduction +2.5%: "
        f"{inflation_case * 100:.3f}% break-even appreciation "
        "at $5,200 starting rent"
    )


if __name__ == "__main__":
    main()

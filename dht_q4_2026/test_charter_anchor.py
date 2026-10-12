"""Read-only checks of charter arithmetic, tenor classification and P/E labels."""

import csv
from datetime import date
from decimal import Decimal as D
import json
import unittest

import run_charter_anchor as anchor


class CharterAnchorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs, cls.pe, cls.profit, cls.summary = anchor.calculate()

    def test_profit_is_not_gross_hire(self):
        row = anchor.ship_profit(D("250000"), 365, self.inputs["profit_example"])
        self.assertEqual(row["gross_hire_m"], "91.2500")
        self.assertEqual(row["illustrative_profit_m"], "78.9594")
        self.assertLess(D(row["illustrative_profit_m"]), D(row["gross_hire_m"]))

    def test_offhire_reduces_revenue_not_calendar_costs(self):
        full = anchor.ship_profit(D("250000"), 365, self.inputs["profit_example"])
        offhire = anchor.ship_profit(D("250000"), 350, self.inputs["profit_example"])
        self.assertEqual(full["other_accounting_costs_m"], offhire["other_accounting_costs_m"])
        self.assertEqual(offhire["illustrative_profit_m"], "75.2562")
        with self.assertRaises(ValueError):
            anchor.ship_profit(D("250000"), 366, self.inputs["profit_example"])

    def test_contract_year_is_not_calendar_year(self):
        split = anchor.calendar_hire_split(date(2026, 10, 1), date(2027, 10, 1), D("250000"))
        self.assertEqual([r["days"] for r in split], [92, 273])
        self.assertEqual([r["gross_hire_m"] for r in split], ["23.00", "68.25"])
        self.assertEqual(sum(r["days"] for r in split), 365)
        with self.assertRaises(ValueError):
            anchor.calendar_hire_split(date(2027, 1, 1), date(2026, 1, 1), D("250000"))

    def test_distinct_pe_denominators(self):
        self.assertEqual(self.summary["dht_static_pe_at_reference"], "20.0153")
        self.assertEqual(self.summary["dht_latest_reported_quarter_annualized_pe"], "5.3293")
        self.assertEqual(self.summary["dht_hypothetical_q4_annualized_pe"], "2.0325")
        self.assertIsNone(self.summary["dht_actual_ntm_charter_supported_pe"])
        by_quarter = {r["quarter"]: r for r in self.pe}
        self.assertEqual(by_quarter["2007Q4"]["annualized_latest_quarter_pe_approx"], "37.50")
        self.assertEqual(by_quarter["2009Q1"]["static_pe_approx"], "1.90")
        self.assertEqual(by_quarter["2009Q1"]["annualized_latest_quarter_pe_approx"], "6.59")
        self.assertEqual(by_quarter["2008Q1"]["latest_annual_eps_approx"], "7.68")

    def test_assessment_is_not_a_signed_fixture(self):
        actuals = self.inputs["recent_contracts"]
        self.assertFalse(any(D(row["daily_hire"]) == 250000 for row in actuals))
        assessed = self.inputs["assessments"][-1]
        self.assertEqual((assessed["date"], assessed["tenor_months"], assessed["daily_hire"]),
                         ("2026-10-07", 12, "230000"))
        historical = {r["vessel"]: r for r in self.inputs["historical_fixtures"]}
        self.assertEqual(historical["Front Champion"]["tenor_months"], 11)
        self.assertEqual(historical["Golden Victory"]["tenor_months"], 16)

    def test_published_artifacts_are_current_without_rewriting(self):
        with (anchor.DATA / "fro_static_dynamic_pe.csv").open(newline="") as handle:
            self.assertEqual(list(csv.DictReader(handle)), self.pe)
        with (anchor.DATA / "single_ship_charter_scenarios.csv").open(newline="") as handle:
            self.assertEqual(list(csv.DictReader(handle)), self.profit)
        self.assertEqual(json.loads((anchor.DATA / "charter_anchor_summary.json").read_text()), self.summary)


if __name__ == "__main__":
    unittest.main()

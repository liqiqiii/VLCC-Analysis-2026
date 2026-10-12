"""Regression checks for historical share basis, EPS bridges and report output."""

import contextlib
import csv
from decimal import Decimal as D
import io
import json
import unittest
import xml.etree.ElementTree as ET

import run_fro_history as history


class HistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            cls.inputs, cls.prices, cls.rows = history.build(write_outputs=False)
        cls.by_quarter = {row["quarter"]: row for row in cls.rows}

    def test_original_share_basis(self):
        for row in self.prices:
            converted = (D(row["vendor_split_adjusted_close"]) / 5).quantize(D("0.01"))
            self.assertEqual(converted, D(row["original_close"]))
            self.assertLessEqual(D(row["original_low"]), converted)
            self.assertGreaterEqual(D(row["original_high"]), converted)

    def test_filed_price_ranges_and_peak_dates(self):
        history.validate_prices(self.prices)
        high = max(self.prices, key=lambda row: D(row["original_high"]))
        close = max(self.prices, key=lambda row: D(row["original_close"]))
        self.assertEqual((high["date"], high["original_high"]), ("2008-06-24", "72.36"))
        self.assertEqual((close["date"], close["original_close"]), ("2008-06-23", "71.76"))

    def test_ten_quarters_and_distinct_denominators(self):
        self.assertEqual(len(self.rows), 10)
        self.assertEqual(self.by_quarter["2008Q2"]["period_ttm_eps_bridge"], "10.20")
        self.assertEqual(self.by_quarter["2008Q2"]["lag_ttm_eps_approx"], "8.45")
        self.assertEqual(self.by_quarter["2009Q1"]["reporting_lag_pe_approx"], "1.90")
        self.assertEqual(self.by_quarter["2009Q1"]["same_year_pe_hindsight"], "13.17")
        self.assertEqual(self.by_quarter["2009Q2"]["period_ttm_pe_hindsight"], "7.43")

    def test_year_end_bridge_and_preliminary_vintage(self):
        for quarter in ("2007Q4", "2008Q4"):
            row = self.by_quarter[quarter]
            self.assertEqual(row["period_ttm_eps_bridge"], row["same_year_final_eps"])
        self.assertEqual(self.by_quarter["2008Q1"]["lag_ttm_eps_approx"], "7.68")
        self.assertEqual(self.inputs["annual"]["2007"]["basic_eps"], "7.62")

    def test_provenance_and_svg(self):
        meta = json.loads((history.DATA / "fro_price_provenance.json").read_text())
        self.assertEqual(meta["rows"], len(self.prices))
        self.assertEqual(meta["split_events"][0]["splitRatio"], "1:5")
        ET.parse(history.HERE / "charts" / "fro_pe_2007_2009.svg")
        self.assertEqual(
            (history.HERE / "charts" / "fro_pe_2007_2009.svg").read_text(),
            history.render_chart(self.rows),
        )
        with (history.DATA / "fro_quarterly_pe_2007_2009.csv").open() as handle:
            self.assertEqual(list(csv.DictReader(handle)), self.rows)

    def test_uncertain_release_dates_are_not_exact_timestamps(self):
        quarters = {row["quarter"]: row for row in self.inputs["quarters"]}
        for key in ("2008Q3", "2009Q1"):
            self.assertIsNone(quarters[key]["release_date"])
            self.assertEqual(len(quarters[key]["release_date_range"]), 2)


if __name__ == "__main__":
    unittest.main()

"""Public behavior checks for the disposable expense-report demonstration."""

import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from expense_report import summarize


class ExpenseReportTests(unittest.TestCase):
    def summarize_rows(self, rows, **options):
        with tempfile.TemporaryDirectory(prefix="test-expense-report-") as directory:
            ledger = Path(directory) / "ledger.csv"
            ledger.write_text("date,category,amount\n" + rows, encoding="utf-8")
            return summarize(ledger, **options)

    def test_whole_amounts_and_refunds(self):
        total, categories = self.summarize_rows(
            "2026-01-01,Hosting,20.00\n2026-01-02,Hosting,-5.00\n"
        )
        self.assertEqual(total, Decimal("15.00"))
        self.assertEqual(categories, {"Hosting": Decimal("15.00")})

    @unittest.expectedFailure
    def test_cents_and_fractional_refunds_are_preserved(self):
        total, categories = self.summarize_rows(
            "2026-01-01,Hosting,19.95\n2026-01-02,Hosting,-4.50\n"
        )
        self.assertEqual(total, Decimal("15.45"))
        self.assertEqual(categories, {"Hosting": Decimal("15.45")})

    @unittest.expectedFailure
    def test_end_date_is_inclusive(self):
        total, categories = self.summarize_rows(
            "2025-12-31,Hosting,100.00\n2026-01-01,Hosting,10.00\n"
            "2026-01-31,Hosting,20.00\n2026-02-01,Hosting,100.00\n",
            start=date(2026, 1, 1), end=date(2026, 1, 31),
        )
        self.assertEqual(total, Decimal("30.00"))
        self.assertEqual(categories, {"Hosting": Decimal("30.00")})

    def test_category_whitespace_and_empty_values(self):
        total, categories = self.summarize_rows(
            "2026-01-01, Hosting ,10.00\n2026-01-02,Hosting,5.00\n"
            "2026-01-03,  ,2.00\n2026-01-04,,3.00\n"
        )
        self.assertEqual(total, Decimal("20.00"))
        self.assertEqual(categories, {"Hosting": Decimal("15.00"), "Uncategorized": Decimal("5.00")})


if __name__ == "__main__":
    unittest.main()

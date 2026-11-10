"""Summarize a CSV expense ledger for the disposable coding demonstration."""

import argparse
import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path


def summarize(path, start=None, end=None):
    """Return the total and category totals for the requested date range."""
    totals = defaultdict(lambda: Decimal("0.00"))
    with Path(path).open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            day = date.fromisoformat(row["date"])
            if start and day < start:
                continue
            if end and day >= end:
                continue
            amount = Decimal(row["amount"])
            category = row["category"]
            totals[category] += amount
    return sum(totals.values(), Decimal("0.00")), dict(totals)


def main():
    parser = argparse.ArgumentParser(description="Summarize a demo expense ledger.")
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--start", type=date.fromisoformat)
    parser.add_argument("--end", type=date.fromisoformat)
    args = parser.parse_args()
    total, categories = summarize(args.ledger, args.start, args.end)
    print("DEMO EXPENSE REPORT")
    print("=" * 44)
    print("Synthetic data. Amounts are in USD.")
    for category, amount in sorted(categories.items()):
        print(f"{category:<28} ${amount:>10.2f}")
    print("-" * 44)
    print(f"{'Total':<28} ${total:>10.2f}")


if __name__ == "__main__":
    main()

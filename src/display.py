"""
display.py - Formatting and display helpers for the CLI.

Keeps all the print logic in one place so tracker.py and main.py
stay focused on behavior, not presentation.
"""

from typing import List
from models import Expense


# Column widths for the expense table
_COL = {"id": 5, "date": 12, "category": 14, "description": 30, "amount": 10}


def _divider() -> str:
    total = sum(_COL.values()) + len(_COL) - 1
    return "-" * total


def print_header() -> None:
    """Print the application banner."""
    print("\n" + "=" * 55)
    print("          EXPENSE TRACKER - CLI Edition")
    print("=" * 55)


def print_expense_table(expenses: List[Expense], title: str = "Expenses") -> None:
    """
    Render a formatted table of expenses to the terminal.

    Args:
        expenses (List[Expense]): Rows to display.
        title (str): Label printed above the table.
    """
    if not expenses:
        print(f"\n  No expenses to show under '{title}'.")
        return

    print(f"\n  {title} ({len(expenses)} record{'s' if len(expenses) != 1 else ''})")
    print("  " + _divider())
    print(
        f"  {'ID':<{_COL['id']}} "
        f"{'Date':<{_COL['date']}} "
        f"{'Category':<{_COL['category']}} "
        f"{'Description':<{_COL['description']}} "
        f"{'Amount':>{_COL['amount']}}"
    )
    print("  " + _divider())

    for e in expenses:
        desc = e.description if len(e.description) <= _COL["description"] else e.description[:27] + "..."
        print(
            f"  {e.expense_id:<{_COL['id']}} "
            f"{e.date:<{_COL['date']}} "
            f"{e.category:<{_COL['category']}} "
            f"{desc:<{_COL['description']}} "
            f"{'₱' + f'{e.amount:,.2f}':>{_COL['amount']}}"
        )

    print("  " + _divider())


def print_summary(total: float, by_category: dict, average: float, count: int) -> None:
    """
    Print a spending summary: total, average, and per-category breakdown.

    Args:
        total (float): Grand total spent.
        by_category (dict): Category -> total mapping.
        average (float): Mean expense amount.
        count (int): Number of expense records.
    """
    print("\n  === SPENDING SUMMARY ===")
    print(f"  Total expenses : {count}")
    print(f"  Total spent    : ₱{total:,.2f}")
    print(f"  Average expense: ₱{average:,.2f}")

    if by_category:
        print("\n  By category:")
        for category, amount in by_category.items():
            bar_len = int((amount / total) * 30) if total > 0 else 0
            bar = "█" * bar_len
            print(f"    {category:<14} ₱{amount:>10,.2f}  {bar}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"\n  [OK] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"\n  [!] {message}")


def print_menu(options: List[str], title: str = "Menu") -> None:
    """
    Print a numbered menu.

    Args:
        options (List[str]): Menu item labels.
        title (str): Menu heading.
    """
    print(f"\n  --- {title} ---")
    for i, option in enumerate(options, start=1):
        print(f"  [{i}] {option}")
    print("  [0] Back / Exit")

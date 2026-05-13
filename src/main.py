"""
main.py - Entry point for the Expense Tracker CLI application.
"""

import sys
from datetime import datetime

from tracker import ExpenseTracker
from models import Expense
from display import (
    print_header,
    print_expense_table,
    print_summary,
    print_success,
    print_error,
    print_menu,
)


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def prompt(label: str, default: str = "") -> str:
    """
    Ask the user for text input and strip whitespace.

    Args:
        label (str): The prompt text shown to the user.
        default (str): Value returned if the user presses Enter with no input.

    Returns:
        str: User-supplied text, or default if blank.
    """
    raw = input(f"  {label}: ").strip()
    return raw if raw else default


def prompt_float(label: str) -> float:
    """
    Ask the user for a positive float. Keeps asking until they get it right.

    Args:
        label (str): The prompt text.

    Returns:
        float: A valid positive number.
    """
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            value = float(raw)
            if value <= 0:
                print_error("Amount must be greater than zero.")
                continue
            return value
        except ValueError:
            print_error(f"'{raw}' is not a valid number. Try again.")


def prompt_date(label: str) -> str:
    """
    Ask the user for a date in YYYY-MM-DD format. Keeps looping on bad input.
    Pressing Enter defaults to today's date.

    Args:
        label (str): Prompt text.

    Returns:
        str: A valid date string in YYYY-MM-DD format.
    """
    today = datetime.today().strftime("%Y-%m-%d")
    while True:
        raw = input(f"  {label} [YYYY-MM-DD, Enter = today ({today})]: ").strip()
        if not raw:
            return today
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print_error(f"'{raw}' doesn't look like a valid date. Use YYYY-MM-DD.")


def prompt_category() -> str:
    """
    Display the category list and prompt the user to pick one by number.

    Returns:
        str: A valid category name from Expense.VALID_CATEGORIES.
    """
    categories = sorted(Expense.VALID_CATEGORIES)
    print("\n  Categories:")
    for i, cat in enumerate(categories, start=1):
        print(f"    [{i}] {cat}")
    while True:
        raw = input("  Choose a category number: ").strip()
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(categories):
                return categories[idx]
            print_error(f"Enter a number between 1 and {len(categories)}.")
        except ValueError:
            print_error("That's not a number. Try again.")


def prompt_int(label: str) -> int:
    """
    Ask for an integer. Keeps looping until the user provides one.

    Args:
        label (str): Prompt text.

    Returns:
        int: The integer the user entered.
    """
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            return int(raw)
        except ValueError:
            print_error(f"'{raw}' is not a valid number.")


# ---------------------------------------------------------------------------
# Feature screens
# ---------------------------------------------------------------------------

def screen_add(tracker: ExpenseTracker) -> None:
    """
    Collect inputs and add a new expense to the tracker.

    Args:
        tracker (ExpenseTracker): The active tracker instance.
    """
    print("\n  --- Add New Expense ---")
    description = prompt("Description")
    if not description:
        print_error("Description cannot be empty.")
        return
    amount = prompt_float("Amount (₱)")
    category = prompt_category()
    date = prompt_date("Date")

    try:
        expense = tracker.add_expense(description, amount, category, date)
        print_success(f"Added: {expense.description} — ₱{expense.amount:,.2f} [{expense.category}]")
    except ValueError as e:
        print_error(str(e))


def screen_delete(tracker: ExpenseTracker) -> None:
    """
    Ask for an expense ID and remove it if it exists.

    Args:
        tracker (ExpenseTracker): The active tracker instance.
    """
    if not tracker.get_all():
        print_error("No expenses to delete.")
        return
    print_expense_table(tracker.get_all(), title="All Expenses")
    expense_id = prompt_int("Enter the ID to delete")
    removed = tracker.delete_expense(expense_id)
    if removed:
        print_success(f"Deleted: '{removed.description}' (₱{removed.amount:,.2f})")
    else:
        print_error(f"No expense found with ID {expense_id}.")


def screen_view(tracker: ExpenseTracker) -> None:
    """
    Display all expenses with sort options.

    Args:
        tracker (ExpenseTracker): The active tracker instance.
    """
    print_menu(
        ["View all (by ID)", "Sort by amount (highest first)", "Sort by date (newest first)", "Sort by category then amount"],
        title="View / Sort"
    )
    choice = input("  Choose: ").strip()

    if choice == "1":
        print_expense_table(tracker.get_all(), title="All Expenses")
    elif choice == "2":
        print_expense_table(tracker.sort_by_amount(), title="Sorted by Amount")
    elif choice == "3":
        print_expense_table(tracker.sort_by_date(), title="Sorted by Date")
    elif choice == "4":
        print_expense_table(tracker.sort_by_category_then_amount(), title="Sorted by Category → Amount")
    else:
        print_error("Invalid choice.")


def screen_filter(tracker: ExpenseTracker) -> None:
    """
    Let the user filter expenses by category, date range, or keyword.

    Args:
        tracker (ExpenseTracker): The active tracker instance.
    """
    print_menu(
        ["Filter by category", "Filter by date range", "Search by description keyword"],
        title="Filter / Search"
    )
    choice = input("  Choose: ").strip()

    if choice == "1":
        used = tracker.categories_used()
        if not used:
            print_error("No expenses recorded yet.")
            return
        print("\n  Categories in use: " + ", ".join(sorted(used)))
        category = prompt("Category name (case-sensitive)")
        results = tracker.filter_by_category(category)
        print_expense_table(results, title=f"Category: {category}")

    elif choice == "2":
        start = prompt_date("Start date")
        end = prompt_date("End date")
        if start > end:
            print_error("Start date must be on or before end date.")
            return
        results = tracker.filter_by_date_range(start, end)
        print_expense_table(results, title=f"{start} to {end}")

    elif choice == "3":
        keyword = prompt("Search keyword")
        if not keyword:
            print_error("Keyword cannot be empty.")
            return
        results = tracker.search_by_description(keyword)
        print_expense_table(results, title=f"Results for '{keyword}'")

    else:
        print_error("Invalid choice.")


def screen_summary(tracker: ExpenseTracker) -> None:
    """
    Print the overall spending summary and top 5 most expensive entries.

    Args:
        tracker (ExpenseTracker): The active tracker instance.
    """
    if not tracker.get_all():
        print_error("No expenses recorded yet.")
        return

    print_summary(
        total=tracker.total_spent(),
        by_category=tracker.spending_by_category(),
        average=tracker.average_expense(),
        count=len(tracker.get_all()),
    )

    print("\n  --- Top 5 Expenses ---")
    print_expense_table(tracker.top_expenses(5), title="Top 5 by Amount")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

MAIN_MENU = [
    "Add expense",
    "View / Sort expenses",
    "Filter / Search expenses",
    "Delete expense",
    "Spending summary",
]


def main() -> None:
    """
    Start the Expense Tracker and run the main menu loop.

    The loop runs until the user enters 0 to exit. Each menu option
    delegates to a dedicated screen function.
    """
    tracker = ExpenseTracker()
    print_header()
    print(f"  {len(tracker.get_all())} expense(s) loaded.\n")

    while True:
        print_menu(MAIN_MENU, title="Main Menu")
        choice = input("  Choose an option: ").strip()

        if choice == "0":
            print("\n  Goodbye. Stay on budget!\n")
            sys.exit(0)
        elif choice == "1":
            screen_add(tracker)
        elif choice == "2":
            screen_view(tracker)
        elif choice == "3":
            screen_filter(tracker)
        elif choice == "4":
            screen_delete(tracker)
        elif choice == "5":
            screen_summary(tracker)
        else:
            print_error(f"'{choice}' is not a valid option. Pick 0–{len(MAIN_MENU)}.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()

"""
tracker.py - Core application logic for the Expense Tracker.

The ExpenseTracker class acts as the controller between the CLI interface
and the storage layer. All business rules (filtering, sorting, summarizing)
live here, keeping main.py thin and readable.
"""

from typing import List, Optional

from models import Expense
from storage import load_expenses, save_expenses, next_id


class ExpenseTracker:
    """
    Manages a collection of Expense objects.

    Loads from and saves to disk automatically. All mutation methods
    (add, delete) persist changes immediately so no data is lost
    if the program exits unexpectedly.

    Attributes:
        expenses (List[Expense]): In-memory list of all expense entries.
    """

    def __init__(self):
        """Load existing expenses from disk on startup."""
        self.expenses: List[Expense] = load_expenses()

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add_expense(self, description: str, amount: float, category: str, date: str) -> Expense:
        """
        Create and store a new expense.

        Args:
            description (str): What the money was spent on.
            amount (float): How much was spent.
            category (str): Spending category.
            date (str): Date in YYYY-MM-DD format.

        Returns:
            Expense: The newly created expense, already saved to disk.

        Raises:
            ValueError: Propagated from Expense.__init__ if inputs are invalid.
        """
        new_expense = Expense(
            expense_id=next_id(self.expenses),
            description=description,
            amount=amount,
            category=category,
            date=date,
        )
        self.expenses.append(new_expense)
        save_expenses(self.expenses)
        return new_expense

    def delete_expense(self, expense_id: int) -> Optional[Expense]:
        """
        Remove an expense by its ID.

        Args:
            expense_id (int): The ID of the expense to delete.

        Returns:
            Optional[Expense]: The deleted expense if found, None otherwise.
        """
        for i, expense in enumerate(self.expenses):
            if expense.expense_id == expense_id:
                removed = self.expenses.pop(i)
                save_expenses(self.expenses)
                return removed
        return None

    def get_all(self) -> List[Expense]:
        """Return a copy of the full expense list, unsorted."""
        return list(self.expenses)

    # ------------------------------------------------------------------
    # Sorting
    # ------------------------------------------------------------------

    def sort_by_amount(self, descending: bool = True) -> List[Expense]:
        """
        Sort expenses by amount using Python's built-in Timsort.

        Args:
            descending (bool): Highest first when True (default).

        Returns:
            List[Expense]: Sorted list; original order on disk is unchanged.
        """
        return sorted(self.expenses, key=lambda e: e.amount, reverse=descending)

    def sort_by_date(self, descending: bool = True) -> List[Expense]:
        """
        Sort expenses by date. Relies on YYYY-MM-DD being lexicographically
        sortable, so no date parsing is needed.

        Args:
            descending (bool): Most recent first when True (default).

        Returns:
            List[Expense]: Sorted list; original order on disk is unchanged.
        """
        return sorted(self.expenses, key=lambda e: e.date, reverse=descending)

    def sort_by_category_then_amount(self) -> List[Expense]:
        """
        Sort by category alphabetically, then by amount descending within
        each category. Useful for spotting which category eats the most.

        Returns:
            List[Expense]: Multi-key sorted list.
        """
        return sorted(self.expenses, key=lambda e: (e.category, -e.amount))

    # ------------------------------------------------------------------
    # Filtering / Search
    # ------------------------------------------------------------------

    def filter_by_category(self, category: str) -> List[Expense]:
        """
        Return only expenses in the given category.

        Args:
            category (str): Category name to filter on (case-sensitive).

        Returns:
            List[Expense]: Matching expenses, or an empty list if none found.
        """
        return [e for e in self.expenses if e.category == category]

    def filter_by_date_range(self, start: str, end: str) -> List[Expense]:
        """
        Return expenses whose date falls within [start, end], inclusive.
        Comparison works because dates are in YYYY-MM-DD format.

        Args:
            start (str): Start date in YYYY-MM-DD format.
            end (str): End date in YYYY-MM-DD format.

        Returns:
            List[Expense]: Expenses within the date range.
        """
        return [e for e in self.expenses if start <= e.date <= end]

    def search_by_description(self, keyword: str) -> List[Expense]:
        """
        Case-insensitive keyword search across expense descriptions.

        Args:
            keyword (str): Term to look for.

        Returns:
            List[Expense]: All expenses whose description contains the keyword.
        """
        keyword_lower = keyword.lower()
        return [e for e in self.expenses if keyword_lower in e.description.lower()]

    # ------------------------------------------------------------------
    # Summary / Analytics
    # ------------------------------------------------------------------

    def total_spent(self) -> float:
        """
        Sum all expense amounts.

        Returns:
            float: Grand total, or 0.0 if no expenses exist.
        """
        return round(sum(e.amount for e in self.expenses), 2)

    def spending_by_category(self) -> dict:
        """
        Aggregate total spending per category.

        Uses a dictionary accumulator pattern: iterate once, build totals.

        Returns:
            dict: Maps category name -> total amount, sorted by total descending.
        """
        totals: dict = {}
        for expense in self.expenses:
            totals[expense.category] = round(
                totals.get(expense.category, 0) + expense.amount, 2
            )
        return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    def top_expenses(self, n: int = 5) -> List[Expense]:
        """
        Return the n most expensive individual entries.

        Args:
            n (int): How many to return. Defaults to 5.

        Returns:
            List[Expense]: Top n expenses by amount, descending.
        """
        return self.sort_by_amount(descending=True)[:n]

    def categories_used(self) -> set:
        """
        Return the set of distinct categories that have at least one expense.

        Returns:
            set: Unique category names in the current data.
        """
        return {e.category for e in self.expenses}

    def average_expense(self) -> float:
        """
        Compute the mean expense amount.

        Returns:
            float: Mean amount, or 0.0 if there are no expenses.
        """
        if not self.expenses:
            return 0.0
        return round(self.total_spent() / len(self.expenses), 2)


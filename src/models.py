"""
models.py - Data model for individual expense entries.

Defines the Expense class that represents a single spending record,
including validation logic and serialization helpers.
"""

from datetime import datetime


class Expense:
    """
    Represents a single expense entry.

    Attributes:
        expense_id (int): Unique identifier for the expense.
        description (str): Short label for what the money was spent on.
        amount (float): How much was spent, in the user's currency.
        category (str): Broad grouping like 'Food', 'Transport', etc.
        date (str): Date of the expense in YYYY-MM-DD format.
    """

    VALID_CATEGORIES = {
        "Food",
        "Transport",
        "Housing",
        "Health",
        "Entertainment",
        "Shopping",
        "Education",
        "Utilities",
        "Other",
    }

    def __init__(self, expense_id: int, description: str, amount: float, category: str, date: str):
        """
        Initialize an Expense instance.

        Args:
            expense_id (int): Unique ID assigned by the tracker.
            description (str): What the expense was for.
            amount (float): Cost of the expense. Must be greater than zero.
            category (str): Must be one of Expense.VALID_CATEGORIES.
            date (str): Date string in YYYY-MM-DD format.

        Raises:
            ValueError: If amount is not positive, category is invalid,
                        or date format is wrong.
        """
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"'{category}' is not a valid category. "
                f"Choose from: {', '.join(sorted(self.VALID_CATEGORIES))}"
            )
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Date '{date}' is not in YYYY-MM-DD format.")

        self.expense_id = expense_id
        self.description = description.strip()
        self.amount = round(amount, 2)
        self.category = category
        self.date = date

    def to_dict(self) -> dict:
        """
        Serialize the expense to a plain dictionary for JSON storage.

        Returns:
            dict: All expense fields as key-value pairs.
        """
        return {
            "expense_id": self.expense_id,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """
        Reconstruct an Expense from a dictionary (e.g., loaded from JSON).

        Args:
            data (dict): Dictionary with keys matching Expense fields.

        Returns:
            Expense: A new Expense instance built from the dictionary.
        """
        return cls(
            expense_id=data["expense_id"],
            description=data["description"],
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
        )

    def __repr__(self) -> str:
        return (
            f"Expense(id={self.expense_id}, '{self.description}', "
            f"₱{self.amount:.2f}, {self.category}, {self.date})"
        )

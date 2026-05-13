"""
storage.py - Handles reading and writing expense data to disk.

Uses JSON as the persistence format. All file I/O goes through
context managers so file handles are always properly closed,
even if something goes wrong mid-operation.
"""

import json
import os
from typing import List

from models import Expense


DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "expenses.json")


def _ensure_data_file() -> None:
    """
    Create the data file and its parent directory if they don't exist yet.
    Called automatically before every read or write.
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_expenses() -> List[Expense]:
    """
    Load all expenses from the JSON data file.

    Returns:
        List[Expense]: Expenses stored on disk, or an empty list if
                       the file is missing or corrupted.
    """
    _ensure_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Expense.from_dict(entry) for entry in raw]


def save_expenses(expenses: List[Expense]) -> None:
    """
    Overwrite the data file with the current list of expenses.

    Args:
        expenses (List[Expense]): The full list to persist.
    """
    _ensure_data_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in expenses], f, indent=2)


def next_id(expenses: List[Expense]) -> int:
    """
    Compute the next available expense ID.

    Args:
        expenses (List[Expense]): Current list of expenses.

    Returns:
        int: One more than the highest existing ID, or 1 if the list is empty.
    """
    if not expenses:
        return 1
    return max(e.expense_id for e in expenses) + 1

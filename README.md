# Expense Tracker CLI

A command-line app for tracking personal expenses. Add spending entries, sort them, filter by category or date, and get a quick summary of where your money is going - all from the terminal, no GUI needed.

---

## Features

- **Add expenses** - description, amount, category, and date (defaults to today)
- **View & sort** - by amount, date, or category-then-amount
- **Filter & search** - by category, date range, or a keyword in the description
- **Delete entries** - by ID, with a live table shown before you pick
- **Spending summary** - total spent, per-category breakdown with a bar chart, average expense, and top 5 biggest entries
- **Persistent storage** - data is saved to `data/expenses.json` automatically after every change

---

## Python Concepts Demonstrated

| Concept | Where |
|---|---|
| Classes and objects | `Expense`, `ExpenseTracker` in `models.py` / `tracker.py` |
| Data structures | Lists, dictionaries, sets throughout `tracker.py` |
| Sorting algorithms | `sort_by_amount`, `sort_by_date`, `sort_by_category_then_amount` |
| List comprehensions | `filter_by_category`, `filter_by_date_range`, `search_by_description` |
| Context managers | `with open(...)` in `storage.py` for all file I/O |
| File handling | JSON read/write via `storage.py` |

---

## Project Structure

```
Reyes_John_FinalProject/
│
├── README.md
├── .gitignore
│
├── src/
│   ├── main.py        # Entry point, CLI loop, user input handling
│   ├── tracker.py     # ExpenseTracker class (core business logic)
│   ├── models.py      # Expense class with validation
│   ├── storage.py     # JSON file read/write
│   └── display.py     # Table formatting and print helpers
│
└── data/
    └── expenses.json  # Persistent data file (auto-created on first run)
```

---

## Sample CLI Usage

```
=======================================================
          EXPENSE TRACKER - CLI Edition
=======================================================
  8 expense(s) loaded.

  --- Main Menu ---
  [1] Add expense
  [2] View / Sort expenses
  [3] Filter / Search expenses
  [4] Delete expense
  [5] Spending summary
  [0] Back / Exit
  Choose an option: 5

  === SPENDING SUMMARY ===
  Total expenses : 8
  Total spent    : ₱9,143.50
  Average expense: ₱1,142.94

  By category:
    Utilities      ₱  2,800.50  ██████████████████████████████
    Shopping       ₱  2,499.00  ██████████████████████████
    Food           ₱  1,570.00  ████████████████
    Education      ₱    895.00  █████████
    Entertainment  ₱    549.00  █████
    Health         ₱    650.00  ██████
    Transport      ₱    180.00  █
```

---

## Video Demonstration

YouTube link: *(to be added before submission)*

---

## Author

**Justin Reyz L. Sorongon**  
Intermediate Programming - Final Project  
Academic Year 2025–2026

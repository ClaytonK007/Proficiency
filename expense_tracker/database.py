import sqlite3

DB_PATH = "expenses.db"

CATEGORIES = ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Health", "Other"]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
        )
    """)
    conn.commit()
    conn.close

def add_expense(description, category, amount, expense_date):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        "INSERT INTO expenses (description, category, amount, date) 
            VALUES (?, ?, ?, ?), (description, category, amount, expense_date)
    """)
    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM expenses ORDER BY date, DESC, id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_expense(expense_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def get_category_totals():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()
    conn.close()
    return [{"category": row[0], "total": row[1]} for row in rows]

def get_total_spent():
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT SUM(aount) FROM expenses").fetchone()
    conn.close()
    return row[0] or 0.0
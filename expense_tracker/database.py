import sqlite3

DATABASE_URL = "sqlite:///./expenses.db"

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount FLOAT NOT NULL,
            date TEXT NOT NULL,
        )
    """)
    conn.commit()
    conn.close

def add_expense(id: int, description: str, category: str, amount: float, date: str):
    pass

def get_expenses():
    pass

def delete_expense():
    pass

def get_category_totals():
    conn = sqlite3.connect(DATABASE_URL)
    conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """)
    conn.close()





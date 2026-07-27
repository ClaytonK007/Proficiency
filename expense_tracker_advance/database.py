import sqlite3
import hashlib
import secrets

DB_PATH = "expenses.db"

CATEGORIES = ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Health", "Other"]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


#   Authentication functions
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"), 
        salt.encode("utf-8"),
        100_000
        )
    return f"{salt}${digest.hex()}"

def verify_password(password, stored_hash):
    salt, _ = stored_hash.split("$")
    return hash_password(password, salt) == stored_hash

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


#   Expense functions
def add_expense(user_id, description, category, amount, expense_date):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO expenses (user_id, description, category, amount, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, description, category, amount, expense_date)
    )
    conn.commit()
    conn.close()


def get_expenses(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_expense(user_id, expense_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id))
    conn.commit()
    conn.close()

def get_category_totals(user_id, start_date=None, end_date=None):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ?"
    params = [user_id]
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    query += " GROUP BY category ORDER BY total DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [{"category": row[0], "total": row[1]} for row in rows]

def get_total_spent(user_id, start_date=None, end_date=None):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT SUM(amount) FROM expenses WHERE user_id = ?"
    params = [user_id]
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    row = conn.execute(query, params).fetchone()
    conn.close()
    return row[0] or 0.0

def get_monthly_totals(user_id):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month
    """, (user_id,)).fetchall()
    conn.close()
    return [{"month": row[0], "total": row[1]} for row in rows]
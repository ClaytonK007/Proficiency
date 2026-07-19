import sqlite3

DB_PATH = "csv_project.db"

#   Establish connection to the database
def get_connection():
    return sqlite3.connect(DB_PATH)

#   Create the table for the database
def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS csv_import (
                 Id INTEGER PRIMARY_KEY,
                 Name TEXT,
                 Surname TEXT,
                 Initials TEXT,
                 Age INTEGER,
                 DateOfBirth TEXT
        )
    """)
    conn.commit()
    conn.close()
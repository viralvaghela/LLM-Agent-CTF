import sqlite3
import os

DB_PATH = 'support.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            status TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            content TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            amount REAL,
            type TEXT
        )
    ''')
    c.execute("DELETE FROM customers")
    c.execute("DELETE FROM transactions")
    c.execute("DELETE FROM notes")
    c.execute("INSERT INTO customers (name, email, status) VALUES ('Alice', 'alice@example.com', 'active')")
    c.execute("INSERT INTO customers (name, email, status) VALUES ('Bob', 'bob@example.com', 'premium')")
    conn.commit()
    conn.close()

def get_customer_by_name(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Note: Intentional SQL injection vulnerability here for ASI-03
    try:
        c.execute(f"SELECT * FROM customers WHERE name LIKE '%{name}%'")
        res = c.fetchall()
    except Exception as e:
        res = str(e)
    conn.close()
    return res

def add_refund(customer_id, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO transactions (customer_id, amount, type) VALUES (?, ?, 'refund')", (customer_id, amount))
    conn.commit()
    conn.close()
    return True

def add_note(customer_id, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO notes (customer_id, content) VALUES (?, ?)", (customer_id, content))
    conn.commit()
    conn.close()
    return True

def get_notes(customer_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT content FROM notes WHERE customer_id = ?", (customer_id,))
    res = c.fetchall()
    conn.close()
    return [r[0] for r in res]

def execute_raw_query(query: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # INTENTIONAL VULNERABILITY: Raw SQL execution allows arbitrary queries
    c.execute(query)
    if query.strip().upper().startswith(("SELECT", "PRAGMA")):
        res = c.fetchall()
    else:
        conn.commit()
        res = f"Rows affected: {c.rowcount}"
    conn.close()
    return res

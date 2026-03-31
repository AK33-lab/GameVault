import sqlite3

def get_db():
    conn = sqlite3.connect('games.db')
    conn.row_factory = sqlite3.Row  # access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # enforce foreign key constraints as SQLITE does not enforce them by default
    return conn
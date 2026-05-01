import sqlite3

def get_db():
    conn = sqlite3.connect('games.db', timeout=10)  # increase timeout to handle concurrent access
    conn.row_factory = sqlite3.Row  # access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # enforce foreign key constraints as SQLITE does not enforce them by default
    conn.execute("PRAGMA journal_mode = WAL") # enable concurrent reads during writes
    return conn
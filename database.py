import sqlite3
import os
import csv

DB_PATH = '/tmp/games.db' if os.environ.get('GAE_ENV') else 'games.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    count = cursor.execute('SELECT COUNT(*) FROM games').fetchone()[0]
    if count == 0:
        print("Seeding database...")
        def clean_float(val):
            try:
                return float(str(val).replace('$', '').strip())
            except (ValueError, TypeError):
                return None

        with open('VideoGamesSales.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row = {k.strip(): v.strip() for k, v in row.items()}
                if not row.get('title') or not row.get('genre') or not row.get('console'):
                    continue
                cursor.execute('INSERT OR IGNORE INTO genres (name) VALUES (?)', (row['genre'],))
                cursor.execute('SELECT id FROM genres WHERE name = ?', (row['genre'],))
                genre_id = cursor.fetchone()[0]
                cursor.execute('INSERT OR IGNORE INTO consoles (name) VALUES (?)', (row['console'],))
                cursor.execute('SELECT id FROM consoles WHERE name = ?', (row['console'],))
                console_id = cursor.fetchone()[0]
                cursor.execute('''
                    INSERT INTO games 
                    (title, console_id, genre_id, publisher, developer, critic_score, total_sales, na_sales, jp_sales)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['title'],
                    console_id,
                    genre_id,
                    row.get('publisher'),
                    row.get('developer'),
                    clean_float(row.get('critic_score')),
                    clean_float(row.get('total_sales(mil)')),
                    clean_float(row.get('na_sales(mil)')),
                    clean_float(row.get('jp_sales(mil)'))
                ))
        conn.commit()
        print("Database seeded!")

    conn.close()

def get_db():
    conn = sqlite3.connect('games.db', timeout=10)  # increase timeout to handle concurrent access
    conn.row_factory = sqlite3.Row  # access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # enforce foreign key constraints as SQLITE does not enforce them by default
    conn.execute("PRAGMA journal_mode = WAL") # enable concurrent reads during writes
    return conn
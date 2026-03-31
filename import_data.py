import sqlite3
import csv

def clean_float(val):
    try:
        return float(str(val).replace('$', '').strip())
    except (ValueError, TypeError):
        return None

def import_data():
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()

    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    with open('VideoGamesSales.csv', 'r', encoding='utf-8-sig') as f:  # utf-8-sig strips the BOM
        reader = csv.DictReader(f)
        for row in reader:
            # Strip all keys and values
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
    conn.close()
    print("Data imported successfully!")

if __name__ == '__main__':
    import_data()
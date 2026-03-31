from flask import Flask, render_template, request, redirect, url_for
from database import get_db

app = Flask(__name__)

@app.route('/')
def home():
    db = get_db()
    games = db.execute('''
        WITH latest_three AS (
            SELECT games.id, games.title, consoles.name AS console, genres.name AS genre,
                   games.critic_score, games.total_sales
            FROM games
            JOIN consoles ON games.console_id = consoles.id
            JOIN genres ON games.genre_id = genres.id
            ORDER BY games.id DESC
            LIMIT 3
        ),
        random_hundred AS (
            SELECT games.id, games.title, consoles.name AS console, genres.name AS genre,
                   games.critic_score, games.total_sales
            FROM games
            JOIN consoles ON games.console_id = consoles.id
            JOIN genres ON games.genre_id = genres.id
            WHERE games.id NOT IN (SELECT id FROM latest_three)
            ORDER BY RANDOM()
            LIMIT 100
        )
        SELECT * FROM random_hundred
        UNION ALL
        SELECT * FROM latest_three
    ''').fetchall()
    db.close()
    return render_template('index.html', games=games)

@app.route('/games/add', methods=['GET', 'POST'])
def add_game():
    db = get_db()
    if request.method == 'POST':
        db.execute('''
            INSERT INTO games (title, console_id, genre_id, publisher, developer, critic_score, total_sales, na_sales, jp_sales)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['title'],
            request.form['console_id'],
            request.form['genre_id'],
            request.form['publisher'],
            request.form['developer'],
            request.form['critic_score'] or None,
            request.form['total_sales'] or None,
            request.form['na_sales'] or None,
            request.form['jp_sales'] or None
        ))
        db.commit()
        db.close()
        return redirect(url_for('home'))
    
    genres = db.execute('SELECT * FROM genres ORDER BY name').fetchall()
    consoles = db.execute('SELECT * FROM consoles ORDER BY name').fetchall()
    db.close()
    return render_template('add_game.html', genres=genres, consoles=consoles)

@app.route('/games/edit/<int:id>', methods=['GET', 'POST'])
def edit_game(id):
    db = get_db()
    if request.method == 'POST':
        db.execute('''
            UPDATE games
            SET title=?, console_id=?, genre_id=?, publisher=?, developer=?,
                critic_score=?, total_sales=?, na_sales=?, jp_sales=?
            WHERE id=?
        ''', (
            request.form['title'],
            request.form['console_id'],
            request.form['genre_id'],
            request.form['publisher'],
            request.form['developer'],
            request.form['critic_score'] or None,
            request.form['total_sales'] or None,
            request.form['na_sales'] or None,
            request.form['jp_sales'] or None,
            id
        ))
        db.commit()
        db.close()
        return redirect(url_for('home'))

    game = db.execute('SELECT * FROM games WHERE id = ?', (id,)).fetchone()
    genres = db.execute('SELECT * FROM genres ORDER BY name').fetchall()
    consoles = db.execute('SELECT * FROM consoles ORDER BY name').fetchall()
    db.close()
    return render_template('edit_game.html', game=game, genres=genres, consoles=consoles)

@app.route('/games/delete/<int:id>')
def delete_game(id):
    db = get_db()
    db.execute('DELETE FROM games WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
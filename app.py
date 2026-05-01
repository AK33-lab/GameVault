from flask import Flask, render_template, request, redirect, url_for
from database import get_db, init_db

app = Flask(__name__)
# Initialize the database when the app starts
init_db()

@app.route('/')
def home():
    per_page = 20
    page = request.args.get('page', 1, type=int)
    if page is None or page < 1:
        page = 1
    db = get_db()
    try:
        total_games = db.execute('SELECT COUNT(*) AS total FROM games').fetchone()['total']
        total_pages = max((total_games + per_page - 1) // per_page, 1)
        if page > total_pages:
            page = total_pages

        offset = (page - 1) * per_page
        games = db.execute('''
            SELECT games.id, games.title, consoles.name AS console, genres.name AS genre,
                   games.critic_score, games.total_sales
            FROM games
            JOIN consoles ON games.console_id = consoles.id
            JOIN genres ON games.genre_id = genres.id
            LIMIT ? OFFSET ?
        ''', (per_page, offset)).fetchall()
        return render_template(
            'index.html',
            games=games,
            page=page,
            total_pages=total_pages,
            has_prev=(page > 1),
            has_next=(page < total_pages)
        )
    finally:
        db.close()

# Route for adding a new game.
@app.route('/games/add', methods=['GET', 'POST'])
def add_game():
    db = get_db()
    try:
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
            return redirect(url_for('home'))

        genres = db.execute('SELECT * FROM genres ORDER BY name').fetchall()
        consoles = db.execute('SELECT * FROM consoles ORDER BY name').fetchall()
        return render_template('add_game.html', genres=genres, consoles=consoles)
    finally:
        db.close()

# Route for editing an existing game.
@app.route('/games/edit/<int:id>', methods=['GET', 'POST'])
def edit_game(id):
    db = get_db()
    try:
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
            return redirect(url_for('home'))

        game = db.execute('SELECT * FROM games WHERE id = ?', (id,)).fetchone()
        genres = db.execute('SELECT * FROM genres ORDER BY name').fetchall()
        consoles = db.execute('SELECT * FROM consoles ORDER BY name').fetchall()
        return render_template('edit_game.html', game=game, genres=genres, consoles=consoles)
    finally:
        db.close()

# Route for deleting a game.
@app.route('/games/delete/<int:id>')
def delete_game(id):
    db = get_db()
    try:
        db.execute('DELETE FROM games WHERE id = ?', (id,))
        db.commit()
        return redirect(url_for('home'))
    finally:
        db.close()

# Filtering route to generate reports based on genre, console, and critic score range.
@app.route('/report', methods=['GET', 'POST'])
def report():
    db = get_db()
    try:
        genres = db.execute('SELECT * FROM genres ORDER BY name').fetchall()
        consoles = db.execute('SELECT * FROM consoles ORDER BY name').fetchall()
        
        games = []
        stats = None
        filters = {}

        if request.method == 'POST':
            filters['genre_id'] = request.form.get('genre_id')
            filters['console_id'] = request.form.get('console_id')
            filters['min_score'] = request.form.get('min_score')
            filters['max_score'] = request.form.get('max_score')

            query = '''
                SELECT games.id, games.title, consoles.name AS console, genres.name AS genre,
                       games.critic_score, games.total_sales, games.na_sales, games.jp_sales
                FROM games
                JOIN consoles ON games.console_id = consoles.id
                JOIN genres ON games.genre_id = genres.id
                WHERE 1=1
            '''
            params = []

            if filters['genre_id']:
                query += ' AND games.genre_id = ?'
                params.append(filters['genre_id'])
            if filters['console_id']:
                query += ' AND games.console_id = ?'
                params.append(filters['console_id'])
            if filters['min_score']:
                query += ' AND games.critic_score >= ?'
                params.append(filters['min_score'])
            if filters['max_score']:
                query += ' AND games.critic_score <= ?'
                params.append(filters['max_score'])

            query += ' ORDER BY games.critic_score DESC'

            games = db.execute(query, params).fetchall()

            if games:
                stats = db.execute('''
                    SELECT COUNT(*) AS total,
                           ROUND(AVG(critic_score), 2) AS avg_score,
                           ROUND(AVG(total_sales), 2) AS avg_sales,
                           ROUND(SUM(total_sales), 2) AS total_sales
                    FROM games
                    JOIN consoles ON games.console_id = consoles.id
                    JOIN genres ON games.genre_id = genres.id
                    WHERE 1=1
                ''' + (
                    (' AND games.genre_id = ?' if filters['genre_id'] else '') +
                    (' AND games.console_id = ?' if filters['console_id'] else '') +
                    (' AND games.critic_score >= ?' if filters['min_score'] else '') +
                    (' AND games.critic_score <= ?' if filters['max_score'] else '')
                ), params).fetchone()

        return render_template('report.html', genres=genres, consoles=consoles,
                               games=games, stats=stats, filters=filters)
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
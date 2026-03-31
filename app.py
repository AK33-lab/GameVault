from flask import Flask, render_template
from database import get_db

app = Flask(__name__)

@app.route('/')
def home():
    db = get_db()
    games = db.execute('''
        SELECT games.id, games.title, consoles.name AS console, genres.name AS genre,
               games.critic_score, games.total_sales
        FROM games
        JOIN consoles ON games.console_id = consoles.id
        JOIN genres ON games.genre_id = genres.id
        LIMIT 100
    ''').fetchall()
    db.close()
    return render_template('index.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)
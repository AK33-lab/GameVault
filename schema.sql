CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS consoles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    console_id INTEGER,
    genre_id INTEGER,
    publisher TEXT,
    developer TEXT,
    critic_score REAL,
    total_sales REAL,
    na_sales REAL,
    jp_sales REAL,
    FOREIGN KEY (console_id) REFERENCES consoles(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);

CREATE INDEX IF NOT EXISTS idx_games_genre ON games(genre_id);
CREATE INDEX IF NOT EXISTS idx_games_console ON games(console_id);
CREATE INDEX IF NOT EXISTS idx_games_score ON games(critic_score);
CREATE INDEX IF NOT EXISTS idx_genres_name ON genres(name);
CREATE INDEX IF NOT EXISTS idx_consoles_name ON consoles(name);
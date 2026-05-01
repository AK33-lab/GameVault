# GameVault - Video Games Sales Dashboard

A web application for browsing and managing video game sales data.

## Author

Aakansha Kedia

## AI Usage Disclaimer

I used Claude to generate commands to test my data integrity directly in the Terminal (correct # of rows etc), add colorful UI elements (in ``templates/base.html``), and to integrate my SQL queries with Flask routes. I also used it to make the baseline ``index.html``. Through my use of AI for this purpose, I learnt about Jinja templates, a topic which I was unfamiliar with prior to working on this project. I also used Claude to help me deploy this project to Google Cloud, which ended up not working, so I switched to Render.


## Tech Stack

- Python 3
- Flask
- SQLite
- HTML (Jinja templates)
- Render

## Features

- View games with pagination (20 per page)
- Add new game records
- Edit existing game records
- Delete game records
- Generate filtered reports by:
	- Genre
	- Console
	- Critic score range
- See report summary statistics:
	- Number of games
	- Average critic score
	- Average total sales
	- Total sales

## Project Structure

- `app.py`: Flask app routes and page logic
- `database.py`: SQLite connection helper
- `import_data.py`: Imports CSV data into SQLite database
- `schema.sql`: Database schema (genres, consoles, games)
- `VideoGamesSales.csv`: Source dataset
- `games.db`: Generated SQLite database file
- `templates/index.html`: Home page with paginated table
- `templates/add_game.html`: Add game form
- `templates/edit_game.html`: Edit game form
- `templates/report.html`: Filtered report page with stats

## Initialize Database

For local system testing, run:

```bash
python3 import_data.py
```

```bash
python3 app.py
```

## Website URL

You can visit: https://gamevault-ufud.onrender.com to run the web-app. Render takes a few seconds to load the page.

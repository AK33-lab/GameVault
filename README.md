# CS348 Project

Flask web app to view video game sales

## Author

Aakansha Kedia

## Project Structure

- app.py: Flask app and route handlers
- database.py: database connection/helper logic
- import_data.py: script to import CSV data into the database
- schema.sql: database schema
- VideoGamesSales.csv: source dataset
- templates/: HTML templates for pages

## Run

Create database with: ``python import_data.py``

Start the app with: ``python app.py``

Then open the local URL printed in the terminal.

## Features

- Delete a game from DB
- Add a new game to DB
- Edit existing game records
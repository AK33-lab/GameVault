from flask import Flask
from database import get_db

app = Flask(__name__)

@app.route('/')
def home():
    return "App is running, LFG!"

if __name__ == '__main__':
    app.run(debug=True)
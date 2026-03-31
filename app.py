from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>CS348 Project Stage 1</h1><p>Hello World! </p>"

if __name__ == '__main__':
    app.run(debug=True)

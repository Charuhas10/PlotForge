# app.py
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Import and register route modules
from routes import generate

generate.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)

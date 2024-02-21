from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_cors import CORS
from backend.config import MONGO_URI  # Import the MONGO_URI

app = Flask(__name__)

# Initialize extensions
mongo = PyMongo(app, uri=MONGO_URI)  # Pass the MONGO_URI here
login_manager = LoginManager(app)
CORS(app)

# Import routes
from backend.app.routes import *  # Update the import statement

if __name__ == '__main__':
    app.run(debug=True)
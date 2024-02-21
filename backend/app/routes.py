# backend/app/routes.py

from flask import request, jsonify, render_template
from flask_login import login_required
from backend.app import app, login_manager, mongo  # Update the import statements
from backend.analysis import analyze_bank_statement
from flask_pymongo import PyMongo
from flask import render_template_string
from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import url_for
from jinja2 import Template
from flask import Flask, render_template, request
from flask import Flask, render_template, redirect, url_for
from flask import send_from_directory
from flask import Flask, render_template, Response, jsonify, send_from_directory
from flask.helpers import get_root_path
from flask import Flask, send_file, render_template, make_response, redirect
from flask_cors import CORS
import subprocess
from werkzeug.utils import secure_filename
import os
from backend.config import MONGO_URI
from flask import jsonify
from bson import ObjectId
from flask import Flask, request, jsonify, json
from json import JSONEncoder
from flask_pymongo import PyMongo
from backend.analysis import analyze_bank_statement
from bson import ObjectId

app = Flask(__name__)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app.json_encoder = CustomJSONEncoder
mongo = PyMongo(app, uri=MONGO_URI)

# Dummy user class for demonstration
class User:
    @staticmethod
    def get(user_id):
        # Implement user loading logic here
        pass

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/api/analyze', methods=['POST'])
def analyze_statement():
    try:
        statement_json = request.get_json()
        if not statement_json:
            return jsonify({"error": "Invalid JSON format"}), 400

        results = analyze_bank_statement(statement_json)

        # Store results in MongoDB
        result_id = mongo.db.analysis_results.insert_one(results).inserted_id

        # Convert ObjectId to string before sending in the response
        results['id'] = str(result_id)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard')
@login_required
def dashboard():
    # Assuming your Streamlit app is running on localhost:8501
    streamlit_url = "http://localhost:8501"
    # Use Flask's render_template_string to embed the URL into an iframe
    return render_template_string('<iframe src="{{ streamlit_url }}" width="100%" height="800px" frameborder="0" scrolling="yes"></iframe>', streamlit_url=streamlit_url)

if __name__ == '__main__':
    app.run(debug=True)
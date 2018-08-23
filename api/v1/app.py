#!/usr/bin/python3
"""
This module creates and runs the Flask app
that supports API v.1
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def app_teardown(self):
    """
    The hook which will be executed on the app teardown
    """
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """
    404 error handler
    """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port)

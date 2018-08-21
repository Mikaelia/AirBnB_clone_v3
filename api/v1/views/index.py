#!/usr/bin/python3
""" This module adds the "status" route to the "/api/v1" blueprint
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """ The "status" route.
        Returns "status": "OK" json
    """
    return jsonify({"status": "OK"})

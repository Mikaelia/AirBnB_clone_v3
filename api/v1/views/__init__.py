#!/usr/bin/python3
""" This module initilizes the "/api/v1" blueprint
"""
from flask import Blueprint

app_views = Blueprint("/api/v1", __name__)
if app_views is not None:
    from api.v1.views.index import *
from api.v1.views.cities import *
from api.v1.views.amenities import *

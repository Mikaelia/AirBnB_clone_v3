#!/usr/bin/python3
from api.v1.views import app_views
from models import storage, City
from flask import abort

@app_views.route('/api/v1/states/<state_id>/cities')
def get_cities(state_id):
    """
    Retrieves list of all City objects of a State
    """
    city_dict = {}
    cities = storage.all(City)
    if cities:
        for city in cities:
            if city.state_id == state_id:
                city_dict.update(city)
        if not city_dict:
            abort(404)




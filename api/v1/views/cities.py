#!/usr/bin/python3
from api.v1.views import app_views
from models import storage, City
from flask import abort, request

@app_views.route('/api/v1/states/<state_id>/cities')
def city_by_state_id(state_id):
    """
    Retrieves list of all City objects of a State
    """
    city_list = []
    cities = storage.all(City)
    city_list = [to_dict(city) for city in cities if city['state_id'] == state_id]
    if len(city_list) == 0:
            abort(404)
    return city_list
@app_views.route('/api/v1/cities/<city_id>')
def city_by_id(city_id):
    """
    Retrieves city by city id. If city_id not linked to City,
    raise 404.
    """
    my_city = None
    cities = storage.all(City)
    city = next(filter(lambda x: x["id"] == city_id, cities), None)
    return to_dict(city) if item else abort(404)

@app_views.route('/api/v1/cities/<city_id>')
def delete_city():
    """
    Deletes city by id. If city_id not linked to City, raise 404
    Returns empty dict with status 200
    """
    cities = storage.all(City)
    city = next(filter(lambda x: x["id"] == city_id, cities), None)
    if city:
        storage.delete(city)
        return {}, 200
    else:
        abort(404)

@app_views.route('/api/v1/states/<state_id>/cities')
def create_city():
    """
    Creates new city. If request body not valid JSON, raises 400
    If state_id not linked to State, raise 404
    If dict does not contain 'name' key, raise 400
    Returns city object with status 201
    """
    if not request.json or not 'name' in request.json:
        abort(400)
    city = {
        'state_id': request.json['state_id'],
        'name': request.json['name'],
        'places': request.json['places']
    }
    storage.new(city)
    storage.save(city)
    return to_dict(city), 201
#need to check if state id linked to state**

@app_views.route('/api/v1/cities/<city_id>')
def put(city_id):
    """
    Updates city. If request not valid JSON, raises 400.
    If city_id not linked to City object, raise 404
    Returns city object with status code 200
    """
    cities = storage.all(City)
    city = [city for city in cities if city['id'] == city_id]
    if len(city) == 0:
            abort(404)
    if not request.json:
            abort(400)
    city[0]['state_name'] = request.json.get('state_name', city[0]['state_name'])
    city[0]['name'] = request.json.get('name', city[0]['name'])
    city[0]['places'] = request.json.get('places', city[0]['places'])

    return to_dict(city[0]), 200

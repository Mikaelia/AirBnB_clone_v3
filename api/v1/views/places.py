#!/usr/bin/python3
from api.v1.views import app_views
from models import storage, Place
from flask import abort, request, jsonify


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['GET'])
def place_list(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    a = storage.get("City", city_id)
    if a is None:
        abort(404)
    return jsonify(a.places)  # check this


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def place_by_id(place_id):
    """
    Retrieves place by place id. If place_id not linked to place,
    raise 404.
    """
    places = storage.all("Place").values()
    place = next(filter(lambda x: x.id == place_id, places), None)
    return jsonify(place.to_dict()) if place else abort(404), 201


@app_views.route(
    '/places/<place_id>',
    strict_slashes=False,
    methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes place by id. If place_id not linked to place, raise 404
    Returns empty dict with status 200
    """
    places = storage.all("Place").values()
    place = next(filter(lambda x: x.id == place_id, places), None)
    if place:
        storage.delete(place)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    '/cities/<city_id>/places',
    strict_slashes=False,
    methods=['POST'])
def create_place(city_id):
    """
    Creates new place. If request body not valid JSON, raises 400
    If dict does not contain 'name' key, raise 400
    Returns place object with status 201
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    kwargs = request.get_json()

    a = storage.get("City", city_id)
    if a is None:
        abort(404)

    if not kwargs.get('user_id'):
        abort(400, description="Missing user_id")
    if not kwargs.get('name'):
        abort(400, description='Missing name')

    my_place = Place(**kwargs)
    storage.new(my_place)
    storage.save()
    return jsonify(my_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """
    Updates place. If request not valid JSON, raises 400.
    If place_id not linked to place object, raise 404
    Returns place object with status code 200
    """
    places = storage.all("Place").values()
    place = next(filter(lambda x: x.id == place_id, places), None)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    args = request.get_json()

    place.name = args.get('name', place.state_id)
    place.description = args.get('description ', place.description)
    place.number_rooms = args.get('number_rooms', place.number_rooms)
    place.number_bathrooms = args.get(
        'number_bathrooms', place.number_bathrooms)
    place.max_guest = args.get('max_guest', place.max_guest)
    place.price_by_night = args.get('price_by_night', place.price_by_night)
    place.latitude = args.get('latitude', place.latitude)
    place.longitude = args.get('longitude', place.longitude)
    place.amenity_ids = args.get('amenity_ids', place.amenity_ids)

    return jsonify(place.to_dict()), 200

    # might need to ignore keys explicityly

#!/usr/bin/python3
from api.v1.views import app_views
from models import storage, Amenity
from flask import abort, request, jsonify


@app_views.route('/amenities/', strict_slashes=False, methods=['GET'])
def amenity_list():
    """
    Retrieves a list of all Amenity objects
    """
    amenities = storage.all("Amenity").values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['GET'])
def amenity_by_id(amenity_id):
    """
    Retrieves amenity by amenity id. If amenity_id not linked to amenity,
    raise 404.
    """
    amenities = storage.all("Amenity").values()
    amenity = next(filter(lambda x: x.id == amenity_id, amenities), None)
    return jsonify(amenity.to_dict()) if amenity else abort(404), 201


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes amenity by id. If amenity_id not linked to amenity, raise 404
    Returns empty dict with status 200
    """
    amenities = storage.all("Amenity").values()
    amenity = next(filter(lambda x: x.id == amenity_id, amenities), None)
    if amenity:
        storage.delete(amenity)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """
    Creates new amenity. If request body not valid JSON, raises 400
    If dict does not contain 'name' key, raise 400
    Returns amenity object with status 201
    """
    if not request.get_json() or 'name' not in request.get_json():
        abort(400, description="Missing name")

    kwargs = request.get_json()
    my_amenity = Amenity(**kwargs)
    storage.new(my_amenity)
    storage.save()
    return jsonify(my_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    strict_slashes=False,
    methods=['PUT'])
def put(amenity_id):
    """
    Updates amenity. If request not valid JSON, raises 400.
    If amenity_id not linked to amenity object, raise 404
    Returns amenity object with status code 200
    """
    amenities = storage.all("Amenity").values()
    amenity = next(filter(lambda x: x.id == amenity_id, amenities), None)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    args = request.get_json()

    amenity.name = args.get('name', amenity.state_id)

    return jsonify(amenity.to_dict()), 200

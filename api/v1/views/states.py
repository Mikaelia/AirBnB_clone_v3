#!/usr/bin/python3
""" This module contains the CRUD for the State API endpoint
"""
from api.v1.views import app_views
from models import storage, State
from flask import abort, jsonify, request


@app_views.route("/states", strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False)
def get_states(state_id=None):
    """ The "states" get route.
        Returns the list of all State objects
        or the state json object if state_id was specified
    """
    states = storage.all("State").values()
    results = []

    for state in states:
        results.append(state.to_dict())

    if state_id is not None:
        for state in states:
            if state_id == state.id:
               return jsonify(state.to_dict())
        return abort(404)

    return jsonify(results)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """ Deletes state by id.
        Returns empty dict with status 200
        If state_id is not linked to state, raises 404
    """
    states = storage.all("State").values()
    state = next(filter(lambda state: state.id == state_id, states), None)
    if state:
        storage.delete(state)
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """ Creates new state. If request body not valid JSON, raises 400
        If state_id not linked to State, raise 404
        If dict does not contain 'name' key, raise 400
        Returns state object with status 201
    """
    try:
        state = request.get_json()
    except:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in state:
        return jsonify({"error": "Missing name"}), 400

    state = State(**state)
    storage.new(state)
    storage.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_states(state_id):
    """ Updates state. If request not valid JSON, raises 400.
        If state_id not linked to State object, raise 404
        Returns state object with status code 200
    """
    try:
        json = request.get_json()
    except:
        return jsonify({"error": "Not a JSON"}), 400

    try:
        state = storage.get("State", state_id)
    except:
       abort(404)

    if not state:
       abort(404)

    attrs_to_skip =  ["id", "created_at", "updated_at"]
    for k, v in json.items():
        if k not in attrs_to_skip:
            setattr(state, k, v)

    state.save()

    return jsonify(state.to_dict()), 200

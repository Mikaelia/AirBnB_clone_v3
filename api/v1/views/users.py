#!/usr/bin/python3
from api.v1.views import app_views
from models import storage, User
from flask import abort, request, jsonify


@app_views.route('/users/', strict_slashes=False, methods=['GET'])
def user_list():
    """
    Retrieves a list of all User objects
    """
    users = storage.all("User").values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def user_by_id(user_id):
    """
    Retrieves user by user id. If user_id not linked to user,
    raise 404.
    """
    users = storage.all("User").values()
    user = next(filter(lambda x: x.id == user_id, users), None)
    return jsonify(user.to_dict()) if user else abort(404), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes user by id. If user_id not linked to user, raise 404
    Returns empty dict with status 200
    """
    users = storage.all("User").values()
    user = next(filter(lambda x: x.id == user_id, users), None)
    if user:
        storage.delete(user)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """
    Creates new user. If request body not valid JSON, raises 400
    If dict does not contain 'name' key, raise 400
    Returns user object with status 201
    """
    if not request.get_json() or 'name' not in request.get_json():
        abort(400, description="Missing name")

    kwargs = request.get_json()
    if not kwargs.get('email'):
        abort(400, description="Missing email")
    if not kwargs.get('password'):
        abort(400, description='Missing password')

    my_user = User(**kwargs)
    storage.new(my_user)
    storage.save()
    return jsonify(my_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """
    Updates user. If request not valid JSON, raises 400.
    If user_id not linked to user object, raise 404
    Returns user object with status code 200
    """
    users = storage.all("User").values()
    user = next(filter(lambda x: x.id == user_id, users), None)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    args = request.get_json()

    user.name = args.get('name', user.state_id)
    user.password = args.get('password', user.password)
    user.first_name = args.get('first_name', user.first_name)
    user.last_name = args.get('last_name', user.last_name)

    return jsonify(user.to_dict()), 200

    # might need to ignore keys explicityly

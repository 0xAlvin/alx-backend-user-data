#!/usr/bin/env python3
"""Module for Login views"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Login route"""
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    users_with_email = User.search({'email': email})
    if not users_with_email:
        return jsonify({"error": "no user found for this email"}), 404
    if not users_with_email[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    user = users_with_email[0]
    session_id = auth.create_session(user.id)
    session_cookie = getenv('SESSION_NAME')
    response = jsonify(user.to_json())
    response.set_cookie(session_cookie, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """Logout route"""
    from api.v1.app import auth

    if auth.destroy_session(request) is True:
        return jsonify({}), 200
    else:
        return abort(404)

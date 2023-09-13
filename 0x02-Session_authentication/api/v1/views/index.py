#!/usr/bin/env python3
"""Module for Index views"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/forbidden', strict_slashes=False)
def forbidden() -> str:
    """
    Raise a forbidden error.

    Returns:
        str: JSON response indicating a forbidden error.
    """
    abort(403)


@app_views.route('/unauthorized', strict_slashes=False)
def unauthorized() -> str:
    """
    Raise an unauthorized error.

    Returns:
        str: JSON response indicating an unauthorized error.
    """
    abort(401)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status

    Returns:
        str: JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats

    Returns:
        str: JSON response with the number of each object (e.g., users).
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)

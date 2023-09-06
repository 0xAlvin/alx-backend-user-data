#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth = getenv('AUTH_TYPE')
if auth == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()


@app.before_request
def handle_request():
    """handles requests authetication"""
    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth is None:
        return
    if not auth.require_auth(request.path, paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(403)
def error_forbidden(error) -> str:
    """unauthorized handler
    """
    return jsonify({"error": "Forbidden"})


@app.errorhandler(401)
def error_unauthorized(error) -> str:
    """unauthorized handler
    """
    return jsonify({"error": "unauthorized"})


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)

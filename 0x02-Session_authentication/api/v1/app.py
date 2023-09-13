#!/usr/bin/env python3
"""Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine the authentication method based on the environment
# variable AUTH_TYPE
auth = None
auth_type = getenv('AUTH_TYPE')
if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
else:
    auth = Auth()


@app.before_request
def handle_request():
    """Handles request authentication and authorization.

    This function is executed before processing each incoming request.
    It checks if authentication and authorization are required for the
    requested path and validates the user's credentials.

    Returns:
        None: If the request is valid and authorized.
        HTTP 401 Unauthorized: If the request lacks proper authentication.
        HTTP 403 Forbidden: If the user does not have permission to
        access the resource.
    """
    paths = ['/api/v1/status/', '/api/v1/unauthorized/',
             '/api/v1/forbidden/', '/api/v1/stat*',
             '/api/v1/auth_session/login/'
             ]
    if auth is None:
        return
    if not auth.require_auth(request.path, paths):
        return
    if auth.authorization_header(request) is None and auth.session_cookie(
            request) is None:
        return None, abort(401)
    if auth.current_user(request) is not None:
        request.current_user = auth.current_user(request)
    else:
        abort(403)


@app.errorhandler(403)
def forbidden(error) -> str:
    """Custom error handler for HTTP 403 Forbidden.

    Returns:
        str: JSON response with an error message.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Custom error handler for HTTP 401 Unauthorized.

    Returns:
        str: JSON response with an error message.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """Custom error handler for HTTP 404 Not Found.

    Returns:
        str: JSON response with an error message.
    """
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

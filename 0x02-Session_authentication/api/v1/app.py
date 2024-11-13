#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth = os.getenv('AUTH_TYPE')
if auth == 'auth':
    auth = Auth()
elif auth == 'basic_auth':
    auth = BasicAuth()
elif auth == "session_auth":
    auth = SessionAuth()

excluded_list = ['/api/v1/status/',
                 '/api/v1/unauthorized/',
                 '/api/v1/forbidden/',
                 '/api/v1/auth_session/login/']


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Not authorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden error handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def filter():
    """Filters requests
    """
    if not auth or not auth.require_auth(request.path, excluded_list):
        return

    request.current_user = auth.current_user(request)
    if not auth.authorization_header(request) and not \
       auth.session_cookie(request):
        abort(401)
        return None
    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


def extract_base64_authorization_header(self,
                                        authorization_header: str) -> str:
    """ extracts base64 from auth header """
    pass


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

#!/usr/bin/env python3
""" views for session auth"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenticate():
    """ views for session login"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            cookie_name = os.getenv('SESSION_NAME')
            output = jsonify(user.to_json())
            output.set_cookie(cookie_name, session_id)
            return output
    return jsonify({"error": "wrong password"}), 401



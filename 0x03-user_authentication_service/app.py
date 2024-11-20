#!/usr/bin/env python3
""" Flask app"""
from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   make_response,
                   redirect)
from auth import Auth
from user import User
from auth import _hash_password


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def message():
    """ returns a message that says Biemvenue
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """ registers a user if doesnt exist
    """
    email = request.form['email']
    password = request.form['password']

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ log in functionality
    """
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        abort(401)
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response()
        response.set_cookie('session_id', session_id)
        return jsonify({"email": f"{email}", "message": "logged in"})
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout functionality
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    auth.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

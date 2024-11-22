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
from sqlalchemy.orm.exc import NoResultFound


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
        response = make_response(jsonify({"email": f"{email}", "message": "logged in"}))
        response.set_cookie('session_id', session_id, secure=True, httponly=True)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout functionality
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ returns a profile from session_id
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password_token():
    """ resets a password token"""
    try:
        email = request.form['email']
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except (ValueError, NoResultFound):
        abort(403)


@app.route('/update_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ updates password """
    email = request.form['email']
    new_password = request.form['new_password']
    reset_token = request.form['reset_token']

    try:
        updated_password = AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

#!/usr/bin/env python3
""" Flask app"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

#!/usr/bin/env python3
""" encrypting password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ hashes a password and returns byte data"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

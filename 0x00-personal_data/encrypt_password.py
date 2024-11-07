#!/usr/bin/env python3
""" encrypting password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ hashes a password and returns byte data"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checks if a password is valid and returns a bool"""
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

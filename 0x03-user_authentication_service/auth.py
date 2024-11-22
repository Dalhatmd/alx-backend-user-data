#!/usr/bin/env python3
""" auth module"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ hashes a password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user
        """
        try:
            proposed_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pw = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pw)

    def valid_login(self, email: str, password: str) -> bool:
        """ validates login
        """
        try:
            login_user = self._db.find_user_by(email=email)
            is_valid_password = bcrypt.checkpw(password.encode('utf-8'),
                                               login_user.hashed_password)
            return is_valid_password

        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """ generates a uid """
        id = uuid.uuid4()
        return str(id)

    def create_session(self, email):
        """creates a session for input email
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """ finds user corresponding to session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        """ destroys a user's session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email):
        """gets token to reset password """
        user = self._db.find_user_by(email=email)
        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token, password):
        """ updates a user's password using reset_token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            updated_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=updated_password)
            return updated_password
        except NoResultFound:
            raise ValueError('User not found')

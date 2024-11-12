#!/usr/bin/env python3
""" BasicAuth module"""
from .auth import Auth
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Auth class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extracts base64 auth header """
        if authorization_header is None:
            return None

        if type(authorization_header) != str:
            return None

        args = authorization_header.split(' ')
        if args[0] == "Basic" and len(args) == 2:
            return args[1]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ decode base64 auth header """
        if base64_authorization_header is None or\
                type(base64_authorization_header) != str:
            return None

        try:
            decoded = base64.b64decode(base64_authorization_header)\
                      .decode('utf-8')
            return decoded
        except Exception as e:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ extracts user credentials from decoded auth header
        """
        if type(decoded_base64_authorization_header) != str:
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        username, password = decoded_base64_authorization_header.split(':')
        return (username, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns user credentials from email and password
        """
        if type(user_email) != str or type(user_pwd) != str:
            return None

        User.load_from_file()
        loaded_users = DATA["User"]

        for user in loaded_users.items():
            print(user.email)
            print(user._password)

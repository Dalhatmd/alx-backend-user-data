#!/usr/bin/env python3
""" auth module """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication functionailty
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires authorization
        """
        if path is None or excluded_paths is None:
            return True

        path = path if path.endswith('/') else path + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ gets the authorization header """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ doc doc doc"""
        return None

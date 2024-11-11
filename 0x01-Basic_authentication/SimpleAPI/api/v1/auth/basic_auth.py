#/usr/bin/env python3
""" BasicAuth module"""
from .auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ extracts base64 auth header """
        if authorization_header is None:
            return None

        if type(authorization_header) != str:
            return None
        
        args = authorization_header.split(' ')
        if args[0] == "Basic" and len(args) == 2:
            return args[1]
        return None

#!/usr/bin/env python3
""" sessuin auth module """
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """session auth functionality class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session for a user
        """
        if not isinstance(user_id, str) or user_id is None:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

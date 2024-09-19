#!/usr/bin/env python3
""" Session authentication implementation."""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ implements session Authentication."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates and returns a session id.
        Args:
            user_id (str)
        Return:
            uuid.uuid(4) (str)
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrieves user_id from user_id_by_session_id
        based on passed in session_id.
        Args:
            session_id (str)
        Return:
            user_id if it exists, None otherwise.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

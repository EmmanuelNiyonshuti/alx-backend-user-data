#!/usr/bin/env python3
""" Session authentication implementation."""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


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
        retrieves user_id from user_id_by_session_id dictinary
        based on passed in session_id.
        Args:
            session_id (str)
        Return:
            user_id if it exists, None otherwise.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        for k, v in SessionAuth.user_id_by_session_id.items():
            if k == session_id:
                user_id = v
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """
        retrieves a user based on a cookie value.
        Args:
            request: The http request object.
        Return:
            user object if a valid session exists, None otherwise.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        for v in self.user_id_by_session_id.values():
            user_id = v
        if user_id is None:
            return None
        return User.get(user_id)

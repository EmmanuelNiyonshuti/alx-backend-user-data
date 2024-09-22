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
        creates a uuid4 as a session id and maps it to a user_id
        as it's value in user_id_by_session_id dictionary.
        Args:
            user_id (str)
        Return:
            session id
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
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        deletes the user session/logout.
        Args:
            request - Request object.
        Return:
            bool.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True

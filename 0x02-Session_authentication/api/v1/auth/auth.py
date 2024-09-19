#!/usr/bin/env python3
""" implements auth class to manage API authentication. """
from flask import request
import os
from typing import List, TypeVar
from models.user import User


class Auth:
    """ Auth class. """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for an endpoint.
        Args:
            path: The path to check.
            excluded_paths: List of paths that do not require authentication.
        Return:
            bool.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith("/"):
            path = path + "/"
        for ex_paths in excluded_paths:
            if ex_paths.endswith("*"):
                if path.startswith(ex_paths[:-1]):
                    return False
            elif path == ex_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ retrieves the value of the request authorization header.
        Args:
            request: Request object.
        Return:
            value of the header request Authorization, None otherwise."""
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user (None in this base implementation).
        Args:
            request: Request object.
        Return:
            None (to be overridden in subclasses).
        """
        return None

    def session_cookie(self, request=None):
        """
        retrieves cookie value from a request.
        Args:
            request.
        Return:
            cookie value if it exists , None otherwise.
        """
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        cookie_val = request.cookies.get(cookie_name)
        return cookie_val

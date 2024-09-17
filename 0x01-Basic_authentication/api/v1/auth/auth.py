#!/usr/bin/env python3
""" implements auth class to manage API authentication. """
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """ Auth class. """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a path.
        Args:
            path: The path to check.
            excluded_paths: List of paths that do not require authentication.
        Return:
            True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith("/"):
            path = path + "/"
        if path in excluded_paths:
            return False
        else:
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

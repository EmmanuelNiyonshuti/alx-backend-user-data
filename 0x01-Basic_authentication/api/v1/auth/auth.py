#!/usr/bin/env python3
""" """
from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """ """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith("/"): path = path + "/"
        if path not in excluded_paths: return True
        if path in excluded_paths: return False

    def authorization_header(self, request=None) -> str:
        """ retrieves the value of the request authorization header.
        Args:
            request: Request object.
        Return:
            value of the header request Authorization, None otherwise."""
        if request is None: return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ """
        return None

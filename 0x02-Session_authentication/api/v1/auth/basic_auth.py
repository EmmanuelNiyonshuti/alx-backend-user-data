#!/usr/bin/env python3
""" implements Basic Auth """

from api.v1.auth.auth import Auth
from models.user import User
import re
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Auth class. """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extract base64 string from the authorization header.
        Args:
            authorization_header (str) - auth string.
        Return:
         base64 string from authorization header if it is valid
         otherwise None."""
        if authorization_header is None or\
                not isinstance(authorization_header, str):
            return None
        if not re.match(r'^Basic\s+[A-Za-z0-9+/]+={0,2}$',
                        authorization_header):

            return None

        auth_list = authorization_header.split(" ")
        auth_str = auth_list[1]
        return auth_str

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        decode a base64 string to a UTF-8 string.
        Args:
            base64_authorization_header (str) - a base64 string.
        Return:
            UTF8 string if base64_authorization_header
            is a valid base64 string otherwise None.
            """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        if not re.match(r'[A-Za-z0-9+/]+={0,2}$', base64_authorization_header):
            return None
        try:
            base64_bytes = base64_authorization_header.encode("utf-8")
            data_bytes = base64.b64decode(base64_bytes)
            return data_bytes.decode("utf-8")
        except (UnicodeDecodeError, base64.binascii.Error):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract credentials from a decoded base64 string.
        Args:
            decoded_base64_authorization_header (str)
        Return:
            a tuple or None if the str is invalid.
            """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user_email, user_pwd = decoded_base64_authorization_header.split(":", 1)
        return (user_email, user_pwd)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns user instance based on his email and password.
        Args:
            user_email (str) - user email.
            user_pwd (str) - user.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        attributes = {"email": user_email}
        users = User.search(attributes)
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user.
        Args:
            request: Request object.
        Return:
            None (to be overridden in subclasses).
        """
        auth_header = self.authorization_header(request)
        base64_str = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(base64_str)
        credentials = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(
                                credentials[0], credentials[1]
                                )
        return user

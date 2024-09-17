#!/usr/bin/env python3
""" implements Basic Auth """

from api.v1.auth.auth import Auth
import re
import base64


class BasicAuth(Auth):
    """ Basic Auth class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract base64 string from the authorization header.
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
        except base64.binascii.Error:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract credentials from a decoded base64 string.
        Args:
            decoded_base64_authorization_header (str)
        Return:
            a tuple or None if the str is invalid.
            """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user = decoded_base64_authorization_header.split(":")
        return (user[0], user[1])

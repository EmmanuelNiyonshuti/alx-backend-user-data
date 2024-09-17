#!/usr/bin/env python3
""" implements Basic Auth """

from api.v1.auth.auth import Auth
import re


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

#!/usr/bin/env python3
""" encrypt password using bcrypt"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash a password.
    Args:
        password (str) - password to be hashed.
    Return:
        byte string representing the password hash.
    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided password matches the hashed password.
    Args:
    hashed_password (bytes) - password hash.
    password (str) - password str.
    Return:
        bool.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

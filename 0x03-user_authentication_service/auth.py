#!/usr/bin/env python3
"""
handle auth.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hash password.
    Args:
        password (str) - input password.
    Return:
        bytes.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password

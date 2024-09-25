#!/usr/bin/env python3
"""
handle user auth.
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User


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


def _generate_uuid() -> str:
    """ generates a uuid4 str"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register a new user.
        Args:
            email (str) - user email.
            password (str) - user password.
        Return:
            user object.
        """
        session = self._db._session
        user = session.query(User).filter_by(email=email).first()
        if user:
            raise ValueError(f"User {email} already exists")
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate user credentials.
        Args:
            email (str) - user email.
            password (str) - user password.
        Return:
            bool.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                password_bytes = password.encode("utf-8")
                return bcrypt.checkpw(password_bytes, user.hashed_password)
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> str:
        """
        """

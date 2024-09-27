#!/usr/bin/env python3
"""
handle user auth.
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional
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
            raise ValueError("User {} already exists".format(email))
        hashed_password = _hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        return new_user

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
            if user is None:
                return False
            password_bytes = password.encode("utf-8")
            return bcrypt.checkpw(password_bytes, user.hashed_password)
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """
        finds a user and set its session id.
        Args:
            email (str) - user email.
        Return:
            session_id (str).
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except (NoResultFound, InvalidRequestError):
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        retrieves a user from the session.
        Args:
            sesssion_id (str)
        Return:
            user object.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a session.
        Args:
            user_id (int).
        Return:
            None.
        """
        try:
            user = self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        set user password reset token.
        Args:
            email (str) - user email.
        Return:
            str.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update user password.
        Args:
            reset_token (str)
            password (str)
        Return:
            None.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update(
                            user.id,
                            hashed_password=hashed_pwd,
                            reset_token=None)
        except NoResultFound:
            raise ValueError

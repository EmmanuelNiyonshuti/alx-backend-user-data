#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.inspection import inspect

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        save the user to the database.
        Args:
            email (str) - user email.
            hashed_password (str) - user password.
        Return:
            User object.
        """
        user = User(
                    email=email,
                    hashed_password=hashed_password
                    )
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs):
        """
        retrieves user from the database based on the provided criteria.
        Args:
            Kwargs: key word args.
        Return:
            user object.
        """
        valid_columns = inspect(User).columns.keys()
        for k in kwargs:
            if k not in valid_columns:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

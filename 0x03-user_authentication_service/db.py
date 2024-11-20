"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User
from user import Base


class DB:
    """DB class
    """
    valid_args = {'email': str,"hashed_password": str, "id": int, 'session_id', int}
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
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: str) -> User:
        """searches for a user in db
        """
        for key, value in kwargs.items():
            if key in self.valid_args:
                user = self._session.query(User).filter_by(**{key: value}).first()
                if not user:
                    raise NoResultFound
                else:
                    return user
            else:
                raise InvalidRequestError

    def update_user(self, user_id, **kwargs: str) -> User:
        """Finds and updates a user using given input"""
        found_user = self.find_user_by(id=user_id)
        if found_user:
            for key, value in kwargs.items():
                if type(kwargs.get(key)) == self.valid_args.get(key):
                    setattr(found_user, key, value)
                    self._session.commit()
                    return found_user
                raise ValueError

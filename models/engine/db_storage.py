#!/usr/bin/python3
"""
using sqlalchemy
"""
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv


class DBStorage:
    """
    class database storage
    """
    __engine = None
    __session = None
    all_classes = ["State", "City", "User", "Place", "Review"]

    def __init__(self):
        """
            constructor function
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        exec_db = 'mysql+mysqldb://{}:{}@{}/{}'.format(
                                            HBNB_MYSQL_USER,
                                            HBNB_MYSQL_PWD,
                                            HBNB_MYSQL_HOST,
                                            HBNB_MYSQL_DB
                                                )
        self.__engine = create_engine(exec_db, pool_pre_ping=True)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database"""
        d = {}
        if cls is None:
            for c in self.all_classes:
                c = eval(c)
                for instance in self.__session.query(c).all():
                    key = instance.__class__.__name__ + '.' + instance.id
                    d[key] = instance
        else:
            for instance in self.__session.query(cls).all():
                key = instance.__class__.__name__ + '.' + instance.id
                d[key] = instance
        return d

    def new(self, obj):
        """
            Creating new instance
        """
        self.__session.add(obj)

    def save(self):
        """
            save db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            delet funtion by object
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
            add new table to database
        """
        Base.metadata.create_all(self.__engine)
        session_db = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_db)
        self.__session = Session()

    def close(self):
        """
            function to close session
        """
        self.reload()
        self.__session.close()

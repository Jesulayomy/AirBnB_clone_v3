#!/usr/bin/python3
""" holds class User"""

from hashlib import md5
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """

    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""

        super().__init__(*args, **kwargs)

    def __setattr__(self, name, val):
        """ Converts the password to an md5 type before storage """

        if name == "password":
            hashed = md5()
            hashed.update(val.encode("utf-8"))
            val = hashed.hexdigest()

        super().__setattr__(name, val)

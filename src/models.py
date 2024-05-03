from db import Base
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime, timedelta
from config import get_settings
import jwt


class Product(Base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True, nullable=False)
    identifier = Column(String(255), index=True)
    price = Column(String(255))
    is_available = Column(Boolean)


class Role(Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255), nullable=False)
    roles = relationship("userRole", back_populates="user")


class userRole(Base):
    __tablename__ = 'userRoles'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'))
    role = Column(String(255))
    user = relationship("User", back_populates="roles")

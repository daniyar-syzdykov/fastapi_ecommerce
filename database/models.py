from sqlalchemy import Integer, String, Column, ForeignKey, MetaData, Boolean, update, delete, select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from .session import async_db_session as session
from .base import DBMixin
from . import Base


class Customer(Base, DBMixin):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    username = Column(String(255), unique=True)
    cart = Column()
    wish_list = Column()


class Product(Base, DBMixin):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    description = Column(String())
    price = Column(Integer())

from sqlalchemy import Table, Integer, String, Column, ForeignKey, MetaData, Boolean, update, delete, select
from sqlalchemy.orm import relationship, joinedload
from ..session import async_db_session as session
from ..base import DBMixin
from .. import Base
class Product(Base, DBMixin):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    description = Column(String())
    price = Column(Integer())
    wish_list = relationship(
        'Customer', secondary='customer_wish_list', back_populates='wish_list')
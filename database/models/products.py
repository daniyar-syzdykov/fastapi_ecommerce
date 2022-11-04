import uuid
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, update, delete, select
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import UUID
from ..base import DBMixin
from .. import Base
from typing import NamedTuple


class Product(Base, DBMixin):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    _uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    name = Column(String(), nullable=False)
    description = Column(String())
    price = Column(Integer())
    wish_list = relationship(
        'Customer', secondary='customer_wish_list', back_populates='wish_list')
    cart = relationship(
        'Customer', secondary='customer_cart', back_populates='cart')

    @property
    def uuid(self):
        return str(self._uuid)

    @classmethod
    async def get_by_id(cls, id, session):
        query = select(Product).where(Product.id == id)
        result = await Product._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    @staticmethod
    def _get_sort_func(rate, order):
        order_by = getattr(Product, order)
        sort_func = getattr(order_by, rate)
        return sort_func

    @classmethod
    async def get_all(cls, session, page_size, page, rate, order):
        sort_func = Product._get_sort_func(rate, order)

        query = select(Product).limit(page_size).offset(
            page_size*(page - 1)).order_by(sort_func())
        result = await Product._execute_query(query, session)
        result = result.all()

        return result

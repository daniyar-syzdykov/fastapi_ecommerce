import uuid
from sqlalchemy import Table, Integer, String, Column, ForeignKey, Boolean, update, delete, select
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
    orders = relationship(
        'Order', secondary='product_orders', back_populates='products')

    @property
    def uuid(self):
        return str(self._uuid)

    @classmethod
    async def get_by_id(cls, id, session, fields_to_joinedload: list[str] = []):
        query = select(Product).where(Product.id == id).options(
            *Product.list_of_fields(fields_to_joinedload))

        result = await Product._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    @staticmethod
    def _get_sort_func(rate, order):
        order_by = getattr(Product, order)
        sort_func = getattr(order_by, rate)
        return sort_func

    @classmethod
    async def get_all(cls, session, page_size, page, rate, order, fields_to_joinedload: list[str] = []):
        sort_func = Product._get_sort_func(rate, order)

        query = select(Product).limit(page_size).offset(page_size*(page - 1)).order_by(
            sort_func()).options(*Product.list_of_fields(fields_to_joinedload))
        result = await Product._execute_query(query, session)
        result = [i[0] for i in result.unique().all()]

        return result


product_orders = Table(
    'product_orders',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('order_id', ForeignKey('orders.id', ondelete='CASCADE')),
    Column('product_id', ForeignKey('products.id', ondelete='CASCADE'))
)

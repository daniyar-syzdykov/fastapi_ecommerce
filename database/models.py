from sqlalchemy import Table, Integer, String, Column, ForeignKey, MetaData, Boolean, update, delete, select
from sqlalchemy.orm import relationship, joinedload
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from .session import async_db_session as session
from .base import DBMixin
from . import Base


customer_wish_list = Table(
    'customer_wish_list',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)

customer_cart = Table(
    'customer_cart',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', ForeignKey('customers.id')),
    Column('product_id', ForeignKey('products.id'))
)


class Customer(Base, DBMixin):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    username = Column(String(255), unique=True)
    cart = relationship('Product', secondary='customer_cart')
    wish_list = relationship(
        'Product', secondary='customer_wish_list', back_populates='wish_list')

    @classmethod
    async def get_by_id(cls, id: int):
        query = select(Customer).where(Customer.id == id).options(
            joinedload(Customer.cart), joinedload(Customer.wish_list))
        # query = select(Customer).where(Customer.id == id).options(
        #     joinedload(Customer.cart))
        try:
            result = await session.execute(query)
            result.unique()
            result = result.unique().one_or_none()
        except Exception as e:
            raise e
        else:
            return result[0] if result else None
        finally:
            await session.close()


class Product(Base, DBMixin):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    description = Column(String())
    price = Column(Integer())
    wish_list = relationship(
        'Customer', secondary='customer_wish_list', back_populates='wish_list')

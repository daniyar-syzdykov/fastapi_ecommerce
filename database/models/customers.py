from sqlalchemy import Table, Integer, String, Column, ForeignKey, MetaData, Boolean, update, delete, select, exists
from sqlalchemy.orm import relationship, joinedload
# from ..session import async_db_session as session
# from ..session import session
from ..base import DBMixin
from .. import Base
from database.utils.hasher import Hasher


class Customer(Base, DBMixin):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    _password = Column(String(), nullable=False)
    is_admin = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)
    cart = relationship('Product', secondary='customer_cart')
    wish_list = relationship(
        'Product', secondary='customer_wish_list', back_populates='wish_list')
    orders = relationship('Order', back_populates='customer')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = Hasher.hash_password(raw_password=raw_password)

    @classmethod
    async def _execute_query(cls, query, session):
        try:
            result = await session.execute(query)
        except Exception as e:
            raise e
        else:
            return result if result else None
        # finally:
        #     await session.close()

    @classmethod
    async def get_all(cls, session):
        query = select(Customer).options(
            joinedload(Customer.cart), joinedload(Customer.wish_list), joinedload(Customer.orders))
        result = await Customer._execute_query(query, session)
        result = [i[0] for i in result.unique().all()]
        return result if result else None

    @classmethod
    async def get_by_id(cls, id: int, session):
        query = select(Customer).where(Customer.id == id).options(
            joinedload(Customer.cart), joinedload(Customer.wish_list), joinedload(Customer.orders))
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None
    
    @classmethod
    async def get_by_username(cls, username: str, session):
        query = select(Customer).where(Customer.username == username).options(
            joinedload(Customer.cart), joinedload(Customer.wish_list), joinedload(Customer.orders))
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None
    
    @classmethod
    async def exists(cls, username, session):
        query = select(Customer).where(Customer.username == username)
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return result

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
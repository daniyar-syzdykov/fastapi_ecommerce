import uuid
from sqlalchemy import Table, Integer, String, Column, ForeignKey, Boolean, text, update, delete, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, joinedload
from ..base import DBMixin
from .. import Base
from security.hasher import Hasher
import inspect


class Customer(Base, DBMixin):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True, nullable=False)
    _uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    name = Column(String(255))
    username = Column(String(255), unique=True, nullable=False)
    _password = Column(String(), nullable=False)
    is_admin = Column(Boolean(), default=False, nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    cart = relationship('Product', secondary='customer_cart',
                        back_populates='cart')
    wish_list = relationship('Product', secondary='customer_wish_list',
                             back_populates='wish_list')
    orders = relationship('Order', back_populates='customer')

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = Hasher.hash_password(raw_password=raw_password)

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
        return True if result else False

    @classmethod
    async def get_customer_with_cart(cls, username, session):
        query = select(Customer).where(Customer.username ==
                                       username).options(joinedload(Customer.cart))
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    @classmethod
    async def get_customer_with_wish_list(cls, username, session):
        query = select(Customer).where(Customer.username ==
                                       username).options(joinedload(Customer.wish_list))
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    async def _modify_field(self, product, field, action, session):
        field = getattr(self, field)
        act = getattr(field, action)
        act(product)
        session.add(self)
        try:
            await session.commit()
        except Exception as e:
            session.rollback()
            raise e
        else:
            return {'success': True}

    async def add_to_field(self, product, field, session):
        return await self._modify_field(product, field, 'append', session)

    async def remove_from_field(self, product, field, session):
        return await self._modify_field(product, field, 'remove', session)

    async def add_to_cart(self, product, session):
        return await self.add_to_field(product, 'cart', session)

    async def remove_from_cart(self, product, session):
        return await self.remove_from_field(product, 'cart', session)

    async def add_to_wish_list(self, product, session):
        return await self.add_to_field(product, 'wish_list', session)

    async def remove_from_wish_list(self, product, session):
        if product not in self.wish_list:
            return False
        return await self.remove_from_field(product, 'wish_list', session)


customer_wish_list = Table(
    'customer_wish_list',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', ForeignKey('customers.id', ondelete='CASCADE')),
    Column('product_id', ForeignKey('products.id', ondelete='CASCADE'))
)

customer_cart = Table(
    'customer_cart',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', ForeignKey('customers.id', ondelete='CASCADE')),
    Column('product_id', ForeignKey('products.id', ondelete='CASCADE'))
)

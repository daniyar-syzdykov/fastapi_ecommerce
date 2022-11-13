import uuid
from sqlalchemy import Table, Integer, String, Column, ForeignKey, Boolean, text, update, delete, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, joinedload
from ..base import DBMixin
from .. import Base
from security.hasher import Hasher
from collections.abc import Iterable


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
    async def get_all(cls, session, fileds_to_load: list[str] = []):
        query = select(Customer).options(
            *Customer.list_of_fields(fileds_to_load))
        result = await Customer._execute_query(query, session)
        result = [i[0] for i in result.unique().all()]
        return result if result else None

    @classmethod
    async def get_by_id(cls, id: int, session, fields_to_load: list[str] = []):
        query = select(Customer).where(Customer.id == id).options(
            *Customer.list_of_fields(fields_to_load))
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    @classmethod
    async def get_by_username(cls, username: str, session, fields_to_load: list[str] = []):
        query = select(Customer).where(Customer.username == username).options(
            *Customer.list_of_fields(fields_to_load))
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    @classmethod
    async def exists(cls, username, session):
        query = select(Customer).where(Customer.username == username)
        result = await Customer._execute_query(query, session)
        result = result.unique().one_or_none()
        return True if result else False

    async def _modify_field(self, obj, field_name, action, session):
        field = getattr(self, field_name)
        act = getattr(field, action)
        act(obj)
        return {'success': True}

    async def _modify_field_and_commit(self, objs: Iterable | object, field_name, action, session):
        if not isinstance(objs, Iterable):
            objs = [objs]

        n = len(objs)
        for _ in range(n):
            await self._modify_field(objs[0], field_name, action, session)
        try:
            session.add(self)
            await session.commit()
            await session.refresh(self)
        except Exception as e:
            raise e

        return {'success': True}

    async def add_to_cart(self, products: Iterable | object, session):
        return await self._modify_field_and_commit(products, 'cart', 'append', session)

    async def remove_from_cart(self, products: Iterable | object, session):
        return await self._modify_field_and_commit(products, 'cart', 'remove', session)

    async def add_to_wish_list(self, products: Iterable | object, session):
        return await self._modify_field_and_commit(products, 'wish_list', 'append', session)

    async def remove_from_wish_list(self, products: Iterable | object, session):
        return await self._modify_field_and_commit(products, 'wish_list', 'remove', session)

    async def add_to_orders(self, orders: Iterable | object, session):
        return await self._modify_field_and_commit(orders, 'orders', 'append', session)

    async def remove_from_orders(self, orders: Iterable | object, session):
        return await self._modify_field_and_commit(orders, 'orders', 'remove', session)


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

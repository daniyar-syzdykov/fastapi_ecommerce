import uuid
import datetime
from sqlalchemy import Integer, String, Column, ForeignKey, MetaData, Boolean, DateTime, select
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import UUID
from ..base import DBMixin
from .. import Base


class Order(Base, DBMixin):
    __tablename__ = 'orders'

    id = Column(Integer(), primary_key=True)
    _uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='orders')
    products = relationship('Product', secondary='product_orders',
                            back_populates='orders')
    created_at = Column(DateTime(), default=datetime.datetime.now())

    @property
    def uuid(self):
        return str(self._uuid)

    async def _modify_field(self, obj, field_name, action, session):
        field = getattr(self, field_name)
        act = getattr(field, action)
        act(obj)
        session.add(self)
        try:
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        else:
            return {'success': True}

    @classmethod
    async def get_by_id(cls, id: int, session, fields: list[str] = []):
        query = select(Order).where(Order.id == id).options(
            *Order.list_of_fields(fields))
        result = await Order._execute_query(query, session)
        result = result.unique().one_or_none()
        return result[0] if result else None

    async def add_to_products(self, product, session):
        return await self._modify_field(product, 'products', 'append', session)

    async def remove_from_products(self, product, session):
        return await self._modify_field(product, 'products', 'remove', session)

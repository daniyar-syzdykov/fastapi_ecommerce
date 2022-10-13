import uuid
import datetime
from sqlalchemy import Integer, String, Column, ForeignKey, MetaData, Boolean, DateTime
from sqlalchemy.orm import relationship, joinedload
from ..session import async_db_session as session
from ..base import DBMixin
from .. import Base


class Order(Base, DBMixin):
    __tablename__ = 'orders'

    id = Column(Integer(), primary_key=True)
    uuid = Column(String(), default=uuid.uuid4)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='orders')
    created_at = Column(DateTime(), default=datetime.datetime.now())

import uuid
from sqlalchemy import Table, Integer, String, Column, ForeignKey, MetaData, Boolean, update, delete, select
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.postgresql import UUID
from ..base import DBMixin
from .. import Base


class Product(Base, DBMixin):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    _uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    name = Column(String(), nullable=False)
    description = Column(String())
    price = Column(Integer())
    wish_list = relationship(
        'Customer', secondary='customer_wish_list', back_populates='wish_list')

    @property
    def uuid(self):
        return str(self._uuid)

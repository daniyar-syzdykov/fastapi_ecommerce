from enum import Enum, auto
from pydantic import Field
from . import BaseCustomerSchema, BaseProductSchema, BaseSchema, BaseOrderSchema, as_form
from .customers import CustomerResultSchema


class Rate(str, Enum):
    asc = 'asc'
    desc = 'desc'


class Order(str, Enum):
    price = 'price'
    name = 'name'
    id = 'id'


class ProductResultSchema(BaseProductSchema):
    cart: list[BaseCustomerSchema] | None = []
    wish_list: list[BaseCustomerSchema] | None = []
    orders: list[BaseOrderSchema] | None = []


@as_form
class ProductCreationSchema(BaseSchema):
    name: str
    description: str | None
    price: int | float


@as_form
class ProductUpdateSchema(BaseSchema):
    name: str | None
    description: str | None
    price: int | float | None


class ProductQuerySchema(BaseSchema):
    order: Order = Order.id
    rate: Rate = Rate.asc
    page_size: int = Field(default=50, gt=0)
    page: int = Field(default=1, gt=0)

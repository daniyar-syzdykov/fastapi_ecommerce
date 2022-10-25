from enum import Enum, auto
from pydantic import Field
from . import BaseCustomerSchema, BaseProductSchema, BaseSchema, as_form


class Rate(str, Enum):
    asc = 'asc'
    desc = 'desc'


class Order(str, Enum):
    price = 'price'
    name = 'name'
    id = 'id'


class ProductResultSchema(BaseProductSchema):
    wish_list: list[BaseCustomerSchema]
    cart: list[BaseCustomerSchema]


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

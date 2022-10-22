import uuid
from pydantic import BaseModel
from sqlalchemy.orm.collections import InstrumentedList
from . import BaseProductSchema, BaseCustomerSchema, BaseOrderSchema, as_form


class CustomerResultSchema(BaseCustomerSchema):
    uuid: str
    wish_list: list[BaseProductSchema]
    cart: list[BaseProductSchema]
    orders: InstrumentedList[BaseOrderSchema]


@as_form
class CustomerCreationSchema(BaseModel):
    username: str
    password: str
    password_2: str


class CustomerAuthSchema(BaseCustomerSchema):
    uuid: str


class CartSchema(BaseModel):
    product_id: int

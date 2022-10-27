from pydantic import BaseModel
from sqlalchemy.orm.collections import InstrumentedList
from . import BaseProductSchema, BaseCustomerSchema, BaseOrderSchema, BaseSchema, as_form


class CustomerResultSchema(BaseCustomerSchema):
    username: str
    uuid: str
    wish_list: list[BaseProductSchema]
    cart: list[BaseProductSchema]
    orders: InstrumentedList[BaseOrderSchema]


@as_form
class CustomerCreationSchema(BaseSchema):
    username: str
    password: str
    password_2: str


class CustomerAuthSchema(BaseCustomerSchema):
    username: str


@as_form
class CustomerUpdateSchema(BaseCustomerSchema):
    username: str | None
    is_active: bool | None


class CartSchema(BaseSchema):
    product_id: int

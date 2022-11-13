from pydantic import BaseModel
from sqlalchemy.orm.collections import InstrumentedList
from . import BaseProductSchema, BaseCustomerSchema, BaseOrderSchema, BaseSchema, as_form


class CustomerResultSchema(BaseCustomerSchema):
    name: str | None
    username: str
    uuid: str
    wish_list: list[BaseProductSchema] | None = []
    cart: list[BaseProductSchema] | None = []
    orders: InstrumentedList[BaseOrderSchema] | None = []


@as_form
class CustomerCreationSchema(BaseSchema):
    username: str
    password: str
    password_2: str


class CustomerAuthSchema(BaseCustomerSchema):
    username: str


@as_form
class CustomerUpdateSchema(BaseSchema):
    name: str | None


class CartSchema(BaseSchema):
    product_id: int

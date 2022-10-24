from pydantic import BaseModel
from sqlalchemy.orm.collections import InstrumentedList
from . import BaseProductSchema, BaseCustomerSchema, BaseOrderSchema, BaseSchema, as_form


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
    pass


@as_form
class CustomerUpdateSchema(BaseCustomerSchema):
    pass


class CartSchema(BaseModel):
    product_id: int

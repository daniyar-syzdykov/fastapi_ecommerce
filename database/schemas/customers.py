import uuid
from pydantic import BaseModel
from . import BaseProductSchema, BaseCustomerSchema, BaseOrderSchema, as_form


class CustomerResultSchema(BaseCustomerSchema):
    uuid: str
    wish_list: list[BaseProductSchema]
    cart: list[BaseProductSchema]
    orders: list[BaseOrderSchema]

    class Config:
        orm_mode = True


@as_form
class CustomerCreationSchema(BaseModel):
    username: str
    password: str
    password_2: str


class CustomerAuthSchema(BaseCustomerSchema):
    uuid: str

    class Config:
        orm_mode = True

class CartSchema(BaseModel):
    products: list[int]
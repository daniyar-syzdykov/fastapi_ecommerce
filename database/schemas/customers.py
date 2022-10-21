import uuid
from pydantic import BaseModel
from . import BaseProductSchema, BaseCustomerSchema, BaseOrderSchema


class CustomerResultSchema(BaseCustomerSchema):
    wish_list: list[BaseProductSchema]
    cart: list[BaseProductSchema]
    orders: list[BaseOrderSchema]

    class Config:
        orm_mode = True


class CustomerCreationSchema(BaseModel):
    username: str
    password: str
    password_2: str


class CustomerAuthSchema(BaseModel):
    username: str
    uuid: str

    class Config:
        orm_mode = True

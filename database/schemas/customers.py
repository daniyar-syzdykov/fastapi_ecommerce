from pydantic import BaseModel
from . import BaseProductSchema, BaseCustomerSchema


class CustomerResultSchema(BaseCustomerSchema):
    wish_list: list[BaseProductSchema]
    cart: list[BaseProductSchema]

    class Config:
        orm_mode = True


class CustomerCreationSchema(BaseModel):
    username: str
    password: str

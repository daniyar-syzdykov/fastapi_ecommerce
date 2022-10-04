from pydantic import BaseModel


class BaseProductSchema(BaseModel):
    id: int
    name: str
    price: int | float


class BaseCustomerSchema(BaseModel):
    id: int
    username: str


class CustomerSchema(BaseCustomerSchema):
    wish_list: list[BaseProductSchema]
    cart: list[BaseProductSchema]

    class Config:
        orm_mode = True


class ProductSchema(BaseProductSchema):
    wish_list: list[BaseCustomerSchema]

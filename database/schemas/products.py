from pydantic import BaseModel
from . import BaseCustomerSchema, BaseProductSchema


class ProductSchema(BaseProductSchema):
    wish_list: list[BaseCustomerSchema]


class ProductCreationSchema(BaseModel):
    name: str
    description: str | None
    price: int

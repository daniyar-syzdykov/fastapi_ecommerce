from pydantic import BaseModel
from . import BaseCustomerSchema, BaseProductSchema, as_form


class ProductSchema(BaseProductSchema):
    wish_list: list[BaseCustomerSchema]


@as_form
class ProductCreationSchema(BaseModel):
    name: str
    description: str | None
    price: int | float

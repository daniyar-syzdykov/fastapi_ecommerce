from . import BaseCustomerSchema, BaseProductSchema, BaseSchema, as_form


class ProductResultSchema(BaseProductSchema):
    wish_list: list[BaseCustomerSchema]
    cart: list[BaseCustomerSchema]


@as_form
class ProductCreationSchema(BaseSchema):
    name: str
    description: str | None
    price: int | float

@as_form
class ProductUpdateSchema(BaseSchema):
    name: str | None
    description: str | None
    price: int | float | None
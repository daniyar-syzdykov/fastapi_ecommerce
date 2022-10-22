from . import BaseCustomerSchema, BaseProductSchema, BaseScheme, as_form


class ProductResultSchema(BaseProductSchema):
    wish_list: list[BaseCustomerSchema]
    cart: list[BaseCustomerSchema]


@as_form
class ProductCreationSchema(BaseScheme):
    name: str
    description: str | None
    price: int | float

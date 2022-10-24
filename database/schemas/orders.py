from . import BaseSchema, BaseProductSchema


class OderSchema(BaseSchema):
    products: list[BaseProductSchema]

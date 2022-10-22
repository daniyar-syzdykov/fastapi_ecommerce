from . import BaseScheme, BaseProductSchema


class OderSchema(BaseScheme):
    products: list[BaseProductSchema]

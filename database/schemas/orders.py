from . import BaseSchema, BaseProductSchema, BaseOrderSchema, BaseCustomerSchema


class OrderResultShema(BaseOrderSchema):
    customer: BaseCustomerSchema
    products: list[BaseProductSchema]

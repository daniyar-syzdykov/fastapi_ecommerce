from pydantic import BaseModel


class BaseCustomerSchema(BaseModel):
    id: int
    username: str


class BaseProductSchema(BaseModel):
    id: int
    name: str
    price: int | float


class BaseOrderSchema(BaseModel):
    id: int
    created_at: str
    products: list[BaseProductSchema]

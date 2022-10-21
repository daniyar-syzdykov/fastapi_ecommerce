import uuid
from pydantic import BaseModel


class BaseCustomerSchema(BaseModel):
    uuid: uuid.UUID
    username: str


class BaseProductSchema(BaseModel):
    id: int
    name: str
    price: int | float


class BaseOrderSchema(BaseModel):
    id: int
    created_at: str
    products: list[BaseProductSchema]

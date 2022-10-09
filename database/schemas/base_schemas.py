from pydantic import BaseModel


class BaseCustomerSchema(BaseModel):
    id: int
    username: str


class BaseProductSchema(BaseModel):
    id: int
    name: str
    price: int | float

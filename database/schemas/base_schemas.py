import inspect
from datetime import datetime
from fastapi import Form
from pydantic import BaseModel


def as_form(cls: BaseModel):
    new_params = []
    for field_name, model_field in cls.__fields__.items():
        new_params.append(
            inspect.Parameter(
                field_name,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form() if model_field.required else Form(
                    model_field.default),
                annotation=model_field.outer_type_
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_params)
    as_form_func.__signature__ = sig
    setattr(cls, 'as_form', as_form_func)
    return cls


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class BaseCustomerSchema(BaseSchema):
    username: str


class BaseProductSchema(BaseSchema):
    id: int
    name: str
    description: str | None
    price: int | float
    uuid: str


class BaseOrderSchema(BaseSchema):
    id: int
    created_at: datetime
    # products: list[BaseProductSchema]

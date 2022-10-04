from fastapi import APIRouter
from fastapi.responses import Response
from database.models import Product
from pydantic import BaseModel


class ProductCreationSchema(BaseModel):
    name: str
    description: str | None
    price: int


product_router = APIRouter(
    prefix='/products'
)


@product_router.get('')
async def get_all_products():
    try:
        products = await Product.get_all()
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': products}


@product_router.get('/{id}')
async def get_products_by_id(id: int):
    try:
        product = await Product.get_by_id(id)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': product.__dict__}


@product_router.post('')
async def create_new_produt(data: ProductCreationSchema):
    try:
        await Product.create(**data.dict())
    except Exception as e:
        raise e
    else:
        return {'success': True}

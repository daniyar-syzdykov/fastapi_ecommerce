from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from database.models import Product
from pydantic import BaseModel
from database.schemas import ProductCreationSchema, ProductResultSchema
from database.session import get_session


product_router = APIRouter(
    prefix='/products'
)


@product_router.get('')
async def get_all_products(session=Depends(get_session)):
    try:
        products = await Product.get_all(session=session)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': products}


@product_router.get('/{id}')
async def get_product_by_id(id: int, session=Depends(get_session)):
    try:
        product_from_db = await Product.get_by_id(id, session=session)

        # if product_from_db is None:
        #     raise HTTPException(status_code=400, detail='This product does not exists')

        product = ProductResultSchema.from_orm(product_from_db)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': product}


@product_router.post('')
async def create_new_produt(data: ProductCreationSchema=Depends(ProductCreationSchema.as_form), session=Depends(get_session)):
    try:
        await Product.create(**data.dict(), session=session)
    except Exception as e:
        raise e
    else:
        return {'success': True}

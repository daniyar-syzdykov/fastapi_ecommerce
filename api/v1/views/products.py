from fastapi import APIRouter, Depends, HTTPException
from database.models import Product, Customer
from database.schemas import ProductUpdateSchema, ProductResultSchema, ProductCreationSchema, ProductQuerySchema
from database.session import get_session
from .auth import get_current_user


product_router = APIRouter(
    prefix='/products'
)


@product_router.get('/')
async def get_all_products(query: ProductQuerySchema = Depends(), session=Depends(get_session)):
    try:
        products = await Product.get_all(session=session, per_page=query.page_size, page=query.page, rate=query.rate, order=query.order)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': products}
    # return {'size': query.page_size, 'page': query.page}


@product_router.get('/{id}')
async def get_product_by_id(id: int, session=Depends(get_session)):
    try:
        product_from_db = await Product.get_by_id(id, session=session)

        if product_from_db is None:
            raise HTTPException(
                status_code=400, detail='This product does not exists')

        product = ProductResultSchema.from_orm(product_from_db)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': product}


@product_router.post('')
async def create_new_produt(user: Customer = Depends(get_current_user), data: ProductCreationSchema = Depends(ProductCreationSchema.as_form), session=Depends(get_session)):
    if not user.is_admin:
        raise HTTPException(status_code=401, detail='You have no permission')

    try:
        await Product.create(**data.dict(), session=session)
    except Exception as e:
        raise e
    else:
        return {'success': True}


@product_router.patch('/{id}')
async def update_product(id: int, user: Customer = Depends(get_current_user), data: ProductUpdateSchema = Depends(ProductUpdateSchema.as_form), session=Depends(get_session)):
    if not user.is_admin:
        raise HTTPException(status_code=401, detail='You have no permission')

    try:
        await Product.update(id=id, session=session, **data.dict())
    except Exception as e:
        raise e
    return {'success': True}


@product_router.delete('/{id}')
async def delete_product(id: int, user: Customer = Depends(get_current_user), session=Depends(get_session)):
    if not user.is_admin:
        raise HTTPException(status_code=401, detail='You have no permission')

    try:
        await Product.delete(id, session)
    except Exception as e:
        raise e
    return {'success': True}

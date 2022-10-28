from fastapi import APIRouter, HTTPException, Depends
from database.models import Customer, Product
from pydantic import parse_obj_as
from database.schemas import CustomerResultSchema, CustomerCreationSchema, CartSchema, BaseProductSchema, CustomerUpdateSchema, CustomerAuthSchema
from database.session import get_session
from .auth import get_current_user, JWT
from sqlalchemy import inspect


customer_router = APIRouter(
    prefix='/customers',
)


@customer_router.get('')
async def get_all_users(customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    if not customer.is_admin:
        raise HTTPException(
            status_code=401, detail='You have no permission to view this page')

    try:
        db_customers = await Customer.get_all(session=session)

        if not db_customers:
            return {'success': False, 'detail': 'There is no users in DB'}

        customers = parse_obj_as(list[CustomerResultSchema], db_customers)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': customers}


@customer_router.get('/{id}')
async def get_user_by_id(id: int, customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    if not customer.is_admin:
        raise HTTPException(
            status_code=401, detail='You have no permission to view this page')

    try:
        db_customer = await Customer.get_by_id(id, session=session)

        if not db_customer:
            return {'success': False, 'detail': 'There is no users in DB'}

        customer = CustomerResultSchema.from_orm(db_customer)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': customer}


@customer_router.patch('/{id}')
async def update_customer_profile(id: int, data: CustomerUpdateSchema = Depends(CustomerUpdateSchema.as_form), customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    try:
        updated_customer = await Customer.update(id=id, session=session, **data.dict())
        print('---------------------------> ', updated_customer.__dict__)
    except Exception as e:
        raise e

    auth_customer = CustomerAuthSchema.from_orm(updated_customer)
    access_token = JWT.gen_new_access_token(auth_customer.dict())

    return {'success': True, 'access_token': access_token, 'token_type': 'bearer'}
    # return {'success': True, 'data': updated_customer}


async def add_to_customer_model_field(data, cutomer: Customer, session):
    pass


@customer_router.post('/cart')
async def add_to_customers_cart(data: CartSchema, customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    product = await Product.get_by_id(data.product_id, session)

    if not product:
        raise HTTPException(
            status_code=400, detail='This product does not exists')

    customer.cart.append(product)
    session.add(customer)

    try:
        await session.commit()
    except Exception as e:
        raise e
    return {'success': True}


@customer_router.post('/wishlist')
async def add_to_customers_wish_list(data: CartSchema, customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    product = await Product.get_by_id(data.product_id, session)

    if not product:
        raise HTTPException(
            status_code=400, detail='This product does not exists')

    customer.wish_list.append(product)
    session.add(customer)

    try:
        await session.commit()
    except Exception as e:
        raise e
    return {'success': True}

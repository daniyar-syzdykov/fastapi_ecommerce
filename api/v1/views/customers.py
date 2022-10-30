from fastapi import APIRouter, HTTPException, Depends
from database.models import Customer, Product
from database.models.customers import customer_cart, customer_wish_list
from pydantic import parse_obj_as
from database.schemas import CustomerResultSchema, CustomerCreationSchema, CartSchema, BaseProductSchema, CustomerUpdateSchema, CustomerAuthSchema
from database.session import get_session
from .auth import get_current_user, get_decoded_token, JWT
from sqlalchemy import exc


customer_router = APIRouter(
    prefix='/customers',
)


async def add_to_customer_field(data, username, field_name, session):
    get_field_func = getattr(Customer, f'get_customer_with_{field_name}')
    customer: Customer = await get_field_func(username, session)

    product: Product = await Product.get_by_id(data.product_id, session)
    add_to_field = getattr(customer, f'add_to_{field_name}')

    if not product:
        raise HTTPException(
            status_code=400, detail='This product does not exists')

    try:
        await add_to_field(product, session)
    except exc.InvalidRequestError:
        raise HTTPException(
            status_code=400, detail=f'This product already in your {field_name}')
    return {'success': True}


async def remove_from_customer_field(data: CartSchema, username: str, field_name, session):
    get_field_func = getattr(Customer, f'get_customer_with_{field_name}')
    customer: Customer = await get_field_func(username, session)
    field = getattr(customer, field_name)
    customer_remove_function = getattr(customer, f'remove_from_{field_name}')

    for product in field:
        if product.id == data.product_id:
            ret = await customer_remove_function(product, session)
            return ret
    return {'success': False}


@customer_router.get('')
async def get_all_customers(customer: Customer = Depends(get_current_user), session=Depends(get_session)):
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
async def get_customer_by_id(id: int, customer: Customer = Depends(get_current_user), session=Depends(get_session)):
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
    if customer.id != id and not customer.is_admin:
        raise HTTPException(
            status_code=400, detail='You have no persmission to edit this profile')

    try:
        updated_customer = await Customer.update(id=id, session=session, **data.dict())
        auth_customer = CustomerAuthSchema.from_orm(updated_customer)
        access_token = JWT.gen_new_access_token(auth_customer.dict())
    except Exception as e:
        raise e

    return {'success': True, 'access_token': access_token, 'token_type': 'bearer'}


@customer_router.post('/cart')
async def add_to_customers_cart(data: CartSchema, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    return await add_to_customer_field(data, token.get('username'), 'cart', session)


@customer_router.post('/wishlist')
async def add_to_customers_wish_list(data: CartSchema, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    return await add_to_customer_field(data, token.get('username'), 'wish_list', session)


@customer_router.delete('/cart')
async def remove_from_customer_cart(data: CartSchema, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    return await remove_from_customer_field(data, token.get('username'), 'cart', session)


@customer_router.delete('/wishlist')
async def remove_from_customer_wish_list(data: CartSchema, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    return await remove_from_customer_field(data, token.get('username'), 'wish_list', session)

from fastapi import APIRouter, HTTPException, Depends
from pydantic import parse_obj_as
from database.models import Customer, Product, Order
from database.schemas import CustomerResultSchema, CustomerCreationSchema, CartSchema, BaseProductSchema, CustomerUpdateSchema, CustomerAuthSchema, OrderResultShema
from database.session import get_session
from .auth import get_current_user, get_decoded_token, JWT
from sqlalchemy import exc


customer_router = APIRouter(
    prefix='/customers',
)


async def add_to_customer_field(data, customer, field_name, session):
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


async def remove_from_customer_field(product_id: int, customer, field_name, session):
    field = getattr(customer, field_name)
    customer_remove_function = getattr(customer, f'remove_from_{field_name}')

    for product in field:
        if product.id == product_id:
            ret = await customer_remove_function(product, session)
            return ret
    return {'success': False}


@customer_router.get('')
async def get_all_customers(customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    if not customer.is_admin:
        raise HTTPException(
            status_code=401, detail='You have no permission to view this page')

    try:
        db_customers = await Customer.get_all(session=session, fileds_to_load=['cart', 'wish_list', 'orders'])

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
        db_customer = await Customer.get_by_id(id, session=session, fields_to_load=['cart', 'wish_list', 'orders'])

        if not db_customer:
            raise HTTPException(
                status_code=404, detail='This customer does not exists')
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
    except Exception as e:
        raise e

    return {'success': True}


@customer_router.post('/cart')
async def add_to_customers_cart(data: CartSchema, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    customer: Customer = await Customer.get_by_username(token.get('username'), session, fields_to_load=['cart'])
    return await add_to_customer_field(data, customer, 'cart', session)


@customer_router.post('/wishlist')
async def add_to_customers_wish_list(data: CartSchema, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    customer: Customer = await Customer.get_by_username(token.get('username'), session, fields_to_load=['wish_list'])
    return await add_to_customer_field(data, customer, 'wish_list', session)


@customer_router.delete('/cart/{product_id}')
async def remove_from_customer_cart(product_id: int, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    customer: Customer = await Customer.get_by_username(token.get('username'), session, fields_to_load=['cart'])
    return await remove_from_customer_field(product_id, customer, 'cart', session)


@customer_router.delete('/wishlist/{product_id}')
async def remove_from_customer_wish_list(product_id: int, token: Customer = Depends(get_decoded_token), session=Depends(get_session)):
    customer: Customer = await Customer.get_by_username(token.get('username'), session, fields_to_load=['wish_list'])
    return await remove_from_customer_field(product_id, customer, 'wish_list', session)


async def create_order(customer: Customer, session) -> Order:
    new_order: Order = await Order.create(session, products=[product for product in customer.cart])
    order: Order = await Order.get_by_id(id=new_order.id, session=session, fields=['customer', 'products'])

    return order


@customer_router.post('/orders', status_code=201)
async def make_purchase(customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    new_order = await create_order(customer, session=session)
    await customer.add_to_orders(new_order, session)
    await customer.remove_from_cart(customer.cart, session)
    return {'success': True}

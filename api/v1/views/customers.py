from fastapi import APIRouter, HTTPException, Depends
from database.models import Customer, Product
from pydantic import parse_obj_as
from database.schemas import CustomerResultSchema, CustomerCreationSchema, CartSchema, BaseProductSchema
from database.session import get_session
from .auth import get_current_user


customer_router = APIRouter(
    prefix='/customers',
)


@customer_router.get('')
async def get_all_users(session=Depends(get_session)):
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
async def get_user_by_id(id: int, session=Depends(get_session)):
    try:
        db_customer = await Customer.get_by_id(id, session=session)

        if not db_customer:
            return {'success': False, 'detail': 'There is no users in DB'}

        customer = CustomerResultSchema.from_orm(db_customer)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': customer}


@customer_router.post('')
async def register_new_user(data: CustomerCreationSchema = Depends(CustomerCreationSchema.as_form), session=Depends(get_session)):
    customer = await Customer.exists(data.username, session=session)

    if customer:
        raise HTTPException(
            status_code=400, detail=f'User with username "{data.username}" already exists')

    if data.password != data.password_2:
        raise HTTPException(status_code=400, detail='Passwords does not match')

    try:
        result = await Customer.create(session=session, username=data.username, password=data.password)
    except Exception as e:
        raise e
    else:
        return {'success': True}


@customer_router.post('/cart')
async def add_to_customers_cart(data: CartSchema, customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    product = await Product.get_by_id(data.product_id, session)
    customer.cart.append(product)
    session.add(customer)
    await session.commit()
    return {'success': True, 'data': customer}

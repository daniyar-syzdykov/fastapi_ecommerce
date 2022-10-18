from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from database.models import Customer
from pydantic import BaseModel, parse_obj_as
from database.schemas import CustomerResultSchema, CustomerCreationSchema
# from database.session import async_db_session as session
from database.session import get_session

# from server import app


customer_router = APIRouter(
    prefix='/customers',
)


@customer_router.get('')
async def get_all_users(session=Depends(get_session)):
    try:
        db_customers = await Customer.get_all(session=session)
        customers = parse_obj_as(list[CustomerResultSchema], db_customers)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': customers}


@customer_router.get('/{id}')
async def get_user_by_id(id: int, session=Depends(get_session)):
    try:
        db_customer = await Customer.get_by_id(id, session=session)
        customer = CustomerResultSchema.from_orm(db_customer)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': customer.__dict__}


@customer_router.post('')
async def register_new_user(data: CustomerCreationSchema, session=Depends(get_session)):
    customer = await Customer.exists(data.username, session=session)
    if customer is not None:
        raise HTTPException(
            status_code=400, detail=f'User with username "{data.username}" already exists')

    if data.password != data.password_2:
        raise HTTPException(status_code=400, detail='Passwords does not match')

    data = data.dict()
    data.pop('password_2')
    try:
        await Customer.create(session=session, **data)
    except Exception as e:
        raise e
    else:
        return {'success': True}


@customer_router.get('/exists/{username}')
async def user_exists(username: str, session=Depends(get_session)):
    try:
        result = await Customer.exists(username, session=session)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': result}


@customer_router.get('/orders')
async def get_users_orders(session=Depends(get_session)):
    try:
        await Customer.get_all(session=session)
    except Exception as e:
        raise e
    else:
        return {'success': True}

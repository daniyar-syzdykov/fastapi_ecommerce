from fastapi import APIRouter
from fastapi.responses import Response
from database.models import Customer
from pydantic import BaseModel, parse_obj_as
from database.schemas import CustomerResultSchema, CustomerCreationSchema


customer_router = APIRouter(
    prefix='/customers',
)


@customer_router.get('')
async def get_all_users():
    try:
        db_customers = await Customer.get_all()
        customers = parse_obj_as(list[CustomerResultSchema], db_customers)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': customers}


@customer_router.get('/{id}')
async def get_user_by_id(id: int):
    try:
        db_customer = await Customer.get_by_id(id)
        customer = CustomerResultSchema.from_orm(db_customer)
    except Exception as e:
        raise e
    else:
        return {'success': True, 'data': customer.__dict__}


@customer_router.post('')
async def register_new_user(data: CustomerCreationSchema):
    try:
        await Customer.create(**data.dict())
    except Exception as e:
        raise e
    return {'success': True}


@customer_router.get('/orders')
async def get_users_orders():
    try:
        await Customer.get_all()
    except Exception as e:
        raise e
    return {'success': True}

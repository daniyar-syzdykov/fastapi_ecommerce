from fastapi import APIRouter
from fastapi.responses import Response
from database.models import Customer
from pydantic import BaseModel
from database.schemas import CustomerSchema



class CustomerCreationSchema(BaseModel):
    username: str


customer_router = APIRouter(
    prefix='/customers',
)


@customer_router.get('')
async def get_all_users():
    customers = await Customer.get_all()
    return {'success': True, 'data': customers}



@customer_router.get('/{id}')
async def get_user_by_id(id: int):
    try:
        db_customer = await Customer.get_by_id(id)
        customer = CustomerSchema.from_orm(db_customer)
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

from fastapi import APIRouter, HTTPException, Depends
from pydantic import parse_obj_as
from database.models import Customer, Product, Order
from database.schemas import BaseProductSchema, BaseCustomerSchema, BaseOrderSchema, OrderResultShema
from database.session import get_session
from .auth import get_current_user, get_decoded_token, JWT
from sqlalchemy import exc

order_router = APIRouter(
    prefix='/orders',
)


@order_router.get('/{id}')
async def get_order_by_id(id: int, customer: Customer = Depends(get_current_user), session=Depends(get_session)):
    try:
        db_order = await Order.get_by_id(id=id, session=session, fields=['customer', 'products'])

        if db_order is None:
            raise HTTPException(
                status_code=404, detail='Order does not exists')

        order = OrderResultShema.from_orm(db_order)

    except Exception as e:
        raise e

    return {'success': True, 'data': order}

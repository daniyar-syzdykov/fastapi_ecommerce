from fastapi import APIRouter
from fastapi.responses import Response
from database.models import Customer
from pydantic import BaseModel, parse_obj_as
from database.schemas import CustomerAuthSchema


auth_router = APIRouter(
    prefix='/auth',
)


@auth_router.post('')
async def auth():
    pass

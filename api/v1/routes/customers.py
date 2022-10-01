from fastapi import APIRouter
from fastapi.responses import Response
from database.models import Customer


customer_router = APIRouter(
    prefix='/customers',
)


@customer_router.get('')
async def get_all_users(request):
    customers = await Customer.get_all()
    return Response({'success': True, 'data': customers})

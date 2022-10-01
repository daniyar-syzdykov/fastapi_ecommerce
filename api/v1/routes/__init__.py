from fastapi import APIRouter

from .customers import customer_router


main_router = APIRouter(prefix='/api')
main_router.include_router(customer_router)
# main_router.add_api_route()

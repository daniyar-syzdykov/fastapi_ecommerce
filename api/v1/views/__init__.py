from fastapi import APIRouter

from .customers import customer_router
from .products import product_router
from .auth import auth_router


main_router = APIRouter(prefix='/api/v1')
main_router.include_router(customer_router)
main_router.include_router(product_router)
main_router.include_router(auth_router)

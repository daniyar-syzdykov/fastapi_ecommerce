from fastapi import APIRouter

from .customers import customer_router
from .products import product_router


main_router = APIRouter(prefix='/api')
main_router.include_router(customer_router)
main_router.include_router(product_router)

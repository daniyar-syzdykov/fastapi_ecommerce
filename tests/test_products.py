import pytest
from .conftest import Env
from httpx import Response


@pytest.mark.asyncio()
async def test_creating_new_product(test_env: Env, random_product: tuple[str, str, float]):
    new_product = {
        'name': random_product[0],
        'description': random_product[1],
        'price': random_product[2]
    }
    response: Response = await test_env.client.post('/api/v1/products', data=new_product)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'success': True}


@pytest.mark.asyncio()
async def test_get_all_products(test_env: Env):
    response: Response = await test_env.client.get('/api/v1/products')
    assert response.status_code == 200

@pytest.mark.asyncio()
async def test_get_product_by_id(test_env: Env):
    response: Response = await test_env.client.get('/api/v1/products/1')
    assert response.status_code == 200
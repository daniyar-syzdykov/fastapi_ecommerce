import pytest
from .conftest import TestEnv
from httpx import Response


@pytest.mark.asyncio()
async def test_creating_new_product(test_env: TestEnv, random_product: tuple[str, str, float]):
    new_product = {
        'name': random_product[0],
        'description': random_product[1],
        'price': random_product[2]
    }
    response: Response = await test_env.client.post('/api/products', json=new_product)
    assert response.status_code == 200
    assert response.json() == {'success': True}


@pytest.mark.asyncio()
async def test_get_all_products(test_env: TestEnv):
    response: Response = await test_env.client.get('/api/products')
    assert response.status_code == 200

@pytest.mark.asyncio()
async def test_get_product_by_id(test_env: TestEnv):
    response: Response = await test_env.client.get('/api/products/1')
    assert response.status_code == 200
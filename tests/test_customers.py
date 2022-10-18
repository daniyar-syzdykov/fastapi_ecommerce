import pytest
from .conftest import TestEnv
from httpx import Response


@pytest.mark.asyncio()
async def test_creating_new_user(test_env: TestEnv, random_user: tuple[str, str]):
    new_user = {'username': random_user[0],
                'password': random_user[1],
                'password_2': random_user[1]}
    response: Response = await test_env.client.post('/api/customers', json=new_user)
    assert response.status_code == 200
    assert response.json() == {'success': True}


@pytest.mark.asyncio()
async def test_getting_all_users(test_env: TestEnv):
    response: Response = await test_env.client.get('/api/customers')
    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_getting_user_by_id(test_env: TestEnv):
    response: Response = await test_env.client.get('/api/customers/1')
    assert response.status_code == 200

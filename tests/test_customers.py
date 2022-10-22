import pytest
from .conftest import Env
from httpx import Response


CACHE = {}


@pytest.mark.asyncio()
async def test_creating_new_user(test_env: Env, random_user: tuple[str, str]):
    new_user = {'username': random_user[0],
                'password': random_user[1],
                'password_2': random_user[1]}

    CACHE.update({'user': new_user})

    response: Response = await test_env.client.post('/api/v1/customers', data=new_user)
    assert response.status_code == 200
    assert response.json() == {'success': True}


@pytest.mark.asyncio()
async def test_get_all_users(test_env: Env):
    response: Response = await test_env.client.get('/api/v1/customers')
    response_json: dict = response.json()
    user: dict = CACHE.get('user')

    assert response.status_code == 200
    response_json.get('data')[0].get('username') == user.get('username')


@pytest.mark.asyncio()
async def test_get_user_by_id(test_env: Env):
    response: Response = await test_env.client.get('/api/v1/customers/1')
    response_json: dict = response.json()
    user: dict = CACHE.get('user')

    assert response.status_code == 200
    assert response_json.get('data').get('username') == user.get('username')


@pytest.mark.asyncio()
async def test_authenticate_user(test_env: Env):
    user: dict = CACHE.get('user')
    response: Response = await test_env.client.post('/api/v1/auth/token', data={'username': user.get('username'), 'password': user.get('password')})
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json.get('access_token')
    assert response_json.get('token_type') == 'bearer'

    CACHE.update(response_json)


@pytest.mark.asyncio()
async def test_validate_user_tokne(test_env: Env):
    response: Response = await test_env.client.get('/api/v1/auth/me', headers={'Authorization': f'Bearer {CACHE.get("access_token")}'})
    response_json: dict = response.json()
    user: dict = CACHE.get('user')

    assert response.status_code == 200
    assert response_json.get('current_user').get(
        'username') == user.get('username')

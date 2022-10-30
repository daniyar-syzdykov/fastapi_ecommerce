import pytest
from .conftest import Env
from httpx import Response
from sqlalchemy import update
from database.models import Customer
from .session import get_test_session
from fastapi import Depends


CACHE = {}


async def make_user_admin(id, session):
    await Customer.update(id, session, is_admin=True)
    return True


@pytest.mark.asyncio()
async def test_creating_new_user(test_env: Env, random_user: tuple[str, str]):
    new_user = {'username': random_user[0],
                'password': random_user[1],
                'password_2': random_user[1]}

    CACHE.update({'user': new_user})
    session = await anext(get_test_session())

    response: Response = await test_env.client.post('/api/v1/auth', data=new_user)
    user_from_db = await Customer.get_by_username(new_user.get('username'), session=session)
    user_is_admin = await make_user_admin(user_from_db.id, session=session)

    assert response.status_code == 201
    assert response.json() == {'success': True}
    assert user_is_admin == True


@pytest.mark.asyncio()
async def test_authenticate_user(test_env: Env):
    user: dict = CACHE.get('user')
    response: Response = await test_env.client.post('/api/v1/auth/token', data={'username': user.get('username'), 'password': user.get('password')})
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json.get('token_type') == 'bearer'

    CACHE.update(response_json)


@pytest.mark.asyncio()
async def test_creating_new_product(test_env: Env, random_product: tuple[str, str, float]):
    new_product = {
        'name': random_product[0],
        'description': random_product[1],
        'price': random_product[2]
    }

    CACHE.update({'product': new_product})
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}

    response: Response = await test_env.client.post('/api/v1/products', data=new_product, headers=headers)
    assert response.status_code == 201
    assert response.json() == {'success': True}


@pytest.mark.asyncio()
async def test_add_to_customer_cart(test_env: Env):
    data = {'product_id': 1}
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.post('/api/v1/customers/cart', json=data, headers=headers)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json == {'success': True}


@pytest.mark.asyncio()
async def test_add_to_customer_wish_list(test_env: Env):
    data = {'product_id': 1}
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.post('/api/v1/customers/wishlist', json=data, headers=headers)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json == {'success': True}


@pytest.mark.asyncio()
async def test_get_all_users(test_env: Env):
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.get('/api/v1/customers', headers=headers)
    response_json: dict = response.json()
    user: dict = CACHE.get('user')

    assert response.status_code == 200
    assert response_json.get('data')[0].get('username') == user.get('username')


@pytest.mark.asyncio()
async def test_get_user_by_id(test_env: Env):
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.get('/api/v1/customers/1', headers=headers)
    response_json: dict = response.json().get('data')
    user_cart: dict = response_json.get('cart')[0]
    user_wish_list: dict = response_json.get('wish_list')[0]
    user: dict = CACHE.get('user')
    product: dict = CACHE.get('product')

    assert response.status_code == 200
    assert response_json.get('username') == user.get('username')
    assert user_cart.get('name') == product.get('name')
    assert user_wish_list.get('name') == product.get('name')


@pytest.mark.asyncio()
async def test_validate_user_tokne(test_env: Env):
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.get('/api/v1/auth/me', headers=headers)
    response_json: dict = response.json()
    user: dict = CACHE.get('user')

    assert response.status_code == 200
    assert response_json.get('current_user').get(
        'username') == user.get('username')


@pytest.mark.asyncio()
async def test_get_all_products(test_env: Env):
    response: Response = await test_env.client.get('/api/v1/products/')
    response_json: dict = response.json().get('data')

    assert response.status_code == 200


@pytest.mark.asyncio()
async def test_get_product_by_id(test_env: Env):
    response: Response = await test_env.client.get('/api/v1/products/1')
    response_json: dict = response.json().get('data')
    product: dict = CACHE.get('product')

    assert response.status_code == 200
    assert response_json.get('name') == product.get('name')
    assert response_json.get('price') == product.get('price')


@pytest.mark.asyncio()
async def test_update_customer_profile(test_env: Env, random_user: tuple[str, str]):
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    new_username = {'username': random_user[0]}
    response: Response = await test_env.client.patch('/api/v1/customers/1', headers=headers, data=new_username)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json.get('success') == True
    assert response_json.get('token_type') == 'bearer'

    CACHE.update({'access_token': response_json.get('access_token')})


@pytest.mark.asyncio()
async def test_remove_from_cutomer_cart(test_env: Env):
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.delete('/api/v1/customers/cart/1', headers=headers)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json == {'success': True}


@pytest.mark.asyncio()
async def test_remove_from_cutomer_wish_list(test_env: Env):
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.delete('/api/v1/customers/wishlist/1', headers=headers)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json == {'success': True}


@pytest.mark.asyncio()
async def test_delete_product(test_env: Env):
    headers = {'Authorization': f'Bearer {CACHE.get("access_token")}'}
    response: Response = await test_env.client.delete('/api/v1/products/1', headers=headers)
    customer: Response = await test_env.client.get('/api/v1/customers/1', headers=headers)
    customer_json: dict = customer.json()
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json == {'success': True}
    assert customer_json.get('cart') is None

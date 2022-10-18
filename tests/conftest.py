import random
import asyncio
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from string import ascii_lowercase, digits
from .test_session import get_test_session, create_tables
from database.session import get_session
from api.v1.views import main_router
# from server import app


class TestEnv:
    def __init__(self, client, app) -> None:
        self.app: FastAPI = app
        self.client: TestClient = client
        # self.session = session


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


def get_env():
    test_app = FastAPI()
    test_app.include_router(main_router)
    client = AsyncClient(app=test_app, base_url='http://127.0.0.1:8000/')
    test_app.dependency_overrides[get_session] = get_test_session
    test_env = TestEnv(client=client, app=test_app)
    yield test_env


async def pytest_sessionstart(session):
    await create_tables()


@pytest_asyncio.fixture(scope='session')
async def connect_to_db():
    await create_tables()


@pytest_asyncio.fixture()
async def test_env():
    test_env = next(get_env())
    return test_env


@pytest_asyncio.fixture()
def random_user() -> tuple[str, str]:
    username = ''
    password = ''
    n = random.randrange(10, 15)
    for _ in range(n):
        username += random.choice(ascii_lowercase + digits)
        password += random.choice(ascii_lowercase + digits)
    return (username, password)


@pytest_asyncio.fixture()
def random_product() -> tuple[str, str, float]:
    name = ''
    description = ''
    price = random.uniform(1000, 10000)
    n = random.randrange(10, 15)
    for _ in range(n):
        name += random.choice(ascii_lowercase + digits)
        description += random.choice(ascii_lowercase + digits)
    return (name, description, price)


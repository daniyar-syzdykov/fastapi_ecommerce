from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER = ''
    POSTGRES_PASSWORD = ''
    POSTGRES_DB = ''
    POSTGRES_HOST = ''
    POSTGRES_PORT = ''

    APP_NAME = 'test_app'

    PRIVATE_KEY = 'private_key'

    # TEST_DB_USER = 'postgres'
    # TEST_DB_PASSWORD = '1234'
    # TEST_DB_HOST = 'localhost'
    # TEST_DB_PORT = '5432'
    # TEST_DB_NAME = 'test_fastapi_ecommerce'

    SECRET = 'a16d4db4e7b13db933e85410ac0b90879fbcd49840248844f6c752336ac295ed'
    ALGORITHM = 'HS256'


settings = Settings()
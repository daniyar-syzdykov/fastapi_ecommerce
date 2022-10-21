from fastapi import FastAPI
from api.v1.views import main_router
from database.session import create_tables, close_connections


app = FastAPI()
app.include_router(main_router)


@app.get('/')
async def main():
    return {'hi': 'there'}


@app.on_event('startup')
async def start():
    await create_tables()


@app.on_event('shutdown')
async def end():
    await close_connections()
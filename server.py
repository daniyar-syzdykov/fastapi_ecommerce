from fastapi import FastAPI
from database.session import async_db_session as session
from api.v1.views import main_router


app = FastAPI()
app.include_router(main_router)


@app.on_event('startup')
async def start():
    await session.init()

@app.on_event('shutdown')
async def end():
    await session.close_connections()

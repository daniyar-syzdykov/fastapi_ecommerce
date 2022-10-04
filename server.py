from fastapi import FastAPI
from database.session import async_db_session as session
from database import Customer
from api.v1.routes import main_router


app = FastAPI()
app.include_router(main_router)


@app.on_event('startup')
async def start():
    await session.init()

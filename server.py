from fastapi import FastAPI
from api.v1.views import main_router


app = FastAPI()
app.include_router(main_router)


@app.get('/')
async def main():
    return {'hi': 'there'}

# @app.on_event('startup')
# async def start():
#     await session.init()

# @app.on_event('shutdown')
# async def end():
#     await session.close_connections()

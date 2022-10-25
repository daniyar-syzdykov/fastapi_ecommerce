import time
import random
import asyncio
import aiohttp

URL = 'http://127.0.0.1:8000/api/v1'


async def create_dummy_users():
    url = URL + '/auth'
    async with aiohttp.ClientSession() as session:
        for i in range(1, 6):
            start = time.perf_counter()
            username = f'testuser{i}'
            user = {
                'username': username,
                'password': 'testpass',
                'password_2': 'testpass'
            }
            async with session.post(url, data=user) as response:
                end = time.perf_counter()
                print(str(end - start) + ':', response.status)


async def create_dummy_products():
    url = URL + '/products'
    headers={'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyMSIsImV4cCI6MTY2NjY3NjMxN30.EvsUwIm2sxES4WWsWgAs2UjsNHK14gVcbue3KWK-xYk'}
    async with aiohttp.ClientSession() as session:
        for i in range(1, 500):
            start = time.perf_counter()
            name = f'product{i}'
            description = f'description{i}'
            product = {
                'name': name,
                'description': description,
                'price': i * 100
            }
            async with session.post(url, data=product, headers=headers) as response:
                end = time.perf_counter()
                print(str(end - start) + ':', response.status)
    


async def main():
    await create_dummy_users()
    await create_dummy_products()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

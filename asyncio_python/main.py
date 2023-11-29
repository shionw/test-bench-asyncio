import asyncio
import aiohttp
import json

URL = "http://127.0.0.1:5000/"
ITEM_URL = "http://127.0.0.1:5000/items"

timeout_seconds = 2
session_timeout = aiohttp.ClientTimeout(
    total=None, sock_connect=timeout_seconds, sock_read=timeout_seconds
)


async def fetch_one(session: aiohttp.ClientSession):
    # hit the endpoint once and print the response
    async with session.get(URL) as response:
        res = await response.text()
        return json.loads(res)["item_id"]


async def item_fetch_one(session: aiohttp.ClientSession, item_id: int):
    # hit the endpoint once and print the response
    async with session.get(f"{ITEM_URL}/{item_id}") as response:
        res = await response.text()
        return json.loads(res)


async def fetch():
    # hit the endpoint 1000 timees asychronously and have a timeout of 3 seconds and print the response as well as handle 500 errors
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        tasks = [fetch_one(session) for _ in range(500)]
        for item in asyncio.as_completed(tasks):
            try:
                res = await item
                item_id = res

                item_res = await item_fetch_one(session, item_id)
                print(item_res)

            except Exception as e:
                print("error", item)


# instead of async.as_completed, we can use asyncio.gather
async def fetch_gather():
    # hit the endpoint 1000 timees asychronously and have a timeout of 3 seconds and print the response as well as handle 500 errors
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        tasks = [asyncio.create_task(fetch_one(session)) for _ in range(500)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, Exception):
                continue
            item_id = res["item_id"]

            item_res = await item_fetch_one(session, item_id)
            print(item_res)


if __name__ == "__main__":
    import time

    start = time.time()
    # asyncio.run(fetch())
    asyncio.run(fetch())
    print(time.time() - start)

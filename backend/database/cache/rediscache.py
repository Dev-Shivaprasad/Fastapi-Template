import redis.asyncio as redis
from redis.asyncio import Redis
from fastapi import FastAPI
import orjson
from contextlib import asynccontextmanager
from utils.helperfunctions import GetEnvVar

cacheurl: str = GetEnvVar("REDIS_URI")


@asynccontextmanager
async def rediscachelifecycle(app: FastAPI):
    if app is None:
        print(
            "Set the refference of fastAPI to Initialise and Uninitialise the Caching"
        )
    else:
        app.state.redis = await redis.from_url(cacheurl, decode_responses=True)
        print("Caching Initialised successfully")
    try:
        yield
    finally:
        await app.state.redis.close()
        print("Caching Uninitialised successfully")


# async def store_cache(app: FastAPI, key: str, value):
#     redis_client: Redis = app.state.redis
#     await redis_client.set(key, orjson.dumps(value).decode())


async def get_cache(app: FastAPI, key: str):
    redis_client: Redis = app.state.redis
    cached = await redis_client.get(key)
    print("Cache hit getcache")
    return orjson.loads(cached) if cached else None


async def invalidate_cache(app: FastAPI, key: str):
    redis_client: Redis = app.state.redis
    await redis_client.delete(key)


async def addorupdate_cache(
    app: FastAPI, key: str, value, otherkeytoupdate: str | None = None
):
    redis_client: Redis = app.state.redis
    data = orjson.dumps(value).decode()

    # Store the main data
    await redis_client.set(key, data)

    if otherkeytoupdate:
        key_type = await redis_client.type(otherkeytoupdate)
        if key_type != b"list":
            await redis_client.delete(otherkeytoupdate)  # clear incorrect type
        redis_client.lpush(otherkeytoupdate, data)

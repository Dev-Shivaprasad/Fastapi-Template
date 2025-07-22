import redis.asyncio as redis
from fastapi import FastAPI
import orjson
from contextlib import asynccontextmanager
from utils.helperfunctions import GetEnvVar

cacheurl: str = GetEnvVar("REDIS_URI")


@asynccontextmanager
async def rediscachelifespan(app: FastAPI):
    if app is None:
        print(
            "Set the refference of fastAPI to Initialise and Uninitialise the Caching"
        )
    else:
        app.state.redis = redis.from_url(cacheurl, decode_responses=True)
        print("Caching Initialised successfully")
    try:
        yield
    finally:
        await app.state.redis.close()
        print("Caching Uninitialised successfully")


async def store_cache(app: FastAPI, key: str, value):
    redis_client = app.state.redis
    await redis_client.set(key, orjson.dumps(value).decode())


async def get_cache(app: FastAPI, key: str):
    redis_client = app.state.redis
    cached = await redis_client.get(key)
    print("Cache hit getcache")
    return orjson.loads(cached) if cached else None


async def invalidate_cache(app: FastAPI, key: str):
    await app.state.redis.delete(key)


async def update_cache(app: FastAPI, todo_id: str, todo_data: dict, ttl: int = 3600):
    redis = app.state.redis
    key = f"todo:{todo_id}"

    # Serialize using orjson (faster than json.dumps)
    encoded_data = orjson.dumps(todo_data)

    # Store the updated todo object
    await redis.set(key, encoded_data, ex=ttl)

    # Maintain the list of todo IDs (ordered list of all todos)
    await redis.lrem("todo:ids", 0, str(todo_id))  # remove if exists
    await redis.lpush(
        "todo:ids", str(todo_id)
    )  # insert at front (change to RPUSH if needed)

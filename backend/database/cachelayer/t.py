import redis.asyncio as redis
from redis.asyncio import Redis
from fastapi import FastAPI
import orjson
from contextlib import asynccontextmanager
from utils.helperfunctions import get_env_var

cacheurl: str = get_env_var("REDIS_URI")


@asynccontextmanager
async def rediscachelifecycle(app: FastAPI):
    """
    Context manager to initialize and clean up the Redis cache connection
    for the FastAPI application lifecycle.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Execution is paused until the context is exited.

    Behavior:
        - Initializes a Redis connection and attaches it to app.state.redis.
        - Closes the Redis connection when the context exits.
    """
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
#     """
#     Stores a value in Redis cache with the specified key.
#
#     Args:
#         app (FastAPI): The FastAPI application instance.
#         key (str): The key under which to store the value.
#         value (Any): The value to store (will be serialized to JSON).
#     """
#     redis_client: Redis = app.state.redis
#     await redis_client.set(key, orjson.dumps(value).decode())


async def get_cache(app: FastAPI, key: str):
    """
    Retrieve a value from Redis cache using the given key.

    Args:
        app (FastAPI): The FastAPI application instance.
        key (str): The key to look up in the cache.

    Returns:
        Any | None: The cached value (deserialized from JSON) if present,
        otherwise None.
    """
    redis_client: Redis = app.state.redis
    cached = await redis_client.get(key)
    print("Cache hit getcache")
    return orjson.loads(cached) if cached else None


async def invalidate_cache(app: FastAPI, key: str):
    """
    Remove a key and its associated value from the Redis cache.

    Args:
        app (FastAPI): The FastAPI application instance.
        key (str): The key to delete from the cache.
    """
    redis_client: Redis = app.state.redis
    await redis_client.delete(key)


async def add_or_update_cache(
    app: FastAPI, key: str, value, otherkeytoupdate: str | None = None
):
    """
    Add or update a value in the Redis cache and optionally update another key.

    Args:
        app (FastAPI): The FastAPI application instance.
        key (str): The primary key under which to store the value.
        value (Any): The value to store (will be serialized to JSON).
        otherkeytoupdate (str | None): Optional secondary key to update
            (used for list-type storage).

    Behavior:
        - Stores the serialized value under the primary key.
        - If otherkeytoupdate is provided and not of type 'list', clears and reinitializes it.
        - Pushes the serialized value into the list at otherkeytoupdate.
    """
    redis_client: Redis = app.state.redis
    data = orjson.dumps(value).decode()

    # Store the main data
    await redis_client.set(key, data)

    if otherkeytoupdate:
        key_type = await redis_client.type(otherkeytoupdate)
        if key_type != b"list":
            await redis_client.delete(otherkeytoupdate)  # clear incorrect type
        redis_client.lpush(otherkeytoupdate, data)

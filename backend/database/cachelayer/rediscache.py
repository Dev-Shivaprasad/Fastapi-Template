import redis.asyncio as redis
from redis.asyncio import Redis
from fastapi import FastAPI
import orjson
from contextlib import asynccontextmanager
from utils.helperfunctions import get_env_var

# Redis connection URL, loaded from environment variables
cacheurl: str = get_env_var("REDIS_URI")

# Global toggle to enable/disable caching across the application
# Set `CACHE_ENABLED=false` in environment variables to disable caching
CACHE_ENABLED = get_env_var("CACHE_ENABLED", "true").lower() == "true"


@asynccontextmanager
async def rediscachelifecycle(app: FastAPI):
    """
    Context manager for managing the Redis cache connection
    during the FastAPI application's lifecycle.

    Behavior:
        - If caching is disabled (`CACHE_ENABLED = False`), skips initialization.
        - If enabled, creates a Redis connection and attaches it to `app.state.redis`.
        - Ensures the connection is closed during application shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Allows FastAPI to continue startup/shutdown sequence.
    """
    if not CACHE_ENABLED:
        print("Redis cache disabled globally.")
        yield
        return

    if app is None:
        print("Set the reference of FastAPI to initialize caching")
    else:
        app.state.redis = await redis.from_url(cacheurl, decode_responses=True)
        print("Caching initialized successfully")
    try:
        yield
    finally:
        await app.state.redis.close()
        print("Caching uninitialized successfully")


async def get_cache(app: FastAPI, key: str):
    """
    Retrieve a cached value from Redis using the specified key.

    Args:
        app (FastAPI): The FastAPI application instance.
        key (str): The Redis key to fetch.

    Returns:
        Any | None:
            - Parsed value (JSON deserialized) if key exists.
            - None if key not found or caching is disabled.
    """
    if not CACHE_ENABLED:
        return None
    redis_client: Redis = app.state.redis
    cached = await redis_client.get(key)
    return orjson.loads(cached) if cached else None


async def invalidate_cache(app: FastAPI, key: str):
    """
    Delete a key and its value from Redis cache.

    Args:
        app (FastAPI): The FastAPI application instance.
        key (str): The Redis key to delete.

    Returns:
        None
    """
    if not CACHE_ENABLED:
        return
    redis_client: Redis = app.state.redis
    await redis_client.delete(key)


async def add_or_update_cache(
    app: FastAPI, key: str, value, otherkeytoupdate: str | None = None
):
    """
    Add or update a value in Redis cache and optionally push it into a list key.

    Behavior:
        - Stores the provided value (JSON serialized) under the primary key.
        - If `otherkeytoupdate` is provided:
            - Ensures it is of type `list` (clears if not).
            - Pushes the serialized value into the list at `otherkeytoupdate`.

    Args:
        app (FastAPI): The FastAPI application instance.
        key (str): The main Redis key for storing data.
        value (Any): The value to store (will be serialized as JSON).
        otherkeytoupdate (str | None): Optional secondary list key to update.

    Returns:
        None
    """
    if not CACHE_ENABLED:
        return
    redis_client: Redis = app.state.redis
    data = orjson.dumps(value).decode()

    # Store the main data under the given key
    await redis_client.set(key, data)

    # Optionally maintain a list-based key for group caching
    if otherkeytoupdate:
        key_type = await redis_client.type(otherkeytoupdate)
        if key_type != b"list":
            await redis_client.delete(otherkeytoupdate)  # Reset if type mismatch
        redis_client.lpush(otherkeytoupdate, data)

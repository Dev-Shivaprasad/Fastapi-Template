from slowapi import Limiter
from slowapi.util import get_remote_address
from utils.helperfunctions import get_env_var


def init_rate_limiter(strategy: str | None = "fixed-window") -> Limiter:
    """
    Initialize and configure a rate limiter using SlowAPI.

    Args:
        strategy (str | None, optional):
            - The rate-limiting strategy to use.
            - Defaults to `"fixed-window"`.
            - Common strategies:
                - `"fixed-window"`: Counts requests per fixed time window.
                - `"moving-window"`: Sliding time window for rate limits.

    Returns:
        Limiter: A configured `Limiter` instance.

    Behavior:
        - `key_func`: Identifies clients using `get_remote_address` (IP-based rate-limiting).
        - `storage_uri`:
            - Defaults to in-memory storage (`memory://`) if `RATELIMITER_STORAGE_URI` is not set.
            - Can be configured to use Redis or other backends (e.g., `redis://` URI).
        - `enabled`:
            - Controlled via the `RATELIMITER_ENABLED` environment variable (default: `"true"`).

    Environment Variables:
        - `RATELIMITER_STORAGE_URI`: URI for rate limiter storage (e.g., Redis).
        - `RATELIMITER_ENABLED`: Enable/disable rate limiting (`true`/`false`).

    Example:
        ```python
        from fastapi import FastAPI
        from slowapi.middleware import SlowAPIMiddleware

        app = FastAPI()

        # Initialize limiter
        limiter = init_rate_limiter()

        # Add middleware for rate limiting
        app.state.limiter = limiter
        app.add_middleware(SlowAPIMiddleware)

        # Use limiter in routes
        @app.get("/limited")
        @limiter.limit("5/minute")
        async def limited_route():
            return {"message": "You are within the limit!"}
        ```
    """
    # Fetch storage URI for rate limiter (defaults to in-memory)
    storageuri = get_env_var("RATELIMITER_STORAGE_URI")

    # Create Limiter instance with strategy, storage, and enabled flag
    Ratelimiter: Limiter = Limiter(
        key_func=get_remote_address,
        strategy=strategy,
        storage_uri="memory://" if storageuri == "" else storageuri,
        enabled=get_env_var("RATELIMITER_ENABLED", "true").lower() == "true",
    )

    return Ratelimiter


def burst_proof_ratelimit(parentlimit: Limiter, limit_value: str):
    """
    Applies two rate limits to a route:
      - A short burst limit (e.g., 2/second)
      - A longer sustained limit (120/minute)
    """

    def decorator(func):
        # Apply burst limit
        func = parentlimit.limit(limit_value=limit_value, per_method=True)(func)
        # Apply sustained limit
        func = parentlimit.limit(limit_value="120/minute", per_method=True)(func)
        return func

    return decorator

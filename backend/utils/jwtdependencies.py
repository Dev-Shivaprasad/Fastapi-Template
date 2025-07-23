# utils/jwt_bearer.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from authentication.auth import verify_jwt

# HTTPBearer security scheme for token-based authentication
security = HTTPBearer()


def JWTBearer(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency for JWT token verification using HTTP Bearer Authentication.

    Args:
        credentials (HTTPAuthorizationCredentials):
            - Automatically extracted by FastAPI from the `Authorization` header.
            - Expected format: `Bearer <JWT token>`.

    Returns:
        dict: The decoded JWT payload if verification is successful.

    Raises:
        HTTPException:
            - 401 UNAUTHORIZED: If the token is invalid or verification fails.

    Workflow:
        1. Extract token from the `Authorization` header.
        2. Pass token to `verify_jwt` for validation and decoding.
        3. If validation fails, raise 401 with the returned error message.
        4. On success, return the payload to be used in protected routes.

    Example:
        ```python
        from fastapi import APIRouter, Depends

        router = APIRouter()

        @router.get("/protected")
        async def protected_route(payload: dict = Depends(JWTBearer)):
            return {"message": "Access granted", "user": payload}
        ```
    """
    # Extract raw token string from credentials
    token = credentials.credentials

    # Verify token using custom verification function
    result: dict = verify_jwt(token)

    # If verification fails, raise 401 Unauthorized
    if result["status"] is not True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=result["statement"]
        )

    # Return decoded payload for use in downstream logic
    return result["payload"]

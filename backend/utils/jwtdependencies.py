# utils/jwt_bearer.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from authentication.auth import verify_jwt  # Import your verify_jwt function

security = HTTPBearer()


def JWTBearer(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    result: dict = verify_jwt(token)

    if result["status"] is not True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=result["statement"]
        )

    return result["payload"]

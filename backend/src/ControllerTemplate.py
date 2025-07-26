from fastapi import APIRouter, Depends
from services.jwtdependencies import JWTBearer


Your_Route_Name = APIRouter(dependencies=[Depends(JWTBearer)])

## YOUR ROUTES HERE

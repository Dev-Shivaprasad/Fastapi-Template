from fastapi import APIRouter, Depends
from utils.jwtdependencies import JWTBearer


Your_Route_Name = APIRouter(dependencies=[Depends(JWTBearer)])

## YOUR ROUTES HERE

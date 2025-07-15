from fastapi import APIRouter, Depends, HTTPException, status

from authentication.auth import generate_jwt, verify_jwt
from database.DB import Session, get_session
from sqlmodel import select
from models.Auth_model import login, user

AuthRoutes = APIRouter()


@AuthRoutes.post("/login/")
async def logindef(userdata: login, session: Session = Depends(get_session)):
    # Retrive data from the DB and embed it with the specfiv attributs
    # It is better to create a Schema of the payload

    data = session.exec(select(user).where(user.EmailId == userdata.Email)).first()
    if data is not None and data.EmailId == userdata.Email:
        return await generate_jwt(
            payload={
                "mail": data.EmailId,
                "username": data.UserName,
                "userid": str(data.UserId),
            }
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with EmailId {userdata.Email} Not found",
    )


@AuthRoutes.post("/register/")
async def Reg(userreg: user, session: Session = Depends(get_session)):
    isavail = session.exec(select(user).where(user.EmailId == userreg.EmailId)).first()
    if isavail is not None and isavail.EmailId == userreg.EmailId:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND, detail="User already exists"
        )
    session.add(userreg)
    session.commit()
    session.refresh(userreg)
    return userreg


@AuthRoutes.post("/validatejwt/")
async def validatejwt(token: str):
    return verify_jwt(token=token)


# @AuthRoutes.post("/auth/register/")
# async def Register(register: user, session: Session = Depends(get_session)):
#     session.add(register)
#     session.commit()
#     session.refresh(register)
#     return register

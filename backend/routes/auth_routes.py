from fastapi import APIRouter, Depends, HTTPException, status
from utils.helperfunctions import is_valid_email
from authentication.auth import generate_jwt, verify_jwt
from database.DB import Session, get_session
from sqlmodel import select
from models.Auth_model import login, user

AuthRoutes = APIRouter()


@AuthRoutes.post("/login/")
async def logindef(userdata: login, session: Session = Depends(get_session)):
    # Retrive data from the DB and embed it with the specfic attributs
    # It is better to create a Schema of the payload

    data = session.exec(select(user).where(user.emailid == userdata.email)).first()
    if data is not None and data.emailid == userdata.email:
        return await generate_jwt(
            payload={
                "mail": data.emailid,
                "username": data.username,
                "userid": str(data.userid),
            }
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with emailid {userdata.email} Not found",
    )


@AuthRoutes.post("/register/")
async def Reg(userreg: user, session: Session = Depends(get_session)):
    if not is_valid_email(userreg.emailid):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email is invalid"
        )
    isavail = session.exec(select(user).where(user.emailid == userreg.emailid)).first()
    if isavail is not None and isavail.emailid == userreg.emailid:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User already with mail id {userreg.emailid} already exists",
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

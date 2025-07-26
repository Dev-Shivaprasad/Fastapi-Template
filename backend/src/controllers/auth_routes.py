from fastapi import APIRouter, Depends, HTTPException, status
from core.helperfunctions import is_valid_email, hashpassword, verifypassword
from core.authentication.auth import generate_jwt
from core.database.DB import Session, get_session
from sqlmodel import select
from src.models.Auth_model import login, user

AuthRoutes = APIRouter(prefix="/auth")


@AuthRoutes.post("/login/")
async def logindef(userdata: login, session: Session = Depends(get_session)):
    # Retrieve user by email
    user_obj = session.exec(select(user).where(user.emailid == userdata.email)).first()

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {userdata.email} not found",
        )

    # Verify password
    if not await verifypassword(userdata.password, user_obj.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    # Generate JWT if password matches
    return await generate_jwt(
        payload={
            "mail": user_obj.emailid,
            "username": user_obj.username,
            "userid": str(user_obj.userid),
        }
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

    newuser = user(
        username=userreg.username,
        emailid=userreg.emailid,
        password=await hashpassword(userreg.password),
    )
    session.add(newuser)
    session.commit()
    session.refresh(newuser)
    return newuser

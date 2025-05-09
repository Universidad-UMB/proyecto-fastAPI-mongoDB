from fastapi import APIRouter, Depends
from schemas.user_schema import User
from schemas.user_login_schema import UserLogin
from services import user_service
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.get("/greeting")
async def greeting():
    return {"message": "Hello world finance"}

@router.post("/register")
async def userRegister(user: User ):
    return await user_service.userRegister(user)

@router.post("/login")
async def login(formData: OAuth2PasswordRequestForm = Depends()):
    user = UserLogin(email=formData.username, password=formData.password)
    currentUser = await user_service.authenticateUser(user)
    accessTokenExpires = timedelta(minutes=30)
    token = user_service.createAccessToken(data={"sub": currentUser["email"]}
                                           , expiresDelta=accessTokenExpires)

    return {"access_token": token, "token_type": "bearer"}

@router.get("/greeting-protected")
def greetingProtected(user = Depends(user_service.decodeAccessToken)):
    return {"user: ": user["email"]}
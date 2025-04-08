from fastapi import HTTPException, Depends
from app.schemas.user_schema import User
from app.schemas.user_login_schema import UserLogin
from app.db.database import collectionItem
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from app.services import category_service

SECRET_KEY = "b8b31e99cf7efbd87920b8c81926bd45b05bbbd1"
ALGORITHM = "HS256"



encrypt = CryptContext(schemes=["bcrypt"], deprecated="auto") 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



async def userRegister(user: User ):
    newUser = user.model_dump()
    
    if await collectionItem.users.find_one({"email": newUser["email"]}):
        raise HTTPException(status_code=409, detail="El correo ya se encuentra registrado, inicie sesion o registre uno nuevo")
    
    newUser["password"] = hashPasword(newUser["password"])
    
    result = await collectionItem.users.insert_one(newUser)
    
    await category_service.createDefaultCategories(result.inserted_id)
    
    return {
        "message": "Usuario creado correctamente",
        "user": newUser["email"]
    }



async def authenticateUser(user: UserLogin):
    userLogin = user.model_dump()
    
    currentUser = await collectionItem.users.find_one({"email": userLogin["email"]})

    if not currentUser or not verifyPassword(userLogin["password"], currentUser["password"]):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    
    return currentUser

def hashPasword(password: str):
    return encrypt.hash(password)

def verifyPassword(plainPassword: str, passwordHash: str):
    return encrypt.verify(plainPassword, passwordHash )


def createAccessToken(data: dict, expiresDelta: Optional[timedelta]=None):
    toEncode = data.copy()
    
    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    toEncode.update({"exp":expire})
    
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encodedJWT



async def decodeAccessToken(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, 
                                detail="Credenciales no validas",
                                headers={"WWW-Authenticate": "Bearer"})
        
        currentUser = await collectionItem.users.find_one({"email": email})
        return currentUser
    except ExpiredSignatureError:
        raise HTTPException(status_code=401,  
                            detail="El token ha expirado, inicia sesion nuevamente",
                            headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401,  
                            detail="El token no es valido",
                            headers={"WWW-Authenticate": "Bearer"})
        
        
        
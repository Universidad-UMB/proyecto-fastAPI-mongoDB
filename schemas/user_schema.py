from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    lastName: str
    email: EmailStr
    password: str
    
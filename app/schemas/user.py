from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
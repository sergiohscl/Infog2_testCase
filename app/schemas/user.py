from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

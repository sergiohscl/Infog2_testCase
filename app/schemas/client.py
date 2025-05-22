from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True

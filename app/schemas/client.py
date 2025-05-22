from pydantic import BaseModel, EmailStr, ConfigDict


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

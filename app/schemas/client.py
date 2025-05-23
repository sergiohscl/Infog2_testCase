from pydantic import BaseModel, EmailStr, ConfigDict, constr

telefone_regex = r"^55\d{10,11}$"


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    telefone: constr(strict=True, pattern=telefone_regex)  # type: ignore


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

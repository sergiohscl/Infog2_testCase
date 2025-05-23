from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class ProductBase(BaseModel):
    nome_produto: str
    descricao: Optional[str] = None
    preco_venda: float
    estoque: int
    validade: Optional[date] = None
    disponivel: Optional[bool] = True
    imagem: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

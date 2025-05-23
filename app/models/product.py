from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nome_produto = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco_venda = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    validade = Column(Date, nullable=True)
    disponivel = Column(Boolean, default=True)
    imagem = Column(String, nullable=True)

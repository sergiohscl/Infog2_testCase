from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# Tabela associativa pedido <-> produto
order_product_table = Table(
    "pedido_products",
    Base.metadata,
    Column("pedido_id", ForeignKey("pedidos.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)


class StatusEnum(str, enum.Enum):
    aguardando = "aguardando"
    pago = "pago"
    enviado = "enviado"
    cancelado = "cancelado"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    data_pedido = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(StatusEnum), default=StatusEnum.aguardando)

    cliente = relationship("Client")
    produtos = relationship("Product", secondary=order_product_table)

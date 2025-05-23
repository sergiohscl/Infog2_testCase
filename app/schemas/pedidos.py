from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime
from enum import Enum


class StatusEnum(str, Enum):
    aguardando = "aguardando"
    pago = "pago"
    enviado = "enviado"
    cancelado = "cancelado"


class PedidoCreate(BaseModel):
    cliente_id: int
    produtos_ids: List[int]


class PedidoUpdate(BaseModel):
    status: StatusEnum


class PedidoOut(BaseModel):
    id: int
    cliente_id: int
    status: StatusEnum
    data_pedido: datetime
    produtos_ids: List[int]

    model_config = ConfigDict(from_attributes=True)

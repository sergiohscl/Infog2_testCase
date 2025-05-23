from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.models.pedidos import Pedido, StatusEnum
from app.models.product import Product
from app.models.client import Client
from app.schemas.pedidos import PedidoCreate, PedidoOut, PedidoUpdate
from app.core.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[PedidoOut])
def list_pedidos(
    cliente_id: Optional[int] = None,
    id_pedido: Optional[int] = None,
    status: Optional[StatusEnum] = None,
    produto_id: Optional[int] = None,
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(Pedido)

    if cliente_id:
        query = query.filter(Pedido.cliente_id == cliente_id)
    if id_pedido:
        query = query.filter(Pedido.id == id_pedido)
    if status:
        query = query.filter(Pedido.status == status)
    if data_inicio:
        query = query.filter(Pedido.data_pedido >= data_inicio)
    if data_fim:
        query = query.filter(Pedido.data_pedido <= data_fim)
    if produto_id:
        query = query.join(Pedido.produtos).filter(Product.id == produto_id)

    pedidos = query.all()

    return [
        PedidoOut(
            id=pedido.id,
            cliente_id=pedido.cliente_id,
            status=pedido.status,
            data_pedido=pedido.data_pedido,
            produtos_ids=[prod.id for prod in pedido.produtos]
        )
        for pedido in pedidos
    ]


@router.post("/", response_model=PedidoOut, status_code=201)
def create_pedido(
    data: PedidoCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cliente = db.query(Client).filter(Client.id == data.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    produtos = db.query(
        Product
    ).filter(Product.id.in_(data.produtos_ids)).all()
    if len(produtos) != len(data.produtos_ids):
        raise HTTPException(
            status_code=400, detail="Um ou mais produtos não existem."
        )

    for produto in produtos:
        if produto.estoque <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Produto {produto.nome_produto} sem estoque."
            )
        produto.estoque -= 1

    pedido = Pedido(cliente_id=data.cliente_id, produtos=produtos)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return PedidoOut(
        id=pedido.id,
        cliente_id=pedido.cliente_id,
        status=pedido.status,
        data_pedido=pedido.data_pedido,
        produtos_ids=[p.id for p in produtos]
    )


@router.get("/{id}", response_model=PedidoOut)
def get_pedido(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return PedidoOut(
        id=pedido.id,
        cliente_id=pedido.cliente_id,
        status=pedido.status,
        data_pedido=pedido.data_pedido,
        produtos_ids=[p.id for p in pedido.produtos]
    )


@router.put("/{id}", response_model=PedidoOut)
def update_pedido(
    id: int,
    data: PedidoUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    pedido.status = data.status
    db.commit()
    db.refresh(pedido)
    return PedidoOut(
        id=pedido.id,
        cliente_id=pedido.cliente_id,
        status=pedido.status,
        data_pedido=pedido.data_pedido,
        produtos_ids=[p.id for p in pedido.produtos]
    )


@router.delete("/{id}", status_code=204)
def delete_pedido(
    id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    db.delete(pedido)
    db.commit()

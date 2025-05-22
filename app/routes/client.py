from app.models.client import Client
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas import client as schemas
from app.models import client as models
from app.core.database import get_db
from typing import List
from app.core.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.ClientOut])
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(models.Client).all()


@router.post("/", response_model=schemas.ClientOut, status_code=201)
def create_client(
    data: schemas.ClientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if db.query(Client).filter(Client.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    if db.query(Client).filter(Client.cpf == data.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    new_client = Client(**data.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@router.get("/{id}", response_model=schemas.ClientOut)
def get_client(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return client


@router.put("/{id}", response_model=schemas.ClientOut)
def update_client(
    id: int,
    data: schemas.ClientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    if db.query(Client).filter(
        Client.email == data.email, Client.id != id
    ).first():
        raise HTTPException(
            status_code=400, detail="Email já em uso por outro cliente."
        )

    if db.query(Client).filter(
        Client.cpf == data.cpf, Client.id != id
    ).first():
        raise HTTPException(
            status_code=400, detail="CPF já em uso por outro cliente."
        )

    for field, value in data.dict().items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client


@router.delete("/{id}", status_code=204)
def delete_client(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    db.delete(client)
    db.commit()
    return

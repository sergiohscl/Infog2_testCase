from datetime import datetime
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import ProductCreate, ProductOut
from app.models.product import Product
from app.core.database import get_db
from app.core.deps import get_current_user
from uuid import uuid4

router = APIRouter()
UPLOAD_DIR = "static/img"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=List[ProductOut])
def list_products(
    produto: Optional[str] = None,
    disponivel: Optional[bool] = None,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(Product)

    if produto:
        query = query.filter(Product.secao.ilike(f"%{produto}%"))
    if disponivel is not None:
        query = query.filter(Product.disponivel == disponivel)
    if preco_min is not None:
        query = query.filter(Product.preco_venda >= preco_min)
    if preco_max is not None:
        query = query.filter(Product.preco_venda <= preco_max)

    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=ProductOut)
def create_product(
    nome_produto: str = Form(...),
    descricao: str = Form(...),
    preco_venda: float = Form(...),
    estoque: int = Form(...),
    validade: Optional[str] = Form(None),
    disponivel: Optional[bool] = Form(True),
    imagem: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    image_url = None
    if imagem:
        ext = imagem.filename.split(".")[-1]
        filename = f"{uuid4()}.{ext}"
        file_path = os.path.join("static/img", filename)
        image_url = f"/static/img/{filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)

    validade_date = None
    if validade:
        try:
            validade_date = datetime.strptime(validade, "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Formato inválido para validade. Use DD-MM-AAAA."
            )

    product = Product(
        nome_produto=nome_produto,
        descricao=descricao,
        preco_venda=preco_venda,
        estoque=estoque,
        validade=validade_date,
        disponivel=disponivel,
        imagem=image_url
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{id}", response_model=ProductOut)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product


@router.put("/{id}", response_model=ProductOut)
def update_product(
    id: int,
    data: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    for attr, value in data.model_dump().items():
        setattr(product, attr, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{id}", status_code=204)
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    db.delete(product)
    db.commit()
    return

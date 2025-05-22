from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from app.core.config import settings
from sqlalchemy.orm import Session
from app.schemas.user import LoginRequest, UserCreate, UserOut
from app.models.user import User
from app.core.database import get_db
from app.core.security import decode_access_token, hash_password, verify_password, create_access_token # noqa E501

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, name=user.name, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(
        login_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/refresh-token")
def refresh_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Token ausente ou inválido"
        )

    token = auth_header.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=401, detail="Token inválido ou expirado"
        )

    new_token = create_access_token(
        data={"sub": payload.get("sub")},
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes)
    )
    return {"access_token": new_token, "token_type": "bearer"}

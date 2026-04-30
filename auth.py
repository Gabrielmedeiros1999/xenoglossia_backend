from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET      = os.getenv("JWT_SECRET")
ALGORITHM       = "HS256"
EXPIRA_EM_HORAS = 24

pwd_context     = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme   = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ─── Senha ────────────────────────────────────────────────────────────────────

def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash: str) -> bool:
    return pwd_context.verify(senha, hash)

# ─── JWT ──────────────────────────────────────────────────────────────────────

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    expira  = datetime.utcnow() + timedelta(hours=EXPIRA_EM_HORAS)
    payload.update({"exp": expira})
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

# ─── Usuário autenticado ──────────────────────────────────────────────────────

def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    payload  = decodificar_token(token)
    email    = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return usuario
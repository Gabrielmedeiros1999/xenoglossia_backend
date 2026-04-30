from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario
from schemas import UsuarioCadastro, UsuarioLogin, TokenResponse
from auth import hash_senha, verificar_senha, criar_token, get_usuario_atual

router_auth = APIRouter(prefix="/auth", tags=["Auth"])

@router_auth.post("/cadastro", status_code=201)
def cadastrar(dados: UsuarioCadastro, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    usuario = Usuario(
        nome       = dados.nome,
        email      = dados.email,
        senha_hash = hash_senha(dados.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return {"mensagem": "Usuário cadastrado com sucesso", "id": usuario.id}


@router_auth.post("/login", response_model=TokenResponse)
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = criar_token({"sub": usuario.email})
    return TokenResponse(access_token=token)


@router_auth.get("/me")
def perfil_atual(usuario: Usuario = Depends(get_usuario_atual)):
    """Rota protegida — retorna os dados do usuário logado."""
    return {
        "id":         usuario.id,
        "nome":       usuario.nome,
        "email":      usuario.email,
        "criado_em":  usuario.criado_em,
    }
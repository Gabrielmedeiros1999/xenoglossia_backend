from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario, Traducao
from schemas import UsuarioCadastro, UsuarioLogin, TokenResponse, UsuarioAtualizar, AlterarSenhaSchema
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

    token = criar_token({"sub": str(usuario.id)})
    return TokenResponse(access_token=token)


@router_auth.get("/me")
def perfil_atual(usuario: Usuario = Depends(get_usuario_atual)):
    """Rota protegida — retorna os dados do usuário logado."""
    return {
        "id":         usuario.id,
        "nome":       usuario.nome,
        "email":      usuario.email,
    }

@router_auth.put("/perfil")
def atualizar_perfil(
    dados: UsuarioAtualizar,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    existe = (
        db.query(Usuario)
        .filter(
            Usuario.email == dados.email,
            Usuario.id != usuario.id
        )
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="E-mail já está em uso"
        )

    usuario.nome = dados.nome
    usuario.email = dados.email

    db.commit()
    db.refresh(usuario)

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
    }

@router_auth.put("/alterar-senha")
def alterar_senha(
    dados: AlterarSenhaSchema,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    if not verificar_senha(
        dados.senha_atual,
        usuario.senha_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Senha atual incorreta"
        )

    usuario.senha_hash = hash_senha(
        dados.nova_senha
    )

    db.commit()

    return {
        "mensagem": "Senha alterada com sucesso"
    }

@router_auth.delete("/conta")
def apagar_conta(
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db)
):
    
    db.query(Traducao).filter(Traducao.usuario_id == usuario.id).delete()

    db.delete(usuario)
    db.commit()

    return {"mensagem": "Conta apagada com sucesso"}
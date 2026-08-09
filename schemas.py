from pydantic import BaseModel, EmailStr, field_validator
import re

class UsuarioCadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, senha: str):
        if len(senha) < 8:
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres"
            )
        
        if len(senha) > 64:
            raise ValueError(
                "A senha deve ter no máximo 64 caracteres"
            )

        if not re.search(r"[A-Z]", senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiúscula"
            )
        
        if not re.search(r"[0-9]", senha):
            raise ValueError(
                "A senha deve conter pelo menos um número"
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial"
            )

        return senha

class AlterarSenhaSchema(BaseModel):
    senha_atual: str
    nova_senha: str

    @field_validator("nova_senha")
    @classmethod
    def validar_senha(cls, senha: str):
        if len(senha) < 8:
            raise ValueError(
                "A senha deve ter pelo menos 8 caracteres"
            )

        if len(senha) > 64:
            raise ValueError(
                "A senha deve ter no máximo 64 caracteres"
            )

        if not re.search(r"[0-9]", senha):
            raise ValueError(
                "A senha deve conter pelo menos um número"
            )
        
        if not re.search(r"[A-Z]", senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiúscula"
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial"
            )

        return senha
    
class UsuarioAtualizar(BaseModel):
    nome: str
    email: EmailStr
class TraducaoRequest(BaseModel):
    texto: str
    origem: str
    destino: str
    modo: str = "texto"

class TraducaoResponse(BaseModel):
    id: int
    traducao: str
    arquivo_audio: str | None = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
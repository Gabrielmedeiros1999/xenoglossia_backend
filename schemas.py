from pydantic import BaseModel, EmailStr

class TraducaoRequest(BaseModel):
    texto: str
    origem: str
    destino: str
    modo: str = "texto"

class TraducaoResponse(BaseModel):
    id: int
    traducao: str
    arquivo_audio: str | None = None

class UsuarioCadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
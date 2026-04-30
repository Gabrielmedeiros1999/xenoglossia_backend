from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from deep_translator import GoogleTranslator
from functools import lru_cache
from database import get_db
from models import Traducao
from schemas import TraducaoRequest
from auth import decodificar_token
from typing import Optional

router = APIRouter()

# Carrega idiomas suportados
IDIOMAS = GoogleTranslator(source='auto', target='en').get_supported_languages(as_dict=True)
IDIOMAS_PT = {}

# Cache de tradução (🔥 ganho grande de performance)
@lru_cache(maxsize=1000)
def traduzir_cache(texto: str, origem: str, destino: str):
    tradutor = GoogleTranslator(source=origem, target=destino)
    return tradutor.translate(texto)


@router.get("/idiomas")
def listar_idiomas():
    return IDIOMAS_PT


@router.post("/traduzir")
def traduzir(
    request: TraducaoRequest,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(default=None)
):
    # valida idiomas
    codigos_validos = set(IDIOMAS.values())
    if request.origem not in codigos_validos or request.destino not in codigos_validos:
        raise HTTPException(status_code=400, detail="Idioma não suportado")

    # tradução com cache
    try:
        texto_traduzido = traduzir_cache(
            request.texto.strip(),
            request.origem,
            request.destino
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao traduzir texto")

    # salvar histórico (se autenticado)
    registro_id = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            decodificar_token(token)

            registro = Traducao(
                texto=request.texto,
                traducao=texto_traduzido,
                origem=request.origem,
                destino=request.destino,
                modo=request.modo,
            )
            db.add(registro)
            db.commit()
            db.refresh(registro)

            registro_id = registro.id
        except:
            pass  # ignora erro de auth sem quebrar tradução

    return {
        "id": registro_id,
        "traducao": texto_traduzido
    }


@router.get("/historico")
def historico(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Traducao)\
        .order_by(Traducao.criado_em.desc())\
        .limit(limit)\
        .all()


@router.delete("/historico/{traducao_id}")
def deletar_traducao(traducao_id: int, db: Session = Depends(get_db)):
    registro = db.get(Traducao, traducao_id)

    if not registro:
        raise HTTPException(status_code=404, detail="Tradução não encontrada")

    db.delete(registro)
    db.commit()

    return {"mensagem": "Tradução removida com sucesso"}
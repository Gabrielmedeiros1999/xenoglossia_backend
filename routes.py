from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, File, Form
from sqlalchemy.orm import Session
from deep_translator import GoogleTranslator
from functools import lru_cache
from database import get_db
from models import Traducao, Usuario
from schemas import TraducaoRequest
from auth import decodificar_token, get_usuario_atual
from typing import Optional
from groq import Groq
from auth import decodificar_token, get_usuario_atual
import os
import base64

router = APIRouter()

# Carrega idiomas suportados
IDIOMAS = GoogleTranslator(source='auto', target='en').get_supported_languages(as_dict=True)

# Cliente Groq
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY não configurada")
    return Groq(api_key=api_key)

# Cache de tradução
@lru_cache(maxsize=1000)
def traduzir_cache(texto: str, origem: str, destino: str):
    tradutor = GoogleTranslator(source=origem, target=destino)
    return tradutor.translate(texto)

@router.post("/traduzir")
def traduzir(
    request: TraducaoRequest,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(default=None)
):
    codigos_validos = set(IDIOMAS.values())
    if request.origem not in codigos_validos or request.destino not in codigos_validos:
        raise HTTPException(status_code=400, detail="Idioma não suportado")

    try:
        texto_traduzido = traduzir_cache(
            request.texto.strip(),
            request.origem,
            request.destino
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao traduzir texto")

    registro_id = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            dados_token = decodificar_token(token)
            usuario = db.query(Usuario)\
                .filter(Usuario.email == dados_token["sub"])\
                .first()
            
            registro = Traducao(
                texto=request.texto,
                traducao=texto_traduzido,
                origem=request.origem,
                destino=request.destino,
                modo=request.modo,
                usuario_id=usuario.id
            )
            db.add(registro)
            db.commit()
            db.refresh(registro)
            registro_id = registro.id
        except:
            pass

    return {
        "id": registro_id,
        "traducao": texto_traduzido
    }

@router.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

@router.get("/historico")
def historico(limit: int = 20, usuario: Usuario = Depends(get_usuario_atual), db: Session = Depends(get_db)):
    return ( 
        db.query(Traducao)
        .filter(Traducao.usuario_id == usuario.id)
        .order_by(Traducao.criado_em.desc())
        .limit(limit)
        .all()
    )


@router.delete("/historico/{traducao_id}")
def deletar_traducao(traducao_id: int, usuario: Usuario = Depends(get_usuario_atual), db: Session = Depends(get_db)):
    registro = (
        db.query(Traducao)
        .filter(
            Traducao.id == traducao_id,
            Traducao.usuario_id == usuario.id
        )
        .first()
    )

    if not registro:
        raise HTTPException(status_code=404, detail="Tradução não encontrada")
    db.delete(registro)
    db.commit()
    return {"mensagem": "Tradução removida com sucesso"}


@router.post("/traduzir-imagem")
async def traduzir_imagem(
    file: UploadFile = File(...),
    origem: str = Form(...),
    destino: str = Form(...),
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
        b64_image = base64.b64encode(contents).decode("utf-8")
        content_type = file.content_type or "image/jpeg"

        client = get_groq_client()
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{content_type};base64,{b64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Extract all visible text from this image. Return only the extracted text, no comments or explanations."
                        }
                    ]
                }
            ],
            max_tokens=1024,
        )

        texto_extraido = response.choices[0].message.content.strip()

        if not texto_extraido:
            raise HTTPException(status_code=400, detail="Nenhum texto encontrado na imagem")

        traducao = GoogleTranslator(source=origem, target=destino).translate(texto_extraido)

        registro_id = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            try:
                dados_token = decodificar_token(token)

                usuario = db.query(Usuario)\
                    .filter(Usuario.email == dados_token["sub"])\
                    .first()
                
                registro = Traducao(
                    texto=texto_extraido,
                    traducao=traducao,
                    origem=origem,
                    destino=destino,
                    modo="imagem",
                    usuario_id=usuario.id
                )
                db.add(registro)
                db.commit()
                db.refresh(registro)
                registro_id = registro.id
            except:
                pass

        return {
            "id": registro_id,
            "texto_extraido": texto_extraido,
            "traducao": traducao
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/traduzir-voz")
async def traduzir_voz(
    file: UploadFile = File(...),
    origem: str = Form(...),
    destino: str = Form(...),
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()

        # Transcrição com Groq Whisper
        client = get_groq_client()
        transcricao = client.audio.transcriptions.create(
            file=("audio.webm", contents, "audio/webm"),
            model="whisper-large-v3-turbo",
            language=origem,
            response_format="text",
        )

        texto_transcrito = transcricao.strip() if isinstance(transcricao, str) else transcricao.text.strip()

        if not texto_transcrito:
            raise HTTPException(status_code=400, detail="Nenhuma fala detectada no áudio")

        # Tradução
        traducao = GoogleTranslator(source=origem, target=destino).translate(texto_transcrito)

        registro_id = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            try:
                dados_token = decodificar_token(token)

                usuario = db.query(Usuario)\
                    .filter(Usuario.email == dados_token["sub"])\
                    .first()
                
                registro = Traducao(
                    texto=texto_transcrito,
                    traducao=traducao,
                    origem=origem,
                    destino=destino,
                    modo="voz",
                    usuario_id=usuario.id
                )
                db.add(registro)
                db.commit()
                db.refresh(registro)
                registro_id = registro.id
            except:
                pass

        return {
            "id": registro_id,
            "texto_transcrito": texto_transcrito,
            "traducao": traducao
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
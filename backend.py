from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import router, IDIOMAS_PT
from routes_auth import router_auth
import json
import os

app = FastAPI(title="Tradutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_JSON = os.path.join(BASE_DIR, "idiomas_pt.json")


def carregar_idiomas():
    if not os.path.exists(CAMINHO_JSON):
        raise FileNotFoundError("❌ idiomas_pt.json não encontrado no backend")

    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        IDIOMAS_PT.update(json.load(f))

    print("✅ Idiomas carregados com sucesso")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    carregar_idiomas()


app.include_router(router)
app.include_router(router_auth)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import router, IDIOMAS, IDIOMAS_PT
from routes_auth import router_auth
from deep_translator import GoogleTranslator
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

def traduzir_idiomas():
    if os.path.exists("idiomas_pt.json"):
        with open("idiomas_pt.json", "r", encoding="utf-8") as f:
            IDIOMAS_PT.update(json.load(f))
        return

    for nome_en, codigo in IDIOMAS.items():
        try:
            nome_pt = GoogleTranslator(source='en', target='pt').translate(nome_en)
            nome_pt = nome_pt.title()
        except:
            nome_pt = nome_en.title()

        IDIOMAS_PT[nome_pt] = codigo

    # salva no arquivo
    with open("idiomas_pt.json", "w", encoding="utf-8") as f:
        json.dump(IDIOMAS_PT, f, ensure_ascii=False, indent=2)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    traduzir_idiomas() 

app.include_router(router)
app.include_router(router_auth)
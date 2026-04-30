from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Traducao(Base):
    __tablename__ = "traducoes"
    id        = Column(Integer, primary_key=True, index=True)
    texto     = Column(Text, nullable=False)
    traducao  = Column(Text, nullable=False)
    origem    = Column(String(10), nullable=False)
    destino   = Column(String(10), nullable=False)
    modo      = Column(String(10), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Usuario(Base):
    __tablename__ = "usuarios"
    id            = Column(Integer, primary_key=True, index=True)
    nome          = Column(String(100), nullable=False)
    email         = Column(String(150), unique=True, nullable=False, index=True)
    senha_hash    = Column(String(255), nullable=False)
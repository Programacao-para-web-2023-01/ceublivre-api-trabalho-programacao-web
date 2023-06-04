from sqlalchemy import Column, ForeignKey, String, Date, DateTime, Integer
from sqlalchemy.orm import relationship
from src.core.configs import settings
import datetime

class User(settings.DBBaseModel):
    __tablename__ = "users"
    id : str = Column(String(250), primary_key=True)
    nome_completo: str = Column(String(250), nullable=False)
    genero: str = Column(String(250), nullable=False)
    cpf: str = Column(String(250), nullable=False)
    email: str = Column(String(250), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    senha: str = Column(String(250), nullable=False)
    preferencia_comunicacao: str = Column(String(250), nullable=False)
    cep: str = Column(String(250), nullable=False)
    telefone: str = Column(String(250), nullable=False)
    endereco: str = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class PaymentInformation(settings.DBBaseModel):
    __tablename__ = "dados_bancarios_pagamento"
    id : str = Column(String(250), primary_key=True)
    nome_titular: str = Column(String(250), nullable=False)
    data_nasc = Column(Date, nullable=False)
    numero_cartao = Column(String(250), nullable=False)
    data_validade = Column(Date, nullable=False)
    user_id = Column(String(250), ForeignKey("users.id"), nullable=False)
    user = relationship(User, backref='dados_bancarios_pagamento')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class ReceiveInformation(settings.DBBaseModel):
    __tablename__ = "dados_bancarios_recebimento"
    id : str = Column(String(250), primary_key=True)
    conta_corrente: str = Column(String(250), nullable=False)
    banco: str = Column(String(250), nullable=False)
    agencia: str = Column(String(250), nullable=False)
    user_id = Column(String(250), ForeignKey("users.id"), nullable=False)
    user = relationship(User, backref='dados_bancarios_recebimento')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

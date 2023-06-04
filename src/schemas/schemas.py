from typing import Optional
from fastapi import Body
from datetime import date, datetime
from pydantic import BaseModel


class User(BaseModel):
    nome_completo: str = None
    genero: str = None
    cpf: str = None
    email: str = None
    data_nascimento: date = None
    senha: str = None
    preferencia_comunicacao: str = None
    cep: str = None
    telefone: str = None
    endereco: str = None

    class Config:
        orm_mode: True


class UpdateUser(BaseModel):
    nome_completo: Optional[str]
    genero: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    preferencia_comunicacao: Optional[str]
    cep: Optional[str]
    telefone: Optional[str]
    endereco: Optional[str]

    class Config:
        orm_mode: True


class PaymentsInformation(BaseModel):
    nome_titular: str
    data_nasc: date
    numero_cartao: str
    validade: date
    user_id: Optional[str]

    class Config:
        orm_mode: True

class UpdatePaymentsInformation(BaseModel):
    nome_titular: str
    data_nasc: date
    numero_cartao: str
    validade: date

    class Config:
        orm_mode: True

class ReceiveInformation(BaseModel):
    conta: str
    banco: str
    agencia: str
    user_id: Optional[str]

    class Config:
        orm_mode: True

class UpdateReceiveInformation(BaseModel):
    conta: str
    banco: str
    agencia: str

    class Config:
        orm_mode: True




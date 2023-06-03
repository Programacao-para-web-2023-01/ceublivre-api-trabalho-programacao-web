from typing import Optional
from fastapi import Body
from datetime import date, datetime
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[str] = Body(None)
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
    created_at: datetime = Body(None)
    updated_at: datetime = Body(None)

    class Config:
        orm_mode: True


class PaymentsInformation(BaseModel):
    id: Optional[str] = Body(None)
    nome_titular: str
    data_nasc: date
    numero_cartao: str
    validade: date
    user_id: str
    created_at: datetime = Body(None)
    updated_at: datetime = Body(None)

    class Config:
        orm_mode: True

class BankDataReceipt:
    id: Optional[str] = Body(None)
    conta: str
    banco: str
    agencia: str
    user_id: str
    created_at: datetime = Body(None)
    updated_at: datetime = Body(None)




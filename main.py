import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from psycopg2 import sql, Error
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, EmailStr, ValidationError
from datetime import date, datetime

app = FastAPI()


conn = psycopg2.connect("postgresql://matheus:<ENTER-SQL-USER-PASSWORD>@db-app-693.g8x.cockroachlabs.cloud:26257/db-app?sslmode=require")

# Modelo de dados de usuário
class User(BaseModel):
    id: str
    rg_type: bool = None #RG_Type = 1 = Vendedor || RG_Type = 0 = Usuario normal
    full_name: str = None
    genero: str = None
    cpf: str = None 
    email: str = None
    birthday: date = None
    password: str = None
    preferencia_comunicacao: str = None
    cep: str = None
    phone: str = None
    address: str = None
    created_at: datetime = None
    updated_at: datetime = None



# Registro de usuário
@app.post("/register/user")
async def register_user(user: User):
    try:
        # Inserir dados do usuário na tabela de usuários
        insert_query = sql.SQL(
            "INSERT INTO users (id, rg_type, full_name, genero, cpf, email, birthday, password, preferencia_comunicacao, cep, phone, address) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
        ).format(
            sql.Literal(user.id),
            sql.Literal(user.rg_type),
            sql.Literal(user.name),
            sql.Literal(user.gender),
            sql.Literal(user.cpf),
            sql.Literal(user.email),
            sql.Literal(user.birthday),
            sql.Literal(user.password),
            sql.Literal(user.preferencia_comunicacao),
            sql.Literal(user.cep),
            sql.Literal(user.phone),
            sql.Literal(user.address)
        )

        conn.cursor.execute(insert_query)
        conn.commit()
    except (ValidationError, Error) as e:
        raise HTTPException(status_code=400, detail=f"Erro ao registrar: {e}")

    # Mensagem de sucesso
    return {"message": "Registro concluido!"}

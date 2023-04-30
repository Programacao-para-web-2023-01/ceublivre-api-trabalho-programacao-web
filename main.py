import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from psycopg2 import sql, Error
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, EmailStr, ValidationError
from datetime import date, datetime
import datetime
app = FastAPI()


conn = psycopg2.connect("postgresql://matheus:<ENTER-SQL-USER-PASSWORD>@db-app-693.g8x.cockroachlabs.cloud:26257/db-app?sslmode=require")
update_sql = 'UPDATE users set full_name = %s, genereo = %s, email = %s, password = %s, preferencia_comunicacao = %s, cep = %s, phone = %s, address, updated_at = %s WHERE id = %s'
get_by_id_sql = 'SELECT * FROM users WHERE id = %s'

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


class EditUser(BaseModel):
    full_name: str = None
    genero: str = None
    email: str = None
    password: str = None
    preferencia_comunicacao: str = None
    cep: str = None
    phone: str = None
    address: str = None
    updated_at: datetime = None


# Registro de usuário
@app.post("/users")
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


# Edit usuário
@app.put("/users/{user_id}")
async def edit_user(id: str, edit_user: EditUser):
    try:
        conn.cursor().execute(update_sql, [id])
        row = conn.cursor().fetchone()
        if row is None:
            raise Exception(f"user with ID {id} not found")
    except Exception as error:
        return str(error)
    
    try:
        updated_user = EditUser(
            full_name=edit_user.full_name,
            genero=edit_user.genero,
            email=edit_user.email,
            password = edit_user.password,
            preferencia_comunicacao=edit_user.preferencia_comunicacao,
            cep = edit_user.preferencia_comunicacao,
            phone=edit_user.phone,
            address=edit_user.address,
            updated_at=datetime.datetime.now()
        )
        conn.cursor().execute(update_sql, (updated_user.full_name, updated_user.genero, updated_user.email, updated_user.password, updated_user.preferencia_comunicacao, updated_user.cep, updated_user.phone, updated_user.address, updated_user.updated_at))
        conn.commit()
        conn.cursor().close()
        conn.close()
        result = {'id': row[0], 
                  'rg_type': row[1],
                  'full_name':updated_user.full_name, 
                  'genero':updated_user.genero, 
                  'cpf': row[4], 
                  'email':updated_user.email, 
                  'birthday': row[6], 
                  'preferencia_comunicacao': updated_user.preferencia_comunicacao, 
                  'cep': updated_user.cep, 'address': updated_user.cep, 
                  'created_at': row[12], 
                  'updated_at': updated_user.updated_at }
        return result
    except Exception as error:
            return f"Error in update: {error}"

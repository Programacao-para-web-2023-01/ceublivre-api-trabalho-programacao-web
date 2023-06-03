from fastapi import Depends, FastAPI, HTTPException
from datetime import datetime
from src.errors.errors import DatabaseError, DuplicateEntryError

from src.schemas.schemas import User
from src.core.database import check_database_connection
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.infra.sqlalchemy.repositories.user_repository import UserRepository



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    if not await check_database_connection():
        raise RuntimeError("Failed to connect to the database")



def validate(user: User):
    if user.nome_completo:
     return "Insiera um nome"

    if user.genero == "":
        return "insira um genero"

    if user.cpf == "":
        return "Insira um cpf"
    if user.telefone == "":
        return "Insira um telefone"

    if user.endereco == "":
        return "Insira um address"

    if user.preferencia_comunicacao == "":
        return "Insira um preferencia de comunicacao"

    if user.email == "":
        return "insira um email!"

    if user.senha == "":
        return "Insira uma senha"
    
    return None


@app.get("/")
async def hello():
    return {"Hello world"}


# Registro de usuário
@app.post("/users")
async def create(user: User, db: AsyncSession = Depends(get_session)):
    try:
        newUser = await UserRepository(db).create(user)
        return newUser
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))


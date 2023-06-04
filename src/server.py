from fastapi import Depends, FastAPI, HTTPException
from datetime import datetime
from src.errors.errors import DatabaseError, DuplicateEntryError, NotFoundError

from src.schemas.schemas import User, UpdateUser, PaymentsInformation, ReceiveInformation
from src.core.database import check_database_connection
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.infra.sqlalchemy.repositories.user_repository import UserRepository
from src.infra.sqlalchemy.repositories.payments_repository import PaymentRepository
from src.infra.sqlalchemy.repositories.receive_repository import ReceiveRepository



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    if not await check_database_connection():
        raise RuntimeError("Failed to connect to the database")



def validate(user: User):
    if user.nome_completo:
     return "Insira um nome"

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

@app.put("/users/{userId}")
async def update(updateUser: UpdateUser, userId:str, db: AsyncSession = Depends(get_session)):
    try:
        await UserRepository(db).update(userId, updateUser)
        return {"Usuario atualizado com sucesso"}
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/users/{userId}/paymentInformation")
async def create(paymentInformation: PaymentsInformation, userId:str, db: AsyncSession = Depends(get_session)):
    try:
        paymentInformation = await PaymentRepository(db).createPaymentInformation(userId, paymentInformation)
        return paymentInformation
    
    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/users/{userId}/receiveInformation")
async def create(receiveInformation: ReceiveInformation, userId:str, db: AsyncSession = Depends(get_session)):
    try:
        receiveInformation = await ReceiveRepository(db).createReceiveInformation(userId, receiveInformation)
        return receiveInformation

    except NotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except DuplicateEntryError as error:
        raise HTTPException(status_code=406, detail=str(error))
    except DatabaseError as error:
        raise HTTPException(status_code=500, detail=str(error))


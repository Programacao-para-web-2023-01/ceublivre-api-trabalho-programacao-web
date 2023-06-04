from sqlalchemy import update
from src.schemas import schemas
from src.infra.sqlalchemy.models.models import User
from src.dto.dto import CreateUserOutput
from src.utils.utils import value_exists, selectValue
from src.errors.errors import DuplicateEntryError, DatabaseError, NotFoundError
from src.core.hash import hash_password
from datetime import datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    async def create(self, userSchema: schemas.User):
        async with self.db as session:
            userExists = await value_exists(self.db, User, User.email, userSchema.email)
            if userExists:
                 raise DuplicateEntryError('Já existe um usuário com este CPF cadastrado. Faca login')
            
            newUser = User(
                id=str(uuid.uuid4()),
                nome_completo=userSchema.nome_completo,
                genero=userSchema.genero,
                cpf=userSchema.cpf,
                email=userSchema.email,
                data_nascimento=userSchema.data_nascimento,
                senha=hash_password(userSchema.senha),
                preferencia_comunicacao=userSchema.preferencia_comunicacao,
                cep=userSchema.cep,
                telefone=userSchema.telefone,
                endereco=userSchema.endereco,
                 created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            userOutput = CreateUserOutput(
                id=newUser.id,
                nome_completo=newUser.nome_completo,
                genero=newUser.nome_completo,
                cpf=newUser.cpf,
                email=newUser.email,
                data_nascimento=newUser.data_nascimento,
                preferencia_comunicacao=newUser.preferencia_comunicacao,
                cep=newUser.cep,
                telefone=newUser.telefone,
                endereco=newUser.endereco,
                created_at=newUser.created_at,
                updated_at=newUser.updated_at
            )

        try:
            session.add(newUser)
            await session.commit()
            return userOutput
        except Exception as error:
            await session.rollback()
            print(f"Error ao inserir no banco de dados: {str(error)}")
            raise DatabaseError(f"Ocorreu um erro ao adicionar o usuário: {str(error)}")
    
    async def update(self, userId:str, updateSchema: schemas.UpdateUser):
        async with self.db as session:
            userExists = await selectValue(self.db, User, User.id, userId)
            if not userExists:
                 raise NotFoundError('Usuário não encontrado')
            hashPassword = hash_password(updateSchema.senha)

            
            query = update(User).where(User.id == userId).values(
                nome_completo=updateSchema.nome_completo,
                genero=updateSchema.genero,
                email=updateSchema.email,
                senha=hashPassword,
                preferencia_comunicacao=updateSchema.preferencia_comunicacao,
                cep=updateSchema.cep,
                telefone=updateSchema.telefone,
                endereco=updateSchema.endereco,
                updated_at = datetime.now()
            )
            try:
                 await session.execute(query)
                 await session.commit()
            except Exception as error:
                await session.rollback()
                print(f"Error ao atualizar no banco de dados: {str(error)}")
                raise DatabaseError(f"Ocorreu um erro ao atualizar o usuário: {str(error)}")
    

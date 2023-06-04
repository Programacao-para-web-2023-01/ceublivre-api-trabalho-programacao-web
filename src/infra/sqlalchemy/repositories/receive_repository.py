import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.errors.errors import DatabaseError, DuplicateEntryError, NotFoundError
from src.infra.sqlalchemy.models.models import User, ReceiveInformation
from src.schemas import schemas
from src.utils.utils import value_exists
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

class ReceiveRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
   
    async def createReceiveInformation(self, userId: str, receiveInformationSchema: schemas.ReceiveInformation):
            async with self.db as session:
                userExists = await value_exists(self.db, User, User.id, userId)
                if not userExists:
                    raise NotFoundError('Usuário nao encontrado')

                receiveInformation = await value_exists(self.db, ReceiveInformation, ReceiveInformation.user_id, userId)
                if receiveInformation:
                    raise DuplicateEntryError('Já existe informações de recebimento para esse usuário. Atualize os valores caso queira mudar algo')
                
                newReceiveInformation = ReceiveInformation(
                    id = str(uuid.uuid4()),
                    conta_corrente=receiveInformationSchema.conta,
                    banco=receiveInformationSchema.banco,
                    agencia=receiveInformationSchema.agencia,
                    user_id=userId,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                try:
                    session.add(newReceiveInformation)
                    await session.commit()
                    return newReceiveInformation
                except Exception as error:
                    await session.rollback()
                    print(f"Error ao inserir no banco de dados: {str(error)}")
                    raise DatabaseError(f"Ocorreu um erro ao adicionar uma nova informacao de recebimento: {str(error)}")
import datetime
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from src.errors.errors import DatabaseError, DuplicateEntryError, NotFoundError
from src.infra.sqlalchemy.models.models import PaymentInformation, User, ReceiveInformation
from src.schemas import schemas
from src.utils.utils import selectValue, value_exists
import uuid
from datetime import datetime


class PaymentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, userId:str):
            paymentInformation = await selectValue(self.db, PaymentInformation, PaymentInformation.user_id, userId)
            if not paymentInformation:
                 raise NotFoundError('Informações de pagamento não encontradas')
            
            return paymentInformation

    async def createPaymentInformation(self, userId: str, paymentInformationSchema: schemas.PaymentsInformation):
        async with self.db as session:
            userExists = await value_exists(self.db, User, User.id, userId)
            if not userExists:
                raise NotFoundError('Usuário nao encontrado')

            paymentInformation = await value_exists(self.db, PaymentInformation, PaymentInformation.user_id, userId)
            if paymentInformation:
                 raise DuplicateEntryError('Já existe informações de pagamento para esse usuário. Atualize os valores caso queira mudar algo')
            
            
            newPaymentInformation = PaymentInformation(
                id = str(uuid.uuid4()),
                nome_titular=paymentInformationSchema.nome_titular,
                data_nasc=paymentInformationSchema.data_nasc,
                numero_cartao=paymentInformationSchema.numero_cartao,
                data_validade=paymentInformationSchema.validade,
                user_id=userId,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            try:
                session.add(newPaymentInformation)
                await session.commit()
                return newPaymentInformation
            except Exception as error:
                await session.rollback()
                print(f"Error ao inserir no banco de dados: {str(error)}")
                raise DatabaseError(f"Ocorreu um erro ao adicionar uma nova informacao de pagamento: {str(error)}")
    
    async def updatePaymentInformation(self, userId: str, updatePaymentInformationSchema: schemas.UpdatePaymentsInformation):
        async with self.db as session:
            userExists = await value_exists(self.db, PaymentInformation, PaymentInformation.user_id, userId)
            if not userExists:
                 raise NotFoundError('Informações de pagamento não encontrada.')
            
            query = update(PaymentInformation).where(PaymentInformation.user_id == userId).values(
                nome_titular=updatePaymentInformationSchema.nome_titular,
                data_nasc=updatePaymentInformationSchema.data_nasc,
                numero_cartao=updatePaymentInformationSchema.numero_cartao,
                data_validade=updatePaymentInformationSchema.validade,
                updated_at=datetime.now()
            )

            try:
                 await session.execute(query)
                 await session.commit()
            except Exception as error:
                await session.rollback()
                print(f"Error ao atualizar no banco de dados: {str(error)}")
                raise DatabaseError(f"Ocorreu um erro ao atualizar a informação de pagamento: {str(error)}")
    
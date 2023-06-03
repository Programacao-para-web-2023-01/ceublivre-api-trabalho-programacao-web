from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from sqlalchemy import Column, exists
from sqlalchemy.future import select


async def value_exists(db: AsyncSession, model: Any, coluna: Column, valor: Any) -> bool:
    async with db as session:
        consulta = select(exists().where(coluna == valor)).select_from(model)
        resultado = await session.execute(consulta)
        return resultado.scalar()

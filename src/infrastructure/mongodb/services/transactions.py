from contextlib import asynccontextmanager
from typing import AsyncGenerator

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.errors import PyMongoError

from src.infrastructure.application import DatabaseError

from src.config import settings
from .session import Session as MongoSession

__all__ = ("transaction_mongo",)

from ..collections import FundsCollection, UsersCollection, LogTransactionsFundsCollection, SubscriptionCollection

__beanie_models__ = [FundsCollection, UsersCollection, LogTransactionsFundsCollection, SubscriptionCollection]


async def init_db():
    """Inicializa la base de datos MongoDB usando Beanie."""
    mongo_session = MongoSession(db_name=settings.DB_NAME)  # Instancia de la clase MongoSession
    await mongo_session.start_session()

    try:
        session: AsyncIOMotorClientSession = mongo_session._session
        # Inicializa Beanie con los modelos de la base de datos
        await init_beanie(
            database=session.client[mongo_session._db.name],  # Selecciona la base de datos
            document_models=__beanie_models__,  # Modelos Beanie
        )
    finally:
        await mongo_session.end_session()


#TODO convert to strategy
@asynccontextmanager
async def transaction_mongo() -> AsyncGenerator[AsyncIOMotorClientSession, None]:
	"""Context manager to handle MongoDB transactions."""
	mongo_session = MongoSession()  # Instancia de la clase de MongoDB adaptada
	await mongo_session.start_session()

	session: AsyncIOMotorClientSession = mongo_session._session

	try:
		# Inicialización de Beanie con los modelos
		await init_beanie(
			database=session.client[settings.DB_NAME],  # Selecciona la base de datos
			document_models=__beanie_models__  # Los modelos de Beanie que usarás
		)

		yield session
		# MongoDB no necesita commit explícito para operaciones sin transacciones.
	except PyMongoError as error:
		# logger.error(f"MongoDB - Error during operation: {error}")
		raise DatabaseError(f"MongoDB operation failed: {str(error)}")
	finally:
		await mongo_session.end_session()

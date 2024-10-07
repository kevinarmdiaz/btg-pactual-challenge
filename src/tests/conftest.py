import subprocess

from typing import AsyncIterator
import pytest_asyncio
from loguru import logger
from pydantic_core._pydantic_core import MultiHostUrl
import pytest
from src.config import settings
from src.infrastructure.mongodb import (FundsCollection, UsersCollection, LogTransactionsFundsCollection,
                                        SubscriptionCollection, transaction_mongo)
from src.main import app

from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

settings.MONGODB_URI = MultiHostUrl.build(
            scheme="mongodb",
            host='localhost',
            port=27018,
        )

__beanie_models__ = [FundsCollection, UsersCollection, LogTransactionsFundsCollection, SubscriptionCollection]


# Ejecutar docker-compose para levantar los servicios
import subprocess
import time
import socket
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from src.main import app
from src.config import settings
from loguru import logger
from src.infrastructure.mongodb import UsersCollection, FundsCollection, SubscriptionCollection

def wait_for_mongodb():
    """Esperar a que MongoDB esté listo antes de continuar."""
    logger.info("Esperando que MongoDB esté listo...")
    while True:
        try:
            # Intenta abrir una conexión al puerto de MongoDB (en este caso, el 27018)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(('localhost', 27018))  # Cambia el puerto si es necesario
            logger.info("MongoDB está listo.")
            break
        except (socket.timeout, ConnectionRefusedError):
            logger.info("MongoDB no está listo, reintentando...")
            time.sleep(5)  # Espera 5 segundos antes de intentar de nuevo

# Función para levantar los contenedores con Docker
def run_docker_compose_up():
    try:
        logger.info("Starting Docker services with docker-compose...")
        subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "up", "--build", "-d"], check=True)
        logger.info("Docker services started successfully.")
        wait_for_mongodb()  # Espera a que MongoDB esté listo
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start Docker services: {e}")
        raise e

# Detener y eliminar los servicios después de las pruebas
def run_docker_compose_down():
    try:
        logger.info("Stopping and removing Docker services with docker-compose...")
        subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "down"], check=True)
        logger.info("Docker services stopped and removed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to stop Docker services: {e}")
        raise e

# Fixture del cliente
@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncIterator[AsyncClient]:
    """Async server client that handles lifespan and teardown."""
    run_docker_compose_up()

    logger.info(f"ENVIRONMENT: {settings.ENVIRONMENT}")

    async with LifespanManager(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as _client:
            try:
                yield _client  # Proporciona el cliente para las pruebas
            except Exception as exc:
                logger.error(f"Error during test execution: {exc}")
            finally:
                # Limpiar la base de datos después de las pruebas
                await clean_database()

    run_docker_compose_down()  # Detener los contenedores después de las pruebas

    
async def clean_database():
    """Limpiar la base de datos antes y después de cada prueba dentro de una transacción."""
    # Iniciar la transacción
    async with transaction_mongo() as session:
        db = session.client[settings.DB_NAME]

        # Limpiar todas las colecciones de la base de datos dentro de la transacción
        collection_names = await db.list_collection_names()
        for collection_name in collection_names:
            collection = db[collection_name]
            await collection.delete_many({})  # Elimina todos los documentos




import pytest
from loguru import logger
from src.infrastructure.mongodb import CTX_SESSION
from src.main import app

"""Tests fixtures."""
from asgi_lifespan import LifespanManager
from httpx import AsyncClient


@pytest.fixture()
async def client_test():
    """
    Create an instance of the client.
    :return: yield HTTP client.
    """
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
            yield ac

def pytest_configure():
    # Disable logs
    alembic_config.set_section_option("logger_alembic", "level", "ERROR")
    logger.disable("src.infrastructure")
    logger.disable("src.presentation")
    logger.disable("src.domain")
    logger.disable("src.application")


# =====================================================================
# Database specific fixtures and mocks
# =====================================================================
@pytest.fixture(autouse=True)
def auto_prune_database():
    """This fixture automatically cleans the database with alembic
    for each test separately.
    """

    alembic_command.upgrade(alembic_config, "head")
    yield
    alembic_command.downgrade(alembic_config, "base")


@pytest.fixture(autouse=True)
async def _auto_close_session():
    """Autoclose each session after each test.
    NOTE: we'd like to be sure that the session is closed in any case.
    """

    yield
    session = CTX_SESSION.get()
    await session.close()


# =====================================================================
# Application specific fixtures
# =====================================================================

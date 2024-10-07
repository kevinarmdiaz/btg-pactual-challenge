from contextvars import ContextVar

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClientSession
from beanie.exceptions import  (
    WrongDocumentUpdateStrategy,
    DocumentNotFound,
    DocumentAlreadyCreated,
    DocumentWasNotSaved,
    CollectionWasNotInitialized,
    MigrationException,
    ReplaceError,
    StateManagementIsTurnedOff,
    StateNotSaved,
    RevisionIdWasChanged,
    NotSupported,
    MongoDBVersionError,
    ViewWasNotInitialized,
    ViewHasNoSettings,
    UnionHasNoRegisteredDocs,
    UnionDocNotInited,
    DocWasNotRegisteredInUnionClass,
    Deprecation,
    ApplyChangesException
)

BEANIE_ODM_EXCEPTIONS = (
    WrongDocumentUpdateStrategy,
    DocumentNotFound,
    DocumentAlreadyCreated,
    DocumentWasNotSaved,
    CollectionWasNotInitialized,
    MigrationException,
    ReplaceError,
    StateManagementIsTurnedOff,
    StateNotSaved,
    RevisionIdWasChanged,
    NotSupported,
    MongoDBVersionError,
    ViewWasNotInitialized,
    ViewHasNoSettings,
    UnionHasNoRegisteredDocs,
    UnionDocNotInited,
    DocWasNotRegisteredInUnionClass,
    Deprecation,
    ApplyChangesException
)
from .engine import create_motor_client

__all__ = ("CTX_SESSION", "Session", "BEANIE_ODM_EXCEPTIONS")

# ContextVar para manejar la sesión de MongoDB
CTX_SESSION: ContextVar[AsyncIOMotorClientSession] = ContextVar("session", default=None)


class Session:
    """Base class to perform MongoDB operations with ClientSession."""

    def __init__(self, db_name: str = "mydatabase") -> None:
        self._client = create_motor_client()
        self._db: AsyncIOMotorDatabase = self._client[db_name]
        self._session: AsyncIOMotorClientSession | None = None

    async def start_session(self):
        """Starts a MongoDB client session and sets it in the context."""
        self._session = await self._client.start_session()
        CTX_SESSION.set(self._session)

    async def end_session(self):
        """Ends the MongoDB client session."""
        if self._session:
            await self._session.end_session()
            self._session = None
            CTX_SESSION.set(None)

from typing import Any, AsyncGenerator, Generic, Type
from pydantic import UUID4
from src.infrastructure.application import (
    DatabaseError,
    NotFoundError,
    UnprocessableError,
)
from .session import BEANIE_ODM_EXCEPTIONS
from ..collections import ConcreteCollection

__all__ = ("BaseRepository",)


class BaseRepository(Generic[ConcreteCollection]):
    """
    Base repository class for working with MongoDB using Beanie ODM.
    Provides common database operations such as get, update, count, and delete.
    """

    schema_class: Type[ConcreteCollection]

    def __init__(self) -> None:
        """
        Initialize the repository. Ensure the schema_class attribute is set.
        Raises:
                UnprocessableError: If schema_class is not provided.
        """
        super().__init__()

        if not self.schema_class:
            raise UnprocessableError(
                message="Cannot initiate the class without schema_class attribute"
            )

    async def _update(
        self, key: str, value: Any, payload: dict[str, Any]
    ) -> ConcreteCollection:
        """
        Updates an existing document in the database based on the key-value pair.
        Args:
                key (str): The key to find the document.
                value (Any): The value associated with the key.
                payload (dict): Data to update the document.

        Raises:
                DatabaseError: If the document cannot be updated.

        Returns:
                ConcreteCollection: The updated document.
        """
        try:
            update_query = {"$set": payload}
            updated_document = await self.schema_class.find_one({key: value}).update(
                update_query
            )

            if not updated_document:
                raise DatabaseError("Cannot update collection")

            return await self.schema_class.get(updated_document.id)

        except BEANIE_ODM_EXCEPTIONS as e:
            raise DatabaseError(detail=str(e), instance="/database/update") from e

    async def _get(
        self, key: str, value: Any, error_message: str = ""
    ) -> ConcreteCollection:
        """
        Retrieves a single document by a key-value pair.
        Args:
                key (str): The key to filter the document.
                value (Any): The value associated with the key.
                error_message (str): Error message to display if not found.

        Returns:
                ConcreteCollection: The retrieved document.
        """
        document = await self.schema_class.find_one({key: value})
        return document

    async def count(self) -> int:
        """
        Counts the total number of documents in the collection.
        Returns:
                int: The number of documents.
        """
        try:
            return await self.schema_class.count_documents({})
        except BEANIE_ODM_EXCEPTIONS as e:
            raise DatabaseError(detail=str(e), instance="/database/count") from e

    async def _first(self, by: str = "_id") -> ConcreteCollection:
        """
        Retrieves the first document in the collection based on a sort order.
        Args:
                by (str): The field to sort by.

        Raises:
                NotFoundError: If no document is found.

        Returns:
                ConcreteCollection: The first document.
        """
        try:
            document = await self.schema_class.find_all().sort(by, 1).first_or_none()
            if not document:
                raise NotFoundError(detail="No document found.")
            return document
        except BEANIE_ODM_EXCEPTIONS as e:
            raise DatabaseError(detail=str(e), instance="/database/first") from e

    async def _last(self, by: str = "id") -> ConcreteCollection:
        """
        Retrieves the last document in the collection based on a sort order.
        Args:
                by (str): The field to sort by.

        Raises:
                NotFoundError: If no document is found.

        Returns:
                ConcreteCollection: The last document.
        """
        try:
            document = await self.schema_class.find_all().sort(by, -1).first_or_none()
            if not document:
                raise NotFoundError(detail="No document found.")
            return document
        except BEANIE_ODM_EXCEPTIONS as e:
            raise DatabaseError(detail=str(e), instance="/database/last") from e

    async def _save(self, payload: dict[str, Any]) -> ConcreteCollection:
        """
        Saves a new document to the collection.
        Args:
                payload (dict): Data to insert into the collection.

        Raises:
                DatabaseError: If the document cannot be saved.

        Returns:
                ConcreteCollection: The newly saved document.
        """
        try:
            schema = self.schema_class(**payload)
            await schema.insert()
            return schema
        except Exception as e:
            raise DatabaseError(detail=str(e), instance="/database/save") from e

    async def _all(self) -> AsyncGenerator[ConcreteCollection, None]:
        """
        Retrieves all documents in the collection as an asynchronous generator.
        Yields:
                ConcreteCollection: Each document in the collection.
        """
        try:
            async for document in self.schema_class.find_all():
                yield document
        except BEANIE_ODM_EXCEPTIONS as e:
            raise DatabaseError(detail=str(e), instance="/database/all") from e

    async def delete(self, id_: UUID4) -> None:
        """
        Deletes a document by its ID.
        Args:
                id_ (UUID4): The ID of the document to delete.

        Raises:
                NotFoundError: If the document is not found.
        """
        try:
            document = await self.schema_class.get(id_)
            if not document:
                raise NotFoundError(detail=f"No document found with id={id_}")
            await document.delete()
        except BEANIE_ODM_EXCEPTIONS as e:
            raise DatabaseError(detail=str(e), instance="/database/delete") from e

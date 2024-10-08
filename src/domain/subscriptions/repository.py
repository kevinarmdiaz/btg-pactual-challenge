from typing import AsyncGenerator

from src.infrastructure.application import DatabaseError
from src.infrastructure.mongodb import (
    BaseRepository,
    SubscriptionCollection,
    FundsCollection,
    UsersCollection,
)
from pydantic import UUID4
from .entities import SubscriptionFlat, SubscriptionUncommited

__all__ = ("SubscriptionsRepository",)

from .subscription_status import SubscriptionStatus
from ...config import settings
from ...infrastructure.application.errors.entities import (
    SubscriptionConflictError,
    NotSubscribedError,
)
from ...infrastructure.logging.entities import LogUncommited
from ...infrastructure.logging.repository import LogTransactionRepository
from ...infrastructure.mongodb.services.session import BEANIE_ODM_EXCEPTIONS
from ...infrastructure.notificator.services.NotificacionService import NotificationService
from ...infrastructure.notificator.services.SESService import SESNotificationService
from ...infrastructure.notificator.services.SNSService import SNSNotificationService


class SubscriptionsRepository(BaseRepository[SubscriptionCollection]):
    schema_class = SubscriptionCollection

    async def all(self) -> AsyncGenerator[SubscriptionFlat, None]:
        """ """
        async for instance in self._all():
            yield SubscriptionFlat.model_validate(instance)

    async def get(self, id_: int) -> SubscriptionCollection:
        """

        :param id_:
        :return:
        """
        instance = await self._get(key="id", value=id_)
        return instance

    async def create(self, schema: SubscriptionUncommited) -> SubscriptionFlat:
        """

        :param schema:
        :return:
        """
        instance: SubscriptionCollection = await self._save(schema.model_dump())
        return SubscriptionFlat.model_validate(instance)

    async def get_subscription(
        self, user_id: UUID4, fund_id: UUID4
    ) -> SubscriptionCollection:
        """
        Verifica si el usuario ya está suscrito a un fondo de forma eficiente.

        :param user_id: El ID del usuario.
        :param fund_id: El ID del fondo.
        :return: True si el fondo está en la lista de suscripciones del usuario, False de lo contrario.
        """
        subscription = await self.schema_class.find_one(
            self.schema_class.user.id == user_id, self.schema_class.fund.id == fund_id
        )

        return subscription

    async def subscribe_in_fund(self, user: UsersCollection, fund: FundsCollection):
        """
        Función para suscribir un usuario a un fondo.

        :param user: El usuario que se suscribe
        :param fund: El fondo al que el usuario desea suscribirse
        """

        try:
            if await SubscriptionsRepository().get_subscription(
                user_id=user.id, fund_id=fund.id
            ):
                raise SubscriptionConflictError(
                    message=f"""El usuario ya está suscrito al fondo: "{fund.name}".""",
                    instance="/subscription/subscribe-fund",
                )

            await user.check_balance(fund_instance=fund)

            # Crear la suscripción
            await user.reduce_balance(
                minimum_investment_amount=fund.minimum_investment_amount
            )

            suscription_unc = SubscriptionCollection(user=user, fund=fund)
            await suscription_unc.insert()

            log_transaction = LogUncommited(
                user_id=user.id,
                fund_id=fund.id,
                transaction_type=SubscriptionStatus.APERTURA,
                message=f"El usuario {user.name} se ha suscrito a {fund.name} exitosamente",
                balance=user.balance,
            )
            
            #FIXME: Poner como inyeccion de dependencia no depender de clases concretas
            if not settings.ENVIRONMENT == 'TESTING':
                sns_sender = SNSNotificationService()
                sms_service = NotificationService(sns_sender)
                sms_service.notify([user.phone], "Suscripción correcta", f"Usted se ha suscrito a {fund.name} exitosamente")
                
                ses_sender = SESNotificationService()
                email_service = NotificationService(ses_sender)
                email_service.notify([user.email], "Suscripción correcta", f"Usted se ha suscrito a {fund.name} exitosamente")

            await LogTransactionRepository().create(schema=log_transaction)
            await user.save_changes()

            return True

        except BEANIE_ODM_EXCEPTIONS as err:
            # Lanza la excepción original pero con un mejor rastreo del error
            raise DatabaseError(instance="/database/operation") from err

    async def cancel_in_fund(self, user: UsersCollection, fund: FundsCollection):
        try:
            db_subscription = await SubscriptionsRepository().get_subscription(
                user_id=user.id, fund_id=fund.id
            )

            if not db_subscription:
                raise NotSubscribedError(
                    user_id=user.id,
                    fund_name=fund.name,
                    instance="/subscription/cancel-fund",
                )

            await user.add_balance(
                minimum_investment_amount=fund.minimum_investment_amount
            )

            await user.save_changes()

            await self.delete(id_=db_subscription.id)
            print(
                f"El fondo {fund.id} fue eliminado de las suscripciones del usuario {user.id}."
            )

            log_transaction = LogUncommited(
                user_id=user.id,
                fund_id=fund.id,
                transaction_type=SubscriptionStatus.CANCELACION,
                message=f"El usuario {user.name} se ha retirado del fondo: {fund.name} exitosamente",
                balance=user.balance,
            )
            await LogTransactionRepository().create(schema=log_transaction)

            return True

        except BEANIE_ODM_EXCEPTIONS as err:
            raise DatabaseError(
                message="Error de conexión con la base de datos.",
                instance="/database/operation",
            ) from err

from abc import ABC, abstractmethod


class NotificationSender(ABC):
    """Clase asbtracta para las notificaciones"""
    @abstractmethod
    def send_notification(self, recipient: str, subject: str, message: str):
        """

        :param recipient:
        :param subject:
        :param message:
        """
        pass

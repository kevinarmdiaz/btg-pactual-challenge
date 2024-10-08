from typing import List

from src.infrastructure.notificator.services.abstract import NotificationSender


class NotificationService:
    """

    """
    def __init__(self, sender: NotificationSender):
        self.sender = sender

    def notify(self, recipients: List[str], subject: str, message: str):
        """
        Envía una notificación a una lista de destinatarios.
        """
        for recipient in recipients:
            self.sender.send_notification(recipient, subject, message)
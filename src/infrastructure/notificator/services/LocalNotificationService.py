from boto3 import client
from loguru import logger
from src.infrastructure.notificator.services.abstract import NotificationSender


class LocalNotificationService(NotificationSender):
    def __init__(self, region_name: str = "us-east-1"):
        self.logger = logger

    def send_notification(self, recipient: str, subject: str, message: str):
        """
        Enviar un correo electrónico.
        """
        try:
            self.logger.info(f"Correo enviado a {recipient}.")
        except Exception as e:
            print(f"Error al enviar el correo electrónico: {str(e)}")

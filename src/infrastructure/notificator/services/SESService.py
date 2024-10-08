from boto3 import client

from src.infrastructure.notificator.services.abstract import NotificationSender


class SESNotificationService(NotificationSender):
    def __init__(self, region_name: str = "us-east-1"):
        self.ses_client = client('ses', region_name=region_name)

    def send_notification(self, recipient: str, subject: str, message: str):
        """
        Enviar un correo electrónico usando SES.
        """
        try:
            response = self.ses_client.send_email(
                Source="noreply@example.com",  # Dirección del remitente verificada en SES
                Destination={'ToAddresses': [recipient]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': message}}
                }
            )
            print(f"Correo enviado a {recipient}. MessageId: {response['MessageId']}")
        except Exception as e:
            print(f"Error al enviar el correo electrónico: {str(e)}")

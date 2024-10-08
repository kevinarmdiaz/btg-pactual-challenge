from src.infrastructure.notificator.services.abstract import NotificationService
from boto3 import client


class SNSNotificationService(NotificationService):
    def __init__(self, region_name="us-east-1"):
        self.sns_client = client("sns", region_name=region_name)
    
    def send_notification(self, recipient: str, subject: str, message: str):
        try:
            response = self.sns_client.publish(
                PhoneNumber=recipient,  # Enviar SMS
                Message=message
            )
            print(f"SMS enviado a {recipient}. MessageId: {response['MessageId']}")
        except Exception as e:
            print(f"Error al enviar el SMS: {str(e)}")

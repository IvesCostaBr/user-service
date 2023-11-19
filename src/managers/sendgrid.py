from src.managers.abstract_manager import AbstractManager
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGridManager(AbstractManager):
    """SendGric mananger class."""

    def __init__(self, credentials: dict) -> None:
        """init sendgrid manager class."""
        self.sendgrid_key = credentials.get("key")
        self.default_email = credentials.get("default_email")
        self.client = None

        self.__create_cliente()

    def __create_cliente(self):
        """Create client."""
        self.client = SendGridAPIClient(self.sendgrid_key)

    def send(self, data: dict) -> bool:
        try:
            template_id = data.get("template_id")
            # verificar se o template existe no nosso banco.
            # montar o payload de envio para o sendgrid
            # gravar o status da request.
            data = self.__create_email_data(data)
            resp = self.client.send(data)
            return True
        except:
            return False

    def __create_email_data(self, data: dict) -> Mail:
        """Create payalod to send email"""
        return Mail(
            from_email=self.default_email,
            to_emails=data.get("email"),
            subject=data.get("subject"),
            html_content="<strong>and easy to do anywhere, even with Python</strong>",
        )

    def heath_check(self) -> bool:
        return True

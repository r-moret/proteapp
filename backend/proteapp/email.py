from jinja2 import Environment, FileSystemLoader
from resend import Emails
import resend
import os

resend.api_key = os.environ["RESEND_API_KEY"]


class EmailSender:
    def __init__(self, template: str, sender: str) -> None:
        env = Environment(loader=FileSystemLoader(searchpath="proteapp/templates"))

        self.template = env.get_template(template)
        self.sender = sender

    def send(self, to: str, subject: str, template_kwargs: dict[str, str]):
        email_content = self.template.render(**template_kwargs)

        params: Emails.SendParams = {
            "from": self.sender,
            "to": to,
            "subject": subject,
            "html": email_content,
        }

        Emails.send(params)

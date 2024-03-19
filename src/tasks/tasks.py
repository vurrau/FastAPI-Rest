import smtplib
from email.message import EmailMessage

from src.api.user.logic import get_email_employee
from src.core.config import SMTP_PASS, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def send_email(email: EmailMessage):
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)


async def send_create_request(background_tasks, session):
    email_message_base = EmailMessage()
    email_message_base['Subject'] = 'New request'
    email_message_base['From'] = SMTP_USER
    email_message_base.set_content('A new request has been created.', subtype='plain')

    staff_and_managers = await get_email_employee(session)

    for user_email in staff_and_managers:
        email_message = EmailMessage()
        email_message['Subject'] = email_message_base['Subject']
        email_message['From'] = email_message_base['From']
        email_message['To'] = user_email
        email_message.set_content(email_message_base.get_content(), subtype='plain')

        background_tasks.add_task(send_email, email_message)

    return {"message": "Request created and notifications sent to staff and managers."}


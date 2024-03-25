from email.message import EmailMessage

import aiosmtplib

from src.api.user.logic import UserService
from src.core.config import SMTP_PASS, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


async def send_email_async(email: EmailMessage):
    smtp = aiosmtplib.SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True)

    await smtp.connect()
    await smtp.login(SMTP_USER, SMTP_PASS)
    await smtp.send_message(email)
    await smtp.quit()


async def send_create_request(background_tasks, data):
    title = data.title
    description = data.description

    email_message_base = EmailMessage()
    email_message_base['Subject'] = 'New request'
    email_message_base['From'] = SMTP_USER
    email_message_base.set_content(
        f'A new request has been created.\n\nTitle: {title}\nDescription: {description}', subtype='plain')

    staff_and_managers = await UserService.get_email_employee()

    for user_email in staff_and_managers:
        email_message = EmailMessage()
        email_message['Subject'] = email_message_base['Subject']
        email_message['From'] = email_message_base['From']
        email_message['To'] = user_email
        email_message.set_content(email_message_base.get_content(), subtype='plain')

        background_tasks.add_task(send_email_async, email_message)

    return {"message": "Request created and notifications sent to employee and managers."}


import smtplib
import ssl
from email.message import EmailMessage
from celery import Celery
from settings import settings
from notes.models import Notes
from notes.views import app
from core import db

celery = Celery(__name__,
                broker=settings.celery_broker,
                backend=settings.celery_result,
                broker_connection_retry_on_startup=True)


@celery.task()
def send_mail(payload):
    msg = EmailMessage()
    msg['From'] = settings.email_host_user
    msg['To'] = payload.get('recipient')
    msg['Subject'] = 'Flask Microservices'
    msg.set_content(payload.get('message'))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.smtp, settings.smtp_port, context=context) as smtp:
        smtp.login(user=settings.email_host_user, password=settings.email_host_password)
        smtp.sendmail(settings.email_host_user, payload.get('recipient'), msg.as_string())
        smtp.quit()
    return f"Mail sent to {payload.get('recipient')}"


@celery.task()
def user_on_delete(user_id: int):
    app.app_context().push()
    Notes.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return f'Notes related to user {user_id} has been deleted.'

from app.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task
def send_result(email, task_title):
    message = f"task was completed. task title: {task_title}"
    send_mail("Task completed", message, settings.EMAIL_HOST_USER, [email])

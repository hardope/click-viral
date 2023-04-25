import os
from email.message import EmailMessage
import ssl
import smtplib


def send_mail(to, subject, body):

    sender = "clickviralng@gmail.com"
    recipient = to
    password = "hjlcnodeitfseaci"

    mail = EmailMessage()
    mail['From'] = sender
    mail['To'] = recipient
    mail['Subject'] = subject

    mail.set_content(body)

    context =  ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, mail.as_string())

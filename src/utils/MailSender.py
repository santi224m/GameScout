import requests
import os

class MailSender:
  def __init__(self):
    pass
  def send_mail(recipient, subject, message):
    key = os.getenv("MAILGUN_API_KEY");
    if key is None: raise ValueError('MAILGUN_API_KEY is not set properly in your .env file')
    return requests.post(
      "https://api.mailgun.net/v3/sandbox6b87086f1f834312911823811e062375.mailgun.org/messages",
      auth=("api", key),
      data={"from": "GameScout <mailgun@sandbox6b87086f1f834312911823811e062375.mailgun.org>",
        "to": [recipient],
        "subject": subject,
        "text": message})
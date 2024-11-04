from mailersend import emails
import os
from src.utils.JWTGenerator import JWTGen

class MailSender:
  def __init__(self):
    self.mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))
  def send_mail(self, recipient, username, template, jwt):
    mail_from = {"name": "GameScout", "email":"gs@trial-jpzkmgqrzkn4059v.mlsender.net"}
    recipients = [{"email": recipient}]
    personalization = [
      {
        "email": recipient,
        "data": {
          "link": "127.0.0.1:5000/verify/" + jwt
        }
      }
    ]
    mail_body={}

    subject = f"Hi {username}, please verify your GameScout account"

    self.mailer.set_mail_from(mail_from, mail_body)
    self.mailer.set_mail_to(recipients, mail_body)
    self.mailer.set_subject(subject, mail_body)
    self.mailer.set_template(template, mail_body)
    self.mailer.set_personalization(personalization, mail_body)

    self.mailer.send(mail_body)
  def send_verification_email(self, uuid, email, username):
    template = "3zxk54vww2xljy6v"

    jwt = JWTGen.encode_jwt(email, uuid)

    self.send_mail(email, username, template, jwt)
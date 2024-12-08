from mailersend import emails
import os
from src.utils.JWTGenerator import JWTGen

class MailSender:
  def __init__(self):
    self.mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))
  def send_mail(self, recipient, template, link, subject):
    mail_from = {"name": "GameScout", "email":"gs@trial-jpzkmgqrzkn4059v.mlsender.net"}
    recipients = [{"email": recipient}]
    personalization = [
      {
        "email": recipient,
        "data": {
          "link": link
        }
      }
    ]
    mail_body={}

    self.mailer.set_mail_from(mail_from, mail_body)
    self.mailer.set_mail_to(recipients, mail_body)
    self.mailer.set_subject(subject, mail_body)
    self.mailer.set_template(template, mail_body)
    self.mailer.set_personalization(personalization, mail_body)

    self.mailer.send(mail_body)
  def send_verification_email(self, uuid, email, username):
    template = "3zxk54vww2xljy6v"

    jwt = JWTGen.encode_jwt(email, uuid)
    link = "http://localhost:5000/verify/" + jwt

    self.send_mail(email, template, link, f"Hi {username}, please verify your GameScout account")

  def send_reset_email(self, uuid, email): 
    template = "jy7zpl9qpq545vx6"

    jwt = JWTGen.encode_jwt(email, uuid, 'password')
    link = "http://localhost:5000/account/recovery/" + jwt

    self.send_mail(email, template, link, f"Password Reset Requested")
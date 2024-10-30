from mailersend import emails
import os

class MailSender:
  def __init__(self):
    self.mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))
  def send_mail(self, recipient, subject, template):
    mail_from = {"name": "GameScout", "email":"gs@trial-jpzkmgqrzkn4059v.mlsender.net"}
    recipients = [{"email": recipient}]
    personalization = [
      {
        "email": recipient,
        "data": {
          "link": "127.0.0.1:5000/verify"
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

email = ""
username = ""
subject = "Hi " + username + ", please verify your GameScout account"
MailSender().send_mail(email, subject, "3zxk54vww2xljy6v")
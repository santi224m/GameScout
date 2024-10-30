from mailersend import emails
import os

class MailSender:
  def __init__(self):
    self.mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))
  def send_mail(self, recipient, subject, message, message_html):
    mail_from = {"name": "GameScout", "email":"gs@trial-jpzkmgqrzkn4059v.mlsender.net"}
    recipients = [{"email": recipient}]
    mail_body={}

    self.mailer.set_mail_from(mail_from, mail_body)
    self.mailer.set_mail_to(recipients, mail_body)
    self.mailer.set_subject(subject, mail_body)
    self.mailer.set_html_content(message_html, mail_body)
    self.mailer.set_plaintext_content(message, mail_body)

    self.mailer.send(mail_body)

email = ""
MailSender().send_mail(email, "GameScout Mail Test", "hello!", "<h1>Hello!</h1>")
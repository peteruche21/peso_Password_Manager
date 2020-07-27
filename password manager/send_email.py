import smtplib, ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailing(object):

    SMTP_CONFIG = {
        'server': 'smtp.aol.com',
        'username': 'pmanager25@aol.com',
        'password': 'nbfkgtcfdytlsief',
        'port': 465
    }
    CONTEXT = ssl.create_default_context()

    def __init__(self):
        smtp_config = self.SMTP_CONFIG
        context = self.CONTEXT

        self.connection = smtplib.SMTP_SSL(smtp_config['server'],
                                           smtp_config['port'],
                                           context=context)
        self.connection.login(smtp_config['username'], smtp_config['password'])

    def send(self, reciever, message, name):
        sender = self.SMTP_CONFIG['username']
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['T0'] = reciever
        msg['Subject'] = 'reset'

        body = f"<h1>please {name} use this {message} for your master. duration is 15 minutes </h1>"
        msg.attach(MIMEText(body, 'html'))
        self.connection.sendmail(sender, reciever, msg.as_string())
        print(
            'email sent, \nplease check your mail \nalso note: it may be in your spam folder'
        )

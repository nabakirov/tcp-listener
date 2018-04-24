import smtplib
from email.mime.text import MIMEText
from .configs import emails, sender


def mail_send(msg, emails=emails, sender=sender):
    smtpObj = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    # smtpObj.starttls()
    smtpObj.login(sender['email'], sender['password'])
    smtpObj.sendmail(sender['email'], emails, msg)
    smtpObj.quit()


def send_email(to_address: iter, subject: str, message: str,
               username=sender['email'], password=sender['password'],
               from_address=None, smtp='smtp.yandex.ru'):

    if from_address is None:
        from_address = username


    server = smtplib.SMTP_SSL(smtp)
    o = server.ehlo()
    # print(o)
    # o = server.starttls()
    # print(o)
    server.login(username, password)
    # print(o)
    if not isinstance(to_address, (list, tuple, set)):
        msg = MIMEText(message)
        msg['From'] = from_address
        msg['TO'] = to_address
        msg['Subject'] = subject
        o = server.send_message(msg)
    else:
        for email in to_address:
            msg = MIMEText(message)
            msg['From'] = from_address
            msg['TO'] = email
            msg['Subject'] = subject
            o = server.send_message(msg)
    # print(o)
    o = server.quit()
    # print(o)


import smtplib

from .configs import emails, sender


def mail_send(msg, emails=emails, sender=sender):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(sender['email'], sender['password'])
    smtpObj.sendmail(sender['email'], emails, msg)
    smtpObj.quit()



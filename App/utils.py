# from App import db 
import random
from email.message import EmailMessage
import smtplib
import ssl
import os


def row2dict(row, column_list=None):
    d = {}
    if column_list == None:
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
    else:
        for column in column_list:
            d[column] = str(getattr(row, column))

    return d

def unitaire(n):
    n+=1
    return n 


# def add_user(new_user):

#     db.session.add(new_user)
#     db.session.commit()   



def generate_code():
    code = int(str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)) +str(random.randint(0,9)))
    return code

def send_mail(subject, body, user_mail):
    em = EmailMessage()
    pwd =os.environ.get('MAIL_MDP')
    email_sender = os.environ.get('MAIL_SENDER')
    em['From'] = email_sender
    em['To'] = user_mail
    em['Subject'] =  subject
    em.set_content(body)



    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, pwd)
        smtp.sendmail(email_sender,user_mail,em.as_string())
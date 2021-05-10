import smtplib
#import sendgrid
import os
#from sendgrid.helpers.mail import Mail, Email, To, Content
SUBJECT = "ALERT FROM MONEYDEED$"
s = smtplib.SMTP('smtp.gmail.com', 587)

def sendmail(TEXT,email):
#    print("sorry we cant process your candidature")
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("saha181930@gmail.com", "sep@181930")
    message  = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    s.sendmail("saha181930@gmail.com", email, message)
    s.quit()
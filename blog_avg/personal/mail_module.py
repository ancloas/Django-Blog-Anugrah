import smtplib
from dotenv import load_dotenv
import os
import datetime as dt
from email.mime.text import MIMEText
from smtplib import SMTPException

load_dotenv()
Gmail_APP_Password=os.getenv('Gmail_APP_Password')
my_email=os.getenv('my_email')
recipient_email=os.getenv('recipient_email')

def send_mail(subject, msg_content, reply_to= None, from_name=None, server_sender=my_email, password=Gmail_APP_Password, receiver=recipient_email):
    msg = MIMEText(msg_content, 'html')
    msg['Subject'] = subject
    msg['From'] = server_sender
    msg['To'] = receiver
    if reply_to:
        msg.add_header('reply-to', reply_to)
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            # Start TLS
            connection.starttls()
            connection.login(user=server_sender, password=password)
            connection.sendmail(from_addr=server_sender, 
                                to_addrs=receiver, 
                                msg=msg.as_string()
                                )
        print('worked and senth as well?')
        return True  # Return True if email is sent successfully
    except SMTPException as e:
        print(f"Error sending email: {e}")
        return False  # Return False if there's an error sending the email

        

# send_mail('Test mail', msg_content='Yo! bro. You are doing some great stuff that will help all of us.',from_name= 'Anugrah Gupta', reply_to='anugrahvardhan@gmail.com')

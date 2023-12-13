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

def send_mail(subject, msg_content, from_name, reply_to, server_sender=my_email, password=Gmail_APP_Password, receiver=recipient_email):
    body = f"""  
        <div style="max-width: 600px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <p>Hello Bubble Of Thoughts,</p>
            <p>You got a new message from {from_name}:</p>
            <div style="border-left: 4px solid #007bff; padding: 12px; font-style: italic; margin-top: 20px;">
                <p style="margin: 0; padding: 0;">
                    {msg_content}
                </p>
            </div>
            <p style="margin-top: 20px; font-style: italic; color: #555;">Best wishes,<br>{from_name}</p>
        </div>
    """

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = reply_to
    msg['To'] = receiver
    msg.add_header('reply-to', reply_to)
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            # Start TLS
            connection.starttls()
            connection.login(user=server_sender, password=password)
            connection.sendmail(from_addr=reply_to, 
                                to_addrs=receiver, 
                                msg=msg.as_string()
                                )
        return True  # Return True if email is sent successfully
    except SMTPException as e:
        print(f"Error sending email: {e}")
        return False  # Return False if there's an error sending the email

        

# send_mail('Test mail', msg_content='Yo! bro. You are doing some great stuff that will help all of us.',from_name= 'Anugrah Gupta', reply_to='anugrahvardhan@gmail.com')

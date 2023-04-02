#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os
import amqp_setup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

monitorBindingKey='notify'

def receiveError():
    amqp_setup.check_setup()
    
    queue_name = "Notify"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    # body = {"customerEmail": customerEmail, "subject": subject, "content": content}
    customerEmail = json.loads(body)['customerEmail']
    subject = json.loads(body)['subject']
    content = json.loads(body)['content']

    # send email to customer
    # Set up the SMTP server details
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = 'esdg1t5@outlook.com' # esdg1t5@outlook.com
    smtp_password = '3sdg1T5@@@' # 3sdg1T5@@@

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = 'esdg1t5@outlook.com'
    msg['To'] = customerEmail
    msg['Subject'] = subject

    # Add the message body
    body = content
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, customerEmail, msg.as_string())


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveError()

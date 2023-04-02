from flask_mail import Mail, Message
import random

from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http
import os, sys
import requests, json
import amqp_setup, pika

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'lokezhankang@gmail.com' # sender Gmail address
app.config['MAIL_PASSWORD'] = 'pkewefqbhwwibywy' # sender Gmail app password
mail = Mail(app)

notification_manager_URL = os.environ.get('notification_manager_URL') or "http://localhost:5005/notification"

@app.route('/send_otp')
def send_otp():
    otp = "".join(str(random.randint(1, 9)) for _ in range(6))
    # replace the receipients list below with the recipient's email address
    msg = Message('Your One Time Password', sender = 'lokezhankang@gmail.com', recipients = ['lokezhankang@gmail.com'])
    msg.body = f'Your OTP is {otp}.'
    mail.send(msg)

    ### HOW TO INTEGRATE PROCESS_OTP WITH MAIL HERE??? ###

    return f'An OTP has been sent to your email. Your OTP is {otp}.'


def process_OTP(mail):
    print('\n-----Invoking Notification Manager microservice-----')
    order_result = invoke_http(notification_manager_URL, method='POST', json=mail)
    print('order_result:', order_result)
  
    code = order_result["code"]
    message = json.dumps(order_result)
    amqp_setup.check_setup()

    if code not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notify", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), order_result)
    
    else:           
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notify", 
            body=message)
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), order_result)

if __name__ == '__main__':
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5300, debug = True)





# from os import environ
# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from flask_mail import Mail, Message

# # from notification_manager import NotificationManager

# # Notification Manager ()

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL') or "mysql+mysqlconnector://root@localhost:3306/notification_manager"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'lokezhankang@gmail.com' # replace with your email address
# app.config['MAIL_PASSWORD'] = 'pkewefqbhwwibywy' # replace with your email password
# mail = Mail(app)

# # db = SQLAlchemy(app)
# CORS(app)

# #Send email through rabbitmq(ampq) server
# import pika
# import json

# # RabbitMQ server settings
# RABBITMQ_HOST = "localhost"
# RABBITMQ_PORT = 5672
# RABBITMQ_USER = "guest"
# RABBITMQ_PASSWORD = "guest"
# RABBITMQ_QUEUE = "email_queue"

# # function to send email
# #email and email_content(OTP) are inputs provided by the CRS
# def send_email(email, email_content):
#     # connect to RabbitMQ server
#     connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=pika.PlainCredentials(
#             RABBITMQ_USER, RABBITMQ_PASSWORD)))
    
#     channel = connection.channel()

#     channel.queue_declare(queue=RABBITMQ_QUEUE)

#     # create the email message
#     email_message = {
#         "to": email,
#         "subject": "Notification Email",
#         "content": email_content
#     }

#     # convert the email message to JSON
#     email_message_json = json.dumps(email_message)

#     # publish the email message to the queue
#     channel.basic_publish(exchange="", routing_key=RABBITMQ_QUEUE, body=email_message_json)

#     # close the connection
#     connection.close()

# # route to send email
# @app.route("/send_email", methods=['POST', 'GET'])
# def send_email_route():
#     email = request.form.get("email_address")
#     email_content = request.form.get("email_content")
#     send_email(email, email_content)
#     return jsonify({"message": "Email sent successfully"})

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5005, debug=True)

from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta

from sqlalchemy import JSON
from invokes import invoke_http
import random
import os, sys
import requests, json
import amqp_setup
import pika
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='./static', static_folder='./static')
app.secret_key = 'esdg1t5' # for session
CORS(app)

product_manager_URL = os.environ.get('product_manager_URL') or "http://localhost:5001/product"
inventory_manager_URL = os.environ.get('inventory_manager_URL') or "http://localhost:5002/inventory"
reservation_manager_URL = os.environ.get('reservation_manager_URL') or "http://localhost:5003/reservation_manager"
customer_manager_URL = os.environ.get('customer_manager_URL') or "http://localhost:5004/customer_manager"
# notification_manager_URL = os.environ.get('notification_manager_URL') or "http://localhost:5005/notification"
refund_URL = os.environ.get('refund_URL') or "http://localhost:5005/refund"
payment_URL = os.environ.get('payment_URL') or "http://localhost:5006/payment"

# Database Tables:
# Customer Manager (CustID, Name, Gender, Email)
# Product Manager (productID, productName, images, productRate)
# Inventory Manager (date, productName, quantity)
# Reservation Manager (reservationID, custID, StartDate, EndDate, productID, Quantity)

# Index html render template 
@app.route("/")
def index():
    return render_template('CheckInn_Index.html')
# Newly Added - Changed
# Reservation_Browse.html
@app.route("/Reservation_Browse.html")
def reservation_browse():
    return render_template('Reservation_Browse.html')
# Newly Added - Changed
# Booking Cart html render template
@app.route("/Booking_Cart.html")
def booking_cart():
    return render_template('Booking_Cart.html')
# Newly Added - Changed
# thanks.html render template
@app.route("/thanks.html")
def thanks():
    return render_template('thanks.html')
#Newly Added - Changed
# Reservation_details render template
@app.route("/Reservation_Details.html")
def reservation_details():
    return render_template('Reservation_Details.html')
# Newly Added - Changed
@app.route("/verify_otp.html")
def verification_otp():
    return render_template('verify_otp.html')

# ================ Use Case 1: Customer Browse Available Rooms ================
# Get available rooms based on dates [fromDate, toDate].
@app.route("/crs/get_rooms")
def list_rooms():
    # Initialise list of productName and dateList within the dates specified for room reservation.
    fromDate = request.args.get('check_in_date')
    toDate = request.args.get('check_out_date')
    print(fromDate)
    print(toDate)
    returnDict = {}
    productNameList = ["Single Room", "Double Room", "Suite"]
    dateList = [] # ["2023-03-11", "2023-03-12", ...]
    
    # populate dateList.
    currDate = datetime.strptime(fromDate, '%Y-%m-%d').date()
    toDate = datetime.strptime(toDate, '%Y-%m-%d').date()
    while currDate <= toDate:
        dateList.append(str(currDate))
        currDate += timedelta(days=1)

    for date in dateList:
        productsDict = {} # {productName: {quantity: 0, productRate: 0}, ...}
        for productName in productNameList:
            productDetail = {} # {quantity: 0, productRate: 0
            productName = productName.replace(" ", "%20")
            
            # Get data from Inventory Manager based on (date and productName).
            inventory = invoke_http(inventory_manager_URL +  "/" + date + "/" + productName, method="GET")

            # link productName and ProductRate.
            if "data" in inventory:
                # Get data from Product Manager based on (productName).
                product = invoke_http(product_manager_URL +  "/" + productName, method="GET")
                productName = inventory["data"]["inventory"][0]["productName"].replace("%20", " ")
                quantity = inventory["data"]["inventory"][0]["quantity"]
                productRate = product["data"]["productRate"]

                # Append to productList.
                productDetail = {
                        "quantity": quantity,
                        "productRate": productRate
                    }
                productsDict[productName] = productDetail
        # Append to returnList if date has results.
        if productsDict != {}:
            returnDict[date] = productsDict

    if returnDict == {}:
        return jsonify({
            "code": 404,
            "message": "No available rooms."
        }), 404
    else:
        # Parse JSON data
        data = json.loads(json.dumps(returnDict))

        # Create HTML div
        div = ''
        for date, rooms in data.items(): # date = "2023-03-11", rooms = {"Double Room": {"productRate": 200.0, "quantity": 150}, ...}
            div += '<div>'
            div += f'<h4 class="p-date">{date}</h4>'
            for room_type, room_data in rooms.items(): # room_type = "Double Room", room_data = {"productRate": 200.0, "quantity": 150}
                div += '<div class="product text-center col-lg-4 col-md-4 col-12">'
                if room_type == "Single Room":
                    div += f'<img src="{url_for("static", filename="/images/r1.jpg")}" alt="" class="img-fluid mb-3">'
                elif room_type == "Double Room":
                    div += f'<img src="{url_for("static", filename="/images/r2.jpg")}" alt="" class="img-fluid mb-3">'
                elif room_type == "Suite":
                    div += f'<img src="{url_for("static", filename="/images/r3.jpg")}" alt="" class="img-fluid mb-3">'
                div += f'<h5 class="p-name">{room_type}</h5>'
                div += f'<h4 class="p-price">{room_data["productRate"]}</h4>'
                div += '<button class="buy-btn"><a href="/Booking_Cart.html">Add to Cart</a></button>'
                div += '</div>'
            div += '</div>'


        # Read HTML file
        with open('./html/Rooms_Query.html', 'r') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')
        output_div = soup.find('div', id='hotel-data')
        output_div.clear()
        output_div.append(BeautifulSoup(div, 'html.parser'))

        with open('./html/Rooms_Query.html', 'w') as f:
            f.write(str(soup))

        return redirect('/Rooms_Query.html')

@app.route('/Rooms_Query.html')
def show_rooms():
    return render_template('Rooms_Query.html')
# ================ END Use Case 1: Customer Browse Available Rooms ================


# ================ Use Case 2: Customer Cancel Reservation ================
@app.route("/send_otp", methods=["POST"])
def send_otp():
    reservationID = request.form['reservationID']
    # Get custID from Reservation Manager based on given reservationID.
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="GET")
    custID = reservation['data']['custID']
    # Get customer name and email from Customer Manager based on custID.
    customer = invoke_http(customer_manager_URL +  "/" + str(custID), method="GET")
    customerName = customer['data']['name']
    customerEmail = customer['data']['email']
    # Generate random 6 digit OTP.
    otp = str(random.randint(100000, 999999))
    # Store the OTP and reservationID in a session variable to be used later by the verify_otp function.
    session['otp'] = otp
    session['reservationID'] = reservationID
    subject = "Your OTP for cancelling reservation"
    content = "Dear " + customerName + ",\n\nYour OTP is " + str(otp) + ".\n\nThank you."

    # Send OTP to customer email. (notification microservice)
    message = json.dumps({"customerEmail": customerEmail, "subject": subject, "content": content})
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))
    
    # redirect webapge to enter otp
    return render_template('verify_otp.html')
    # return redirect('http://localhost/ESDG1T5/Booking_Hotel/microservices/flask_stripe/flask_stripe/templates/verify_otp.html')

@app.route('/crs/verify_otp', methods=['POST'])
def verify_otp():
    first = request.form['first']
    second = request.form['second']
    third = request.form['third']
    fourth = request.form['fourth']
    fifth = request.form['fifth']
    sixth = request.form['sixth']
    user_otp = str(first) + str(second) + str(third) + str(fourth) + str(fifth) + str(sixth)

    # Get the OTP and reservationID from the session variable
    otp = session['otp']
    reservationID = session['reservationID']
    # Verify the OTP entered by the user
    if user_otp == str(otp):
        # redirect to cancel_reservation function
        return render_template('Cancel_Reservation.html')
        # return redirect('http://localhost/ESDG1T5/Booking_Hotel/microservices/flask_stripe/flask_stripe/templates/Cancel_Reservation.html')
    else:
        return "OTP verification failed."
    
@app.route('/crs/cancel_reservation', methods=['POST'])
def cancel_reservation():
    reservationID = session['reservationID']
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="GET")
    payment_intent_id = reservation['data']['session_id']
    refund = invoke_http(refund_URL +  "/" + str(payment_intent_id), method="POST")
    print(payment_intent_id)
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="DELETE")
    print(reservation)
    ## process refund.
    # get session_id from reservation manager
    # return render_template('CheckInn_Index.html')
    return redirect('http://localhost:5000/')

# ================ END Use Case 2: Customer Cancel Reservation ================

# ================ Use Case 3: Customer Make Payment for Room Reservation ================
@app.route("/crs/payment/<int:reservationID>", methods=["POST"])
def make_payment(reservationID):
    # Get custID, productID and quantity from Reservation Manager based on given reservationID.
    reservation = invoke_http(reservation_manager_URL +  "/" + str(reservationID), method="GET")
    custID = reservation['data']['custID']
    productID = reservation['data']['productID']
    quantity = reservation['data']['quantity']
    # Get customer name and email from Customer Manager based on custID.
    customer = invoke_http(customer_manager_URL +  "/" + str(custID), method="GET")
    customerName = customer['data']['name']
    customerEmail = customer['data']['email']

    # Get productRate from Product Manager based on productID.
    product = invoke_http(product_manager_URL +  "/id/" + str(productID), method="GET")
    productRate = product['data']['productRate']
    # Calculate total amount.
    totalAmount = productRate * quantity
    # Call payment microservice to make payment.


    # If payment is successful, send email to customer.
    subject = "Your payment for reservation"
    content = "Dear " + customerName + ",\n\nYour payment of $" + str(totalAmount) + " is successful.\n\nThank you."
    message = json.dumps({"customerEmail": customerEmail, "subject": subject, "content": content})
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2))

    # return output
    return jsonify({
        "data": totalAmount
        }), 200

# ================ END Use Case 3: Customer Make Payment for Room Reservation ================

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
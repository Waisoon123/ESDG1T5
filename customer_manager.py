from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Customer Manager (CustID, Name, Gender, Email)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

class CustomerManager(db.Model):
    __tablename__ = "customer_manager"

    custID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(256), nullable=False)

    def __init__(self, custID, name, gender, email):
        self.custID = custID
        self.name = name
        self.gender = gender
        self.email = email

    def json(self):
        return {
            "custID": self.custID,
            "name": self.name,
            "gender": self.gender,
            "email": self.email,
        }

# Get customer by custID.
# Returns in the format of JSON.
@app.route("/customer_manager/<int:custID>")
def find_by_custID(custID):
    customer = CustomerManager.query.filter_by(custID=custID).first()
    if customer:
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Customer with ID {} not found.".format(custID)
        }
    ), 404

# Create new customer.
# Gets the data (custId, name, gender, email) from the request body.
@app.route("/customer_manager", methods=["POST"])
def create_customer():
    if (CustomerManager.query.filter_by(custID=request.json["custID"]).first()):
        return jsonify(
            {
                "code": 409,
                "data": {
                    "custID": request.json["custID"]
                },
                "message": "Customer with ID {} already exists.".format(request.json["custID"])
            }
        ), 409

    data = request.get_json()
    customer = CustomerManager(**data)

    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "custID": data["custID"]
                },
                "message": "An error occurred while creating the customer."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": customer.json()
        }
    ), 201




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)
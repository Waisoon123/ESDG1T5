from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Inventory Manager (date, productName, quantity)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

class InventoryManager(db.Model):
    __tablename__ = "inventory_manager"

    date = db.Column(db.Date, primary_key=True)
    productName = db.Column(db.String(256), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, date, productName, quantity):
        self.date = date
        self.productName = productName
        self.quantity = quantity

    def json(self):
        return {
            "date": self.date,
            "productName": self.productName,
            "quantity": self.quantity,
        }

# Get all inventory items.
# Returns in the format of JSON.
@app.route("/inventory_manager")
def get_all_inventory():
    inventoryList = InventoryManager.query.all()
    if len(inventoryList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [inventory.json() for inventory in inventoryList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no inventory."
        }
    ), 404

# Get all inventory by date and productName.
# Returns in the format of JSON.
@app.route("/inventory_manager/<string:date>/<string:productName>")
def find_by_date_and_productName(date, productName):
    inventoryList = InventoryManager.query.filter_by(date=date, productName=productName).all()
    if len(inventoryList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "inventory": [inventory.json() for inventory in inventoryList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Inventory not found."
        }
    ), 404


@app.route("/inventory_manager/update", methods=['UPDATE'])
def update_inventory():
    updateDetail = request.get_json()
    productName = updateDetail['productName']
    quantity = updateDetail['quantity']

    productInventory = InventoryManager.query.filter_by(productName=productName).first()
    if productInventory:
        productInventory.quantity = quantity
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": productInventory.json()
            }
        )

    return jsonify(
        {
            "code": 404,
            "message": f"Reservation with name {productName} not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Product Manager (productID, productName, images, productRate)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)

class ProductManager(db.Model):
    __tablename__ = "product_manager"

    productID = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(256), nullable=False)
    images = db.Column(db.String(256), nullable=False)
    productRate = db.Column(db.Float, nullable=False)

    def __init__(self, productID, productName, images, productRate):
        self.productID = productID
        self.productName = productName
        self.images = images
        self.productRate = productRate

    def json(self):
        return {
            "productID": self.productID,
            "productName": self.productName,
            "images": self.images,
            "productRate": self.productRate,
        }

# Get all products.
# Returns in the format of JSON.
@app.route("/product_manager")
def get_all_product():
    productList = ProductManager.query.all()
    if len(productList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "product": [product.json() for product in productList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no products."
        }
    ), 404

# Get product by productName.
# Returns in the format of JSON.
@app.route("/product_manager/<string:productName>")
def find_by_productName(productName):
    product = ProductManager.query.filter_by(productName=productName).first()
    if product:
        return jsonify(
            {
                "code": 200,
                "data": product.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Product with Name {} not found.".format(productName)
        }
    ), 404

# Get product by productID.
# Returns in the format of JSON.
@app.route("/product_manager/id/<int:productID>")
def find_by_productID(productID):
    product = ProductManager.query.filter_by(productID=productID).first()
    if product:
        return jsonify(
            {
                "code": 200,
                "data": product.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Product with ID {} not found.".format(productID)
        }
    ), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
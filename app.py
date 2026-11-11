
from flask import Flask, request, jsonify

from database import (
    initialize_database,
    get_all_products,
    get_product,
    add_product
)

app = Flask(__name__)

# Initialize the Product database
initialize_database()


# Health check endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Product Service",
        "status": "Running",
        "message": "Product Service is operational"
    }), 200


# Retrieve all products
@app.route("/products", methods=["GET"])
def list_products():
    products = get_all_products()

    return jsonify({
        "count": len(products),
        "products": products
    }), 200


# Retrieve a product using its ID
@app.route("/products/<int:product_id>", methods=["GET"])
def retrieve_product(product_id):
    product = get_product(product_id)

    if product is None:
        return jsonify({
            "error": "Product not found",
            "product_id": product_id
        }), 404

    return jsonify(product), 200


# Add a new product
@app.route("/products", methods=["POST"])
def create_product():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must contain valid JSON"
        }), 400

    name = data.get("name")
    description = data.get("description", "")
    price = data.get("price")
    stock = data.get("stock")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "Product name is required"
        }), 400

    if price is None or stock is None:
        return jsonify({
            "error": "Price and stock are required"
        }), 400

    try:
        price = float(price)
        stock = int(stock)

        if price < 0 or stock < 0:
            raise ValueError

    except (ValueError, TypeError, OverflowError):
        return jsonify({
            "error": "Price and stock must be valid non-negative numbers"
        }), 400

    product = add_product(
        name.strip(),
        description,
        price,
        stock
    )

    return jsonify({
        "message": "Product created successfully",
        "product": product
    }), 201


# Start the Flask application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )

from flask import Flask, render_template ,request, flash, redirect, url_for, session, jsonify
from pymongo import MongoClient
import random
import os



app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.urandom(24)  # Generates a new random key each time the server restarts
client = MongoClient("mongodb://localhost:27017/")
db = client["hci"]
product_collection = db["Product"]

@app.route("/")
def index():
    products = list(product_collection.find())
    random_products = random.sample(products, min(len(products), 3))
    # print("Random Products:", random_products)
    return render_template("index.html", random_products=random_products)

# ...
@app.route('/about/')
def about():
    return render_template('about.html')

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart_items=cart_items)

@app.route("/add_to_cart/<product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    # Check if the product is already in the cart
    for item in cart:
        if item["Product_id"] == product_id:
            item["quantity"] += 1
            session.modified = True
            flash("Item quantity updated in cart!", "success")
            return redirect(request.referrer)  # Redirect back to the same page

    # Fetch product details from MongoDB
    product = product_collection.find_one({"Product_id": product_id})
    if product:
        new_item = {
            "Product_id": product["Product_id"],
            "Product_name": product["Product_name"],
            "Description": product["Description"],
            "Images": product["Images"][0],  # Take first image
            "quantity": 1  # Initialize quantity
        }
        cart.insert(0, new_item)  # Add new item to the beginning of the list
        session.modified = True
        flash("Item added to cart!", "success")
        return redirect(request.referrer)  # Redirect back to the same page

    flash("Product not found!", "error")
    return redirect(request.referrer)

@app.route("/update_cart/<product_id>/<action>")
def update_cart(product_id, action):
    cart_items = session.get("cart", [])
    
    for item in cart_items:
        if item["Product_id"] == product_id:
            if action == "increase":
                item["quantity"] += 1
            elif action == "decrease":
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                else:
                    cart_items.remove(item)  # Remove item if quantity becomes 0
            break

    session["cart"] = cart_items
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<product_id>")
def remove_from_cart(product_id):
    cart_items = session.get("cart", [])
    session["cart"] = [item for item in cart_items if item["Product_id"] != product_id]
    session.modified = True  
    return redirect(url_for("cart"))


if __name__ == '__main__':
    app.run(debug=True)


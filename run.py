from flask import Flask, render_template ,request, flash, redirect, url_for, session, jsonify
from pymongo import MongoClient
import random
import os
from bson import ObjectId


app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.urandom(24)  # Generates a new random key each time the server restarts
client = MongoClient("mongodb://localhost:27017/")
db = client["hci"]
product_collection = db["Product"]

def get_product_by_id(product_id):
    """ Fetch a single product by ID from MongoDB """
    return product_collection.find_one({"Product_id": str(product_id)}) 

@app.route("/")
def index():
    products = list(product_collection.find())
    # random_products = random.sample(products, min(len(products), 3))
    # print("Random Products:", random_products)
    return render_template("index.html", random_products=products)

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

@app.route('/product/<product_id>')
def product_details(product_id):
    product = product_collection.find_one({"Product_id": product_id})  # Match by Product_id
    
    if product:
        # Ensure Images is always a list
        if isinstance(product.get("Images"), str):
            product["Images"] = [product["Images"]]  # Convert single string to list
        elif not isinstance(product.get("Images"), list):
            product["Images"] = ["placeholder.jpg"]  # Default if missing

        return render_template('view_details.html', product=product)

    return "Product Not Found", 404


if __name__ == '__main__':
    app.run(debug=True)


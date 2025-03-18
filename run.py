from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    jsonify,
)
from pymongo import MongoClient
import random
import os
from bson import ObjectId


app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.secret_key = os.urandom(
    24
)  # Generates a new random key each time the server restarts
client = MongoClient("mongodb://localhost:27017/")
db = client["hci"]
product_collection = db["Product"]


def get_product_by_id(product_id):
    """Fetch a single product by ID from MongoDB"""
    return product_collection.find_one({"Product_id": str(product_id)})


@app.route("/")
def index():
    products = list(product_collection.find())
    # random_products = random.sample(products, min(len(products), 3))
    # print("Random Products:", random_products)
    return render_template("index.html", random_products=products)


# ...
@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])

    # Use discount_price if available, otherwise use original_price
    subtotal = sum(
        item.get("discount_price", item.get("original_price", 0)) * item["quantity"]
        for item in cart_items
    )

    return render_template("cart.html", cart_items=cart_items, subtotal=subtotal)


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
            return redirect(request.referrer)

    # Fetch product details from MongoDB
    product = product_collection.find_one({"Product_id": product_id})
    if product:
        original_price = product.get("original_price", 0)
        discounted_price = product.get(
            "discount_price", original_price
        )  # Use discount_price if available

        new_item = {
            "Product_id": product["Product_id"],
            "Product_name": product["Product_name"],
            "Description": product["Description"],
            "Images": (
                product["Images"][0]
                if isinstance(product["Images"], list)
                else "placeholder.jpg"
            ),
            "quantity": 1,
            "original_price": original_price,
            "discounted_price": discounted_price,
        }
        cart.insert(0, new_item)
        session.modified = True
        flash("Item added to cart!", "success")
        return redirect(request.referrer)

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


@app.route("/product/<product_id>")
def product_details(product_id):
    product = product_collection.find_one(
        {"Product_id": product_id}
    )  # Match by Product_id

    if product:
        # Ensure Images is always a list
        if isinstance(product.get("Images"), str):
            product["Images"] = [product["Images"]]  # Convert single string to list
        elif not isinstance(product.get("Images"), list):
            product["Images"] = ["placeholder.jpg"]  # Default if missing

        return render_template("view_details.html", product=product)

    return "Product Not Found", 404


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart_items = session.get("cart", [])

    if not cart_items:
        flash("Your cart is empty!", "error")
        return redirect(url_for("cart"))

    subtotal = sum(
        item.get("discounted_price", item.get("original_price", 0)) * item["quantity"]
        for item in cart_items
    )
    shipping_fee = 50 if subtotal < 1000 else 0  # Free shipping for orders above ₹1000
    total = subtotal + shipping_fee

    if request.method == "POST":
        # Store shipping details in session for later use
        session["shipping_details"] = {
            "name": request.form.get("name"),
            "address": request.form.get("address"),
            "city": request.form.get("city"),
            "pincode": request.form.get("pincode"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "total": total,
        }
        return redirect(url_for("payment_options"))

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        subtotal=subtotal,
        shipping_fee=shipping_fee,
        total=total,
    )


@app.route("/payment-options")
def payment_options():
    if "shipping_details" not in session:
        return redirect(url_for("checkout"))
    return render_template("payment_options.html")


@app.route("/pay-with-card", methods=["GET", "POST"])
def pay_with_card():
    if "shipping_details" not in session:
        return redirect(url_for("checkout"))

    if request.method == "POST":
        return redirect(url_for("otp_page"))

    return render_template("payment_with_card.html")


@app.route("/otp", methods=["GET", "POST"])
def otp_page():
    if "shipping_details" not in session:
        return redirect(url_for("checkout"))

    if request.method == "POST":
        return redirect(url_for("order_confirmation"))

    return render_template("otp.html")


@app.route("/order-confirmation")
def order_confirmation():
    if "shipping_details" not in session:
        return redirect(url_for("checkout"))

    flash("Order placed successfully! 🎉", "success")
    session["cart"] = []  # Clear the cart after checkout
    session.pop("shipping_details", None)  # Clear shipping details
    session.modified = True
    return render_template("order_confirmation.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
from pymongo import MongoClient
import random

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
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

if __name__ == '__main__':
    app.run(debug=True)


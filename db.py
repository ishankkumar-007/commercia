from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["hci"]

# Collections
admin_collection = db["Admin"]
product_collection = db["Product"]
orders_collection = db["Orders"]

# Sample Admins
admins = [
    {
        "Admin_id": "Admin123",
        "Admin_name": "Nimisha Thallpally",
        "E-mail": "somethingra@idk.com",
        "Password": "admin123",
        "Address": "somewhere",
        "Contact": "555-1234"
    },
    {
        "Admin_id": "Admin456",
        "Admin_name": "John Doe",
        "E-mail": "john.doe@example.com",
        "Password": "admin456",
        "Address": "unknown",
        "Contact": "555-5678"
    }
]

# Function to calculate discount
def calculate_discount(original_price, discounted_price):
    return round(((original_price - discounted_price) / original_price) * 100, 2)

# Sample Products (20 Products with Prices & Discounts)
products = [
    {
        "Product_id": f"Prod{101 + i}",
        "Product_name": name,
        "Description": desc,
        "Images": [f"/static/images/{img1}", f"/static/images/{img2}"],
        "original_price": original_price,
        "discounted_price": discounted_price,
        "discount": calculate_discount(original_price, discounted_price)  # Dynamic discount calculation
    }
    for i, (name, desc, img1, img2, original_price, discounted_price) in enumerate([
        ("Laptop", "High-performance laptop with the latest processor", "laptop1.jpg", "laptop2.jpg", 1200, 999),
        ("Smartphone", "Latest model smartphone with AI-powered camera", "phone1.jpg", "phone2.jpg", 800, 699),
        ("Wireless Headphones", "Noise-canceling over-ear headphones with deep bass", "headphones1.jpg", "headphones2.jpg", 150, 119),
        ("Gaming Mouse", "High DPI gaming mouse with RGB lighting", "mouse1.jpg", "mouse2.jpg", 60, 49),
        ("Mechanical Keyboard", "RGB mechanical keyboard with blue switches", "keyboard1.jpg", "keyboard2.jpg", 100, 79),
        ("Smartwatch", "Fitness tracking smartwatch with heart rate monitoring", "smartwatch1.jpg", "smartwatch2.jpg", 200, 159),
        ("Bluetooth Speaker", "Portable Bluetooth speaker with waterproof design", "speaker1.jpg", "speaker2.jpg", 120, 89),
        ("External Hard Drive", "1TB external hard drive with fast transfer speeds", "harddrive1.jpg", "harddrive2.jpg", 90, 69),
        ("Wireless Earbuds", "Compact earbuds with noise isolation", "earbuds1.jpg", "earbuds2.jpg", 140, 109),
        ("4K Monitor", "27-inch 4K UHD monitor with HDR", "monitor1.jpg", "monitor2.jpg", 350, 299),
        ("VR Headset", "Next-gen VR headset with immersive experience", "vr1.jpg", "vr2.jpg", 500, 449),
        ("Action Camera", "Waterproof 4K action camera", "actioncam1.jpg", "actioncam2.jpg", 250, 199),
        ("Smart Home Hub", "Voice-controlled smart home hub", "smarthub1.jpg", "smarthub2.jpg", 180, 149),
        ("Drone", "Compact drone with 4K camera", "drone1.jpg", "drone2.jpg", 600, 499),
        ("Portable Projector", "Mini HD projector with Wi-Fi", "projector1.jpg", "projector2.jpg", 250, 199),
        ("Smart Light Bulbs", "Wi-Fi LED bulbs with colors", "lightbulb1.jpg", "lightbulb2.jpg", 50, 39),
        ("Electric Toothbrush", "Rechargeable toothbrush with modes", "toothbrush1.jpg", "toothbrush2.jpg", 80, 59),
        ("Dash Cam", "Full HD dash cam with night vision", "dashcam1.jpg", "dashcam2.jpg", 150, 129),
        ("Wireless Charger", "Fast wireless charging pad", "charger1.jpg", "charger2.jpg", 40, 29),
        ("Robot Vacuum Cleaner", "Smart vacuum with mapping", "robotvacuum1.jpg", "robotvacuum2.jpg", 450, 399)
    ])
]

# Sample Orders
orders = [
    {
        "Invoice": f"INV_Cust{i}_Prod{101 + i % 20}",
        "Customer_id": f"Cust{i}",
        "Product_id": f"Prod{101 + i % 20}",
        "Quantity": (i % 5) + 1,
        "Status": "Pending" if i % 3 == 0 else "Shipped" if i % 3 == 1 else "Delivered"
    }
    for i in range(123, 143)
]

# Insert Sample Data
def populate_data():
    # Insert Admins
    admin_collection.delete_many({})
    admin_collection.insert_many(admins)
    print("✅ Admin data inserted!")

    # Insert Products
    product_collection.delete_many({})
    product_collection.insert_many(products)
    print("✅ Product data inserted!")

    # Insert Orders
    orders_collection.delete_many({})
    orders_collection.insert_many(orders)
    print("✅ Order data inserted!")

# Run Data Population
if __name__ == "__main__":
    populate_data()
    print("\n📌 Database successfully populated with sample data!")

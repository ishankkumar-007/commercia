from pymongo import MongoClient
from random import randint, choice, uniform

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
offers_list = [
    "Get extra 10% off with code SAVE10",
    "Free shipping on orders above ₹5000",
    "Buy 1 Get 1 Free on select items",
    "Get a ₹500 gift card on your next purchase",
    "Flat ₹200 off on prepaid orders",
    "Extra 5% cashback on select bank credit cards",
    "Extended 1-year warranty for free",
    "Exchange old product & get ₹1000 off"
]
# Function to calculate discount
def calculate_discount(original_price, discounted_price):
    return round(((original_price - discounted_price) / original_price) * 100, 2)

# Sample Specifications
specs_dict = {
   "Laptop": {
        "Processor": "Intel i7 12th Gen",
        "RAM": "16GB DDR4",
        "Storage": "512GB SSD",
        "Display": "15.6-inch Full HD",
        "Graphics": "NVIDIA GeForce GTX 1650",
        "Battery Life": "10 hours",
        "Weight": "1.8 kg",
        "Keyboard": "Backlit",
        "Ports": "3 x USB 3.0, 1 x USB-C, HDMI",
        "Audio": "Stereo Speakers with Dolby Audio",
        "Webcam": "720p HD",
        "Operating System": "Windows 11",
        "Cooling": "Dual Fan",
        "Connectivity": "Wi-Fi 6",
        "Bluetooth": "5.0",
        "SD Card Slot": "Yes",
        "Webcam Privacy Shutter": "Yes",
        "Fingerprint Sensor": "Yes",
        "Color": "Silver",
        "Security": "TPM 2.0"
    },
    "Smartphone": {
        "Processor": "Snapdragon 8 Gen 2",
        "RAM": "12GB",
        "Storage": "256GB",
        "Display": "6.7-inch AMOLED",
        "Resolution": "3200x1440",
        "Battery": "5000mAh",
        "Charging": "65W Fast Charging",
        "Camera": "108MP main sensor",
        "Front Camera": "32MP",
        "Operating System": "Android 13",
        "Connectivity": "5G",
        "Bluetooth": "5.3",
        "Wi-Fi": "Wi-Fi 6",
        "Fingerprint Scanner": "Under-display",
        "Face Unlock": "Yes",
        "NFC": "Yes",
        "IP Rating": "IP68",
        "Dual SIM": "Yes",
        "Color": "Black, Silver, Blue",
        "Audio": "Stereo speakers"
    },
    "Wireless Headphones": {
        "Battery Life": "30 hours",
        "Noise Cancellation": "Yes",
        "Connectivity": "Bluetooth 5.0",
        "Charging Port": "USB-C",
        "Drivers": "40mm dynamic drivers",
        "Foldable Design": "Yes",
        "Sweat Resistance": "Yes",
        "Microphone": "Built-in mic",
        "Volume Control": "Yes",
        "Voice Assistant": "Supported",
        "Weight": "250g",
        "Color": "Black, White, Blue",
        "Charging Time": "1.5 hours",
        "Wireless Range": "10 meters",
        "Controls": "Touch-sensitive",
        "EQ": "Customizable sound",
        "Active Noise Cancellation Levels": "Adjustable",
        "Impedance": "32 ohms",
        "Frequency Response": "20Hz - 20kHz",
        "Multi-point Connection": "Yes"
    },
    "Gaming Mouse": {
        "DPI": "16000",
        "Buttons": "7",
        "RGB": "Yes",
        "Sensor": "Optical",
        "Connectivity": "Wired",
        "Weight": "85g",
        "Cable": "1.8 meters braided",
        "Switches": "Omron switches",
        "Customizable Buttons": "Yes",
        "Polling Rate": "1000Hz",
        "Grip Type": "Ambidextrous",
        "Software": "Customizable macros",
        "Cable Type": "Flexible",
        "Sensor Type": "PixArt 3335",
        "Lighting": "Full RGB Spectrum",
        "Lift-Off Distance": "Adjustable",
        "Weight Tuning": "Yes",
        "Color": "Black, White, Gray",
        "Ergonomic Design": "Yes",
        "Onboard Memory": "Yes"
    },
    "Mechanical Keyboard": {
        "Switch Type": "Blue",
        "Backlight": "RGB",
        "Connectivity": "Wired",
        "Keys": "104",
        "Key Rollover": "Anti-Ghosting",
        "Polling Rate": "1000Hz",
        "Keycaps": "ABS",
        "Weight": "1.2 kg",
        "Audio Feedback": "Clicky",
        "Key Switch Lifespan": "50 million keystrokes",
        "Color": "Black, White",
        "RGB Zones": "Customizable",
        "Warranty": "2 years",
        "Macro Support": "Yes",
        "Onboard Memory": "Yes",
        "Cable Length": "1.8 meters",
        "Programmable Keys": "Yes",
        "Media Controls": "Yes",
        "Ergonomic Design": "Yes",
        "Compatibility": "Windows, Mac, Linux"
    },
    "Smartwatch": {
        "Heart Rate Monitor": "Yes",
        "Water Resistance": "5 ATM",
        "Display": "1.4-inch AMOLED",
        "Battery Life": "48 hours",
        "Charging": "Magnetic charging",
        "GPS": "Built-in",
        "Bluetooth": "5.0",
        "Operating System": "Wear OS",
        "Steps Tracker": "Yes",
        "Sleep Tracker": "Yes",
        "Sleep Stages": "Yes",
        "Notifications": "Text, Calls, Apps",
        "Color": "Black, Silver, Gold",
        "Voice Assistant": "Yes",
        "Music Control": "Yes",
        "Storage": "4GB",
        "Sensors": "Accelerometer, Gyroscope",
        "Display Resolution": "454x454",
        "Weight": "40g"
    },
    "Bluetooth Speaker": {
        "Battery Life": "12 hours",
        "Waterproof": "IPX7",
        "Bluetooth Version": "5.0",
        "Audio Output": "Stereo",
        "Driver Size": "40mm",
        "Charging Port": "USB-C",
        "Audio Input": "AUX",
        "Built-in Mic": "Yes",
        "Color": "Black, Blue, Red",
        "Power Output": "10W",
        "Weight": "350g",
        "Voice Assistant": "Supported",
        "Frequency Response": "20Hz - 20kHz",
        "Dimensions": "7.5 x 7.5 x 10 cm",
        "Connectivity": "Bluetooth, Aux",
        "Bluetooth Range": "10 meters",
        "Sound Modes": "Bass Boost",
        "Material": "Rubberized plastic",
        "Speakerphone": "Yes",
        "Built-in Subwoofer": "Yes"
    },
    "External Hard Drive": {
        "Capacity": "1TB",
        "Interface": "USB 3.1",
        "Data Transfer Speed": "5Gbps",
        "Form Factor": "Portable",
        "Dimensions": "11.5 x 7.5 x 1.5 cm",
        "Weight": "200g",
        "Compatibility": "Windows, Mac, Linux",
        "Shockproof": "Yes",
        "Password Protection": "Yes",
        "Encryption": "AES 256-bit",
        "Warranty": "3 years",
        "Connection Type": "USB-C, USB-A",
        "Operating System Support": "Windows 10, macOS 10.13+",
        "Durability": "Military-grade",
        "Power Supply": "Bus-powered",
        "Color": "Black, Silver",
        "Backup Software": "Yes",
        "Speed Boost": "Yes",
        "Portability": "Yes"
    },
    "Wireless Earbuds": {
        "Battery Life": "24 hours",
        "Active Noise Cancellation": "Yes",
        "Charging Case": "Yes",
        "Bluetooth": "5.0",
        "Water Resistance": "IPX4",
        "Sound Quality": "Hi-Fi",
        "Drivers": "10mm",
        "Microphone": "Built-in",
        "Touch Controls": "Yes",
        "Voice Assistant": "Yes",
        "Charging Time": "1 hour",
        "Weight": "4.5g per earbud",
        "Range": "10 meters",
        "Connectivity": "Bluetooth",
        "Latency": "Low",
        "Color": "Black, White",
        "Ear Tips": "Multiple sizes",
        "Charging Port": "USB-C",
        "Sweat Resistance": "Yes"
    },
    "4K Monitor": {
        "Size": "27 inches",
        "Resolution": "3840x2160",
        "Refresh Rate": "144Hz",
        "Color Gamut": "100% sRGB",
        "Ports": "2 x HDMI, 1 x DisplayPort",
        "Response Time": "1ms",
        "HDR Support": "Yes",
        "Stand Type": "Height adjustable",
        "VESA Mount": "Yes",
        "Panel Type": "IPS",
        "Brightness": "350 nits",
        "Viewing Angle": "178°",
        "G-Sync": "Yes",
        "Flicker-Free": "Yes",
        "Blue Light Filter": "Yes",
        "Weight": "4.5kg",
        "Speakers": "Built-in",
        "USB Hub": "Yes",
        "Power Consumption": "50W"
    },
    "VR Headset": {"Field of View": "110°", "Wireless": "Yes"},
    "Action Camera": {"Resolution": "4K", "Waterproof": "Yes"},
    "Smart Home Hub": {"Voice Assistant": "Alexa", "Connectivity": "Wi-Fi"},
    "Drone": {"Camera": "4K", "Flight Time": "30 minutes"},
    "Portable Projector": {"Resolution": "1080p", "Battery": "Yes"},
    "Smart Light Bulbs": {"Colors": "16M", "Smart Control": "Yes"},
    "Electric Toothbrush": {"Modes": "3", "Battery Life": "14 days"},
    "Dash Cam": {"Resolution": "1080p", "Night Vision": "Yes"},
    "Wireless Charger": {"Fast Charging": "Yes", "Power Output": "15W"},
    "Robot Vacuum Cleaner": {"Mapping": "Yes", "Suction Power": "2500Pa"}
}

# Sample Ratings & Reviews
customer_reviews = [
    {"Customer": "Alice", "Rating": 5, "Review": "Amazing product! Totally worth it."},
    {"Customer": "Bob", "Rating": 4, "Review": "Good quality but slightly expensive."},
    {"Customer": "Charlie", "Rating": 3, "Review": "Works fine but expected better."},
    {"Customer": "Dave", "Rating": 5, "Review": "Best purchase I've made this year!"},
    {"Customer": "Emma", "Rating": 4, "Review": "Pretty good, but delivery was slow."}
]

# Sample Products (20 Products with New Fields)
products = [
    {
        "Product_id": f"Prod{101 + i}",
        "Product_name": name,
        "Description": desc,
        "Images": [f"/static/images/{img1}", f"/static/images/{img2}"],
        "original_price": original_price,
        "discounted_price": discounted_price,
        "discount": calculate_discount(original_price, discounted_price),  # Dynamic discount calculation
        "Specifications": specs_dict.get(name, {}),
        "Available": choice(["In Stock", "Limited Stock", "Out of Stock"]),
        "Offers": [choice(offers_list) for _ in range(3)],
        "Rating": round(uniform(3.5, 5), 1),  # Random rating between 3.5 and 5
        "Customer_Reviews": [choice(customer_reviews) for _ in range(randint(3, 5))]  # Random reviews (1 to 5)
    }
    for i, (name, desc, img1, img2, original_price, discounted_price) in enumerate([
        ("Laptop", "Experience lightning-fast performance with the latest Intel i9 processor and a stunning 15.6-inch 4K OLED display. Whether you’re a professional content creator, a hardcore gamer, or someone who needs power on the go, this laptop is designed to meet your needs. With 32GB of DDR5 RAM, a 1TB SSD, and an NVIDIA RTX 4070 graphics card, it delivers seamless multitasking and immersive graphics. Its sleek aluminum design and long-lasting battery make it a perfect companion for work and entertainment.", "laptop1.jpg", "laptop2.jpg", 1200, 999),
        ("Smartphone",  "Unleash the power of AI with this cutting-edge smartphone featuring a 108MP triple-camera setup, an ultra-smooth 120Hz AMOLED display, and a powerful Snapdragon 8 Gen 2 processor. Capture stunning photos even in low light, enjoy seamless gaming, and experience all-day battery life with its 5000mAh capacity. With 12GB of RAM and 256GB of storage, you'll have all the speed and space you need. Built with 5G connectivity, this phone ensures ultra-fast browsing and streaming.", "phone1.jpg", "phone2.jpg", 800, 699),
        ("Wireless Headphones",          "Immerse yourself in high-fidelity sound with these premium noise-canceling headphones. With up to 30 hours of battery life, these headphones ensure you enjoy uninterrupted music, podcasts, or calls. Designed for comfort with plush ear cushions, they feature adaptive noise cancellation and a built-in mic for crystal-clear calls. Bluetooth 5.2 provides a seamless connection, and the foldable design makes them easy to carry anywhere.", "headphones1.jpg", "headphones2.jpg", 150, 119),
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

# Insert Data into Database
def populate_data():
    admin_collection.delete_many({})
    admin_collection.insert_many(admins)
    print("✅ Admin data inserted!")

    product_collection.delete_many({})
    product_collection.insert_many(products)
    print("✅ Product data inserted!")

# Run Data Population
if __name__ == "__main__":
    populate_data()
    print("\n📌 Database successfully populated with updated product details!")

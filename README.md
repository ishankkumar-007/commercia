# Commercia – HCI Case Study on E-Commerce Design

**Commercia** is an HCI-focused e-commerce prototype built to explore the application of core interaction design principles in real-world web applications. This project simulates an end-to-end online shopping experience with a clean, minimal interface and responsive UI. It is designed using Flask and styled entirely with Tailwind CSS.

---

## Objectives

The primary goal of Commercia is to investigate how established HCI laws influence user behavior and improve usability in e-commerce platforms. Key design principles include:

* **Tesler’s Law** – Simplifying user interactions without removing necessary complexity.
* **Power Law of Practice** – Improving learnability and efficiency through repetition.
* **Hick’s Law** – Reducing cognitive load by minimizing user choices.
* **Fitts’ Law** – Optimizing the size and placement of interactive elements.
* **Gestalt Laws** – Enhancing perception through alignment, proximity, and continuity.
* **Color Theory** – Using color strategically to guide attention and evoke emotion.
* **Minimalism** – Focusing on essential elements for a distraction-free experience.
* **Pareto Principle (80/20 Rule)** – Prioritizing high-impact features.
* **Multiplicity of Features** – Offering multiple pathways to achieve the same goal (e.g., search vs. category navigation).
* **Law of Recency and Primacy** – Displaying critical information prominently.
* **Inverted Pyramid Structure** – Presenting key functionality and offers at the top.

---

## Features

* **User Authentication** – Sign Up / Sign In with validation
* **Product Listings** – Browse products by category
* **Product Details** – View detailed information with call-to-action
* **Shopping Cart** – Add/remove items, view total
* **Checkout Flow** – Seamless order placement interface
* **Order Confirmation** – Clear success feedback
* **Responsive UI** – Fully responsive and optimized for all screen sizes
* **Tailwind CSS Styling** – Custom-built utility-first UI components

---

## 📁 Project Structure

```
app/
│
├── static/
│   └── css/
│       ├── main.css                # Compiled Tailwind output
│       ├── style.css               # Custom styles
│       └── styles.css              # Tailwind base styles
│
├── templates/
│   ├── components/
│   │   ├── base.html
│   │   ├── header.html
│   │   └── footer.html
│   ├── index.html
│   ├── signin.html
│   ├── signup.html
│   ├── products.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── order_success.html
│
├── db.py                # Initializes MongoDB collections
├── run.py               # Flask app entry point
├── tailwind.config.js   # Tailwind CSS configuration
├── package.json         # Tailwind build script and dependency
├── package-lock.json
└── README.md
```

---

## Requirements

* Python 3.8+
* Node.js (for Tailwind CSS)
* Flask (install via pip)
* Tailwind CSS (installed via npm)
* MongoDB (local or cloud instance)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ishankumar007/commercia.git
cd commercia
```

### 2. Set Up Python Environment

```bash
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
pip install flask pymongo
```

### 3. Start MongoDB (Local)

Ensure MongoDB is running on your machine:

```bash
sudo systemctl start mongod
```

Check status with:

```bash
sudo systemctl status mongod
```

### 4. Initialize the Database

```bash
python db.py
```

### 5. Install Node.js Dependencies

```bash
npm install
```

### 6. Compile Tailwind CSS

```bash
npm run css
```

> Watches `styles.css` and compiles output to `main.css`.

### 7. Run the Flask App

```bash
python run.py
```

### 8. Access the Web App

Open your browser and go to:

```
http://localhost:5000
```

## Notes

* Tailwind styles can be customized in the `static/css` directory.
* MongoDB collections are initialized in `db.py` based on basic schema.

---

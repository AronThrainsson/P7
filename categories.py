from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('babyfood.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to fetch products by category
def get_category_products(database="babyfood.db"):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    categories = ["Breakfast", "Lunch", "Dinner"]
    category_products = {}

    for category in categories:
        cursor.execute("""
            SELECT p.id, p.name, b.name AS brand_name, p.kcal, p.heavy_metals, 
                   p.pesticides, p.microplastics, p.images
            FROM Products p
            JOIN Brands b ON p.brand_id = b.id
            WHERE p.category = ?
            LIMIT 10
        """, (category,))
        rows = cursor.fetchall()

        category_products[category] = [
            {
                "id": row["id"],
                "name": row["name"],
                "brand_name": row["brand_name"],
                "kcal": row["kcal"],
                "heavy_metals": row["heavy_metals"],
                "pesticides": row["pesticides"],
                "microplastics": row["microplastics"],
                "images": row["images"]
            }
            for row in rows
        ]

    conn.close()
    return category_products

# Silently save a product to the grocery list
def save_product_silently(product_id, database="babyfood.db"):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Insert into GroceryList without checking or giving feedback
    cursor.execute("INSERT OR IGNORE INTO GroceryList (product_id) VALUES (?)", (product_id,))
    conn.commit()
    conn.close()

# Function to remove a product from the grocery list
def remove_from_grocery_list(product_id, database="babyfood.db"):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Delete the product from the GroceryList
    cursor.execute("DELETE FROM GroceryList WHERE product_id = ?", (product_id,))
    conn.commit()

    # Check if the product was successfully removed
    cursor.execute("SELECT * FROM GroceryList WHERE product_id = ?", (product_id,))
    result = cursor.fetchone()
    conn.close()

    # If no record is found, return success
    return result is None

# Route for categories
@app.route('/categories')
def categories():
    categories = get_categories_with_products()  # Fetch categories and products from DB
    return render_template('categories.html', categories=categories)

@app.route('/save_product/<int:product_id>', methods=['POST'])
def save_product(product_id):
    # Add product to grocery list
    product = Product.query.get(product_id)
    if product:
        # Assuming you have a GroceryList model
        new_entry = GroceryList(product_id=product.id)  # Modify this based on your actual table structure
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"status": "saved"})
    return jsonify({"status": "error"}), 400

@app.route('/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    # Remove product from grocery list
    product_entry = GroceryList.query.filter_by(product_id=product_id).first()
    if product_entry:
        db.session.delete(product_entry)
        db.session.commit()
        return jsonify({"status": "removed"})
    return jsonify({"status": "error"}), 400

def get_categories_with_products():
    # Fetch categories and their associated products from DB
    categories = {}  # Dictionary to store categories and their products
    products = Product.query.all()  # Query all products (you may want to filter this based on categories)
    for product in products:
        category = product.category.name  # Assuming product has a relationship to category
        if category not in categories:
            categories[category] = []
        categories[category].append(product)

    return categories

# Route to display the grocery list
@app.route("/grocery_list")
def grocery_list():
    conn = sqlite3.connect("babyfood.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all saved products from grocery list
    cursor.execute("""
        SELECT p.id, p.name, b.name AS brand_name, p.kcal, p.heavy_metals, 
               p.pesticides, p.microplastics, p.images
        FROM GroceryList g
        JOIN Products p ON g.product_id = p.id
        JOIN Brands b ON p.brand_id = b.id
    """)
    rows = cursor.fetchall()

    grocery_items = [
        {
            "id": row["id"],
            "name": row["name"],
            "brand_name": row["brand_name"],
            "kcal": row["kcal"],
            "heavy_metals": row["heavy_metals"],
            "pesticides": row["pesticides"],
            "microplastics": row["microplastics"],
            "images": row["images"]
        }
        for row in rows
    ]

    conn.close()
    return render_template("grocery_list.html", grocery_items=grocery_items)


if __name__ == "__main__":
    app.run(debug=True)

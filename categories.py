import sqlite3

# Helper function to get a database connection
def get_db():
    conn = sqlite3.connect('babyfood.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to fetch category products
def get_category_products(database="babyfood.db"):
    conn = get_db()
    cursor = conn.cursor()
    categories = ["Breakfast", "Lunch", "Dinner"]
    category_products = {}

    for category in categories:
        cursor.execute("""
            SELECT p.id, p.name, b.name AS brand_name, p.kcal, p.heavy_metals, 
                   p.pesticides, p.microplastics, p.images, p.stores
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
                "images": row["images"],
                "stores": row["stores"]
            }
            for row in rows
        ]

    conn.close()
    return category_products

# Function to save product silently to the grocery list
def save_product_silently(product_id, user_id, database="babyfood.db"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO GroceryList (product_id, user_id)
        VALUES (?, ?)
    """, (product_id, user_id))
    conn.commit()
    conn.close()

# Function to remove a product from the grocery list
def remove_from_grocery_list(product_id, user_id, database="babyfood.db"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM GroceryList
        WHERE product_id = ? AND user_id = ?
    """, (product_id, user_id))
    conn.commit()
    conn.close()
    return True
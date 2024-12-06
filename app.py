from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sqlite3
import secrets
import base64
from PIL import Image
from io import BytesIO
import easyocr
import numpy as np

from categories import get_category_products, save_product_silently
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management
reader = easyocr.Reader(['en', 'da'])  # Initialize EasyOCR for English

# Hash a password
hashed_password = generate_password_hash("your_password")

# Verify the password
is_correct = check_password_hash(hashed_password, "your_password")
print(is_correct)  # Should print True if the password is correct

def check_user_data():
    conn = sqlite3.connect('babyfood.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, password FROM users")
    users = cursor.fetchall()
    conn.close()
    for user in users:
        print(user)

check_user_data()

# Function to connect to the database
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn

def get_user_id_from_db(username):
    conn = get_db_connection('babyfood.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user['user_id']
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/expert")
def expert():
    return render_template("expert.html")

@app.route("/common")
def common():
    return render_template("common.html")

@app.route("/general")
def general():
    return render_template("general.html")

@app.route("/camera")
def camera():
    return render_template("camera.html")

# OCR scanning function
@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.get_json()
        image_data = data.get('image')
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data provided.'})

        # Decode Base64 image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_data))

        # Convert PIL Image to NumPy array
        image_array = np.array(image)

        # Perform OCR
        result = reader.readtext(image_array, detail=0)  # EasyOCR accepts NumPy arrays
        extracted_text = " ".join(result)

        return jsonify({'success': True, 'text': extracted_text})
    except Exception as e:
        print(f"Error during OCR: {e}")  # Log the error for debugging
        return jsonify({'success': False, 'message': str(e)})

# Handle signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        with get_db_connection('babyfood.db') as conn:
            cursor = conn.cursor()
            
            # Check if the username already exists
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print("Username already exists")  # Debugging log
                return render_template('signup.html', error="Username already exists.")
            
            # Insert the new user
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]

        session['username'] = username  # Store username in session
        session['user_id'] = user_id  # Store user_id in session
        print(session)  # Debugging log
        return redirect(url_for('categories'))  # Redirect to categories page after signup
    return render_template('signup.html')

# Handle login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection('babyfood.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            # User not found
            print("User not found")  # Debugging log
            return render_template("login.html", error="Invalid username or password.")
        
        user_id, hashed_password = user

        # Verify the password
        if not check_password_hash(hashed_password, password):
            print("Invalid password")  # Debugging log
            return render_template("login.html", error="Invalid username or password.")

        # Store user_id in session
        session['username'] = username  # Store username in session
        session['user_id'] = user_id  # Store user_id in session
        print(f"User logged in, session['user_id']: {session['user_id']}")  # Debugging log
        print(session)  # Debugging log
        return redirect(url_for("categories"))

    return render_template("login.html")

# Search route for brands and products from babyfoodlabels.db
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("query")

    # If no search term is provided, show a message
    if not query or query.strip() == "":
        return render_template("results.html", products=[], message="Please enter a search term.")

    try:
        conn = get_db_connection("babyfoodlabels.db")
        cursor = conn.cursor()

        # SQL query to search for the term in brand or any of the product columns (products1 to products5)
        cursor.execute("""
            SELECT brands, products1, products2, products3, products4, products5, image1, image2, image3, image4, image5
            FROM babyfoodlabels
            WHERE brands LIKE ? OR products1 LIKE ? OR products2 LIKE ? OR products3 LIKE ? OR products4 LIKE ? OR products5 LIKE ?
        """, ('%' + query + '%',) * 6)  # Search all product columns for the term (LIKE = search)

        rows = cursor.fetchall()
        conn.close()

        # Process the query results
        products = []
        for row in rows:
            brand = row["brands"]  # Accessing brand from the row
            product_data = []  # Initialize product_data inside the loop for each brand
            for i in range(1, 6):  # Iterate over products1 to products5 columns
                product = row[f"products{i}"]  # Access product columns by name
                image = row[f"image{i}"]  # Access corresponding image column
                print(f"Product {i}: {product}, Image: {image}")  # Debugging: Print the product for each iteration
                
                if product:  # Ensure that the product is not None or empty
                    if query.lower() in product.lower() or query.lower() in brand.lower():  # Case-insensitive matching for products or brands
                        product_data.append({"brand": brand, "product": product, "image": image})  # Add brand and product to the list

            if product_data:
                products.append(product_data)

        # If no products are found, set the message
        message = f"No results for '{query}'." if not products else ""

        # Return the results template with products and message
        return render_template("results.html", products=products, message=message, query=query)

    except Exception as e:
        print(f"Database error: {e}")
        return "Database connection or query failed.", 500
    
# Display product details page
@app.route('/product/<product_name>')
def product_details(product_name):
    # Connect to the database
    conn = sqlite3.connect('babyfoodlabels.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = """
    SELECT 
        b.brands AS brand_name,
        b.products1, b.products2, b.products3, b.products4, b.products5,
        b.image1, b.image2, b.image3, b.image4, b.image5,
        h.toxic_metals, h.pesticides, h.microplastics, h.protein_name
    FROM 
        babyfoodlabels b
    JOIN 
        healthiness h ON b.labelID = h.label_id
    WHERE 
        b.products1 = ? OR b.products2 = ? OR b.products3 = ? OR b.products4 = ? OR b.products5 = ?;
    """
    
    # Execute the query
    cursor.execute(query, (product_name, product_name, product_name, product_name, product_name))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        # Iterate over product columns to find the matching product
        product_names = [result['products1'], result['products2'], result['products3'], result['products4'], result['products5']]
        product_images = [result['image1'], result['image2'], result['image3'], result['image4'], result['image5']]

        # Check if the product_name matches any of the product columns
        product_index = None
        for i, name in enumerate(product_names):
            if name and name.lower() == product_name.lower():
                product_index = i
                break

        if product_index is not None:
            # Get the matching product and its corresponding image
            product_data = {
                'brand': result['brand_name'],
                'product': product_names[product_index],
                'image': product_images[product_index],
                'toxic_metals': result['toxic_metals'],
                'pesticides': result['pesticides'],
                'microplastics': result['microplastics'],
                'protein_name': result['protein_name']
            }
            # Render the product details page with the selected product
            return render_template('product_details.html', product=product_data)
        else:
            return render_template('product_not_found.html', product_name=product_name)
    else:
        # If the product is not found, show a 404 or product not found page
        return render_template('product_not_found.html', product_name=product_name)

# Route to display the grocery list
@app.route("/grocery_list")
def grocery_list():
    print(session)  # Debugging log
    user_id = session.get('user_id')
    conn = get_db_connection('babyfood.db')
    cursor = conn.cursor()

    if user_id:
        print(f"User ID from session: {user_id}")  # Debugging log
        # Query to get product details for the user's grocery list
        cursor.execute("""
            SELECT p.id, p.name, b.name AS brand_name, p.kcal, p.heavy_metals, p.pesticides, p.microplastics, p.images, p.stores 
            FROM Products p
            JOIN GroceryList g ON p.id = g.product_id
            JOIN Brands b ON p.brand_id = b.id
            WHERE g.user_id = ?
        """, (user_id,))
    else:
        print("No user logged in")  # Debugging log
        # If no user is logged in, get products from session
        grocery_list = session.get('grocery_list', [])
        if grocery_list:
            cursor.execute("""
                SELECT p.id, p.name, b.name AS brand_name, p.kcal, p.heavy_metals, p.pesticides, p.microplastics, p.images, p.stores 
                FROM Products p
                JOIN Brands b ON p.brand_id = b.id
                WHERE p.id IN ({})
            """.format(','.join('?' * len(grocery_list))), grocery_list)
        else:
            cursor.execute("SELECT 1 WHERE 0")  # No products to fetch

    grocery_items = cursor.fetchall()
    print(f"Grocery items fetched: {grocery_items}")  # Debugging log
    conn.close()

    if not grocery_items:
        message = "No products added yet."
        print(message)  # Debugging log
        return render_template('grocery_list.html', grocery_items=[], message=message)
    else:
        return render_template('grocery_list.html', grocery_items=grocery_items)

# Route to display the categories and products
@app.route("/products", methods=['GET', 'POST'])
def categories():
    category_products = get_category_products("babyfood.db")  # Get products from categories.py
    saved_product_ids = []

    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection('babyfood.db')
        cursor = conn.cursor()
        cursor.execute("SELECT product_id FROM GroceryList WHERE user_id = ?", (user_id,))
        saved_product_ids = [row['product_id'] for row in cursor.fetchall()]
        conn.close()

    return render_template("products.html", categories=category_products, saved_product_ids=saved_product_ids)

# Route to save a product to the grocery list
@app.route('/save_product/<int:product_id>', methods=['POST'])
def save_product(product_id):
    if 'user_id' not in session:
        # If not logged in, return a message prompting the user to log in
        return jsonify({"status": "not_logged_in", "message": "Please log in to save products to your grocery list."})
    
    user_id = session['user_id']
    save_product_silently(product_id, user_id)
    return jsonify({"status": "saved"})

# Route to remove a product from the grocery list
@app.route('/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    if 'user_id' not in session:
        # If not logged in, return an error message
        return jsonify({"status": "error", "message": "Please log in to remove products from your grocery list."})
    
    user_id = session['user_id']
    conn = get_db_connection('babyfood.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM GroceryList WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "removed"})

# Route to log out the user
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    print(session)  # Debugging log
    return redirect(url_for('index'))  # Redirect to the homepage or login page

if __name__ == "__main__":
    app.run(debug=True)
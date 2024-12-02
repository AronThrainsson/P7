from flask import Flask, render_template, request, session, redirect
import sqlite3
from categories import get_category_products

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # For session management

# Function to connect to the database
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn

# Render functions for web pages
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
def toxins():
    return render_template("general.html")

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

# Display categorized products from babyfood.db
@app.route("/categories")
def categories():
    #call the function from categories.py
    category_products = get_category_products("babyfood.db")
    return render_template("categories.html", categories=category_products)
    
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('babyfoodlabels.db')  # Corrected path
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

# Search route
@app.route('/search', methods=['GET'])
def search_labels():
    query = request.args.get('query')

    if not query:
        return "Please provide a search term", 400

    try:
        conn = get_db_connection() 
        cursor = conn.cursor()

        # Search query
        cursor.execute("""
            SELECT * FROM babyfoodlabels 
            WHERE name LIKE ? OR products LIKE ?
        """, (f'%{query}%', f'%{query}%'))
        results = cursor.fetchall()
        conn.close()

        # Convert results to a list of dictionaries
        labels = [dict(row) for row in results]

        # Render the results in an HTML template
        return render_template("results.html", query=query, labels=labels)

    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error occurred: {e}")
        return "An error occurred while processing your request.", 500

if __name__ == '__main__':
    app.run(debug=True)
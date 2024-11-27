import random
import sqlite3

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Function to connect to the database
def connect_db():
    connection = sqlite3.connect('movies.db')
    connection.row_factory = sqlite3.Row  # Allows accessing columns by name
    return connection

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/expert")
def expert():
    return render_template("expert.html")

@app.route("/common")
def common():
    return render_template("common.html")

@app.route("/toxins")
def toxins():
    return render_template("toxins.html")

if __name__ == '__main__':
    app.run(debug=True)

#NEW

# Home route to render the main page
# Search route
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get the search query from the URL
    if not query:
        return jsonify({"error": "No query provided"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Query the database for movies with titles containing the search word
    cursor.execute(
        "SELECT title, year FROM movies WHERE title LIKE ?",
        (f"%{query}%",)
    )
    results = [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries

    conn.close()

    return jsonify(results)  # Return results as JSON
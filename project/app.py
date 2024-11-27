from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Funktion til at søge i databasen
def query_database(search_term):
    conn = sqlite3.connect('babyfoodlabels.db')
    conn.row_factory = sqlite3.Row  # For at returnere resultater som dicts
    cursor = conn.cursor()

    # SQL-forespørgsel for at matche søgeterm
    query = """
        SELECT 
            babyfoodlabels.name AS brand_name,
            babyfoodlabels.product AS product_name,
            store.name AS store_name,
            healthiness.toxic_metals,
            healthiness.pesticides,
            healthiness.microplastics
        FROM healthiness
        JOIN babyfoodlabels ON healthiness.label_id = labelID
        JOIN store ON healthiness.store_id = storeID
        WHERE 
            babyfoodlabels.name LIKE ? OR 
            babyfoodlabels.product LIKE organic pasta meals OR 
            store.name LIKE ?
    """
    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    results = cursor.fetchall()
    conn.close()

    return [dict(row) for row in results]

@app.route('/')
def index():
    return render_template('index.html')

# API-endepunkt til søgning
@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('keyword', '')  # Hent søgeterm fra forespørgslen
    results = query_database(search_term)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
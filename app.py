import sqlite3

def query_database(search_term):
    # Opret forbindelse til databasen
    conn = sqlite3.connect('babyfoodlabels.db')
    conn.row_factory = sqlite3.Row  # For at få resultater som dictionaries
    cursor = conn.cursor()
    
    # SQL-forespørgsel for at kombinere babyfoodlabels, stores og healthiness-tabellerne
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
            babyfoodlabels.product LIKE ? OR 
            store.name LIKE ?
    """
    
    # Udfør forespørgslen med søgetermen (brug wildcard for LIKE)
    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    
    # Hent resultaterne
    results = cursor.fetchall()
    
    # Luk forbindelsen
    conn.close()
    
    # Returner resultater som en liste af dictionaries
    return [dict(row) for row in results]
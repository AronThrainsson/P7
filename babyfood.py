import sqlite3

# Opret forbindelse til SQLite-databasen
conn = sqlite3.connect("babyfood.db")
cursor = conn.cursor()

# Opret Brands-tabellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS Brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Opret Products-tabellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand_id INTEGER NOT NULL,
    category TEXT NOT NULL,  -- Breakfast, Lunch, or Dinner
    kcal INT NOT NULL,
    heavy_metals TEXT,
    pesticides TEXT,
    FOREIGN KEY (brand_id) REFERENCES Brands (id)
)
""")

# Liste over babybrands
brands = [
    "Little Spoon", "Healthy Baby", "Once Upon a Farm", "Serenity Kids Baby",
    "Baby Gourmet", "Gerber", "Plum Organics", "Beech-Nut",
    "Happy Baby", "Cerebelly"
]

# Produkter med kategorier, kcal, tungmetaller og pesticider
products = {
    "Little Spoon": [
        ("Butternut Squash Pear Blend", "Breakfast", 90, "Lead: <20 ppb", "None"),
        ("Carrot Apple Ginger Purée", "Lunch", 80, "Lead: <20 ppb", "None"),
        ("Spinach Mango Banana Blend", "Dinner", 85, "None", "None"),
        ("Blueberry Chickpea Quinoa Purée", "Breakfast", 95, "Lead: <20 ppb", "None"),
        ("Sweet Potato Apple Blend", "Dinner", 100, "Arsenic: <20 ppb", "None")
    ],
    "Healthy Baby": [
        ("Organic Apple Cinnamon Oatmeal", "Breakfast", 110, "Lead: <10 ppb", "Traces"),
        ("Quinoa Banana Mango Purée", "Lunch", 120, "None", "None"),
        ("Organic Vegetable Medley", "Dinner", 130, "None", "None"),
        ("Pear Kale Spinach Blend", "Breakfast", 100, "None", "None"),
        ("Organic Brown Rice Cereal", "Dinner", 150, "Arsenic: <15 ppb", "None")
    ],
    "Once Upon a Farm": [
        ("Wild Rumpus Avocado", "Breakfast", 95, "Lead: <10 ppb", "None"),
        ("Green Kale & Apples", "Lunch", 90, "None", "None"),
        ("Magic Velvet Mango", "Dinner", 85, "None", "None"),
        ("OhMyMega Veggie", "Lunch", 100, "None", "Traces"),
        ("Strawberry Patch", "Breakfast", 80, "None", "None")
    ],
    "Serenity Kids Baby": [
        ("Organic Savory Beef with Vegetables", "Lunch", 120, "Lead: <10 ppb", "Traces"),
        ("Free-Range Chicken with Peas & Carrots", "Dinner", 130, "None", "None"),
        ("Wild-Caught Salmon with Butternut Squash", "Lunch", 125, "None", "Traces"),
        ("Grass-Fed Bison with Organic Kale", "Dinner", 140, "None", "None"),
        ("Pasture-Raised Turkey with Sweet Potato", "Lunch", 115, "None", "None")
    ],
    "Baby Gourmet": [
        ("Orchard Apple, Carrot & Prune Purée", "Breakfast", 100, "None", "None"),
        ("Banana, Apple & Blueberry Purée", "Lunch", 105, "Lead: <10 ppb", "None"),
        ("Sweet Potato, Apple & Amaranth Purée", "Dinner", 110, "None", "None"),
        ("Juicy Pear & Garden Greens Purée", "Lunch", 95, "None", "Traces"),
        ("Vanilla Banana Berry Risotto", "Breakfast", 115, "None", "None")
    ]
}

# Indsæt brands i Brands-tabellen
for brand in brands:
    cursor.execute("INSERT INTO Brands (name) VALUES (?)", (brand,))

# Indsæt produkter i Products-tabellen
for brand, product_list in products.items():
    # Find brand_id
    cursor.execute("SELECT id FROM Brands WHERE name = ?", (brand,))
    brand_id = cursor.fetchone()[0]
    # Indsæt produkter for dette brand
    for product, category, kcal, heavy_metals, pesticides in product_list:
        cursor.execute("""
            INSERT INTO Products (name, brand_id, category, kcal, heavy_metals, pesticides)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product, brand_id, category, kcal, heavy_metals, pesticides))

# Gem ændringer og luk forbindelsen
conn.commit()
conn.close()

print("Database created and populated successfully.")

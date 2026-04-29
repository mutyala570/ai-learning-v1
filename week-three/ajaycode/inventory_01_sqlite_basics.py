import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row   # lets us do row["column_name"]
cur = conn.cursor()

cur.executescript("""
CREATE TABLE products (
    sku_id   TEXT PRIMARY KEY,
    sku_name TEXT NOT NULL,
    stock    INTEGER NOT NULL
);

CREATE TABLE suppliers (
    sku_id        TEXT PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    lead_time_days INTEGER NOT NULL,
    FOREIGN KEY (sku_id) REFERENCES products(sku_id)
);
""")

cur.executemany("INSERT INTO products VALUES (?, ?, ?)", [
    ("SKU-001", "Wireless Headphones", 200),
    ("SKU-002", "Paracetamol 500mg",   800),
    ("SKU-003", "Instant Noodles",    1200),
])

cur.executemany("INSERT INTO suppliers VALUES (?, ?, ?)", [
    ("SKU-001", "TechImports Ltd", 21),
    ("SKU-002", "MedSupply Co",     7),
    ("SKU-003", "FoodDist Pvt",     4),
])

conn.commit()

print(f"{'SKU':<10} {'Name':<25} {'Stock':>6} {'Lead (days)':>12} {'Supplier'}")
print("-" * 70)

rows = cur.execute("""
    SELECT p.sku_id, p.sku_name, p.stock,
           s.lead_time_days, s.supplier_name
    FROM   products p
    JOIN   suppliers s ON s.sku_id = p.sku_id
    ORDER  BY p.sku_id
""").fetchall()

for r in rows:
    print(f"{r['sku_id']:<10} {r['sku_name']:<25} {r['stock']:>6} {r['lead_time_days']:>12} {r['supplier_name']}")

def fetch_product(sku_id: str) -> dict | None:
    row = cur.execute(
        "SELECT p.*, s.lead_time_days, s.supplier_name "
        "FROM products p JOIN suppliers s ON s.sku_id = p.sku_id "
        "WHERE UPPER(p.sku_id) = UPPER(?)",
        (sku_id,)
    ).fetchone()
    return dict(row) if row else None

print("\nLookup SKU-002:", fetch_product("SKU-002"))
print("Lookup SKU-999:", fetch_product("SKU-999"))

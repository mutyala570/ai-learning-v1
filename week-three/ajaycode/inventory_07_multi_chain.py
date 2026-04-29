
import math
import sqlite3
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool

load_dotenv()

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.executescript("""
CREATE TABLE inventory (
    sku_id TEXT PRIMARY KEY, sku_name TEXT, category TEXT,
    current_stock REAL, service_level REAL
);
CREATE TABLE lead_time (
    sku_id TEXT PRIMARY KEY, lead_time_days REAL, supplier_name TEXT
);
CREATE TABLE demand (
    sku_id TEXT PRIMARY KEY, avg_daily_demand REAL
);
""")
cur.executemany("INSERT INTO inventory VALUES (?,?,?,?,?)", [
    ("SKU-001","Wireless Headphones","Electronics", 200, 98),
    ("SKU-002","Paracetamol 500mg",  "Pharma",      800, 99),
    ("SKU-005","Laptop 15-inch",     "Electronics",  50, 99),
])
cur.executemany("INSERT INTO lead_time VALUES (?,?,?)", [
    ("SKU-001", 21, "TechImports Ltd"),
    ("SKU-002",  7, "MedSupply Co"),
    ("SKU-005", 30, "GlobalTech"),
])
cur.executemany("INSERT INTO demand VALUES (?,?)", [
    ("SKU-001", 8), ("SKU-002", 40), ("SKU-005", 3),
])
conn.commit()

def fetch_sku(sku_id: str) -> dict | None:
    row = cur.execute("""
        SELECT i.*, l.lead_time_days, l.supplier_name, d.avg_daily_demand
        FROM inventory i
        JOIN lead_time l ON l.sku_id = i.sku_id
        JOIN demand d ON d.sku_id = i.sku_id
        WHERE UPPER(i.sku_id) = UPPER(?)
    """, (sku_id,)).fetchone()
    return dict(row) if row else None

@tool
def safety_stock_tool(avg_daily_demand: float, lead_time_days: float, service_level_pct: float) -> dict:
    """Compute safety stock and desired stock level with exact arithmetic."""
    z = {90: 1.28, 95: 1.65, 97: 2.05, 98: 2.05, 99: 2.33}.get(int(service_level_pct), 1.65)
    ss = round(z * math.sqrt(lead_time_days) * avg_daily_demand, 2)
    desired = round(avg_daily_demand * lead_time_days + ss, 2)
    return {"z_score": z, "safety_stock": ss, "desired_stock": desired}

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

compute_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an inventory planning expert.\n"
     "The calculations below were done by a trusted tool — do NOT redo them.\n"
     "Explain the result clearly and end with:\nDESIRED_STOCK: {desired_stock}"),
    ("human",
     "SKU: {sku_id} | {sku_name} ({category})\n"
     "Current Stock   : {current_stock}\n"
     "Lead Time       : {lead_time_days} days\n"
     "Daily Demand    : {avg_daily_demand} units/day\n"
     "Service Level   : {service_level}%\n\n"
     "Tool results:\n"
     "  Z-score       : {z_score}\n"
     "  Safety Stock  : {safety_stock}\n"
     "  Desired Stock : {desired_stock}"),
])
compute_chain = compute_prompt | llm | StrOutputParser()

reorder_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an inventory planning advisor.\n"
     "Reorder Quantity = max(0, Desired Stock - Current Stock).\n"
     "State the quantity and whether an immediate reorder is needed."),
    ("human",
     "SKU: {sku_id} | {sku_name}\n"
     "Current Stock: {current_stock}   Supplier: {supplier_name}\n\n"
     "Stock Computation:\n{computation}"),
])
reorder_chain = reorder_prompt | llm | StrOutputParser()

def run_pipeline(sku_id: str) -> None:
    record = fetch_sku(sku_id)
    if not record:
        print(f"SKU {sku_id} not found.")
        return

    # Step 1: exact arithmetic via tool
    tool_result = safety_stock_tool.invoke({
        "avg_daily_demand":  record["avg_daily_demand"],
        "lead_time_days":    record["lead_time_days"],
        "service_level_pct": record["service_level"],
    })
    print(f"\n[Tool] safety_stock_tool → {tool_result}")

    # Step 2: chain 1 — explain computation
    computation = compute_chain.invoke({**record, **tool_result})
    print(f"\n--- Chain 1: Stock Computation ---\n{computation}")

    # Step 3: chain 2 — reorder recommendation (consumes chain 1 output)
    recommendation = reorder_chain.invoke({
        "sku_id":        record["sku_id"],
        "sku_name":      record["sku_name"],
        "current_stock": record["current_stock"],
        "supplier_name": record["supplier_name"],
        "computation":   computation,
    })
    print(f"\n--- Chain 2: Reorder Recommendation ---\n{recommendation}")


# ── Run ───────────────────────────────────────────────────────────────────────
for sku in ["SKU-001", "SKU-005"]:
    print(f"\n{'='*60}")
    print(f"Processing {sku}")
    print("="*60)
    run_pipeline(sku)
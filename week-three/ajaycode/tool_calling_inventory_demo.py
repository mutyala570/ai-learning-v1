import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

INVENTORY = {
    "SKU-001": {"name": "Industrial Valve",    "stock": 120, "reorder_point": 50,  "unit_cost": 84.50},
    "SKU-002": {"name": "Hydraulic Pump",      "stock": 18,  "reorder_point": 25,  "unit_cost": 430.00},
    "SKU-003": {"name": "Conveyor Belt",       "stock": 5,   "reorder_point": 10,  "unit_cost": 210.75},
    "SKU-004": {"name": "Safety Helmet",       "stock": 300, "reorder_point": 100, "unit_cost": 12.00},
    "SKU-005": {"name": "Pressure Gauge",      "stock": 42,  "reorder_point": 40,  "unit_cost": 55.00},
}

DAILY_DEMAND = {
    "SKU-001": 8,
    "SKU-002": 3,
    "SKU-003": 2,
    "SKU-004": 15,
    "SKU-005": 6,
}


@tool
def get_stock_level(sku: str) -> str:
    """Return current stock level and reorder point for a given SKU."""
    item = INVENTORY.get(sku.upper())
    if not item:
        return f"SKU {sku} not found."
    status = "LOW" if item["stock"] <= item["reorder_point"] else "OK"
    return (
        f"{item['name']} ({sku}): stock={item['stock']}, "
        f"reorder_point={item['reorder_point']}, status={status}"
    )


@tool
def calculate_reorder_quantity(sku: str, lead_time_days: int = 7) -> str:
    """Calculate recommended reorder quantity for a SKU given supplier lead time in days."""
    item = INVENTORY.get(sku.upper())
    if not item:
        return f"SKU {sku} not found."
    daily = DAILY_DEMAND.get(sku.upper(), 1)
    safety_stock = daily * lead_time_days
    reorder_qty = (daily * lead_time_days * 2) - item["stock"]
    reorder_qty = max(reorder_qty, 0)
    total_cost = reorder_qty * item["unit_cost"]
    return (
        f"{item['name']} ({sku}): recommend ordering {reorder_qty} units "
        f"(safety_stock={safety_stock}, lead_time={lead_time_days}d, "
        f"estimated_cost=${total_cost:,.2f})"
    )


@tool
def days_until_stockout(sku: str) -> str:
    """Estimate how many days until a SKU runs out of stock at current demand rate."""
    item = INVENTORY.get(sku.upper())
    if not item:
        return f"SKU {sku} not found."
    daily = DAILY_DEMAND.get(sku.upper(), 1)
    days = item["stock"] / daily
    return (
        f"{item['name']} ({sku}): {days:.1f} days until stockout "
        f"(stock={item['stock']}, daily_demand={daily})"
    )


@tool
def list_low_stock_items() -> str:
    """List all SKUs that are at or below their reorder point and need restocking."""
    low = [
        f"{sku} ({item['name']}): stock={item['stock']}, reorder_point={item['reorder_point']}"
        for sku, item in INVENTORY.items()
        if item["stock"] <= item["reorder_point"]
    ]
    if not low:
        return "All items are adequately stocked."
    return f"Items needing reorder ({len(low)} total): " + "; ".join(low)


def chat_with_tools(user_message: str) -> str:
    messages = [HumanMessage(content=user_message)]

    response = llm_with_tools.invoke(messages)
    messages.append(response)

    if response.tool_calls:
        for tc in response.tool_calls:
            result = tool_map[tc["name"]].invoke(tc["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))

        final_response = llm_with_tools.invoke(messages).content
    else:
        final_response = response.content

    return final_response


tools = [get_stock_level, calculate_reorder_quantity, days_until_stockout, list_low_stock_items]
tool_map = {t.name: t for t in tools}

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools(tools)

response_1 = chat_with_tools("What is the current stock level for SKU-003?")
response_2 = chat_with_tools("Which items need to be reordered right now?")
response_3 = chat_with_tools("How many days until SKU-002 runs out of stock?")
response_4 = chat_with_tools("What quantity of SKU-003 should I order if my supplier takes 10 days to deliver?")

print(response_1)
print(response_2)
print(response_3)
print(response_4)

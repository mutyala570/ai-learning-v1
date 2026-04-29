
import json
import math
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

load_dotenv()

# ── Tool definitions ──────────────────────────────────────────────────────────

@tool
def calculate_safety_stock(avg_daily_demand: float, lead_time_days: float, service_level_pct: float) -> float:
    """
    Calculate safety stock using the standard formula.
    safety_stock = Z * sqrt(lead_time_days) * avg_daily_demand
    Z-scores: 90%->1.28, 95%->1.65, 98%->2.05, 99%->2.33
    """
    z_map = {90: 1.28, 95: 1.65, 97: 2.05, 98: 2.05, 99: 2.33}
    z = z_map.get(int(service_level_pct), 1.65)
    return round(z * math.sqrt(lead_time_days) * avg_daily_demand, 2)


@tool
def calculate_reorder_point(avg_daily_demand: float, lead_time_days: float, safety_stock: float) -> float:
    """
    Calculate the reorder point (ROP).
    ROP = (avg_daily_demand * lead_time_days) + safety_stock
    """
    return round(avg_daily_demand * lead_time_days + safety_stock, 2)


@tool
def lookup_sku_stock(sku_id: str) -> dict:
    """
    Look up current stock and demand parameters for a SKU from the inventory database.
    Returns: sku_id, sku_name, current_stock, avg_daily_demand, lead_time_days, service_level
    """
    # Simulated DB
    db = {
        "SKU-001": {"sku_name": "Wireless Headphones", "current_stock": 200, "avg_daily_demand": 8,  "lead_time_days": 21, "service_level": 98},
        "SKU-002": {"sku_name": "Paracetamol 500mg",   "current_stock": 800, "avg_daily_demand": 40, "lead_time_days":  7, "service_level": 99},
        "SKU-005": {"sku_name": "Laptop 15-inch",       "current_stock":  50, "avg_daily_demand":  3, "lead_time_days": 30, "service_level": 99},
    }
    record = db.get(sku_id.upper())
    if not record:
        return {"error": f"{sku_id} not found"}
    return {"sku_id": sku_id.upper(), **record}


# ── LLM with tools bound ──────────────────────────────────────────────────────
tools = [calculate_safety_stock, calculate_reorder_point, lookup_sku_stock]
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0).bind_tools(tools)

# Map tool name → callable for the dispatch loop
TOOL_MAP = {t.name: t for t in tools}

# ── Simple agent loop ─────────────────────────────────────────────────────────
def run_agent(user_question: str) -> str:
    """Run a single-turn tool-calling agent loop."""
    messages = [HumanMessage(content=user_question)]

    while True:
        response = llm.invoke(messages)
        messages.append(response)

        # No tool calls → final answer
        if not response.tool_calls:
            return response.content

        # Dispatch each tool call
        for tc in response.tool_calls:
            print(user_question)
            print(tc["name"], "\n\n")
            fn = TOOL_MAP[tc["name"]]
            result = fn.invoke(tc["args"])
            messages.append(ToolMessage(
                content=json.dumps(result),
                tool_call_id=tc["id"],
            ))
            print(f"  [tool] {tc['name']}({tc['args']}) → {result}")


# ── Try it ────────────────────────────────────────────────────────────────────
questions = [
    "What is the safety stock for SKU-001?",
    "Does SKU-005 need to be reordered? Show the reorder point.",
    "Calculate the reorder point for an item with daily demand of 60, lead time 5 days, and 95% service level.",
]

for q in questions:
    print(f"\nQ: {q}")
    answer = run_agent(q)
    print(f"A: {answer}")
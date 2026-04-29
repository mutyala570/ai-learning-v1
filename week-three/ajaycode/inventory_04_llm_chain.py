
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an inventory planning expert.

Given these parameters, compute the desired stock level step by step.

Formulas:
  Safety Stock  = Z * sqrt(lead_time_days) * avg_daily_demand
  Desired Stock = (avg_daily_demand * lead_time_days) + Safety Stock

Z-scores: 90% → 1.28 | 95% → 1.65 | 98% → 2.05 | 99% → 2.33

End your response with exactly:
DESIRED_STOCK: <number>"""),
    ("human",
     "SKU: {sku_id} ({sku_name})\n"
     "Lead Time  : {lead_time_days} days\n"
     "Daily Demand: {avg_daily_demand} units/day\n"
     "Service Level: {service_level}%"),
])

chain = prompt | llm | StrOutputParser()

test_cases = [
    {"sku_id": "SKU-001", "sku_name": "Wireless Headphones", "lead_time_days": 21, "avg_daily_demand": 8,  "service_level": 98},
    {"sku_id": "SKU-003", "sku_name": "Instant Noodles",     "lead_time_days":  4, "avg_daily_demand": 80, "service_level": 95},
]

for params in test_cases:
    print(f"\n{'='*60}")
    print(f"SKU: {params['sku_id']} — {params['sku_name']}")
    print("="*60)
    result = chain.invoke(params)
    print(result)

import chromadb
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# ── Build the vector store (same as snippet 03) ───────────────────────────────
embed = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

client = chromadb.Client()
col = client.create_collection("inv_kb", metadata={"hnsw:space": "cosine"})

KB = [
    ("ss",  "Safety Stock = Z * sqrt(lead_time) * avg_daily_demand. Z=1.65 for 95%, Z=2.33 for 99%."),
    ("rop", "Reorder Point (ROP) = (avg_daily_demand * lead_time) + Safety Stock."),
    ("elec","Electronics: lead times 14-30 days, high obsolescence risk."),
    ("ph",  "Pharma: 99%+ service level, strict FIFO, expiry dates matter."),
    ("slv", "Raising service level from 95% to 99% roughly doubles safety stock."),
    ("var", "High demand variability requires more safety stock for the same service level."),
]
vecs = embed.embed_documents([t for _, t in KB])
col.add(ids=[i for i, _ in KB], embeddings=vecs, documents=[t for _, t in KB])

def retrieve_context(query: str, n: int = 3) -> str:
    qv = embed.embed_query(query)
    res = col.query(query_embeddings=[qv], n_results=n)
    return "\n".join(f"- {c}" for c in res["documents"][0])

# ── Chain WITHOUT RAG ─────────────────────────────────────────────────────────
bare_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an inventory planning expert. Advise on reorder strategy."),
    ("human",
     "SKU: {sku_name} | Category: {category}\n"
     "Current Stock: {current_stock} | Lead Time: {lead_time_days} days\n"
     "Daily Demand: {avg_daily_demand} | Service Level: {service_level}%"),
])

# ── Chain WITH RAG ────────────────────────────────────────────────────────────
rag_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an inventory planning expert. Advise on reorder strategy.\n\n"
     "Relevant domain knowledge:\n{rag_context}"),
    ("human",
     "SKU: {sku_name} | Category: {category}\n"
     "Current Stock: {current_stock} | Lead Time: {lead_time_days} days\n"
     "Daily Demand: {avg_daily_demand} | Service Level: {service_level}%"),
])

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
parser = StrOutputParser()

bare_chain = bare_prompt | llm | parser
rag_chain  = rag_prompt  | llm | parser

# ── Run comparison ────────────────────────────────────────────────────────────
sku = {
    "sku_name":         "Paracetamol 500mg",
    "category":         "Pharma",
    "current_stock":    800,
    "lead_time_days":   7,
    "avg_daily_demand": 40,
    "service_level":    99,
}

# Retrieve relevant context for this SKU
query = f"{sku['category']} inventory reorder safety stock {sku['service_level']}%"
context = retrieve_context(query)

print("=== Retrieved Context ===")
print(context)

print("\n=== Response WITHOUT RAG ===")
print(bare_chain.invoke(sku))

print("\n=== Response WITH RAG ===")
print(rag_chain.invoke({**sku, "rag_context": context}))
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
#  pip3 install chromadb langchain-huggingface 
# abve line is to install the libraries for vector db and langchain huggingface embeddings

embed = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

client = chromadb.Client()
collection = client.create_collection("inventory_kb", metadata={"hnsw:space": "cosine"})

docs = [
    {"id": "ss-formula",   "text": "Safety Stock = Z * sqrt(lead_time) * avg_daily_demand. Z=1.65 for 95%, Z=2.33 for 99%.", "meta": {"topic": "formula"}},
    {"id": "rop-formula",  "text": "Reorder Point (ROP) = (avg_daily_demand * lead_time) + safety_stock.",                   "meta": {"topic": "formula"}},
    {"id": "electronics",  "text": "Electronics: lead times 14-30 days, service level 95-99%, high obsolescence risk.",       "meta": {"topic": "category"}},
    {"id": "pharma",       "text": "Pharma: lead times 7-21 days, service level 99%+, strict FIFO and expiry management.",   "meta": {"topic": "category"}},
    {"id": "fmcg",         "text": "FMCG: lead times 3-7 days, high steady demand, service level 95-98%.",                   "meta": {"topic": "category"}},
    {"id": "raw-mat",      "text": "Raw materials: lead times 10-45 days, service level 90-95%.",                             "meta": {"topic": "category"}},
    {"id": "abc",          "text": "ABC Analysis: A-items need tight control and high service levels.",                        "meta": {"topic": "best_practice"}},
    {"id": "variability",  "text": "High demand variability requires more safety stock to maintain service level.",            "meta": {"topic": "best_practice"}},
]

print("Embedding and storing documents...")
vectors = embed.embed_documents([d["text"] for d in docs])#this ths the vector db call
collection.add(
    ids=[d["id"] for d in docs],
    embeddings=vectors,
    documents=[d["text"] for d in docs],
    metadatas=[d["meta"] for d in docs],
)
print(f"Collection has {collection.count()} documents\n")

def retrieve(query: str, n: int = 3, where: dict | None = None) -> list[str]:
    qv = embed.embed_query(query)
    kwargs = {"query_embeddings": [qv], "n_results": n}
    if where:
        kwargs["where"] = where
    results = collection.query(**kwargs)
    return results["documents"][0]

print("=== Query: 'pharma reorder safety stock' ===")
for chunk in retrieve("pharma reorder safety stock"):
    print(" •", chunk)

print()

print("=== Query: 'how to calculate stock' (formulas only) ===")
for chunk in retrieve("how to calculate stock", where={"topic": "formula"}):
    print(" •", chunk)

print()

print("=== Query: 'electronics inventory management' (category only) ===")
for chunk in retrieve("electronics inventory management", where={"topic": "category"}):
    print(" •", chunk)

# ─────────────────────────────────────────────────────────────────────────────
# RAG retrieval demo — uses TWO libraries doing TWO different jobs:
#   • sentence-transformers (via langchain_huggingface) → turns text into vectors
#   • chromadb                                          → stores vectors and runs fast nearest-neighbour search
# ─────────────────────────────────────────────────────────────────────────────

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
#  pip3 install chromadb langchain-huggingface
# abve line is to install the libraries for vector db and langchain huggingface embeddings

# ─── EMBEDDING MODEL (sentence-transformers) ─────────────────────────────────
# The "translator". Takes any string → returns a 384-number vector.
# Used for both: (a) embedding the docs once at startup
#                (b) embedding each incoming query at search time.
embed = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},  # forces every vector to length 1 → dot product = cosine similarity
)

# ─── VECTOR DATABASE (ChromaDB) ──────────────────────────────────────────────
# The "smart filing cabinet". Holds vectors + metadata, runs HNSW
# nearest-neighbour search, supports metadata filtering. NO embedding model
# inside — we feed it vectors produced by the embedder above.
#
# What ChromaDB adds over raw NumPy (file 02):
#   1. Indexed search (HNSW) — finds nearest neighbours in O(log n) instead of
#      brute-force O(n). Critical when the corpus grows past a few thousand docs.
#   2. Metadata filtering — where={"topic": "formula"} restricts the search to
#      docs tagged as formulas. NumPy can't do this without manual filtering code.
#   3. Persistent storage — Chroma can save vectors to disk; restart the script
#      and they're still there. NumPy arrays disappear when the process ends.
#   4. Production patterns — distance metrics, batch operations, collections,
#      schema migration, hybrid search, etc., out of the box.
client = chromadb.Client()
collection = client.create_collection("inventory_kb", metadata={"hnsw:space": "cosine"})  # score by cosine similarity

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

# STEP 1 — EMBEDDER's job: turn each doc's text into a 384-dim vector.
# (NOT a vector DB call — this is sentence-transformers running locally on CPU.)
vectors = embed.embed_documents([d["text"] for d in docs])

# STEP 2 — VECTOR DB's job: store the vectors + ids + raw text + metadata.
# After this line, ChromaDB has 8 vectors indexed and searchable.
collection.add(
    ids=[d["id"] for d in docs],
    embeddings=vectors,
    documents=[d["text"] for d in docs],
    metadatas=[d["meta"] for d in docs],
)
print(f"Collection has {collection.count()} documents\n")


def retrieve(query: str, n: int = 3, where: dict | None = None) -> list[str]:
    # STEP 1 — EMBEDDER: turn the user's question into a 384-dim vector.
    # MUST use the same model the docs were embedded with — different models
    # produce incomparable vector spaces.
    qv = embed.embed_query(query)

    # STEP 2 — Build the search query for ChromaDB.
    kwargs = {"query_embeddings": [qv], "n_results": n}
    if where:
        # Optional metadata filter — restricts the search to docs whose metadata matches.
        # e.g. where={"topic": "formula"} → only the 2 formula docs are searched, not all 8.
        kwargs["where"] = where

    # STEP 3 — VECTOR DB: nearest-neighbour search (HNSW algorithm + cosine similarity).
    # Returns the top-n most similar documents, optionally narrowed by the metadata filter.
    results = collection.query(**kwargs)
    return results["documents"][0]


# ─── Query 1 — no filter: search across ALL 8 docs ───────────────────────────
print("=== Query: 'pharma reorder safety stock' ===")
for chunk in retrieve("pharma reorder safety stock"):
    print(" •", chunk)

print()

# ─── Query 2 — metadata filter: only the formula docs ────────────────────────
print("=== Query: 'how to calculate stock' (formulas only) ===")
for chunk in retrieve("how to calculate stock", where={"topic": "formula"}):
    print(" •", chunk)

print()

# ─── Query 3 — metadata filter: only the category docs ───────────────────────
print("=== Query: 'electronics inventory management' (category only) ===")
for chunk in retrieve("electronics inventory management", where={"topic": "category"}):
    print(" •", chunk)

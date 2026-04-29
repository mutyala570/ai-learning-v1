
import numpy as np
from sentence_transformers import SentenceTransformer
# pip3 install sentence-transformers 
#install above line in terminal to get the library for sentence embedding.

# after i run this file got this KeyError: 'sentence-transformers/all-MiniLM-L6-v2'
# to fix that 
# 1.pip3 install "numpy<2"
# 2.pip3 install "sentence-transformers<3" "transformers<4.45"  
# after this it run this file sucessully

PASSAGES = [
    "Safety Stock = Z-score * sqrt(lead_time) * avg_daily_demand",
    "Reorder Point = (avg_daily_demand * lead_time) + safety_stock",
    "Electronics: lead times 14-30 days, high obsolescence risk.",
    "Pharma: strict FIFO, 99%+ service level, expiry management.",
    "FMCG: short lead times 3-7 days, high steady demand.",
    "ABC Analysis: A-items need tight control, C-items tolerate bulk orders.",
]

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print("Embedding passages...")
passage_vectors = model.encode(PASSAGES, normalize_embeddings=True)#6 vectors here  
print(f"Passage matrix shape: {passage_vectors.shape}\n")

#need to ask claude for the explanation
def top_k(query: str, k: int = 3) -> list[tuple[float, str]]:
    qv = model.encode(query, normalize_embeddings=True)
    scores = passage_vectors @ qv          # shape: (num_passages,)
    ranked = np.argsort(scores)[::-1][:k]
    return [(float(scores[i]), PASSAGES[i]) for i in ranked]

queries = [
    "How do I calculate safety stock?",
    "What should I know about electronics inventory?",
    "Tell me about demand patterns for consumer goods.",
]

for query in queries:
    print(f"Query: {query!r}")
    for score, passage in top_k(query):
        print(f"  {score:.3f}  {passage}")
    print()



    #  scores = passage_vectors @ qv       this line is not scalable so thay chosse vecotr db 03 file



    # i need to ask this how it gave that answers

#     Query: 'How do I calculate safety stock?'
#   0.594  Safety Stock = Z-score * sqrt(lead_time) * avg_daily_demand
#   0.493  Reorder Point = (avg_daily_demand * lead_time) + safety_stock
#   0.195  ABC Analysis: A-items need tight control, C-items tolerate bulk orders.

# Query: 'What should I know about electronics inventory?'
#   0.403  Electronics: lead times 14-30 days, high obsolescence risk.
#   0.321  ABC Analysis: A-items need tight control, C-items tolerate bulk orders.
#   0.262  Safety Stock = Z-score * sqrt(lead_time) * avg_daily_demand

# Query: 'Tell me about demand patterns for consumer goods.'
#   0.332  ABC Analysis: A-items need tight control, C-items tolerate bulk orders.
#   0.291  FMCG: short lead times 3-7 days, high steady demand.
#   0.231  Safety Stock = Z-score * sqrt(lead_time) * avg_daily_demand
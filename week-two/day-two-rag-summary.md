# Week 2 — Day 2: RAG Summary — Key Design Questions

A high-level recap of everything covered in `day-two-rag-architecture.md`, organized around the six design questions any team has to answer when building a RAG system. Each section is a one-paragraph summary plus the sub-topics that sit inside it, with pointers back to the slide where the full explanation lives.

## Topics Covered in This Document

1. [**Query Preprocessing**](#1-query-preprocessing)
2. [**Which Embedding Model to Use**](#2-which-embedding-model-to-use)
3. [**What is My Chunking Strategy**](#3-what-is-my-chunking-strategy)
4. [**Which Vector DB to Choose**](#4-which-vector-db-to-choose)
5. [**What Should Be My Retrieval Strategy**](#5-what-should-be-my-retrieval-strategy)
6. [**How to Evaluate the RAG System**](#6-how-to-evaluate-the-rag-system)

---

## 1. Query Preprocessing

**Covered in:** Slide 13.

Raw user queries are messy — they have typos, are too vague, use different vocabulary than the documents, or may even be unsafe to run. Query preprocessing is the set of fixes applied before the query reaches the retriever, and it is the cheapest place to improve retrieval quality.

- **Query classification** — decide what kind of question it is (popular vs long tail, broad vs narrow, factual vs reasoning) so the right retrieval path can be chosen.
- **Query cleaning and rewriting** — remove special characters, fix typos, apply lemmatization and stemming, optionally use step-back prompting to broaden the question before searching.
- **Query expansion** — enrich the query with synonyms or use **HyDE** (generate a hypothetical answer with an LLM, embed that, and use its vector as the search query).
- **Policy and safety check** — profanity filter, PII redaction, and topic relevance check before the query is allowed to reach the retriever or LLM.

**One-liner:** classify → clean → expand → safety-check.

---

## 2. Which Embedding Model to Use

**Covered in:** Slide 14.

The embedding model turns both documents and queries into vectors, so it is the heart of the retriever. There is no single best model — the right pick is the one that balances five factors against your use case. Changing the embedding model later is expensive because the whole corpus has to be re-embedded, so this decision is worth making carefully up front.

- **Relevance** — how accurately the model ranks the truly relevant chunks at the top for *your* queries. Measured on a small golden set with Recall@k and NDCG@k.
- **Domain specificity** — general-purpose models work for generic text but often fail on specialized domains (law, medicine, finance) where domain-tuned models (`LegalBERT`, `BioBERT`, `FinBERT`) retrieve better.
- **Performance vs cost** — bigger models retrieve better but cost more in storage (vector dimensions) and latency (inference time). A mid-tier model plus a reranker usually beats a giant model used alone.
- **Language support** — multilingual corpora require multilingual models (e.g. `multilingual-e5`); using an English-only model on multilingual data is a common silent failure.
- **Hosting** — API-based (OpenAI, Cohere, Voyage) for convenience, self-hosted open-source (`bge`, `nomic-embed`, `jina-embeddings`) for control and data privacy.

**One-liner:** pick the model that retrieves well on your data, fits your domain, fits your budget, speaks your languages, and runs where your data is allowed to live.

---

## 3. What is My Chunking Strategy

**Covered in:** Slides 9, 10, 11, 12.

Long documents have to be broken into smaller pieces before embedding. The chunking strategy decides both *how* to cut (fixed, semantic, recursive) and *when* to cut (before or after embedding). Bad chunking silently caps retrieval quality no matter how good the rest of the stack is.

- **Fixed size chunking** (Slide 9) — cuts every N tokens with a small overlap. Simple and fast, but can cut mid-sentence.
- **Semantic chunking** (Slide 10) — groups sentences into chunks based on embedding similarity and cuts when the topic shifts. More accurate but threshold tuning is tricky.
- **Recursive chunking** (Slide 11) — cuts at natural boundaries first (paragraph → sentence → word) and only goes deeper if the chunk is still too big. Common production default.
- **Naive vs late chunking** (Slide 12) — naive = chunk first then embed each chunk independently (context between chunks is lost). Late = embed the whole document first, then cut the token embeddings into chunks (context is preserved, but requires a long-context embedding model).

**One-liner:** recursive chunking is the default; reach for semantic or late chunking when cross-chunk context matters.

---

## 4. Which Vector DB to Choose

**Covered in:** Slide 15 (class discussion).

Once vectors exist, they need somewhere to be stored and searched fast. The choice is between renting a managed service, self-hosting an open-source system for prototyping, or self-hosting one for production.

- **Pinecone** — Fully managed SaaS. Handles billions of vectors with zero DevOps effort. Easy to use, low latency, high throughput. Trade-off: paid, and data lives on their infrastructure.
- **Chroma** — Open-source, Python-native, simple to start with. Ideal for prototyping and R&D up to ~10M vectors. Not built for massive scale.
- **Qdrant** — Open-source, production-grade. Scales to billions of vectors with low latency and high throughput. Slightly more complex to run than Chroma because of its production features.

**One-liner:** Chroma for building, Pinecone for renting, Qdrant for owning.

---

## 5. What Should Be My Retrieval Strategy

**Covered in:** Slides 3, 4, 5, 6.

Retrieval decides which documents get fed to the LLM. The strategy depends on whether the data is structured (rows in a SQL table) or unstructured (free-text documents), and on whether the user's wording will literally match the documents.

- **Tabular retrieval / Text-to-SQL** (Slide 4) — for structured data. The LLM turns the question into SQL, the SQL engine computes the answer, and the LLM turns the result into a readable sentence.
- **Term-based retrieval (BM25)** (Slide 5) — classical keyword matching. Fast and exact, great for product codes, technical keywords, and rare entity names. Fails on synonyms and paraphrasing.
- **Embedding-based retrieval** (Slide 6) — semantic search using cosine similarity between query and document vectors. Handles synonyms and paraphrasing but can miss exact-match keywords.
- **Hybrid search** (Slide 6) — combines BM25 and embedding-based retrieval and merges the results. Usually the best choice in production because it keeps the strengths of both.

**One-liner:** SQL for rows, BM25 for exact terms, embeddings for meaning — and hybrid when both matter.

---

## 6. How to Evaluate the RAG System

**Covered in:** Slide 7.

Retrieval quality has to be measured before anything else can be tuned. Evaluation is an **offline** activity done with a golden set of queries and known-correct answers — not on live production traffic. The four standard metrics split into two families based on whether ranking order matters.

- **Precision** (set-based) — of the chunks I retrieved, how many were actually relevant?
- **Recall** (set-based) — of all the relevant chunks that exist, how many did I retrieve? In RAG, **Recall@k** is the key metric — did the relevant chunks make it into the prompt at all?
- **MRR — Mean Reciprocal Rank** (rank-aware) — how high is the *first* relevant result? Best for single-answer Q&A and chatbots.
- **NDCG — Normalized Discounted Cumulative Gain** (rank-aware) — scores the entire ranked list, weighting higher positions more. Best when the whole top-k matters (search, recommendations, RAG).

In production, these offline metrics are wrapped into higher-level measures like **Context Precision** and **Context Recall** (frameworks like RAGAS), typically judged by an LLM against the golden set.

**One-liner:** Precision / Recall for coarse quality, MRR for top-1 questions, NDCG for full-ranking quality, all run offline on a golden set.

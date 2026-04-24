# Week 2 — Day 2: RAG Architecture (Video 2)

## Slides Covered in This Document

### Slide 1 — Retrieval Augmented Generation (Overview)
1. [**What RAG Stands For**](#what-rag-stands-for)
2. [**The Core Idea in One Line**](#the-core-idea-in-one-line)
3. [**The Four Main Components**](#the-four-main-components)
4. [**End-to-End Flow**](#end-to-end-flow)
5. [**Why Context Augmentation is the Key Step**](#why-context-augmentation-is-the-key-step)
6. [**Without RAG vs With RAG**](#without-rag-vs-with-rag)

### Slide 2 — Limitations of LLM
1. [**No Access to Proprietary Data**](#no-access-to-proprietary-data)
2. [**Training Cutoff**](#training-cutoff)
3. [**Hallucinations**](#hallucinations)
4. [**Long Tail Entity Recall**](#long-tail-entity-recall)
5. [**How These Limitations Map to RAG**](#how-these-limitations-map-to-rag)

### Slide 3 — Retrieval: Getting Data Out of Database
1. [**The Retrieval Problem**](#the-retrieval-problem)
2. [**Query Pre-Processing**](#query-pre-processing)
3. [**Key Questions in Retrieval**](#key-questions-in-retrieval)
4. [**Types of Retrieval**](#types-of-retrieval)

### Slide 4 — Retrieving Tabular Data (Text-to-SQL)
1. [**What Tabular Retrieval Is**](#what-tabular-retrieval-is)
2. [**End-to-End Flow**](#end-to-end-flow-tabular)
3. [**Why the LLM Is Used Twice**](#why-the-llm-is-used-twice)
4. [**When to Use This Pattern**](#when-to-use-this-pattern)

### Slide 5 — Term-Based Retrieval
1. [**Key Idea**](#key-idea-term-based)
2. [**The Common-Word Problem**](#the-common-word-problem)
3. [**BM25**](#bm25)
4. [**Limitation: Literal Matching**](#limitation-literal-matching)

### Slide 6 — Embedding-Based Retrieval
1. [**Key Idea**](#key-idea-embedding-based)
2. [**Indexing Flow (Offline)**](#indexing-flow-offline)
3. [**Query Flow (Runtime)**](#query-flow-runtime)
4. [**Cosine Similarity**](#cosine-similarity)
5. [**Why This Beats Term-Based**](#why-this-beats-term-based)
6. [**Trade-Offs and Hybrid Search**](#trade-offs-and-hybrid-search)

### Slide 7 — Retrieval Evaluation Metrics (Precision, Recall, MRR, NDCG)
*MRR = Mean Reciprocal Rank · NDCG = Normalized Discounted Cumulative Gain*
1. [**The Family Tree**](#the-family-tree)
2. [**When to Use Which**](#when-to-use-which)
3. [**Where These Metrics Fit in the RAG Lifecycle**](#where-these-metrics-fit-in-the-rag-lifecycle)

### Slide 8 — Developer Decisions When Building a RAG System
1. [**Ingestion Decisions**](#ingestion-decisions)
2. [**Storage Decisions**](#storage-decisions)
3. [**Retrieval Decisions**](#retrieval-decisions)
4. [**Generation Decisions**](#generation-decisions)

### Slide 9 — Chunking Strategies: Fixed Size Chunking
1. [**How Fixed Size Chunking Works**](#how-fixed-size-chunking-works)
2. [**Chunk Size and Overlap**](#chunk-size-and-overlap)
3. [**Fixed Size: Pros and Cons**](#fixed-size-pros-and-cons)

### Slide 10 — Chunking Strategies: Semantic Chunking
1. [**How Semantic Chunking Works**](#how-semantic-chunking-works)
2. [**Semantic: Pros and Cons**](#semantic-pros-and-cons)

### Slide 11 — Chunking Strategies: Recursive Chunking
1. [**How Recursive Chunking Works**](#how-recursive-chunking-works)
2. [**Recursive: Pros and Cons**](#recursive-pros-and-cons)

---

# Slide 1 — Retrieval Augmented Generation (Overview)

This slide introduces the basic RAG architecture — the simplest form of the pattern, before any optimizations like rerankers or hybrid search are added. It shows how a user query flows through a database, gets combined with retrieved knowledge, and is sent to the LLM to produce a grounded answer.

## What RAG Stands For

RAG stands for **Retrieval Augmented Generation**. It is a design pattern that gives a Large Language Model (LLM) access to external knowledge at the time of answering a question. The LLM does not need to memorize the knowledge during training. Instead, the system fetches the relevant information on demand and hands it to the model as part of the prompt.

Breaking the name apart makes the idea clear:

- **Retrieval** — pull relevant documents from a knowledge source.
- **Augmented** — add those documents to the user's original question to build a richer prompt.
- **Generation** — the LLM reads that richer prompt and generates an answer grounded in those documents.

## The Core Idea in One Line

> **Retrieve external knowledge → feed it to the LLM along with the user query.**

Everything else in RAG — chunking, embeddings, vector databases, rerankers — exists to make this one sentence work well at scale.

## The Four Main Components

The basic RAG architecture has four building blocks. Each has a clear, single responsibility.

### User Query

This is the question the user types in plain language, such as "What is the refund policy for late deliveries?". The query is used in two places at the same time:

1. It is sent to the database to find documents that relate to the question.
2. It is passed forward to the LLM, so the model knows what the user actually asked.

This dual use is why the diagram shows two arrows leaving the User Query.

### Database (Knowledge Source)

The database stores the external knowledge that the LLM will rely on. In production RAG systems, this is almost always a **vector database** (for example Chroma, Qdrant, or Pinecone), not a traditional relational database.

Before any query happens, documents are prepared offline:

- **Chunking** — break long documents into smaller pieces that fit inside the LLM's context window.
- **Embedding** — convert each chunk into a numeric vector using an embedding model.
- **Storing** — save those vectors along with metadata (source, chunk id, timestamps) into the vector DB.

This preparation is a one-time or incremental cost. Once done, retrieval at query time becomes a fast similarity lookup.

### Retrieval

When the user query arrives, the retrieval step does the following:

1. Convert the query into a vector using the same embedding model used for the documents.
2. Search the vector database for the chunks whose vectors are closest to the query vector. Closeness is typically measured using **cosine similarity** or **dot product**.
3. Return the top-k most similar chunks (for example, the top 5 or top 10).

The output of this step is a small set of documents that are most likely to contain the answer. These documents are the external knowledge that will be added to the prompt.

### Context Augmentation

Context augmentation is the step that turns a plain question into a grounded prompt. It takes the retrieved documents and the original user query and combines them into a single prompt for the LLM.

A common shape for this prompt is:

```
Use the following context to answer the question.
If the answer is not in the context, say you do not know.

Context:
<retrieved chunk 1>
<retrieved chunk 2>
<retrieved chunk 3>

Question: <user query>
```

This merged prompt is what the LLM actually receives. It is no longer a bare question — it is a question plus the facts needed to answer it.

### LLM Model

The LLM reads the augmented prompt and generates the final answer. Because the prompt contains both the question and the supporting context, the model is steered toward an answer that is grounded in the retrieved documents rather than in its training data alone.

The output of the LLM is the **Response** that is returned to the user.

## End-to-End Flow

Putting the pieces together, a single request moves through the system like this:

1. The user types a question.
2. The query is embedded and sent to the vector database.
3. The database returns the top-k most similar document chunks.
4. The Context Augmentation step merges the query and the retrieved chunks into one prompt.
5. The merged prompt is sent to the LLM.
6. The LLM generates an answer grounded in the retrieved knowledge.
7. The answer is returned to the user as the response.

Each step has a single, well-defined job. This separation is what makes RAG easy to reason about and easy to improve in pieces (better chunking, better retriever, better reranker, better prompt) without rewriting the whole system.

## Why Context Augmentation is the Key Step

Retrieval on its own is just search. What makes RAG different from a normal search engine is the **augmentation** step — putting the search results directly into the LLM's prompt so the model treats them as source material rather than as a list of links.

Three properties come from this step:

- **Grounding** — the model has the facts in front of it, so it does not need to guess.
- **Traceability** — because the prompt lists the retrieved chunks, the system can cite them back to the user.
- **Freshness** — the knowledge in the prompt is as recent as the database, not as old as the training data.

If retrieval brings in the wrong chunks, context augmentation cannot save the answer. If augmentation is done badly (for example, chunks are dropped or formatted poorly), retrieval quality is wasted. Both steps must work together.

## Without RAG vs With RAG

A short side-by-side helps make the value of RAG concrete.

**Without RAG:**
- The LLM answers only from what it learned during training.
- Knowledge is stale after the training cutoff.
- Private or domain-specific data is invisible to the model.
- Hallucinations are more likely for rare or specific topics.
- Answers cannot be traced back to a source.

**With RAG:**
- The LLM answers using fresh, external knowledge fetched at query time.
- Private and internal documents can be used without retraining the model.
- Answers are grounded in specific retrieved passages, reducing hallucinations.
- Citations become possible because the prompt knows exactly which chunks were used.
- The knowledge base can be updated independently of the model.

This is why the diagram's one-line caption captures the whole pattern so well: the value of RAG is in retrieving external knowledge and feeding it to the LLM along with the user query.

---

# Slide 2 — Limitations of LLM

This slide lists the four main limitations of a plain LLM. Each one is a reason the model alone is not enough for a real product, and each one is something RAG is designed to fix.

## No Access to Proprietary Data

LLMs are trained on public data — the open internet, public books, open-source code. They have no visibility into your company's internal systems, such as CRM data, order history, or internal policies. Any company-specific knowledge must be fetched at query time from your own data sources.

## Training Cutoff

Every LLM is frozen at a specific training date. Anything that happened after that date — new product launches, updated policies, recent events — is invisible to the model. Fresh information has to come from an external source at the time of the query.

## Hallucinations

When an LLM does not actually know the answer, it tends to invent one that sounds confident and plausible but is wrong. This is the most dangerous limitation in production. Giving the model real retrieved facts reduces the pressure to guess.

## Long Tail Entity Recall

LLMs learn by how often something appears in training data. Popular topics are well understood, but rare or niche entities — a small regional company, an obscure medication, a little-used library — appear too few times for the model to learn them reliably. Retrieval surfaces those rare entities on demand.

## How These Limitations Map to RAG

Each limitation maps directly to a property that RAG provides.

| Limitation | How RAG fixes it |
|------------|------------------|
| No proprietary data | Retrieval pulls from your own database |
| Training cutoff | Retrieval pulls from fresh, up-to-date sources |
| Hallucinations | Retrieved facts ground the model and reduce guessing |
| Long tail recall | Retrieval surfaces rare entities on demand |

This is the bridge between Slide 1 and Slide 2: Slide 1 shows *what* RAG is, and this slide shows *why* RAG is needed.

---

# Slide 3 — Retrieval: Getting Data Out of Database

This slide zooms into the "R" in RAG — the retrieval step — and sets up the rest of the video. The flow shown is `User Query → Query pre-processing → Database → Documents`.

## The Retrieval Problem

Retrieval answers one central question: given a user query and a database of thousands or millions of documents, how do I pick the small set that is actually relevant? The quality of the final answer is bounded by the quality of this step. If retrieval returns the wrong documents, no amount of clever prompting or a smart LLM can fix it.

## Query Pre-Processing

Before the query is sent to the database, it is usually cleaned and transformed. This can include removing stopwords, fixing typos, rewriting the query into a form better suited to search, or converting the query into an embedding vector. Pre-processing is what makes the raw user question machine-searchable.

## Key Questions in Retrieval

Two important questions the slide raises:

- **Finding the right documents:** out of thousands of documents, which are relevant to this query?
- **Does order matter?** Yes. Retrieval returns a ranked list, and only the top few make it into the prompt. If the truly relevant document is ranked tenth, and only the top five are used, the LLM never sees it.

## Types of Retrieval

The slide introduces three retrieval styles, each covered in its own slide next:

- **Tabular retrieval** — for structured data in SQL tables.
- **Term-based retrieval** — classical keyword matching (BM25).
- **Embedding-based retrieval** — semantic search on vectors.

Think of this slide as the table of contents for everything that follows.

---

# Slide 4 — Retrieving Tabular Data (Text-to-SQL)

This slide covers retrieval when the knowledge lives in a **structured database** — rows and columns in SQL — instead of free-text documents.

## What Tabular Retrieval Is

Tabular retrieval means fetching answers from a relational database using SQL. The user asks a question in plain English, the system translates it into a SQL query, runs it, and translates the numeric result back into English. The technique is commonly called **Text-to-SQL**.

## End-to-End Flow (Tabular)

Using the example from the slide:

1. **Query:** *"How many units of product 12345 were sold between 1st September and 4th September?"*
2. **LLM (Text-to-SQL):** the model reads the question and the table schema, then generates SQL such as `SELECT SUM(Units_Sold) FROM TABLE1 WHERE PRODUCT_ID = 12345 AND Date BETWEEN '2025-09-01' AND '2025-09-04'`.
3. **Database:** the SQL query is executed against the real table and returns the numeric result.
4. **LLM (Response Generation):** the model turns that result into a natural-language answer: *"100 units of product 12345 were sold between 1st and 4th September."*

## Why the LLM Is Used Twice

The LLM appears at both the start and the end of the pipeline. At the start it translates the question into SQL. At the end it translates the raw row data back into a readable sentence. In between, the actual computation is done by the SQL engine, not the LLM. This separation matters: LLMs are unreliable at arithmetic over many rows, but SQL engines are precise and fast. Letting each do what it is best at produces accurate answers.

## When to Use This Pattern

Use Text-to-SQL retrieval when the answer depends on data stored in a relational database — orders, inventory, transactions, analytics, logs. You would not embed every row into a vector database for this kind of question; you would write SQL (or have the LLM write it for you).

---

# Slide 5 — Term-Based Retrieval

This is classical keyword search — the original approach to information retrieval, still widely used today.

## Key Idea (Term-Based)

> A document is relevant to the query if the terms in the query appear in the document.

From the slide's example, for the query "Banana":

- *"Bananas are inexpensive but healthy"* — contains "banana", so it matches.
- *"Banana is sweet"* — contains "banana", so it matches.
- *"Mango is the king of fruits"* — no "banana", so it does not match.

This is fast and works well when the user knows the exact terms to search for, like product codes, names, or technical keywords.

## The Common-Word Problem

If every shared word counted equally, queries would be dominated by common words such as "is", "an", and "the", which appear in almost every document. To avoid this, term-based retrieval weighs terms by how distinctive they are: rare terms that appear in a few documents are more informative than common terms that appear everywhere.

## BM25

**BM25** is the standard scoring algorithm for term-based retrieval. It formalizes the intuition above: it rewards query terms that appear frequently inside a given document (term frequency) but rarely across the whole corpus (inverse document frequency), and it normalizes for document length. BM25 is the default term-based scorer in search engines like Elasticsearch and Lucene.

## Limitation: Literal Matching

Term-based retrieval is **literal**. If the user searches for "banana" but the document only says "yellow tropical fruit", the match will fail even though the meaning is identical. This is the gap that embedding-based retrieval fills.

---

# Slide 6 — Embedding-Based Retrieval

This is semantic search — matching on meaning, not on exact words. It is the approach that made modern RAG possible.

## Key Idea (Embedding-Based)

> Embeddings capture the meaning of words, sentences, and documents as numeric vectors.

An embedding model turns a piece of text into a vector of numbers. Texts that mean similar things end up as vectors that point in similar directions in the vector space. From the slide's example, the query *"Yellow tasty tropical fruit"* and the document *"Banana"* share no common words, but their embeddings are close together because they mean the same thing.

## Indexing Flow (Offline)

Before any query is handled, the knowledge base is prepared:

1. Break long documents into smaller **chunks**.
2. Run each chunk through an **embedding model** (for example `text-embedding-3-small` or `bge-small`) to produce a vector.
3. Store chunks and their vectors in a **vector database** such as Chroma, Qdrant, or Pinecone.

This step is done once (or incrementally as new documents arrive). It is the expensive part, but it happens before any user query.

## Query Flow (Runtime)

When a user query arrives:

1. Embed the query using the **same embedding model** used for the documents.
2. Compare the query vector to all document vectors using a similarity metric.
3. Return the top-k most similar chunks.

Because the vectors are pre-computed, this step is fast even across millions of chunks.

## Cosine Similarity

Cosine similarity measures the angle between two vectors rather than their magnitude. Values near 1 mean the vectors point in nearly the same direction (very similar meaning), values near 0 mean they are unrelated, and values near -1 mean they are opposite. In a vector database, documents are **ranked by cosine similarity** to the query, and the top results are returned.

## Why This Beats Term-Based

Embedding-based retrieval handles things term-based cannot:

- **Synonyms** — "doctor" is close to "physician".
- **Paraphrasing** — "yellow tropical fruit" is close to "banana".
- **Related concepts** — "Python" is close to "FastAPI" in a programming context.

This is why embedding-based retrieval is the default for natural-language questions over documents.

## Trade-Offs and Hybrid Search

Each retrieval style has a weakness:

- **Term-based (BM25)** is fast and exact but fails on synonyms and paraphrasing. It shines on technical keywords, product codes, and rare entity names.
- **Embedding-based** is semantic but can miss exact-match keywords that matter (for example a specific error code).

In practice, the best production RAG systems combine both — a pattern called **hybrid search**. The results of BM25 and dense retrieval are merged and re-ranked so the system gets the strengths of both without the weaknesses of either.

---

# Slide 7 — Retrieval Evaluation Metrics (Precision, Recall, MRR, NDCG)

All four are Information Retrieval metrics that measure the quality of a retriever, but they look at the problem from different angles.

## The Family Tree

The metrics split into two groups based on whether they care about **the order** of the retrieved results.

```
Retrieval quality metrics
│
├── SET-BASED (ignore ranking order)
│     ├── Precision — of retrieved, how much is relevant?
│     └── Recall    — of all relevant, how much did I retrieve?
│
└── RANK-AWARE (position in the ranked list matters)
      ├── MRR  (Mean Reciprocal Rank) — how high is the FIRST relevant result?
      └── NDCG (Normalized Discounted Cumulative Gain) — full rank-aware score (position + grade of relevance)
```

The big shift between the two groups: precision and recall treat retrieval as a set — "these 10 documents came back" — and do not care whether the relevant ones are at rank 1 or rank 10. MRR and NDCG treat retrieval as a ranked list, so a relevant document at rank 1 is worth more than the same document at rank 10.

## When to Use Which

| Use case | Best metric |
|----------|-------------|
| "Did I retrieve the right stuff?" (coarse quality) | Precision / Recall |
| "Is the top-1 answer usually right?" (chatbots, single-answer Q&A) | MRR |
| "Is my whole ranking good?" (search, recommendations, RAG top-k) | NDCG |
| "Did the relevant chunks make it into the prompt at all?" (RAG) | Recall@k |
| "Are the top chunks mostly useful?" (RAG) | Precision@k or NDCG@k |

## Where These Metrics Fit in the RAG Lifecycle

These four metrics are **offline evaluation** metrics — they only run when you are testing or tuning the retriever, not when a real user asks a question in production.

```
RAG lifecycle
│
├── 1. BUILDING (chunking, embedding, indexing)   → no metrics yet
│
├── 2. EVALUATION (offline, with golden set)      ← Precision / Recall / MRR / NDCG live here
│       - Compare BM25 vs embedding vs hybrid
│       - Tune top-k, chunk size, reranker
│       - Regression-test when you change anything
│
├── 3. PRODUCTION (real user queries)             → no metrics, just serve answers
│
└── 4. MONITORING (after prod)                    → re-run golden set periodically
                                                    + LLM-as-judge on sampled real queries
```

In short: the metrics are for **developers tuning the retriever**, not for **users sending live queries**. In production, frameworks like RAGAS wrap these into higher-level **Context Precision** and **Context Recall** scores, usually judged by an LLM against a golden set.

---

# Slide 8 — Developer Decisions When Building a RAG System

Chunking is only one of many choices a developer makes when building a RAG system. Production-quality RAG involves decisions at every stage — how the data is prepared, where it is stored, how it is retrieved, and how the answer is generated. This section lists the full set of decisions grouped by stage.

## Ingestion Decisions

These decisions shape how raw documents are broken down before they are indexed.

- **Chunking strategy** — fixed-length, recursive, or semantic. Recursive is the common default.
- **Chunk size** — typically 200 to 1000 tokens. Smaller chunks give more precise matches but carry less context per chunk.
- **Chunk overlap** — typically 10 to 20 percent of the chunk size. Overlap prevents ideas from being lost at chunk boundaries.

## Storage Decisions

These decisions shape how chunks are turned into vectors and where they live.

- **Embedding model** — OpenAI `text-embedding-3-small` (cheap, good default), BGE, or a local model. The trade-off is cost, quality, and whether you need private/offline embeddings.
- **Vector database** — Chroma for development and prototyping, Qdrant or Pinecone for production scale.

## Retrieval Decisions

These decisions shape which documents are returned for a given query.

- **Retrieval type** — BM25 (term-based), dense (embedding-based), or hybrid. Hybrid usually wins in practice.
- **Top-k** — how many chunks to retrieve. Typical range is 3 to 10. Larger k improves recall but produces a noisier prompt.
- **Reranker** — an optional second-pass cross-encoder (for example Cohere Rerank or a BGE reranker) that re-orders the top-k by true relevance. It adds latency but gives a big quality boost.

## Generation Decisions

These decisions shape how the LLM turns retrieved chunks into a final answer.

- **Prompt template** — how retrieved chunks and the user query are formatted into the LLM input. Small changes here can swing quality significantly.
- **LLM choice** — Groq (fast, cheap), OpenAI GPT, or Claude. The trade-off is speed, quality, and cost.

---

# Slide 9 — Chunking Strategies: Fixed Size Chunking

Fixed size chunking is the simplest chunking strategy. It splits a document into chunks of a preset size — measured in characters or, more commonly, in tokens — without looking at the content's meaning.

## How Fixed Size Chunking Works

The developer picks a chunk size (for example, 500 tokens) and the splitter cuts the document into consecutive pieces of exactly that size. Since ideas in a document do not line up with token counts, a chunk often ends mid-sentence or mid-paragraph. To reduce the damage this causes, fixed size chunking is almost always paired with an overlap setting so that some text appears in both adjacent chunks.

## Chunk Size and Overlap

Fixed size chunking has two knobs a developer controls:

- **Chunk size** — how many characters or tokens per chunk. Typical range is 200 to 1000 tokens. Smaller chunks give more precise retrieval matches but carry less context; larger chunks carry more context but dilute relevance.
- **Chunk overlap** — how much of the end of one chunk is repeated at the start of the next. Typical overlap is 10 to 20 percent of the chunk size. Overlap exists so that an idea split across two chunks still appears in at least one complete retrievable piece.

## Fixed Size: Pros and Cons

- **Advantage:** It is simple to implement and fast to execute. This makes it a good starting point when prototyping a RAG system before investing in more sophisticated strategies.
- **Disadvantage:** The main drawback is that it can cut off semantic meaning mid-sentence or mid-paragraph. The splitter has no awareness of where ideas begin and end — it only counts tokens.

---

# Slide 10 — Chunking Strategies: Semantic Chunking

Semantic chunking groups sentences that are about the same topic into a single chunk. Instead of cutting by token count, it cuts at places where the meaning changes.

## How Semantic Chunking Works

The flow is:

1. **Segment the document** into smaller units — usually sentences or paragraphs.
2. **Embed each segment** using an embedding model so every segment becomes a vector.
3. **Open an initial first chunk** with the first segment.
4. **Keep adding new segments** to the current chunk as long as each new segment's embedding is similar to the chunk's running embedding.
5. **Close the chunk** when the cosine similarity drops drastically — that drop signals a topic shift. A new "initial second chunk" is opened with the next segment.
6. **Repeat** until the document is fully processed. The result is a set of final chunks, where each chunk contains semantically related segments and each chunk is a self-contained topic.

## Semantic: Pros and Cons

- **Advantage:** Retrieval accuracy goes up because chunks are richer and more meaningful. Each chunk represents a single idea or topic, so when a chunk matches a query, it is more likely to fully answer it.
- **Disadvantage:** Choosing the similarity threshold for what counts as a "drastic drop" is tricky. Too strict and you get too many tiny chunks; too loose and unrelated ideas end up merged. This threshold usually requires tuning on real documents.

---

# Slide 11 — Chunking Strategies: Recursive Chunking

Recursive chunking starts with naturally meaningful units such as paragraphs or thematic sections and only splits them further if they exceed the chunk size limit. It respects document structure first and falls back to smaller splits only when necessary.

## How Recursive Chunking Works

The flow is:

1. **Segment the document** into large natural units — paragraphs or thematic sections.
2. **Pick a segment** and check whether its size is greater than the chunk size limit.
   - **No** → keep it as a final chunk.
   - **Yes** → split it further recursively into smaller units (for example, sentences, then words) and repeat the check on each piece.
3. **Continue until every segment** fits within the chunk size limit.

In practice, libraries like LangChain's `RecursiveCharacterTextSplitter` implement this by trying a hierarchy of separators in order: first `\n\n` (paragraphs), then `\n` (lines), then `. ` (sentences), then ` ` (words), and finally individual characters. Each level is used only if the previous level still produces chunks that are too big.

## Recursive: Pros and Cons

- **Advantage:** Retrieval accuracy goes up because chunks respect natural boundaries such as paragraphs and sentences instead of blindly cutting at a fixed token count. This is why recursive chunking is a common default in production RAG systems.
- **Disadvantage:** Implementation and computational complexity. There are more moving parts than in fixed size chunking, and tuning the separator hierarchy and chunk size together takes some care.

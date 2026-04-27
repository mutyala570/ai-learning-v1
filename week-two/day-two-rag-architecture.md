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

### Slide 12 — Chunking Strategies: Naive Chunking vs Late Chunking
1. [**The Core Difference in One Line**](#the-core-difference-in-one-line)
2. [**Naive Chunking (i.i.d. Embeddings)**](#naive-chunking-iid-embeddings)
3. [**Late Chunking (Conditional Embeddings)**](#late-chunking-conditional-embeddings)
4. [**Why Late Chunking Beats Naive Chunking**](#why-late-chunking-beats-naive-chunking)
5. [**Trade-Offs and When to Use Late Chunking**](#trade-offs-and-when-to-use-late-chunking)

### Slide 13 — Query Pre-Processing: Modifying Queries to Improve Retrieval
1. [**Why Query Pre-Processing Exists**](#why-query-pre-processing-exists)
2. [**Query Classification**](#query-classification)
3. [**Query Cleaning and Rewriting**](#query-cleaning-and-rewriting)
4. [**Query Expansion**](#query-expansion)
5. [**Policy and Safety Check**](#policy-and-safety-check)
6. [**The Order of the Four Steps**](#the-order-of-the-four-steps)

### Slide 14 — Choosing the Right Embedding Model in RAG
1. [**Why This Choice Matters**](#why-this-choice-matters)
2. [**Relevance**](#relevance)
3. [**Domain Specificity**](#domain-specificity)
4. [**Performance vs Cost**](#performance-vs-cost)
5. [**Language Support**](#language-support)
6. [**Hosting**](#hosting)
7. [**How to Actually Pick One**](#how-to-actually-pick-one)

### Slide 15 — Which Vector Database to Choose: Pinecone vs Chroma vs Qdrant
1. [**Why the Choice Matters**](#why-the-choice-matters)
2. [**The Three Options in One Line Each**](#the-three-options-in-one-line-each)
3. [**Type: Who Hosts It**](#type-who-hosts-it)
4. [**Scalability: How Big Can It Go**](#scalability-how-big-can-it-go)
5. [**Ease of Use: How Fast Can You Start**](#ease-of-use-how-fast-can-you-start)
6. [**Performance: Latency and Throughput**](#performance-latency-and-throughput)
7. [**How to Actually Pick One**](#how-to-actually-pick-one-vector-db)

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

---

# Slide 12 — Chunking Strategies: Naive Chunking vs Late Chunking

Fixed size, semantic, and recursive chunking all differ in *where* they cut the document, but they share one assumption: the cuts happen **before** the text is embedded. This slide introduces a different axis of choice — *when* the cut happens relative to the embedding step. That choice separates **naive chunking** from **late chunking**.

## The Core Difference in One Line

> **Naive chunking = chunk first, then embed. Late chunking = embed first, then chunk.**

That single swap changes how much context each chunk's vector actually carries, and it is the reason late chunking was introduced.

## Naive Chunking (i.i.d. Embeddings)

Naive chunking is the default pipeline used by fixed size, semantic, and recursive strategies. The flow is:

1. Take the long document.
2. Split it into **Chunk1, Chunk2, … ChunkN** using whichever chunking strategy is chosen.
3. Send **each chunk independently** through the embedding model.
4. Pool the token outputs inside that chunk into a single vector — the chunk embedding.
5. Store each chunk embedding in the vector database.

Because every chunk goes through the embedding model on its own, its vector is computed in complete isolation from the other chunks. The embedding model never sees the surrounding document. This property is called **i.i.d. embeddings** — independent and identically distributed. Chunk 5 has no idea what Chunk 4 said, and Chunk 4 has no idea what Chunk 6 will say.

The problem this creates is a loss of context at chunk boundaries. Suppose Chunk 1 says *"Apple released a new phone last week."* and Chunk 2 says *"It has a better camera and longer battery life."* To a human the two chunks are clearly about the same phone, but the vector for Chunk 2 is computed with no knowledge of Chunk 1. The word *"It"* has nothing to anchor to. A query like *"Apple phone camera"* may match Chunk 1 but completely miss Chunk 2, even though Chunk 2 holds the actual answer.

## Late Chunking (Conditional Embeddings)

Late chunking flips the order of the two steps. The flow is:

1. Take the long document.
2. Feed the **entire document** through the embedding model in a single pass. The model produces one vector per token for every token in the document. Because modern embedding models are built on transformers, each token's vector is influenced by every other token in the document through the attention mechanism. Every token embedding already carries the full document's context.
3. **Now** decide the chunk boundaries and split the **sequence of token embeddings** (not the raw text) into groups — tokens 1 through 200 become Chunk 1, tokens 201 through 400 become Chunk 2, and so on.
4. Pool the token embeddings inside each group into one chunk vector.
5. Store the chunk vectors in the vector database.

Because the token vectors were produced while the model was looking at the whole document, each chunk embedding is **conditioned on the rest of the document**, not just its own text. This property is called **conditional embeddings**. Chunk 2 now knows that *"It"* refers to the phone mentioned earlier, because the token vectors for Chunk 2 were computed in the presence of Chunk 1's tokens.

The chunking step is called "late" because it is deferred until after the expensive embedding pass is done.

## Why Late Chunking Beats Naive Chunking

Late chunking fixes the specific weakness that naive chunking introduces: broken references across chunk boundaries. Three concrete gains fall out of it:

- **Pronouns and references survive.** Words like *it*, *they*, *this product*, *the policy* keep their meaning because the token embeddings were computed with the full document in view.
- **Short or vague chunks become retrievable.** A chunk like *"It has a better camera"* is almost useless under naive chunking because the embedding has no signal about *what* has a better camera. Under late chunking, that same chunk's vector carries enough surrounding context to still match a relevant query.
- **Chunking strategy becomes less fragile.** The penalty for cutting slightly in the wrong place is smaller, because the tokens on either side of the cut were embedded together.

## Trade-Offs and When to Use Late Chunking

Late chunking is not free. It comes with two real requirements:

- **The embedding model must support long inputs.** The entire document has to fit through the model in one pass, so the embedding model needs a long context window. Models designed for this include Jina Embeddings v2 and v3 and Nomic Embed. A standard short-context embedding model cannot do late chunking on a long document without first splitting it — which defeats the purpose.
- **A single long forward pass replaces many short ones.** Total compute is often similar or even lower than naive chunking, but memory usage per pass is higher because the full token sequence must be held at once.

As a rule of thumb, prefer **naive chunking** (with a recursive splitter) as the baseline — it is simple, fast, and good enough for most prototypes. Reach for **late chunking** when the documents are long, when references across chunks matter (legal text, technical manuals, research papers, long policies), or when retrieval quality on short chunks is noticeably poor. Late chunking is an optimization on top of a chunking strategy, not a replacement for one — you still need to pick *how* to cut; you just cut later.

---

# Slide 13 — Query Pre-Processing: Modifying Queries to Improve Retrieval

Slide 3 introduced query pre-processing as one of the boxes in the retrieval pipeline (`User Query → Query pre-processing → Database → Documents`). This slide opens that box and shows what actually happens inside it. The raw question a user types is almost never in the ideal shape for retrieval — it may have typos, be too vague, be too narrow, use different vocabulary than the documents, or even be unsafe to run. Query pre-processing is the set of fixes applied to the raw query before it reaches the retriever, grouped into four buckets.

## Why Query Pre-Processing Exists

The retriever only sees the query it is given. If that query is messy, narrow, or off-topic, retrieval will be bad no matter how good the vector database or the embedding model is. Pre-processing exists to give the retriever the best possible version of the user's question. It is the cheapest place to improve retrieval quality — changes here cost nothing at storage time and often more than pay for themselves in answer quality.

> **The goal of pre-processing is to turn a raw human question into a well-shaped search query.**

## Query Classification

Before anything else, the system decides *what kind of question* it is dealing with. Different kinds of questions need different retrieval paths, and classifying up front lets the system pick the right one. Three useful splits are:

- **Popular vs long tail** — Popular questions like *"What is Python?"* are well covered and retrieve easily. Long-tail questions like *"What is the retry behavior of library X version 3.2.1?"* are rare and usually need more aggressive retrieval or expansion to hit the right chunk.
- **Broad and ambiguous vs narrow** — A broad query like *"Tell me about AI"* is too open to retrieve well and usually needs a clarifying question or aggressive expansion. A narrow query like *"What is the default timeout in requests.get?"* can go straight to the retriever.
- **Factual vs reasoning** — Factual questions ask for a stored fact (*"When was OpenAI founded?"*). Reasoning questions ask the LLM to weigh options (*"Should we use RAG or fine-tuning for our case?"*). Retrieval is enough for factual; reasoning questions usually retrieve supporting context but lean on the LLM to think.

Classification is the branching point for everything that follows.

## Query Cleaning and Rewriting

Once the query type is known, the raw text is tidied up so the retriever can actually work with it.

- **Remove special characters and fix typos** — A query like *"wht is RAG??!!"* becomes *"what is RAG"*. This is basic hygiene but matters a lot for term-based retrieval (BM25), which does literal matching.
- **Lemmatization and stemming** — Reduce words to their root form so different surface forms match the same token. *"running"*, *"ran"*, and *"runs"* all collapse to *"run"*. Lemmatization is the smarter, dictionary-based version; stemming is the faster, rule-based version. Both help BM25 recall.
- **Step-back prompting** — Instead of searching with the original narrow question, ask an LLM to rewrite it into a broader, more general question first. For example, *"Did Einstein attend ETH Zurich in 1896?"* steps back to *"What is Einstein's education history?"*. The retriever runs on the broader question, which pulls in richer context, and the LLM then uses that context to answer the original narrow question. This is particularly useful when the narrow question matches few documents directly but sits inside a well-documented topic.

## Query Expansion

Even a clean query may be too short or too literal to retrieve well. Expansion adds more signal to the query so it can match documents that use different wording.

- **Add synonyms** — If the user asks about *"doctor"*, expand the query to also search for *"physician"*, *"clinician"*, and *"MD"*. This is essential for term-based retrieval where the user's word and the document's word must literally overlap.
- **HyDE — Hypothetical Document Embeddings** — A clever technique that flips the search direction. Instead of embedding the short question and hoping it lands near the real answer, ask an LLM to write a **hypothetical answer** to the question, embed that hypothetical answer, and use its vector as the search query. The intuition is that a full answer-shaped passage looks more like the real document you are trying to find than a short question does, so cosine similarity has a much easier job. The hypothetical answer can be factually wrong — it is only used for retrieval, never shown to the user. The real answer is generated later using the documents that were actually retrieved.

## Policy and Safety Check

Before the query goes to the retriever or the LLM, it is run through safety filters. This bucket is not about improving retrieval quality — it is about preventing the system from doing something it should not do.

- **Profanity check** — Block or sanitize abusive language before it propagates into logs, retrieval, or downstream prompts.
- **PII redaction** — Strip personally identifiable information (names, email addresses, phone numbers, card numbers) from the query. This protects the user, keeps logs safe, and avoids sending personal data to an external LLM provider.
- **Topic relevance check** — Confirm the question is in scope for this system. A medical chatbot should not be answering legal questions; an internal HR assistant should not be answering coding questions. Off-topic queries are refused here rather than retrieved against the wrong corpus, which would produce confidently wrong answers.

## The Order of the Four Steps

The four buckets are usually applied in this order: **classify → clean → expand → safety-check**. Classification decides which path to take. Cleaning and rewriting fixes how the query reads. Expansion makes the query richer. The safety check is the final gate before the query is allowed to hit the retriever or the LLM. Each step is cheap on its own, but together they lift retrieval quality more than most people expect — which is why production RAG systems almost always invest here before they invest in fancier retrievers or rerankers.

---

# Slide 14 — Choosing the Right Embedding Model in RAG

The embedding model is the heart of the retriever — it is what turns both the stored documents and the incoming user query into vectors so they can be compared. If the embedding model is wrong for the use case, every retrieval after it suffers, and no amount of clever chunking, reranking, or prompting can fully fix it. There is no single "best" embedding model; the right choice depends on five factors that this slide lays out.

## Why This Choice Matters

Unlike a chunking strategy or a top-k setting, the embedding model is **hard to change later**. Every document in the vector database was embedded with a specific model, and every query must be embedded with the same model. Switching embedding models means re-embedding the entire corpus — a one-time cost that can be large for a big knowledge base. That is why the embedding model deserves a careful decision up front, weighed against all five factors below.

## Relevance

Relevance is the primary factor. An embedding model's job is to map text into a vector space so that pieces of text with similar meaning end up close together and unrelated pieces end up far apart. For RAG the only question that matters is whether this mapping is **accurate enough that relevant chunks end up at the top of the ranked list** when a query is embedded. A model that scores well on generic similarity benchmarks but ranks the wrong chunks first for the actual queries users will ask is useless. Relevance must be measured on your own data, not on someone else's benchmark.

In practice, you test this by running a small golden set of real queries against a few candidate models and comparing Recall@k and NDCG@k (the metrics from Slide 7). Whichever model ranks the right chunks highest on that golden set wins — regardless of what the public leaderboards say.

## Domain Specificity

General-purpose embedding models such as `text-embedding-3-small` and `bge-small` are trained on the open web and work well for general text. Specialized domains are a different story, because they carry their own vocabulary and their own notion of what "similar" means:

- In **law**, the word *"consideration"* has a precise contractual meaning, not its everyday sense.
- In **medicine**, *"MI"* is myocardial infarction and *"PE"* is pulmonary embolism — not terms a general model will understand correctly out of the box.
- In **finance**, *"call"* and *"put"* are options contracts, not phone calls.

On specialized corpora, a general model often clusters documents by surface vocabulary rather than by domain meaning, which produces subtly wrong retrieval. For those cases, a **domain-tuned embedding model** (for example `LegalBERT`, `BioBERT`, `FinBERT`) or an embedding model fine-tuned on your own domain data usually retrieves noticeably better.

## Performance vs Cost

Bigger and newer embedding models generally retrieve better, but they come with two real cost axes that have to be weighed against quality.

The first is **storage cost, driven by vector dimensions**. A 1536-dimensional vector takes roughly twice the disk and memory of a 768-dimensional one. Across millions of chunks this turns into a real infrastructure bill — vector databases charge by vector count and size.

The second is **inference cost, driven by latency**. Larger models take longer to embed text both during indexing and at query time. Query-time latency is the painful one because it adds to every single user request. A 300 millisecond embedding step in front of the retriever is very different from a 30 millisecond one when compounded with LLM generation time.

For most production systems, a mid-tier embedding model combined with a reranker on top (see Slide 8) beats a giant embedding model used alone. You pay less for embedding and let the reranker do the heavy lifting only on the top-k candidates.

## Language Support

If the users or the documents are not all in English, a **multilingual embedding model** is required — one where, for example, *"doctor"* in English, *"médecin"* in French, and *"医生"* in Chinese end up near each other in the vector space. Common multilingual options include `multilingual-e5` and `paraphrase-multilingual-MiniLM`.

Using an English-only embedding model on a multilingual corpus is one of the most common silent failures in RAG systems. Retrieval appears to "sort of work" because English queries do fine, but quality on non-English queries is quietly terrible and the problem is easy to miss until users complain.

## Hosting

There are two paths for running an embedding model, each with its own trade-offs.

The first path is **API-based models** — services like OpenAI, Cohere, or Voyage. The appeal is convenience: a single HTTP call, no infrastructure to manage, and automatic scaling. The trade-offs are per-call cost, vendor lock-in, and most importantly the fact that data is being sent to a third party. For many projects, especially in regulated industries, that last point alone decides the question.

The second path is **self-hosted open-source models** — running something like `bge`, `nomic-embed`, or `jina-embeddings` on your own infrastructure. You get full control, predictable cost, and full data privacy. The trade-offs are operational overhead, GPU provisioning, and the responsibility of keeping the model and its deployment up to date.

The right choice here is less about which model is slightly better on a leaderboard and more about whether your data is allowed to leave your infrastructure and whether your team wants to own machine learning operations.

## How to Actually Pick One

A practical workflow: start with a reasonable default (a general-purpose model like `text-embedding-3-small` or `bge-small`), build a small golden set of queries with known-correct chunks, measure Recall@k and NDCG@k against two or three candidate models, and only move to a domain-specific or larger model if the numbers justify it. Cost and hosting constraints then narrow the candidate list further. The winner is whichever model sits at the best point of the **quality / cost / privacy** triangle for your specific use case — not whichever model is most popular.

---

# Slide 15 — Which Vector Database to Choose: Pinecone vs Chroma vs Qdrant

Once documents have been chunked and embedded, the vectors need somewhere to live — a place that can store millions (or billions) of them and search them quickly by similarity. That is what a vector database does. The three most commonly compared options are **Pinecone, Chroma, and Qdrant**, and the right choice among them usually comes down to three questions: who hosts the database, how big does it need to scale, and how much operational effort is the team willing to take on.

## Why the Choice Matters

Like the embedding model, the vector database is a decision that is costly to change later. Your chunks and their vectors, your metadata schema, and sometimes your client code all get shaped around the database you pick. Migrating vectors between databases is possible but slow and error-prone at scale. The trade-off is not really about raw performance — all three options perform well when configured correctly — but about the operational model: renting a service versus running one yourself.

## The Three Options in One Line Each

> **Pinecone — fully managed. Chroma — open-source, simple, prototyping-first. Qdrant — open-source, production-grade at scale.**

Everything that follows is the detail behind those three one-liners.

## Type: Who Hosts It

**Pinecone** is a **fully managed SaaS**. You do not install anything and you do not run any servers. You sign up, get an API key, and call their API. They handle hosting, scaling, upgrades, and failover. The trade-off is that Pinecone is a paid service and your data lives on their infrastructure.

**Chroma** is **open-source**. You can run it locally on your own laptop for development or deploy it on your own servers. Chroma also offers a hosted cloud option for teams that want someone else to operate it.

**Qdrant** is also **open-source**, with the same dual pattern — self-host it on your own infrastructure, or use Qdrant's managed cloud. Both Chroma and Qdrant give you control over where the data lives.

The key split here is between **Pinecone as rented convenience** and **Chroma or Qdrant as open-source tools you control**.

## Scalability: How Big Can It Go

**Pinecone** is built for **massive scale**. It can handle billions of vectors and scales automatically — you do not need DevOps effort to grow from thousands to millions to billions. This is its primary selling point.

**Chroma** is built for **small to medium scale**, typically up to around **10 million vectors**. It is the right choice for prototyping, personal projects, internal tools, and R&D. Beyond that scale, its performance and operational characteristics start to struggle.

**Qdrant** is built for **massive scale** as well. It is designed to handle billions of vectors with good performance, comparable to Pinecone in raw capability — but you are responsible for running and tuning the cluster yourself (or paying for their managed cloud).

The practical rule: a million vectors? Any of them will work. A billion vectors? You want Pinecone or Qdrant, not Chroma.

## Ease of Use: How Fast Can You Start

**Pinecone** is **easy** to use. It hides all infrastructure complexity behind a simple API — sign up, get an API key, and start inserting vectors with a handful of lines of code.

**Chroma** is **simple and Python-native**. It is the easiest option to get started with for development because it installs as a Python package and runs in the same process as your code. This is why most RAG tutorials and prototypes use Chroma — it minimizes the distance between "I have an idea" and "I have a working demo."

**Qdrant** is **moderate** in ease of use. It is slightly more involved than Chroma because it is built with production features in mind — cluster management, sharding, replication, and rich filtering capabilities. Those features are exactly what make it production-ready, but they also mean there is more to configure and understand.

## Performance: Latency and Throughput

**Pinecone** delivers **low latency and high throughput** at any scale, by design. Performance is consistent and predictable, which is part of what you are paying for.

**Chroma** offers **good performance for small scale**. It is fast enough for prototypes, demos, and small production workloads, but was not engineered to handle heavy production traffic.

**Qdrant** delivers **low latency and high throughput** on par with Pinecone when properly configured. Achieving that performance is your responsibility rather than the provider's — which is the core trade-off of the self-hosted path.

## How to Actually Pick One (Vector DB)

A practical decision tree:

- **Prototyping, learning, or building an internal tool?** Use **Chroma**. It is the fastest path from idea to working RAG demo, and it is more than capable up to around 10 million vectors.
- **Going to production, do not want to manage infrastructure, and have a budget?** Use **Pinecone**. You pay for convenience and get predictable performance, automatic scaling, and zero DevOps effort in return.
- **Going to production, need full control over your data and infrastructure, and have a team that can run distributed systems?** Use **Qdrant**. You get the same scale and performance profile as Pinecone, but open-source and self-hostable.

The underlying principle is the same as the embedding model decision: pick whatever sits at the best point of the **convenience / control / cost** triangle for your specific situation, not whichever database is most fashionable this quarter.

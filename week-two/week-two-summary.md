# Week 2 — Prose Summary

A structured summary of everything covered in `week-two/`, broken out so every concept and every sub-item gets its own heading and explanation. The glossary-style one-liner reference lives in `week-two-recap.md`. Read this file before starting Week 3 — it gives the full picture without forcing you to read whole paragraphs to find a single idea.

## Topics Covered in This Document

1. [**The Agent Frame**](#1-the-agent-frame)
2. [**Why RAG Exists**](#2-why-rag-exists)
3. [**The Vanilla RAG Pipeline End-to-End**](#3-the-vanilla-rag-pipeline-end-to-end)
4. [**The Design Choices a RAG Team Has to Make**](#4-the-design-choices-a-rag-team-has-to-make)

---

# 1. The Agent Frame

A modern AI agent is a system that takes a user's question, decides what to do with it, and returns an answer. The LLM at the centre is the **reasoning and routing engine** — not the whole system. Around it sit memory, tools, and RAG.

## 1.1 Modern Agent Flow

When a question arrives, the LLM decides which path the question should take: pull from memory, call a tool, run RAG, or answer directly. In modern frameworks the routing is done by the LLM itself through **function calling**, not by a separate intent-classifier model. The chosen path's output is gathered back into context, and the LLM produces the final answer.

## 1.2 Memory — Two Categories, Four Types

The agent's memory is split into **short-term** (the live chat) and **long-term** (everything that persists across sessions). Long-term memory has three sub-types: semantic, episodic, and procedural.

### 1.2.1 Short-Term Memory

Holds the **current conversation** — the last N messages between the user and the agent. It gives the agent immediate context for follow-up questions and pronoun resolution (e.g. "make it shorter" — what is "it"?). Implementation is usually a session cache in Redis, an in-process buffer, or a conversation object. Bounded by the LLM's context window — once a chat grows too long, older messages are either dropped or summarised.

### 1.2.2 Long-Term Memory — Three Types

Anything the agent needs to remember **across sessions** lives in long-term memory. These three sub-types are all "long-term" relative to the short-term chat buffer.

#### 1.2.2.1 Semantic Memory

Stable **facts about the user** — name, language, timezone, role, preferences. Things that do not change often. Implemented in a structured database (Postgres, MongoDB) as key-value pairs or JSON documents, or sometimes in a vector DB if you want to retrieve facts by meaning ("find facts about the user's work preferences").

#### 1.2.2.2 Episodic Memory

**Past conversations and past events** — what the user asked last week, what happened in the previous transaction. Implemented in a vector DB with timestamps so retrieval can be both semantic (by meaning) and temporal (by time). Long conversations are usually summarised before being stored, so each episode is a compact, meaningful record rather than a raw transcript.

#### 1.2.2.3 Procedural Memory

**Skills and workflows** — how to send an email, how to create a ticket, how to book a meeting. In practice this is stored as **prompt templates, code snippets, or tool definitions**. In most agent frameworks, the set of registered tools (with their schemas and system prompts) effectively *is* the agent's procedural memory.

## 1.3 Function Calling — Six Steps

The mechanism that lets the LLM reach outside itself. Anthropic calls it "tool use", OpenAI and Gemini call it "function calling", LangChain wraps all three.

### 1.3.1 Step 1 — Define Tools as Schemas

Register each tool with a name, description, and parameter schema. The LLM reads these definitions and uses them to decide when a tool is appropriate.

### 1.3.2 Step 2 — Send Message + Tool List to LLM

When a request comes in, send the user's message along with the full list of available tool definitions to the LLM in one call.

### 1.3.3 Step 3 — LLM Decides Direct Answer or Tool Call

The LLM reads the message and decides whether to answer from its own knowledge or to request a tool call. If it picks a tool, it returns a structured JSON with the tool name and arguments.

### 1.3.4 Step 4 — Application Executes the Tool

Your code receives the tool-call request and actually runs the function — call the API, run the calculation, query the DB. **The LLM does not execute the tool itself.** It only requests; your application controls execution, and that is what keeps the system safe.

### 1.3.5 Step 5 — Send Tool Result Back to the LLM

Once the tool returns a result, send that result back to the LLM in a follow-up call so the model can use it.

### 1.3.6 Step 6 — LLM Generates the Final Response

With the tool's output now in its context, the LLM produces a natural-language answer for the user.

## 1.4 RAG vs Tools — When to Use Which

The decision depends on **where the information lives** and **how often it changes**, not on whether it is in the model's training data.

### 1.4.1 Use RAG When

The information lives in **documents you control**, is **relatively stable**, and can be **indexed ahead of time**. Examples: product manuals, policy docs, internal wikis, support articles. The corpus is chunked, embedded, and stored once, then retrieved fast at query time.

### 1.4.2 Use Tools When

The information is **real-time** or **dynamic**, lives in a **live system** (DB, CRM, SaaS API), requires **computation**, or the agent needs to **perform an action** (send email, create record, book a meeting). Tools give the agent access to the outside world and the ability to act, not just read.

### 1.4.3 Quick Rule of Thumb

- **Static document information** → RAG
- **Live, dynamic, or action-based** → Tool
- **User-specific context** → Memory
- **General knowledge already in training** → plain LLM

---

# 2. Why RAG Exists

A plain LLM has hard limitations, and RAG exists to fix them by injecting external knowledge into the prompt at query time.

## 2.1 LLM Limitations — Four Categories

### 2.1.1 Training Cutoff

Every LLM is frozen at a specific training date. Anything that happened after — new product launches, updated policies, recent events — is invisible to the model. Fresh information has to come from an external source at the time of the query.

### 2.1.2 No Access to Proprietary Data

LLMs are trained on public data: the open internet, public books, open-source code. They have no visibility into your CRM, order history, or internal policies. Any company-specific knowledge must be fetched at query time from your own data sources.

### 2.1.3 Hallucinations

When an LLM does not know an answer, it tends to invent one that sounds confident and plausible but is wrong. This is the most dangerous failure in production. Giving the model real retrieved facts reduces the pressure to guess.

### 2.1.4 Long-Tail Entity Recall

LLMs learn by how often something appears in training data. Popular topics are well understood, but rare or niche entities — a small regional company, an obscure medication, a little-used library — appear too few times for the model to learn them reliably.

## 2.2 What RAG Adds Beyond Limitation Fixes

### 2.2.1 Privacy and Compliance

Sensitive data (customer records, internal policies, proprietary research) should not enter model weights. RAG keeps such information inside retrieval systems the organisation owns and controls. The model reads from these systems on demand, so the sensitive data never becomes part of the model itself.

### 2.2.2 Domain-Specific Accuracy

General LLMs have wide but shallow coverage and often struggle in specialised fields (medicine, law, internal company processes). RAG lets the model reach into curated domain corpora and use them as the source of truth.

## 2.3 RAG Scenarios — Three Use Cases

### 2.3.1 Retrieving External Knowledge

The most common scenario. When a question goes beyond what the LLM knows because the information is recent, specialised, or private, the system retrieves relevant documents from an external knowledge base and provides them as supporting context.

### 2.3.2 Retrieving Context History

In long-running conversations, keeping every past message in the prompt is impractical because of context-window limits and cost. RAG stores earlier parts of the conversation in a retrievable form. When the current turn refers back to an older topic, the system fetches only the relevant history.

### 2.3.3 Retrieving In-Context Training Examples

LLMs can learn new tasks from examples placed inside the prompt — **in-context learning**. RAG dynamically retrieves the most relevant examples for each incoming query from a stored pool and injects them into the prompt. This is **dynamic few-shot prompting**, and it differs from static few-shot (where examples are hard-coded) and from prompt chaining (where a task is split across multiple sequential LLM calls).

---

# 3. The Vanilla RAG Pipeline End-to-End

Vanilla RAG is the baseline pattern. Every more advanced RAG system is built on top of it. It has two flows that meet at one merging point.

## 3.1 Offline Indexing — Prepares the Knowledge Base

Done once, ahead of time. Three steps.

### 3.1.1 Chunking

Long documents are split into smaller pieces that are semantically coherent and fit inside the LLM's context window. Each chunk should still make sense on its own when retrieved later.

### 3.1.2 Embedding

Each chunk is passed through an **embedding model** (e.g. `text-embedding-3-small`, `bge-small`) which converts it into a numeric vector representing its meaning.

### 3.1.3 Storing

The vectors plus their metadata (source, chunk id, timestamps) are saved into a **vector database** such as Chroma, Qdrant, or Pinecone, which supports fast similarity search.

## 3.2 Online Query — Runs Per Request

When a user submits a question, four steps happen in sequence.

### 3.2.1 Embed the Query

Convert the query into a vector using the **same embedding model** that was used during indexing. This is critical — different models produce incomparable vector spaces.

### 3.2.2 Retrieve Top-k

Search the vector database for the chunks whose vectors are closest to the query vector, ranked by **cosine similarity** or dot product. Return the top k most similar chunks.

### 3.2.3 Augment

Merge the retrieved chunks and the original query into a single structured prompt with clear sections labelled *Context* and *Question*, plus an explicit instruction such as "answer using only the context above".

### 3.2.4 Generate

Send the augmented prompt to the LLM. The LLM reads the context, interprets the question, and produces a grounded answer.

## 3.3 Top-k Choice

How many chunks to return.

### 3.3.1 Small k (1–3)

Precise, less noise, but may miss the right chunk. Cheaper.

### 3.3.2 Medium k (5–10)

Balanced. Common production default.

### 3.3.3 Large k (20+)

Higher recall but produces a noisy prompt. Hits the **"lost in the middle"** problem where the LLM overlooks information buried inside too much content.

## 3.4 Why Context and Question Travel Together

LLMs are **stateless** — every API call is independent. The model has no memory of previous calls. Anything the model needs must fit inside one single prompt. The **context** is the open-book knowledge source; the **question** is the instruction telling the model what to extract from that context. Neither part is useful on its own.

## 3.5 Why Chunking Matters

### 3.5.1 Semantic Coherence

A good chunk contains a complete idea or section so it still makes sense when retrieved on its own. Chunks that cut across ideas retrieve poorly.

### 3.5.2 Context-Window Limits

LLMs have a fixed input window. Regardless of document size, only a limited number of tokens fit in one prompt. Chunking breaks long documents into pieces that fit.

### 3.5.3 Precise Retrieval

Instead of fetching an entire document when only one paragraph is relevant, the system fetches just the matching pieces. This avoids clutter in the context and lets the model focus on what is actually useful.

## 3.6 Limitations of Vanilla RAG

### 3.6.1 Fragile Retrieval

If the retriever fetches the wrong chunks, the answer is wrong regardless of how capable the LLM is.

### 3.6.2 Naive Chunking

Fixed-size chunking often cuts across sentence or paragraph boundaries, destroying meaning.

### 3.6.3 Single-Shot Retrieval

The system cannot refine its query or re-rank results. Whatever the retriever returns is what the LLM sees.

### 3.6.4 Weak Multi-Hop

Questions that need information from multiple documents combined are not handled well.

### 3.6.5 Noise Confusion

When too many irrelevant chunks are included, the LLM can become confused rather than better informed.

## 3.7 What Comes After Vanilla RAG

Query rewriting and HyDE to reformulate the query, **rerankers** to sort candidates more accurately, **hybrid search** to combine vector similarity with BM25, **multi-hop or agentic RAG** for iterative retrieval, and smarter chunking strategies based on semantic boundaries or document structure.

---

# 4. The Design Choices a RAG Team Has to Make

Six decisions every team faces. They sit in different parts of the pipeline but they all have to be answered before anything ships.

## 4.1 Query Pre-Processing — Four Steps

The retriever can only do well on a well-shaped query. Pre-processing is the cheapest place to lift retrieval quality. The four steps run in this order: classify → clean → expand → safety-check.

### 4.1.1 Classify

Decide what kind of question this is. Three useful splits: **popular vs long-tail**, **broad vs narrow**, **factual vs reasoning**. Different question types need different retrieval paths — a narrow factual question can go straight to the retriever, a broad one usually needs expansion first, a reasoning question retrieves supporting context but leans on the LLM to think.

### 4.1.2 Clean and Rewrite

Tidy up the raw text so the retriever can work with it. Remove special characters, fix typos, apply **lemmatisation/stemming** to collapse word forms (running/ran/runs → run), and optionally use **step-back prompting** to broaden a narrow question before searching.

### 4.1.3 Expand

Make a clean query richer so it can match documents that use different wording. Add **synonyms** (doctor → physician, clinician), or use **HyDE (Hypothetical Document Embeddings)** — have an LLM write a hypothetical answer to the question, embed that answer, and use its vector as the search query. The hypothetical answer can be factually wrong; it is only used for retrieval, never shown to the user.

### 4.1.4 Safety-Check

The final gate before the query reaches the retriever or LLM. **Profanity filter**, **PII redaction** (strip names, emails, phone numbers, card numbers), and **topic-relevance check** (refuse off-topic queries here rather than retrieving against the wrong corpus).

## 4.2 Chunking Strategy

Chunking decides both **how** to cut the document and **when** to cut relative to embedding.

### 4.2.1 How — Three Strategies

#### 4.2.1.1 Fixed Size

**How it works:** pick a chunk size in tokens, cut the document into consecutive pieces of that size, paired with a small overlap (typically 10–20%).

**Advantage:** simple to implement, fast to execute, almost no tuning.

**Disadvantage:** the splitter has no awareness of meaning, so it routinely cuts mid-sentence or mid-paragraph and breaks local context.

#### 4.2.1.2 Semantic

**How it works:** embed each sentence, keep adding to the current chunk while the embeddings are similar, close the chunk when cosine similarity drops sharply (a topic shift).

**Advantage:** each chunk holds one self-contained topic, so when a chunk matches a query it usually fully answers it.

**Disadvantage:** the similarity-drop threshold is fiddly. Too strict produces tiny fragmented chunks; too loose merges unrelated ideas together.

#### 4.2.1.3 Recursive

**How it works:** split by paragraph first, then sentence, then word, only going deeper if the current piece still exceeds the size limit. LangChain's `RecursiveCharacterTextSplitter` is the canonical implementation.

**Advantage:** respects natural document structure. Common production default because chunks stay coherent without manually tuning a similarity threshold.

**Disadvantage:** more moving parts. Tuning the separator hierarchy together with chunk size takes careful iteration.

### 4.2.2 When — Naive vs Late

The "when" axis is independent of the "how" axis: you still pick a strategy, you just choose when to apply it relative to embedding.

#### 4.2.2.1 Naive Chunking

**How it works:** chunk first, then embed each chunk **independently** through the embedding model. Each chunk's vector is computed in isolation from the others.

**Problem:** loss of context at chunk boundaries. If Chunk 1 says *"Apple released a new phone"* and Chunk 2 says *"It has a better camera"*, Chunk 2's embedding has no anchor for *"It"*. A query like *"Apple phone camera"* may miss Chunk 2 entirely.

#### 4.2.2.2 Late Chunking

**How it works:** feed the **entire document** through the embedding model first, so every token's vector is conditioned on the whole document via attention. *Then* cut the sequence of token embeddings into chunks and pool each group into one chunk vector.

**Advantage:** pronouns and references survive, short chunks remain retrievable, cutting in slightly the wrong place hurts less.

**Trade-off:** requires a long-context embedding model (Jina v2/v3, Nomic Embed). Memory per pass grows; total compute is similar or lower than naive.

## 4.3 Embedding Model — Five Factors

The embedding model is the heart of the retriever and is **hard to change later** — switching means re-embedding the whole corpus. Five factors decide the right pick.

### 4.3.1 Relevance

Does the model rank truly relevant chunks at the top **for your queries**? Measure on a small golden set with Recall@k and NDCG@k. Public leaderboards are not enough — relevance is domain-specific.

### 4.3.2 Domain Specificity

General-purpose models (`text-embedding-3-small`, `bge-small`) work for generic text but often fail in specialised fields where words have precise meanings: law's "consideration", medicine's "MI" (myocardial infarction), finance's "call/put". For those, domain-tuned models like LegalBERT, BioBERT, FinBERT retrieve much better.

### 4.3.3 Performance vs Cost

Bigger models retrieve better but cost more in two axes: **storage** (vector dimensions — 1536-dim takes roughly twice the disk and memory of 768-dim) and **inference latency** (query-time embedding adds to every request). A mid-tier model plus a reranker on top usually beats a giant model used alone.

### 4.3.4 Language Support

Multilingual corpora need multilingual models (`multilingual-e5`, `paraphrase-multilingual-MiniLM`) where "doctor" / "médecin" / "医生" land near each other in vector space. Using an English-only model on multilingual data is a common silent failure.

### 4.3.5 Hosting

**API-based** (OpenAI, Cohere, Voyage) — convenient, no infra, but data leaves your perimeter and you pay per call. **Self-hosted open-source** (`bge`, `nomic-embed`, `jina-embeddings`) — full control, predictable cost, data privacy, but operational overhead and GPU provisioning.

## 4.4 Vector Database — Three Options

The decision is not really about raw performance — all three perform well when configured correctly — but about the **operational model**.

### 4.4.1 Pinecone

**Fully managed SaaS.** Sign up, get an API key, start inserting vectors. Handles billions at scale with zero DevOps. **Trade-off:** paid service, data lives on their infrastructure.

### 4.4.2 Chroma

**Open-source, Python-native.** Runs as a Python package in the same process as your code, which is why every RAG tutorial uses it. Best for prototyping and R&D up to ~10M vectors. **Trade-off:** not built for massive scale.

### 4.4.3 Qdrant

**Open-source, production-grade.** Scales to billions of vectors with low latency, comparable to Pinecone, but you run the cluster (or pay for their managed cloud). Slightly more complex than Chroma because of production features (sharding, replication, rich filtering). **Trade-off:** operational overhead.

### 4.4.4 Decision Rule

**Chroma for building, Pinecone for renting, Qdrant for owning.**

## 4.5 Retrieval Strategy — Four Styles

The right style depends on whether the data is structured or unstructured, and whether the user's wording will literally match the documents.

### 4.5.1 Tabular / Text-to-SQL

For **structured data in SQL tables** — orders, inventory, transactions, analytics. The LLM reads the question and the table schema, generates SQL, the SQL engine runs it, and the LLM turns the rows back into a natural-language sentence. The LLM appears at both ends; the actual computation is done by the SQL engine, not the LLM.

### 4.5.2 Term-Based (BM25)

**Classical keyword matching.** A document is relevant if the query terms appear in it. **BM25** is the standard scoring algorithm — it rewards terms frequent in a document but rare across the corpus, normalised for document length. **Strength:** fast and exact; great for product codes, technical keywords, rare entity names. **Weakness:** literal matching — if the user types "banana" but the document says "yellow tropical fruit", BM25 misses.

### 4.5.3 Embedding-Based

**Semantic search using cosine similarity** between query and chunk vectors. Embeddings capture meaning, so paraphrases and synonyms still match. **Strength:** handles synonyms ("doctor" ≈ "physician"), paraphrasing, related concepts. **Weakness:** can miss exact-match keywords that matter (e.g. a specific error code).

### 4.5.4 Hybrid Search

Run BM25 and embedding-based retrieval **together**, merge and rerank the results. Inherits the strengths of both without the weaknesses of either. Default winning pattern in production RAG.

## 4.6 Reranker — Two-Stage Architecture

Plain vector similarity is fast at scale but coarsely accurate. The fix is to add a second, slower-but-more-precise stage on top.

### 4.6.1 Why Vector Similarity Alone Is Not Enough

It **ignores rare-word importance**, **loses nuance** by compressing each chunk down to one vector, and **struggles with long-tail data** the embedding model rarely saw during training. Good for casting a wide net; bad for ranking the final list.

### 4.6.2 Bi-Encoder — Stage 1

**What it is:** the first-stage retriever. Embeds query and documents **separately**; document vectors are pre-computed and stored.

**Why it is fast:** at query time only the query is freshly embedded, then compared against pre-stored document vectors. Search scales to millions of chunks.

**Where it falls short:** the model never sees query and document together, so it misses fine-grained word-level interactions and ranks the candidate set coarsely.

### 4.6.3 Cross-Encoder — Stage 2

**What it is:** the second-stage reranker. Takes query and one document **jointly** into the same model pass and outputs one relevance score for that pair.

**Why it is more accurate:** query and document share a single forward pass, so the model captures deep word-level interactions a vector dot product cannot see (e.g. "refund" in the query matches "money back" in the document).

**Why it is slow:** embeddings cannot be pre-computed. Each new query needs a fresh model pass per candidate, so cost grows linearly with the candidate count.

### 4.6.4 Bi-Encoder vs Cross-Encoder — The Trade

**Bi-encoder:** fast at scale, coarsely accurate. **Cross-encoder:** precisely accurate, slow. Used alone, neither works — bi-encoder lacks final precision, cross-encoder is too slow at scale. Combined, they cover each other.

### 4.6.5 Two-Stage Retrieval Flow

```
Query → Bi-Encoder → Top-100 candidates → Cross-Encoder → Top-5 → Filter → LLM
        (millions of docs)                  (rerank shortlist)
```

Bi-encoder narrows millions of docs to hundreds quickly. Cross-encoder reranks those hundreds with fine-grained precision. A final **filter** step drops low-score candidates, deduplicates, applies permission checks, and caps the list to fit the LLM's context window.

## 4.7 Evaluation — Four Metrics

Retrieval quality must be measured before anything else can be tuned. Evaluation is **offline** — done with a golden set of queries and known-correct chunks, not on live production traffic. The four metrics split into two families based on whether ranking order matters.

### 4.7.1 Set-Based Metrics — Order Doesn't Matter

#### 4.7.1.1 Precision

Of the chunks I retrieved, how many were actually relevant? Best for coarse quality checks.

#### 4.7.1.2 Recall

Of all the relevant chunks that exist, how many did I retrieve? In RAG, **Recall@k** is the key metric — did the relevant chunks make it into the prompt at all?

### 4.7.2 Rank-Aware Metrics — Position Matters

#### 4.7.2.1 MRR (Mean Reciprocal Rank)

How high in the ranked list is the **first** relevant result? Best for single-answer Q&A, chatbots — when only the top-1 answer is shown.

#### 4.7.2.2 NDCG (Normalized Discounted Cumulative Gain)

Scores the **entire** ranked list, weighting higher positions more and accounting for the relevance grade of each result. Best for search, recommendations, and RAG top-k where the whole shortlist matters.

### 4.7.3 In Production

These offline metrics are wrapped into higher-level measures like **Context Precision** and **Context Recall** in frameworks like RAGAS, typically judged by an LLM against the same golden set. The metrics themselves live in evaluation, not in production: developers tune the retriever using them; users sending live queries never see them.

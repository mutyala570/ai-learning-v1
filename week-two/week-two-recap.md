# Week 2 Recap — Topics Covered (Pre-Week 3 Reference)

A compressed snapshot of every topic from `week-two/` so I can walk into Week 3 with the prior context loaded. Each sub-heading is followed by a roughly twenty-word, high-level explanation. For full detail, follow the pointer at the top of each section back to the original note in `week-two/`.

## Topics Covered in This Document

1. [**Agent Architecture (Big-Picture Frame)**](#1-agent-architecture-big-picture-frame)
2. [**RAG Fundamentals**](#2-rag-fundamentals)
3. [**RAG Component Deep-Dive**](#3-rag-component-deep-dive)
4. [**Six RAG Design Questions**](#4-six-rag-design-questions)

---

# 1. Agent Architecture (Big-Picture Frame)

**Source:** `week-two/agent-architecture.md`

## Modern Agent Flow

User question goes to LLM, which routes via reasoning to memory, tools, RAG, or direct answer, then synthesises.

## Step 1 — User Asks a Question

Plain question entry point. The whole agent system exists to convert this question into a grounded answer.

## Step 2 — LLM Reasoning Decides the Route

LLM acts as router using function calling, picking memory, tool, RAG, or direct answer based on the question.

## Step 3 — Memory Path

Used for user-specific questions. LLM picks one of four memory stores depending on the kind of context needed.

## Step 4 — Tool Path

Used when answer needs real-time data, computation, external system access, or an action like sending an email.

## Step 5 — RAG Path

Used for questions about document corpora. Flow is embedding, vector DB, retrieval, reranking, then LLM synthesis.

## Step 6 — LLM Generates the Final Response

LLM synthesises gathered context into the final answer. It generates, it does not select; selection happened earlier.

## Memory Type 1 — Short-Term

Holds the current chat window. Implemented as session cache or buffer; bounded by the model's context window.

## Memory Type 2 — Semantic

Stable user facts like name, language, role, preferences. Stored in Postgres, MongoDB, or sometimes a vector database.

## Memory Type 3 — Episodic

Past conversations and events. Stored in a vector DB with timestamps so retrieval can be semantic and temporal.

## Memory Type 4 — Procedural

Skills and workflows. In practice the agent's registered tools and prompt templates effectively are its procedural memory.

## Function Calling — Six-Step Flow

Define tool schema, send tools plus message to LLM, LLM requests a tool, app executes, result returns, LLM answers.

## Function Calling — Mental Model

The LLM never executes a tool itself. It only requests; your application controls execution and so controls safety.

## RAG vs Tools Decision

Static document knowledge goes through RAG. Live, dynamic, computational, or action-based information goes through tools instead.

## Quick Rule of Thumb

Static docs → RAG. Live/dynamic/action → tool. User-specific → memory. General knowledge already trained → plain LLM call.

---

# 2. RAG Fundamentals

**Source:** `week-two/rag-notes.md`

## Why RAG — Knowledge Cutoff

LLMs are frozen at their training date. RAG injects fresh information at query time so answers stay current.

## Why RAG — Privacy and Compliance

Sensitive customer or internal data should not enter model weights. RAG keeps it inside controlled retrieval systems instead.

## Why RAG — Reduce Hallucinations

Grounding the model in retrieved passages reduces invented answers and gives users a way to verify the source.

## Why RAG — Domain-Specific Accuracy

General LLMs are wide but shallow. RAG plugs in curated domain knowledge bases for medicine, law, internal processes.

## Why RAG — Long-Tail Entity Recall

Rare entities are weakly represented in training data. Retrieval surfaces them on demand for reliable, accurate answers.

## RAG Scenario — External Knowledge

Most common case. System retrieves relevant docs from an external knowledge base when the question exceeds LLM training.

## RAG Scenario — Context History

Long conversations exceed context windows. RAG stores past turns and fetches only the parts relevant to the current question.

## RAG Scenario — In-Context Training Examples

System retrieves the most relevant worked examples and injects them so the LLM learns the task without retraining.

## Prompting — Zero-shot

Only the instruction is given, no examples. Model relies entirely on its training knowledge to perform the task.

## Prompting — One-shot

One worked example is shown before the real task so the model learns the expected format and style.

## Prompting — Few-shot

Several examples are shown before the task. Useful for subtle patterns or strict output formatting requirements.

## Prompting — Dynamic Few-shot

RAG-powered. System retrieves the best examples per query from a pool, instead of hard-coding them in the prompt.

## Dynamic Few-shot vs Prompt Chain

Dynamic few-shot decides what enters one prompt. Prompt chain splits a task across multiple sequential LLM calls.

## Vanilla RAG Pipeline

Two parallel flows. Indexing makes vectors offline; retrieval and augmentation happen at query time before LLM generation.

## Indexing Stage

Documents are chunked, each chunk embedded, and the vectors stored in a vector database for fast similarity search.

## Retrieval Stage

User query is embedded with the same model, then top-k similar chunks are pulled from the vector database.

## Top-k Choice

How many chunks to return. Small k is precise but risks misses; large k boosts recall but adds noise.

## Context Engineering / Augment

Retrieved chunks plus original query are merged into one structured prompt, with section headers and explicit usage instructions.

## Why Context and Question Travel Together

LLMs are stateless. Each call is independent, so everything the model needs must fit inside one single prompt.

## Generation Stage

The augmented prompt goes to the LLM, which synthesises a grounded answer using the retrieved context, not training data.

## Why Chunking Matters

Chunks must be semantically coherent, fit the context window, and enable precise retrieval of just the relevant passages.

## Limitations of Vanilla RAG

Fragile retrieval, naive chunking, single-shot search, weak multi-hop handling, and noise when too many irrelevant chunks return.

## What Comes After Vanilla RAG

Query rewriting, HyDE, rerankers, hybrid search, multi-hop or agentic RAG, and smarter chunking strategies all stack here.

## Reranker — Why It Is Needed

Vector similarity is fast but coarse. A reranker fixes the precision gap so only truly relevant chunks reach the LLM.

## Vector Similarity — The Good

Fast at scale because comparing vectors is just a dot product. Handles variable-length documents and is supported by mature vector DBs.

## Vector Similarity — The Bad

Ignores rare-word importance, loses nuance by compressing chunks to one vector, and struggles with long-tail data the embedding model rarely saw.

## Bi-Encoder — What It Is

The first-stage retriever. Embeds query and documents separately, then compares the vectors using cosine similarity or dot product.

## Bi-Encoder — Why It Is Fast

Document vectors are pre-computed and stored. At query time only the query is freshly embedded, so search scales to millions.

## Bi-Encoder — Where It Falls Short

The model never sees query and document together, so it misses word-level interactions and ranks the candidate set coarsely.

## Cross-Encoder — What It Is

The second-stage reranker. Takes query and one document jointly into the same model pass and outputs one relevance score.

## Cross-Encoder Flow

Concatenate query and document, feed the pair into the transformer, get a score. Repeat for every candidate the bi-encoder returned.

## Cross-Encoder — Why It Is More Accurate

Query and document share a single forward pass, so the model captures deep word-level interactions a vector dot product cannot see.

## Cross-Encoder — Why It Is Slow

Embeddings cannot be pre-computed. Each new query needs a fresh model pass per candidate, so cost grows linearly with shortlist size.

## Bi-Encoder vs Cross-Encoder — The Trade

Bi-encoder: fast at scale, coarsely accurate. Cross-encoder: precise but slow. Use bi-encoder to filter, cross-encoder to rerank.

## Two-Stage Retrieval Architecture

Bi-encoder narrows millions of docs to hundreds quickly. Cross-encoder reranks those hundreds with fine-grained precision before generation.

## Why Two Stages Instead of One

Bi-encoder alone lacks precision. Cross-encoder alone is too slow at scale. Combining them buys both scalability and accuracy.

## Filter Stage

After reranking, drop low-score candidates, deduplicate, apply permissions, and cap the list to fit the LLM context window.

---

# 3. RAG Component Deep-Dive

**Source:** `week-two/day-two-rag-architecture.md`

## What RAG Stands For

Retrieval Augmented Generation. Pull relevant docs, attach them to the query, let the LLM generate a grounded answer.

## The Four Main Components

User query, knowledge database, retrieval step, context augmentation step. Each has a single responsibility you can reason about.

## Without RAG vs With RAG

Without: stale, no private data, more hallucination, no citations. With: fresh, grounded, traceable, updateable without retraining.

## Limitation 1 — No Proprietary Data

LLMs see only public data. Internal CRM, order history, and policies are invisible without retrieval at query time.

## Limitation 2 — Training Cutoff

Anything after the training date is invisible to the model. Retrieval is the only honest way to add freshness.

## Limitation 3 — Hallucinations

When a model does not know it invents confident-sounding wrong answers. Retrieved facts reduce the pressure to guess.

## Limitation 4 — Long-Tail Entity Recall

Rare entities appear too few times in training data to be learned well. Retrieval surfaces them on demand.

## Retrieval — Tabular (Text-to-SQL)

For SQL data. LLM writes SQL, engine runs it, LLM turns the rows back into a natural-language answer.

## Retrieval — Term-Based (BM25)

Classical keyword matching with rare-word weighting. Fast and exact for product codes; fails on synonyms and paraphrases.

## Retrieval — Embedding-Based

Semantic search via cosine similarity between query and chunk vectors. Handles synonyms and paraphrasing where BM25 fails.

## Retrieval — Hybrid Search

Run BM25 and embedding retrieval together, merge and rerank results. Default winning pattern in production RAG systems.

## Cosine Similarity

Measures angle between vectors, not magnitude. Near 1 means same direction and meaning; near 0 means unrelated content.

## Evaluation — Precision

Of the chunks retrieved, how many were actually relevant. Set-based; ignores the rank order of returned results.

## Evaluation — Recall

Of all the relevant chunks that exist, how many were retrieved. Recall@k is the key RAG metric.

## Evaluation — MRR

Mean Reciprocal Rank. How high is the first relevant result. Best for top-1 chatbot Q&A scenarios.

## Evaluation — NDCG

Normalized Discounted Cumulative Gain. Full rank-aware score weighting both position and relevance grade across the entire list.

## Where Metrics Fit

All four are offline, used during evaluation against a golden set, never on live production traffic for users.

## Chunking — Fixed Size — How It Works

Pick a chunk size in tokens, cut the document into consecutive pieces of that size, paired with a small overlap.

## Chunking — Fixed Size — Advantage

Simple to implement, fast to execute, almost no tuning needed. Good baseline when prototyping before investing in better strategies.

## Chunking — Fixed Size — Disadvantage

Splitter has no awareness of meaning, so it routinely cuts mid-sentence or mid-paragraph and destroys local semantic coherence.

## Chunking — Semantic — How It Works

Embed each sentence, keep adding to the current chunk while similar, close it when cosine similarity drops sharply.

## Chunking — Semantic — Advantage

Each chunk holds a single self-contained topic, so when a chunk matches a query it usually fully answers it.

## Chunking — Semantic — Disadvantage

The similarity-drop threshold is tricky. Too strict produces tiny fragmented chunks; too loose merges unrelated ideas together.

## Chunking — Recursive — How It Works

Split by paragraph first, then sentence, then word, only going deeper if the current piece still exceeds the size limit.

## Chunking — Recursive — Advantage

Respects natural document structure. Common production default because chunks stay coherent without manually tuning a similarity threshold.

## Chunking — Recursive — Disadvantage

More moving parts than fixed size. Tuning the separator hierarchy together with chunk size takes careful iteration on real documents.

## Chunking — Naive vs Late — Core Difference

Naive chunks first then embeds each chunk in isolation. Late embeds the whole document first then cuts the token embeddings.

## Why Late Chunking Wins

Pronouns and references survive the cut. Short chunks remain retrievable. Cutting in slightly wrong places hurts less.

## Late Chunking Trade-offs

Requires a long-context embedding model. Memory per pass grows; compute is similar or lower than naive.

## Query Pre-Processing — Why It Exists

Cheapest place to lift retrieval quality. The retriever can only do well on a well-shaped input query.

## Query Pre-Processing — Classification

Decide popular vs long-tail, broad vs narrow, factual vs reasoning. Different question types need different retrieval paths.

## Query Pre-Processing — Cleaning and Rewriting

Remove special characters, fix typos, lemmatize, and optionally step-back-prompt to broaden the question before searching.

## Query Pre-Processing — Expansion

Add synonyms, or use HyDE: LLM writes a hypothetical answer, embed that, search with the answer-shaped vector.

## Query Pre-Processing — Safety Check

Profanity filter, PII redaction, and topic relevance gate. Final guard before retrieval or LLM ever sees the query.

## Query Pre-Processing Order

Always classify, then clean, then expand, then safety-check. Each stage cheap on its own; together they boost quality significantly.

## Embedding Model — Why The Choice Matters

Hard to change later. Switching means re-embedding every document. Pick carefully because every retrieval depends on this mapping.

## Embedding Factor 1 — Relevance

Does the model rank truly relevant chunks at the top for your queries. Measure on your own golden set.

## Embedding Factor 2 — Domain Specificity

Specialised fields like law, medicine, finance often need domain-tuned models like LegalBERT, BioBERT, FinBERT for accuracy.

## Embedding Factor 3 — Performance vs Cost

Bigger models retrieve better but cost more in storage and latency. Mid-tier model plus reranker usually wins.

## Embedding Factor 4 — Language Support

Multilingual corpora need multilingual models. English-only model on multilingual data is a common silent retrieval failure.

## Embedding Factor 5 — Hosting

API services are convenient but send data out. Self-hosted open-source gives privacy and control with operational overhead.

## Vector DB — Pinecone

Fully managed SaaS. Handles billions, zero DevOps, predictable performance. Trade-off: paid service and data on their infrastructure.

## Vector DB — Chroma

Open-source, Python-native, ideal up to about ten million vectors. Best choice for prototyping, demos, and internal tools.

## Vector DB — Qdrant

Open-source, production-grade. Scales like Pinecone but you run the cluster. Self-hosted control instead of managed convenience.

## Vector DB Decision Rule

Chroma for building. Pinecone for renting. Qdrant for owning. Pick the convenience-control-cost point that fits the situation.

---

# 4. Six RAG Design Questions

**Source:** `week-two/day-two-rag-summary.md`

## Q1 — Query Preprocessing

Classify, clean, expand, safety-check. Cheapest place to improve retrieval quality before touching embeddings, retrievers, or rerankers.

## Q2 — Which Embedding Model

Balance relevance, domain, cost, languages, hosting. Validate on a golden set with Recall@k and NDCG@k against candidates.

## Q3 — Chunking Strategy

Recursive is default. Reach for semantic when topic boundaries matter, late chunking when cross-chunk references matter.

## Q4 — Which Vector DB

Chroma for prototyping under ten million vectors, Pinecone for managed production, Qdrant for self-hosted production at scale.

## Q5 — Retrieval Strategy

SQL for tabular rows, BM25 for exact terms, embeddings for meaning, hybrid search when both literal and semantic matter.

## Q6 — How to Evaluate

Precision and Recall for coarse quality, MRR for top-1 questions, NDCG for full ranking, all offline on golden set.

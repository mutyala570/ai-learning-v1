# Week 2 — Day 2: RAG Architecture (Video 2)

## Slides Covered in This Document

### Slide 1 — Retrieval Augmented Generation (Overview)
1. [**What RAG Stands For**](#what-rag-stands-for)
2. [**The Core Idea in One Line**](#the-core-idea-in-one-line)
3. [**The Four Main Components**](#the-four-main-components)
4. [**End-to-End Flow**](#end-to-end-flow)
5. [**Why Context Augmentation is the Key Step**](#why-context-augmentation-is-the-key-step)
6. [**Without RAG vs With RAG**](#without-rag-vs-with-rag)

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

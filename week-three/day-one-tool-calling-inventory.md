# Week 3 — Day 1: Tool Calling & Inventory Case Study (Video 1)

**Agenda:** Part A — Tool Calling (deep dive). Part B — Inventory Case Study.

## Slides Covered in This Document

### Slide 1 — Why We Need Tool Calling
1. [**The Core Problem**](#the-core-problem)
2. [**The Four Gaps**](#the-four-gaps)
3. [**What Tool Calling Solves**](#what-tool-calling-solves)

### Slide 2 — End-to-End Tool Calling Sequence
1. [**The Four Actors**](#the-four-actors)
2. [**The Flow — Eight Messages**](#the-flow--eight-messages)
3. [**Why the Agent Sits in the Middle**](#why-the-agent-sits-in-the-middle)

---

# Slide 1 — Why We Need Tool Calling

A plain LLM is capable at one thing — generating text from patterns it learned during training — but it is sealed off from the live world. Tool calling is what bridges that gap.

## The Core Problem

An LLM is a frozen function. Text in, text out, with no built-in ability to look anything up, change anything, or compute anything outside its own weights. Everything it knows was baked in at training and stops updating the moment training ends. For a casual chatbot this is fine; for a product where the user asks *"what is my order status"* or *"what is the weather today"*, the answer simply does not live in the weights.

## The Four Gaps

1. **No live data.** Frozen at training cutoff — current prices, today's stock, the user's latest order, this morning's news are all invisible. The model can only guess, and the guess sounds confident even when wrong.
2. **No actions.** LLMs only generate text. They cannot send an email, create a record, or update a row. A request like *"reorder product X"* is an action, not an information question — the model can advise but never do.
3. **No reliable computation.** LLMs are bad at arithmetic and worse at applying business rules consistently. For *"total value of all pending orders for branch B"*, the right answer is a SQL query or calculator, not a smarter prompt.
4. **No access to private systems.** LLMs are trained on public data and have no view into the CRM, order DB, or internal wiki. **RAG** handles the document side of this gap; **tool calling** handles the live-system side.

## What Tool Calling Solves

The LLM stays in its lane — reasoning over text — but gains the ability to **request** external operations like *"fetch this order"* or *"send this email"*. The application executes the request and feeds the result back into the model's context for synthesis. The LLM never touches the database or API directly, but its answers are now grounded in live data, real computation, and real actions, while the application controls what is allowed to run. That separation is what makes tool calling both **useful** and **safe**.

---

# Slide 2 — End-to-End Tool Calling Sequence

A sequence diagram of one full tool-calling round, drawn across four columns: **Task**, **Agent**, **Model**, **Tool**. The Agent sits in the middle as the orchestrator. The Model never calls Tools directly — it only decides which Tool to use and asks the Agent to run it.

## The Four Actors

**Task** is the user's request entering the system from outside. **Agent** is the orchestrator that receives the Task, talks to the Model, runs Tool calls on the Model's behalf, and feeds results back; all routing and execution control lives here. **Model** is the LLM — it reasons over text and decides which Tool to call and with what arguments, but never executes Tools itself. **Tool** is the external function or API that actually does the work — query the DB, call the weather service, send the email — and only sees its own arguments and result.

## The Flow — Eight Messages

The diagram shows eight messages in order:

1. **Task → Agent.** The user sends a request into the system. The Agent now owns the round.
2. **Agent → Model: Task + Tools.** The Agent forwards the Task along with the full list of Tool definitions (name, description, parameter schema), so the Model knows both what to do and what is available.
3. **Model → Agent: which Tool to use.** The Model decides whether a Tool is needed and replies with the Tool name plus arguments. This is a decision, not an execution.
4. **Agent → Tool: tool call.** The Agent actually runs the chosen Tool with the chosen arguments. Permissions, validation, and rate limits are enforced here before the Tool runs.
5. **Tool → Agent: tool result.** The Tool returns its raw output (JSON, number, row). The Agent now holds the live data the Model needed but did not have.
6. **Agent → Model: Task + Tool result.** The Agent makes a second call to the Model, this time including both the original Task and the Tool result. This re-injection is what makes the Tool's output useful — without it the Model never sees what came back.
7. **Model → Agent: done.** With both pieces in context, the Model produces the final natural-language answer and signals completion.
8. **Agent → out: final answer.** The Agent returns the answer to whoever sent the original Task. The Model–Tool round-trip in the middle is invisible to the user.

## Why the Agent Sits in the Middle

The Model never talks to the Tool directly, and the Tool never talks to the Model directly — both speak only through the Agent. That triangulation gives the Agent three powers: it **enforces safety** (deciding which Tool calls are allowed before running them), it **shapes context** (deciding how much of the Tool result to feed back into the Model), and it **loops** — steps 2 through 6 can repeat with different Tools until the Model says "done". Multi-step agent reasoning is just this same diagram with more loops in the middle, not a different architecture.

---

# Week 3 — Day 1: Tool Calling & Inventory Case Study (Video 1)

This file is the home for today's Week 3 Day 1 session. The session has two parts on the agenda — a deep dive on **Tool Calling** and an **Inventory Case Study** that applies it to a real B2B problem. I will fill in the slide-by-slide notes while watching; the pre-session context section below is the bridge from what I already know (Week 2 covered the basics of function calling) to what the video is about to layer on top.

> **How to use this file while watching:** keep the "Slide N — TBD" placeholders open, add the slide title and notes as each slide appears, and jot any question that pops into the **Discussion Points** section at the bottom. Then come back here to discuss with me.

## Topics Covered in This Document

1. [**Pre-Session Context — What I Already Know**](#1-pre-session-context--what-i-already-know)
2. [**Agenda for This Session**](#2-agenda-for-this-session)
3. [**Part A — Tool Calling (Deep Dive)**](#3-part-a--tool-calling-deep-dive)
4. [**Part B — Inventory Case Study**](#4-part-b--inventory-case-study)
5. [**Discussion Points (Fill After Watching)**](#5-discussion-points-fill-after-watching)
6. [**Connection to My Qwipo Project**](#6-connection-to-my-qwipo-project)

---

# 1. Pre-Session Context — What I Already Know

Week 2 already introduced **function calling / tool use** as the mechanism that lets an LLM reach external systems. Today's video is a deeper pass on the same topic, so I want this section to be the anchor — when the video says "step 3 of the tool-call loop", I can map it onto what I already learned. Anything new in the video should attach to a node here, not float.

## 1.1 The Six-Step Tool Calling Flow (from Week 2)

### 1.1.1 Step 1 — Define Tools as Schemas

Every tool is registered with a **name**, a **description**, and a **parameter schema**. The LLM reads these descriptions and uses them to decide when each tool is appropriate.

### 1.1.2 Step 2 — Send Message + Tool List

The user message and the full list of available tool definitions are sent to the LLM in one call.

### 1.1.3 Step 3 — LLM Decides

The LLM either answers directly from training or returns a structured JSON requesting a specific tool with specific arguments.

### 1.1.4 Step 4 — Application Executes

**The LLM does not run the tool itself.** Your application receives the tool-call request and actually runs the function — calls the API, queries the DB, sends the email. This separation is what makes tool use safe.

### 1.1.5 Step 5 — Send Result Back

The tool's output is sent back to the LLM in a follow-up call so the model has the result in its context.

### 1.1.6 Step 6 — LLM Synthesises Final Response

With the tool result now in context, the LLM produces the natural-language answer for the user.

## 1.2 RAG vs Tools — Why Inventory Belongs to the Tool Path

From Week 2's decision rule: **static document knowledge → RAG, live/dynamic/action → Tool, user-specific → Memory**. Inventory data is **live and dynamic** — stock counts change every minute as orders come in and out — so inventory questions belong on the **tool path**, not the RAG path. That is exactly why the case study is paired with tool calling rather than with the RAG slides from Week 2.

## 1.3 What I Expect to Learn New Today

I do not know the slides yet, but based on the agenda I would expect the deeper tool-calling pass to cover at least: how schemas are written in practice (JSON Schema specifics, required vs optional fields, type hints), how the LLM picks between **multiple** tools, how parallel/concurrent tool calls work, what to do when a tool errors, and how to keep cost/latency under control when several tool calls chain. The inventory case study should then put all of this into a worked end-to-end example.

---

# 2. Agenda for This Session

## 2.1 Part A — Tool Calling (Deep Dive)

A more detailed pass on tool calling than the Week 2 introduction. Likely covers schema design, multi-tool selection, parallel calls, error handling, and patterns for keeping the loop bounded.

## 2.2 Part B — Inventory Case Study

A worked example where tool calling answers real B2B inventory questions — stock checks, low-stock alerts, reorder triggers, branch-level availability. The case study makes the abstract tool-calling flow concrete on a problem similar to my Qwipo project.

---

# 3. Part A — Tool Calling (Deep Dive)

> Fill in the slide title and notes as each slide appears. Use full sentences in the body, not bullet dumps. If a slide has multiple sub-topics, break each into its own `##` sub-heading inside the slide.

## 3.1 Slide 1 — TBD

*Add slide title once it appears. Then write the explanation in your own words — what the slide says, why it matters, and how it connects to the Week 2 six-step flow above.*

## 3.2 Slide 2 — TBD

*Add slide title and explanation here.*

## 3.3 Slide 3 — TBD

*Add slide title and explanation here.*

## 3.4 Slide 4 — TBD

*Add slide title and explanation here.*

## 3.5 Slide 5 — TBD

*Add slide title and explanation here.*

> Add more `## 3.N Slide N — TBD` blocks below if the part has more slides than placeholders. Renumber if needed.

---

# 4. Part B — Inventory Case Study

> Same approach — fill in slides as they appear. Pay extra attention to: which tools are defined, what each tool's schema looks like, what data each tool returns, how the agent loop chains them, and how the final answer is composed.

## 4.1 Slide 1 — TBD

*Add slide title and explanation here.*

## 4.2 Slide 2 — TBD

*Add slide title and explanation here.*

## 4.3 Slide 3 — TBD

*Add slide title and explanation here.*

## 4.4 Slide 4 — TBD

*Add slide title and explanation here.*

## 4.5 Slide 5 — TBD

*Add slide title and explanation here.*

> Add more slides below if needed.

---

# 5. Discussion Points (Fill After Watching)

A scratch area for things to bring back to the chat. Phrase each one as a real question, not a topic, so it is ready to discuss.

## 5.1 Conceptual Questions

*e.g. "Does the LLM see the tool's full output, or only a summary the application chooses to pass back?"*

- TBD
- TBD

## 5.2 Implementation Questions

*e.g. "How does the LLM behave if two tools have overlapping descriptions?"*

- TBD
- TBD

## 5.3 Comparison Questions

*Anything that contrasts with what I learned in Week 2 — places the video disagrees with, refines, or extends the earlier material.*

- TBD

## 5.4 "Did I understand this right?" Checks

*Short statements I want to verify with the chat. Useful when something *seems* clear but I am not 100 percent sure.*

- TBD

---

# 6. Connection to My Qwipo Project

The whole reason this video matters is the Qwipo Order & Logistics agent. Tool calling is the mechanism the agent will use to reach `bms-order-service` and `logistics-*` services for live data, and inventory is one of the first realistic intents the agent will need to handle. This section is where I link today's lesson to the real project so I do not lose the thread.

## 6.1 Which Project Milestones This Unblocks

### 6.1.1 M4 — Single Tool

The first real implementation milestone after the FastAPI skeleton (M1) and intent classifier (M2). The video's concrete tool examples should let me design my first tool's schema and call loop.

### 6.1.2 M5 — Multi-Tool Agent Loop

If the video covers multi-tool selection and parallel calls, that maps directly onto M5. Note here anything the video says about loop termination, max iterations, and confidence thresholds.

## 6.2 Inventory-Specific Tools I Probably Need

Based on the case study, sketch the tools I think my Qwipo agent will need. These are guesses; the video will sharpen them.

- **`get_stock_for_product(product_id, branch_id)`** — current on-hand stock at a branch.
- **`get_low_stock_items(branch_id, threshold)`** — products below threshold.
- **`get_order_status(order_id)`** — the existing M0 use case but as a tool.
- **TBD** — add or correct after watching.

## 6.3 Open Decisions This Video Might Resolve

From the dashboard `goal/README.md`:

- [ ] Final intent list — confirm draft `order_status | cancellation | policy_qa | small_talk | out_of_scope` (the case study might add **inventory** as a first-class intent → before M2).
- [ ] Primary LLM choice — the video's tool-calling examples may favour one provider's schema → before M5.

---

> **After watching:** ping me with "done with day 1" and we will walk through the Discussion Points section together, then update `goal/04-learning-status.md` to reflect what was covered.

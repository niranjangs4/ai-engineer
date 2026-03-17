# 🏗️ SYSTEM ARCHITECTURE (DETAILED)

## 🧠 Architectural Philosophy

This system is designed as a **Cognitive Autonomous Agent**, not a traditional automation framework.

It follows:

* **Agentic Architecture**
* **Closed-loop reasoning (ReAct)**
* **Memory-augmented intelligence (RAG)**
* **Failure-aware execution**
* **Self-improving feedback loop**

---

# 🔷 1. HIGH-LEVEL ARCHITECTURE

```text
                         ┌────────────────────────────┐
                         │         USER INTENT        │
                         │   (Natural Language Goal)  │
                         └────────────┬───────────────┘
                                      ↓
                         ┌────────────────────────────┐
                         │        PLANNER LAYER       │
                         │  (LLM-based decomposition) │
                         └────────────┬───────────────┘
                                      ↓
                         ┌────────────────────────────┐
                         │     EXECUTION PLANNER      │
                         │   (Structured Step Plan)   │
                         └────────────┬───────────────┘
                                      ↓
     ┌──────────────────────────────────────────────────────────────┐
     │              COGNITIVE EXECUTION ENGINE (ReAct)              │
     │                                                              │
     │   ┌──────────┐   ┌──────────┐   ┌────────────┐               │
     │   │ THINK    │→→│ ACTION   │→→│ EXECUTION  │               │
     │   └──────────┘   └──────────┘   └────┬───────┘               │
     │                                     ↓                       │
     │                               ┌──────────┐                  │
     │                               │ OBSERVE  │                  │
     │                               └────┬─────┘                  │
     │                                     ↓                       │
     │                               ┌──────────┐                  │
     │                               │ EVALUATE │                  │
     │                               └────┬─────┘                  │
     │                                     ↑                       │
     └─────────────────────────────────────┘───────────────────────┘
                                          ↓
                         ┌────────────────────────────┐
                         │    ACTION EXECUTION LAYER  │
                         │      (Playwright Engine)   │
                         └────────────┬───────────────┘
                                      ↓
                         ┌────────────────────────────┐
                         │        APPLICATION UI      │
                         └────────────────────────────┘
```

---

# 🔷 2. SUPPORTING INTELLIGENCE SYSTEMS

These operate **parallel to execution** and enhance system intelligence.

```text
                ┌──────────────────────────────┐
                │        RAG MEMORY            │
                │  - Selector learning         │
                │  - Confidence scoring        │
                └─────────────▲────────────────┘
                              │
                              │
                ┌─────────────┴────────────────┐
                │        VALIDATION LAYER      │
                │  - Tool validation           │
                │  - Selector verification     │
                └─────────────▲────────────────┘
                              │
                              │
                ┌─────────────┴────────────────┐
                │     FAILURE COLLECTION       │
                │  - Screenshot capture        │
                │  - DOM snapshot              │
                └─────────────▲────────────────┘
                              │
                              │
                ┌─────────────┴────────────────┐
                │       VISION INTELLIGENCE    │
                │  - Error detection           │
                │  - Root cause inference      │
                │  - Bug report generation     │
                └──────────────────────────────┘
```

---

# 🔷 3. LAYERED ARCHITECTURE

## 🧠 Layer 1: Intent & Planning Layer

**Responsibility:**

* Convert natural language goal → structured execution plan

**Components:**

* Planner LLM (`golden_prompts.py`)

**Output:**

```text
Step-by-step executable plan
```

---

## 🔁 Layer 2: Cognitive Execution Layer (ReAct Engine)

**Responsibility:**

* Dynamic decision making
* Adaptive execution
* Retry and recovery

**States:**

```text
START → THOUGHT → ACTION → EXECUTE → OBSERVE → EVALUATE → DONE
```

---

## 🎯 Layer 3: Selector Intelligence Layer

**Core innovation of the system**

### Multi-tier Strategy:

```text
1. RAG selector (historical knowledge)
2. LLM selector (contextual reasoning)
3. Healed selector (DOM-based recovery)
```

---

### Healing Algorithm:

```text
Input Selector
   ↓
Compare with DOM elements
   ↓
Score:
   - Exact match
   - Partial match
   - Token similarity
   ↓
Return best match
```

---

## ⚙️ Layer 4: Execution Layer

**Responsibility:**

* Perform actual browser actions

**Technology:**

* Playwright (sync API)

---

## 📚 Layer 5: Memory Layer (RAG)

**Responsibility:**

* Store execution knowledge
* Retrieve best selectors

---

### Memory Structure:

```json
{
  "action": "click login",
  "selector": "button:has-text('Sign In')",
  "confidence": 0.8,
  "page": "login"
}
```

---

### Retrieval Strategy:

```text
Semantic similarity + confidence weighting
```

---

## 👁 Layer 6: Vision Intelligence Layer

**Triggered when:**

* Execution fails after retries

---

### Capabilities:

* Detect UI errors
* Identify blocking states
* Extract visible text
* Generate structured bug reports

---

## 🛡 Layer 7: Validation Layer

**Ensures:**

* Valid tool usage
* Valid selectors (DOM or RAG)

---

## 📸 Layer 8: Observability Layer

**Captures:**

* Screenshots
* DOM state
* Execution context

---

# 🔷 4. EXECUTION CONTROL FLOW (DETAILED)

```text
FOR each step:

  THINK:
    → Analyze goal + DOM + history

  ACTION:
    → Decide action_type + selector

  EXECUTE:
    → Resolve selectors (RAG → LLM → Heal)
    → Try execution loop

  IF success:
    → Store in RAG
    → Continue

  IF failure:
    → Retry (max 2)

  IF repeated failure:
    → Capture evidence
    → Run vision analysis
    → Stop if critical

  OBSERVE:
    → Capture outcome

  EVALUATE:
    → Decide next transition
```

---

# 🔷 5. DATA FLOW ARCHITECTURE

```text
Goal
 ↓
Planner
 ↓
Execution Plan
 ↓
ReAct Engine
 ↓
Selector Resolution
 ↓
Executor → Browser
 ↓
Result
 ↓
 ├── Success → Learn (RAG)
 └── Failure → Vision Analysis
```

---

# 🔷 6. FEEDBACK & LEARNING LOOP

```text
Execution Success
   ↓
Extract selector
   ↓
Store in RAG
   ↓
Increase confidence
   ↓
Prioritize next time
```

---

# 🔷 7. DESIGN PATTERNS USED

* ReAct Pattern (Reason + Act loop)
* RAG (Memory Augmentation)
* Strategy Pattern (Selector resolution)
* Observer Pattern (Execution feedback)
* Retry + Circuit Breaker logic

---

# 🔷 8. SCALABILITY & EXTENSIBILITY

The system is designed to support:

* New tools (plug-and-play)
* Multi-application support
* Multi-model LLM integration
* Future CI/CD integration
* Distributed execution (future-ready)

---

# 🔷 9. ARCHITECTURAL DIFFERENTIATION

```text
Traditional Automation:
   Script → Execute → Fail

This System:
   Think → Decide → Adapt → Learn → Improve
```

---

# 🔷 10. ARCHITECTURAL MATURITY

This framework demonstrates:

* Autonomous agent design
* AI-native system thinking
* Resilient execution model
* Continuous learning loop
* Intelligent failure recovery

---

# 💡 FINAL ARCHITECTURE SUMMARY

```text
Planner + ReAct Engine + RAG Memory + Self-Healing + Vision Intelligence

= Autonomous QA Agent System
```

---

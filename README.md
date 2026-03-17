# 🚀 Agentic QA Framework

### Self-Healing AI Test Automation (ReAct + RAG + Vision)

---

# 📌 Overview

The **Agentic QA Framework** is an intelligent automation system that transforms traditional test automation into an **AI-driven autonomous agent**.

Instead of writing static scripts, this system:

* Understands goals
* Plans steps dynamically
* Executes actions intelligently
* Learns from past executions
* Heals failures automatically

---

# 🎯 What Problem It Solves

Traditional automation:

* ❌ Breaks when UI changes
* ❌ Hardcoded selectors
* ❌ No learning
* ❌ Manual maintenance

This system:

* ✅ Self-heals selectors
* ✅ Learns from previous runs (RAG)
* ✅ Uses reasoning (ReAct loop)
* ✅ Detects UI errors using Vision AI

---

# 🧠 Core Concepts Used

* **ReAct Pattern** → Reason + Act loop
* **RAG (Retrieval-Augmented Generation)** → Memory-based learning
* **Self-Healing Automation** → Fix broken selectors
* **Vision AI** → Screenshot-based failure analysis
* **Tool-based Execution** → Modular action system

---

# 🏗️ Architecture Overview

## 🔷 High-Level Flow

```text
                ┌──────────────────────┐
                │       USER GOAL      │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │     PLANNER (LLM)    │
                └─────────┬────────────┘
                          ↓
                ┌──────────────────────┐
                │   EXECUTION PLAN     │
                └─────────┬────────────┘
                          ↓
                ┌─────────────────────────────────────┐
                │      REACT EXECUTION ENGINE         │
                │                                     │
                │ THINK → ACT → EXECUTE → OBSERVE     │
                │                ↺                    │
                └─────────┬───────────────────────────┘
                          ↓
            ┌─────────────┴──────────────┐
            │                            │
     SUCCESS PATH                 FAILURE PATH
            │                            │
            ↓                            ↓
   Next Step Execution        Retry → Heal → Analyze
                                         ↓
                               ┌──────────────────┐
                               │   VISION AGENT   │
                               └────────┬─────────┘
                                        ↓
                               Bug Report / Stop
```

---

## 🔷 Supporting Systems

```text
RAG Memory         → selector learning
Validator          → prevent invalid actions
Failure Collector  → logs + screenshots
Vision Agent       → error detection + bug report
```

---

# 🔁 DETAILED EXECUTION FLOW (VERY IMPORTANT)

## 🧠 Step-by-Step Runtime Flow

```text
START
  ↓
User provides GOAL
  ↓
Browser opens application
  ↓
RAG Memory Search (context)
  ↓
Planner generates steps
  ↓
FOR EACH STEP:
```

---

## 🔄 ReAct Loop Execution

```text
STATE: START
  ↓
STATE: THOUGHT
  → Extract DOM
  → Build semantic DOM
  → Generate prompt
  → Call LLM
  → Get decision (action_type, selector, value)
```

---

```text
STATE: ACTION
  → Validate LLM output
  → If invalid → retry (max 2)
```

---

```text
STATE: EXECUTE

  1. Get candidate selectors:
     - RAG selector
     - LLM selector
     - Healed selector

  2. Remove empty selectors

  3. Detect repeated actions (avoid loops)

  4. Try each selector:
        → validate
        → execute

  5. If success:
        → store in history
        → learn in RAG

  6. If failure:
        → retry (max 2)

  7. If still failure:
        → capture screenshot
        → run vision analysis
        → stop if critical error
```

---

```text
STATE: OBSERVE
  → Capture result
```

---

```text
STATE: EVALUATE
  → If success → mark step complete
  → Else → stop step
```

---

```text
NEXT STEP → repeat
  ↓
END
```

---

# 🎯 SELECTOR STRATEGY (CORE INNOVATION)

```text
Priority Order:

1. RAG selector (learned from past)
2. LLM selector (current decision)
3. Healed selector (DOM similarity)
```

---

## 🔧 Self-Healing Logic

```text
Input selector → compare with DOM text
   ↓
Find best match:
   - exact match
   - partial match
   - keyword match
   ↓
Return closest working selector
```

---

# 📚 RAG MEMORY SYSTEM

## What it Stores

```json
{
  "action": "click login",
  "selector": "button:has-text('Sign In')",
  "confidence": 0.7
}
```

---

## How it Works

```text
Before execution:
   → search similar actions

After success:
   → store selector
   → increase confidence

Future runs:
   → reuse selector first
```

---

# 👁 VISION FAILURE ANALYSIS

Triggered when:

* Action fails after retries

---

## Flow:

```text
Failure detected
   ↓
Take screenshot
   ↓
Send to Vision Model
   ↓
Detect:
   - error messages
   - UI issues
   - blocking problems
   ↓
Generate structured bug report
```

---

# ⚙️ COMPONENT BREAKDOWN

## 🧠 Planner (`golden_prompts.py`)

* Converts goal → steps

---

## 🔁 ReAct Engine (`react_pipeline.py`)

* Core brain of system
* Handles:

  * reasoning
  * retries
  * execution flow

---

## 📚 RAG Memory (`rag_memory.py`)

* Stores selectors
* Improves stability over time

---

## ⚙️ Executor (`agentic_web_qa.py`)

* Executes Playwright actions

---

## 👁 Vision Agent (`vision_agent.py`)

* Analyzes failure screenshots

---

## 🛡 Validator (`action_validator.py`)

* Prevents invalid actions

---

## 📸 Failure Collector (`failure_collector.py`)

* Captures logs + screenshots

---

# 🔄 CONTROL FLOW SUMMARY

```text
FOR each step:

THINK
 → LLM decides action

ACT
 → validate action

EXECUTE
 → try selectors (RAG → LLM → heal)

IF success:
 → store in memory

IF fail:
 → retry

IF still fail:
 → vision analysis
 → stop if critical
```

---

# 🧠 LEARNING LOOP

```text
Success
 ↓
Store selector
 ↓
Increase confidence
 ↓
Reuse next time
```

---

# 🧪 SAMPLE GOAL

```text
open zodiac application and login and verify dashboard
```

---

# 🧰 TECH STACK

* Python
* Playwright
* Ollama (LLM runtime)
* Sentence Transformers
* NumPy

---

# 🤖 MODELS USED

```text
Planner      → llama3.1
Executor     → qwen2.5
Vision       → qwen2.5vl
Code Gen     → deepseek-coder
```

---

# ⚠️ LIMITATIONS

* Depends on visible UI text
* LLM output variability
* Vision model may misinterpret UI
* Single-thread execution

---

# 🔮 FUTURE IMPROVEMENTS

* Multi-tab handling
* API validation
* Dashboard reporting
* CI/CD integration
* Parallel execution

---

# 🎤 HOW TO EXPLAIN IN INTERVIEW (IMPORTANT)

Say this:

```text
"This framework is an agentic automation system built on the ReAct pattern.

The planner converts a goal into steps.
The ReAct pipeline executes each step using reasoning.

Selectors are resolved using a 3-level strategy:
RAG memory, LLM output, and DOM-based healing.

Execution is done via Playwright, and failures are handled using retries,
logging, and vision-based analysis.

The system continuously learns using RAG, making future executions more stable."
```

---

# 💡 ONE-LINE SUMMARY

```text
Traditional Automation → Script-based
This System → AI Agent-based Automation
```

---

# 🚀 FINAL NOTE

This is not just a framework.

👉 This is a **Self-Learning Autonomous QA Agent**

---

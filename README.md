# Week 8 — Combined Agent (Planner + ReAct)

## Goal

Build a **Combined AI Agent** that integrates:

* Planner
* ReAct reasoning
* Tool registry
* Executor
* Memory
* Self-reflection

This architecture is similar to how modern agent frameworks operate.

---

# Why a Combined Agent?

So far we built different types of agents:

| Week  | Agent Type    |
| ----- | ------------- |
| Week5 | Tool Agent    |
| Week6 | Planner Agent |
| Week7 | ReAct Agent   |

Each solved a different problem.

Now we combine them into **one intelligent system**.

---

# Combined Agent Architecture

```text
User Request
     │
     ▼
Planner
(task decomposition)
     │
     ▼
Step Executor
     │
     ▼
ReAct Reasoning
     │
     ▼
Dynamic Tool Selection
     │
     ▼
Tool Registry
     │
     ▼
Tool Execution
     │
     ▼
Observation
     │
     ▼
Self Reflection
     │
     ▼
Memory Update
     │
     ▼
Final Result
```

---

# Component Overview

## Planner

The planner converts a user request into a list of steps.

Example:

User request:

```
Automate login feature
```

Planner output:

```
Step1 Generate testcases
Step2 Generate automation
Step3 Run tests
Step4 Analyze failures
Step5 Generate report
```

---

# ReAct Reasoning

Inside each step the agent can reason dynamically.

ReAct loop:

```
Thought
Action
Observation
```

Example:

```
Thought: Need Playwright automation
Action: generate_automation
Observation: automation script created
```

---

# Tool Registry

Tools are stored in a registry.

Example:

```
generate_testcases
generate_automation
run_tests
analyze_failures
generate_report
```

Instead of hardcoding logic, the agent selects tools dynamically.

---

# Executor

The executor runs each step created by the planner.

Example:

```
Step1 → generate_testcases
Step2 → generate_automation
Step3 → run_tests
```

---

# Memory

Memory stores outputs between steps.

Example structure:

```
memory["testcases"]
memory["automation"]
memory["test_results"]
memory["analysis"]
```

This allows later steps to reuse earlier results.

---

# Self Reflection

The agent reviews its own output and improves results.

Example:

```
Observation: Test failed

Reflection:
Selector changed

Action:
Update automation code
```

---

# Example Combined Agent Workflow

User request:

```
Automate login feature
```

Agent workflow:

```
Planner
↓
Generate testcases
↓
Generate automation
↓
Run tests
↓
Observe failures
↓
Analyze failures
↓
Generate report
```

Inside steps the agent can reason dynamically using ReAct.

---

# Example Realistic Agent Behavior

```
User: Automate login feature
```

Agent:

```
Step1 Generate testcases
Step2 Generate automation
Step3 Run tests
```

Execution:

```
Running tests...
2 failures detected
```

Reflection:

```
Locator outdated
```

Agent fixes automation and reruns tests.

---

# Technologies Used

Language:

Python

Local LLM runtime:

Ollama

Libraries:

requests

---

# Learning Outcomes

By completing Week 8 you will understand:

```
Combined agent architecture
Planner + ReAct integration
Dynamic tool selection
Agent memory usage
Self-reflection workflows
```

These concepts are foundational for **autonomous AI systems**.

---

# Learning Progress

Roadmap so far:

```
Week1 Python CLI AI
Week2 Chat assistant
Week3 Embeddings
Week4 RAG system
Week5 Tool agents
Week6 Planner agents
Week7 ReAct agents
Week8 Combined agents
```

---

# Next Step

Next we will implement:

```
week8/combined_agent.py
```

This will be the **first autonomous multi-capability agent in your project**.

# Week 7 — ReAct Agent Implementation

## Goal

Build an AI agent that can **reason, take actions, observe results, and iterate until the task is solved**.

This approach is called the **ReAct Pattern**.

ReAct stands for:

```
Reason + Act
```

This pattern allows an AI agent to **think step-by-step while solving a problem**.

---

# What is the ReAct Pattern?

The ReAct pattern allows an AI agent to **reason about a task before deciding what action to take**.

Instead of a single step:

```
User → LLM → Answer
```

The system becomes:

```
User
 ↓
Thought
 ↓
Action
 ↓
Observation
 ↓
Next Thought
 ↓
Final Answer
```

This loop continues until the task is complete.

---

# ReAct Agent Workflow

```
User Question
      │
      ▼
Thought (reason about problem)
      │
      ▼
Action (select tool)
      │
      ▼
Observation (tool result)
      │
      ▼
Next Thought
      │
      ▼
Final Answer
```

---

# Example ReAct Reasoning

User request:

```
What browsers does Playwright support?
```

Agent reasoning:

```
Thought: I need documentation about Playwright
Action: search_docs
Observation: Playwright supports Chromium Firefox WebKit
Thought: I now know the answer
Final Answer: Playwright supports Chromium Firefox WebKit
```

---

# Another Example (Math)

User question:

```
What is 45 * 12?
```

Agent reasoning:

```
Thought: This is a math calculation
Action: calculator
Observation: 540
Thought: I now know the answer
Final Answer: 540
```

---

# ReAct Architecture

```
            User
             │
             ▼
       LLM Reasoning
             │
             ▼
        Select Tool
             │
             ▼
        Execute Tool
             │
             ▼
        Observation
             │
             ▼
        Next Reasoning
             │
             ▼
         Final Answer
```

---

# Components of a ReAct Agent

A ReAct agent typically contains the following components:

```
LLM Reasoning Engine
Tool Registry
Executor
Observation Loop
Memory
```

---

# Tool Examples

Tools allow the agent to interact with external systems.

Examples:

```
calculator
search_docs
generate_testcases
generate_automation
run_tests
analyze_failures
generate_report
```

Each tool performs a specific task.

---

# ReAct vs Planner Agent

| Feature     | Planner Agent     | ReAct Agent       |
| ----------- | ----------------- | ----------------- |
| Planning    | creates task plan | dynamic reasoning |
| Execution   | sequential steps  | iterative loop    |
| Flexibility | structured tasks  | adaptive tasks    |

Example Planner workflow:

```
Plan → Execute Step1 → Execute Step2 → Result
```

Example ReAct workflow:

```
Thought → Action → Observation → Thought → Result
```

---

# Combined Agent Architecture

Modern AI systems combine both **Planner and ReAct patterns**.

Example architecture:

```
User Request
      │
      ▼
Planner Agent
      │
      ▼
Step Execution
      │
      ▼
ReAct Reasoning inside each step
      │
      ▼
Tool Execution
      │
      ▼
Final Result
```

This combination is used in frameworks like:

```
LangGraph
CrewAI
```

---

# Example for QA Automation Agent

User request:

```
Automate login feature
```

Planner creates steps:

```
Step1 Generate testcases
Step2 Generate automation
Step3 Run tests
Step4 Analyze failures
Step5 Generate report
```

Inside Step3 the agent may use ReAct reasoning:

```
Thought: Tests failed
Action: analyze_failures
Observation: locator changed
Thought: Update selector
Action: fix automation
```

---

# Learning Objectives

By completing Week 7 you will learn:

```
ReAct reasoning pattern
Agent decision loops
Dynamic tool selection
Observation-based reasoning
```

These skills are essential for building **advanced AI agents**.

---

# Learning Progress

Roadmap progress:

```
Week1  Python CLI AI tool
Week2  Chat assistant
Week3  Embeddings
Week4  RAG system
Week5  Tool agents
Week6  Planner agents
Week7  ReAct agents
```

---

# Next Step

Next we will implement:

```
week7/react_agent.py
```

This script will demonstrate a **working ReAct reasoning loop**.

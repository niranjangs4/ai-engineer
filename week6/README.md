# Week 6 — Planner Agent (Multi-Step Agent)

## Goal

Build an AI agent that can **break a task into multiple steps and execute them sequentially**.

Unlike simple agents that answer a question directly, a **Planner Agent creates a structured plan and executes each step**.

---

# What is a Planner Agent?

A planner agent is an AI system that:

1. Understands a user request
2. Creates a task plan
3. Executes steps one by one
4. Produces a final result

Basic workflow:

```
User Request
↓
Planner (LLM)
↓
Task Plan
↓
Execute Step 1
↓
Execute Step 2
↓
Execute Step 3
↓
Final Result
```

Planner agents are commonly used for:

* automation pipelines
* coding assistants
* workflow automation
* AI developer tools

---

# Planner Agent Architecture

```
                User Request
                     │
                     ▼
               Planner (LLM)
                     │
                     ▼
                 Task Plan
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Step1       Step2       Step3
      Tool        Tool        Tool
        │           │           │
        ▼           ▼           ▼
      Executor → Executor → Executor
                     │
                     ▼
                 Final Result
```

---

# Components of the Planner Agent

A planner agent typically contains **four core components**.

```
1 Planner
2 Tools
3 Executor
4 Memory
```

---

# 1. Planner

The planner is responsible for **breaking a user request into steps**.

Example input:

```
Generate Playwright automation for login feature
```

Planner output:

```
Step1 Generate testcases
Step2 Generate automation code
Step3 Validate code
```

The planner is usually powered by an LLM such as:

* Ollama models like `phi3` or `mistral`

---

# 2. Tools

Tools are functions that perform real work.

Examples:

```
generate_testcases()
generate_code()
search_docs()
calculator()
```

Example execution:

```
Step1 → generate_testcases
Step2 → generate_code
```

Tools allow the agent to interact with the **real world**.

---

# 3. Executor

The executor runs the steps **in sequence**.

Example:

```
Step1 run generate_testcases
Step2 run generate_code
Step3 run validation
```

The executor ensures each step completes before moving to the next.

---

# 4. Memory

Memory stores results from earlier steps.

Example:

```
Testcases generated
↓
Used to generate automation code
```

Memory allows the agent to **reuse information across steps**.

---

# Example Planner Agent Workflow

User request:

```
Generate automation for login feature
```

Planner generates steps:

```
1 Generate testcases
2 Generate automation code
3 Validate code
```

Execution:

```
Step1 generate_testcases()
Step2 generate_code()
Step3 validate_code()
```

Final result:

```
Automation script ready
```

---

# Planner Agent vs ReAct Agent

| Feature         | ReAct Agent            | Planner Agent        |
| --------------- | ---------------------- | -------------------- |
| Reasoning style | dynamic loop           | predefined plan      |
| Execution       | step-by-step reasoning | structured workflow  |
| Best for        | research & exploration | automation pipelines |

Example ReAct reasoning:

```
Thought → Action → Observation
```

Example Planner workflow:

```
Plan → Execute steps
```

---

# Week 6 Implementation Plan

You will implement the planner agent in:

```
week6/planner_agent.py
```

The agent will:

```
1 Understand the user request
2 Generate a task plan
3 Execute each step
4 Return the final output
```

---

# Example Interaction

User input:

```
Generate Playwright test for login
```

Agent output:

```
Plan created:

Step1 Generate testcases
Step2 Generate automation code
Step3 Validate script
```

Execution:

```
Running Step1...
Running Step2...
Running Step3...
```

Final result:

```
Playwright automation script generated successfully
```

---

# Tools Used

| Purpose  | Tool   |
| -------- | ------ |
| Language | Python |
| LLM      | Ollama |

Later extensions may include:

```
Vector databases
Automation tools
Jira integration
```

---

# Learning Outcomes

By completing Week 6 you will understand:

```
Planner agents
Task decomposition
Multi-step AI workflows
Tool execution pipelines
```

These are core skills for building **advanced AI agents**.

---

# Learning Progress

Your journey so far:

```
Week1  Python CLI AI tool
Week2  Chat assistant
Week3  Embeddings and vector search
Week4  RAG systems
Week5  Tool agents and reasoning
Week6  Planner agents
```

---

# Next Step

Next stage of the roadmap:

```
Week7  Automation Agent
```

The agent will begin using real automation tools such as:

```
Generate testcases
Generate automation code
Run Playwright tests
Analyze failures
Generate reports
```

This moves toward the final goal:

```
AI QA Automation Engineer Agent
```

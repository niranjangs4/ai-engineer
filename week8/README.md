# Week 8 — Combined Agent Architecture (Planner + ReAct + Tools + Memory + Reflection)

This document summarizes the **Combined Agent architecture** and the **Agent Controller Pattern** implemented in Week-8.

The goal of this stage is to build an AI system that combines all previous capabilities into **one coordinated intelligent agent**.

---

# Goal of Week 8

Create a **Combined AI Agent** capable of:

* Planning tasks
* Executing steps
* Using tools dynamically
* Storing results in memory
* Reflecting on outputs
* Producing a final result

This architecture is similar to the systems used in modern AI agent frameworks.

---

# Agent Evolution So Far

Your learning progression:

```text
Week1  Python CLI AI tool
Week2  Chat assistant
Week3  Embeddings
Week4  RAG system
Week5  Tool agents
Week6  Planner agents
Week7  ReAct agents
Week8  Combined agents
```

Each stage added a new capability.

---

# Combined Agent Architecture

The combined agent integrates multiple modules.

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

# Core Components

The combined agent contains six major components.

```text
1 Planner
2 Executor
3 ReAct reasoning
4 Tool registry
5 Memory
6 Reflection
```

Each component plays a specific role.

---

# Planner

The planner converts a user request into structured steps.

Example request:

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

The planner decides **what actions must be taken**.

---

# Executor

The executor runs each step sequentially.

Example execution pipeline:

```
Step1 → generate_testcases
Step2 → generate_automation
Step3 → run_tests
Step4 → analyze_failures
Step5 → generate_report
```

The executor ensures tasks run **in the correct order**.

---

# ReAct Reasoning

ReAct means:

```
Reason + Act
```

Inside each step the agent performs reasoning.

ReAct loop:

```
Thought
Action
Observation
```

Example:

```
Thought: Need automation code
Action: generate_automation
Observation: script generated
```

This allows the agent to **adapt dynamically**.

---

# Tool Registry

All tools are stored in a central registry.

Example tools:

```
generate_testcases
generate_automation
run_tests
analyze_failures
generate_report
```

Tool registry example:

```python
tools = {
    "generate_testcases": generate_testcases,
    "generate_automation": generate_automation,
    "run_tests": run_tests,
    "analyze_failures": analyze_failures,
    "generate_report": generate_report
}
```

This allows the agent to select tools dynamically.

---

# Memory

Memory stores outputs between steps.

Example memory structure:

```
memory["testcases"]
memory["automation"]
memory["test_results"]
memory["analysis"]
```

Example workflow:

```
Generate testcases
↓
Store in memory
↓
Generate automation using testcases
↓
Run tests
```

Memory enables **multi-step workflows**.

---

# Self Reflection

Reflection allows the agent to **evaluate its own output**.

Example:

```
Observation: Test failed
Reflection: Locator outdated
Action: Update automation
```

Reflection improves reliability.

---

# Example Combined Agent Workflow

User request:

```
Automate login feature
```

Agent pipeline:

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

Reflection may improve steps automatically.

---

# Example Execution

```
User: Automate login feature
```

Agent plan:

```
Step1 Generate testcases
Step2 Generate automation
Step3 Run tests
Step4 Analyze failures
Step5 Generate report
```

Execution example:

```
Running tests...
2 tests passed
1 failed
```

Reflection:

```
Locator changed
```

Agent updates automation and produces final report.

---

# Agent Controller Pattern

As agents become complex, a **central controller** is used to orchestrate all modules.

Controller architecture:

```
User
 ↓
Agent Controller
 ↓
Planner
 ↓
Executor
 ↓
Tools
 ↓
Memory
 ↓
Reflection
```

The controller coordinates the entire system.

---

# Controller Responsibilities

The controller performs the following actions:

```
Receive user request
Create task plan
Execute steps
Manage memory
Run reflection
Return final result
```

This design keeps the system modular.

---

# Example Controller Flow

User request:

```
Automate login feature
```

Controller pipeline:

```
Planner → generate steps
↓
Executor → run step1
↓
Reflection → evaluate result
↓
Memory → store outputs
↓
Next step
↓
Final result
```

---

# Example Controller Implementation

Example simplified structure:

```python
class AgentController:

    def __init__(self):
        self.memory = {}

    def run(self, user_request):

        plan = create_plan(user_request)
        steps = parse_steps(plan)

        for step in steps:

            result = execute_step(step, user_request)
            reflection = reflect(result)

            self.memory[step] = result

        return generate_report()
```

The controller orchestrates the entire workflow.

---

# Benefits of Controller Pattern

Advantages:

```
Cleaner architecture
Modular components
Easy debugging
Scalable system
Production-ready structure
```

Most advanced agent systems use an **orchestrator or controller layer**.

---

# Final Combined Agent Architecture

```
User Request
      │
      ▼
Agent Controller
      │
      ▼
Planner
      │
      ▼
Executor
      │
      ▼
ReAct Reasoning
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
Reflection
      │
      ▼
Memory
      │
      ▼
Final Result
```

---

# Learning Outcomes

After completing Week-8 you understand:

```
Combined agent architecture
Planner + ReAct integration
Dynamic tool selection
Tool registry pattern
Agent memory
Self-reflection workflows
Agent controller orchestration
```

These are the building blocks for **advanced AI agents**.

---

# Next Stage

Next stage of the roadmap:

```
Week9 — Automation Agent
```

This agent will interact with **real automation tools** such as:

```
Playwright
Test execution
Failure analysis
Report generation
```

This will move the system toward the final goal:

```
AI QA Automation Engineer Agent
```

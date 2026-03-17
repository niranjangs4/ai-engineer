# Week 11 — Model Fine-Tuning

## Goal

Understand how to **train or fine-tune a language model for a specific task**.

Instead of relying only on prompts or external documents, the model itself learns **new behavior from data**.

Fine-tuning allows the model to become specialized for tasks like:

```text
Testcase generation
Automation code generation
Bug analysis
QA documentation assistance
```

---

# What is Model Fine-Tuning?

Fine-tuning means **continuing training on a smaller task-specific dataset**.

Original training:

```text
Large dataset
↓
General language model
```

Fine-tuning:

```text
General model
+
Custom dataset
↓
Specialized model
```

The new model learns your **domain knowledge and task patterns**.

---

# Example

General model prompt:

```text
Write testcases for login
```

Output may be generic.

Fine-tuned model trained with QA datasets:

```text
Input:
Generate testcases for login feature

Output:
TC1 Valid login
TC2 Invalid password
TC3 Locked account
TC4 Empty fields
```

The model learns **how QA engineers write testcases**.

---

# Fine-Tuning vs RAG

Both techniques add knowledge to AI systems but work differently.

| Method      | How it works                         |
| ----------- | ------------------------------------ |
| RAG         | retrieves information from documents |
| Fine-tuning | changes the model behavior itself    |

Example comparison:

```text
RAG
↓
Model + external knowledge
```

```text
Fine-tuning
↓
Model internal knowledge updated
```

Most production systems combine both.

---

# Training Pipeline

Typical fine-tuning pipeline:

```text
Dataset
↓
Data formatting
↓
Tokenization
↓
Training
↓
Evaluation
↓
New model
```

---

# Example Dataset Format

Instruction-response format is common.

Example dataset:

```json
{
  "instruction": "Generate Playwright test for login",
  "response": "test('login', async ({page}) => {...})"
}
```

Another example:

```json
{
  "instruction": "Write testcases for checkout feature",
  "response": "TC1 Successful payment..."
}
```

These examples teach the model how to respond.

---

# Tools for Fine-Tuning

Common open-source tools include:

```text
HuggingFace Transformers
PEFT (Parameter Efficient Fine Tuning)
LoRA
QLoRA
```

These techniques allow training models on **consumer GPUs**.

---

# Local Training Architecture

```text
Dataset
      │
      ▼
Tokenizer
      │
      ▼
Base Model
      │
      ▼
Fine-Tuning Method (LoRA / QLoRA)
      │
      ▼
New Model
```

The result is a **task-specialized AI model**.

---

# Example QA Training Dataset

Example dataset for automation tasks:

```text
Instruction:
Generate Playwright automation for login

Response:
test('login', async ({page}) => {

  await page.goto('/login')

  await page.fill('#username','user')

  await page.fill('#password','pass')

  await page.click('#login')

})
```

After training the model can generate similar scripts.

---

# Why Fine-Tuning is Useful

Benefits:

```text
Better domain understanding
More consistent outputs
Less prompting required
Custom behavior
```

This is useful when building **specialized AI assistants**.

---

# When to Use Fine-Tuning

Fine-tuning is useful when:

```text
You have large domain datasets
You want consistent outputs
You need specific task behavior
```

RAG is better when:

```text
Knowledge changes frequently
Documents are large
You need real-time updates
```

Most advanced systems combine both.

---

# Example Combined System

Modern AI systems often combine:

```text
Fine-Tuned Model
+
RAG Knowledge Base
+
Agents
```

Architecture:

```text
User Request
      │
      ▼
Agent
      │
      ▼
RAG Retrieval
      │
      ▼
Fine-Tuned Model
      │
      ▼
Final Response
```

This approach powers many enterprise AI systems.

---

# Learning Outcomes

By completing Week-11 you will understand:

```text
What training means
Fine-tuning pipelines
Instruction datasets
Parameter efficient training
Domain-specific AI models
```

These skills are important for **building specialized AI assistants**.

---

# Learning Progress

Roadmap progress:

```text
Week1  Python CLI AI
Week2  Chat assistant
Week3  Embeddings
Week4  RAG system
Week5  Tool agents
Week6  Planner agents
Week7  ReAct agents
Week8  Combined agents
Week9  Automation agents
Week10 RAG QA assistant
Week11 Model fine-tuning
```

---

# Next Stage

Final stage of the roadmap:

```text
Week12 Autonomous QA Engineer
```

In this stage the system will combine:

```text
Agents
Automation tools
RAG
Fine-tuned models
```

to create a **fully autonomous AI QA assistant**.

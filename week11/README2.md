# Week 11 – LoRA Fine-Tuning with Phi-2

## Overview

In Week 11 we implemented **parameter-efficient fine-tuning (LoRA)** on the **Microsoft Phi-2** language model to create a small domain-specific AI assistant for generating **software testing test cases**.

The goal was to understand the full fine-tuning workflow:

Dataset → LoRA Training → Adapter Weights → Inference

Instead of retraining the entire model, **LoRA (Low Rank Adaptation)** updates only a small number of parameters in attention layers, making training faster and memory-efficient.

---

## Technologies Used

* Python
* PyTorch
* HuggingFace Transformers
* TRL (SFTTrainer)
* PEFT (LoRA adapters)
* CUDA GPU acceleration

Model:

* Microsoft Phi-2

GPU Used:

* NVIDIA RTX 3080 Ti Laptop GPU (16GB VRAM)

---

## Project Structure

week11/

│
├── dataset.json
├── train_lora.py
├── test_model.py
├── checking.py
├── phi2-lora/
│   └── checkpoint-3/
│       ├── adapter_config.json
│       ├── adapter_model.safetensors
│       ├── optimizer.pt
│       ├── scheduler.pt
│       ├── tokenizer.json
│       └── trainer_state.json
│
└── README.md

---

## Dataset Format

The dataset follows an **instruction tuning format**.

Example:

```
[
  {
    "instruction": "Generate testcases",
    "input": "Login feature",
    "output": "TC1 Valid login\nTC2 Invalid password\nTC3 Empty username"
  }
]
```

During training this is converted into a prompt format:

```
### Instruction:
Generate testcases

### Input:
Login feature

### Response:
TC1 Valid login
TC2 Invalid password
TC3 Empty username
```

---

## Training Pipeline

Steps performed in `train_lora.py`:

1. Load dataset using HuggingFace datasets
2. Load Phi-2 base model
3. Load tokenizer
4. Configure LoRA parameters
5. Use TRL `SFTTrainer` for supervised fine-tuning
6. Train adapters on GPU
7. Save LoRA checkpoint

---

## LoRA Configuration

```
LoraConfig(
 r=8,
 lora_alpha=16,
 target_modules=["q_proj","v_proj"],
 lora_dropout=0.05,
 bias="none",
 task_type="CAUSAL_LM"
)
```

Explanation:

* r → rank of adaptation matrix
* lora_alpha → scaling factor
* target_modules → layers to inject LoRA
* dropout → regularization

---

## GPU Acceleration

Training used CUDA GPU.

Verification:

```
import torch
print(torch.cuda.is_available())
```

Output:

```
CUDA available: True
GPU: NVIDIA GeForce RTX 3080 Ti Laptop GPU
```

GPU training significantly reduces training time.

---

## Training Output

Example training result:

```
train_runtime: 1.537 seconds
train_loss: 3.403
mean_token_accuracy: 0.4826
epoch: 3
```

Since the dataset contained only 3 examples, this run served as a **pipeline validation** rather than full model learning.

---

## Adapter Files

LoRA training produces small adapter files instead of full model weights.

Important files:

```
adapter_config.json
adapter_model.safetensors
```

These files contain the **LoRA learned parameters**.

---

## Inference

Inference loads the base model and attaches LoRA adapters.

Example (`test_model.py`):

```
base_model = "microsoft/phi-2"
lora_path = "./phi2-lora/checkpoint-3"

model = AutoModelForCausalLM.from_pretrained(base_model)
model = PeftModel.from_pretrained(model, lora_path)
```

Prompt example:

```
### Instruction:
Generate testcases

### Input:
Login feature
```

Example output:

```
Test Steps:
1. Navigate to login page
2. Enter valid credentials
3. Click login
4. Verify successful login

Status: Pass
```

---

## Key Learnings

* Understanding LoRA fine-tuning
* Efficient model adaptation without full retraining
* GPU acceleration using CUDA
* Using HuggingFace TRL for supervised fine-tuning
* Loading LoRA adapters for inference
* Creating instruction-based datasets

---

## Limitations

The training dataset was very small (3 samples).
For meaningful model improvements, datasets should contain:

* 100+ examples (minimum)
* 1000+ examples (recommended)

---

## Future Improvements

Next steps in the AI engineering roadmap:

* Increase dataset size
* Apply QLoRA (4-bit quantization)
* Fine-tune larger models (7B+)
* Implement RAG (Retrieval Augmented Generation)
* Build a UI with Gradio

---

## Summary

In Week 11 we successfully built a **domain-specific AI model for software testing assistance** using LoRA fine-tuning on Phi-2. This approach enables efficient customization of large language models while keeping training lightweight and scalable.

---

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, BitsAndBytesConfig
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer
import torch

model_name = "microsoft/phi-2"

# Load dataset
dataset = load_dataset("json", data_files="dataset.json")

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# Prepare model for QLoRA
model = prepare_model_for_kbit_training(model)
model.gradient_checkpointing_enable()

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

# Disable cache
model.config.use_cache = False

# Training config
training_args = TrainingArguments(
    output_dir="./phi2-lora",
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    num_train_epochs=3,
    fp16=False,
    bf16=False,
    logging_steps=5,
    dataloader_pin_memory=True
)


# Formatting function
def formatting_func(example):
    return example["text"]

# Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    args=training_args,
    peft_config=peft_config,
    processing_class=tokenizer,
    formatting_func=formatting_func
)

trainer.train()
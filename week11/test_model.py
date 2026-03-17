from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

base_model = "microsoft/phi-2"
lora_path = "./phi2-lora/checkpoint-3"

tokenizer = AutoTokenizer.from_pretrained(base_model)

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    trust_remote_code=True
).to("cuda")

model = PeftModel.from_pretrained(model, lora_path)

prompt = """### Instruction:
Generate testcases

### Input:
Login feature

### Response:
"""

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=120,
    temperature=0.3,
    top_p=0.9,
    do_sample=True
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
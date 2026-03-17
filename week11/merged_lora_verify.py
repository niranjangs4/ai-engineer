from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "./phi2-merged"

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16
).to(device)

# Set evaluation mode
model.eval()

# Compile model for faster inference (PyTorch 2.x)
model = torch.compile(model)

prompt = """### Instruction:
Generate testcases

### Input:
Login feature

### Response:
"""

inputs = tokenizer(prompt, return_tensors="pt").to(device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        temperature=0.3,
        top_p=0.9,
        do_sample=True
    )

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
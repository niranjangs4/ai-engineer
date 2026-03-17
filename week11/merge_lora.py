# from transformers import AutoModelForCausalLM, AutoTokenizer
# from peft import PeftModel
#
# base_model = "microsoft/phi-2"
# lora_path = "./phi2-lora/checkpoint-3"
#
# # Load tokenizer
# tokenizer = AutoTokenizer.from_pretrained(base_model)
#
# # Load base model
# model = AutoModelForCausalLM.from_pretrained(
#     base_model,
#     trust_remote_code=True
# )
#
# # Load LoRA adapter
# model = PeftModel.from_pretrained(model, lora_path)
#
# # Merge LoRA weights into base model
# model = model.merge_and_unload()
#
# # Save merged model
# model.save_pretrained("./phi2-merged")
# tokenizer.save_pretrained("./phi2-merged")
#
# print("Merged model saved!")

# GPU version
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

base_model = "microsoft/phi-2"
lora_path = "./phi2-lora/checkpoint-3"

# Detect device
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model)

# Load base model on GPU
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    trust_remote_code=True,
    torch_dtype=torch.float16
).to(device)

# Load LoRA adapter
model = PeftModel.from_pretrained(model, lora_path)

# Merge LoRA weights into base model
model = model.merge_and_unload()

# Move to CPU before saving (recommended)
model = model.to("cpu")

# Save merged model
model.save_pretrained("./phi2-merged")
tokenizer.save_pretrained("./phi2-merged")

print("Merged model saved!")
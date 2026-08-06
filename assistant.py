# Deprecated script for a single question and answer.

import os
os.environ["HF_HUB_DISABLE_XET"] = "1" # Disable XET as it can slow down downloads.

# import tokenizer and model classes
from transformers import AutoTokenizer, AutoModelForCausalLM
import huggingface_hub # for logging in to Hugging Face

# login to Hugging Face
token = os.environ["HF_TOKEN"]
huggingface_hub.login(token=token)

# instantiate tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct", token=token)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-3B-Instruct", token=token)

prompt = input("\nAsk anything: ") # ask for user prompt
print("Forming a response...", end="", flush=True)
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print("\r\n") # clear the loading text
print(response) # print the language model response
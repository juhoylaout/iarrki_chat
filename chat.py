import os
from getpass import getpass
os.environ["HF_HUB_DISABLE_XET"] = "1" # Disable XET as it can slow down downloads.

# import tokenizer and model classes
from transformers import AutoTokenizer, AutoModelForCausalLM
import huggingface_hub # for logging in to Hugging Face

# login to Hugging Face
token = os.getenv("HF_TOKEN")
if token:
    print(f"Found token starting with: {token[:8]}...")
else:
    os.environ["HF_TOKEN"] = getpass("Enter your Hugging Face token (can be left empty): ")
    token = os.getenv("HF_TOKEN")

if token != "":
    huggingface_hub.login(token=token)

# Read the model name from file model.txt
f = open("model.txt", "r")
model_name = f.readline()
f.close()

# instantiate tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
model = AutoModelForCausalLM.from_pretrained(model_name, token=token)

print("\nWelcome to the chat!")

while True:
    prompt = input("\nAsk anything or type 'exit' to exit: ") # ask for user prompt

    if prompt == "exit":
        break
    else:

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
            max_new_tokens=1024
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        print("\r\n") # clear the loading text
        print(response) # print the language model response
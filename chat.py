import os
from getpass import getpass
os.environ["HF_HUB_DISABLE_XET"] = "1" # Disable XET as it can slow down downloads.

# import tokenizer and model classes
from transformers import AutoTokenizer, AutoModelForCausalLM
import huggingface_hub # for logging in to Hugging Face

# Prompt login to Hugging Face Hub
try:
    huggingface_hub.whoami()
    print("Already logged in to Hugging Face.")
except Exception:
    choice = input("Not logged in. Log in? [y/N]: ")

    if choice.lower() == "y":
        token = getpass("Enter your Hugging Face token: ")
        huggingface_hub.login(token=token)
    else:
        print("Continuing without Hugging Face authentication.")

# Read the model name from file model.txt
f = open("model.txt", "r")
model_name = f.readline().strip()
f.close()

# instantiate tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("\nWelcome to Iarrki Chat! This AI tool is powered by Qwen3. Type 'T' to activate thinking mode.")
thinking_mode = False

while True:
    prompt = input("\nAsk anything or type 'exit' to exit: ") # ask for user prompt
    if prompt.lower() == "t":
        thinking_mode = True
        print("Thinking mode activated.")
        continue

    if prompt == "exit":
        break
    else:

        print("\nForming a response...", end="", flush=True)

        # prepare the model input
        messages = [
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=True # Switches between thinking and non-thinking modes. Default is True.
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        # conduct text completion
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=32768
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

        # parsing thinking content
        try:
            # rindex finding 151668 (</think>)
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0

        if thinking_mode:
            thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
            content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

            print("\rThinking content:", thinking_content)
            print("Content:", content)
        else:
            content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

            print("\r", content)
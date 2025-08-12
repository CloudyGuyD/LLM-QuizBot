from llama_cpp import Llama
from random import randint

def generate_until_stop(llm, prompt, stop_token=None, max_tokens=300): #basic generation without prompt engineering
    assert isinstance(llm, Llama), "must be a llama model"
    if stop_token is None: #give basic end token
        stop_token = [""]
    
    output = ""
    for response in llm(prompt, max_tokens=max_tokens, stream=True): #iterate over all streamed tokens
        text = response['choices'][0]['text'] #save the token
        print(text, end='', flush=True) #print the token for more appealing look during generation
        output += text
        # Check if output ends with any stop token
        if any(output.endswith(stop) for stop in stop_token):
            break
    return output


model_path = r"model\mistral-7b-instruct-v0.1-q4_k_m.gguf" 

llm = Llama(model_path=model_path, n_thread=8, verbose=False, flash_attn=True) #adjust for cpu cores, change as needed

# prompt = "Explain photosynthesis in relation to how it is a complex process." #sample prompt
# response = generate_until_stop(llm, prompt) #generate and print to terminal

def generate_quiz(llm, topic, num_questions=5):
    #creates a prompt featuring a topic, using JSON format for easy access to questions
    TF = randint(0, num_questions//2) # generate a random number of T/F questions, only up to half of the total number of questions
    prompt = f"""
    Create {TF} True/False questions, and {num_questions-TF} multiple-choice questions on the topic "{topic}" in **valid JSON**.
    Output only {num_questions} in JSON. Do not include explanations, instructions, or extra text.
    The JSON should be structured as:
    {{
        "quiz" : [
            {{
                "question" : "..."
                "options" : "..."
                "answer" : "..."
            }},
            {{
                "question" : "..."
                "options" : "..."
                "answer" : "..."
            }},
            ...
        ]
    }}
    """

    response = llm(prompt, max_tokens=500)

    return response
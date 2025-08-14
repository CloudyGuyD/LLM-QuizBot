from llama_cpp import Llama
from random import randint
import regex as re
import json
import time

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
seed = randint(0, 10000)
llm = Llama(model_path=model_path, n_thread=8, verbose=False, flash_attn=True, seed=seed, n_ctx=768) #adjust for cpu cores, change as needed
print("Model Loaded!")

# prompt = "Explain photosynthesis in relation to how it is a complex process." #sample prompt
# response = generate_until_stop(llm, prompt) #generate and print to terminal

def generate_quiz(llm, topic, num_questions=5):
    #creates a prompt featuring a topic, using JSON format for easy access to questions
    TF = randint(0, num_questions//2) # generate a random number of T/F questions, only up to half of the total number of questions
    prompt = f"""
    You are an expert quiz creator. Your goal is to create high-quality quiz questions based strictly on {topic}.  

    Instructions:  
    - Generate exactly {num_questions} questions:  
        1. {TF} True/False  
        2. {num_questions-TF} single/multiple-choice (1-4 correct answers)   
    - Each incorrect option must be plausible but wrong.  
    - Questions should be clear, concise, and unambiguous. Each question must have 3–5 options, including all correct answers.  
    - Answers must be chosen exactly from the corresponding "options" array, Do not paraphrase or invent new answers.
    - For questions containing 'not' or 'except', select the options that are factually not part of the correct group.
    - Format the output as **valid JSON** only. No explanations or extra text outside of JSON output.
    - Only output JSON. Nothing else. 
    - The JSON output should contain {num_questions} questions with a "question" field, {num_questions} "options" fields, and {num_questions} "answers" fields that includes correct answers only. The order of the questions does not matter.

    JSON schema:  
    {{
    "quiz": [
        {{
        "question": "question-string",
        "options": ["string", "string", ...],
        "answers": ["string", "string", ...] 
        }},
        {{
        "question": "string",
        "options": ["string", "string", ...],
        "answers": ["string", "string", ...] 
        }},
        ...
    ]
    }}
    """

    response = llm(prompt, max_tokens=500)

    return response

def extract_json(text):
    pat = re.compile(r'\{(?:(?>[^{}]+)|(?R))*\}', re.DOTALL)
    m = pat.search(text)
    if not m:
        raise ValueError("No JSON object found")
    quiz = json.loads(m.group(0))
    return quiz


enc = llm.tokenizer() #grab Llama tokenizer 
print("Beginning Generation:")
time0 = time.time()
response = generate_quiz(llm, "photosynthesis", num_questions=2)['choices'][0]['text']
time1 = time.time()
print(f"length of text: {len(enc.encode(response))} tokens")
print(f"generation time: {time1 - time0:.4f} seconds")
extracted = extract_json(response)
print(f"Question 1: {extracted['quiz'][0]['question']}")
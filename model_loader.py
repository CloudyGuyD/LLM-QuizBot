from llama_cpp import Llama

def generate_until_stop(llm, prompt, stop_token=None, max_tokens=300):
    assert isinstance(llm, Llama), "must be a llama model"
    if stop_token is None: #give basic end token
        stop_token = ""
    
    output = ""
    for response in llm(prompt, max_tokens=max_tokens, stream=True): #iterate over all streamed tokens
        text = response['choices'][0]['text'] #save the token
        print(text, end='', flush=True) #print the token for more appealing look during generation
        output += text
        # Check if output ends with any stop token
        if any(output.endswith(stop) for stop in stop_token):
            break
    return output


model_path = "model\mistral-7b-instruct-v0.1-q4_k_m.gguf"

llm = Llama(model_path=model_path, n_thread=8) #adjust for cpu cores

prompt = "Explain photosynthesis in relation to how it is a complex process."
response = generate_until_stop(llm, prompt) 
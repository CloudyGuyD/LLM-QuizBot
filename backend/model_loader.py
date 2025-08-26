from llama_cpp import Llama
import regex as re
import json
from backend.rag_utils import rag_text_to_chunks

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


def generate_quiz(llm, topic, num_questions=5, RAG=False, text=None):
    if (RAG and not text) or (not RAG and text is not None):
        raise ValueError("RAG and text arguments must both be empty or filled.")
    #creates a prompt featuring a topic, using JSON format for easy access to questions
    if RAG:
        context = rag_text_to_chunks(text=text, user_topic=topic)
        context = "\n\n".join(context)
        prompt_header = f"""You are an expert quiz creator. Your **only task** is to create a quiz based **strictly on the provided context**.

        **CRITICAL INSTRUCTIONS:**
        - **DO NOT** use any information outside of the provided context.
        - Every question, option, and answer **MUST** be derived directly from the text in the context below.
        - If the context is insufficient to create a full quiz, create as many questions as you can from the given text.
        - **DO NOT** make up questions about general knowledge topics like capitals or planets.

        ### CONTEXT ###
        {context}
        ### END CONTEXT ###
        """
    else:
        prompt_header = f"""You are an expert quiz creator. Your goal is to create high-quality quiz questions based strictly on {topic}."""  

    base_prompt = f"""
      Instructions:
      - Generate exactly {num_questions} questions based **only** on the context provided. 
      - Create a mix of question types. **Do not** make them all simple definitions. For example, ask about functions, relationships, or what a component is *not*.
      - For each question, generate 3-5 options.
      - The "answers" array must contain **all** the correct options.
      - The incorrect options (distractors) **must be plausible but definitively wrong** according to the provided context.
      - **CRITICAL**: The final output must be **only** a single, valid JSON object and nothing else. Do not add any text or explanations before or after the JSON.
      - The "answers" field should only have correct answers.

      JSON schema:
      {{
      "quiz": [
          {{
          "question": "question-string",
          "options": ["string", "string", ...],
          "answers": ["string", "string", ...]
          }},
          ...
      ]
      }}
      """
    
    prompt = prompt_header + base_prompt + "\n{" #concatenate prompt sections together, also primes the response
    stop = [
      "}]}",
      # Common variations with newlines and spaces
      "}]\n}",
      "}] }",
      "}\n]\n}",
      "} ] }",
      "} ]\n}",
      " }]}" 
      "}]}\n\n"
    ]
    response = llm(prompt, max_tokens=1500, temperature=0.4, stop=stop)
    return response

def extract_json(text):
    if not text.startswith("{"): # our prompt should start our output without this first brace
        text = "{" + text
    #use a regex pattern to recursively extract the json object
    pat = re.compile(r'\{(?:(?>[^{}]+)|(?R))*\}', re.DOTALL)
    m = pat.search(text)
    if not m: # if m is None
        raise ValueError("No JSON object found")
    quiz = json.loads(m.group(0)) # 0 will collect the entire match
    print("JSON extracted successfully!")
    return quiz


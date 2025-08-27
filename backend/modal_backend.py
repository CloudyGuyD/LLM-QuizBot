from modal import App, Image, asgi_app, Secret
import os


backend_path = os.path.dirname(__file__)
#define environment
image = (Image.from_registry(f"nvidia/cuda:12.2.0-devel-ubuntu22.04",add_python='3.12')
        .run_commands(
        "pip install https://github.com/abetlen/llama-cpp-python/releases/download/v0.3.16-cu122/llama_cpp_python-0.3.16-cp312-cp312-linux_x86_64.whl",
        "pip install torch --index-url https://download.pytorch.org/whl/cu121",
        "pip install huggingface_hub fastapi regex sentence_transformers"
        )
        .add_local_dir(local_path=backend_path, remote_path="/root/backend")
    )
app = App('quiz-generator-backend')


#model loading
class QuizModel:
    def __init__(self):
        from llama_cpp import Llama
        from huggingface_hub import hf_hub_download
        from random import randint

        model_path = hf_hub_download(
            repo_id="itlwas/Mistral-7B-Instruct-v0.1-Q4_K_M-GGUF",
            filename="mistral-7b-instruct-v0.1-q4_k_m.gguf"
        )
        seed = randint(0, 10000)
        self.llm = Llama(model_path=model_path, verbose=False, flash_attn=True, n_ctx=8192, n_gpu_layers=-1, seed=seed)
    
    def generate(self, text_content, topic, RAG=False):
        from backend.model_loader import generate_quiz, extract_json

        print("Generating quiz!")
        raw_output = generate_quiz(self.llm, topic, RAG=RAG, text=text_content)
        processed = extract_json(raw_output)
        return processed

#deploy the web server
@app.function(image=image, gpu='T4', secrets=[Secret.from_name("quiz-app-secret")], timeout=300)
@asgi_app()
def fastapi_app():
    from fastapi import FastAPI, Request, Header, HTTPException
    
    model = QuizModel()
    web_app = FastAPI()

    #get secret token from environment
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    
    @web_app.post("/generate")
    async def create_quiz(request: Request, authorization: str | None = Header(default=None)):
        if not authorization or authorization != f"Bearer {AUTH_TOKEN}":
            raise HTTPException(status_code=401, detail="Unauthorized")

        request_data = await request.json()
        quiz_json = model.generate(
            request_data['text_content'],
            request_data['topic'],
            request_data["RAG"]
        )
        return quiz_json
    return web_app
from modal import App, Image, asgi_app

#define environment
image = Image.debian_slim().pip_install("llama-cpp-python", "huggingface_hub", "fastapi")
app = App('quiz-generator-backend')

@app.function(image=image)
def dummy_quiz():
    #returns a dummy quiz for development purposes
    quiz = {
        "quiz": [
            {
            "question": "What is the capital of Japan?",
            "options": [
                "Beijing",
                "Seoul",
                "Tokyo",
                "Bangkok"
            ],
            "answers": ["Tokyo"]
            },
            {
            "question": "What is the chemical symbol for water?",
            "options": [
                "H2O",
                "CO2",
                "O2",
                "NaCl"
            ],
            "answers": ["H2O"]
            },
            {
            "question": "Which of the following are presidents of the United States?",
            "options": [
                "Thomas Jefferson",
                "Abraham Lincoln",
                "John Adams",
                "George Washington"
            ],
            "answers": ["Thomas Jefferson",
                "Abraham Lincoln",
                "John Adams",
                "George Washington"
                ]
            }
        ]
    }
    return quiz

#model loading
class QuizModel:
    def __enter__(self):
        from llama_cpp import Llama
        from huggingface_hub import hf_hub_download

        model_path = hf_hub_download(
            repo_id="itlwas/Mistral-7B-Instruct-v0.1-Q4_K_M-GGUF",
            filename="mistral-7b-instruct-v0.1-q4_k_m.gguf"
        )
        self.llm = Llama(model_path=model_path, n_ctx=8192, n_gpu_layers=-1)
    
    def generate(self, text_content, topic, RAG=False):
        print("Generating quiz!")
        return {
                "quiz": [
                    {
                    "question": "What is the capital of Japan?",
                    "options": [
                        "Beijing",
                        "Seoul",
                        "Tokyo",
                        "Bangkok"
                    ],
                    "answers": ["Tokyo"]
                    },
                    {
                    "question": "What is the chemical symbol for water?",
                    "options": [
                        "H2O",
                        "CO2",
                        "O2",
                        "NaCl"
                    ],
                    "answers": ["H2O"]
                    },
                    {
                    "question": "Which of the following are presidents of the United States?",
                    "options": [
                        "Thomas Jefferson",
                        "Abraham Lincoln",
                        "John Adams",
                        "George Washington"
                    ],
                    "answers": ["Thomas Jefferson",
                        "Abraham Lincoln",
                        "John Adams",
                        "George Washington"
                        ]
                    }
                ]
                }

#deploy the web server
@app.function(image=image, gpu='T4')
@asgi_app()
def fastapi_app():
    from fastapi import FastAPI, Request
    web_app = FastAPI()
    
    @web_app.post("/generate")
    async def create_quiz(request: Request):
        request_data = await request.json()
        model = QuizModel()
        quiz_json = model.generate(
            request_data['text_content'],
            request_data['topic'],
            request_data["RAG"]
        )
        return quiz_json
    return web_app
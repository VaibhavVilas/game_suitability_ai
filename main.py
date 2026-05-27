from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest
from graph import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AI Gaming Advisor Running 🚀"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    state = {
        "user_message": request.message
    }

    result = graph.invoke(state)

    return {
        "response": result["final_response"]
    }
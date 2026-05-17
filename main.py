from fastapi import FastAPI

from models import ChatRequest
from graph import graph

app = FastAPI()


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
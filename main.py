from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpcore import request
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

    # state = {
    #     "user_message": request.message
    # }

    conversation = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in request.messages
    ]

    latest_user_message = request.messages[-1].content

    state = {
        "messages": conversation,
        "user_message": latest_user_message
    }

    result = graph.invoke(state)

    return {
        "response": result["final_response"]
    }
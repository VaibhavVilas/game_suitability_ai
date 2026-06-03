from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models import ChatRequest
from graph import graph
from nodes import summarize_conversation, fetch_games_data, stream_response

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


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

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
        "user_message": latest_user_message,
        "games_data": [],
        "conversation_summary": ""
    }

    state = summarize_conversation(state)
    state = fetch_games_data(state)

    return StreamingResponse(
        stream_response(state),
        media_type="text/plain"
    )
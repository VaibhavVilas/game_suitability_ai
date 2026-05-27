from pydantic import BaseModel

# class ChatRequest(BaseModel):
#     message: str


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
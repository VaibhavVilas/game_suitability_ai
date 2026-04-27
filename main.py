from fastapi import FastAPI
from models import GameRequest
from graph import graph

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Game Suitability AI with IGDB is running 🚀"}


@app.post("/check-game")
def check_game(request: GameRequest):

    state = {
        "liked_games": request.liked_games,
        "difficulty": request.difficulty,
        "story_focus": request.story_focus,
        "game_to_check": request.game_to_check
    }

    result = graph.invoke(state)

    return {
        "game": request.game_to_check,
        "analysis": result["result"]
    }
from pydantic import BaseModel
from typing import List


class GameRequest(BaseModel):
    liked_games: List[str]
    difficulty: str
    story_focus: bool
    game_to_check: str
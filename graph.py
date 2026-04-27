from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

from nodes import analyze_player, fetch_game_data, llm_decision


class GameState(TypedDict):
    liked_games: List[str]
    difficulty: str
    story_focus: bool
    game_to_check: str
    game_data: Dict[str, Any]
    result: Dict[str, Any]


builder = StateGraph(GameState)

builder.add_node("analyze_player", analyze_player)
builder.add_node("fetch_game_data", fetch_game_data)
builder.add_node("llm_decision", llm_decision)

builder.set_entry_point("analyze_player")

builder.add_edge("analyze_player", "fetch_game_data")
builder.add_edge("fetch_game_data", "llm_decision")

graph = builder.compile()
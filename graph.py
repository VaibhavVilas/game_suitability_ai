from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

from nodes import (
    fetch_liked_games,
    build_player_profile,
    fetch_target_game,
    llm_decision
)


class GameState(TypedDict):
    liked_games: List[str]
    game_to_check: str
    liked_games_data: List[Dict[str, Any]]
    player_profile: Dict[str, Any]
    game_data: Dict[str, Any]
    result: Dict[str, Any]


builder = StateGraph(GameState)

builder.add_node("fetch_liked_games", fetch_liked_games)
builder.add_node("build_profile", build_player_profile)
builder.add_node("fetch_target", fetch_target_game)
builder.add_node("decision", llm_decision)

builder.set_entry_point("fetch_liked_games")

builder.add_edge("fetch_liked_games", "build_profile")
builder.add_edge("build_profile", "fetch_target")
builder.add_edge("fetch_target", "decision")

graph = builder.compile()
from typing import TypedDict

from langgraph.graph import StateGraph

from nodes import (
    fetch_games_data,
    generate_response
)


# ====================================================
# STATE
# ====================================================

class GameState(TypedDict):

    messages: list

    user_message: str

    games_data: list

    final_response: str


# ====================================================
# GRAPH
# ====================================================

builder = StateGraph(GameState)

builder.add_node(
    "fetch_games_data",
    fetch_games_data
)

builder.add_node(
    "generate_response",
    generate_response
)

builder.set_entry_point(
    "fetch_games_data"
)

builder.add_edge(
    "fetch_games_data",
    "generate_response"
)

builder.set_finish_point(
    "generate_response"
)

graph = builder.compile()
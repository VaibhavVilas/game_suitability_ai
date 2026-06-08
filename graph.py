# from typing import TypedDict

# from langgraph.graph import StateGraph

# from nodes import (
#     fetch_games_data,
#     generate_response
# )


# # ====================================================
# # STATE
# # ====================================================

# class GameState(TypedDict):

#     messages: list

#     user_message: str

#     games_data: list

#     final_response: str


# # ====================================================
# # GRAPH
# # ====================================================

# builder = StateGraph(GameState)

# builder.add_node(
#     "fetch_games_data",
#     fetch_games_data
# )

# builder.add_node(
#     "generate_response",
#     generate_response
# )

# builder.set_entry_point(
#     "fetch_games_data"
# )

# builder.add_edge(
#     "fetch_games_data",
#     "generate_response"
# )

# builder.set_finish_point(
#     "generate_response"
# )

# graph = builder.compile()


from typing import TypedDict

from langgraph.graph import StateGraph

from nodes import (
    fetch_games_data,
    summarize_conversation,
    classify_message,
    route_message,
    generate_response
)


# ==========================================
# STATE
# ==========================================

class GameState(TypedDict):

    user_message: str

    messages: list

    games_data: list

    conversation_summary: str

    message_type: str

    final_response: str


# ==========================================
# GRAPH
# ==========================================

builder = StateGraph(GameState)


builder.add_node(
    "summarize_conversation",
    summarize_conversation
)

builder.add_node(
    "classify_message",
    classify_message
)

builder.add_node(
    "fetch_games_data",
    fetch_games_data
)

builder.add_node(
    "generate_response",
    generate_response
)


# ==========================================
# FLOW
# ==========================================

builder.set_entry_point(
    "summarize_conversation"
)

builder.add_edge(
    "summarize_conversation",
    "classify_message"
)

builder.add_conditional_edges(
    "classify_message",
    route_message,
    {
        "recommendation": "fetch_games_data",
        "comparison":     "fetch_games_data",
        "general_question": "generate_response"
    }
)

builder.add_edge(
    "fetch_games_data",
    "generate_response"
)

builder.set_finish_point(
    "generate_response"
)

graph = builder.compile()
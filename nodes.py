# import requests
# import json
# from langchain_openai import ChatOpenAI
# from langchain.messages import HumanMessage
# from config import get_igdb_token, IGDB_CLIENT_ID


# # 🔹 Initialize LLM
# llm = ChatOpenAI(
#     model="gpt-4.1",
#     temperature=0.7
# )


# # 🔹 Node 1: Analyze Player (optional)
# def analyze_player(state):
#     return state


# # 🔹 Node 2: Fetch Game Data from IGDB
# def fetch_game_data(state):
#     game_name = state["game_to_check"]

#     token = get_igdb_token()

#     url = "https://api.igdb.com/v4/games"

#     headers = {
#         "Client-ID": IGDB_CLIENT_ID,
#         "Authorization": f"Bearer {token}"
#     }

#     query = f"""
#     search "{game_name}";
#     fields name,genres.name,rating,summary;
#     limit 1;
#     """

#     response = requests.post(url, headers=headers, data=query)
#     data = response.json()

#     if not data:
#         state["game_data"] = None
#         return state

#     game = data[0]

#     state["game_data"] = {
#         "name": game.get("name"),
#         "genres": [g["name"] for g in game.get("genres", [])] if game.get("genres") else [],
#         "rating": game.get("rating"),
#         "summary": game.get("summary", "")[:500]  # limit size
#     }
#     print("IGDB DATA:", state["game_data"])

#     return state


# # 🔹 Node 3: LLM Decision (REAL AI 🧠)
# def llm_decision(state):
#     game = state.get("game_data")

#     print("SENDING TO LLM:", game)

#     if not game:
#         state["result"] = {
#             "recommendation": "Game not found",
#             "reason": "Could not find this game in IGDB database"
#         }
#         return state

#     prompt = f"""
# You are a gaming recommendation expert.

# User Preferences:
# - Liked games: {state['liked_games']}
# - Preferred difficulty: {state['difficulty']}
# - Likes story: {state['story_focus']}

# Game Data:
# - Name: {game['name']}
# - Genres: {game['genres']}
# - Rating: {game['rating']}
# - Summary: {game['summary']}

# Task:
# Decide if the game is suitable.

# Respond ONLY in JSON:
# {{
#   "recommendation": "Highly Recommended / Recommended / Not Recommended",
#   "reason": "Short explanation"
# }}
# """

#     response = llm.invoke([HumanMessage(content=prompt)])

#     try:
#         state["result"] = json.loads(response.content)
#     except:
#         state["result"] = {
#             "recommendation": "Unknown",
#             "reason": response.content
#         }

#     return state


import requests
import json
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from config import get_igdb_token, IGDB_CLIENT_ID


llm = ChatOpenAI(model="gpt-4.1", temperature=0.7)


# 🔹 Helper: Fetch one game from IGDB
def fetch_single_game(game_name):
    token = get_igdb_token()

    url = "https://api.igdb.com/v4/games"

    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    query = f'''
    search "{game_name}";
    fields name,genres.name,rating,summary;
    limit 1;
    '''

    response = requests.post(url, headers=headers, data=query)
    data = response.json()

    if not data:
        return None

    game = data[0]
    print("single game",game)

    return {
        "name": game.get("name"),
        "genres": [g["name"] for g in game.get("genres", [])] if game.get("genres") else [],
        "rating": game.get("rating"),
        "summary": game.get("summary", "")[:300]
    }


# 🔹 Node 1: Fetch liked games data
def fetch_liked_games(state):
    liked_games = state["liked_games"]

    data = []
    for g in liked_games:
        game_data = fetch_single_game(g)
        if game_data:
            data.append(game_data)
    print("liked games", data)

    state["liked_games_data"] = data
    return state


# 🔹 Node 2: Build player profile (LLM)
def build_player_profile(state):
    liked_games_data = state["liked_games_data"]

    prompt = f"""
Analyze the user's gaming preferences based ONLY on these games:

{liked_games_data}

Return JSON:
{{
  "preferred_genres": [],
  "difficulty_preference": "...",
  "story_preference": "high/medium/low"
}}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        state["player_profile"] = json.loads(response.content)
    except:
        state["player_profile"] = {
            "preferred_genres": [],
            "difficulty_preference": "unknown",
            "story_preference": "unknown"
        }

    return state


# 🔹 Node 3: Fetch target game
def fetch_target_game(state):
    game_name = state["game_to_check"]
    state["game_data"] = fetch_single_game(game_name)
    return state


# 🔹 Node 4: Final LLM decision
def llm_decision(state):
    game = state.get("game_data")
    profile = state.get("player_profile")

    print(f"game : {game}, player : {profile}")

    if not game:
        state["result"] = {
            "recommendation": "Game not found",
            "reason": "Could not find this game in IGDB"
        }
        return state

    prompt = f"""
You MUST use the provided data only.

Player Profile:
{profile}

Game:
{game}

Decide if the game is suitable.

Return JSON:
{{
  "recommendation": "Highly Recommended / Recommended / Not Recommended",
  "reason": "Short explanation"
}}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        state["result"] = json.loads(response.content)
    except:
        state["result"] = {
            "recommendation": "Unknown",
            "reason": response.content
        }

    return state
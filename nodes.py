import requests
import json
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from config import get_igdb_token, IGDB_CLIENT_ID


# 🔹 Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)


# 🔹 Node 1: Analyze Player (optional)
def analyze_player(state):
    return state


# 🔹 Node 2: Fetch Game Data from IGDB
def fetch_game_data(state):
    game_name = state["game_to_check"]

    token = get_igdb_token()

    url = "https://api.igdb.com/v4/games"

    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    query = f"""
    search "{game_name}";
    fields name,genres.name,rating,summary;
    limit 1;
    """

    response = requests.post(url, headers=headers, data=query)
    data = response.json()

    if not data:
        state["game_data"] = None
        return state

    game = data[0]

    state["game_data"] = {
        "name": game.get("name"),
        "genres": [g["name"] for g in game.get("genres", [])] if game.get("genres") else [],
        "rating": game.get("rating"),
        "summary": game.get("summary", "")[:500]  # limit size
    }

    return state


# 🔹 Node 3: LLM Decision (REAL AI 🧠)
def llm_decision(state):
    game = state.get("game_data")

    if not game:
        state["result"] = {
            "recommendation": "Game not found",
            "reason": "Could not find this game in IGDB database"
        }
        return state

    prompt = f"""
You are a gaming recommendation expert.

User Preferences:
- Liked games: {state['liked_games']}
- Preferred difficulty: {state['difficulty']}
- Likes story: {state['story_focus']}

Game Data:
- Name: {game['name']}
- Genres: {game['genres']}
- Rating: {game['rating']}
- Summary: {game['summary']}

Task:
Decide if the game is suitable.

Respond ONLY in JSON:
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
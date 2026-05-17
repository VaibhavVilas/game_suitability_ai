import re
import requests

from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage

from config import get_igdb_token, IGDB_CLIENT_ID


llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.7,
    max_tokens=500
)


# ====================================================
# HELPER → EXTRACT GAME NAMES
# ====================================================

def extract_possible_games(text):

    prompt = f"""
Extract all video game names from this message.

Message:
{text}

Return ONLY comma separated game names.

Example:
Sekiro, Elden Ring, Bloodborne

If none found return:
NONE
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    content = response.content.strip()

    print("\nEXTRACTED GAMES:\n", content)

    if content == "NONE":
        return []

    games = [g.strip() for g in content.split(",")]

    return games


# ====================================================
# HELPER → FETCH GAME
# ====================================================

def fetch_single_game(game_name):

    token = get_igdb_token()

    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    query = f"""
    search "{game_name}";
    fields name,genres.name,rating,summary;
    limit 1;
    """

    response = requests.post(
        "https://api.igdb.com/v4/games",
        headers=headers,
        data=query
    )

    data = response.json()

    print("\nIGDB DATA:\n", data)

    if not data:
        return None

    game = data[0]

    return {
        "name": game.get("name"),
        "genres": [g["name"] for g in game.get("genres", [])] if game.get("genres") else [],
        "rating": game.get("rating"),
        "summary": game.get("summary", "")[:500]
    }


# ====================================================
# NODE 1 → FETCH ALL GAME DATA
# ====================================================

def fetch_games_data(state):

    user_message = state["user_message"]

    games = extract_possible_games(user_message)

    games_data = []

    for game in games:

        data = fetch_single_game(game)

        if data:
            games_data.append(data)

    state["games_data"] = games_data

    return state


# ====================================================
# NODE 2 → GENERATE RESPONSE
# ====================================================

def generate_response(state):

    games_data = state["games_data"]

    user_message = state["user_message"]

    # No games found
#     if len(games_data) == 0:

#         prompt = f"""
# You are a conversational gaming advisor.

# User Message:
# {user_message}

# Respond naturally.
# """

#     else:

    prompt = f"""
You are an expert gaming recommendation advisor.

Your job is NOT just to describe games.
Your job is to understand the user's gaming taste, habits, frustrations, and playstyle, then recommend games accordingly.

CORE BEHAVIOR:
- Be conversational, natural, and opinionated.
- Give direct recommendations instead of staying neutral.
- Explain WHY a game suits or does not suit the user.
- Focus heavily on gameplay feel, pacing, progression style, and player experience.
- Avoid generic summaries.

VERY IMPORTANT:
Understand the USER'S TASTE PROFILE.

Examples:
- If the user dislikes confusing maps, mention navigation friction.
- If the user prefers cinematic games, prioritize story pacing and immersion.
- If the user dislikes grinding or side quests, warn about open-world fatigue or level gating.
- If the user drops difficult games, warn about skill checks, parry systems, or punishing bosses.
- If the user likes linear games, mention whether progression is smooth or exploration-heavy.

IMPORTANT RECOMMENDATION FACTORS:
Always analyze:
- Story focus
- Gameplay pacing
- Exploration complexity
- Navigation/map clarity
- Combat difficulty
- RPG/system complexity
- Main story length
- Side quest dependence
- Whether the game respects a "main story only" playstyle
- Whether the game is casual-friendly or demanding

USE IGDB DATA:
Use the IGDB data heavily whenever possible:
- genres
- themes
- ratings
- summaries
- similar games
- gameplay style

DO NOT:
- Do not just list features.
- Do not sound like a review website.
- Do not recommend games blindly because ratings are high.
- Do not pretend every game suits every player.
- Do not overhype games.

BE HONEST:
- If a game is risky for the user, say so clearly.
- If the user may drop a game midway, explain why.
- If a game starts strong but becomes grindy later, mention it.
- If the game has pacing issues or confusing progression, warn them.

STYLE:
- Sound like a knowledgeable gamer friend.
- Be specific and insightful.
- Use comparisons to games the user already played whenever possible.

OUTPUT FORMAT:
1. Clear recommendation verdict
2. Why it suits / does not suit the user
3. Biggest strengths
4. Biggest risks/frustrations
5. Final recommendation

User Message:
{user_message}

IGDB Data:
{games_data}

Generate a detailed personalized gaming recommendation response.
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    state["final_response"] = response.content

    return state
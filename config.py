import os
from dotenv import load_dotenv
import requests

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IGDB_CLIENT_ID = os.getenv("IGDB_CLIENT_ID")
IGDB_CLIENT_SECRET  = os.getenv("IGDB_CLIENT_SECRET")
MAX_TOKENS = 200

_token_cache = {"token": None}

def get_igdb_token():
    if _token_cache["token"]:
        return _token_cache["token"]

    url = "https://id.twitch.tv/oauth2/token"

    params = {
        "client_id": IGDB_CLIENT_ID,
        "client_secret": IGDB_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, params=params)
    data = response.json()

    if "access_token" not in data:
        raise Exception(f"IGDB TOKEN ERROR: {data}")

    _token_cache["token"] = data["access_token"]

    return _token_cache["token"]
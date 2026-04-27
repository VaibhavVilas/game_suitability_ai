import os
from dotenv import load_dotenv
import requests

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IGDB_CLIENT_ID = os.getenv("IGDB_CLIENT_ID")
IGDB_CLIENT_SECRET  = os.getenv("IGDB_CLIENT_SECRET")


# 🔑 Get IGDB access token dynamically
def get_igdb_token():
    url = "https://id.twitch.tv/oauth2/token"

    params = {
        "client_id": IGDB_CLIENT_ID,
        "client_secret": IGDB_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, params=params)
    data = response.json()

    return data["access_token"]
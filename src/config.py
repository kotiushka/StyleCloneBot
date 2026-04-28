from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
BACKEND_URL = getenv("BACKEND_URL")
OPENAI_KEY = getenv("OPENAI_API_KEY")

DATABASE_URL = getenv("DATABASE_URL")

CHANNEL_ID = getenv("CHANNEL_ID")

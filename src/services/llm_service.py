from openai import AsyncOpenAI

from src.config import OPENAI_KEY
from src.models.schemas import UserMessage
from src.prompts.templates import get_prompt

client = AsyncOpenAI(api_key=OPENAI_KEY)

async def generate_reply(message: UserMessage, history: list[dict], mirror_user_name: str, example_messages: list[str]) -> str:

    response = await client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=get_prompt(message, history, mirror_user_name, "\n".join(f"- {msg}" for msg in example_messages)),
        reasoning_effort="low",
    )


    return response.choices[0].message.content

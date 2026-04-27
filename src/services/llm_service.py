from openai import AsyncOpenAI

from src.config import OPENAI_KEY
from src.models.schemas import UserMessage
from src.prompts.templates import get_prompt

client = AsyncOpenAI(api_key=OPENAI_KEY)

async def generate_reply(message: UserMessage):

    conversation = client.conversations.create()
    print(f"conversation: {conversation}")

    response = await client.chat.completions.create(
        model="gpt-5.4-nano",
        messages=get_prompt(message),
        reasoning_effort="low",
        conversation=conversation
    )


    return response.choices[0].message.content

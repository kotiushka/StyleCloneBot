from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import httpx

from src.config import EXAMPLE_MESSAGES, MIRROR_USER_NAME
from src.models.schemas import UserMessage

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("""
<b>Привет! Я StyleMirror 🪞</b>

<i>Я умею отвечать в стиле конкретного человека.
                         
Просто напиши мне любое сообщение — и я отвечу так, как ответил бы он. </i>                        
""")

@router.message(Command("help"))
async def cmd_help(message: Message):
    ...

@router.message(F.text)
async def handle_text(message: Message, http_client: httpx.AsyncClient):
    
    payload = UserMessage(user_id=message.from_user.id, username=message.from_user.username,
                          first_name=message.from_user.first_name, message_text=message.text,
                          mirror_user_name=MIRROR_USER_NAME, example_messages=EXAMPLE_MESSAGES)

    response = await http_client.post("/chat", json=payload.model_dump())
    
    data = response.json()
    await message.answer(data["response"])

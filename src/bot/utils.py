from aiogram import Bot

from src.config import CHANNEL_ID

async def is_subscribed(bot: Bot, user_id: int) -> bool:
    member = await bot.get_chat_member(
        chat_id=CHANNEL_ID,
        user_id=user_id
    )
    return member.status in ("member", "administrator", "creator")
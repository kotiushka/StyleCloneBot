from aiogram import Bot

async def is_subscribed(bot: Bot, user_id: int) -> bool:
    member = await bot.get_chat_member(
        chat_id="@trycatchlife",
        user_id=user_id
    )
    return member.status in ("member", "administrator", "creator")
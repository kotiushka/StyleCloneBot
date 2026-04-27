import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import httpx

import logging

from aiogram.client.default import DefaultBotProperties

from src import config
from src.bot.handlers import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    
    dp["http_client"] = httpx.AsyncClient(base_url=config.BACKEND_URL, timeout=10.0)
    
    dp.include_router(router)

    me = await bot.get_me()
    logger.info(f"Bot @{me.username} started, polling...")

    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    finally:
        await dp["http_client"].aclose()

if __name__ == "__main__":
    asyncio.run(main())
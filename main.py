from aiogram import Bot, Dispatcher
import logging
import asyncio
from config import TOKEN
from handlers import router



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    


if __name__ == "__main__":
    asyncio.run(main())
    

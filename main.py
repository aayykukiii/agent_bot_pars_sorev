from aiogram import Bot, Dispatcher
import logging
import asyncio
import os
from config import TOKEN
from handlers import router
from database.db import create_tables



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(TOKEN)
    dp = Dispatcher()
    if os.getenv("CREATE_TABLES_ON_STARTUP", "0") == "1":
        create_tables()

    dp.include_router(router)
    await dp.start_polling(bot)
    


if __name__ == "__main__":
    asyncio.run(main())
    

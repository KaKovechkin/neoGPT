import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.handlers.business import router
from app.database.db import init_db
#import redis.asyncio as aioredis
#from aiogram.fsm.storage.redis import RedisStorage



async def main():
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token = os.getenv('TG_TOKEN'))
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)
    
    
async def startup(dispatcher:Dispatcher):
    await init_db()
    print('Бот запущен...')
    

async def shutdown(dispatcher:Dispatcher):
    print('Бот завершил работу.')

    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен.')
    

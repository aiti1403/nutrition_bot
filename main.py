import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import common, survey, admin, payment
from database.database import create_tables

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота (замените на свой)
BOT_TOKEN = "8188855240:AAEc8nEaKcbp2mdkXXearU5ZRfujBgg9V0A"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрация роутеров
dp.include_router(common.router)
dp.include_router(survey.router)
dp.include_router(admin.router)
dp.include_router(payment.router)

async def main():
    # Создание таблиц в БД
    await create_tables()
    
    # Удаление вебхука на случай, если он был установлен
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запуск поллинга
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

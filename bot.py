import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer(f"Hello, <b>{message.from_user.full_name}</b>! This is a test bot.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# BotFather-dan aldığınız tokeni bura daxil edin
TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salam! Telegram Stars satışı botuna xoş gəlmisiniz.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

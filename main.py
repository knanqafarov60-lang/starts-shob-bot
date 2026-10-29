import asyncio
import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import LabeledPrice

# Bot tokenin (BotFather-dan aldığın əsas bot tokeni)
TOKEN = "9282671426:AAHBCW8SikhLIhSGf5ZO3W1bde_LiOKVOPU"

# Smart Glocal Test tokenimiz
PAYMENT_TOKEN = "1877036958:TEST:56cbc53299ea0c6623df291781129311413cc7a2"

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Salam! Starts Market-ə xoş gəlmisiniz. Məhsul almaq üçün /buy əmrini göndərin.")

@dp.message(Command("buy"))
async def cmd_buy(message: types.Message):
    # Apple Pay / Google Pay / Kart vasitəsilə ödəniş fakturası
    prices = [LabeledPrice(label="Test Məhsul", amount=100)] # 1.00 USD
    
    await message.answer_invoice(
        title="Starts Market Məhsulu",
        description="Apple Pay və ya kart ilə test ödənişi",
        payload="test-invoice-payload",
        provider_token=PAYMENT_TOKEN,
        currency="USD",
        prices=prices,
        start_parameter="test-payment",
    )

@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer("Təbriklər! Ödəniş uğurla tamamlandı 🎉")

# Render üçün sadə veb-server (Port tələbini ödəmək üçün)
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render-in təyin etdiyi portu oxuyur (və ya default 10000)
    import os
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    bot = Bot(token=TOKEN)
    # Veb serveri və bot polling-i eyni vaxtda işə salırıq
    await asyncio.gather(web_server(), dp.start_polling(bot))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


from aiogram import Bot, Dispatcher, types
import asyncio
from dotenv import dotenv_values

config = dotenv_values()


token = config.get('token')
admin_id = config.get('admin_id')


async def start_app(bot: Bot):
    await bot.send_message(admin_id, text='Bot started')


async def stop_app(bot: Bot):
    await bot.send_message(admin_id, text='Bot shutdown')


async def echo(msg: types.Message):
    await msg.answer(msg.text)


async def start():
    bots = Bot(token)
    dp = Dispatcher()

    dp.startup.register(start_app)
    dp.shutdown.register(start_app)

    dp.message.register(echo)

    await dp.start_polling(bots)


if __name__ == '__main__':
    asyncio.run(start())

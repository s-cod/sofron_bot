import asyncio
import logging
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from dotenv import dotenv_values

from bot.handlers.fsm import start_app, stop_app, admin, comm_start, text, echo

config = dotenv_values()

# получаем переменные среды
token = config.get('token')
admin_id = config.get('admin_id')


async def start():
    logging.basicConfig(level=logging.INFO)

    # Функция запуска бота
    bots = Bot(token)
    dp = Dispatcher()

    # раздел регистрации обработчиков
    dp.startup.register(start_app)
    dp.shutdown.register(stop_app)

    dp.message.register(admin, F.from_user.id == int(admin_id), F.text == 'Привет')
    dp.message.register(comm_start, Command(commands=['start', 'go']))
    dp.message.register(text, F.text == 'Салют')
    dp.message.register(echo)

    await dp.start_polling(bots)


if __name__ == '__main__':
    asyncio.run(start())

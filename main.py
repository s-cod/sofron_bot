import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Text, Command
from dotenv import dotenv_values

config = dotenv_values()

# получаем переменные среды
token = config.get('token')
admin_id = config.get('admin_id')

# Создаем логер
logger = logging.getLogger(__name__)


async def comm(bot: Bot):
    command = [
        types.BotCommand(command='start', description='Начало работы'),
        types.BotCommand(command='help', description='Помощь'),
    ]
    await bot.set_my_commands(command, types.BotCommandScopeDefault())


async def start_app(bot: Bot):
    # Функция выполняемая при запуске бота
    await comm(bot)
    await bot.send_message(admin_id, text='Бот запущен!')


async def stop_app(bot: Bot):
    # Функция выполняемая при остановке бота
    await bot.send_message(admin_id, text='Бот выключен!')


async def echo(msg: types.Message):
    await msg.answer(msg.text)


async def text(msg: types.Message):
    await msg.answer('Ты ввел текст: ' + msg.text)


async def comm_start(msg: types.Message):
    await msg.reply('Начинаем работать')


async def admin(msg: types.Message):
    await msg.answer('Привет, Админ!')


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
    dp.message.register(text, Text(text='Салют'))
    dp.message.register(echo)

    await dp.start_polling(bots)


if __name__ == '__main__':
    asyncio.run(start())

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    BotCommand,
    Message,
    callback_query,
    BotCommandScopeDefault,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.filters import Text, Command

from aiogram.fsm.context import FSMContext


from dotenv import dotenv_values

config = dotenv_values()


# получаем переменные среды
token = config.get('token')
admin_id = config.get('admin_id')


# Создаем логер
logger = logging.getLogger(__name__)


async def comm(bot: Bot):
    command = [
        BotCommand(command='start', description='Начало работы'),
        BotCommand(command='help', description='Помощь'),
    ]
    await bot.set_my_commands(command, BotCommandScopeDefault())


keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='Кнопка 1',
            ),
            KeyboardButton(text='Кнопка 2'),
            KeyboardButton(text='Кнопка 3'),
            KeyboardButton(text='Кнопка 4'),
            KeyboardButton(text='Кнопка 5'),
        ],
        [
            KeyboardButton(text='Убираю кнопки'),
        ],
    ],
)


async def start_app(bot: Bot):
    # Функция выполняемая при запуске бота
    await comm(bot)
    await bot.send_message(admin_id, text='Бот запущен!', reply_markup=keyboard)


async def stop_app(bot: Bot):
    # Функция выполняемая при остановке бота
    await bot.send_message(admin_id, text='Бот выключен!')


async def state_start(msg: Message, state: FSMContext):
    await msg.answer('показываю текстовые кнопки', reply_markup=keyboard)


async def text_button(msg: Message, state: FSMContext):
    await msg.answer(text='Нажата кнопка ' + msg.text)


async def dell_button(msg: Message):
    await msg.answer(text='Убираю кнопки', reply_markup=ReplyKeyboardRemove())


async def start():

    logging.basicConfig(level=logging.INFO)

    # Функция запуска бота
    bot = Bot(token)
    dp = Dispatcher()

    # раздел регистрации обработчиков
    dp.startup.register(start_app)
    dp.shutdown.register(stop_app)

    dp.message.register(text_button, Text([f'Кнопка {i+1}' for i in range(4)]))
    dp.message.register(dell_button, Text('Убираю кнопки'))
    dp.message.register(state_start, Command(commands=['start', 'go']))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())

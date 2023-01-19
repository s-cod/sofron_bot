import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    BotCommand,
    Message,
    callback_query,
    BotCommandScopeDefault,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import Text, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from dotenv import dotenv_values

config = dotenv_values()


# получаем переменные среды
token = config.get('token')
admin_id = config.get('admin_id')


# Создаем логер
logger = logging.getLogger(__name__)


class States(StatesGroup):
    first_name = State()
    last_name = State()
    telephone = State()
    complete = State()


async def comm(bot: Bot):
    command = [
        BotCommand(command='start', description='Начало работы'),
        BotCommand(command='help', description='Помощь'),
    ]
    await bot.set_my_commands(command, BotCommandScopeDefault())


async def start_app(bot: Bot):
    # Функция выполняемая при запуске бота
    await comm(bot)
    await bot.send_message(admin_id, text='Бот запущен!')


async def stop_app(bot: Bot):
    # Функция выполняемая при остановке бота
    await bot.send_message(admin_id, text='Бот выключен!')


async def state_start(msg: Message, state: FSMContext):
    await msg.answer('Введите необходимые данные. \nВведите имя ')
    await state.set_state(States.first_name)


async def state_first_name(msg: Message, state: FSMContext):
    await msg.answer('вы ввели имя: ' + msg.text + '\nВведите фамилию')

    await state.set_state(States.last_name)
    await state.update_data(first_name=msg.text)


async def state_last_name(msg: Message, state: FSMContext):
    await msg.answer('вы ввели фамилию: ' + msg.text + '\nВедите номер телефона')
    await state.set_state(States.telephone)
    await state.update_data(last_name=msg.text)


async def state_telephone(msg: Message, state: FSMContext):
    await msg.answer('вы ввели телефон: ' + msg.text)
    await state.set_state(States.complete)
    await state.update_data(telephone=msg.text)
    data = await state.get_data()
    await msg.answer(
        "Введенные данные:\n"
        f"Имя: {data['first_name']}\n"
        f"Фамилия: {data['last_name']}\n"
        f"Телефон: {data['telephone']}\n"
        'Подтвердите данные!',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Подтвердить', callback_data='confirm'),
                    InlineKeyboardButton(text='Отменить', callback_data='cancel'),
                ],
                [
                    InlineKeyboardButton(text='Перейти на сайт', url='mail.ru'),
                ],
            ]
        ),
    )


async def confirm(call: callback_query.CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id, reply_markup=None
    )
    # await call.answer('Данные приняты')
    # await bot.send_message(call.message.chat.id, 'Данные приняты')
    await bot.answer_callback_query(call.id, 'Данные подтверждены', show_alert=True)

    await state.clear()


async def cancel(call: callback_query.CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(
        call.message.chat.id, call.message.message_id, reply_markup=None
    )
    await bot.answer_callback_query(call.id, 'Отмена данных', show_alert=True)
    # await call.answer('Данные отклонены')
    await state.clear()


async def start():

    logging.basicConfig(level=logging.INFO)

    # Функция запуска бота
    bots = Bot(token)
    dp = Dispatcher()

    # раздел регистрации обработчиков
    dp.startup.register(start_app)
    dp.shutdown.register(stop_app)

    dp.message.register(cancel, Text(text='cancel', ignore_case=True))
    dp.message.register(state_start, Command(commands=['start', 'go']))
    dp.message.register(state_first_name, States.first_name)
    dp.message.register(state_last_name, States.last_name)
    dp.message.register(state_telephone, States.telephone)
    dp.callback_query.register(cancel, States.complete, F.data == 'cancel')
    dp.callback_query.register(confirm, States.complete, F.data == 'confirm')

    await dp.start_polling(bots)


if __name__ == '__main__':
    asyncio.run(start())

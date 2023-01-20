from aiogram import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, callback_query, BotCommandScopeDefault, BotCommand
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import kb_confirm
from dotenv import dotenv_values

config = dotenv_values()


# получаем переменные среды
token = config.get('token')
admin_id = config.get('admin_id')


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
        reply_markup=kb_confirm,
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


async def admin(msg: Message):
    await msg.answer('Привет, Админ!')


async def echo(msg: Message):
    await msg.answer(msg.text)


async def text(msg: Message):
    await msg.answer('Ты ввел текст: ' + msg.text)


async def comm_start(msg: Message):
    await msg.reply('Начинаем работать')

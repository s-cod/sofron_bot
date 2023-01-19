import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
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


async def state_start(msg: types.Message, state: FSMContext):
    await msg.answer('Введите необходимые данные. \nВведите имя ')
    await state.set_state(States.first_name)


async def state_first_name(msg: types.Message, state: FSMContext):
    await msg.answer('вы ввели имя: ' + msg.text + '\nВведите фамилию')

    await state.set_state(States.last_name)
    await state.update_data(first_name=msg.text)


async def state_last_name(msg: types.Message, state: FSMContext):
    await msg.answer('вы ввели фамилию: ' + msg.text + '\nВедите номер телефона')
    await state.set_state(States.telephone)
    await state.update_data(last_name=msg.text)


async def state_telephone(msg: types.Message, state: FSMContext):
    await msg.answer('вы ввели телефон: ' + msg.text)
    await state.set_state(States.complete)
    await state.update_data(telephone=msg.text)
    data = await state.get_data()
    await msg.answer(
        "Введенные данные:\n"
        f"Имя: {data['first_name']}\n"
        f"Фамилия: {data['last_name']}\n"
        f"Телефон: {data['telephone']}\n"
        'Проверьте данные и введите finish для завершения\nили cancel для отмены!'
    )


async def state_complete(msg: types.Message, state: FSMContext):
    await msg.answer('Данные приняты')

    await state.clear()


async def state_cancel(msg: types.Message, state: FSMContext):
    await msg.answer('Данные отклонены')
    await state.clear()


async def start():

    logging.basicConfig(level=logging.INFO)

    # Функция запуска бота
    bots = Bot(token)
    dp = Dispatcher()

    # раздел регистрации обработчиков
    dp.startup.register(start_app)
    dp.shutdown.register(stop_app)

    dp.message.register(state_cancel, Text(text='cancel', ignore_case=True))
    dp.message.register(state_start, Command(commands=['start', 'go']))
    dp.message.register(state_first_name, States.first_name)
    dp.message.register(state_last_name, States.last_name)
    dp.message.register(state_telephone, States.telephone)
    dp.message.register(state_complete, States.complete, Text(text='finish', ignore_case=True))

    await dp.start_polling(bots)


if __name__ == '__main__':
    asyncio.run(start())

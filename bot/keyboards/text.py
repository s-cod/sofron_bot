from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


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

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


kb_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить', callback_data='confirm'),
            InlineKeyboardButton(text='Отменить', callback_data='cancel'),
        ],
        [
            InlineKeyboardButton(text='Перейти на сайт', url='mail.ru'),
        ],
    ]
)

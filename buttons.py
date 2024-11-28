from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_example_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Создание бота", callback_data="example_create_bot"),
        InlineKeyboardButton("CallbackQuery", callback_data="example_callback"),
        InlineKeyboardButton("Middleware", callback_data="example_middleware"),
    )
    return keyboard

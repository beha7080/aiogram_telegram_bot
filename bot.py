import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from state import *
from buttons import *

TELEGRAM_TOKEN = "7428826678:AAGEX0_5eCKhxX9lLvVmPQlu2zr_txfb29w"
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(
        "Добро пожаловать в бот документации Aiogram 2.25.1! 🛠️\n"
        "Доступные команды:\n"
        "/docs - Общая документация\n"
        "/examples - Примеры кода\n"
        "/faq - Часто задаваемые вопросы\n"
        "/search <запрос> - Поиск в документации"
    )

@dp.message_handler(commands=["docs"])
async def send_docs(message: types.Message):
    await message.reply("Официальная документация: https://docs.aiogram.dev/en/2.25.1/")

@dp.message_handler(commands=["examples"])
async def send_examples(message: types.Message):
    await message.reply("Выберите пример, чтобы увидеть код:", reply_markup=get_example_buttons())

@dp.callback_query_handler(lambda c: c.data.startswith("example_"))
async def handle_examples(callback_query: types.CallbackQuery):
    examples = {
        "example_create_bot": "Пример создания бота:\n\n"
                              "```python\n"
                              "from aiogram import Bot, Dispatcher\n\n"
                              "bot = Bot(token='YOUR_TOKEN')\n"
                              "dp = Dispatcher(bot)\n"
                              "```",
        "example_callback": "Пример обработки CallbackQuery:\n\n"
                            "```python\n"
                            "@dp.callback_query_handler(lambda c: c.data == 'button_click')\n"
                            "async def process_callback(callback_query: types.CallbackQuery):\n"
                            "    await bot.answer_callback_query(callback_query.id)\n"
                            "    await callback_query.message.reply('Кнопка нажата!')\n"
                            "```",
        "example_middleware": "Пример использования Middleware:\n\n"
                              "```python\n"
                              "from aiogram.dispatcher.middlewares import BaseMiddleware\n\n"
                              "class ExampleMiddleware(BaseMiddleware):\n"
                              "    async def on_pre_process_update(self, update, data):\n"
                              "        print('Middleware сработал!')\n\n"
                              "dp.middleware.setup(ExampleMiddleware())\n"
                              "```",
    }
    code = examples.get(callback_query.data)
    if code:
        await callback_query.message.reply(code, parse_mode="Markdown")
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(commands=["faq"])
async def send_faq(message: types.Message):
    await message.reply(
        "Часто задаваемые вопросы:\n"
        "1. **Как установить Aiogram?**\n"
        "   ```bash\n"
        "   pip install aiogram==2.25.1\n"
        "   ```\n"
        "2. **Где найти документацию?**\n"
        "   [Документация](https://docs.aiogram.dev/en/2.25.1/)\n"
        "3. **Какие версии Python поддерживаются?**\n"
        "   Aiogram 2.25.1 поддерживает Python 3.7+."
    )

@dp.message_handler(commands=["search"])
async def search_docs(message: types.Message):
    query = message.get_args()
    if not query:
        await message.reply("Пожалуйста, введите запрос, например:\n/search Dispatcher")
        return
    search_url = f"https://docs.aiogram.dev/en/2.25.1/search.html?q={query}"
    await message.reply(f"Результаты поиска для '{query}':\n{search_url}")

@dp.message_handler(commands='start', state='*')
async def start_form(message: types.Message):
    await Form.name.set()
    await message.reply("Как тебя зовут?")

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("Сколько тебе лет?")

@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await message.reply(f"Тебя зовут {data['name']} и тебе {data['age']} лет!")
    await state.finish()

@dp.errors_handler()
async def error_handler(update, exception):
    logging.error(f"Error: {exception}")
    return True

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("Вот список доступных команд:\n"
                         "/start - Начать\n"
                         "/docs - Документация\n"
                         "/examples - Примеры\n"
                         "/faq - Часто задаваемые вопросы\n"
                         "/search - Поиск в документации\n"
                         "/help - Помощь")

@dp.message_handler(commands=["contact"])
async def contact_command(message: types.Message):
    await message.reply("Для связи с нами, пожалуйста, напишите на email: support@aiogram.com")

@dp.message_handler(commands=["version"])
async def version_command(message: types.Message):
    await message.reply("Вы используете Aiogram версии 2.25.1")

@dp.message_handler(commands=["info"])
async def info_command(message: types.Message):
    await message.reply("Это бот для получения информации о библиотеке Aiogram. Напишите /help для получения списка команд.")

@dp.message_handler(commands=["news"])
async def news_command(message: types.Message):
    await message.reply("Новостей пока нет, следите за обновлениями на официальном сайте.")

@dp.message_handler(commands=["changelog"])
async def changelog_command(message: types.Message):
    await message.reply("Изменения в версии 2.25.1:\n- Улучшенная производительность\n- Исправления багов\n- Обновления документации")

@dp.message_handler(commands=["tutorial"])
async def tutorial_command(message: types.Message):
    await message.reply("Посмотрите наш обучающий курс по Aiogram: https://docs.aiogram.dev/en/2.25.1/tutorial/")

@dp.message_handler(commands=["community"])
async def community_command(message: types.Message):
    await message.reply("Присоединяйтесь к нашему сообществу на GitHub и Discord!\n"
                         "GitHub: https://github.com/aiogram/aiogram\n"
                         "Discord: https://discord.gg/aiogram")

@dp.message_handler(commands=["donate"])
async def donate_command(message: types.Message):
    await message.reply("Поддержите проект Aiogram, сделав пожертвование: https://aiogram.dev/donate")

@dp.message_handler(commands=["feedback"])
async def feedback_command(message: types.Message):
    await message.reply("Мы ценим ваш отзыв! Пожалуйста, оставьте его на нашем GitHub или напишите на email.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

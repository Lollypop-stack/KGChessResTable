from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import asyncio

BOT_TOKEN = "7682601122:AAGwXpVtCYdg4xYU4t-h2Yl_l2o5NKvqgbA"
API_TOKEN = "lip_tmvRHokFcmSpLTPn27II"

# Параметры для создания турнира
TOURNAMENT_PARAMS = {
    "name": "Классический учебный турнир",
    "clockTime": 5,  # Уменьшили время на партию до 5 минут
    "clockIncrement": 0,
    "minutes": 20,  # Увеличили продолжительность турнира до 60 минут
    "waitMinutes": 5,
    "variant": "standard",
    "rated": True,
    "berserkable": True,
    "streakable": True,
    "description": "Присоединяйтесь к нашему классическому турниру!",
}

async def create_tournament():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    print("Отправляемый запрос:", TOURNAMENT_PARAMS)
    print("Заголовки запроса:", headers)

    async with aiohttp.ClientSession() as session:
        async with session.post("https://lichess.org/api/tournament", json=TOURNAMENT_PARAMS,
                                headers=headers) as response:
            if response.status == 200:
                tournament_data = await response.json()
                print("Ответ от сервера:", tournament_data)
                tournament_url = f"https://lichess.org/tournament/{tournament_data['id']}"
                return f"Турнир создан! Ссылка: {tournament_url}"
            else:
                error_data = await response.text()
                print(f"Ошибка: {response.status}, {error_data}")
                return f"Ошибка при создании турнира: {response.status}, {error_data}"

# Обработчик команды /start
async def on_top(message: types.Message):
    message_text = "Выберите топ:\n"
    categories = [
        ("ТОП 20 по стандарту среди мужчин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=M"),
        ("ТОП 20 по рапиду среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=M&age1=0&age2=0"),
        ("ТОП 20 по блицу среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=M&age1=0&age2=0"),
        ("ТОП 20 по стандарту среди женщин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=F"),
        ("ТОП 20 по рапиду среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=F&age1=0&age2=0"),
        ("ТОП 20 по блицу среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=F&age1=0&age2=0"),
        ("ТОП 20 по стандарту среди юниоров до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=0&age2=20"),
    ]
    for category, url in categories:
        message_text += f"[{category}]({url})\n"
    await message.answer(message_text, parse_mode='Markdown')

# Обработчик команды /create_tournament
async def on_create_tournament(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать турнир", callback_data="create_tournament")]
    ])
    await message.answer("Нажмите кнопку ниже, чтобы создать турнир:", reply_markup=keyboard)

# Обработчик callback-запросов
async def on_callback_query(callback_query: types.CallbackQuery):
    if callback_query.data == "create_tournament":
        result = await create_tournament()
        await callback_query.message.answer(result)
        await callback_query.answer()

# Основная функция запуска
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем обработчики
    dp.message.register(on_top, Command("top"))
    dp.message.register(on_create_tournament, Command("cr_t"))
    dp.callback_query.register(on_callback_query)

    # Запуск бота
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
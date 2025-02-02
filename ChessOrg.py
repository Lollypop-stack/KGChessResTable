from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
import asyncio
import time

BOT_TOKEN = "7682601122:AAGwXpVtCYdg4xYU4t-h2Yl_l2o5NKvqgbA"
API_TOKEN = "lip_Fu5PnnS0CRde5QIz3ZRc"

# Текущее время для старта турнира (например, через 5 минут)
start_time = int((time.time() + 300) * 1000)  # Время начала в миллисекундах
end_time = start_time + 60 * 60 * 1000  # Время окончания через 1 час

# Параметры для создания турнира
TOURNAMENT_PARAMS = {
    "clockTime": 1,  # Время на партию в минутах (1 минута)
    "minutes": 20,
    "clockIncrement": 0,  # Без прибавления времени
    "rated": True,  # Рейтинговый турнир
    "variant": "standard",  # Стандартная игра
    "name": "Быстрый учебный турнир",  # Имя турнира
    "nbPlayers": 38,  # Количество игроков
    "startsAt": start_time,  # Время начала турнира в миллисекундах
    "finishesAt": end_time,  # Время окончания турнира в миллисекундах
    "status": 10,  # Статус турнира (например, активен)
    "perf": {"key": "bullet", "name": "Пуля"},  # Тип игры: "bullet"
    "maxRating": 2000,  # Максимальный рейтинг игроков
    "minRatedGames": 20,  # Минимальное количество рейтинговых игр
    "schedule": {"freq": "hourly", "speed": "bullet"},  # Частота турниров и скорость игры
}

# Категории для получения ТОП-20 игроков
categories = [
    ("ТОП 20 по стандарту среди мужчин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=M"),
    ("ТОП 20 по рапиду среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=M&age1=0&age2=0"),
    ("ТОП 20 по блицу среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=M&age1=0&age2=0"),
    ("ТОП 20 по стандарту среди женщин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=F"),
    ("ТОП 20 по рапиду среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=F&age1=0&age2=0"),
    ("ТОП 20 по блицу среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=F&age1=0&age2=0"),
    ("ТОП 20 по стандарту среди юниоров до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=0&age2=20"),
]

# Функция для создания турнира
async def create_tournament():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://lichess.org/api/tournament", json=TOURNAMENT_PARAMS,
                                headers=headers) as response:
            if response.status == 200:
                tournament_data = await response.json()
                tournament_url = tournament_data.get('url', None)
                if tournament_url:
                    return f"Турнир создан! Ссылка: {tournament_url}"
                else:
                    return "Ошибка: Ссылка на турнир не получена."
            else:
                error_data = await response.text()  # Получаем текст ошибки
                return f"Ошибка при создании турнира: {response.status}, {error_data}"

# Обработчик команды /start
async def on_top(message: types.Message):
    # Отправляем сообщение с текстовыми ссылками
    message_text = "Выберите топ:\n"
    for category, url in categories:
        message_text += f"[{category}]({url})\n"

    await message.answer(message_text, parse_mode='Markdown')

# Обработчик команды /create_tournament
async def on_create_tournament(message: types.Message):
    result = await create_tournament()
    await message.answer(result)

# Основная функция запуска
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем обработчики
    dp.message.register(on_top, Command("top"))
    dp.message.register(on_create_tournament, Command("cr_t"))

    # Запуск бота
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())

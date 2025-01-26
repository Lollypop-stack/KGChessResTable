# import aiohttp
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command
# import asyncio
# from bs4 import BeautifulSoup
#
# BOT_TOKEN = "7682601122:AAGwXpVtCYdg4xYU4t-h2Yl_l2o5NKvqgbA"
#
# categories = [
#     ("ТОП 20 по стандарту среди мужчин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=M"),
#     ("ТОП 20 по рапиду среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=M&age1=0&age2=0"),
#     ("ТОП 20 по блицу среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=M&age1=0&age2=0"),
#     ("ТОП 20 по стандарту среди женщин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=F"),
#     ("ТОП 20 по рапиду среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=F&age1=0&age2=0"),
#     ("ТОП 20 по блицу среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=F&age1=0&age2=0"),
#     ("ТОП 20 по стандарту среди юниоров до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=0&age2=20"),
# ]
#
# async def get_top_20(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             html = await response.text()
#             soup = BeautifulSoup(html, "html.parser")
#
#     players = []
#
#     # Ищем все строки таблицы (кроме заголовков)
#     rows = soup.select('table tbody tr')
#
#     for row in rows:
#         # Извлекаем данные из ячеек
#         place = row.select_one('td').get_text(strip=True)
#         name = row.select_one('td a').get_text(strip=True)
#         rating = row.select('td')[4].get_text(strip=True)
#         year_of_birth = row.select('td')[5].get_text(strip=True)
#
#         players.append(f"{place}: {name}, {rating}, {year_of_birth}")
#
#     return "\n".join(players) if players else "Игроки не найдены."
#
#
# async def on_start(message: types.Message):
#     # Создание сообщений с ссылками на ТОП 20 категории
#     response_message = "Выберите топ:\n"
#     for category, url in categories:
#         response_message += f"{category}: [ссылка]({url})\n"
#
#     await message.answer(response_message, parse_mode='Markdown')
#
#
# async def on_category(message: types.Message):
#     # Получаем URL, соответствующий выбранной категории
#     category = message.text
#     for cat, url in categories:
#         if cat == category:
#             players = await get_top_20(url)
#             await message.answer(players)
#             await message.answer(f"Для более подробной информации перейдите по [ссылке]({url})", parse_mode='Markdown')
#
#
# async def main():
#     bot = Bot(token=BOT_TOKEN)
#     dp = Dispatcher()  # Создаем диспетчер без передачи бота на этом этапе
#
#     # Регистрируем обработчики
#     dp.message.register(on_start, Command("start"))
#     dp.message.register(on_category, lambda message: message.text in [cat[0] for cat in categories])
#
#     try:
#         await dp.start_polling(bot)  # Передаем объект bot при запуске polling
#     except asyncio.CancelledError:
#         print("Задача была отменена.")
#     except KeyboardInterrupt:
#         print("Программа была прервана вручную.")
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from bs4 import BeautifulSoup
import aiohttp

BOT_TOKEN = "7682601122:AAGwXpVtCYdg4xYU4t-h2Yl_l2o5NKvqgbA"

categories = [
    ("ТОП 20 по стандарту среди мужчин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=M"),
    ("ТОП 20 по рапиду среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=M&age1=0&age2=0"),
    ("ТОП 20 по блицу среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=M&age1=0&age2=0"),
    ("ТОП 20 по стандарту среди женщин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=F"),
    ("ТОП 20 по рапиду среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=F&age1=0&age2=0"),
    ("ТОП 20 по блицу среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=F&age1=0&age2=0"),
    ("ТОП 20 по стандарту среди юниоров до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=0&age2=20"),
]

async def get_top_20(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

    players = []

    # Ищем все строки таблицы (кроме заголовков)
    rows = soup.select('table tbody tr')

    for row in rows:
        # Извлекаем данные из ячеек
        place = row.select_one('td').get_text(strip=True)
        name = row.select_one('td a').get_text(strip=True)
        rating = row.select('td')[4].get_text(strip=True)
        year_of_birth = row.select('td')[5].get_text(strip=True)

        players.append(f"{place}: {name}, {rating}, {year_of_birth}")

    return "\n".join(players) if players else "Игроки не найдены."


async def on_start(message: types.Message):
    # Отправляем сообщение с текстовыми ссылками
    message_text = "Выберите топ:\n"
    for category, url in categories:
        message_text += f"[{category}]({url})\n"

    await message.answer(message_text, parse_mode='Markdown')


async def on_category(message: types.Message):
    category = message.text.strip()
    for cat, url in categories:
        if cat == category:
            players = await get_top_20(url)
            await message.answer(players)
            await message.answer(f"Для более подробной информации перейдите по [ссылке]({url})", parse_mode='Markdown')


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем обработчики
    dp.message.register(on_start, Command("start"))
    dp.message.register(on_category)

    await dp.start_polling(bot)  # Запуск polling


if __name__ == "__main__":
    asyncio.run(main())



import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

# Токен Telegram-бота
BOT_TOKEN = "7682601122:AAGwXpVtCYdg4xYU4t-h2Yl_l2o5NKvqgbA"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    instructions = (
        "Привет! Этот бот показывает шахматные рейтинги игроков из Кыргызстана.\n"
        "Выбери интересующую категорию:\n\n"
    )

    categories = [
        ("ТОП 20 по стандарту среди мужчин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=M"),
        ("ТОП 20 по рапиду среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=M&age1=0&age2=0"),
        ("ТОП 20 по блицу среди мужчин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=M&age1=0&age2=0"),
        ("ТОП 20 по стандарту среди женщин", "https://ratings.fide.com/rankings.phtml?country=KGZ&gender=F"),
        ("ТОП 20 по рапиду среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=F&age1=0&age2=0"),
        ("ТОП 20 по блицу среди женщин", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=F&age1=0&age2=0"),
        ("ТОП 20 по стандарту среди юниоров до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=0&age2=20"),
        ("ТОП 20 по рапиду среди юниоров до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender=M&age1=0&age2=20"),
        ("ТОП 20 по блицу среди юниоров до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=M&age1=0&age2=20"),
        ("ТОП 20 по стандарту среди юниорок до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=F&age1=0&age2=20"),
        ("ТОП 20 по рапиду среди юниорок до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=rapid&gender==F&age1=0&age2=20"),
        ("ТОП 20 по блицу среди юниорок до 20 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=blitz&gender=F&age1=0&age2=20"),
        ("ТОП 20 по стандарту среди сеньоров 50-64 лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=50&age2=64"),
        ("ТОП 20 по стандарту среди сеньоров 65+ лет", "https://ratings.fide.com/rankings.phtml?continent=0&country=KGZ&rating=standard&gender=M&age1=65&age2=0"),
    ]

    for text, url in categories:
        instructions += f"{text}: [ссылка]({url})\n"

    # await message.answer(instructions, parse_mode="Markdown")


# Основная точка входа
async def main():
    try:
        # Здесь предполагается, что bot и dp уже настроены
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Задача была отменена.")
    except KeyboardInterrupt:
        print("Программа была прервана вручную.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if  __name__ == "__main__":
    asyncio.run(main())
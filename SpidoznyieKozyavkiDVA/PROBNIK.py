from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiohttp
import asyncio

BOT_TOKEN = "7682601122:AAGwXpVtCYdg4xYU4t-h2Yl_l2o5NKvqgbA"
API_TOKEN = "lip_Fu5PnnS0CRde5QIz3ZRc"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для получения активных матчей
async def get_active_games():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = "https://lichess.org/api/account/playing"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("nowPlaying", [])
            else:
                print(f"Ошибка при получении активных матчей: {response.status}")
                return []

# Функция для завершения матча
async def finish_game(game_id: str):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = f"https://lichess.org/api/bot/game/{game_id}/resign"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return True
            else:
                print(f"Ошибка при завершении матча {game_id}: {response.status}")
                return False

# Функция для получения активных турниров
async def get_active_tournaments():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = "https://lichess.org/api/tournament/created"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Ошибка при получении активных турниров: {response.status}")
                return []

# Функция для завершения турнира
async def finish_tournament(tournament_id: str):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    url = f"https://lichess.org/api/tournament/{tournament_id}/finish"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                return True
            else:
                print(f"Ошибка при завершении турнира {tournament_id}: {response.status}")
                return False

# Обработчик команды /active_m
async def on_active_matches(message: types.Message):
    # Получаем активные матчи
    active_games = await get_active_games()
    # Получаем активные турниры
    active_tournaments = await get_active_tournaments()

    response_message = ""

    if not active_games and not active_tournaments:
        response_message = "Нет турниров."
    else:
        if active_tournaments:
            response_message += "\nАктивные турниры:\n"
            for tournament in active_tournaments:
                tournament_id = tournament.get("id")
                tournament_name = tournament.get("fullName", "Без названия")
                response_message += f"- Турнир ID: {tournament_id}, Название: {tournament_name}\n"

    await message.answer(response_message)

# Обработчик команды /stop_m
async def on_stop_matches(message: types.Message):
    # Завершаем активные матчи
    active_games = await get_active_games()
    if active_games:
        for game in active_games:
            game_id = game.get("gameId")
            success = await finish_game(game_id)
            if success:
                await message.answer(f"Матч {game_id} завершен.")
            else:
                await message.answer(f"Не удалось завершить матч {game_id}.")
    else:
        await message.answer("Нет активных матчей для завершения.")

    # Завершаем активные турниры
    active_tournaments = await get_active_tournaments()
    if active_tournaments:
        for tournament in active_tournaments:
            tournament_id = tournament.get("id")
            success = await finish_tournament(tournament_id)
            if success:
                await message.answer(f"Турнир {tournament_id} завершен.")
            else:
                await message.answer(f"Не удалось завершить турнир {tournament_id}.")
    else:
        await message.answer("Нет активных турниров для завершения.")

# Регистрация обработчиков
dp.message.register(on_active_matches, Command("active_m"))
dp.message.register(on_stop_matches, Command("stop_m"))

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
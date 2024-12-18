import logging
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

API_TOKEN = '7871114248:AAHpOr0l7R53OPjhYmvrXFa4xuUdnlsE7rQ'
GIPHY_API_KEY = 'RRy1KkwxuJstmfU8DSdsFNnNEXCkHqKD'
JOKE_API_URL = 'https://v2.jokeapi.dev/joke/Any?type=single'  # API для шуток
GIPHY_API_URL = f'https://api.giphy.com/v1/gifs/random?tag=funny&api_key={GIPHY_API_KEY}'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для получения случайной шутки
def get_joke():
    response = requests.get(JOKE_API_URL)
    joke_data = response.json()
    return joke_data.get('joke', 'Шутка не найдена.')

# Функция для получения случайного GIF
def get_gif():
    response = requests.get(GIPHY_API_URL)
    gif_data = response.json()
    if 'data' in gif_data and 'images' in gif_data['data']:
        gif_url = gif_data['data']['images']['original']['url']
        return gif_url
    return ''

# Команда для приветствия
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я могу присылать тебе шутки и GIF-ки. Используй /joke или /gif.")

# Команда для отправки шутки
@dp.message(Command("joke"))
async def send_joke(message: Message):
    joke = get_joke()
    await message.answer(joke)

# Команда для отправки GIF
@dp.message(Command("gif"))
async def send_gif(message: Message):
    # Отображение индикатора загрузки
    await bot.send_chat_action(chat_id=message.chat.id, action="upload_document")

    gif_url = get_gif()
    if gif_url:
        await message.answer_animation(gif_url)
    else:
        await message.answer("Извините, я не смог найти GIF.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

import os
import random
import requests
import time
from dotenv import load_dotenv
from twitchio.ext import commands

# Загружаем переменные окружения
load_dotenv('fox.env')

# Конфигурация Twitch API и бота
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_OAUTH_TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
TWITCH_BOT_USERNAME = os.getenv('TWITCH_BOT_USERNAME')
TWITCH_CHANNEL = "Dyadushka_Fox"  # Имя канала

# Список вопросов для чата
questions = [
    "Какой твой любимый жанр игр?",
    "Что думаешь о последних обновлениях в игре?",
    "Какую игру ты планируешь пройти в ближайшее время?",
]

# Основной класс бота
class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=TWITCH_OAUTH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL]
        )

    async def event_ready(self):
        print(f'Bot {TWITCH_BOT_USERNAME} is online and ready to chat!')
        await self.send_random_question()

    async def send_random_question(self):
        while True:
            question = random.choice(questions)
            await self.connected_channels[0].send(question)
            await self.wait_for_ready()
            await asyncio.sleep(1800)  # Отправляет вопрос каждые 30 минут

    async def event_message(self, message):
        print(f'{message.author.name}: {message.content}')
        await self.handle_commands(message)


# Функция для запуска бота
def run_bot():
    bot = TwitchBot()
    bot.run()


if __name__ == '__main__':
    run_bot()

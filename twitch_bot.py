import time
import requests
import os
import random
from dotenv import load_dotenv
from twitchio import Client, Message

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
    "Какие твои любимые игры в жанре RPG?",
    "Кто твой любимый персонаж в играх?",
    "Какую игру ты считаешь самой сложной?",
    "Какие стримы ты обычно смотришь на Twitch?",
    "Какие игры ты больше всего ждешь в следующем году?",
    "Что ты думаешь о VR-играх?",
    "Какую игру ты бы порекомендовал друзьям?",
    # Добавьте остальные вопросы
]

# Функция для проверки, идет ли стрим
def check_stream_status():
    url = f'https://api.twitch.tv/helix/streams?user_login={TWITCH_CHANNEL}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_OAUTH_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if data['data']:
        return True  # Стрим идет
    return False  # Стрим не идет

# Основной класс бота
class TwitchBot(Client):

    def __init__(self):
        super().__init__(token=TWITCH_OAUTH_TOKEN)

    async def event_ready(self):
        print(f'Bot {TWITCH_BOT_USERNAME} is online and ready to chat!')
        
        # Пока стрим не начнется, ждем его
        while not check_stream_status():  
            print("Stream is offline. Waiting for stream to go live...")
            time.sleep(60)  # Проверяем каждую минуту

        print("Stream is live! Starting bot...")
        await self.send_random_question()

    async def send_random_question(self):
        # Выбираем случайный вопрос
        question = random.choice(questions)
        await self.channel.send(question)

    async def event_message(self, message: Message):
        # Ожидаем сообщений и реагируем
        print(f'{message.author.name}: {message.content}')

# Функция для запуска бота
def run_bot():
    bot = TwitchBot()
    bot.run()

if __name__ == '__main__':
    run_bot()

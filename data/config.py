import os
from dotenv import load_dotenv

load_dotenv()

# Админы бота
admins = [
    33180657,
    12345678,
    87654321
]

# База данных для хранения пользователей и уведомлений
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
POSTGRES_USER = str(os.getenv("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
POSTGRES_DATABASE = str(os.getenv("POSTGRES_DB"))
POSTGRES_HOST = str(os.getenv("POSTGRES_HOST"))
POSTGRES_PORT = str(os.getenv("POSTGRES_PORT"))
POSTGRES_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

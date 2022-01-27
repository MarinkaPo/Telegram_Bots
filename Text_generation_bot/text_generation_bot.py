from func_generate_text import generate_text
from telegram_bot_api_token import API_TOKEN # API-токен бота

# -------------------- Imports --------------------
# import numpy as np
# import pandas as pd
# import re
# import random
# import transformers
# import textwrap
import torch
from tqdm.notebook import tqdm # прогресс-бар


import logging # чтобы следить, как всё работает
from aiogram import Bot, Dispatcher, executor, types  # 4 класса для тг-бота

# -------------------- Loading model --------------------
from transformers import GPT2Tokenizer # загружаем модель
# или .... !!!!

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# -------------------- Configure logging --------------------
logging.basicConfig(level=logging.INFO)

# -------------------- Initialize bot and dispatcher ------------------------
bot = Bot(token=API_TOKEN) # задаём бота
dp = Dispatcher(bot) # задаём диспетчера


@dp.message_handler(commands=['start', 'help']) # декоратор, общая функция
async def send_welcome(message: types.Message): # её корректируем своей функцией
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Здравствуй, друг!\nОтправляемся в Петушки с минуты на минуту!\nНапиши пару слов.")


@dp.message_handler()
async def echo(message: types.Message):

    my_out = generate_text(message['text'])

    await message.answer(my_out)


if __name__ == '__main__': # обязательнод для выполнения бота
    executor.start_polling(dp, skip_updates=True) # "выполняльщик" :)